import sys
import random
import pygame
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide


#GLOBAL-VARIABLES----------------------------

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SPACESHIP_SPEED = 5
BULLET_SPEED = 5
FALLING_SPEED = 1
BULLET_COOLDOWN = 100
BOTTOM_PADDING = 70
SIDE_PADDING = 50
LETTER_SPAWN_CHANCE = 60
FALL_OFFSET = -50

CYAN = (0, 255, 255)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (51, 51, 51)
DARK_BLUE = (10, 31, 68)

LETTER_SEQUENCE = "EID MUBARAK"
ALL_LETTERS = "EIDMUBARAKEIDMUBARAK  "
COLLECTED = ""

SPACESHIP_IMG= "spaceship.bmp"


####INIT-----------------------------------------------

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("Arial", 30)



####CLASSES----------------------------------------------

class Spaceship(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(SPACESHIP_IMG)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.lastShot = pygame.time.get_ticks()

    def update(self):
        key = pygame.key.get_pressed()
        if key[K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPACESHIP_SPEED
        if key[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += SPACESHIP_SPEED
        
        timeNow = pygame.time.get_ticks()
        if key[K_SPACE] and (timeNow - self.lastShot) > BULLET_COOLDOWN:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bulletGroup.add(bullet)
            self.lastShot = timeNow
            

class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()
        
        hit_letters = spritecollide(self, letterGroup, True)
        if hit_letters:
            self.kill()

class FallingLetter(Sprite):
    def __init__(self, x, y, letter):
        super().__init__()
        self.letter = letter
        letter_surface = font.render(self.letter, True, YELLOW)
        
        box_width = letter_surface.get_width() + 20
        box_height = letter_surface.get_height() + 20
        self.image = pygame.Surface((box_width, box_height))
        self.image.fill(DARK_GRAY)
        pygame.draw.rect(self.image, WHITE, (0, 0, box_width, box_height), 2)
        
        text_x = (box_width - letter_surface.get_width()) // 2
        text_y = (box_height - letter_surface.get_height()) // 2
        self.image.blit(letter_surface, (text_x, text_y))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += FALLING_SPEED
        if self.rect.top > SCREEN_HEIGHT:
            game_over()


############FUNCTIONS-----------------------
def game_over():
    print("Game Over!")
    pygame.quit()
    sys.exit()

def win_game():
    print("You won! You completed 'EID MUBARAK'.")
    pygame.quit()
    sys.exit()

def check_game_exit():
    key = pygame.key.get_pressed()
    if key[K_ESCAPE]:
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()



bulletGroup = Group()
letterGroup = Group()
ship = Spaceship(SCREEN_WIDTH // 2, SCREEN_HEIGHT - BOTTOM_PADDING)

def create_falling_letter():
    letter = random.choice(ALL_LETTERS)

    i = len(COLLECTED)
    letterNeed= LETTER_SEQUENCE[i]
    
    prob = random.randint(1,100)
    if prob >  65 : letter = letterNeed

    x = random.randint(SIDE_PADDING, SCREEN_WIDTH - SIDE_PADDING)
    falling_letter = FallingLetter(x, FALL_OFFSET, letter)
    letterGroup.add(falling_letter)

while True:
    screen.fill(DARK_BLUE)
    clock.tick(FPS)
    
    check_game_exit()
    
    if random.randint(1, LETTER_SPAWN_CHANCE) == 1:
        create_falling_letter()
    
    ship.update()
    bulletGroup.update()
    letterGroup.update()
    
    for letter in letterGroup.sprites():
        if spritecollide(ship, letterGroup, True):
            COLLECTED += letter.letter
            print(f"Collected Letter: {letter.letter}")

            if not LETTER_SEQUENCE.startswith(COLLECTED):
                print("Wrong character....")
                game_over()

            if COLLECTED == LETTER_SEQUENCE:
                win_game()
    

    screen.blit(ship.image, ship.rect)
    bulletGroup.draw(screen)
    letterGroup.draw(screen)
    

    #show current COLLECTED letters
    collectedSurface = font.render(f"Collected: {COLLECTED}", True, YELLOW)
    text_rect = collectedSurface.get_rect(center=(SCREEN_WIDTH // 2, 30))
    screen.blit(collectedSurface, text_rect)


    
    pygame.display.flip()

