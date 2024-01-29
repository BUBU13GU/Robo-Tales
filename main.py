import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player
from level import Level

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robo Tales")

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def main_menu(screen):
    menu_options = ["Start Game", "Settings", "Exit"]
    current_option = 0

    def draw_menu():
        screen.fill((0, 0, 0))
        for i, option in enumerate(menu_options):
            text = option
            if i == current_option:
                text = "> " + option + " <"
            draw_text(screen, text, 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + i * 40)
        pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_option = (current_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    current_option = (current_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if menu_options[current_option] == "Start Game":
                        running = False  # Start the game
                    elif menu_options[current_option] == "Exit":
                        pygame.quit()
                        sys.exit()
                    # Handle other options like "Settings", "Levels", etc.
        draw_menu()
def pause_game(screen):
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Resume game
                    paused = False
                elif event.key == pygame.K_ESCAPE:  # Additional way to unpause
                    paused = False
                elif event.key == pygame.K_x: 
                        pygame.quit()
                        sys.exit()    

        screen.fill((0, 0, 0))
        draw_text(screen, "Game Paused", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text(screen, "Press ENTER to Resume", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text(screen, "Press X to EXIT", 30, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.display.flip()
# Main game loop
def main():
    clock = pygame.time.Clock()
    player = Player()  # Create a player instance
    level = Level(player, screen)  # Create a level instance
    all_sprites = pygame.sprite.Group()  # Create a sprite group
    all_sprites.add(player)
    player.current_level = level

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Pause game
                    pause_game(screen)    
            if event.type == pygame.USEREVENT:
                player.deactivate_power_up()
            if pygame.sprite.spritecollide(player, level.enemies, False):
                print("Player hit an enemy!")    
        # Game logic updates
        all_sprites.update()  # Update all sprites
        level.update() 

        # Collision detection with platforms
        platforms_hit = pygame.sprite.spritecollide(player, level.platforms, False)
        for platform in platforms_hit:
            if player.velocity_y > 0:
                player.rect.bottom = platform.rect.top
                player.velocity_y = 0

        screen.fill((0, 0, 0))
        level.run()
        level.draw_score()
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu(screen)
    main()
