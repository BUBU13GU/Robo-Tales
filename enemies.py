import pygame
from settings import SCREEN_WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, health=3):
        super().__init__()
        self.image = pygame.image.load('assets/e1.png').convert_alpha()  # Load enemy sprite
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.health = health  # Health attribute

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speed = -self.speed
        self.rect.y += 2 if self.rect.x % 20 < 10 else -2

    def take_damage(self, damage):
        """Decrease health by the damage amount."""
        self.health -= damage
        if self.health <= 0:
            self.kill()  # Remove sprite if health is 0 or less

    def is_alive(self):
        """Check if the enemy is still alive."""
        return self.health > 0