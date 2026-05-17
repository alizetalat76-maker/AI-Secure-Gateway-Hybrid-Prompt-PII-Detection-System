import yaml

# Load thresholds from config file
with open("config/gateway_config.yaml") as f:
    config = yaml.safe_load(f)

BLOCK_THRESHOLD = config["thresholds"]["block"]
PII_WEIGHT      = config["weights"]["pii"]

def make_decision(rule_score, semantic_score, pii_entities):
    """
    Combine all risk scores and decide: ALLOW, MASK, or BLOCK.

    Logic:
    - final_risk = worst of (rule_score, semantic_score) + small pii boost
    - If final_risk is high → BLOCK
    - If PII is found but not an attack → MASK
    - Otherwise → ALLOW
    """

    # Add pii weight only if PII was detected
    pii_risk = PII_WEIGHT if pii_entities else 0.0

    # Take the highest risk score, add pii penalty
    final_risk = max(rule_score, semantic_score) + pii_risk
    final_risk = round(min(final_risk, 1.0), 2)  # cap at 1.0

    # Determine reason codes for audit log
    reason_codes = []
    if rule_score >= 0.3:
        reason_codes.append("RULE_INJECTION")
    if semantic_score >= 0.5:
        reason_codes.append("SEMANTIC_INJECTION")
    if pii_entities:
        entity_types = [e["type"] for e in pii_entities]
        if "API_KEY" in entity_types:
            reason_codes.append("SECRET_EXTRACTION")
        else:
            reason_codes.append("PII_DETECTED")

    # Make final decision
    if final_risk >= BLOCK_THRESHOLD:
        decision = "BLOCK"
    elif pii_entities:
        decision = "MASK"
    else:
        decision = "ALLOW"

    return decision, final_risk, reason_codes
