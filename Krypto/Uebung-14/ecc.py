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

def edgecases(x1, y1, x2, y2, a ,b ,p):



    if x1 ==0 and y1 == 0:
        """addition mit 0 """
        return x2, y2
    elif x2 == 0 and y2 == 0:
        return x1, y1

    if y2 == -y1:
       """return 0"""

    if x1 == x2 and y1 == y2:
        """pointdoubling"""
    else:
        """pointaddition"""


import sys

def print_help():
    print("ECC Group Operations")
    print("====================")
    print("Usage:   python script.py -x1 <x1> -y1 <y1> -x2 <x2> -y2 <y2> -a <a> -b <b> -p <p>")
    print()
    print("Parameters:")
    print("  -x1, -y1  : coordinates of point P")
    print("  -x2, -y2  : coordinates of point Q")
    print("  -a, -b    : curve parameters of y² = x³ + ax + b")
    print("  -p        : prime modulus")
    print()
    print("Example:  python script.py -x1 3 -y1 7 -x2 5 -y2 2 -a 4 -b 7 -p 41")

def parse_args(argv):
    args = {}
    required = {"-x1", "-y1", "-x2", "-y2", "-a", "-b", "-p"}

    i = 0
    while i < len(argv):
        if argv[i] in required:
            if i + 1 >= len(argv):
                print(f"Error: missing value for {argv[i]}")
                print()
                print_help()
                sys.exit(1)
            args[argv[i].lstrip("-")] = int(argv[i + 1])
            i += 2
        else:
            print(f"Error: unknown parameter '{argv[i]}'")
            print()
            print_help()
            sys.exit(1)

    # check if any required parameter is missing
    missing = [r for r in required if r.lstrip("-") not in args]
    if missing:
        print("Error: missing parameters:", ", ".join(missing))
        print()
        print_help()
        sys.exit(1)

    return args

if __name__ == "__main__":
    if len(sys.argv) == 1 or "--help" in sys.argv or "-h" in sys.argv:
        print_help()
        sys.exit(0)

    args = parse_args(sys.argv[1:])

    x1, y1 = args["x1"], args["y1"]
    x2, y2 = args["x2"], args["y2"]
    a, b, p = args["a"], args["b"], args["p"]

    checkcurve(a, b, p)
    edgecases(x1,y1, x2, y2, a, b ,p)
    print("Addition:  ", pointaddition(x1, y1, x2, y2, p))
    print("Doubling:  ", pointdoubling(x1, y1, a, p))