import re


def clean_text(text: str) -> str:
    """Normalize text without changing its basic meaning."""
    text = text.replace("\x00", " ") #changing invisible null characters to space
    text = re.sub(r"\s+", " ", text) #replacing multiple whitespace characters with a single space
    return text.strip() #removing leading and trailing whitespace
