# power_ups.py

import pygame

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Power-up size
        self.image.fill((0, 255, 0))  # Green color for visibility
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
