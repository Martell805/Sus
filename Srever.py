import pygame
import socket


class Server:
    pygame.init()
    players = {}
    players_group = pygame.sprite.Group()
    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    def start(self, ip, port):
        self.server.bind(ip, port)

