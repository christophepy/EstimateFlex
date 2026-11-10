# string_utils.py
import re
import unicodedata


def normalize_name(value: str) -> str:
    value = value.strip().lower()

    # suppression accents
    value = "".join(
        c
        for c in unicodedata.normalize("NFD", value)
        if unicodedata.category(c) != "Mn"
    )

    # remplacer séparateurs par espace
    value = value.replace("-", " ").replace("_", " ")

    # espaces multiples
    value = re.sub(r"\s+", " ", value)

    return value
