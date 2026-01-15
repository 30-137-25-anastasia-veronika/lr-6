import pytest
import tempfile
import os
import purchase_analyzer


def create_test_file(content):
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8')
    temp_file.write(content)
    temp_file.close()
    return temp_file.name

def test_read_valid_purchases():
    content = """2023-10-15;Еда;Хлеб;50.0;2
2023-10-16;Электроника;Наушники;2000.0;1
2023-10-17;Книги;Питон для начинающих;1200.5;1"""

    filename = create_test_file(content)
    purchases = purchase_analyzer.read_purchases(filename)

    assert len(purchases) == 3
    assert purchases[0]['category'] == 'Еда'
    assert purchases[0]['name'] == 'Хлеб'
    assert purchases[0]['price'] == 50.0
    assert purchases[0]['qty'] == 2

    os.unlink(filename)

def test_skip_invalid_purchases():
    content = """2023-10-15;Еда;Хлеб;50.0;2
неправильный формат
2023-10-17;Книги;Питон;сто двадцать;1
2023-10-18;Техника;;1500.0;1"""

    filename = create_test_file(content)
    purchases = purchase_analyzer.read_purchases(filename)

    assert len(purchases) == 1
    assert purchases[0]['name'] == 'Хлеб'

    os.unlink(filename)

def test_count_errors():
    content = """2023-10-15;Еда;Хлеб;50.0;2
плохая строка
2023-10-17;Книги;Питон;1200;1
2023-10-18;Техника;Телефон;1500.0;-1
еще одна плохая
2023-10-19;Еда;Молоко;80;2"""

    filename = create_test_file(content)
    errors = purchase_analyzer.count_errors(filename)

    assert errors == 4

    os.unlink(filename)


def test_total_spent():
    purchases = [
        {'date': '2023-10-15', 'category': 'Еда', 'name': 'Хлеб', 'price': 50.0, 'qty': 2},
        {'date': '2023-10-16', 'category': 'Еда', 'name': 'Молоко', 'price': 80.0, 'qty': 1},
        {'date': '2023-10-17', 'category': 'Книги', 'name': 'Учебник', 'price': 500.0, 'qty': 1}
    ]

    total = purchase_analyzer.total_spent(purchases)
    expected_total = (50.0 * 2) + (80.0 * 1) + (500.0 * 1)

    assert total == expected_total

def test_spent_by_category():
    purchases = [
        {'date': '2023-10-15', 'category': 'Еда', 'name': 'Хлеб', 'price': 50.0, 'qty': 2},
        {'date': '2023-10-16', 'category': 'Еда', 'name': 'Молоко', 'price': 80.0, 'qty': 3},
        {'date': '2023-10-17', 'category': 'Книги', 'name': 'Учебник', 'price': 500.0, 'qty': 1},
        {'date': '2023-10-18', 'category': 'Книги', 'name': 'Роман', 'price': 350.0, 'qty': 2}
    ]

    category_totals = purchase_analyzer.spent_by_category(purchases)

    assert 'Еда' in category_totals
    assert 'Книги' in category_totals
    assert category_totals['Еда'] == (50.0 * 2) + (80.0 * 3)
    assert category_totals['Книги'] == (500.0 * 1) + (350.0 * 2)

def test_top_n_expensive():
    purchases = [
        {'date': '2023-10-15', 'category': 'Еда', 'name': 'Хлеб', 'price': 50.0, 'qty': 2},
        {'date': '2023-10-16', 'category': 'Техника', 'name': 'Ноутбук', 'price': 50000.0, 'qty': 1},
        {'date': '2023-10-17', 'category': 'Книги', 'name': 'Учебник', 'price': 1200.0, 'qty': 1},
        {'date': '2023-10-18', 'category': 'Еда', 'name': 'Икра', 'price': 3000.0, 'qty': 2}
    ]

    top3 = purchase_analyzer.top_n_expensive(purchases, 3)

    assert len(top3) == 3
    assert top3[0]['name'] == 'Ноутбук'
    assert top3[1]['name'] == 'Икра'
    assert top3[2]['name'] == 'Учебник'

def test_top_n_with_different_n():
    purchases = [
        {'date': '2023-10-15', 'category': 'Еда', 'name': 'Хлеб', 'price': 50.0, 'qty': 2},
        {'date': '2023-10-16', 'category': 'Еда', 'name': 'Молоко', 'price': 80.0, 'qty': 1}
    ]

    top1 = purchase_analyzer.top_n_expensive(purchases, 1)
    top5 = purchase_analyzer.top_n_expensive(purchases, 5)

    assert len(top1) == 1
    assert len(top5) == 2


if __name__ == '__main__':
    pytest.main()
