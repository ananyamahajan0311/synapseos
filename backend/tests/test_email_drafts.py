
import sys
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))

import database
import models
import services.email_drafts as email_drafts


@pytest.fixture
def test_db(monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    models.Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    monkeypatch.setattr(email_drafts, "SessionLocal", TestingSessionLocal)

    yield TestingSessionLocal
    engine.dispose()


def test_draft_persists_in_database(test_db):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Test subject",
        "Test body",
    )

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )
        assert saved is not None
        assert saved.recipient == "test@example.com"
        assert saved.subject == "Test subject"
        assert saved.body == "Test body"
        assert saved.status == "pending"
    finally:
        db.close()


def test_recovery_marks_interrupted_send_uncertain(test_db):
    now = datetime.now(timezone.utc)
    db = test_db()
    try:
        db.add(
            models.EmailDraft(
                draft_id="interrupted-test",
                recipient="test@example.com",
                subject="Test",
                body="Test body",
                status="sending",
                created_at=now,
                expires_at=now + timedelta(minutes=15),
                updated_at=now,
            )
        )
        db.commit()
    finally:
        db.close()

    recovered = email_drafts.recover_incomplete_sends()

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id="interrupted-test")
            .first()
        )
        assert recovered == 1
        assert saved.status == "send_uncertain"
    finally:
        db.close()


def test_invalid_recipient_never_calls_gmail(test_db, monkeypatch):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Test subject",
        "Test body",
    )

    def unexpected_send(*args, **kwargs):
        pytest.fail("Gmail must not be called for an invalid recipient")

    monkeypatch.setattr(email_drafts, "send_email", unexpected_send)

    result = email_drafts.send_approved_draft(
        draft["draft_id"],
        "not-an-email",
        "Test subject",
        "Test body",
    )

    assert result["status"] == "error"
    assert "valid email" in result["message"].lower()


def test_gmail_exception_marks_send_uncertain(test_db, monkeypatch):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Test subject",
        "Test body",
    )

    def simulated_gmail_failure(*args, **kwargs):
        raise TimeoutError("Simulated timeout")

    monkeypatch.setattr(
        email_drafts,
        "send_email",
        simulated_gmail_failure,
    )

    result = email_drafts.send_approved_draft(
        draft["draft_id"],
        "test@example.com",
        "Test subject",
        "Test body",
    )

    assert result["status"] == "error"

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )
        assert saved.status == "send_uncertain"
    finally:
        db.close()

def test_modified_content_is_rejected_before_gmail(test_db, monkeypatch):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Original subject",
        "Original body",
    )

    def unexpected_send(*args, **kwargs):
        pytest.fail("Gmail must not be called for modified content")

    monkeypatch.setattr(email_drafts, "send_email", unexpected_send)

    result = email_drafts.send_approved_draft(
        draft["draft_id"],
        "attacker@example.com",
        "Changed subject",
        "Changed body",
    )

    assert result["status"] == "error"
    assert "match" in result["message"].lower()

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )
        assert saved.status == "pending"
        assert saved.recipient == "test@example.com"
        assert saved.subject == "Original subject"
        assert saved.body == "Original body"
    finally:
        db.close()


def test_second_send_request_cannot_claim_same_draft(test_db, monkeypatch):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Test subject",
        "Test body",
    )

    calls = []

    def simulated_gmail(to, subject, body):
        calls.append((to, subject, body))
        return {
            "status": "success",
            "message": "Email sent",
            "message_id": "mock-message-id",
        }

    monkeypatch.setattr(email_drafts, "send_email", simulated_gmail)

    first = email_drafts.send_approved_draft(
        draft["draft_id"],
        "test@example.com",
        "Test subject",
        "Test body",
    )

    second = email_drafts.send_approved_draft(
        draft["draft_id"],
        "test@example.com",
        "Test subject",
        "Test body",
    )

    assert first["status"] == "success"
    assert second["status"] == "error"
    assert len(calls) == 1

def test_update_draft_persists_edited_content(test_db):
    draft = email_drafts.create_draft(
        "original@example.com",
        "Original subject",
        "Original body",
    )

    result = email_drafts.update_draft(
        draft["draft_id"],
        "updated@example.com",
        "Updated subject",
        "Updated body",
    )

    assert result["status"] == "success"

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )

        assert saved.recipient == "updated@example.com"
        assert saved.subject == "Updated subject"
        assert saved.body == "Updated body"
        assert saved.status == "pending"
    finally:
        db.close()


def test_update_draft_rejects_invalid_recipient(test_db):
    draft = email_drafts.create_draft(
        "original@example.com",
        "Original subject",
        "Original body",
    )

    result = email_drafts.update_draft(
        draft["draft_id"],
        "invalid-email",
        "Updated subject",
        "Updated body",
    )

    assert result["status"] == "error"

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )

        assert saved.recipient == "original@example.com"
        assert saved.subject == "Original subject"
        assert saved.body == "Original body"
    finally:
        db.close()


@pytest.mark.parametrize("status", ["cancelled", "sent", "send_uncertain"])
def test_update_draft_rejects_non_pending_status(test_db, status):
    draft = email_drafts.create_draft(
        "original@example.com",
        "Original subject",
        "Original body",
    )

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )
        saved.status = status
        db.commit()
    finally:
        db.close()

    result = email_drafts.update_draft(
        draft["draft_id"],
        "updated@example.com",
        "Updated subject",
        "Updated body",
    )

    assert result["status"] == "error"

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )

        assert saved.status == status
        assert saved.recipient == "original@example.com"
        assert saved.subject == "Original subject"
        assert saved.body == "Original body"
    finally:
        db.close()


def test_update_draft_rejects_expired_draft(test_db):
    draft = email_drafts.create_draft(
        "original@example.com",
        "Original subject",
        "Original body",
    )

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )
        saved.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
        db.commit()
    finally:
        db.close()

    result = email_drafts.update_draft(
        draft["draft_id"],
        "updated@example.com",
        "Updated subject",
        "Updated body",
    )

    assert result["status"] == "error"
    assert "expired" in result["message"].lower()

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )

        assert saved.status == "expired"
        assert saved.recipient == "original@example.com"
        assert saved.subject == "Original subject"
        assert saved.body == "Original body"
    finally:
        db.close()
