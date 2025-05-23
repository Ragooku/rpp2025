import os
import csv
from datetime import datetime


def count_files_in_directory(directory):
    """Функция для подсчета количества файлов в указанной директории"""
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return len(files)
    except Exception as e:
        print(f"Ошибка при подсчете файлов: {e}")
        return 0


def read_traffic_light_data(filename):
    """Чтение данных о светофорах из CSV файла"""
    data = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Преобразование строк в соответствующие типы данных
                row['№'] = int(row['№'])
                row['дата и время включения'] = datetime.strptime(row['дата и время включения'], '%Y-%m-%d %H:%M:%S')
                row['дата и время выключения'] = datetime.strptime(row['дата и время выключения'], '%Y-%m-%d %H:%M:%S')
                row['количество проехавших автомобилей'] = int(row['количество проехавших автомобилей'])
                row['количество автомобилей в ожидании'] = int(row['количество автомобилей в ожидании'])
                data.append(row)
    except FileNotFoundError:
        print(f"Файл {filename} не найден. Будет создан новый при сохранении.")
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
    return data


def print_data(data, title=""):
    """Вывод данных о светофорах в удобочитаемом формате"""
    if title:
        print(f"\n=== {title} ===")
    if not data:
        print("Нет данных для отображения")
        return

    # Форматирование заголовков
    headers = ["№", "Включен", "Выключен", "Проехало", "В ожидании"]
    print(f"{headers[0]:<5} {headers[1]:<20} {headers[2]:<20} {headers[3]:<10} {headers[4]:<10}")
    print("-" * 70)

    for item in data:
        print(f"{item['№']:<5} "
              f"{item['дата и время включения'].strftime('%Y-%m-%d %H:%M:%S'):<20} "
              f"{item['дата и время выключения'].strftime('%Y-%m-%d %H:%M:%S'):<20} "
              f"{item['количество проехавших автомобилей']:<10} "
              f"{item['количество автомобилей в ожидании']:<10}")


def save_data_to_csv(filename, data):
    """Сохранение данных в CSV файл"""
    if not data:
        print("Нет данных для сохранения")
        return

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            fieldnames = ['№', 'дата и время включения', 'дата и время выключения',
                          'количество проехавших автомобилей', 'количество автомобилей в ожидании']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in data:
                # Преобразование datetime обратно в строку для сохранения
                item_copy = item.copy()
                item_copy['дата и время включения'] = item['дата и время включения'].strftime('%Y-%m-%d %H:%M:%S')
                item_copy['дата и время выключения'] = item['дата и время выключения'].strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow(item_copy)
        print(f"Данные успешно сохранены в {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")


def add_new_record(data):
    """Добавление новой записи о работе светофора"""
    print("\nДобавление новой записи:")
    try:
        new_record = {}
        new_record['№'] = int(input("Введите номер светофора: "))
        new_record['дата и время включения'] = datetime.strptime(
            input("Введите дату и время включения (формат ГГГГ-ММ-ДД ЧЧ:ММ:СС): "),
            '%Y-%m-%d %H:%M:%S')
        new_record['дата и время выключения'] = datetime.strptime(
            input("Введите дату и время выключения (формат ГГГГ-ММ-ДД ЧЧ:ММ:СС): "),
            '%Y-%m-%d %H:%M:%S')
        new_record['количество проехавших автомобилей'] = int(
            input("Введите количество проехавших автомобилей: "))
        new_record['количество автомобилей в ожидании'] = int(
            input("Введите количество автомобилей в ожидании: "))

        data.append(new_record)
        print("Запись успешно добавлена!")
    except ValueError as e:
        print(f"Ошибка ввода данных: {e}")


def main():
    # 1. Подсчет файлов в директории
    directory = input("Введите путь к директории для подсчета файлов: ")
    file_count = count_files_in_directory(directory)
    print(f"\nКоличество файлов в директории {directory}: {file_count}")

    # 2. Работа с данными светофоров
    filename = "data.csv"
    traffic_data = read_traffic_light_data(filename)

    while True:
        print("\nМеню:")
        print("1. Показать исходные данные")
        print("2. Сортировать по номеру светофора (строковое поле)")
        print("3. Сортировать по количеству проехавших автомобилей (числовое поле)")
        print("4. Фильтровать по количеству автомобилей в ожидании (более N)")
        print("5. Добавить новую запись")
        print("6. Сохранить данные в файл")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            print_data(traffic_data, "Исходные данные")

        elif choice == "2":
            sorted_data = sorted(traffic_data, key=lambda x: str(x['№']))
            print_data(sorted_data, "Сортировка по номеру светофора")

        elif choice == "3":
            sorted_data = sorted(traffic_data, key=lambda x: x['количество проехавших автомобилей'])
            print_data(sorted_data, "Сортировка по количеству проехавших автомобилей")

        elif choice == "4":
            try:
                threshold = int(input("Введите минимальное количество автомобилей в ожидании: "))
                filtered_data = [x for x in traffic_data if x['количество автомобилей в ожидании'] > threshold]
                print_data(filtered_data, f"Светофоры с более чем {threshold} автомобилями в ожидании")
            except ValueError:
                print("Ошибка: введите целое число")

        elif choice == "5":
            add_new_record(traffic_data)

        elif choice == "6":
            save_data_to_csv(filename, traffic_data)

        elif choice == "0":
            print("Выход из программы")
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите действие из меню.")


if __name__ == "__main__":
    main()