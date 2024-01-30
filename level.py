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
        self.screen = screen  # Store the screen for drawing
        self.coins = pygame.sprite.Group()
        self.load_coins()
        self.load_level()
        self.score = 0 
        self.power_ups = pygame.sprite.Group()
        self.load_power_ups()
        self.enemies = pygame.sprite.Group()
        self.load_enemies()


    def load_level(self):
        # Floor platform
        floor_height = 40  # Height of the floor platform
        floor = Platform(0, SCREEN_HEIGHT - floor_height, SCREEN_WIDTH, floor_height)
        self.platforms.add(floor)

        # Procedural generation of other platforms
        last_y = SCREEN_HEIGHT - 40 - floor_height  # Start above the floor
        for _ in range(10):  # Generate 10 platforms as an example
            width = random.randint(50, 100)
            height = 20  # Fixed height for platforms
            x = random.randint(0, SCREEN_WIDTH - width)
            max_jump_height = 120
            y = max(random.randint(last_y - max_jump_height, last_y), floor_height)

            platform = Platform(x, y, width, height)
            self.platforms.add(platform)
            last_y = y

    def load_enemies(self):
        # Place enemies at random positions
        for _ in range(5):  # Example: Generate 5 enemies
            x = random.randint(0, SCREEN_WIDTH - 40)
            y = random.randint(0, SCREEN_HEIGHT - 80)
            enemy = Enemy(x, y, 40, 40, random.choice([-2, 2]))
            self.enemies.add(enemy)

    def load_power_ups(self):
        # Place power-ups at random positions
        for _ in range(3):  # Example: Generate 3 power-ups
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(0, SCREEN_HEIGHT - 60)
            power_up = PowerUp(x, y)
            self.power_ups.add(power_up)


    def load_coins(self):
        # Place coins at random positions
        for _ in range(20):  # Example: Generate 10 coins
            x = random.randint(0, SCREEN_WIDTH - 20)
            y = random.randint(0, SCREEN_HEIGHT - 60)
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
        self.enemies.update()
        coins_collected = pygame.sprite.spritecollide(self.player, self.coins, True)
        if coins_collected:
            self.score += len(coins_collected)
        power_up_collected = pygame.sprite.spritecollide(self.player, self.power_ups, True)
        if power_up_collected:
            self.player.activate_power_up()    
        pass
