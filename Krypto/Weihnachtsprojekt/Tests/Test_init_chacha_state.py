from rubshared.Krypto.Weihnachtsprojekt.chacha20 import init_chacha_state

def test_init_chacha_state():

    key = 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
    nonce = 0x000000090000004a00000000

    state = init_chacha_state(key, nonce)

    stateshouldlook = [0x61707865,  0x3320646e,  0x79622d32,  0x6b206574, 0x03020100,  0x07060504,  0x0b0a0908,  0x0f0e0d0c, 0x13121110,  0x17161514,  0x1b1a1918,  0x1f1e1d1c, 0x00000001,  0x09000000,  0x4a000000,  0x00000000]



    assert stateshouldlook == state