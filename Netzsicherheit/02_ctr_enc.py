from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def xor_bytes(a, b):
    if len(a) != len(b):
        raise ValueError("Die Bytefolgen muessen gleich lang sein.")
    result = bytearray()
    for i in range(len(a)):
        result.append(a[i] ^ b[i])
    return bytes(result)


def aes_encrypt_block(key, block):
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    return encryptor.update(block) + encryptor.finalize()


def ctr_crypt(key, nonce, data):
    # Implement here
    counter = 0
    ciphertext = bytearray()
    for i in range(0, len(data), 16):
        counter_block = nonce + counter.to_bytes(8, "big")
        keystream = aes_encrypt_block(key, counter_block)
        counter += 1
        ciphertext.extend(xor_bytes(data[i:i+16], keystream[:len(data[i:i+16])]))

    print(ciphertext)
    return ciphertext

    raise NotImplementedError


def main():
    key = bytes.fromhex("00112233445566778899aabbccddeeff")
    nonce = bytes.fromhex("0102030405060708")
    message = b"Netzsicherheit 1!"
    expected = bytes.fromhex("ef1ef24773af6e3c004591365f4f63ea31")

    for length in [0, 1, 16, 17]:
        data = message[:length]
        ciphertext = ctr_crypt(key, nonce, data)
        assert ciphertext == expected[:length]
        assert ctr_crypt(key, nonce, ciphertext) == data

    print("Alle Tests erfolgreich.")
    print("Chiffretext:", ctr_crypt(key, nonce, message).hex())



if __name__ == "__main__":
    main()
