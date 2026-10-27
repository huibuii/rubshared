def dh_values(p, g, a, b):
    # Implement here
    pass


def discrete_log(p, g, value):
    # Implement here
    pass


def passive_key(p, g, A, B):
    # Implement here
    pass


if __name__ == "__main__":
    assert dh_values(23, 5, 6, 15) == (8, 19, 2, 2)
    assert discrete_log(23, 5, 8) == 6
    assert discrete_log(23, 5, 1) == 0
    assert discrete_log(23, 4, 5) is None
    assert passive_key(23, 5, 8, 19) == 2
    assert dh_values(29, 2, 3, 4) == (8, 16, 7, 7)
    print("Alle Selbsttests bestanden.")
