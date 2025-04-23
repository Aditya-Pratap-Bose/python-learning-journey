import pygame
import random
import time
import os
pygame.init()


WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")
pygame.display.set_icon(pygame.image.load("rain.png"))

BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))
FPS = 60

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 50
PLAYER_VEL = 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 2

FONT = pygame.font.SysFont("comicsans", 30)

def draw(player, elasped_time, stars):
    WIN.blit(BG, (0, 0))
    
    time_text = FONT.render(f"Time: {round(elasped_time)}s", True, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)
    
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run = True
    
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elasped_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False
    
    while run:
        star_count += clock.tick(FPS)
        elasped_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 70)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break 
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        
        if hit:
            WIN.blit(BG, (0, 0))
            FONT = pygame.font.SysFont("comicsans", 100)
            lost_text = FONT.render("YOU LOST!", True, "white")
            WIN.blit(lost_text,(WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            
            FONT = pygame.font.SysFont("comicsans", 50)
            play_again_text = FONT.render(f"Yoyr Score: {round(elasped_time)} seconds ,, ENTER to play again...", True, "white")
            WIN.blit(play_again_text, (WIDTH/2 - play_again_text.get_width()/2, HEIGHT/2 + 50))
            pygame.display.update()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)  or event.type == pygame.QUIT:
                        waiting = False
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        waiting = False
                        main()



        draw(player, elasped_time, stars)
          
    
    
if __name__ == "__main__":
    main()