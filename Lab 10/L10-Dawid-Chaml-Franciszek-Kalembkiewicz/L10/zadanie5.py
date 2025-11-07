"""
compare_sorts.py

Porównanie wizualne działania heap_sort i quick_sort (Hoare) na pliku roboty.txt.
"""
from typing import List, Callable
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

# Parametry wizualizacji
definitions = '''
MAX_LOG = 20      # liczba pierwszych elementów do wyświetlenia
STEP_LIMIT = 200  # maksymalna liczba kroków
PAUSE_TIME = 0.3  # przerwa między krokami
'''

MAX_LOG = 20
STEP_LIMIT = 200
PAUSE_TIME = 0.3


@dataclass
class Robot:
    fields: List[str]

    def __post_init__(self):
        self.price = float(self.fields[1])

    def __repr__(self):
        return f"{self.fields[0]}: {self.price}"


def load_robots(filename: str) -> List[Robot]:
    robots = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(';')
            if len(parts) < 2:
                parts = line.strip().split()
            if len(parts) < 2:
                continue
            robots.append(Robot(parts))
    return robots

# ===== Heap Sort z nagrywaniem =====


def heapify(arr, n, i, record):
    largest = i
    l, r = 2*i+1, 2*i+2
    if l < n and arr[l].price > arr[largest].price:
        largest = l
    if r < n and arr[r].price > arr[largest].price:
        largest = r
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        record([x.price for x in arr])
        heapify(arr, n, largest, record)


def heap_sort(arr: List[Robot], record: Callable[[List[float]], None]):
    n = len(arr)
    for i in range(n//2-1, -1, -1):
        heapify(arr, n, i, record)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        record([x.price for x in arr])
        heapify(arr, i, 0, record)

# ===== Quick Sort Hoare z nagrywaniem =====


def partition_hoare(arr, low, high, record):
    pivot = arr[(low+high)//2].price
    i, j = low, high
    while True:
        while arr[i].price < pivot:
            i += 1
        while arr[j].price > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]
        record([x.price for x in arr])
        i += 1
        j -= 1


def quick_sort(arr: List[Robot], low: int, high: int, record: Callable[[List[float]], None]):
    if low < high:
        p = partition_hoare(arr, low, high, record)
        quick_sort(arr, low, p, record)
        quick_sort(arr, p+1, high, record)

# ===== Wizualizacja =====


def visualize_sorts():
    robots = load_robots('roboty.txt')
    initial = [r.price for r in robots]

    heap_steps = [initial.copy()]
    quick_steps = [initial.copy()]

    def rec_heap(state):
        if len(heap_steps) < STEP_LIMIT:
            heap_steps.append(state[:MAX_LOG])

    def rec_quick(state):
        if len(quick_steps) < STEP_LIMIT:
            quick_steps.append(state[:MAX_LOG])

    heap_sort(robots.copy(), rec_heap)
    quick_sort(robots.copy(), 0, len(robots)-1, rec_quick)

    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    max_steps = max(len(heap_steps), len(quick_steps))
    for k in range(max_steps):
        ax1.clear()
        ax2.clear()
        if k < len(heap_steps):
            ax1.bar(range(len(heap_steps[k])), heap_steps[k])
            ax1.set_title(f'Heap Sort krok {k+1}/{len(heap_steps)}')
        else:
            ax1.text(0.5, 0.5, 'Koniec', ha='center', va='center')
        if k < len(quick_steps):
            ax2.bar(range(len(quick_steps[k])), quick_steps[k])
            ax2.set_title(f'Quick Sort krok {k+1}/{len(quick_steps)}')
        else:
            ax2.text(0.5, 0.5, 'Koniec', ha='center', va='center')
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(PAUSE_TIME)
    plt.ioff()
    plt.show()


if __name__ == '__main__':
    print('Rozpoczynam wizualizację z roboty.txt')
    visualize_sorts()
