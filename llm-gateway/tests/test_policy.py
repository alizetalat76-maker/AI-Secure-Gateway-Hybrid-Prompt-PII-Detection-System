"""
tests/test_policy.py
Tests for the policy engine decisions.
Run with: pytest tests/
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.policy.policy_engine import make_decision


def test_block_on_high_rule_score():
    decision, risk, codes = make_decision(0.9, 0.1, [])
    assert decision == "BLOCK"

def test_block_on_high_semantic_score():
    decision, risk, codes = make_decision(0.1, 0.9, [])
    assert decision == "BLOCK"

def test_mask_on_pii_only():
    decision, risk, codes = make_decision(0.0, 0.0, [{"type": "EMAIL_ADDRESS", "score": 0.9}])
    assert decision == "MASK"

def test_allow_benign():
    decision, risk, codes = make_decision(0.0, 0.0, [])
    assert decision == "ALLOW"

def test_block_on_api_key():
    decision, risk, codes = make_decision(0.0, 0.0, [{"type": "API_KEY", "score": 0.95}])
    # API key alone causes PII risk boost
    assert "SECRET_EXTRACTION" in codes or decision in ["MASK", "BLOCK"]

def test_reason_codes_present():
    decision, risk, codes = make_decision(0.8, 0.9, [])
    assert len(codes) > 0
