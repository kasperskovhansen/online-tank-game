import socket
from _thread import *
from sprites.player import Player
import pickle
from random import randint

dev = True
server = "12.34.56.78"
port = 5555
if dev:
    server = "localhost"
    port = 5555


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Serving at (local): {}:{}".format(server, port))
print("Waiting for a connection, Server Started")

players = []

def threaded_client(conn, player):
    conn.send(pickle.dumps([player, players]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            print(data[0])
            players[data[0]] = data[1]
            print(data[1].x)

            if not data:
                print("Disconnected")
                break
            else:               
                players[data[0]].disconnected = False
                reply = players

                # print("Received: ", data)
                # print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    players[data[0]].disconnected = True
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("conn")
    print("Connected to:", addr)
    players.append(Player(randint(50, 400),randint(50, 400),50,50,(255,0,0)))

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1