import socket
from threading import Thread
import pygame
from player import Player
import json


class Client:
    RES = WIDTH, HEIGHT = 400, 300

    screen = pygame.display.set_mode(RES)
    player_group = pygame.sprite.Group()
    connected = False
    clock = pygame.time.Clock()

    player = None
    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    players = {}

    def listen_server(self):
        while self.connected:
            try:
                data = json.loads(self.client.recv(2048).decode("utf-8"))
            except json.decoder.JSONDecodeError as e:
                print(e)
                continue

            players = {}
            for id, player_info in data.items():
                if int(id) == self.player.id:
                    self.player.load(player_info)
                else:
                    players[int(id)] = Player.create(player_info)
            self.players = players

    def init_player(self):
        player_info = self.client.recv(2048)
        self.player = Player.create(player_info.decode("utf-8"))
        self.player_group.add(self.player)

    def connect(self, ip, port):
        self.client.connect((ip, port))

        self.init_player()

        self.connected = True
        Thread(target=self.listen_server).start()

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.connected = False
                    exit()

            data = json.dumps(
                {'up': pygame.key.get_pressed()[pygame.K_w],
                 'down': pygame.key.get_pressed()[pygame.K_s],
                 'left': pygame.key.get_pressed()[pygame.K_a],
                 'right': pygame.key.get_pressed()[pygame.K_d],
                 }
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
    client.start("127.0.0.1", 1234)

