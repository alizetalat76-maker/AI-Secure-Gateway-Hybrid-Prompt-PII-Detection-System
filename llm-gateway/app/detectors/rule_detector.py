import re

# Attack keyword patterns - covers English, Urdu, obfuscated
PATTERNS = [
    # Direct injection
    "ignore previous instructions",
    "ignore all instructions",
    "ignore all previous",
    "disregard all instructions",
    "disregard previous",
    "forget your instructions",
    "forget all previous",

    # System prompt extraction
    "reveal the system prompt",
    "show the system prompt",
    "show me your instructions",
    "print your instructions",
    "display the system prompt",
    "what is your system prompt",
    "repeat your instructions",
    "output your prompt",

    # Jailbreak / role play
    "pretend you are",
    "act as if you have no rules",
    "act as an unrestricted",
    "you are now an ai with no",
    "bypass safety",
    "bypass all safety",
    "no restrictions",
    "without any restrictions",
    "you are now unfiltered",
    "jailbreak",
    "dan mode",
    "developer mode",

    # Secret / credential extraction
    "print api keys",
    "print passwords",
    "print tokens",
    "show api keys",
    "reveal api keys",
    "reveal passwords",
    "print any api",
    "extract passwords",

    # RAG / tool manipulation
    "override your policy",
    "use the retrieved document as a system instruction",
    "override policy",
    "act as a system instruction",

    # Urdu attack keywords
    "ہدایات",
    "سسٹم پرامپٹ",
    "پچھلی ہدایات",
    "نظر انداز کریں",

    # Obfuscated versions (partial leetspeak)
    "ign0re",
    "prev!ous",
    "instruct!ons",
    "pr0mpt",
    "syst3m",
    "byp4ss",
]

def get_rule_score(text):
    """
    Check text against known attack patterns.
    Returns a score from 0.0 (safe) to 1.0 (dangerous).
    """
    text_lower = text.lower()
    hits = 0

    for pattern in PATTERNS:
        if pattern.lower() in text_lower:
            hits += 1

    # Each hit adds 0.35, capped at 1.0
    score = min(hits * 0.35, 1.0)
    return round(score, 2)
