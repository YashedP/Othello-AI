import pygame
import asyncio
from menu import show_menu
from game import start_game

pygame.init()

# Window setup
WIDTH, HEIGHT = 640, 720  # 80 extra px for top and bottom bars
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello AI")

state = "MENU"
clock = pygame.time.Clock()

while True:
    if state == "MENU":
        # Menu is still synchronous
        state = show_menu(screen)

    elif state == "GAME":
        # Run the async game loop
        state = asyncio.run(start_game(screen))

    elif state == "QUIT":
        break

    clock.tick(60)

pygame.quit()