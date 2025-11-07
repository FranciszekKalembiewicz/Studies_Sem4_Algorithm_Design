from cli import read_robots, choose_param, parse_list_values
from search_algos import binary_search


def main():
    # Wczytanie danych
    robots = read_robots()
    if not robots:
        print("Brak danych o robotach.")
        return

    # 1) Wybór parametru
    param, idx = choose_param()

    # 2) Pobranie listy dopuszczalnych wartości
    raw = input(
        f"Podaj dopuszczalne wartości dla '{param}' (oddzielone przecinkami): ")
    allowed = parse_list_values(raw, param)

    # 3) Sortowanie po wybranym parametrze
    robots.sort(key=lambda r: r[idx])

    # 4) Wyszukiwanie binarne po każdej wartości
    for val in allowed:
        pos = binary_search(robots, idx, val)
        if pos != -1:
            print("Znaleziono robota:", robots[pos])
            return

    print("brak")


if __name__ == "__main__":
    main()
