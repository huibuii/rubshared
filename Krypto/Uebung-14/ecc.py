class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.is_infinity = (x is None and y is None)

    def __str__(self):
        if self.is_infinity:
            return "O (point at infinity)"
        return f"({self.x}, {self.y})"

class Curve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def __str__(self):
        return f"({self.a}, {self.b}, {self.p})"

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
    a = a % p  # Normalize in case a >= p or a is negative
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



def pointaddition(P:Point, Q:Point, p):

    yu = (Q.y - P.y) % p
    xu = (Q.x - P.x) % p
    xuinv = modular_inverse(xu, p)
    s = yu * xuinv % p
    # calc new point
    xnew = (s**2 - P.x - Q.x) % p
    ynew = (s * (P.x - xnew) - P.y) % p
    return Point(xnew, ynew)


def pointdoubling(P:Point, a, p):

    xu = (3*P.x**2 + a) % p
    yu = (2*P.y) % p
    yinv = modular_inverse(yu, p)

    s = xu * yinv % p
    # calc new point
    xnew = (s**2 - 2*P.x) % p
    ynew = (s * (P.x - xnew) - P.y) % p
    return Point(xnew, ynew)


import sys

def print_help():
    print("ECC Group Operations")
    print("====================")
    print("Usage:   python ecc.py -P <(x,y)> -Q <(x,y)> -E <(a,b,p)>")
    print()
    print("Parameters:")
    print("  -P        : coordinates of point P")
    print("  -Q        : coordinates of point Q")
    print("  -E    : curve parameters of y\u00B2 = x\u00B3 + ax + b")
    print()
    print("Example:  python ecc.py -P \"(1,2)\" -Q \"(1,3)\" -E \"(4,7,41)\"")


if __name__ == "__main__":
    argv = __import__("sys").argv
    if len(argv) == 1 or "--help" in argv or "-h" in argv:
        print_help()
        raise SystemExit(0)

    values = argv[1:]
    i = 0
    P = None
    Q = None
    E = None
    while i < len(values) - 1:
        match values[i]:
            case "-P":
                pv = values[i + 1].strip("()").split(",")
                if len(pv) != 2:
                    P = Point()
                else:
                    P = Point(int(pv[0]), int(pv[1]))
                print("Point P: ", P)
            case "-Q":
                qv = values[i + 1].strip("()").split(",")
                if len(qv) != 2:
                    Q = Point()
                else:
                    Q = Point(int(qv[0]), int(qv[1]))
                print("Point Q: ", Q)
            case "-E":
                ev = values[i + 1].strip("()").split(",")
                if len(ev) != 3:
                    print(f"wrong input for curve: {values[i + 1]}")
                    raise SystemExit(1)
                E = Curve(int(ev[0]), int(ev[1]), int(ev[2]))
                print(f"Curve E: y\u00B2 = x\u00B3 + {E.a}x + {E.b} mod {E.p}")
            case _:
                print(f"unknown parameter: {values[i]}")
                raise SystemExit(1)
        i += 2

    if P is None:
        print(f"P is missing")
        raise SystemExit(1)
    if Q is None:
        print(f"Q is missing")
    if E is None:
        print(f"E is missing")
        raise SystemExit(1)

    checkcurve(E.a, E.b, E.p)


    if Q.is_infinity:
        """addition mit 0 """
        print(P)
        raise SystemExit(0)
    elif P.is_infinity:
        print(Q)
        raise SystemExit(0)

    if Q.x == P.x and Q.y == -P.y:
       R = Point()
       print(R)
       raise SystemExit(0)


    if P.x == Q.x and P.y == Q.y:
        """pointdoubling"""
        print("Point doubling, R: ", pointdoubling(P, E.a, E.p))
        raise SystemExit(0)
    else:
        """pointaddition"""
        print("Point addition, R: ", pointaddition(P, Q, E.p))
        raise SystemExit(0)