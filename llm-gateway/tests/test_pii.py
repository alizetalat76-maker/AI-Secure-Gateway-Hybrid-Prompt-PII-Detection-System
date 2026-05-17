"""
tests/test_pii.py
Tests for the Presidio PII detector.
Run with: pytest tests/
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.pii.presidio_custom import analyze_pii


def test_email_detected():
    entities, safe = analyze_pii("My email is test@example.com")
    types = [e["type"] for e in entities]
    assert "EMAIL_ADDRESS" in types

def test_cnic_detected():
    entities, safe = analyze_pii("My CNIC is 35202-1234567-1")
    types = [e["type"] for e in entities]
    assert "CNIC" in types

def test_student_id_detected():
    entities, safe = analyze_pii("My student ID is FA21-BCS-123")
    types = [e["type"] for e in entities]
    assert "STUDENT_ID" in types

def test_api_key_detected():
    entities, safe = analyze_pii("My API key is sk-abcdefghij1234567890xyz")
    types = [e["type"] for e in entities]
    assert "API_KEY" in types

def test_pk_phone_detected():
    entities, safe = analyze_pii("Call me on 0333-1234567")
    types = [e["type"] for e in entities]
    assert "PK_PHONE" in types

def test_safe_text_anonymized():
    entities, safe = analyze_pii("Email me at hidden@example.com please")
    assert "hidden@example.com" not in safe

def test_benign_has_no_pii():
    entities, safe = analyze_pii("Explain what machine learning is")
    assert len(entities) == 0
