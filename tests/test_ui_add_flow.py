import os
import sys
from types import SimpleNamespace
from tinydb import TinyDB

# Ensure project root is on sys.path so we can import main
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import main


def test_add_flow_injected_inputs(tmp_path, monkeypatch):
    # Arrange: create app but don't call build() (avoids KivyMD init issues)
    app = main.ExpenseTrackerApp()

    # Initialize a temporary TinyDB and assign to module-level db
    db_path = str(tmp_path / "test_expenses.json")
    test_db = TinyDB(db_path)
    monkeypatch.setattr(main, 'db', test_db)

    # Create fake main_screen with ids that contain amount/category/note
    # Create minimal fake widgets that provide the attributes/methods used by update_list()
    fake_expense_list = SimpleNamespace(
        clear_widgets=lambda: None,
        add_widget=lambda widget: None
    )
    fake_total_label = SimpleNamespace(text='')
    fake_select_all = SimpleNamespace(active=False)
    fake_delete_selected_button = SimpleNamespace(disabled=True, opacity=0.0)

    fake_ids = SimpleNamespace(
        amount=SimpleNamespace(text='123.45'),
        category=SimpleNamespace(text='TestCategory'),
        note=SimpleNamespace(text='Unit test note'),
        expense_list=fake_expense_list,
        total_label=fake_total_label,
        select_all_checkbox=fake_select_all,
        delete_selected_button=fake_delete_selected_button
    )
    fake_screen = SimpleNamespace(ids=fake_ids)

    # Monkeypatch get_main_screen to return our fake screen
    monkeypatch.setattr(app, 'get_main_screen', lambda: fake_screen)
    # Monkeypatch KivyMD widgets used by update_list() to avoid GUI init
    class DummyListItem:
        def __init__(self, **kwargs):
            self.text = kwargs.get('text', '')
            self.secondary_text = kwargs.get('secondary_text', '')
            self.size_hint_y = kwargs.get('size_hint_y', None)
            self.height = kwargs.get('height', None)
        def add_widget(self, w):
            pass

    class DummyIcon:
        def __init__(self, **kwargs):
            self.icon = kwargs.get('icon', '')

    monkeypatch.setattr(main, 'TwoLineAvatarListItem', DummyListItem)
    monkeypatch.setattr(main, 'IconLeftWidget', DummyIcon)

    # Act: call add_expense which will read from our injected fake ids
    app.add_expense()

    # Assert: DB now has one entry with matching values
    entries = test_db.all()
    assert len(entries) == 1
    e = entries[0]
    assert float(e['amount']) == 123.45
    assert e['category'] == 'TestCategory'
    assert 'Unit test note' in e['note']
    # Cleanup
    test_db.close()
