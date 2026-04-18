import socket
import pygame
import json

# server baglantilari - "Localhost" kendine baglar
SERVER_IP = "localhost"
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))
client.setblocking(False)

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
running = True

while running:
    clock.tick(30)

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
    
    if msg:
        try:
            client.send(msg.encode())
        except:
            pass

    # Gamestate verisi alinmasi
    try:
        data = client.recv(2048)
        if data:
            state = json.loads(data.decode())
    except:
        pass

    # Ekran cizilmesi
    screen.fill(GREY)
    
    # Sunucuya baglanilmadiysa
    if not state:
        score_text = font.render("Sunucuya baglaniliyor...", True, WHITE)
        screen.blit(score_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2))

    # Lobi ekrani   
    elif state.get("lobby"):
        text = font.render(f"LOBI: {state['p_count']} / 4 OYUNCU (Host bekleniyor...)", True, WHITE)
        screen.blit(text, (WINDOW_WIDTH//2 - 250, WINDOW_HEIGHT//2))

    # Kazanan ekrani    
    elif state.get("winner"):
        text = font.render(f"OYUN BITTI! KAZANAN: {state['winner'].upper()}", True, RED)
        screen.blit(text, (WINDOW_WIDTH//2 - 180, WINDOW_HEIGHT//2))
        
    else:
        pygame.draw.circle(screen, WHITE, state["ball_center"], 8)
        
        # Aktif raketlerin cizimi 
        for p in state["paddles"]:
            pygame.draw.rect(screen, WHITE, pygame.Rect(p[0], p[1], p[2], p[3]))
        
        # canlar
        try:
            lives = state.get("lives", {})
            y_offset = 20
            if "p1" in lives: 
                screen.blit(font.render(f"p1 can:{lives['p1']}", True, WHITE), (20, y_offset))
                y_offset += 30
            if "p2" in lives: 
                screen.blit(font.render(f"p2 can:{lives['p2']}", True, WHITE), (20, y_offset))
                y_offset += 30
            if "p3" in lives: 
                screen.blit(font.render(f"p3 can:{lives['p3']}", True, WHITE), (20, y_offset))
                y_offset += 30
            if "p4" in lives: 
                screen.blit(font.render(f"p4 can:{lives['p4']}", True, WHITE), (20, y_offset))
        except:
            score_text = font.render("Canlar yuklenemedi", True, WHITE)
            screen.blit(score_text, (20, 20))
            
    pygame.display.flip()

pygame.quit()
client.close()