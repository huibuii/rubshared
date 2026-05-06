from sympy import true


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


def checkcurve(a, b, p):

    a = 4 * a**3 % p
    b = 27 * b**2 % p
    res = (a + b) % p
    if res == 0:
        raise ValueError("the elliptic curve doesnt meet the requirements.")
    else:
        return True


def pointaddition(x1, y1, x2, y2, p):

    yu = (y2 - y1) % p
    xu = (x2 - x1) % p
    xuinv = modular_inverse(xu, p)
    s = yu * xuinv % p
    # calc new point
    xnew = (s**2 - x1 - x2) % p
    ynew = (s * (x1 - xnew) - y1) % p
    return xnew, ynew


