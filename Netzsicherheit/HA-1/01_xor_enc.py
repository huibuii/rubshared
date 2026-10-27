import secrets


def xor_bytes(a, b):
    # Implement here
    if len(a) != len(b):
        raise ValueError('The two byte arrays must have the same length')

    result = bytearray()
    for i in range(0, len(a)):
        result.append(a[i] ^ b[i])

    return result


def main():
    assert xor_bytes(b"", b"") == b""
    assert xor_bytes(bytes.fromhex("1234"), bytes.fromhex("ff00")) == bytes.fromhex("ed34")

    text = "Grüße"
    hex_text = "48616c6c6f"
    # Implement here
    bytefolge = bytearray(text.encode('utf-8'))

    print("Anzahl der Zeichen:", len(bytefolge.decode('utf-8')))
    print("Anzahl der Bytes:", len(bytefolge))
    print("Anzahl der Bits:", len(bytefolge) * 8)
    print("Hexadezimaldarstellung:", bytefolge.hex())

    print(bytes.fromhex(hex_text).decode('utf-8'))

    key = secrets.token_bytes(len(bytefolge))
    cipher = xor_bytes(bytefolge, key)
    plain = xor_bytes(cipher, key)
    print("Chiffrat in Hex:", cipher.hex())
    print("Plaintext:", plain.decode('utf-8'))

    pass


if __name__ == "__main__":
    main()
