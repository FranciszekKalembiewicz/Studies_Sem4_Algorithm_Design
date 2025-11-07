from cli import read_robots
from search_algos import build_chain, search_chain, build_open, search_open
import time
import math
import matplotlib.pyplot as plt


def main():
    # 1) Wczytanie robotów
    robots = read_robots()
    if not robots:
        print("Brak danych o robotach.")
        return

    # 2) Zapewnienie unikatowości cen (dodanie małego offsetu w razie duplikatów)
    seen = {}
    unique_robots = []
    for typ, cena, zasieg, kamera in robots:
        if cena in seen:
            seen[cena] += 1
            cena = cena + seen[cena] * 1e-6
        else:
            seen[cena] = 0
        unique_robots.append((typ, cena, zasieg, kamera))
    robots = unique_robots

    # 3) Sortowanie po cenie i przygotowanie listy cen
    robots.sort(key=lambda r: r[1])
    prices = [r[1] for r in robots]

    # 4) Pobranie zestawu wartości load factor α
    raw = input(
        "Podaj wartości load factor α oddzielone przecinkami (np. 0.5,1.0,2.0): ")
    try:
        alphas = [float(x.strip()) for x in raw.split(',') if x.strip()]
    except ValueError:
        print("Błędny format wartości α.")
        return

    # 5) Pomiar czasu wyszukiwania dla łańcuchowania i open addressing
    avg_chain = []
    avg_open = []
    for alpha in alphas:
        # Budowa struktur
        table_chain = build_chain(robots, 1, alpha)
        table_open = build_open(robots, 1, alpha, probing='quadratic')

        total_chain = 0.0
        total_open = 0.0
        # Wyszukiwanie po każdej cenie
        for price in prices:
            start = time.perf_counter()
            _ = search_chain(table_chain, 1, price)
            total_chain += time.perf_counter() - start

            start = time.perf_counter()
            _ = search_open(table_open, 1, price, probing='quadratic')
            total_open += time.perf_counter() - start

        avg_chain.append(total_chain / len(prices))
        avg_open.append(total_open / len(prices))

    # 6) Wykres porównawczy
    plt.figure()
    plt.plot(alphas, avg_chain, marker='o', label='Łańcuchowanie')
    plt.plot(alphas, avg_open, marker='x',
             label='Otwarte adresowanie (kwadratowe sondowanie)')
    plt.xlabel('Load factor α')
    plt.ylabel('Średni czas wyszukiwania [s]')
    plt.title('Porównanie prędkości algorytmów wyszukiwania')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
