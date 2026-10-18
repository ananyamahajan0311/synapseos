
import sys
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from googleapiclient.errors import HttpError
from services.email_drafts import _classify_gmail_error


def test_http_400_is_classified_as_failed():
    response = Mock()
    response.status = 400
    error = HttpError(response, b"Invalid request")

    assert _classify_gmail_error(error) == "failed"


def test_http_500_is_uncertain():
    response = Mock()
    response.status = 500
    error = HttpError(response, b"Server error")

    assert _classify_gmail_error(error) == "send_uncertain"


def test_timeout_is_uncertain():
    assert (
        _classify_gmail_error(TimeoutError())
        == "send_uncertain"
    )
