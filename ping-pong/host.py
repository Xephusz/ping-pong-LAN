import socket
import pygame
import json
import random


HOST = "0.0.0.0"
PORT = 5555

# network setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for connection...")
conn, addr = server.accept()
print("Connected to:", addr)

conn.setblocking(False)


# pygame setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong - Player 2 (Client) ")
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (65, 69, 66)
font = pygame.font.SysFont(None, 24, italic=False, bold=False)

# gamestate setup
rect_width = 15
rect_length = 90
center_height = WINDOW_WIDTH // 2
center_height = WINDOW_HEIGHT//2

ball = pygame.Rect(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, rect_width, 10)
ball_vel = [4, 4]
p1 = pygame.Rect(20, center_height - 50, rect_width, rect_length)
p2 = pygame.Rect(WINDOW_WIDTH - 30, center_height-50, rect_width, rect_length)
pygame.display.set_caption("Pong - Player 1 (Host) ")
p1_score = 0
p2_score = 0
speed_on_hit = 2
control_speed = 12
running = True


# fonksiyonlar
def reset_ball(direction):
    pygame.time.delay(500)
    ball.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    start_speed = 6
    ball_vel[0] = start_speed * direction
    ball_vel[1] = random.choice([-3, -2, 2, 3])


def clamp_paddle(paddle):
    if paddle.y < 0:
        paddle.y = 0
    if paddle.bottom > WINDOW_HEIGHT:
        paddle.bottom = WINDOW_HEIGHT


while running:
    clock.tick(30)

    # cikis
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # client kontrolu
    try:
        data = conn.recv(1024)
        if data:
            msg = data.decode()
            if msg == "UP":
                p2.y -= control_speed
                clamp_paddle(p2)
            elif msg == "DOWN":
                p2.y += control_speed
                clamp_paddle(p2)
    except:
        pass

    # Host kontrolu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        p1.y -= control_speed
    if keys[pygame.K_s]:
        p1.y += control_speed
    clamp_paddle(p1)

    # Top hareketi updateleme
    ball.x += ball_vel[0]
    ball.y += ball_vel[1]

    if ball.top <= 0 or ball.bottom >= WINDOW_HEIGHT:
        ball_vel[1] *= -1

    if ball.colliderect(p1) and ball_vel[0] < 0:
        offset = (ball.centery - p1.centery) / (p1.height / 2)
        ball.left = p1.right
        ball_vel[0] *= -1
        ball_vel[1] = int(offset * 5)
        ball_vel[0] += speed_on_hit

    if ball.colliderect(p2) and ball_vel[0] > 0:
        offset = (ball.centery - p2.centery) / (p2.height / 2)
        ball.right = p2.left
        ball_vel[0] *= -1
        ball_vel[1] = int(offset * 5)
        ball_vel[0] -= speed_on_hit

    # Skorlar
    if ball.left > WINDOW_WIDTH:
        p1_score += 1
        reset_ball(direction=-1)

    if ball.right < 0:
        p2_score += 1
        reset_ball(direction=1)

    # Gamestate
    game_state = {
        "ball": (ball.x, ball.y),
        "p1": p1.y,
        "p2": p2.y,
        "score": (p1_score, p2_score)
    }

    # client'a veri gonderilmesi
    try:
        conn.send((json.dumps(game_state) + "\n").encode())
    except:
        pass

    # Ekran cizilmesi
    screen.fill(GREY)
    pygame.draw.rect(screen, WHITE, p1)
    pygame.draw.rect(screen, WHITE, p2)
    pygame.draw.rect(screen, WHITE, ball)
    score_text = font.render(
        f"p1 skor:{p1_score}   p2 skor:{p2_score}", True, WHITE)
    screen.blit(score_text, (WINDOW_WIDTH//2 - 40, 20))
    pygame.display.flip()

pygame.quit()
conn.close()
