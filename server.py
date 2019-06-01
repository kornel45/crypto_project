"""Server for multithreaded (asynchronous) chat application."""
import random
import ssl
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

from common import HOST, PORT, BUFF_SIZE, is_veto

index = 0


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("{} has connected.".format(client_address))
        client = context.wrap_socket(client, server_side=True)
        client.send(bytes("Type your name: ", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def get_name(client):
    global index
    name = client.recv(BUFF_SIZE)
    name = name.decode("utf8")
    if name not in clients.values():
        welcome = r'Welcome {}! If you ever want to quit, type \q to exit.'.format(name)
        client.send(bytes(welcome, "utf8"))
        time.sleep(0.01)
        client.send(bytes('Twoje id wynosi {}'.format(index), "utf8"))
        client_id = index
        index += 1
    else:
        client.send(bytes('This nickname is already taken. Please provide different nick: ', "utf8"))
        return get_name(client)
    return name, client_id


def get_g_p(client, client_id):
    global response_p_g, g, p, agreement, przeszedlem, ktory_wybiera
    if client_id == ktory_wybiera:
        msg = 'Zaproponuj proszę g, p w postacie g,p [liczba przcinek liczba]'
        client.send(bytes(msg, 'utf-8'))
        response = client.recv(BUFF_SIZE).decode('utf-8')
        response_p_g[client_id] = response
        g, p = [int(x) for x in response.split(',')]
        while not len(clients) == 3:
            pass
        msg = 'Zaproponowano g, p = {}.'.format(response)
        broadcast(bytes(msg, 'utf-8'))
    else:
        response = client.recv(BUFF_SIZE).decode('utf-8')
        response_p_g[client_id] = response
        if response == 'y':
            agreement += 1
            print('Zgodzono sie na dane g = {} oraz p = {}'.format(g, p))
            while len(response_p_g) != 2 or przeszedlem:
                pass
        elif response == 'n':
            broadcast(bytes('Nie możesz nie zaakaceptować. Zresetuj serwer i nastepnym razem zaakceptuj', 'utf-8'))


def handle_client(client):
    global clients_public_keys, client_answers, p, agreement, ktory_wybiera, should_print
    name, client_id = get_name(client)
    msg = "{} dołączył do czatu!".format(name)
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    get_g_p(client, client_id)
    przeszedlem = True
    if client_id == ktory_wybiera:
        broadcast(bytes('Wcisnij enter aby wyslac klucz publiczny', 'utf-8'))
    first = True
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
                        broadcast(bytes('Pytanie: Czy papież łowi łyby? [t/n]', 'utf-8'))
                        time.sleep(0.01)
                elif msg.decode('utf-8').isdigit():
                    client_answers[client_id] = int(msg.decode('utf-8'))
                    time.sleep(0.01)
                    if len(client_answers.keys()) == 3 and should_print:
                        tmp_client_answers = [x[1] for x in sorted([[x, y] for x, y in client_answers.items()])]
                        result = is_veto(tmp_client_answers, p)
                        msg = 'Wasza odpowiedź to: {}'.format(str(result))
                        broadcast(bytes(msg, 'utf-8'))
                        should_print = False




                # elif msg.decode('utf-8').isdigit():


        except ConnectionResetError:
            del clients_public_keys[client_id]
            del clients[client]


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


g = 3
p = 2003
przeszedlem = False
agreement = 1
answer = 0
should_print = True
response_p_g = {}
clients = {}
addresses = {}
clients_public_keys = {}
client_answers = {}
ktory_wybiera = random.randint(0, 2)
ADDR = (HOST, PORT)

server_cert = 'server.crt'
server_key = 'server.key'
client_certs = 'client.crt'
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(certfile=server_cert, keyfile=server_key)
context.load_verify_locations(cafile=client_certs)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
