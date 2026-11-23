import hashlib



def md5(password, constant):
    m = hashlib.md5()
    m.update(str.encode(password + constant))
    return m.hexdigest()

def lmh(password):
    pw = password.ljust(14, "0")          # auf 14 mit '0' auffüllen
    block1 = md5(pw[:7],  netconstant)[:16]   # erste 8 Byte = 16 Hex
    block2 = md5(pw[7:14], netconstant)[:16]
    return block1 + block2

# Beispielrechnung aus Aufgabe 1
netconstant = "NetSec1"
print("c98484bc0ee0509fda498b1fe098c2c3")
print(md5("2233445", netconstant))
print(md5("5000000", netconstant))


# Check für Aufgabe 1
# Abgefangener Hash:
print("83b9d443bd3080a9f7c70735c3524785")
# Gefundenes Passwort durch Brute Force (s. unten):
print(lmh("317838698"))




start = 000000000
end   = 999999999

# Abgefangener Hash:
hash = "83b9d443bd3080a9f7c70735c3524785"
for i in range(start, end + 1):

    temp = lmh(f"{i:09d}")
    if i % 10_000_000 == 0:
        print(f"... bei {temp} ({i / 10_000_000:.0f}%)")
    if temp == hash:
        print(f"{i:09d}")
        print(temp)
        break