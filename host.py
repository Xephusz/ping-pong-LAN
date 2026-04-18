import socket
import pygame
import json
import random

HOST = "0.0.0.0"
PORT = 5555

# network setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(3) 
server.setblocking(False)

# pygame setup
pygame.init()
WINDOW_SIZE = 800 
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Pong - Host (Lobi)")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (65, 69, 66)
RED = (200, 50, 50)
font = pygame.font.SysFont(None, 36)

# Raket boyutları
rect_w = 15
rect_l = 120
ball = pygame.Rect(WINDOW_SIZE//2, WINDOW_SIZE//2, 16, 16)
ball_vel = [0, 0]

# P1: Sol P2: Sağ P3: Üst P4: Alt
p1 = pygame.Rect(20, WINDOW_SIZE//2 - rect_l//2, rect_w, rect_l)
p2 = pygame.Rect(WINDOW_SIZE - 20 - rect_w, WINDOW_SIZE//2 - rect_l//2, rect_w, rect_l)
p3 = pygame.Rect(WINDOW_SIZE//2 - rect_l//2, 20, rect_l, rect_w)
p4 = pygame.Rect(WINDOW_SIZE//2 - rect_l//2, WINDOW_SIZE - 20 - rect_w, rect_l, rect_w)

control_speed = 12
speed_on_hit = 1

# Oyun Durumu Değişkenleri
clients = [] 
lobby_mode = True
active_players = ["p1"]
lives = {}
winner = None

# fonksiyonlar
def reset_ball():
    pygame.time.delay(500)
    ball.center = (WINDOW_SIZE// 2, WINDOW_SIZE // 2)
    
    # Rastgele yön (Dikey ya da Yatay)
    main_axis = random.choice([0, 1])

    if main_axis == 0:
        # Yataya giderse
        ball_vel[0] = random.choice([-6, 6])        
        ball_vel[1] = random.choice([-3, -2, 2, 3]) 
    else:
        # Dikeye giderse
        ball_vel[1] = random.choice([-6, 6])        
        ball_vel[0] = random.choice([-3, -2, 2, 3]) 

def clamp_paddle(paddle, is_vertical):
    if is_vertical:
        if paddle.top < 0: paddle.top = 0
        if paddle.bottom > WINDOW_SIZE: paddle.bottom = WINDOW_SIZE
    else:
        if paddle.left < 0: paddle.left = 0
        if paddle.right > WINDOW_SIZE: paddle.right = WINDOW_SIZE

def take_damage(player_id):
    lives[player_id] -= 1
    if lives[player_id] <= 0:
        active_players.remove(player_id)

running = True
print("Lobi oluşturuldu oyuncular bekleniyor")

while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Space ile lobiyi baslatma
        if lobby_mode and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            lobby_mode = False
            pygame.display.set_caption("Pong - Host")
            
            # Lobideki sayiya gore raket olusturma
            if len(clients) >= 1: active_players.append("p2")
            if len(clients) >= 2: active_players.append("p3")
            if len(clients) >= 3: active_players.append("p4")
            
            for p in active_players:
                lives[p] = 5 
            
            reset_ball()

    # lobi girisi
    if lobby_mode:
        try:
            conn, addr = server.accept()
            conn.setblocking(False)
            if len(clients) < 3:
                clients.append(conn)
                print(f"Oyuncu eklendi Toplam Oyuncu: {len(clients) + 1}")
        except:
            pass

    if not lobby_mode and not winner:

        # lobi boşsa
        if len(active_players) == 1:
            winner = active_players[0]
            ball_vel = [0, 0]
            ball.center = (-100, -100) 
        
        # client kontrolu
        for i, conn in enumerate(clients):
            try:
                data = conn.recv(1024)
                if data:
                    msg = data.decode()
                    if i == 0 and "p2" in active_players:
                        if "U" in msg: p2.y -= control_speed
                        if "D" in msg: p2.y += control_speed
                        clamp_paddle(p2, True)
                    elif i == 1 and "p3" in active_players:
                        if "L" in msg: p3.x -= control_speed
                        if "R" in msg: p3.x += control_speed
                        clamp_paddle(p3, False)
                    elif i == 2 and "p4" in active_players:
                        if "L" in msg: p4.x -= control_speed
                        if "R" in msg: p4.x += control_speed
                        clamp_paddle(p4, False)
            except:
                pass
        
        # Host kontrolu
        if "p1" in active_players:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: p1.y -= control_speed
            if keys[pygame.K_s]: p1.y += control_speed
            clamp_paddle(p1, True)

        # Top hareketi updateleme

        ball.x += ball_vel[0]
        ball.y += ball_vel[1]

        if ball.left <= 0:
            if "p1" in active_players: take_damage("p1"); reset_ball()
            else: ball.left = 0; ball_vel[0] *= -1 
        if ball.right >= WINDOW_SIZE:
            if "p2" in active_players: take_damage("p2"); reset_ball()
            else: ball.right = WINDOW_SIZE; ball_vel[0] *= -1
        if ball.top <= 0:
            if "p3" in active_players: take_damage("p3"); reset_ball()
            else: ball.top = 0; ball_vel[1] *= -1
        if ball.bottom >= WINDOW_SIZE:
            if "p4" in active_players: take_damage("p4"); reset_ball()
            else: ball.bottom = WINDOW_SIZE; ball_vel[1] *= -1

        if "p1" in active_players and ball.colliderect(p1) and ball_vel[0] < 0:
            offset = (ball.centery - p1.centery) / (p1.height / 2)
            ball.left = p1.right
            ball_vel[0] *= -1
            ball_vel[1] = int(offset * 5)
            ball_vel[0] += speed_on_hit

        if "p2" in active_players and ball.colliderect(p2) and ball_vel[0] > 0:
            offset = (ball.centery - p2.centery) / (p2.height / 2)
            ball.right = p2.left
            ball_vel[0] *= -1
            ball_vel[1] = int(offset * 5)
            ball_vel[0] -= speed_on_hit

        if "p3" in active_players and ball.colliderect(p3) and ball_vel[1] < 0:
            offset = (ball.centerx - p3.centerx) / (p3.width / 2)
            ball.top = p3.bottom
            ball_vel[1] *= -1
            ball_vel[0] = int(offset * 5)
            ball_vel[1] += speed_on_hit

        if "p4" in active_players and ball.colliderect(p4) and ball_vel[1] > 0:
            offset = (ball.centerx - p4.centerx) / (p4.width / 2)
            ball.bottom = p4.top
            ball_vel[1] *= -1
            ball_vel[0] = int(offset * 5)
            ball_vel[1] -= speed_on_hit

    # Gamestate
    game_state = {
        "lobby": lobby_mode,
        "p_count": len(clients) + 1,
        "ball_center": (ball.centerx, ball.centery),
        "paddles": [],
        "lives": lives,
        "winner": winner
    }
    
    if "p1" in active_players: game_state["paddles"].append((p1.x, p1.y, p1.width, p1.height))
    if "p2" in active_players: game_state["paddles"].append((p2.x, p2.y, p2.width, p2.height))
    if "p3" in active_players: game_state["paddles"].append((p3.x, p3.y, p3.width, p3.height))
    if "p4" in active_players: game_state["paddles"].append((p4.x, p4.y, p4.width, p4.height))

    # client'a veri gonderilmesi
    state_str = json.dumps(game_state) + "\n"
    for conn in clients:
        try: conn.send(state_str.encode())
        except: pass

    # Ekran cizilmesi
    screen.fill(GREY)
    
    if lobby_mode:
        text = font.render(f"LOBI: {len(clients) + 1} / 4 OYUNCU (Baslamak icin SPACE)", True, WHITE)
        screen.blit(text, (WINDOW_SIZE//2 - 250, WINDOW_SIZE//2))
    elif winner:
        text = font.render(f"Oyun bitti KAZANAN: {winner.upper()}", True, RED)
        screen.blit(text, (WINDOW_SIZE//2 - 180, WINDOW_SIZE//2))
    else:
        pygame.draw.circle(screen, WHITE, ball.center, 8)
        for p in game_state["paddles"]:
            pygame.draw.rect(screen, WHITE, pygame.Rect(p[0], p[1], p[2], p[3]))
        
        # Canlarin listelenmesi
        y_offset = 20
        if "p1" in lives: 
            screen.blit(font.render(f"P1 Can: {lives['p1']}", True, WHITE), (20, y_offset))
            y_offset += 30
        if "p2" in lives: 
            screen.blit(font.render(f"P2 Can: {lives['p2']}", True, WHITE), (20, y_offset))
            y_offset += 30
        if "p3" in lives: 
            screen.blit(font.render(f"P3 Can: {lives['p3']}", True, WHITE), (20, y_offset))
            y_offset += 30
        if "p4" in lives: 
            screen.blit(font.render(f"P4 Can: {lives['p4']}", True, WHITE), (20, y_offset))

    pygame.display.flip()

pygame.quit()
server.close()