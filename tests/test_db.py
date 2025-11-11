import pytest
from tinydb import TinyDB, Query
import os
import datetime

@pytest.fixture
def test_db():
    # Create a temporary test database
    db_path = "test_expenses.json"
    db = TinyDB(db_path)
    yield db
    # Cleanup after tests
    db.close()
    try:
        os.remove(db_path)
    except:
        pass

def test_db_operations(test_db):
    # Test inserting an expense
    doc_id = test_db.insert({
        "amount": 123.45,
        "category": "Test Category",
        "note": "Test Note",
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    assert doc_id is not None
    
    # Test retrieving all expenses
    expenses = test_db.all()
    assert len(expenses) == 1
    assert expenses[0]["amount"] == 123.45
    assert expenses[0]["category"] == "Test Category"
    
    # Test querying expenses
    Expense = Query()
    results = test_db.search(Expense.category == "Test Category")
    assert len(results) == 1
    assert results[0]["amount"] == 123.45
    
    # Test updating an expense
    test_db.update({"amount": 456.78}, doc_ids=[doc_id])
    updated = test_db.get(doc_id=doc_id)
    assert updated["amount"] == 456.78
    
    # Test deleting an expense
    test_db.remove(doc_ids=[doc_id])
    assert len(test_db.all()) == 0
    
    # Test bulk operations
    ids = []
    for i in range(3):
        doc_id = test_db.insert({
            "amount": float(i * 100),
            "category": f"Category {i}",
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        ids.append(doc_id)
    
    assert len(test_db.all()) == 3
    
    # Test bulk delete
    test_db.remove(doc_ids=ids)
    assert len(test_db.all()) == 0