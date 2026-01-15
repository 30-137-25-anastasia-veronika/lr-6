def read_purchases(path):
    purchases = []
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(';')
                if len(parts) != 5:
                    continue
                date, category, name, price_str, qty_str = parts
                date = date.strip()
                category = category.strip()
                name = name.strip()
                price_str = price_str.strip()
                qty_str = qty_str.strip()
                if len(date) != 10 or date[4] != '-' or date[7] != '-':
                    continue
                try:
                    price = float(price_str)
                    qty = int(qty_str)

                    if price < 0 or qty <= 0:
                        continue
                except ValueError:
                    continue
                purchases.append({
                    'date': date,
                    'category': category,
                    'name': name,
                    'price': price,
                    'qty': qty
                })
    except FileNotFoundError:
        print(f"Ошибка: файл {path} не найден")
        return []
    return purchases


def count_errors(path):
    error_count = 0
    total_lines = 0
    try:
        with open(path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                total_lines += 1
                parts = line.split(';')
                if len(parts) != 5:
                    error_count += 1
                    continue
                date, category, name, price_str, qty_str = parts
                if len(date) != 10 or date[4] != '-' or date[7] != '-':
                    error_count += 1
                    continue
                try:
                    price = float(price_str.strip())
                    qty = int(qty_str.strip())
                    if price < 0 or qty <= 0:
                        error_count += 1
                        continue
                except ValueError:
                    error_count += 1
                    continue
    except FileNotFoundError:
        return 0
    return error_count


def total_spent(purchases):
    total = 0.0
    for purchase in purchases:
        total += purchase['price'] * purchase['qty']
    return total


def spent_by_category(purchases):
    category_totals = {}

    for purchase in purchases:
        category = purchase['category']
        amount = purchase['price'] * purchase['qty']

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    return category_totals


def top_n_expensive(purchases, n=3):
    purchases_with_total = []
    for purchase in purchases:
        purchase_copy = purchase.copy()
        purchase_copy['total_cost'] = purchase['price'] * purchase['qty']
        purchases_with_total.append(purchase_copy)

    sorted_purchases = sorted(
        purchases_with_total,
        key=lambda x: x['total_cost'],
        reverse=True
    )

    return sorted_purchases[:n]


def write_report(purchases, errors, out_path):
    try:
        with open(out_path, 'w', encoding='utf-8') as file:
            file.write("=" * 50 + "\n")
            file.write("ОТЧЕТ ПО АНАЛИЗУ ПОКУПОК\n")
            file.write("=" * 50 + "\n\n")

            file.write(f"Обработано валидных записей: {len(purchases)}\n")
            file.write(f"Найдено ошибок в данных: {errors}\n\n")
            total = total_spent(purchases)
            file.write(f"Общая сумма покупок: {total:.2f} руб.\n\n")
            file.write("Суммы по категориям:\n")
            file.write("-" * 30 + "\n")
            category_totals = spent_by_category(purchases)
            for category, amount in sorted(category_totals.items()):
                file.write(f"{category}: {amount:.2f} руб.\n")
            file.write("\n")
            file.write("Топ-3 самых дорогих покупок:\n")
            file.write("-" * 50 + "\n")
            top_purchases = top_n_expensive(purchases, 3)
            for i, purchase in enumerate(top_purchases, 1):
                total_cost = purchase['price'] * purchase['qty']
                file.write(f"{i}. {purchase['name']} ({purchase['category']})\n")
                file.write(f"   Дата: {purchase['date']}\n")
                file.write(f"   Цена: {purchase['price']:.2f} руб. × {purchase['qty']} шт.\n")
                file.write(f"   Итого: {total_cost:.2f} руб.\n\n")
            if not top_purchases:
                file.write("Нет данных о покупках\n")
            file.write("=" * 50 + "\n")
            file.write("Отчет сгенерирован автоматически\n")
            file.write("=" * 50 + "\n")
        print(f"Отчет успешно сохранен в файл: {out_path}")
    except Exception as e:
        print(f"Ошибка при записи отчета: {e}")
