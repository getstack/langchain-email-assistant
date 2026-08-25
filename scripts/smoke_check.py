from services import format_email_result, parse_email_json
from graph import build_graph

raw = '{"subject": "Hello", "body": "World"}'
data = parse_email_json(raw)
assert data["subject"] == "Hello", data
assert data["body"] == "World", data
assert "Subject: A" in format_email_result({"subject": "A", "body": "B"})
g = build_graph()
assert g is not None
print("all_smoke_ok")
