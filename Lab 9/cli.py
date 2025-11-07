import math
import os

param_map = {'typ': 0, 'cena': 1, 'zasieg': 2, 'kamera': 3}


def read_robots():
    # Funkcja wczytująca flotę robotów z pliku
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "roboty.txt")

    if not os.path.exists(file_path):
        print(f"Plik '{file_path}' nie istnieje.")
        return []

    robots = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            typ, cena, zasieg, kamera = line.split()
            robots.append((typ, float(cena), int(zasieg), int(kamera)))
    return robots


def choose_param():
    while True:
        p = input("Wybierz parametr (typ, cena, zasieg, kamera): ").strip().lower()
        if p in param_map:
            return p, param_map[p]
        print("Nieznany parametr, spróbuj ponownie.")


def read_alpha(prompt="Podaj load factor α (np. 0.5,1.0,2.0): "):
    while True:
        try:
            a = float(input(prompt))
            if a > 0:
                return a
            print("α musi być > 0.")
        except ValueError:
            print("Niepoprawna wartość.")


def choose_probing():
    """
    Pyta użytkownika o metodę sondowania:
    - 'l'  => 'linear'
    - 'q'  => 'quadratic'
    Zwraca string z nazwą metody.
    """
    while True:
        p = input("Sondowanie ('l' = linear, 'q' = quadratic): ").strip().lower()
        if p == 'l':
            return 'linear'
        if p == 'q':
            return 'quadratic'
        print("Niepoprawna opcja. Wpisz 'l' lub 'q'.")


def parse_list_values(raw, param):
    parts = [x.strip() for x in raw.split(',') if x.strip()]
    if param == 'typ':
        return parts
    if param == 'cena':
        return [float(x) for x in parts]
    return [int(x) for x in parts]


def parse_single_value(raw, param):
    raw = raw.strip()
    if param == 'typ':
        return raw
    if param == 'cena':
        return float(raw)
    return int(raw)
