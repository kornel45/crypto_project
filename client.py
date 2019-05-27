import random
import re
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from common import HOST, PORT, BUFF_SIZE, modinv


def receive():
    global i, g, p, public_keys, is_veto, last_answer
    while True:
        try:
            msg = client_socket.recv(BUFF_SIZE).decode("utf8")
            if 'Twoje id wynosi' in msg:
                tmp = msg[::]
                i = int(re.sub(r'\D', '', tmp))
            elif 'Ustalono g, p' in msg:
                g, p = [int(x) for x in re.findall(r'\d+', msg)]
            elif 'Każdy z was wysłał pub_key' in msg:
                public_keys = eval(msg.split('\n')[1])
            if '?' in msg:
                last_answer = True
            print(msg)
        except OSError:
            break


def send():
    global i, g, p, x_i, last_answer, is_veto
    while True:
        msg = input()
        if last_answer:
            is_veto = True if msg == 't' else False
            msg = str(gen_answer(is_veto))
        elif msg.isdigit():
            x_i = int(msg)
            msg = str(g ** int(msg) % p)
        client_socket.send(bytes(msg, "utf8"))
        if msg == r"\q":
            client_socket.close()
            break


def gen_answer(is_veto):
    global p, i, x_i, public_keys
    gy = 1
    n = 3
    user_number = i
    tmp_public_keys = [x[1] for x in sorted([[x, y] for x, y in public_keys.items()])]
    for j in range(user_number):
        gy = gy * tmp_public_keys[j] % p
    for j in range(user_number + 1, n):
        gy = gy * modinv(tmp_public_keys[j], p) % p
    if is_veto:
        x_i += random.randint(0, p - 1)
    return gy ** x_i % p


def gen_g_x(g, p):
    r = random.randint(0, p - 1)
    return g ** r % p


g = None
p = None
i = None
x_i = None
public_keys = {}
is_veto = None
last_answer = None

if __name__ == '__main__':
    ADDR = (HOST, PORT)

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)

    receive_thread = Thread(target=receive)
    send_thread = Thread(target=send)
    receive_thread.start()
    send_thread.start()
