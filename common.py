import random


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def is_veto(answers, p):
    l = 1
    for i in answers:
        l = l * i % p
    if l == 1:
        return False
    else:
        return True


def gen_answer(public_keys, p, user_numer, does_he_veto, x, n):  # i to numer usera od 0 do n-1
    gy = 1
    for j in range(user_numer):
        gy = gy * public_keys[j] % p
    for j in range(user_numer + 1, n):
        gy = gy * modinv(public_keys[j], p) % p
    if does_he_veto:
        x += random.randint(0, p - 1)
    return gy ** x % p


HOST = 'localhost'
PORT = 33000
BUFF_SIZE = 1024
