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

    def to_json(self):
        return json.dumps(self).encode('utf-8')

    def load(self, player_info):
        player_info = json.load(player_info.decode('utf-8'))

        self.id = player_info['id']
        self.x = player_info['x']
        self.y = player_info['y']
        self.y = player_info['y']
        self.y = player_info['y']

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
