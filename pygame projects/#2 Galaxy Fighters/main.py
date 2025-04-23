import pygame
import time
import os
pygame.init()

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighters")
pygame.display.set_icon(pygame.image.load("assets/icon.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', '749.jpg')), (WIDTH, HEIGHT))
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 64, 64
VEL = 3
BULLET_VEL = 7
MAX_BULLETS = 4

PINK_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont("comicsans", 20)
WINNER_FONT = pygame.font.SysFont("comicsans", 70)
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'explode.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'laser.mp3'))

PINK_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'pink.png'))
PINK_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(PINK_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assets', 'blue.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

def draw(pink, blue, pink_bullets, blue_bullets, pink_health, blue_health):
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, (0, 0, 0), BORDER)
    WIN.blit(PINK_SPACESHIP, (pink.x, pink.y))
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))


    for bullet in pink_bullets[:]:
        pygame.draw.rect(WIN, "pink", bullet)

    for bullet in blue_bullets[:]:
        pygame.draw.rect(WIN, "blue", bullet)

    pink_score = HEALTH_FONT.render(f"Health: {pink_health}", True, "white")
    blue_score = HEALTH_FONT.render(f"Health: {blue_health}", True, "white")
    WIN.blit(pink_score, (10, 10))
    WIN.blit(blue_score, (WIDTH - pink_score.get_width() - 15, 10))

    pygame.display.update()

# W, A, S, D
def pink_handle_movement(keys_pressed, pink):
        if keys_pressed[pygame.K_a] and pink.x - VEL >= 0:
            pink.x -= VEL
        if keys_pressed[pygame.K_d] and pink.x + pink.width + VEL <= BORDER.x:
            pink.x += VEL
        if keys_pressed[pygame.K_w] and pink.y - VEL>= 0:
            pink.y -= VEL
        if keys_pressed[pygame.K_s] and pink.y + pink.height + VEL <= HEIGHT:
            pink.y += VEL

# UP, DWON, LEFT, RIGHT
def blue_handle_movement(keys_pressed, blue):
        if keys_pressed[pygame.K_LEFT] and blue.x - VEL >= BORDER.width + BORDER.x:
            blue.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and blue.x + VEL + blue.width <= WIDTH :
            blue.x += VEL
        if keys_pressed[pygame.K_UP] and blue.y - VEL >= 0:
            blue.y -= VEL
        if keys_pressed[pygame.K_DOWN] and blue.y + blue.height + VEL <= HEIGHT:
            blue.y += VEL

def handle_bullets(pink_bullets, blue_bullets, pink, blue):
    for bullet in pink_bullets:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            pink_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            pink_bullets.remove(bullet)

    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if pink.colliderect(bullet):
            pygame.event.post(pygame.event.Event(PINK_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x < 0:
            blue_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, True, "white")
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    
    prompt_text = HEALTH_FONT.render("Press ENTER to play again or ESC to quit", True, "white")
    WIN.blit(prompt_text, (WIDTH/2 - prompt_text.get_width()/2, HEIGHT/2 + 50))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return



def main():
    pink = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    blue = pygame.Rect(800, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    pink_bullets = []
    blue_bullets = []

    pink_health = 10
    blue_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(pink_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(pink.x + pink.width, pink.y + pink.height//2 - 2, 10, 5)
                    pink_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                
                if event.key == pygame.K_RCTRL and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x, blue.y + blue.height//2 - 2, 10, 5)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == PINK_HIT:
                pink_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == BLUE_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()
                
        winner_text = ""
        if pink_health <= 0:
            winner_text = "BLUE WINS!"

        if blue_health <= 0:
            winner_text = "PINK WINS!"
        
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        pink_handle_movement(keys_pressed, pink)
        blue_handle_movement(keys_pressed, blue)
        handle_bullets(pink_bullets, blue_bullets, pink, blue)


        draw(pink, blue, pink_bullets, blue_bullets, pink_health, blue_health)

if __name__ == "__main__":
    while True:
        main()