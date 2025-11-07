from cli import read_robots, choose_param, read_alpha, choose_probing, parse_single_value
from search_algos import build_open, search_open


def main():
    # 1) Wczytanie danych
    robots = read_robots()
    if not robots:
        print("Brak danych o robotach.")
        return

    # 2) Wybór parametru do haszowania
    param, idx = choose_param()

    # 3) Wczytanie parametru α (load factor)
    alpha = read_alpha()

    # 4) Wybór metody sondowania
    probing = choose_probing()

    # 5) Budowa tablicy otwartego adresowania
    table = build_open(robots, idx, alpha, probing)
    print(
        f"Utworzono tablicę otwartego adresowania [{probing}] o rozmiarze {len(table)}.")

    # 6) Wczytanie wartości do wyszukania
    raw = input(f"Podaj wartość parametru '{param}' do wyszukania: ")
    try:
        target = parse_single_value(raw, param)
    except ValueError as e:
        print(e)
        return

    # 7) Wyszukiwanie w tablicy
    result = search_open(table, idx, target, probing)
    if result:
        print("Znaleziono robota:", result)
    else:
        print("brak")


if __name__ == "__main__":
    main()
