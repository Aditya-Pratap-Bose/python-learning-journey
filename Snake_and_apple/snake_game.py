import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 100, 5)

class Apple:
    def __init__(self, parent_screen):
         self.image = pygame.image.load("resources/apple.jpg").convert()
         self.parent_screen = parent_screen
         self.x = SIZE*3
         self.y = SIZE*3

    def draw(self):
        self.parent_screen.blit(self.image,(self.x,self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(2,24)*SIZE
        self.y = random.randint(2,14)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


    
    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'
        
    def move_up(self):
        self.direction = 'up'
        
    def move_down(self):
        self.direction = 'down'
        
    
    def walk(self):
        # body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        # head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range (self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Apple Game")

        pygame.mixer.init()
        self.play_bg_music()

        self.surface = pygame.display.set_mode((1000,600))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False
    
    def play_bg_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play() 
   
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)
    
    def render_bg(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg , (0,0))

    def play(self):
        self.render_bg()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake apple collision logic.
        if self.is_collision(self.snake.x[0],self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake snake collision logic
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision Occured"
            
        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 600):
            self.play_sound('crash')
            raise "Hit the boundry error"  
        
    def show_game_over(self):
        self.render_bg()
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game is Over! Your score is: {self.snake.length}", True, (255,255,255))
        self.surface.blit(line1, (330,260))
        line2 = font.render("To play again press enter. To exit press escape!",  True, (255,255,255))
        self.surface.blit(line2, (240,310))
        
        pygame.display.flip()

        pygame.mixer.music.pause()
        

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score, (850,10))


    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)
    
    def run(self):
        self.clock = pygame.time.Clock()
        running = True
        pause = False

        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_UP and self.snake.direction != 'down':
                            self.snake.move_up()

                        if event.key == K_DOWN and self.snake.direction != 'up':
                            self.snake.move_down()

                        if event.key == K_LEFT and self.snake.direction != 'right':
                            self.snake.move_left()

                        if event.key == K_RIGHT and self.snake.direction != 'left':
                            self.snake.move_right()
                    
                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                self.reset()
                pause = True

            time.sleep(0.2)
            




if __name__ == '__main__':
    game = Game()
    game.run()
 