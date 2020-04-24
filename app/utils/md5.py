import hashlib
def md5(str):
    md = hashlib.md5()
    md.update(str.encode(encoding='utf-8'))
    strMd5 = md.hexdigest()
    print('传入的密文', str)
    print('加密之后的密文', strMd5)
    return strMd5


