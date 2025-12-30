from rubshared.Krypto.Weihnachtsprojekt.chacha20 import quarterround

def test_quarterround():
    input = [
        286331153,
        16909060,
        2609737539,
        19088743
    ]
    output = [
        3928658676,
        3407673550,
        1166100270,
        1484899515
    ]

    quarterround(input, 0, 1, 2, 3)

    assert input == output