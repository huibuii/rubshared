import hashlib, time

def getUpLetter(number):
	return chr(ord('A')+number)

def getHexByteStr(number):
	return "%02x" % number

def md5(password, constant):
	m = hashlib.md5()
	m.update(str.encode(password + constant))
	return m.hexdigest()

def lmh(password, constant):
	while len(password) <= 14:
		password = password + "0"
	password = password.upper()
	return md5(password[:7], constant)[:16] + md5(password[7:14], constant)[:16]

def wnth(password, constant):
	while len(password) <= 14:
		password = password + "0"
	return md5(password, constant)[:32]

def chap(password, constant, challenge):
	firstHash = lmh(password, constant) + "0000000000"
	secondHash = wnth(password, constant) + "0000000000"
	res1 = md5(firstHash[:14],challenge)[:16]
	res2 = md5(firstHash[14:28],challenge)[:16]
	res3 = md5(firstHash[28:42],challenge)[:16]
	res4 = md5(secondHash[:14],challenge)[:16]
	res5 = md5(secondHash[14:28],challenge)[:16]
	res6 = md5(secondHash[28:42],challenge)[:16]
	return res1 + res2 + res3 + res4 + res5 + res6

pwd = "b00000000"
const = "NetSec1"
chall = "GoodLuck!"

"""
print("md5 hash of " + pwd + "\nwith constant " + const + "\nis " + md5(pwd, const) + "\n")
print("lmh of " + pwd + "\nwith constant " + const + "\nis " + lmh(pwd, const) + "\n")
print("response of " + pwd + "\nwith constant " + const + "\nand " + chall + "\nis " + chap(pwd, const, chall) + "\n")
"""
const = "NetSec1"
chall = "GoodLuck!"






"""
print(lmh("317838698", const))
print("hier folgt der resp: ")
print(chap("baaaaaaaa", const, chall))
"""
#resp = "25e4b9db85e091705ffe4099d53744d40cae26e7a9cc4014f2121f126cd9b5e6251a036b8754b74ce8271e0cfb1539d4"






resp = "fd1c103fe67100eb4b3f6d39f177bb08332188b99f7f64cb874627e5f2dfc0519134525203266fdb948c28f744698861"
print(resp)
resp1 = resp[:16]
resp2 = resp[16:32]
resp3 = resp[32:48]
resp4 = resp[48:64]
resp5 = resp[64:80]
resp6 = resp[80:96]
start = time.perf_counter()


#### Step 1
print("Step 1")
h14 = ""
h15 = ""
print(resp3)
for i in range(0x10000):
    hexwert = f"{i:04X}"
    block = hexwert.lower().ljust(14, "0")
    temp = md5(block, chall)
    if temp[:16] == resp3:
        print(f"Treffer für h14 und h15 bei i = {hexwert}: {temp[:16]}")
        h14=block[:2]
        h15=block[2:4]
        print(f"h14: {h14} h15: {h15}")
        break

#### Step 2
print("Step 2")
candidates = {}
from string import ascii_uppercase

for a in ascii_uppercase:
    for b in ascii_uppercase:
        p78 = a + b
        res = lmh("0"*7 + p78 + "0"*5, const)[16:]
        if res[12:14] == h14 and res[14:16] == h15:
            candidates[p78] = res

print(f"Kandidaten für h8 bis h15: {candidates}")

### Step 3
print("Step 3")
h7 = ""
P7P8 =""
for p78, res in candidates.items():
    for i in range(0x100):
        block = f"{i:02x}" + res[:12]          # H7 (geraten) + H8..H13
        if md5(block, chall)[:16] == resp2:
            h7 = block[:2]
            print(f"Treffer für h7: {h7}  (Paar P7P8 = {p78})")
            P7P8 = p78
            break
    if h7:
        break
### Step 4
print("Step 4")
P0="b"
import itertools
from string import ascii_uppercase

gesamt = 26**6
schritt = gesamt // 100
limit = int(gesamt * 1)   # 6178315 -- vor die Schleife gezogen

candidates = {}              # pw -> res

for n, rest in enumerate(itertools.product(ascii_uppercase, repeat=6)):
    if n % schritt == 0:
        print(f"{n // schritt} %")
    if n >= limit:
        break
    pw = P0 + "".join(rest)
    res = lmh(pw, const)[:16]
    if res[14:] == h7:
        candidates[pw] = res
        #print(f"Kandidat für h0 bis h7: {res}")
        #print(f"zugehöriges pw {pw}")
print(f"Kandidaten für h0 bis h7 {list(candidates.values())}")


### Step 5
print("Step 5")
uppercase_pw = ""
for pw, res in candidates.items():
    temp = md5(res[:14], chall)
    if temp[:16] == resp1:
        h06 = res[:14]
        print(f"Treffer für h0 bis h6 bei: {h06}")
        print(f"zugehöriges pw: {pw}")
        uppercase_pw = pw
        break

### Step 6
print("Step 6")

base = uppercase_pw[1:] + P7P8   # rekonstruierte Buchstaben (Schreibweise egal)
print(f"Base für die Rekonstruktion: {base}")
# pro Stelle beide Varianten
optionen = [(ch.lower(), ch.upper()) for ch in base]

for combo in itertools.product(*optionen):
    kandidat = "b" + "".join(combo)
    if chap(kandidat, const, chall) == resp:
        print("Passwort:", kandidat)
        break



dauer = time.perf_counter() - start
print(f"Dauer: {dauer:.2f} s")



