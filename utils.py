import re


def safe_parse_amount(amount_str):
    """Try to parse amount string to float. Returns float or None on failure."""
    try:
        if amount_str is None:
            return None
        s = amount_str.strip()
        if s == "":
            return None
        # Allow commas as thousand separators
        s = s.replace(',', '')
        # basic numeric check
        if not re.match(r'^-?\d+(?:\.\d+)?$', s):
            return None
        val = float(s)
        return val
    except (ValueError, TypeError):
        return None


def validate_expense(amount_str, category):
    """Validate amount and category. Returns (True, None) or (False, error_key).

    error_key is a translation key like 'fill_all_fields' or 'invalid_amount'.
    """
    if amount_str is None or category is None:
        return False, 'fill_all_fields'
    if str(amount_str).strip() == '' or str(category).strip() == '':
        return False, 'fill_all_fields'

    val = safe_parse_amount(amount_str)
    if val is None:
        return False, 'invalid_amount'
    if val < 0:
        return False, 'negative_amount'

    return True, None
