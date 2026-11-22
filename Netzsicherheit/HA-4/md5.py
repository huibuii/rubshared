import hashlib

def md5(password, constant):
    m = hashlib.md5()
    m.update(str.encode(password + constant))
    return m.hexdigest()

print(md5("password", "constant"))
