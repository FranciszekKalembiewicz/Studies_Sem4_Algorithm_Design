import math

# ----------------------------------------
# Algorytmy wyszukiwania i budowy struktur
# ----------------------------------------


def binary_search(robots, idx, target):
    """
    Wyszukiwanie binarne po liście posortowanej wg robots[*][idx].
    Zwraca index znalezionego elementu lub -1.
    """
    lo, hi = 0, len(robots) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        val = robots[mid][idx]
        if val == target:
            return mid
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1

# -----------------------
# Hash chaining (łańcuchy)
# -----------------------


def build_chain(robots, idx, alpha):
    """
    Tworzy tablicę z łańcuchowaniem:
      - robots: lista krotek
      - idx: indeks pola jako klucz
      - alpha: docelowy load factor (>0)
    Zwraca listę bucketów (każdy to lista elementów).
    """
    n = len(robots)
    if alpha <= 0:
        raise ValueError("Load factor α musi być > 0.")
    m = max(1, math.ceil(n / alpha))
    table = [[] for _ in range(m)]
    for rob in robots:
        h = hash(rob[idx]) % m
        table[h].append(rob)
    return table


def search_chain(table, idx, target):
    """
    Przeszukuje tablicę łańcuchową i zwraca pierwszy element,
    którego element[idx] == target, lub None.
    """
    m = len(table)
    h = hash(target) % m
    for rob in table[h]:
        if rob[idx] == target:
            return rob
    return None

# --------------------------------
# Open addressing (otwarte adresowanie)
# --------------------------------


def my_hash(key, m):
    """
    Prosta funkcja haszująca:
      - str: suma kodów ASCII % m
      - int/float: int(key) % m
    """
    if isinstance(key, str):
        return sum(ord(c) for c in key) % m
    elif isinstance(key, (int, float)):
        return int(key) % m
    else:
        raise TypeError(f"Nieobsługiwany typ klucza: {type(key)}")


def insert_with_probing(table, rob, idx, probing='quadratic'):
    """
    Wstawia element rob do tablicy table używając sondowania:
      - 'linear':   h = (h0 + i)
      - 'quadratic': h = (h0 + i*i)
    Zwraca True jeśli wstawiono sukcesem, False jeśli wymaga rehash.
    """
    m = len(table)
    key = rob[idx]
    h0 = my_hash(key, m)
    for i in range(m):
        if probing == 'linear':
            h = (h0 + i) % m
        else:
            h = (h0 + i*i) % m
        if table[h] is None:
            table[h] = rob
            return True
    return False


def resize_and_rehash(robots, idx, alpha, probing='quadratic'):
    """
    Iteracyjnie zwiększa rozmiar tablicy i rehaszuje wszystkie elementy,
    aż uda się wstawić każdy element bez konfliktu.
    """
    n = len(robots)
    # rozpocznij od dwukrotności minimalnego rozmiaru
    new_m = max(1, math.ceil(n / alpha)) * 2
    while True:
        table = [None] * new_m
        success = True
        for rob in robots:
            if not insert_with_probing(table, rob, idx, probing):
                success = False
                break
        if success:
            return table
        # zwiększ rozmiar i spróbuj ponownie
        new_m *= 2


def build_open(robots, idx, alpha, probing='quadratic'):
    """
    Tworzy tablicę otwartego adresowania:
      - robots: lista krotek
      - idx: indeks pola jako klucz
      - alpha: load factor
      - probing: 'linear' lub 'quadratic'
    Autorehash jeśli początkowo pełna.
    """
    n = len(robots)
    if alpha <= 0:
        raise ValueError("Load factor α musi być > 0.")
    # początkowy rozmiar
    m = max(1, math.ceil(n / alpha))
    table = [None] * m
    # spróbuj wstawić wszystkie
    if all(insert_with_probing(table, rob, idx, probing) for rob in robots):
        return table
    # jeśli się nie udało, rehash iteracyjnie
    return resize_and_rehash(robots, idx, alpha, probing)


def search_open(table, idx, target, probing='quadratic'):
    """
    Wyszukuje pierwszy element w tablicy otwartego adresowania,
    którego element[idx] == target. Zwraca krotkę lub None.
    """
    m = len(table)
    h0 = my_hash(target, m)
    for i in range(m):
        if probing == 'linear':
            h = (h0 + i) % m
        else:
            h = (h0 + i*i) % m
        entry = table[h]
        if entry is None:
            return None
        if entry[idx] == target:
            return entry
    return None
