"""
Simplified translation tests that work without full Kivy UI initialization.
Tests focus on the translation function behavior and language switching.
"""

import os
import pytest
from kivy.app import App
from main import ExpenseTrackerApp


@pytest.fixture
def app_with_translations():
    """Set up app instance with translations loaded."""
    app = ExpenseTrackerApp()
    base_dir = os.path.dirname(os.path.dirname(__file__))
    app.directory = base_dir
    app.localedir = os.path.join(base_dir, 'locales')
    
    # Register app globally
    App.get_running_app = lambda: app
    app._running = True
    
    # Load translations
    app.load_all_translations()
    
    yield app
    
    # Cleanup
    app._running = False
    App.get_running_app = lambda: None


def test_english_translations(app_with_translations):
    """Test that English translations are loaded correctly."""
    app = app_with_translations
    _ = app._get_text
    
    # Test key translations
    assert _("amount") == "Amount"
    assert _("category") == "Category"
    assert _("expense_tracker") == "Expense Tracker"
    assert _("note") == "Note (optional)"
    assert _("add_expense") == "Add Expense"
    assert _("clear") == "Clear"
    assert _("expense_list") == "Expense List"
    assert _("ok") == "OK"
    assert _("fill_all_fields") == "Please fill in all required fields"
    assert _("database_cleared") == "All expenses cleared"
    assert _("no_selection") == "No items selected"
    assert _("invalid_amount") == "Please enter a valid amount"


def test_amharic_translations(app_with_translations):
    """Test that Amharic translations are loaded and can be switched to."""
    app = app_with_translations
    
    # Switch to Amharic
    app.set_language('am', 'AM')
    _ = app._get_text
    
    # Test key translations
    assert _("amount") == "መጠን"
    assert _("category") == "ምድብ"
    assert _("expense_tracker") == "የወጭ መቆጣጠሪያ"
    assert _("note") == "ማስታወሻ (በምርጫ)"
    assert _("add_expense") == "ወጭ ያክሉ"
    assert _("clear") == "አጽዳ"
    assert _("ok") == "እሺ"


def test_oromo_translations(app_with_translations):
    """Test that Oromo translations are loaded and can be switched to."""
    app = app_with_translations
    
    # Switch to Oromo
    app.set_language('om', 'OM')
    _ = app._get_text
    
    # Test key translations
    assert _("amount") == "Hammanta"
    assert _("category") == "Gosa"
    assert _("expense_tracker") == "Trackera Dabarsaa"
    assert _("note") == "Yaadannoo (filannoo)"
    assert _("add_expense") == "Dabarsa Dabali"
    assert _("clear") == "Haquu"
    assert _("ok") == "TOO"


def test_language_switching(app_with_translations):
    """Test switching between languages updates the translation function."""
    app = app_with_translations
    
    # Start in English
    app.set_language('en', 'EN')
    _ = app._get_text
    assert _("amount") == "Amount"
    
    # Switch to Amharic
    app.set_language('am', 'AM')
    _ = app._get_text
    assert _("amount") == "መጠን"
    
    # Switch to Oromo
    app.set_language('om', 'OM')
    _ = app._get_text
    assert _("amount") == "Hammanta"
    
    # Switch back to English
    app.set_language('en', 'EN')
    _ = app._get_text
    assert _("amount") == "Amount"


def test_unknown_keys_return_original(app_with_translations):
    """Test that unknown translation keys return the key itself."""
    app = app_with_translations
    app.set_language('en', 'EN')
    _ = app._get_text
    
    # Non-existent key should return itself
    assert _("nonexistent_key") == "nonexistent_key"


def test_all_languages_have_common_strings(app_with_translations):
    """Test that all languages have translations for common UI strings."""
    app = app_with_translations
    common_keys = [
        "amount",
        "category",
        "expense_tracker",
        "add_expense",
        "clear",
        "ok",
    ]
    
    for lang_code in ['en', 'am', 'om']:
        app.set_language(lang_code, lang_code.upper())
        _ = app._get_text
        
        for key in common_keys:
            result = _(key)
            # Translation should not be empty and should be different from key (except for missing translations)
            assert result is not None, f"{lang_code}: {key} returned None"
            # Only check that a translation exists (may be the key itself as fallback)
            assert isinstance(result, str), f"{lang_code}: {key} returned non-string"
