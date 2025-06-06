import pygame
import time
import os
import random
pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space shooter")

# aliens ship
ALIEN_1 = pygame.image.load(os.path.join("assets", "alien.png"))
ALIEN_2 = pygame.image.load(os.path.join("assets", "alien2.png"))
ALIEN_3 = pygame.image.load(os.path.join("assets", "alien3.png"))

# player ship
PLAYER = pygame.transform.scale(pygame.image.load(os.path.join("assets", "shooter.png")), (64, 64))

# laser
ALIEN_1_LASER = pygame.image.load(os.path.join("assets", "alienlaser.png"))
ALIEN_2_LASER = pygame.image.load(os.path.join("assets", "alienlaser2.png"))
ALIEN_3_LASER = pygame.image.load(os.path.join("assets", "alienlaser3.png"))
PLAYER_LASER = pygame.image.load(os.path.join("assets", "playerlaser.png"))

# background 
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "bg.jpg")), (WIDTH, HEIGHT))

class Laser:
    def __init__(self, x , y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window) :
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=200):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x , self.y , self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=200):
        super().__init__(x, y, health)
        self.ship_img = PLAYER
        self.laser_img = PLAYER_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.health_bar(window)

    def health_bar(self, window):
        pygame.draw.rect(window, "red", (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 5))
        pygame.draw.rect(window, "green", (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width()*(self.health/self.max_health), 5))
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + 32 , self.y , self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Enemy(Ship):
    COLOR_MAP = {
                "green": (ALIEN_1, ALIEN_1_LASER),
                "yellow": (ALIEN_2, ALIEN_2_LASER),
                "blue": (ALIEN_3, ALIEN_3_LASER)
    }

    def __init__(self, x, y, color, health=200):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 30)
    lost_font = pygame.font.SysFont("comicsans", 40)

    enemies = []
    wave_length = 4
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5
  
    player = Player(300, 340)

    Clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", True, "white")
        level_label = main_font.render(f"Level: {level}", True, "white")

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, "white")
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, HEIGHT/2 - lost_label.get_height()/2))


        pygame.display.update()

    while run:
        Clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <=0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 4
            for i in range(wave_length):
                enemy = Enemy(random.randrange(32, WIDTH - 64), random.randrange(-1400, -100), random.choice(["green", "yellow", "blue"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*FPS) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        
        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        WIN.blit(BG,(0,0))
        title_label1 = title_font.render("MAIN MENU", 1, "white")
        title_label2 = title_font.render("Press the mouse to begin.....", 1, "white")
        WIN.blit(title_label1,(WIDTH/2 - title_label1.get_width()/2, title_label1.get_height()/2))
        WIN.blit(title_label2,(WIDTH/2 - title_label2.get_width()/2, HEIGHT/2 - title_label2.get_height()/2))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    
    pygame.quit()

main_menu()