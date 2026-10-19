
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


def test_valid_recipient_has_no_generic_identity_warning(test_db):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Test subject",
        "Test body",
    )

    assert draft["validation"]["recipient_format_valid"] is True
    assert draft["validation"]["warnings"] == []
def test_reserved_invalid_domain_is_rejected(test_db, monkeypatch):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Test subject",
        "Test body",
    )
    assert draft["status"] != "error"

    result = email_drafts.update_draft(
        draft["draft_id"],
        "user@invalid",
        "Test subject",
        "Test body",
    )

    assert result["status"] == "error"

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

@pytest.mark.parametrize(
    "field,changed_value",
    [
        ("recipient", "other@example.com"),
        ("subject", "Changed subject"),
        ("body", "Changed body"),
    ],
)
def test_each_modified_field_is_rejected(
    test_db, monkeypatch, field, changed_value
):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Approved subject",
        "Approved body",
    )

    submitted = {
        "recipient": "test@example.com",
        "subject": "Approved subject",
        "body": "Approved body",
    }
    submitted[field] = changed_value

    def unexpected_send(*args, **kwargs):
        pytest.fail("Modified content must never reach Gmail")

    monkeypatch.setattr(email_drafts, "send_email", unexpected_send)

    result = email_drafts.send_approved_draft(
        draft["draft_id"],
        submitted["recipient"],
        submitted["subject"],
        submitted["body"],
    )

    assert result["status"] == "error"
    assert "match" in result["message"].lower()

from googleapiclient.errors import HttpError
from unittest.mock import Mock


def test_gmail_client_error_marks_send_failed(test_db, monkeypatch):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Test subject",
        "Test body",
    )

    response = Mock()
    response.status = 400

    def simulated_gmail_rejection(*args, **kwargs):
        raise HttpError(
            response,
            b'{"error":{"message":"Invalid request"}}',
        )

    monkeypatch.setattr(
        email_drafts,
        "send_email",
        simulated_gmail_rejection,
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
        assert saved.status == "failed"
    finally:
        db.close()


def test_database_failure_after_gmail_success_does_not_resend(
    test_db, monkeypatch
):
    draft = email_drafts.create_draft(
        "test@example.com",
        "Test subject",
        "Test body",
    )

    send_calls = []

    def simulated_gmail(to, subject, body):
        send_calls.append((to, subject, body))
        return {
            "status": "success",
            "message": "Gmail accepted the email.",
            "message_id": "mock-message-id",
        }

    original_session_local = email_drafts.SessionLocal
    session_calls = 0

    def simulated_session_local():
        nonlocal session_calls
        session_calls += 1

        session = original_session_local()

        # The first session claims the draft.
        # The second session records the Gmail result.
        if session_calls == 2:
            def failed_commit():
                raise RuntimeError("Simulated database failure")

            session.commit = failed_commit

        return session

    monkeypatch.setattr(email_drafts, "send_email", simulated_gmail)
    monkeypatch.setattr(
        email_drafts,
        "SessionLocal",
        simulated_session_local,
    )

    result = email_drafts.send_approved_draft(
        draft["draft_id"],
        "test@example.com",
        "Test subject",
        "Test body",
    )

    assert result["status"] == "success"
    assert len(send_calls) == 1

    db = test_db()
    try:
        saved = (
            db.query(models.EmailDraft)
            .filter_by(draft_id=draft["draft_id"])
            .first()
        )
        assert saved.status == "sending"
    finally:
        db.close()

    second_result = email_drafts.send_approved_draft(
        draft["draft_id"],
        "test@example.com",
        "Test subject",
        "Test body",
    )

    assert second_result["status"] == "error"
    assert len(send_calls) == 1
