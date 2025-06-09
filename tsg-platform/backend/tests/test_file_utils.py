import sys
from pathlib import Path
import pytest

# Ensure the backend directory is on the Python path when running tests from the
# repository root. This allows importing the `app` package.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.utils.file_utils import validate_file_type, get_file_mime_type


def test_validate_file_type_accepts_allowed_extension():
    assert validate_file_type("document.pdf", [".pdf", ".jpg"]) is True


def test_validate_file_type_rejects_disallowed_extension():
    assert validate_file_type("malware.exe", [".pdf", ".jpg"]) is False


def test_get_file_mime_type_without_magic(tmp_path, monkeypatch):
    monkeypatch.setattr("app.utils.file_utils.magic", None)
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello")
    assert get_file_mime_type(file_path) == "text/plain"
