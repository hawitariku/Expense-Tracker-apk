import pytest
from utils import validate_expense, safe_parse_amount

def test_safe_parse_amount():
    # Valid amounts
    assert safe_parse_amount("123.45") == 123.45
    assert safe_parse_amount("1000") == 1000.0
    assert safe_parse_amount("1,000.50") == 1000.50
    assert safe_parse_amount("-123.45") == -123.45  # Negative allowed in parser
    
    # Invalid amounts - should return None instead of raising
    assert safe_parse_amount("") is None
    assert safe_parse_amount(None) is None
    assert safe_parse_amount("abc") is None
    assert safe_parse_amount("12.34.56") is None
    assert safe_parse_amount("$100") is None

def test_validate_expense():
    # Valid expenses
    assert validate_expense("123.45", "Food") == (True, None)
    assert validate_expense("1000", "Rent") == (True, None)
    assert validate_expense("1,234.56", "Transport") == (True, None)
    
    # Invalid expenses - missing or empty fields
    assert validate_expense(None, "Food") == (False, "fill_all_fields")
    assert validate_expense("", "Food") == (False, "fill_all_fields")
    assert validate_expense("123.45", "") == (False, "fill_all_fields")
    assert validate_expense("123.45", None) == (False, "fill_all_fields")
    
    # Invalid amount format
    assert validate_expense("abc", "Food") == (False, "invalid_amount")
    assert validate_expense("12.34.56", "Food") == (False, "invalid_amount")
    assert validate_expense("$100", "Food") == (False, "invalid_amount")
    
    # Negative amount (valid in parser but rejected by validator)
    assert validate_expense("-100", "Food") == (False, "negative_amount")
    assert validate_expense("-123.45", "Food") == (False, "negative_amount")