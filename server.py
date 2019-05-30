"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from common import HOST, PORT, BUFF_SIZE, is_veto, gen_answer

index = 0


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("{} has connected.".format(client_address))
        client.send(bytes("Type your name: ", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def get_name(client):
    global index
    name = client.recv(BUFF_SIZE).decode("utf8")
    if name not in clients.values():
        welcome = r'Welcome {}! If you ever want to quit, type \q to exit.'.format(name)
        client.send(bytes(welcome, "utf8"))
        time.sleep(0.01)
        client.send(bytes('Ustalono g, p = {}, {}.'.format(g, p), "utf8"))
        time.sleep(0.01)
        client.send(bytes('Twoje id wynosi {}'.format(index), "utf8"))
        index += 1
    else:
        client.send(bytes('This nickname is already taken. Please provide different nick: ', "utf8"))
        return get_name(client)
    return name


def handle_client(client):
    global clients_public_keys, client_answers, p
    name = get_name(client)
    first = True
    msg = "{} dołączył do czatu!".format(name)
    broadcast(bytes(msg, "utf8"))
    client_id = int(index)
    clients[client] = name
    msg = 'Podaj x. Klient wyśle na serwer g^x mod p.'
    client.send(bytes(msg, "utf8"))
    while True:
        try:
            msg = client.recv(BUFF_SIZE)
            if msg == bytes(r"\q", "utf8"):
                client.close()
                del clients[client]
                broadcast(bytes("{} opuścił czat! Hurra!".format(name), "utf8"))
                break
            else:
                if msg.decode('utf-8').isdigit() and first:
                    client.send(bytes('Podałeś {}. Czekamy na pozostałe osoby.'.format(int(msg)), "utf8"))
                    clients_public_keys[client_id] = int(msg)
                    first = False
                    if len(clients_public_keys.keys()) == 3:
                        broadcast(bytes('Każdy z was wysłał pub_key:\n{}'.format(clients_public_keys), 'utf-8'))
                        time.sleep(0.01)
                        broadcast(bytes('Otrzymacie zaraz pytanie, proszę odpowiedzieć na nie.', 'utf-8'))
                        time.sleep(0.01)
                        broadcast(bytes('Czy papież łowi łyby? [t/n]', 'utf-8'))
                elif msg.decode('utf-8').isdigit():
                    client_answers[client_id] = int(msg)
                    if len(client_answers.keys()) == 3:
                        tmp_client_answers = [x[1] for x in sorted([[x, y] for x, y in client_answers.items()])]
                        result = is_veto(tmp_client_answers, p)
                        msg = 'Wasza odpowiedź to: {}'.format(str(result))
                        broadcast(bytes(msg, 'utf-8'))

        except ConnectionResetError:
            del clients_public_keys[client_id]
            del clients[client]


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


g = 3
p = 1023

clients = {}
addresses = {}
clients_public_keys = {}
client_answers = {}
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    CALC_THREAD = Thread(target=gen_answer)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
