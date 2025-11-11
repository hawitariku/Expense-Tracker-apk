"""
Desktop validation test - checks core functionality without full Kivy UI.
Tests translations, database, and utility functions independently.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_database_functionality():
    """Test that the database works independently."""
    print("✓ Testing database functionality...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, 'expenses.json')
        
        from tinydb import TinyDB, Query
        db = TinyDB(db_path)
        
        # Insert test entries
        doc_id1 = db.insert({
            "amount": 100.0,
            "category": "Food",
            "note": "Lunch",
            "date": "2025-11-11 12:00"
        })
        
        doc_id2 = db.insert({
            "amount": 50.0,
            "category": "Transport",
            "note": "Taxi",
            "date": "2025-11-11 14:00"
        })
        
        assert doc_id1 is not None
        assert doc_id2 is not None
        print(f"  ✓ Inserted 2 test entries")
        
        # Query and verify
        Expense = Query()
        results = db.search(Expense.category == "Food")
        assert len(results) == 1
        assert results[0]['amount'] == 100.0
        print(f"  ✓ Query results verified")
        
        # Test update by doc_id
        db.update({'amount': 120.0}, doc_ids=[doc_id1])
        updated = db.get(doc_id=doc_id1)
        assert updated is not None
        assert updated['amount'] == 120.0
        print(f"  ✓ Update functionality works")
        
        # Test delete
        db.remove(doc_ids=[doc_id2])
        remaining = db.all()
        assert len(remaining) == 1
        print(f"  ✓ Delete functionality works")
        
        db.close()


def test_validation_functions():
    """Test utility validation functions."""
    print("✓ Testing validation functions...")
    
    from utils import validate_expense, safe_parse_amount
    
    # Test safe_parse_amount - valid cases
    assert safe_parse_amount("100.50") == 100.50
    assert safe_parse_amount("100") == 100.0
    assert safe_parse_amount("0.99") == 0.99
    print("  ✓ Amount parsing: valid cases pass")
    
    # Test safe_parse_amount - invalid cases
    assert safe_parse_amount("") is None
    assert safe_parse_amount("invalid") is None
    assert safe_parse_amount("abc123") is None
    print("  ✓ Amount parsing: invalid cases fail gracefully")
    
    # Test expense validation - valid
    ok, err = validate_expense("100.50", "Food")
    assert ok is True, f"Expected validation to pass: {err}"
    print("  ✓ Valid expense passes validation")
    
    # Test expense validation - invalid (empty amount)
    ok, err = validate_expense("", "Food")
    assert ok is False
    print("  ✓ Empty amount fails validation")
    
    # Test expense validation - invalid (empty category)
    ok, err = validate_expense("100.50", "")
    assert ok is False
    print("  ✓ Empty category fails validation")
    
    # Test expense validation - invalid (negative)
    ok, err = validate_expense("-50", "Food")
    assert ok is False
    print("  ✓ Negative amount fails validation")


def test_translation_po_files():
    """Test that translation PO files exist and are valid."""
    print("✓ Testing translation files...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    locales_dir = os.path.join(base_dir, 'locales')
    
    # Check English
    en_po = os.path.join(locales_dir, 'en', 'LC_MESSAGES', 'app.po')
    assert os.path.exists(en_po), f"English PO file not found: {en_po}"
    print("  ✓ English translation file exists")
    
    # Check Amharic
    am_po = os.path.join(locales_dir, 'am', 'LC_MESSAGES', 'app.po')
    assert os.path.exists(am_po), f"Amharic PO file not found: {am_po}"
    print("  ✓ Amharic translation file exists")
    
    # Check Oromo
    om_po = os.path.join(locales_dir, 'om', 'LC_MESSAGES', 'app.po')
    assert os.path.exists(om_po), f"Oromo PO file not found: {om_po}"
    print("  ✓ Oromo translation file exists")
    
    # Verify PO files have content
    for lang, po_file in [('English', en_po), ('Amharic', am_po), ('Oromo', om_po)]:
        with open(po_file, 'r', encoding='utf-8') as f:
            content = f.read()
        assert 'msgid' in content
        assert 'msgstr' in content
        assert len(content) > 100
        print(f"  ✓ {lang} PO file has valid content")


def test_translation_loading():
    """Test that translations can be loaded and parsed."""
    print("✓ Testing translation loading...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    locales_dir = os.path.join(base_dir, 'locales')
    
    # Manually parse a simple PO file to verify structure
    po_file = os.path.join(locales_dir, 'en', 'LC_MESSAGES', 'app.po')
    
    translations = {}
    with open(po_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    msgid = None
    for line in lines:
        line = line.strip()
        if line.startswith('msgid '):
            msgid = line[6:].strip().strip('"')
        elif line.startswith('msgstr '):
            msgstr = line[7:].strip().strip('"')
            if msgid and msgid != '':
                translations[msgid] = msgstr
                msgid = None
    
    # Verify some common keys are present
    common_keys = ['amount', 'category', 'expense_tracker', 'clear', 'ok']
    for key in common_keys:
        assert key in translations, f"Missing translation key: {key}"
    
    print(f"  ✓ Found {len(translations)} translation entries")
    print(f"  ✓ Common keys verified: {', '.join(common_keys)}")


def test_app_structure():
    """Test that the app structure is valid without running it."""
    print("✓ Testing app structure...")
    
    import main
    
    # Check required classes exist
    assert hasattr(main, 'ExpenseTrackerApp')
    assert hasattr(main, 'MainScreen')
    print("  ✓ Main application classes exist")
    
    # Check required functions exist
    assert hasattr(main, 'update_translations')
    print("  ✓ Translation functions exist")
    
    # Check KV string exists
    assert hasattr(main, 'KV')
    assert len(main.KV) > 0
    print("  ✓ KV layout definition exists")


def test_config_files():
    """Test that configuration files are valid."""
    print("✓ Testing configuration files...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Check buildozer.spec
    buildozer_spec = os.path.join(base_dir, 'buildozer.spec')
    assert os.path.exists(buildozer_spec)
    with open(buildozer_spec, 'r') as f:
        content = f.read()
    assert 'title' in content
    assert 'package.name' in content
    print("  ✓ buildozer.spec is valid")
    
    # Check requirements.txt
    requirements = os.path.join(base_dir, 'requirements.txt')
    assert os.path.exists(requirements)
    with open(requirements, 'r') as f:
        content = f.read()
    assert 'kivy' in content.lower()
    assert 'tinydb' in content.lower()
    print("  ✓ requirements.txt is valid")


def main():
    """Run all desktop validation tests."""
    print("\n" + "="*70)
    print("DESKTOP VALIDATION TEST SUITE")
    print("="*70 + "\n")
    
    tests = [
        test_database_functionality,
        test_validation_functions,
        test_translation_po_files,
        test_translation_loading,
        test_app_structure,
        test_config_files,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"  ✗ FAILED: {e}")
            import traceback
            traceback.print_exc()
        print()
    
    print("="*70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*70 + "\n")
    
    if failed == 0:
        print("✓ ALL TESTS PASSED - App is ready for desktop use!")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
