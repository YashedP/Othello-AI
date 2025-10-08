import pygame
from menu import show_menu
from game import start_game

pygame.init()

# Window setup
WIDTH, HEIGHT = 640, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello AI")

# Game loop control
state = "MENU"
clock = pygame.time.Clock()

while True:
    if state == "MENU":
        state = show_menu(screen)
    elif state == "GAME":
        state = start_game(screen)
    elif state == "QUIT":
        break

    clock.tick(60)

pygame.quit()