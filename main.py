import sys
import subprocess
import pygame
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


pygame.init()

WINDOW_W, WINDOW_H = 800, 800
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Pong LAN - Main Menu")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREY = (65, 69, 66)
DARK = (30, 30, 30)
YELLOW = (255, 220, 100)
RED = (200, 50, 50)

title_font = pygame.font.SysFont(None, 72)
menu_font = pygame.font.SysFont(None, 48)
info_font = pygame.font.SysFont(None, 32)

menu_options = ["HOSTLA", "KATIL", "CIK"]
game_state_mode = "MENU"
selected = 0

menu_mode = "main"
ip_text = ""

running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Menü ekranlarında Seçimler
        if menu_mode == "main":
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    selected = (selected - 1) % len(menu_options)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    selected = (selected + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    choice = menu_options[selected]

                    if choice == "HOSTLA":
                        game_state_mode = "MENU"
                        subprocess.Popen(
                            [sys.executable, os.path.join(BASE_DIR, "host.py")])
                        running = False
                    elif choice == "KATIL":
                        game_state_mode = "MENU"
                        menu_mode = "join_ip"
                        ip_text = ""
                    elif choice == "CIK":
                        running = False

        elif menu_mode == "join_ip":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu_mode = "main"
                elif event.key == pygame.K_RETURN:
                    entered_ip = ip_text.strip()
                    if entered_ip == "":
                        entered_ip = "127.0.0.1"  # localhost

                    subprocess.Popen([sys.executable, os.path.join(
                        BASE_DIR, "client.py"), entered_ip])
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    ip_text = ip_text[:-1]
                else:
                    if event.unicode in "0123456789.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-":
                        ip_text += event.unicode

    # Menu ve Lobi ekranlari Cizimi
    screen.fill(DARK)
    if menu_mode == "main":
        game_state_mode = "MENU"
        title = title_font.render("PONG LAN", True, WHITE)
        screen.blit(title, (WINDOW_W // 2 - title.get_width() // 2, 120))

        for i, option in enumerate(menu_options):
            color = YELLOW if i == selected else WHITE
            prefix = "> " if i == selected else "  "
            text = menu_font.render(prefix + option, True, color)
            screen.blit(text, (WINDOW_W // 2 - 120, 280 + i * 90))

        info1 = info_font.render("W/S veya Yukari/Asagi ile sec", True, GREY)
        info2 = info_font.render("ENTER ile onayla", True, GREY)

        screen.blit(info1, (WINDOW_W // 2 - info1.get_width() // 2, 620))
        screen.blit(info2, (WINDOW_W // 2 - info2.get_width() // 2, 655))

    elif menu_mode == "join_ip":
        title = title_font.render("HOSTA KATIL", True, WHITE)
        screen.blit(title, (WINDOW_W // 2 - title.get_width() // 2, 120))

        info = info_font.render("Host IP adresini gir:", True, WHITE)
        screen.blit(info, (WINDOW_W // 2 - info.get_width() // 2, 270))

        box = pygame.Rect(WINDOW_W // 2 - 220, 330, 440, 60)
        pygame.draw.rect(screen, GREY, box, border_radius=8)
        pygame.draw.rect(screen, WHITE, box, 3, border_radius=8)

        shown_ip = ip_text if ip_text else "ornek: 192.168.1.15"
        color = WHITE if ip_text else (180, 180, 180)
        ip_surface = menu_font.render(shown_ip, True, color)
        screen.blit(ip_surface, (box.x + 15, box.y + 13))

        info2 = info_font.render(
            "Bos birakirsan kendi pc'ne baglanir", True, GREY)
        info3 = info_font.render("ENTER = baglan | ESC = geri don", True, GREY)

        screen.blit(info2, (WINDOW_W // 2 - info2.get_width() // 2, 430))
        screen.blit(info3, (WINDOW_W // 2 - info3.get_width() // 2, 470))

    pygame.display.flip()

pygame.quit()
