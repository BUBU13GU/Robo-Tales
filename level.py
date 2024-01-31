# level.py
import random
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from game_objects import Coin
from game_objects import Platform
from game_objects import PowerUp
from enemies import Enemy

class Level:
    def __init__(self, player, screen):
        self.platforms = pygame.sprite.Group()
        self.player = player
        self.screen = screen
        self.coins = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.score = 0
        self.vertical_travel = 0
        self.platform_generation_threshold = 100
        self.last_player_y = player.rect.y  # Track the last Y position of the player
        self.load_level()
        self.load_coins()
        self.load_power_ups()
        self.load_enemies()


    def load_level(self):
        # Create the initial floor platform
        floor_height = 40
        floor = Platform(0, SCREEN_HEIGHT - floor_height, SCREEN_WIDTH, floor_height)
        self.platforms.add(floor)

        # Create a few initial visible platforms
        for i in range(5):  # Number of initial platforms
            width = random.randint(50, 100)
            height = 20
            x = random.randint(0, SCREEN_WIDTH - width)
            y = SCREEN_HEIGHT - floor_height - (i * 100)  # Spacing them out vertically
            platform = Platform(x, y, width, height)
            self.platforms.add(platform)
            self.highest_platform_y = y

    def generate_new_platform(self):
        width = random.randint(40, 100)
        height = 20
        x = random.randint(0, SCREEN_WIDTH - width)

        # Define player's maximum jump height
        player_jump_height = 120

        # Calculate the highest point the player can reach
        max_reachable_height = self.player.rect.y - player_jump_height

        # Define the vertical gap range
        min_vertical_gap = 20
        max_vertical_gap = 60

        # Generate the Y-coordinate of the new platform
        y_gap = random.randint(min_vertical_gap, max_vertical_gap)
        y = max_reachable_height - y_gap

        # Adjust to ensure platforms are not generated off-screen
        # The maximum height for new platforms is the screen height minus a certain threshold
        screen_threshold = 150  # Adjust this value as needed
        y = min(y, SCREEN_HEIGHT - screen_threshold)

        new_platform = Platform(x, y, width, height)
        self.platforms.add(new_platform)
        self.highest_platform_y = y

        print(f"New platform generated at x: {x}, y: {y}, width: {width}, height: {height}")


    def remove_offscreen_objects(self):
        # Remove platforms and other objects that are off the screen
        for sprite in list(self.platforms) + list(self.coins) + list(self.power_ups) + list(self.enemies):
            if sprite.rect.y > SCREEN_HEIGHT:
                sprite.kill()

    def load_enemies(self):
        for _ in range(5):  # Example: Generate 5 enemies
            x = random.randint(0, SCREEN_WIDTH - 40)
            y = random.randint(0, max(self.player.rect.y - 150, 0))  # Adjust Y-coordinate
            enemy = Enemy(x, y, 40, 40, random.choice([-2, 2]))
            self.enemies.add(enemy)

    def load_power_ups(self):
        for _ in range(3):  # Example: Generate 3 power-ups
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(0, max(self.player.rect.y - 200, 0))  # Adjust Y-coordinate
            power_up = PowerUp(x, y)
            self.power_ups.add(power_up)



    def load_coins(self):
        for _ in range(20):  # Example: Generate 10 coins
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(0, max(self.player.rect.y - 100, 0))  # Adjust Y-coordinate
            coin = Coin(x, y)
            self.coins.add(coin)
            
    def run(self):
        self.platforms.draw(self.screen)
        self.coins.draw(self.screen)
        self.power_ups.draw(self.screen)  # Draw the platforms using the provided screen
        self.enemies.draw(self.screen) 

    def draw_score(self):
        # Function to draw the score on the screen
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
    
    def update(self):
        if self.player.rect.y < SCREEN_HEIGHT / 4:  # If player moves above 1/4th screen height
            camera_move_y = SCREEN_HEIGHT / 4 - self.player.rect.y
            self.player.rect.y += camera_move_y
            for group in [self.platforms, self.coins, self.power_ups, self.enemies]:
                for sprite in group:
                    sprite.rect.y += camera_move_y

        self.vertical_travel += max(0, self.last_player_y - self.player.rect.y)
        self.last_player_y = self.player.rect.y

        if self.vertical_travel >= self.platform_generation_threshold:
            self.generate_new_platform()
            self.vertical_travel = 0

        self.remove_offscreen_objects()
        self.enemies.update()

        coins_collected = pygame.sprite.spritecollide(self.player, self.coins, True)
        if coins_collected:
            self.score += len(coins_collected)

        power_up_collected = pygame.sprite.spritecollide(self.player, self.power_ups, True)
        if power_up_collected:
            self.player.activate_power_up()
    pass
