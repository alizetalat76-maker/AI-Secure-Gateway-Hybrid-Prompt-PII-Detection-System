from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

# -------------------------------------------------------
# Customization 1: Pakistan CNIC (e.g. 35202-1234567-1)
# -------------------------------------------------------
cnic_recognizer = PatternRecognizer(
    supported_entity="CNIC",
    patterns=[
        Pattern(
            name="cnic_pattern",
            regex=r"\b\d{5}-\d{7}-\d{1}\b",
            score=0.9
        )
    ],
    context=["cnic", "national id", "identity card", "id card", "شناختی کارڈ"]
)

# -------------------------------------------------------
# Customization 2: Student Registration Number (e.g. FA21-BCS-123)
# -------------------------------------------------------
student_id_recognizer = PatternRecognizer(
    supported_entity="STUDENT_ID",
    patterns=[
        Pattern(
            name="student_id_pattern",
            regex=r"\b[A-Z]{2}\d{2}-[A-Z]{2,4}-\d{3,4}\b",
            score=0.85
        )
    ],
    context=["student", "registration", "reg no", "student id", "roll number"]
)

# -------------------------------------------------------
# Customization 3: API Key (e.g. sk-abc123...)
# -------------------------------------------------------
api_key_recognizer = PatternRecognizer(
    supported_entity="API_KEY",
    patterns=[
        Pattern(
            name="api_key_pattern",
            regex=r"\bsk-[a-zA-Z0-9]{20,}\b",
            score=0.95
        )
    ],
    context=["api", "key", "token", "secret", "credential", "authorization"]
)

# -------------------------------------------------------
# Customization 4: Pakistani Phone Number (e.g. 0333-1234567)
# -------------------------------------------------------
pk_phone_recognizer = PatternRecognizer(
    supported_entity="PK_PHONE",
    patterns=[
        Pattern(
            name="pk_phone_pattern",
            regex=r"\b03\d{2}-?\d{7}\b",
            score=0.85
        )
    ],
    context=["phone", "number", "call", "contact", "mobile", "cell"]
)

# -------------------------------------------------------
# Setup the analyzer with all custom + built-in recognizers
# -------------------------------------------------------
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(cnic_recognizer)
analyzer.registry.add_recognizer(student_id_recognizer)
analyzer.registry.add_recognizer(api_key_recognizer)
analyzer.registry.add_recognizer(pk_phone_recognizer)

anonymizer = AnonymizerEngine()

def analyze_pii(text):
    """
    Detect PII in text using Presidio with custom recognizers.
    Returns:
        entities: list of detected PII with type and confidence score
        safe_text: text with PII replaced by placeholders like <EMAIL_ADDRESS>
    """
    results = analyzer.analyze(text=text, language="en")
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)

    entities = [
        {
            "type": r.entity_type,
            "score": round(r.score, 2)
        }
        for r in results
    ]

    return entities, anonymized.text
