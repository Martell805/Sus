import pygame.draw
from pygame import sprite
import json


class Player(sprite.Sprite):
    def __init__(self, id, x, y, color, angle, *groups):
        super().__init__(*groups)
        self.id = id
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color

    def __repr__(self):
        return f"Player {self.id}: ({self.x}, {self.y})"

    def to_json(self):
        return json.dumps(self).encode('utf-8')

    def load(self, player_info):
        player_info = json.load(player_info.decode('utf-8'))

        self.id = player_info['id']
        self.x = player_info['x']
        self.y = player_info['y']
        self.angle = player_info['angle']
        self.color = player_info['color']

    @staticmethod
    def create(player_info):
        player_info = json.load(player_info.decode('utf-8'))

        player = Player(player_info['id'],
                        player_info['x'], player_info['y'],
                        player_info['angle'], player_info['color'])

        return player

    def update(self, controls, *args, **kwargs):
        if controls['up']:
            self.y -= 1
        if controls['down']:
            self.y += 1
        if controls['left']:
            self.x -= 1
        if controls['right']:
            self.x += 1

        self.angle = controls['angle']

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 50)
