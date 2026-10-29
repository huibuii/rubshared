def dh_values(p, g, a, b):
    # Implement here
    A = pow(g, a, p)
    B = pow(g, b, p)
    kA = pow(A, b, p)
    kB=pow(B, a, p)
    return A, B, kA, kB
    pass


def discrete_log(p, g, value):
    # Implement here
    for i in range(0, p-2):
        temp = pow(g, i, p)
        if temp == value:
            return i
    return None
    pass


def passive_key(p, g, A, B):
    # Implement here
    a = discrete_log(p,g,A)
    kAB = pow(B, a, p)
    return kAB
    pass


if __name__ == "__main__":
    assert dh_values(23, 5, 6, 15) == (8, 19, 2, 2)
    assert discrete_log(23, 5, 8) == 6
    assert discrete_log(23, 5, 1) == 0
    assert discrete_log(23, 4, 5) is None
    assert passive_key(23, 5, 8, 19) == 2
    assert dh_values(29, 2, 3, 4) == (8, 16, 7, 7)
    print("Alle Selbsttests bestanden.")
