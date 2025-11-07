from cli import read_robots, choose_param, read_alpha, parse_single_value
from search_algos import build_chain, search_chain


def main():
    # 1) Wczytanie danych
    robots = read_robots()
    if not robots:
        print("Brak danych o robotach.")
        return

    # 2) Wybór parametru
    param, idx = choose_param()

    # 3) Wczytanie load factor α
    alpha = read_alpha()

    # 4) Budowa tablicy łańcuchowej
    table = build_chain(robots, idx, alpha)
    print(f"Utworzono tablicę łańcuchową o rozmiarze {len(table)}.")

    # 5) Wczytanie wartości do wyszukania
    raw = input(f"Podaj wartość parametru '{param}' do wyszukania: ")
    try:
        target = parse_single_value(raw, param)
    except ValueError as e:
        print(e)
        return

    # 6) Wyszukiwanie w łańcuchowaniu
    result = search_chain(table, idx, target)
    if result:
        print("Znaleziono robota:", result)
    else:
        print("brak")


if __name__ == "__main__":
    main()
