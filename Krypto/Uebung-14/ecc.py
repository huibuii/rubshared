class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.is_infinity = (x is None and y is None)

    def __str__(self):
        if self.is_infinity:
            return "O (point at infinity)"
        return f"({self.x}, {self.y})"

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
    print("Usage:   python ecc.py -P <(x,y)> -Q <(x,y)> -a <a> -b <b> -p <p>")
    print()
    print("Parameters:")
    print("  -P        : coordinates of point P")
    print("  -Q        : coordinates of point Q")
    print("  -a, -b    : curve parameters of y² = x³ + ax + b")
    print("  -p        : prime modulus")
    print()
    print("Example:  python script.py -P (1,2) -Q (1,3) -a 4 -b 7 -p 41")


def parse_args(argv):
    args = {}
    required = {"-P", "-Q", "-a", "-b", "-p"}

    i = 0
    while i < len(argv):
        if argv[i] in required:
            if i + 1 >= len(argv):
                print(f"Error: missing value for {argv[i]}")
                print()
                print_help()
                raise SystemExit(1)
            args[argv[i].lstrip("-")] = int(argv[i + 1])
            i += 2
        else:
            print(f"Error: unknown parameter '{argv[i]}'")
            print()
            print_help()
            raise SystemExit(1)

    missing = [r for r in required if r.lstrip("-") not in args]
    if missing:
        print("Error: missing parameters:", ", ".join(missing))
        print()
        print_help()
        raise SystemExit(1)

    return args

if __name__ == "__main__":
    argv = __import__("sys").argv

    if len(argv) == 1 or "--help" in argv or "-h" in argv:
        print_help()
        raise SystemExit(0)

    args = parse_args(argv[1:])
    a, b, p = args["a"], args["b"], args["p"]

    # if x/y missing → point at infinity
    P = Point(args.get("x1"), args.get("y1"))
    Q = Point(args.get("x2"), args.get("y2"))

    checkcurve(a, b, p)


    if Q.is_infinity:
        """addition mit 0 """
        print(P)
        exit(0)
    elif P.is_infinity:
        print(Q)
        exit(0)

    if Q.x == P.x and Q.y == -P.y:
       R = Point()
       print(R)
       exit(0)


    if P.x == Q.x and P.y == Q.y:
        """pointdoubling"""
        print(pointdoubling(P, a, p))
        exit(0)
    else:
        """pointaddition"""
        print(pointaddition(P, Q, p))
        exit(0)
