from dataclasses import dataclass
from typing import List


@dataclass
class Robot:
    fields: List[str]  # pełna lista kolumn jako stringi

    def __post_init__(self):
        # Cena w drugiej kolumnie (index 1)
        try:
            self.price = float(self.fields[1])
        except (IndexError, ValueError):
            raise ValueError(f"Nieprawidłowa cena w wierszu: {self.fields}")

    def __repr__(self):
        # Wyświetlamy nazwę i cenę dla czytelności logu
        name = self.fields[0]
        return f"{name}: {self.price}"


def load_robots(filename: str, delimiter: str = ';') -> List[Robot]:
    robots: List[Robot] = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split(delimiter)
            if len(parts) < 2:
                parts = line.split()
            if len(parts) < 2:
                raise ValueError(
                    f"Nieprawidłowy wiersz (za mało kolumn): {line}")

            robots.append(Robot(parts))
    return robots


def save_robots(robots: List[Robot], filename: str, delimiter: str = ';'):
    with open(filename, 'w', encoding='utf-8') as f:
        for r in robots:
            f.write(delimiter.join(r.fields) + "\n")


def print_heap(arr: List[Robot], size: int):
    # Wyświetla kopiec jako lista indeksów i cen, z limitem do 20 wierszy
    limit = min(size, 20)
    print(f"Kopiec (rozmiar = {size}), pokazuję pierwsze {limit} elementów:")
    for i in range(limit):
        print(f"[{i}] {arr[i]}")
    if size > limit:
        print(f"... oraz jeszcze {size - limit} elementów")
    print()


def heapify(arr: List[Robot], n: int, i: int, step: bool = False):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left].price > arr[largest].price:
        largest = left
    if right < n and arr[right].price > arr[largest].price:
        largest = right

    if largest != i:
        # Logujemy tylko zamianę dwóch węzłów
        if step:
            print(
                f"Zamiana: indeks {i} ({arr[i].price}) <-> indeks {largest} ({arr[largest].price})")
            print_heap(arr, n)
            input("Naciśnij Enter, aby kontynuować...")
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest, step)


def heap_sort(arr: List[Robot], step: bool = False) -> List[Robot]:
    n = len(arr)

    if step:
        print("=== Budowanie kopca maksymalnego ===")
        print_heap(arr, n)
        input("Enter: start heapify batched")
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i, step)
        # Usunięto dodatkowe podsumowanie stanu kopca, żeby uniknąć duplikatów

    if step:
        print("=== Ekstrakcja elementów ===")
        input("Enter: rozpocznij wydobycie")
    for i in range(n - 1, 0, -1):
        if step:
            print(
                f"Wymieniam korzeń z elementem na indeksie {i}: {arr[0].price} <-> {arr[i].price}")
            print_heap(arr, i+1)
            input("Enter: po zamianie, przed heapify")
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0, step)
        # Usunięto dodatkowe podsumowanie po wydobyciu, zostaje tylko heapify logika

    return arr


def run(input_file: str = 'roboty.txt', output_file: str = 'heap_sort.txt', delimiter: str = ';', step: bool = False):
    roboty = load_robots(input_file, delimiter)
    if step:
        print("Wczytane roboty:")
        for idx, r in enumerate(roboty):
            print(f"[{idx}] {r}")
        print()
        input("Enter: przed budową kopca")

    posortowane = heap_sort(roboty, step)

    print("\nPosortowane roboty:")
    for r in posortowane:
        print(r)

    save_robots(posortowane, output_file, delimiter)
    if step:
        print(f"\nZapisano posortowaną listę do {output_file}")


if __name__ == '__main__':
    run(step=True)
