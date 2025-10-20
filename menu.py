import pygame


def show_menu(screen):
    screen_width, screen_height = screen.get_size()

    # Fonts
    title_font = pygame.font.Font(None, 100)
    button_font = pygame.font.Font(None, 50)

    # Button setup
    button_width, button_height = 300, 60
    button_color = (180, 180, 180)  # Default grey
    hover_color = (220, 220, 220)  # Lighter grey on hover
    text_color = (0, 0, 0)

    # Buttons' text
    buttons = [
        ("Play as Black", "black"),
        ("Play as White", "white"),
        ("Quit", "QUIT")
    ]

    # Compute vertical spacing
    spacing = 30
    total_height = len(buttons) * button_height + (len(buttons) - 1) * spacing
    start_y = (screen_height - total_height) // 2 + 50  # shift down to leave space for title

    button_rects = []
    for i, (text, _) in enumerate(buttons):
        rect = pygame.Rect(
            (screen_width - button_width) // 2,
            start_y + i * (button_height + spacing),
            button_width,
            button_height
        )
        button_rects.append(rect)

    title_text = title_font.render("Othello", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_width // 2, 100))

    while True:
        screen.fill((0, 100, 0))  # Green background

        # Draw title
        screen.blit(title_text, title_rect)

        # Get mouse position
        mx, my = pygame.mouse.get_pos()

        # Draw buttons with hover effect
        for i, (text, _) in enumerate(buttons):
            rect = button_rects[i]
            color = hover_color if rect.collidepoint(mx, my) else button_color
            pygame.draw.rect(screen, color, rect, border_radius=10)
            rendered_text = button_font.render(text, True, text_color)
            text_rect = rendered_text.get_rect(center=rect.center)
            screen.blit(rendered_text, text_rect)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT", None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(event.pos):
                        choice = buttons[i][1]
                        if choice == "QUIT":
                            return "QUIT", None
                        else:
                            return "GAME", choice
