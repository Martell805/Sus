import json
import random

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

    clock = pygame.time.Clock()

    last_id = 0

    def dumps_players(self) -> str:
        players_info = {}
        for id, player in self.players.items():
            players_info[id] = player.to_json()
        return json.dumps(players_info)

    def send_all(self) -> None:
        data = self.dumps_players()
        to_send = self.users.items()
        for id, user in to_send:
            user.send(data.encode("utf-8"))

    def listen_player(self, id: int) -> None:
        player = self.players[id]
        user = self.users[id]
        address = self.addresses[id]
        while True:
            try:
                player.update(user.recv(2048).decode("utf-8"))
            except ConnectionResetError:
                del self.players[id]
                del self.users[id]
                del self.addresses[id]
                player.kill()
                print(f"Player {id} was disconnected")
                break

    def check_for_connection(self) -> None:
        while True:
            player_socket, address = self.server.accept()
            print(address)

            self.last_id += 1
            cur_player = Player(self.last_id, 200, 200, 0,
                                (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)),
                                self.player_group)
            self.players[self.last_id] = cur_player
            self.users[self.last_id] = player_socket
            self.addresses[self.last_id] = address

            print(f"{address} was connected")

            player_socket.send(cur_player.to_json().encode("utf-8"))

            threading.Thread(
                target=self.listen_player,
                args=(self.last_id, )
            ).start()

    def start(self, ip: str, port: int) -> None:
        self.server.bind((ip, port))
        self.server.listen()

        threading.Thread(
            target=self.check_for_connection,
            args=()
        ).start()

        while True:
            # print(self.players)
            self.send_all()
            self.clock.tick(60)


if __name__ == '__main__':
    server = Server()
    server.start("127.0.0.1", 1234)
