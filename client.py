import socket
from threading import Thread
import pygame
from player import Player
import json


class Client:
    RES = WIDTH, HEIGHT = 400, 300

    screen = pygame.display.set_mode(RES)
    player_group = pygame.sprite.Group()
    clock = pygame.time.Clock()

    player = None
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    players = {}

    def listen_server(self):
        while True:
            data = json.load(self.client.recv(2048).decode("utf-8"))
            for player_info in data:
                if player_info['id'] == self.player.id:
                    self.player.load(player_info)
                else:
                    self.players['id'].load(player_info)

    def init_player(self):
        data = self.client.recv(2048)
        self.player = Player.create(data)
        self.player_group.add(self.player)

    def connect(self, ip, port):
        self.client.connect((ip, port))

        self.init_player()

        listen_thread = Thread(target=self.listen_server)
        listen_thread.start()

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                data = json.dumps(
                    {'up': pygame.key.get_pressed()[pygame.K_w],
                     'down': pygame.key.get_pressed()[pygame.K_s],
                     'left': pygame.key.get_pressed()[pygame.K_a],
                     'right': pygame.key.get_pressed()[pygame.K_d], }
                ).encode("utf-8")

                self.client.send(data)

            for id in self.players:
                self.players[id].draw(self.screen)
                self.player.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(60)

    def start(self, ip, port):
        self.connect(ip, port)
        self.run()


if __name__ == '__main__':
    client = Client()
    client.start("127.0.0.1", 1337)
