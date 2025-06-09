import pytest
from app.utils.file_utils import validate_file_type


def test_validate_file_type_accepts_allowed_extension():
    assert validate_file_type("document.pdf", [".pdf", ".jpg"]) is True


def test_validate_file_type_rejects_disallowed_extension():
    assert validate_file_type("malware.exe", [".pdf", ".jpg"]) is False
