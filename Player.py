import pygame.draw
from pygame import sprite


class Player(sprite.Sprite):
    def __init__(self, player_info, *groups):
        super().__init__(*groups)
        self.id = player_info['id']
        self.adress = player_info['adress']
        self.x = player_info['x']
        self.y = player_info['y']
        self.color = player_info['color']
        self.angle = player_info['angle']

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
