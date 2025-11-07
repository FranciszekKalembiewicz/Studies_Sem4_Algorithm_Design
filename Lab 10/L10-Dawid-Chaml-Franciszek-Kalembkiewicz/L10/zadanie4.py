from typing import List


def positional_sort(matrix: List[List[int]]) -> List[List[int]]:
    """
    Sortuje wiersze macierzy według pozycyjnie: najpierw kolumna 0, potem 1 itd.
    Zwraca nową, posortowaną macierz.
    """
    # Używamy sortowania stabilnego i klucza tuple wiersza
    return sorted(matrix, key=lambda row: tuple(row))


if __name__ == '__main__':
    print("Czy chcesz użyć domyślnej macierzy? (t/n)")
    wybor = input().strip().lower()
    if wybor == 't':
        # Domyślona macierz M=4, N=3
        macierz = [
            [100111, 111011, 111101],
            [100111, 101011, 111011],
            [101011,   1111, 101000],
            [110011, 100001, 101101]
        ]
    else:
        # Wczytywanie od użytkownika
        first = input("Podaj ilość wierszy i kolumn (M N): ").strip().split()
        if len(first) != 2:
            raise ValueError("Podaj dwie liczby: M i N")
        M, N = map(int, first)
        macierz = []
        for i in range(M):
            row = input(
                f"Wiersz {i+1}/{M} (oddzielone spacją): ").strip().split()
            if len(row) != N:
                raise ValueError(
                    f"Wiersz musi mieć {N} elementów, podałeś: {row}")
            macierz.append(list(map(int, row)))

    print("Oryginalna macierz:")
    for w in macierz:
        print(w)

    posortowana = positional_sort(macierz)

    print("Posortowana macierz:")
    for w in posortowana:
        print(w)
