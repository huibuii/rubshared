import sys


def square(a,c):
    result = (a * a) % c
    print(f"Square: A = A^2 = {a}^2 mod {c} = {result}")
    return result

def multiply(a,b,c):
    result = (a * b) % c
    print(f"Multiply: A = A * x = {a} * {b} mod {c} = {result}")
    return result

def sqm(x,d,n):
    print("d = ", d, "=", bin(d)[2:])
    print()
    print("-----------------------------")
    print("Initialisierung: A = x =", x)
    print()
    result = x

    for bit in bin(d)[3:]:
        if bit == '1':
            result = square(result, n)
            result = multiply(result, x, n)
            print()
        elif bit == '0':
            result = square(result, n)
            print()
        else:
            raise ValueError(f"Bad bit: {bit}")
    return result

def print_help():
    print("Square-and-multiply algorithm")
    print("====================")
    print("Usage:   python3", sys.argv[0], "-x <> -d <> -n <>")
    print("Parameters:")
    print("  -x        : Basis")
    print("  -d        : Exponent")
    print("  -n        : modulus")
    print()
    print()
    print("Example 8^55 mod 151:             python3", sys.argv[0], "-x 8 -d 55 -n 191")

if __name__ == "__main__":
    argv = __import__("sys").argv
    if len(argv) == 1 or "--help" in argv or "-h" in argv:
        print_help()
        raise SystemExit(0)

    values = argv[1:]
    i = 0
    x = None
    d = None
    n = None

    while i < len(values) - 1:
        match values[i]:
            case "-x":
                x = int(values[i + 1])
            case "-d":
                d = int(values[i + 1])
            case "-n":
                n = int(values[i + 1])
            case _:
                raise ValueError(f"unknown parameter: {values[i]}")

        i += 2

    if x is None:
        raise ValueError(f"x is missing")
    if d is None:
        raise ValueError(f"d is missing")
    if n is None:
        raise ValueError(f"n is missing")

    print("Berechne: ", x, "^", d, "mod", n)

    print ("Ergebnis: ", sqm(x,d,n))