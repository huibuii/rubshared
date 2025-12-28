from rubshared.Krypto.Weihnachtsprojekt.chacha20 import cyclic_shift

def test_cyclic_shift():
    assert cyclic_shift(12345, 6) == [2, 3, 4, 5, 1]
    assert cyclic_shift(12345, 2) == [3, 4, 5, 1, 2]