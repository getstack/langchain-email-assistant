# tests/test_parsing.py — lightweight unit checks (no API calls)
from services import parse_email_json, format_email_result


def test_parse_email_json_happy_path():
    data = parse_email_json('{"subject": "Hello", "body": "World"}')
    assert data["subject"] == "Hello"
    assert data["body"] == "World"


def test_parse_email_json_fallback():
    data = parse_email_json("Subject: Status\n\nHi there")
    assert data["subject"] == "Status"
    assert "Hi there" in data["body"]


def test_format_email_result():
    text = format_email_result({"subject": "A", "body": "B"})
    assert text.startswith("Subject: A")
    assert "B" in text
