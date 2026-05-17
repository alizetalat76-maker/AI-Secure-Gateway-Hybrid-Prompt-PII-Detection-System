import json
import os
from datetime import datetime

LOG_FILE = "results/audit_log.jsonl"

def log_request(data):
    """Save every request and its result to a log file."""
    os.makedirs("results", exist_ok=True)
    data["timestamp"] = datetime.now().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(data) + "\n")
