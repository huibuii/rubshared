def rsa_keys(p, q, e):
    # Implement here
    n=p*q
    phin=(p-1)*(q-1)
    d = pow(e, -1, phin)
    return (n, d)
    pass


def encrypt(m, e, n):
    # Implement here
    c = pow(m, e, n)
    return c
    pass


def decrypt(c, d, n):
    # Implement here
    m = pow(c, d, n)
    return m
    pass


def recover_message(c, e, n, r, oracle):
    # Implement here
    c2 = (c * pow(r, e, n)) % n
    m2 = oracle(c2)
    m = (m2 * pow(r, -1, n)) % n
    return m
    pass


def decrypt_oracle(c):
    if c == 15:
        raise ValueError("Der Zielchiffretext ist gesperrt.")
    return pow(c, 23, 187)


if __name__ == "__main__":
    assert rsa_keys(11, 17, 7) == (187, 23)
    assert encrypt(42, 7, 187) == 15
    assert decrypt(15, 23, 187) == 42
    assert decrypt(encrypt(11, 7, 187), 23, 187) == 11
    assert recover_message(15, 7, 187, 2, decrypt_oracle) == 42
    assert recover_message(15, 7, 187, 3, decrypt_oracle) == 42
    print("Alle Selbsttests bestanden.")
