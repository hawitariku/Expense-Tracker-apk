from main import get_icon_for_category


def test_get_icon_for_common_category():
    assert get_icon_for_category('Food') == 'food'
    assert get_icon_for_category('transport') == 'car'
    assert get_icon_for_category('') == 'cash'

