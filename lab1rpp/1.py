import random


def get_list_from_input():
    """Получает список чисел от пользователя"""
    while True:
        try:
            lst = list(map(int, input("Введите элементы списка через пробел: ").split()))
            return lst
        except ValueError:
            print("Ошибка ввода! Введите только целые числа.")


def get_list_from_random(size=7, min_val=0, max_val=10):
    """Генерирует список случайных чисел"""
    return [random.randint(min_val, max_val) for _ in range(size)]


def find_min_index(lst):
    """Находит индекс минимального элемента (без использования min)"""
    min_val = lst[0]
    min_index = 0
    for i in range(1, len(lst)):
        if lst[i] < min_val:
            min_val = lst[i]
            min_index = i
    return min_index


def find_max_index(lst):
    """Находит индекс максимального элемента (без использования max)"""
    max_val = lst[0]
    max_index = 0
    for i in range(1, len(lst)):
        if lst[i] > max_val:
            max_val = lst[i]
            max_index = i
    return max_index


def remove_multiples_of_three_no_std(lst):
    """Удаляет элементы, кратные 3, между минимальным и максимальным элементами (без стандартных функций)"""
    min_index = find_min_index(lst)
    max_index = find_max_index(lst)

    if max_index > min_index:
        start, end = min_index, max_index
    else:
        start, end = max_index, min_index

    result = []
    for i in range(len(lst)):
        if start < i < end and lst[i] % 3 == 0:
            continue
        result.append(lst[i])

    return result


def remove_multiples_of_three_std(lst):
    """Удаляет элементы, кратные 3, между минимальным и максимальным элементами (с использованием стандартных функций)"""
    min_index = lst.index(min(lst))
    max_index = lst.index(max(lst))

    if max_index > min_index:
        start, end = min_index, max_index
    else:
        start, end = max_index, min_index

    return lst[:start + 1] + [x for x in lst[start + 1:end] if x % 3 != 0] + lst[end:]


def main():
    """Основная функция программы"""
    choice = input("Выберите способ ввода (1 - вручную, 2 - случайная генерация): ")

    if choice == '1':
        A = get_list_from_input()
    elif choice == '2':
        A = get_list_from_random()
        print("Сгенерированный список:", A)
    else:
        print("Некорректный выбор! Выход из программы.")
        return

    print("Результат без стандартных функций:", remove_multiples_of_three_no_std(A))
    print("Результат со стандартными функциями:", remove_multiples_of_three_std(A))


if __name__ == "__main__":
    main()

