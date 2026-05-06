def extended_gcd(a, b):
    """Returns (gcd, x, y) such that a*x + b*y = gcd."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y


def modular_inverse(a, p):
    """
    Calculates the modular inverse of a mod p.
    Returns x such that (a * x) % p == 1.

    Raises ValueError if the inverse does not exist
    (i.e. gcd(a, p) != 1).
    """
    a = a % p  # Normalise in case a >= p or a is negative
    gcd, x, _ = extended_gcd(a, p)

    if gcd != 1:
        raise ValueError(
            f"Modular inverse does not exist: gcd({a}, {p}) = {gcd}, "
            "inputs must be coprime."
        )

    return x % p  # Ensure the result is positive


if __name__ == "__main__":
    test_cases = [
        (3, 11),    # 3 * 4 = 12 ≡ 1 (mod 11)  → 4
        (10, 17),   # 10 * 12 = 120 ≡ 1 (mod 17) → 12
        (7, 26),    # 7 * 15 = 105 ≡ 1 (mod 26)  → 15
        (2, 4),     # No inverse: gcd(2,4) = 2
    ]

    for a, p in test_cases:
        try:
            inv = modular_inverse(a, p)
            print(f"modular_inverse({a}, {p}) = {inv}  →  verify: ({a} * {inv}) % {p} = {(a * inv) % p}")
        except ValueError as e:
            print(f"modular_inverse({a}, {p}) → Error: {e}")