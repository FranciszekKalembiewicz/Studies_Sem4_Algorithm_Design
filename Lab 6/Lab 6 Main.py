import math
import random
import time
import matplotlib.pyplot as plt

#! Zadanie 1


def prime_factors(n):
    if n <= 1:
        return []
    # Sprawdzamy dzielniki od 2 do sqrt(n)
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            # Znaleziono dzielnik – rekurencyjnie faktoryzujemy obie części
            return prime_factors(i) + prime_factors(n // i)
    # Jeśli żaden dzielnik nie pasuje, n jest liczbą pierwszą
    return [n]

#! Zadanie 2: Sito Eratostenesa


def sieve_eratosthenes(p):
    sieve = [True] * (p + 1)
    sieve[0:2] = [False, False]  # 0 i 1 nie są pierwsze
    for i in range(2, int(math.sqrt(p)) + 1):
        if sieve[i]:
            # Wykluczamy wielokrotności i
            for j in range(i * i, p + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

#! Zadanie 3.1: Największy wspólny dzielnik (NWD)
# ? Metoda 1: Algorytm Euklidesa


def gcd_euclid(a, b):
    while b:
        a, b = b, a % b
    return a

# ? Metoda 2: Rozkład na czynniki pierwsze


def gcd_by_factors(a, b):
    """
    Oblicza NWD(a, b) przez rozkład na czynniki:
    bierze iloczyn wspólnych czynników.
    """
    fa = prime_factors(a)
    fb = prime_factors(b)
    common = []
    # Dla każdej unikalnej podstawy uwzględniamy min(krotności)
    for p in set(fa):
        common += [p] * min(fa.count(p), fb.count(p))
    result = 1
    for p in common:
        result *= p
    return result

#! Zadanie 3.2: Testy wydajności


def performance_test(n, m):
    qs = list(range(1, m + 1))
    times_factor = []
    times_euclid = []
    for q in qs:
        start = time.time()
        gcd_by_factors(n, q)
        times_factor.append(time.time() - start)
        start = time.time()
        gcd_euclid(n, q)
        times_euclid.append(time.time() - start)
    # Rysujemy wykres porównawczy
    plt.plot(qs, times_factor, label='RNWD (rozklad)')
    plt.plot(qs, times_euclid, label='ENWD (Euklides)')
    plt.xlabel('q')
    plt.ylabel('czas [s]')
    plt.legend()
    plt.title(f'Porównanie RNWD i ENWD dla n={n}')
    plt.show()

#! Zadanie 4: Probabilistyczne testy pierwszości
# Szybkie potęgowanie modulo


def mod_pow(a, d, n):
    """Oblicza (a^d) mod n efektywnie przy użyciu potęgowania binarnego."""
    result = 1
    a = a % n
    while d > 0:
        if d & 1:
            result = (result * a) % n
        a = (a * a) % n
        d >>= 1
    return result

# Test Fermata


def is_prime_fermat(p, k=5):
    """
    Test Fermata: sprawdzamy, czy a^(p-1) ≡ 1 (mod p)
    dla k losowych podstaw a.
    """
    if p < 4:
        return p in (2, 3)
    for _ in range(k):
        a = random.randrange(2, p - 1)
        if mod_pow(a, p - 1, p) != 1:
            return False
    return True

# Test Millera–Rabina


def is_prime_miller_rabin(p, k=5):
    """
    Test Millera–Rabina: rozkładamy p-1 = 2^s * d,
    a następnie wykonujemy k prób z losową podstawą a.
    """
    if p < 4:
        return p in (2, 3)
    # Rozkład p-1
    d = p - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(k):
        a = random.randrange(2, p - 1)
        x = mod_pow(a, d, p)
        if x in (1, p - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % p
            if x == p - 1:
                break
        else:
            return False
    return True

#! Zadanie 5: RSA
# Generowanie kluczy RSA


def generate_rsa_keys(p, q, e=65537):
    """
    Generuje klucze RSA (n, e, d) dla danych p, q i wykładnika e.
    """
    n = p * q
    phi = (p - 1) * (q - 1)
    if gcd_euclid(e, phi) != 1:
        raise ValueError("Wykładnik e nie jest względnie pierwszy z phi(n)")
    # Rozszerzony algorytm Euklidesa

    def egcd(a, b):
        if b == 0:
            return (1, 0)
        x1, y1 = egcd(b, a % b)
        return (y1, x1 - (a // b) * y1)
    x, y = egcd(e, phi)
    d = x % phi
    return n, e, d

# Szyfrowanie i odszyfrowanie pojedynczej liczby


def rsa_encrypt(m, e, n):
    """Szyfruje m jako c = m^e mod n."""
    return mod_pow(m, e, n)


def rsa_decrypt(c, d, n):
    """Odszyfrowuje c jako m = c^d mod n."""
    return mod_pow(c, d, n)


# Przykładowe uruchomienie wszystkich zadań
if __name__ == "__main__":
    # Zadanie 1
    print("Czynniki pierwsze 12:", prime_factors(12))
    print("Czynniki pierwsze 1500:", prime_factors(1500))

    # Zadanie 2
    print("Liczby pierwsze do 12:", sieve_eratosthenes(12))
    print("Liczby pierwsze do 130:", sieve_eratosthenes(130))

    # Zadanie 3.1
    print("GCD(12,20) Euklides:", gcd_euclid(12, 20),
          "rozklad:", gcd_by_factors(12, 20))
    print("GCD(630,2430) Euklides:", gcd_euclid(630, 2430),
          "rozklad:", gcd_by_factors(630, 2430))
    # Zadanie 3.2
    performance_test(10000, 200)  # odkomentuj, by zobaczyć wykres

    # Zadanie 4
    for val in [12, 1500]:
        print(f"Fermat({val}) ->", is_prime_fermat(val))
    for val in [12, 130]:
        print(f"Miller-Rabin({val}) ->", is_prime_miller_rabin(val))
    for val in [14021, 3001]:
        print(f"Fermat({val}) ->", is_prime_fermat(val),
              f"M-R({val}) ->", is_prime_miller_rabin(val))

    # Zadanie 5
    for p, q in [(2003, 3001), (191, 199)]:
        n, e, d = generate_rsa_keys(p, q)
        print(f"RSA dla p={p},q={q} -> n={n}, e={e}, d={d}")
        for k in [28981, 2213]:
            c = rsa_encrypt(k, e, n)
            m = rsa_decrypt(c, d, n)
            print(f"  k={k}: c={c}, m={m}")
        # Szyfrowanie tekstu przykład
        text = "ciekawy tekst"
        nums = [ord(ch) for ch in text]
        cipher = [rsa_encrypt(mv, e, n) for mv in nums]
        plain = ''.join(chr(rsa_decrypt(cv, d, n)) for cv in cipher)
        print("  tekst -> szyfr -> odszyfr:", plain)
