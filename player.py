# player.py
import pygame
from settings import SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 5
        self.velocity_y = 0  # Vertical velocity for jumping
        self.gravity = 0.5
        self.is_running = False
        self.is_jumping = False
        self.scale_factor = 0.1
        self.current_level = None
        self.animation_speed = 150  # Animation speed; lower is faster
        self.current_time = 0
        self.last_update_time = pygame.time.get_ticks()  # Placeholder, set this to the current level object

        # Load the sprite sheet and setup animations
        self.sprite_sheet = pygame.image.load('assets/player_mov.png').convert_alpha()

        # Define the number of columns and rows in your sprite sheet
        num_columns = 5  # Replace with the actual number of columns
        num_rows = 3     # Replace with the actual number of rows

        self.idle_frames = self.extract_frames(8, 9, num_columns, num_rows)
        self.running_frames = self.extract_frames(0, 9, num_columns, num_rows)
        self.jumping_frames = self.extract_frames(11, 13, num_columns, num_rows)
        self.current_frames = self.idle_frames
        self.frame_index = 0
        self.image = self.current_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100 

    def extract_frames(self, start_frame, end_frame, num_columns, num_rows):
        frames = []
        frame_width = self.sprite_sheet.get_width() // num_columns
        frame_height = self.sprite_sheet.get_height() // num_rows
        scaled_width = int(frame_width * self.scale_factor)
        scaled_height = int(frame_height * self.scale_factor)

        for i in range(start_frame, end_frame):
            x = (i % num_columns) * frame_width
            y = (i // num_columns) * frame_height
            frame = self.sprite_sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frame = pygame.transform.scale(frame, (scaled_width, scaled_height))
            frames.append(frame)
        return frames

    def activate_power_up(self):
        self.velocity_y *= 2
        self.speed *= 2  # Example effect: double the speed
        pygame.time.set_timer(pygame.USEREVENT, 5000)  # 5 seconds

    def deactivate_power_up(self):
        self.velocity_y /= 2
        self.speed /= 2  # Revert to normal speed
        pygame.time.set_timer(pygame.USEREVENT, 0)  # 5 seconds

    def update(self):
        self.current_time = pygame.time.get_ticks()
        self.handle_keys()
        self.rect.y += self.velocity_y  # Apply vertical velocity
        self.velocity_y += self.gravity  # Apply gravity
        # Prevent falling off the screen (temporary solution)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
        if self.current_time - self.last_update_time > self.animation_speed * 1000:
            self.frame_index = (self.frame_index + 1) % len(self.current_frames)
            self.last_update_time = self.current_time
        # Animation logic
        if self.is_running:
            self.current_frames = self.running_frames
        elif self.is_jumping:
            self.current_frames = self.jumping_frames
        else:
            self.current_frames = self.idle_frames

        self.image = self.current_frames[self.frame_index]
        self.frame_index = (self.frame_index + 1) % len(self.current_frames)

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.is_running = True
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.is_running = True
        else:
            self.is_running = False

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
