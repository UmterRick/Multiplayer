import pickle
import socket
from _thread import *
import sys
from colors import *
from player import Player
server = "192.168.0.101"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for a connection, Server Started")

players = [Player(0, 0, 50, 50, RED), Player(100, 100, 50, 50, BLUE)]


def threaded_Client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048 * 1))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]

                print("Recieved: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))

        except:
            break
    print("Lost Connection")
    conn.close()


current_player = 0
while True:
    conn, addr = s.accept()
    print("Connection to:", addr)
    start_new_thread(threaded_Client, (conn, current_player))
    current_player += 1
