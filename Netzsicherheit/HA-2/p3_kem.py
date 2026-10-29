from hashlib import sha256


def derive_key(shared, p):
    length = (p.bit_length() + 7) // 8
    data = shared.to_bytes(length, "big")
    return sha256(data).digest()


def encapsulate(p, g, public_b, a):
    # Implement here
    X = pow(g,a,p)
    shared = pow(public_b, a, p)
    key = derive_key(shared, p)
    return X, key
    pass


def decapsulate(p, b, X):
    # Implement here
    k = pow(X, b, p)
    key = derive_key(k, p)
    return key
    pass


def has_repeated_x(values):
    # Implement here
    if len(values) != len(set(values)):
        return True
    return False
    pass


if __name__ == "__main__":
    X, key = encapsulate(23, 5, 19, 6)
    assert X == 8
    assert key == derive_key(2, 23)
    assert key == decapsulate(23, 15, X)
    assert encapsulate(23, 5, 19, 6) == (X, key)
    X2, key2 = encapsulate(23, 5, 19, 7)
    assert X2 == 17
    assert key2 == decapsulate(23, 15, X2)
    assert key2 != key
    assert has_repeated_x([X, X2, X]) is True
    assert has_repeated_x([X, X2]) is False
    assert has_repeated_x([]) is False
    print("Alle Selbsttests bestanden.")
