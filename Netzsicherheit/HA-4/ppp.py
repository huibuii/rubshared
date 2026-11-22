import hashlib

def getUpLetter(number):
	return str(unichr(ord('A')+number))

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

pwd = "password"
const = "NetSec1"
chall = "GoodLuck!"

print("md5 hash of " + pwd + "\nwith constant " + const + "\nis " + md5(pwd, const) + "\n")
print("lmh of " + pwd + "\nwith constant " + const + "\nis " + lmh(pwd, const) + "\n")
print("response of " + pwd + "\nwith constant " + const + "\nand " + chall + "\nis " + chap(pwd, const, chall) + "\n")

const = "NetSec1"
chall = "GoodLuck!"
resp = "1acad1cd833b82bbe379c4984786cdf501bc0a8d020ab4ab617719e1fce1bc7f6130f8b1ff02a5d9462b8b8865213d64"

# Beispiel:
#  Das Passwort ist 9 Zeichen lang.
#  Das erste Passwortzeichen ist b (siehe P0).
#  Zeichen 2-9 (also P1...P8) sind Groß- und Kleinbuchstaben.
# Tipp: Starten Sie Ihre Suche bei a bzw. A.    
P0="b" 

##### Folgend die Loesung:
