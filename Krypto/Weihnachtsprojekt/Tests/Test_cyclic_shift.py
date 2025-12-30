from rubshared.Krypto.Weihnachtsprojekt.chacha20 import cyclic_shift

def test_cyclic_shift():
    # basic:
    assert cyclic_shift(1, 1) == 2
    assert cyclic_shift(4294967295, 1) == 4294967295