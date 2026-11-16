"""SBAGLIATO APPOSTA: i nomi non iniziano con test, quindi pytest non li raccoglie."""
from app.schemas import tidy_title


def check_tidy_title_collapses_spaces():
    assert tidy_title("  La   vita  è bella ") == "La vita è bella"


def should_reject_a_blank_title():
    assert tidy_title("   ") == ""
