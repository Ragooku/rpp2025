import os
import csv
from datetime import datetime
from typing import List, Dict, Any, Iterator, Generator


class TrafficLightBase:
    """Базовый класс для работы с данными светофоров"""

    @staticmethod
    def count_files_in_directory(directory: str) -> int:
        """Статический метод для подсчета количества файлов в указанной директории"""
        try:
            files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            return len(files)
        except Exception as e:
            print(f"Ошибка при подсчете файлов: {e}")
            return 0


class TrafficLightData(TrafficLightBase):
    """Класс для работы с данными о светофорах"""

    def __init__(self, filename: str = "data.csv"):
        self._data = []
        self.filename = filename
        self._load_data()

    def __setattr__(self, name: str, value: Any) -> None:
        """Контроль установки атрибутов"""
        if name == '_data' and hasattr(self, '_data'):
            raise AttributeError("Невозможно напрямую изменить данные. Используйте методы класса.")
        super().__setattr__(name, value)

    def __getitem__(self, index: int) -> Dict[str, Any]:
        """Доступ к элементам по индексу"""
        return self._data[index]

    def __len__(self) -> int:
        """Количество записей"""
        return len(self._data)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Итератор по данным"""
        return iter(self._data)

    def __repr__(self) -> str:
        """Строковое представление объекта"""
        return f"TrafficLightData(filename='{self.filename}', records={len(self._data)})"

    def _load_data(self) -> None:
        """Загрузка данных из файла"""
        try:
            with open(self.filename, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Преобразование строк в соответствующие типы данных
                    processed_row = self._process_row(row)
                    self._data.append(processed_row)
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден. Будет создан новый при сохранении.")
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")

    def _process_row(self, row: Dict[str, str]) -> Dict[str, Any]:
        """Обработка строки данных"""
        processed = {}
        processed['№'] = int(row['№'])
        processed['дата и время включения'] = datetime.strptime(
            row['дата и время включения'], '%Y-%m-%d %H:%M:%S')
        processed['дата и время выключения'] = datetime.strptime(
            row['дата и время выключения'], '%Y-%m-%d %H:%M:%S')
        processed['количество проехавших автомобилей'] = int(
            row['количество проехавших автомобилей'])
        processed['количество автомобилей в ожидании'] = int(
            row['количество автомобилей в ожидании'])
        return processed

    def save_to_csv(self) -> None:
        """Сохранение данных в CSV файл"""
        if not self._data:
            print("Нет данных для сохранения")
            return

        try:
            with open(self.filename, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = ['№', 'дата и время включения', 'дата и время выключения',
                              'количество проехавших автомобилей', 'количество автомобилей в ожидании']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for item in self._data:
                    item_copy = item.copy()
                    item_copy['дата и время включения'] = item['дата и время включения'].strftime('%Y-%m-%d %H:%M:%S')
                    item_copy['дата и время выключения'] = item['дата и время выключения'].strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow(item_copy)
            print(f"Данные успешно сохранены в {self.filename}")
        except Exception as e:
            print(f"Ошибка при сохранении файла: {e}")

    def add_record(self, record: Dict[str, Any]) -> None:
        """Добавление новой записи"""
        try:
            processed = self._process_row(record)
            self._data.append(processed)
            print("Запись успешно добавлена!")
        except Exception as e:
            print(f"Ошибка при добавлении записи: {e}")

    def print_data(self, title: str = "") -> None:
        """Вывод данных в удобочитаемом формате"""
        if title:
            print(f"\n=== {title} ===")
        if not self._data:
            print("Нет данных для отображения")
            return

        headers = ["№", "Включен", "Выключен", "Проехало", "В ожидании"]
        print(f"{headers[0]:<5} {headers[1]:<20} {headers[2]:<20} {headers[3]:<10} {headers[4]:<10}")
        print("-" * 70)

        for item in self._data:
            print(f"{item['№']:<5} "
                  f"{item['дата и время включения'].strftime('%Y-%m-%d %H:%M:%S'):<20} "
                  f"{item['дата и время выключения'].strftime('%Y-%m-%d %H:%M:%S'):<20} "
                  f"{item['количество проехавших автомобилей']:<10} "
                  f"{item['количество автомобилей в ожидании']:<10}")

    def sort_by_id(self) -> None:
        """Сортировка по номеру светофора"""
        self._data.sort(key=lambda x: str(x['№']))

    def sort_by_passed_cars(self) -> None:
        """Сортировка по количеству проехавших автомобилей"""
        self._data.sort(key=lambda x: x['количество проехавших автомобилей'])

    def filter_by_waiting_cars(self, threshold: int) -> Generator[Dict[str, Any], None, None]:
        """Генератор для фильтрации по количеству автомобилей в ожидании"""
        for item in self._data:
            if item['количество автомобилей в ожидании'] > threshold:
                yield item


class TrafficLightManager(TrafficLightData):
    """Расширенный класс для управления светофорами с дополнительной функциональностью"""

    def __init__(self, filename: str = "data.csv"):
        super().__init__(filename)

    def get_traffic_light_by_id(self, light_id: int) -> Dict[str, Any]:
        """Получение данных светофора по ID"""
        for item in self._data:
            if item['№'] == light_id:
                return item
        raise ValueError(f"Светофор с ID {light_id} не найден")

    def get_average_passed_cars(self) -> float:
        """Среднее количество проехавших автомобилей"""
        if not self._data:
            return 0.0
        total = sum(item['количество проехавших автомобилей'] for item in self._data)
        return total / len(self._data)

    def get_max_waiting_time(self) -> float:
        """Максимальное время ожидания в часах"""
        if not self._data:
            return 0.0
        max_time = max(
            (item['дата и время выключения'] - item['дата и время включения']).total_seconds() / 3600
            for item in self._data
        )
        return max_time


def input_record() -> Dict[str, str]:
    """Функция для ввода новой записи"""
    record = {}
    record['№'] = input("Введите номер светофора: ")
    record['дата и время включения'] = input(
        "Введите дату и время включения (формат ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")
    record['дата и время выключения'] = input(
        "Введите дату и время выключения (формат ГГГГ-ММ-ДД ЧЧ:ММ:СС): ")
    record['количество проехавших автомобилей'] = input(
        "Введите количество проехавших автомобилей: ")
    record['количество автомобилей в ожидании'] = input(
        "Введите количество автомобилей в ожидании: ")
    return record


def main():
    # 1. Подсчет файлов в директории (статический метод)
    directory = input("Введите путь к директории для подсчета файлов: ")
    file_count = TrafficLightBase.count_files_in_directory(directory)
    print(f"\nКоличество файлов в директории {directory}: {file_count}")

    # 2. Работа с данными светофоров
    manager = TrafficLightManager("data.csv")

    while True:
        print("\nМеню:")
        print("1. Показать исходные данные")
        print("2. Сортировать по номеру светофора")
        print("3. Сортировать по количеству проехавших автомобилей")
        print("4. Фильтровать по количеству автомобилей в ожидании (более N)")
        print("5. Добавить новую запись")
        print("6. Сохранить данные в файл")
        print("7. Показать среднее количество проехавших автомобилей")
        print("8. Показать максимальное время ожидания")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            manager.print_data("Исходные данные")

        elif choice == "2":
            manager.sort_by_id()
            manager.print_data("Сортировка по номеру светофора")

        elif choice == "3":
            manager.sort_by_passed_cars()
            manager.print_data("Сортировка по количеству проехавших автомобилей")

        elif choice == "4":
            try:
                threshold = int(input("Введите минимальное количество автомобилей в ожидании: "))
                filtered = manager.filter_by_waiting_cars(threshold)
                print("\n=== Отфильтрованные данные ===")
                headers = ["№", "Включен", "Выключен", "Проехало", "В ожидании"]
                print(f"{headers[0]:<5} {headers[1]:<20} {headers[2]:<20} {headers[3]:<10} {headers[4]:<10}")
                print("-" * 70)
                for item in filtered:
                    print(f"{item['№']:<5} "
                          f"{item['дата и время включения'].strftime('%Y-%m-%d %H:%M:%S'):<20} "
                          f"{item['дата и время выключения'].strftime('%Y-%m-%d %H:%M:%S'):<20} "
                          f"{item['количество проехавших автомобилей']:<10} "
                          f"{item['количество автомобилей в ожидании']:<10}")
            except ValueError:
                print("Ошибка: введите целое число")

        elif choice == "5":
            record = input_record()
            manager.add_record(record)

        elif choice == "6":
            manager.save_to_csv()

        elif choice == "7":
            avg = manager.get_average_passed_cars()
            print(f"\nСреднее количество проехавших автомобилей: {avg:.2f}")

        elif choice == "8":
            max_time = manager.get_max_waiting_time()
            print(f"\nМаксимальное время ожидания: {max_time:.2f} часов")

        elif choice == "0":
            print("Выход из программы")
            break

        else:
            print("Неверный ввод. Пожалуйста, выберите действие из меню.")


if __name__ == "__main__":
    main()