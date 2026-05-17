from langdetect import detect

def detect_language(text):
    """Detect the language of the input text."""
    try:
        lang = detect(text)
        return lang
    except:
        return "en"
