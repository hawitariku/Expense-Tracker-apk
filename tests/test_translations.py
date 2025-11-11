import os
import gettext
import pytest

def get_translation(lang_code):
    """Helper to load translations for testing"""
    localedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locales')
    try:
        trans = gettext.translation('app', localedir, languages=[lang_code])
        trans.install()
        return trans.gettext
    except Exception as e:
        pytest.skip(f"Translation file for {lang_code} not found: {e}")

def test_english_translations():
    _ = get_translation('en')
    # Test core UI texts
    assert _("expense_tracker") == "Expense Tracker"
    assert _("amount") == "Amount"
    assert _("category") == "Category"
    assert _("note") == "Note (optional)"
    
    # Test action buttons
    assert _("add_expense") == "Add Expense"
    assert _("clear") == "Clear"
    assert _("ok") == "OK"
    
    # Test new notification messages
    assert _("expense_added") == "Expense added"
    assert _("expense_deleted") == "Expense deleted"
    assert _("database_cleared") == "All expenses cleared"
    
    # Test validation messages
    assert _("invalid_amount") == "Please enter a valid amount"
    assert _("negative_amount") == "Amount cannot be negative"
    assert _("fill_all_fields") == "Please fill in all required fields"

def test_amharic_translations():
    _ = get_translation('am')
    # Test core UI texts
    assert _("expense_tracker") == "የወጭ መቆጣጠሪያ"
    assert _("amount") == "መጠን"
    assert _("category") == "ምድብ"
    
    # Test validation messages
    assert _("fill_all_fields") == "እባክዎን ሁሉንም የተጠየቁ መስኮች ይሙሉ"
    assert _("invalid_amount") == "እባክዎን ትክክለኛ መጠን ያስገቡ"
    assert _("negative_amount") == "መጠኑ አሉታዊ መሆን አይችልም"

def test_oromo_translations():
    _ = get_translation('om')
    # Test core UI texts
    assert _("expense_tracker") == "Trackera Dabarsaa"
    assert _("amount") == "Hammanta"
    assert _("category") == "Gosa"
    
    # Test validation messages
    assert _("fill_all_fields") == "Meeshaa bu'uuraa hunda guuti"
    assert _("invalid_amount") == "Maaloo hammanta sirrii galchi"
    assert _("negative_amount") == "Hammantni gara gadii ta'uu hin danda'u"

def test_translation_fallbacks():
    """Test fallback behavior for missing translations"""
    _ = get_translation('xy')  # Non-existent language code
    # Should fall back to returning the message key
    assert _("expense_tracker") == "expense_tracker"
    assert _("invalid_amount") == "invalid_amount"

def test_all_languages_have_required_keys():
    """Verify that all languages have the same essential message keys"""
    required_keys = {
        # Core UI
        "expense_tracker", "amount", "category", "note",
        "add_expense", "clear", "ok", "total",
        # Actions
        "expense_added", "expense_deleted", "database_cleared",
        "exported_to", "no_data_to_export",
        # Multi-select
        "no_selection", "selection_deleted",
        # Validation
        "invalid_amount", "negative_amount", "fill_all_fields"
    }
    
    for lang in ['en', 'am', 'om']:
        _ = get_translation(lang)
        for key in required_keys:
            translated = _(key)
            # Translation should exist and not be the same as the key
            # (unless it's English where some might match)
            if lang != 'en':
                assert translated != key, f"Missing translation for '{key}' in {lang}"
            assert translated, f"Empty translation for '{key}' in {lang}"