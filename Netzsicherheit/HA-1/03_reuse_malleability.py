def xor_bytes(a, b):
    if len(a) != len(b):
        raise ValueError("Die Bytefolgen muessen gleich lang sein.")
    result = bytearray()
    for i in range(len(a)):
        result.append(a[i] ^ b[i])
    return bytes(result)


def recover_message(known_plaintext, known_ciphertext, target_ciphertext):
    # Implement here
    known_keystream = xor_bytes(known_plaintext, known_ciphertext)
    target_plaintext = xor_bytes(target_ciphertext, known_keystream[:len(target_ciphertext)])

    return bytes(target_plaintext)

    raise NotImplementedError


def change_message(ciphertext, offset, old, new):
    # Implement here
    cpy = bytearray(ciphertext)
    input = xor_bytes(old, new)

    for i in range(0, len(old)):
        cpy[offset + i] ^= input[i]
    return bytes(cpy)

    raise NotImplementedError


def main():
    known_plaintext = b"Dies ist eine bekannte Nachricht."
    known_ciphertext = bytes.fromhex("684ddf7dc341afff962e5fa4f0918833828095073bf7b45d11281484c4eb43a262")
    target_ciphertext = bytes.fromhex("5856df688558a9e5dd3f0ba2fad49825888097367fa1")

    recovered = recover_message(known_plaintext, known_ciphertext, target_ciphertext)
    print("Rekonstruierter Klartext:", recovered.decode("utf-8"))

    ciphertext = bytes.fromhex("6c9d07211c47deb17acaa2ddc1a892e328d866786d37b8af7da4")
    changed = change_message(ciphertext, 22, b"0100", b"0900")
    print("Manipulierter Chiffretext:", changed.hex())



if __name__ == "__main__":
    main()
