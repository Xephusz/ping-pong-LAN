import sys
import subprocess
import os
import socket
import pygame
import json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# server baglantilari
SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
error_text = ""

try:
    client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    client.connect((SERVER_IP, PORT))
    client.setblocking(False)
    connected = True
except Exception as e:
    error_text = str(e)

# pygame setup
pygame.init()

# oyun sesleri
pygame.mixer.init()
try:
    hit_sound = pygame.mixer.Sound("hit.wav")
    hit_sound.set_volume(0.5)
except:
    hit_sound = None
    print("UYARI: hit.wav dosyasi bulunamadi, oyun sessiz calisacak.")
win_sound_played = False
try:
    win_sound = pygame.mixer.Sound("win.wav")
    win_sound.set_volume(0.7)
except:
    win_sound = None

WHITE = (255, 255, 255)
GREY = (65, 69, 66)
RED = (200, 50, 50)

font = pygame.font.SysFont(None, 36)
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong - Client")
clock = pygame.time.Clock()

gamestate = {}
recv_buffer = ""  # Sunucudan gelen JSON verilerini parça parça toplamak için
my_id = None
my_color = WHITE
game_state_mode = "GAME"
running = True

while running:
    clock.tick(60)  # artık daha akıcı

    # cikis
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_state_mode = "MENU"
            subprocess.Popen(
                [sys.executable, os.path.join(BASE_DIR, "main.py")]
            )
            running = False

    # input verisi gonderilmesi
    keys = pygame.key.get_pressed()
    msg = ""
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        msg += "U"
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        msg += "D"
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        msg += "L"
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        msg += "R"

    if connected and msg:
        try:
            # Send i Sendall la değiştirdim daha iyi oldu (garanti) + \n eklendi
            client.sendall((msg + "\n").encode())
        except:
            connected = False
            error_text = "Sunucu ile baglanti kurulamadi"

    # Gamestate verisi alinmasi + artık id ve color var
    try:
        data = client.recv(4096)
        if not data:
            connected = False
            error_text = "Sunucu baglantisi kesildi"

        else:
            recv_buffer += data.decode()
            while "\n" in recv_buffer:
                line, recv_buffer = recv_buffer.split("\n", 1)
                if line.strip():
                    try:
                        gamestate = json.loads(line)
                        my_id = gamestate.get("my_id")

                        color_data = gamestate.get("player_colors", {})
                        if my_id and my_id in color_data:
                            my_color = tuple(color_data[my_id])

                        if gamestate.get("play_sound") and hit_sound:
                            hit_sound.play()

                    except json.JSONDecodeError:
                        print("Packet decode Error")
                        pass

    except BlockingIOError:
        pass
    except:
        connected = False

    # Ekran cizilmesi
    screen.fill(GREY)

    if not connected:
        text1 = font.render(
            "Hosta baglanilamadi (Menüye dönmek için ESC)", True, RED)
        text2 = font.render(f"IP: {SERVER_IP}:{PORT}", True, WHITE)
        text3 = font.render("Host acik mi? IP dogru mu?", True, WHITE)
        text4 = font.render(error_text, True, RED)

        screen.blit(text1, (WINDOW_WIDTH//2 -
                    text1.get_width()//2, WINDOW_HEIGHT//2 - 50))
        screen.blit(text2, (WINDOW_WIDTH//2 -
                    text2.get_width()//2, WINDOW_HEIGHT//2))
        screen.blit(text3, (WINDOW_WIDTH//2 -
                    text3.get_width()//2, WINDOW_HEIGHT//2 + 50))
        screen.blit(text4, (WINDOW_WIDTH//2 - text4.get_width() //
                    2, WINDOW_HEIGHT//2 + 100))
        pygame.display.flip()

        continue

    # Sunucuya baglanilmadiysa
    if not gamestate:
        score_text = font.render("Sunucuya baglaniliyor...", True, WHITE)
        screen.blit(score_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2))

    # Lobi ekrani
    elif gamestate.get("lobby"):
        # artık kendi renginde bekleme yazısı
        text = font.render(
            f"LOBI: {gamestate['p_count']} / 4 OYUNCU (Host bekleniyor...)", True, my_color)
        screen.blit(text, (WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2))

    # Kazanan ekrani
    elif gamestate.get("winner"):
        if win_sound and not win_sound_played:
            win_sound.play()
            win_sound_played = True
        text = font.render(
            f"OYUN BITTI! KAZANAN: {gamestate['winner'].upper()}", True, RED)
        text_restart = font.render(
            "Hostun lobiyi yeniden kurmasi bekleniyor... (Cikmak icin ESC)", True, WHITE)
        screen.blit(text, (WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2))
        screen.blit(text_restart, (WINDOW_WIDTH //
                    2 - 280, WINDOW_HEIGHT//2 + 40))

    else:
        pygame.draw.circle(screen, WHITE, gamestate["ball_center"], 8)

        # Aktif raketlerin cizimi + renkli
        player_colors = gamestate.get("player_colors", {})
        for pid, p in gamestate["paddles"].items():
            color = tuple(player_colors.get(pid, [255, 255, 255]))
            pygame.draw.rect(screen, color, pygame.Rect(
                p[0], p[1], p[2], p[3]))

        # canlar
        try:
            lives = gamestate.get("lives", {})
            y_offset = 20
            for pid in ["p1", "p2", "p3", "p4"]:
                if pid in lives:
                    color = tuple(player_colors.get(pid, [255, 255, 255]))
                    screen.blit(font.render(
                        f"{pid.upper()} Can: {lives[pid]}", True, color), (20, y_offset))
                    y_offset += 30
        except:
            pass

    pygame.display.flip()

pygame.quit()
client.close()
