import sys
print(sys.executable)

import socket
import pygame
import json

# server baglantilari - "Localhost" kendine baglar
SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connected = False
error_text = ""

try:
    client.connect((SERVER_IP, PORT))
    client.setblocking(False)
    connected = True
except Exception as e:
    error_text = str(e)

# pygame setup
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (65, 69, 66)
RED = (200, 50, 50)
font = pygame.font.SysFont(None, 36, italic=False, bold=False) 
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 800 
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong - Client")
clock = pygame.time.Clock()

state = {} 

recv_buffer = ""   # Sunucudan gelen JSON verilerini parça parça toplamak için

my_id = None
my_color = WHITE

running = True

while running:
    clock.tick(35) #artık daha akıcı

    # cikis
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # input verisi gonderilmesi
    keys = pygame.key.get_pressed()
    msg = ""
    if keys[pygame.K_UP] or keys[pygame.K_w]: msg += "U"
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: msg += "D"
    if keys[pygame.K_LEFT] or keys[pygame.K_a]: msg += "L"
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: msg += "R"
    
    if connected and msg:
        try:
            client.sendall(msg.encode()) #Send i Sendall la değiştirdim daha iyi oldu (garanti)
        except OSError as e:
            connected = False
            error_text = f"Veri gonderilemedi: {e}"

    # Gamestate verisi alinmasi + artık id ve color var
    try:
        data = client.recv(4096)

        if not data:
            connected = False
            error_text = "Sunucu baglantiyi kapatti."

        else:
            recv_buffer += data.decode()

            while "\n" in recv_buffer:
                line, recv_buffer = recv_buffer.split("\n", 1)

                if line.strip():
                    try:
                        state = json.loads(line)
                        my_id = state.get("my_id")

                        color_data = state.get("player_colors", {})
                        if my_id and my_id in color_data:
                            my_color = tuple(color_data[my_id])

                    except json.JSONDecodeError:
                        error_text = "Sunucudan bozuk veri geldi."

    except BlockingIOError:
        pass

    except ConnectionResetError:
        connected = False
        error_text = "Sunucu baglantiyi kesti."

    except OSError as e:
        connected = False
        error_text = f"Ag hatasi: {e}"

    # Ekran cizilmesi
    screen.fill(GREY)
    
    if not connected:
        text1 = font.render("Hosta baglanilamadi", True, RED)
        text2 = font.render(f"IP: {SERVER_IP}:{PORT}", True, WHITE)
        text3 = font.render("Host acik mi? IP dogru mu?", True, WHITE)
        text4 = font.render(error_text, True, RED)

        screen.blit(text1, (WINDOW_WIDTH//2 - text1.get_width()//2, WINDOW_HEIGHT//2 - 50))
        screen.blit(text2, (WINDOW_WIDTH//2 - text2.get_width()//2, WINDOW_HEIGHT//2))
        screen.blit(text3, (WINDOW_WIDTH//2 - text3.get_width()//2, WINDOW_HEIGHT//2 + 50))
        screen.blit(text4, (WINDOW_WIDTH//2 - text4.get_width()//2, WINDOW_HEIGHT//2 + 100))

        pygame.display.flip()
        continue
    
    # Sunucuya baglanilmadiysa
    if not state:
        score_text = font.render("Sunucuya baglaniliyor...", True, WHITE)
        screen.blit(score_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2))

    # Lobi ekrani   
    elif state.get("lobby"):
        text = font.render(f"LOBI: {state['p_count']} / 4 OYUNCU (Host bekleniyor...)", True, my_color) # artık kendi renginde bekleme yazısı
        screen.blit(text, (WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2))

    # Kazanan ekrani    
    elif state.get("winner"):
        text = font.render(f"OYUN BITTI! KAZANAN: {state['winner'].upper()}", True, RED)
        screen.blit(text, (WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2))
        
    else:
        pygame.draw.circle(screen, WHITE, state["ball_center"], 8)
        
        # Aktif raketlerin cizimi + renkli
        player_colors = state.get("player_colors", {})

        for pid, p in state["paddles"].items():
            color = tuple(player_colors.get(pid, [255, 255, 255]))
            pygame.draw.rect(screen, color, pygame.Rect(p[0], p[1], p[2], p[3]))
        
        # canlar
        try:
            lives = state.get("lives", {})
            player_colors = state.get("player_colors", {})
            y_offset = 20

            if "p1" in lives:
                color = tuple(player_colors.get("p1", [255, 255, 255]))
                screen.blit(font.render(f"P1 Can: {lives['p1']}", True, color), (20, y_offset))
                y_offset += 30

            if "p2" in lives:
                color = tuple(player_colors.get("p2", [255, 255, 255]))
                screen.blit(font.render(f"P2 Can: {lives['p2']}", True, color), (20, y_offset))
                y_offset += 30

            if "p3" in lives:
                color = tuple(player_colors.get("p3", [255, 255, 255]))
                screen.blit(font.render(f"P3 Can: {lives['p3']}", True, color), (20, y_offset))
                y_offset += 30

            if "p4" in lives:
                color = tuple(player_colors.get("p4", [255, 255, 255]))
                screen.blit(font.render(f"P4 Can: {lives['p4']}", True, color), (20, y_offset))
        except:
            score_text = font.render("Canlar yuklenemedi", True, WHITE)
            screen.blit(score_text, (20, 20))
            
    pygame.display.flip()

pygame.quit()
client.close()