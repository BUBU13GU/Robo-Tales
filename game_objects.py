import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load('assets/coin.png')
        width, height = original_image.get_size()
        self.image = pygame.transform.scale(original_image, (width // 20, height // 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):    #Added width and height parameters
        super().__init__()
        self.original_image = pygame.image.load('assets/platform.jpg')
        self.image = pygame.transform.scale(self.original_image , (width , height))   #Scaled image according to provided width and height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Power-up size
        self.image.fill((0, 255, 0))  # Green color for visibility
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
