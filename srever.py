import json

import pygame
import socket
import threading

from player import Player


class Server:
    pygame.init()
    players = {}
    users = {}
    addresses = {}
    player_group = pygame.sprite.Group()
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    last_id = 0

    def dumps_players(self):
        return json.dumps(self.players).encode('utf-8')

    def send_all(self):
        data = self.dumps_players()
        for user in self.users:
            user.send(data)

    def listen_player(self, id):
        player = self.players[id]
        user = self.users[id]
        address = self.addresses[id]
        disconnected = False
        while not disconnected:
            try:
                player[id].load(user.recv(2048))
            except ConnectionResetError:
                print(f"Player {id} was disconnected")
                disconnected = True

    def check_for_connection(self):
        player_socket, address = self.server.accept()

        self.last_id += 1
        cur_player = Player(self.last_id, address, 0, 0, (255, 255, 255), self.player_group)
        self.players[self.last_id] = cur_player
        self.users[self.last_id] = player_socket
        self.addresses[self.last_id] = address

        print(f"{address} was connected")

        player_socket.send(cur_player.to_json())

        threading.Thread(
            target=self.listen_player,
            args=(self.last_id, )
        ).start()

    def start(self, ip, port):
        self.server.bind((ip, port))
        self.server.listen()

        while True:
            self.check_for_connection()
            self.send_all()

