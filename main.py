import sys
import random
import pygame
from time import sleep
from pygame.locals import *
from pygame.sprite import Sprite, Group, spritecollide

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
SPACESHIP_SPEED = 8
BULLET_SPEED = 5
FALLING_SPEED = 1
BULLET_COOLDOWN = 100
SPACESHIP_Y_OFFSET = 70
LETTER_SPAWN_CHANCE = 60
LETTER_FALL_START_Y = -50

CYAN = (0, 255, 255)
YELLOW = (255, 215, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (51, 51, 51)
DARK_BLUE = (10, 31, 68)

LETTER_SEQUENCE = "EID MUBARAK"
ALL_LETTER = "EEEEEEEIIIIIIIDDDDMMMMMUUUUBBBAAARRRAAKKKKKFSDOHAFUDSIOHFOISDAFSIOFHSDOFHSDIOAFHODWAFHOSD                                  "
collected = ""

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship Letter Collector")
font = pygame.font.SysFont("Arial", 30)

def check_game_exit():
    key = pygame.key.get_pressed()
    if key[K_ESCAPE]:
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

class Spaceship(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("image/spaceship.bmp")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        key = pygame.key.get_pressed()
        if key[K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPACESHIP_SPEED
        if key[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += SPACESHIP_SPEED
        
        time_now = pygame.time.get_ticks()
        if key[K_SPACE] and (time_now - self.last_shot) > BULLET_COOLDOWN:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullet_group.add(bullet)
            self.last_shot = time_now

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
        
        hit_letters = spritecollide(self, falling_letters, True)
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

def game_over():
    print("Game Over!")
    pygame.quit()
    sys.exit()

def win_game():
    print("You won! You completed 'EID MUBARAK'.")
    pygame.quit()
    sys.exit()

spaceship_group = Group()
bullet_group = Group()
falling_letters = Group()

spaceship = Spaceship(SCREEN_WIDTH // 2, SCREEN_HEIGHT - SPACESHIP_Y_OFFSET)
spaceship_group.add(spaceship)

def create_falling_letter():
    letter = random.choice(ALL_LETTER)
    x = random.randint(50, SCREEN_WIDTH - 50)
    falling_letter = FallingLetter(x, LETTER_FALL_START_Y, letter)
    falling_letters.add(falling_letter)

while True:
    screen.fill(DARK_BLUE)
    clock.tick(FPS)
    
    check_game_exit()
    
    if random.randint(1, LETTER_SPAWN_CHANCE) == 1:
        create_falling_letter()
    
    spaceship.update()
    bullet_group.update()
    falling_letters.update()
    
    for letter in falling_letters.sprites():
        if spritecollide(spaceship, falling_letters, True):
            collected += letter.letter
            print(f"Collected Letter: {letter.letter}")

            if not LETTER_SEQUENCE.startswith(collected):
                print("Wrong character....")
                game_over()

            if collected == LETTER_SEQUENCE:
                win_game()
    
    spaceship_group.draw(screen)
    bullet_group.draw(screen)
    falling_letters.draw(screen)
    
    collected_surface = font.render(f"Collected: {collected}", True, YELLOW)
    text_rect = collected_surface.get_rect(center=(SCREEN_WIDTH // 2, 30))
    screen.blit(collected_surface, text_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()
