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


def pointdoubling(x, y, a, p):

    xu = (3*x**2 + a) % p
    yu = (2*y) % p
    yinv = modular_inverse(yu, p)

    s = xu * yinv % p
    # calc new point
    xnew = (s**2 - 2*x) % p
    ynew = (s * (x - xnew) - y) % p
    return xnew, ynew

def edgecases(x1, y1, x2, y2):



    if x1 ==0 and y1 == 0 or x2 == 0 and y2 == 0:
        """addition mit 0 """

    if y2 == -y1 or y1 == -y2:
       """return 0"""

    if x1 == x2 and y1 == y2:
        """pointdoubling"""
    else:
        """pointaddition"""
