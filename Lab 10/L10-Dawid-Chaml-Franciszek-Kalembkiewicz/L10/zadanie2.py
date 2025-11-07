from dataclasses import dataclass
from typing import List, Literal

MAX_LOG = 10  # maksymalna liczba cen do wyświetlenia w logu


@dataclass
class Robot:
    fields: List[str]

    def __post_init__(self):
        try:
            self.price = float(self.fields[1])
        except (IndexError, ValueError):
            raise ValueError(f"Nieprawidłowa cena w wierszu: {self.fields}")

    def __repr__(self):
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


def log_prices(arr: List[Robot], low: int, high: int):
    prices = [r.price for r in arr[low:high+1]]
    n = len(prices)
    to_show = prices[:MAX_LOG]
    more = n - len(to_show)
    log = to_show + (['...'] if more > 0 else [])
    print(
        f"Ceny indeksy [{low}:{high}] (pierwsze {len(to_show)} z {n}): {log}")


def partition_lomuto(arr: List[Robot], low: int, high: int, step: bool) -> int:
    pivot = arr[high].price
    i = low - 1
    if step:
        print(f"Lomuto partycja dla podzakresu [{low}:{high}], pivot={pivot}")
    for j in range(low, high):
        if arr[j].price <= pivot:
            i += 1
            if step:
                print(
                    f"Zamiana arr[{i}] ({arr[i].price}) <-> arr[{j}] ({arr[j].price})")
            arr[i], arr[j] = arr[j], arr[i]
            if step:
                log_prices(arr, low, high)
                input("Naciśnij Enter...")
    arr[i+1], arr[high] = arr[high], arr[i+1]
    if step:
        print(f"Przenoszę pivot na pozycję {i+1}")
        log_prices(arr, low, high)
        input("Naciśnij Enter...")
    return i + 1


def partition_hoare(arr: List[Robot], low: int, high: int, step: bool) -> int:
    pivot = arr[(low + high) // 2].price
    i, j = low, high
    if step:
        print(f"Hoare partycja dla podzakresu [{low}:{high}], pivot={pivot}")
    while True:
        while arr[i].price < pivot:
            i += 1
        while arr[j].price > pivot:
            j -= 1
        if i >= j:
            if step:
                print(f"Hoare zwraca indeks {j}")
                input("Naciśnij Enter...")
            return j
        if step:
            print(
                f"Zamiana arr[{i}] ({arr[i].price}) <-> arr[{j}] ({arr[j].price})")
        arr[i], arr[j] = arr[j], arr[i]
        if step:
            log_prices(arr, low, high)
            input("Naciśnij Enter...")
        i += 1
        j -= 1


def quicksort(arr: List[Robot], low: int, high: int,
              step: bool = False,
              partycja: Literal['hoare', 'lomuto'] = 'hoare'):
    if low < high:
        if step:
            log_prices(arr, low, high)
            input("Naciśnij Enter, aby kontynuować partycjonowanie...")
        if partycja == 'lomuto':
            p = partition_lomuto(arr, low, high, step)
            quicksort(arr, low, p-1, step, partycja)
            quicksort(arr, p+1, high, step, partycja)
        else:
            p = partition_hoare(arr, low, high, step)
            quicksort(arr, low, p, step, partycja)
            quicksort(arr, p+1, high, step, partycja)


def run(input_file: str = 'roboty.txt',
        output_file: str = 'quick_sort.txt',
        delimiter: str = ';',
        step: bool = False,
        partycja: str = 'hoare'):
    robots = load_robots(input_file, delimiter)
    if step:
        print("Wczytane ceny:", [r.price for r in robots])
        input("Naciśnij Enter, aby rozpocząć sortowanie...")
    quicksort(robots, 0, len(robots)-1, step, partycja)
    print("\nPosortowane roboty:")
    for r in robots:
        print(r)
    save_robots(robots, output_file, delimiter)
    if step:
        print(f"\nZapisano posortowaną listę do {output_file}")


if __name__ == '__main__':
    # Przykład: run(step=True, partycja='lomuto')
    run(step=True, partycja='hoare')
