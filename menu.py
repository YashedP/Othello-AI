import pygame


def show_menu(screen):
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)

    start_text = font.render("Start Game", True, (255, 255, 255))
    quit_text = font.render("Quit", True, (255, 255, 255))

    start_rect = start_text.get_rect(center=(320, 250))
    quit_rect = quit_text.get_rect(center=(320, 350))

    while True:
        screen.fill((0, 100, 0))  # Green background
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    return "GAME"
                elif quit_rect.collidepoint(event.pos):
                    return "QUIT"