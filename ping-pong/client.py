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
font = pygame.font.SysFont(None, 24, italic=False, bold=False)
WINDOW_WIDTH, WINDOW_HEIGHT = 1024, 720
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong - Player 2 (Client) ")
clock = pygame.time.Clock()


# gamestate
rect_width = 15
rect_length = 90
center_height = WINDOW_WIDTH // 2
center_height = WINDOW_HEIGHT//2

ball = pygame.Rect(10, center_height, 10, 10)
p1 = pygame.Rect(20, center_height - 50, rect_width, rect_length)
p2 = pygame.Rect(WINDOW_WIDTH - 30, center_height-50, rect_width, rect_length)
p1_score = 0
p2_score = 0

running = True

while running:
    clock.tick(30)

    # cikis
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # input verisi gonderilmesi
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        try:
            client.send(b"UP")
        except:
            pass
    elif keys[pygame.K_DOWN]:
        try:
            client.send(b"DOWN")
        except:
            pass

    # Gamestate verisi alinmasi
    try:
        data = client.recv(1024)
        if data:
            state = json.loads(data.decode())

            ball.x, ball.y = state["ball"]
            p1.y = state["p1"]
            p2.y = state["p2"]
            p1_score, p2_score = state["score"]
    except:
        pass

    # Ekran cizilmesi
    screen.fill(GREY)
    pygame.draw.rect(screen, WHITE, p1)
    pygame.draw.rect(screen, WHITE, p2)
    pygame.draw.rect(screen, WHITE, ball)
    try:
        score_text = font.render(
            f"p1 skor:{p1_score}   p2 skor:{p2_score}", True, WHITE)
        screen.blit(score_text, (WINDOW_WIDTH//2 - 40, 20))
    except:
        score_text = font.render(
            f"p1 skor:{-1}   p2 skor:{-1}", True, WHITE)
        screen.blit(score_text, (WINDOW_WIDTH//2 - 40, 20))
    pygame.display.flip()

pygame.quit()
client.close()
