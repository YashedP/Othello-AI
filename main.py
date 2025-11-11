"""
Othello AI Project
Authors: Daniel Acosta, Yash Jani
Intro Artificial Intelligence
Date of Submission: 11/10/2025
"""

import pygame
import asyncio
from menu import show_menu
from game import start_game

pygame.init()

# Window setup
WIDTH, HEIGHT = 640, 720  # 80 extra px for top and bottom bars
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello Game")

state = "MENU"
player_color = "black"  # default
clock = pygame.time.Clock()

while True:
    if state == "MENU":
        state, player_color = show_menu(screen)

    elif state == "GAME":
        state = asyncio.run(start_game(screen, player_color))

    elif state == "QUIT":
        break

pygame.quit()