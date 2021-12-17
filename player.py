import pygame.draw
from pygame import sprite
import json


class Player(sprite.Sprite):
    def __init__(self, id, x, y, angle, color, *groups):
        super().__init__(*groups)
        self.id = id
        self.x = x
        self.y = y
        self.angle = angle
        self.color = color

    def __repr__(self) -> str:
        return f"Player {self.id}: ({self.x}, {self.y})"

    def to_json(self) -> str:
        player_info = {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "angle": self.angle,
            "color": self.color,
        }

        return json.dumps(player_info)

    def load(self, player_info) -> None:
        player_info = json.loads(player_info)

        self.id = player_info['id']
        self.x = player_info['x']
        self.y = player_info['y']
        self.angle = player_info['angle']
        self.color = player_info['color']

    @staticmethod
    def create(player_info):
        player_info = json.loads(player_info)

        player = Player(player_info['id'],
                        player_info['x'], player_info['y'],
                        player_info['angle'], player_info['color'])

        return player

    def update(self, controls, *args, **kwargs):
        controls = json.loads(controls)

        if controls['up']:
            self.y -= 1
        if controls['down']:
            self.y += 1
        if controls['left']:
            self.x -= 1
        if controls['right']:
            self.x += 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 50)
