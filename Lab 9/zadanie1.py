from cli import read_robots


def matches(robot, criteria):
    """
    Sprawdza, czy pojedynczy robot pasuje do listy kryteriów.
    """
    for val, crit in zip(robot, criteria):
        if crit is None:
            continue
        if isinstance(crit, list):
            if val not in crit:
                return False
        else:
            if val != crit:
                return False
    return True


def linear_search(robots, criteria):
    """
    Wyszukiwanie liniowe: zwraca pierwszy robota pasującego do kryteriów lub None.
    """
    for rob in robots:
        if matches(rob, criteria):
            return rob
    return None


def main():
    robots = read_robots()
    if not robots:
        print("Brak danych o robotach.")
        return

    # Testy Z1
    criteria1 = ["AGV", None, [39, 40, 41, 42, 43], None]
    criteria2 = ["AFV", 6353, 30, 0]

    result1 = linear_search(robots, criteria1)
    result2 = linear_search(robots, criteria2)

    print("Test 1:", result1 if result1 else "brak")
    print("Test 2:", result2 if result2 else "brak")


if __name__ == "__main__":
    main()
