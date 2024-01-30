import pygame
from settings import SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/player_mov.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 300  # Adjust as needed

        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.4
        self.is_running = False
        self.is_jumping = False
        self.facing_right = True  
        self.rotation_angle = 0

    def activate_power_up(self):
        self.velocity_y *= 2
        self.speed *= 2  # Example effect: double the speed
        pygame.time.set_timer(pygame.USEREVENT, 5000)  # 5 seconds

    def deactivate_power_up(self):
        self.velocity_y /= 2
        self.speed /= 2  # Revert to normal speed
        pygame.time.set_timer(pygame.USEREVENT, 0)  # 5 seconds

    def update(self):
        self.handle_keys()
        self.rect.y += self.velocity_y
        self.velocity_y += self.gravity

        if self.is_running:
            self.rotation_angle = (self.rotation_angle ) % 360
            self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)

        if not self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image

        # Prevent falling off the screen
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.is_running = True
            self.rotation_angle += 10
            self.facing_right = False  
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.is_running = True
            self.rotation_angle -= 10
            self.facing_right = True  # Rotate clockwise
        else:
            self.is_running = False
            self.rotation_angle = 0  # Reset rotation when not moving
            self.image = self.original_image  # Reset image to original

        if keys[pygame.K_SPACE]:
            self.jump()


    def jump(self):
        # Check if player is on the ground by trying a small downward movement and testing for collision
        self.rect.y += 1  # Move down slightly
        platforms_hit = pygame.sprite.spritecollide(self, self.current_level.platforms, False)
        self.rect.y -= 1  # Move back to the original position

        # If touching a platform from above, then jump
        if platforms_hit:
            self.velocity_y = -10   # Jump velocity
