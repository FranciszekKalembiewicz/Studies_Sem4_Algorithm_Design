from dataclasses import dataclass
from typing import List


@dataclass
class Robot:
    fields: List[str]

    def __post_init__(self):
        # Zakładamy, że zasięg jest w trzeciej kolumnie (index 2)
        try:
            self.range = int(self.fields[2])
        except (IndexError, ValueError):
            raise ValueError(f"Nieprawidłowy zasięg w wierszu: {self.fields}")

    def __repr__(self):
        name = self.fields[0]
        return f"{name}: zasięg={self.range}"


def load_robots(filename: str, delimiter: str = ';') -> List[Robot]:
    robots: List[Robot] = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(delimiter)
            if len(parts) < 3:
                parts = line.split()
            if len(parts) < 3:
                raise ValueError(
                    f"Nieprawidłowy wiersz (za mało kolumn): {line}")
            robots.append(Robot(parts))
    return robots


def counting_sort_list(arr: List[int]) -> List[int]:
    if not arr:
        return []
    min_v = min(arr)
    max_v = max(arr)
    k = max_v - min_v + 1
    count = [0] * k
    for x in arr:
        count[x - min_v] += 1
    for i in range(1, k):
        count[i] += count[i-1]
    output = [0] * len(arr)
    for x in reversed(arr):
        idx = x - min_v
        count[idx] -= 1
        output[count[idx]] = x
    return output


def counting_sort_robots(robots: List[Robot]) -> List[Robot]:
    if not robots:
        return []
    min_r = min(r.range for r in robots)
    max_r = max(r.range for r in robots)
    k = max_r - min_r + 1
    count = [0] * k
    for r in robots:
        count[r.range - min_r] += 1
    for i in range(1, k):
        count[i] += count[i-1]
    output: List[Robot] = [None] * len(robots)
    for r in reversed(robots):
        idx = r.range - min_r
        count[idx] -= 1
        output[count[idx]] = r
    return output


def run():
    print("Wybierz opcję:")
    print("1) Sortowanie przykładowej listy liczb")
    print("2) Sortowanie floty robotów względem zasięgu")
    choice = input("Twój wybór (1/2): ").strip()
    if choice == '1':
        sample = [6, 3, 6, 1, 4, 9, 0, 1, 8, 2, 6, 4, 9, 3, 7, 5,
                  9, 2, 7, 3, 2, 4, 1, 8, 7, 0, 8, 5, 8, 3, 6, 2, 5, 3]
        print(f"Oryginalna lista: {sample}")
        sorted_list = counting_sort_list(sample)
        print(f"Posortowana lista: {sorted_list}")
    elif choice == '2':
        filename = input(
            "Podaj nazwę pliku z robotami (np. roboty.txt): ").strip()
        robots = load_robots(filename)
        print("Oryginalna flota robotów (nazwa:zasięg):")
        for r in robots:
            print(r)
        sorted_robots = counting_sort_robots(robots)
        print("\nPosortowana flota robotów:")
        for r in sorted_robots:
            print(r)
        out = input("Podaj nazwę pliku wyjściowego: ").strip()
        with open(out, 'w', encoding='utf-8') as f:
            for r in sorted_robots:
                f.write(';'.join(r.fields) + "\n")
        print(f"Zapisano wynik do {out}")
    else:
        print("Nieprawidłowy wybór. Kończę.")


if __name__ == '__main__':
    run()
