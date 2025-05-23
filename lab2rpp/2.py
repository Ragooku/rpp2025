import numpy as np


def generate_matrix(n: int, m: int, low: int = 0, high: int = 10) -> np.ndarray:
    """Генерирует матрицу размера n x m со случайными целыми числами в диапазоне [low, high)."""
    return np.random.randint(low, high, (n, m))


def remove_row(matrix: np.ndarray, l: int) -> np.ndarray:
    """
    Исключает строку с индексом l из матрицы и возвращает новую матрицу.
    """
    return np.delete(matrix, l, axis=0)


def save_to_file(filename: str, original: np.ndarray, modified: np.ndarray):
    """
    Сохраняет исходную и обработанную матрицу в файл.
    """
    with open(filename, 'w') as f:
        f.write("Исходная матрица:\n")
        np.savetxt(f, original, fmt='%d')
        f.write("\nМатрица после удаления строки:\n")
        np.savetxt(f, modified, fmt='%d')


def main():
    # Задаем размеры матрицы и индекс удаляемой строки
    n, m, l = 5, 4, 2  # Можно изменить параметры

    # Генерация матрицы
    matrix = generate_matrix(n, m)
    print("Исходная матрица:")
    print(matrix)

    # Удаление строки
    modified_matrix = remove_row(matrix, l)
    print("\nМатрица после удаления строки:")
    print(modified_matrix)

    # Сохранение результатов в файл
    save_to_file("matrix_result.txt", matrix, modified_matrix)


if __name__ == "__main__":
    main()
