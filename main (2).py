import purchase_analyzer


def main():
    input_file = "purchases.txt"
    output_file = "report.txt"

    print("Начинаю анализ данных о покупках...")

    purchases = purchase_analyzer.read_purchases(input_file)
    print(f"Прочитано валидных записей: {len(purchases)}")

    errors = purchase_analyzer.count_errors(input_file)
    print(f"Найдено строк с ошибками: {errors}")

    print("Формирование отчета...")
    purchase_analyzer.write_report(purchases, errors, output_file)

    print("Анализ завершен!")


if __name__ == "__main__":
    main()
