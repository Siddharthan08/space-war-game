import pygame

pygame.font.init()

pygame.mixer.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
VEL = 1
BULLET_VEL = 2
MAX_BULLET = 2
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
pygame.display.set_caption("Space War")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 5, HEIGHT)
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load("spaceship_yellow.png")
RED_SPACESHIP_IMAGE = pygame.image.load("spaceship_red.png")
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load("space.png"), (WIDTH, HEIGHT))
yellow_bullet = []
red_bullet = []
BULLET_SOUND = pygame.mixer.Sound("Gun+Silencer.mp3")
HIT_SOUND = pygame.mixer.Sound("Grenade+1.mp3")


def draw_Window(yellow, red, yellow_bullet, red_bullet, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)
    YELLOW_HEALTH_TEXT = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    RED_HEALTH_TEXT = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    WIN.blit(YELLOW_HEALTH_TEXT, (10, 10))
    WIN.blit(RED_HEALTH_TEXT, (WIDTH - RED_HEALTH_TEXT.get_width() - 10, 10))
    for bullet in red_bullet:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullet:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL < BORDER.x - SPACESHIP_HEIGHT:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL < HEIGHT - SPACESHIP_WIDTH:  # down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - 1 > BORDER.x + 5:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + 1 < WIDTH - SPACESHIP_HEIGHT:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - 1 > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + 1 < HEIGHT - SPACESHIP_WIDTH:  # down
        red.y += VEL


def handle_bullets(yellow_bullet, red_bullet, yellow, red):
    for bullet in yellow_bullet:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullet.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullet.remove(bullet)
    for bullet in red_bullet:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullet.remove(bullet)
        elif bullet.x < 0:
            red_bullet.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, GREEN)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    yellow = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(800, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_health = 10
    yellow_health = 10
    RUN = True
    Clock = pygame.time.Clock()
    while RUN:
        for event in pygame.event.get():
            Clock.tick(FPS)
            if event.type == pygame.QUIT:
                RUN = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(yellow.x + SPACESHIP_HEIGHT, yellow.y + SPACESHIP_WIDTH // 2, 10, 5)
                    yellow_bullet.append(bullet)
                    BULLET_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(red.x, red.y + SPACESHIP_WIDTH // 2, 10, 5)
                    red_bullet.append(bullet)
                    BULLET_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                HIT_SOUND.play()
        winner_text = ''
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullet, red_bullet, yellow, red)
        draw_Window(yellow, red, yellow_bullet, red_bullet, red_health, yellow_health)
    main()


if __name__ == '__main__':
    main()
