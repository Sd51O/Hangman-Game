import pygame
import sys
from pygame.locals import *
import math
import random

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
red = (139, 0, 0)
FPS = 60
SCREENWIDTH = 950
SCREENHEIGHT = 650
GAME_WIN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

FPSCLOCK = pygame.time.Clock()
pygame.display.set_caption("HANGMAN")

RADIUS = 18
GAP = 20
letters = []
start_x = round((SCREENWIDTH - (RADIUS * 2 + GAP) * 13) / 2)
start_y = 500
A = 65
for i in range(26):
    x = start_x + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = start_y + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

alphabet_font = pygame.font.SysFont(None, 30)
win_font = pygame.font.SysFont(None, 50, bold=False, italic=True)
word_font = pygame.font.SysFont(None, 50)


def text_screen(text, color, x, y):
    screen_text = win_font.render(text, True, color)
    GAME_WIN.blit(screen_text, [x, y])


images = []
for i in range(7):
    img = pygame.image.load("hangman" + str(i) + ".png")
    images.append(img)


hangmanstatus = 0
words = ["INDIA", "APPLE", "ENGINEER", "SCIENTIST", "DOCTOR", "LAPTOP", "COMPUTER", "ANACONDA", "PYTHON", "SCHOOL",
         "STUPID", "SCENE", "RULE", "FAST", "TEETH", "RAILWAY", "GARDEN", "GROUND"]

word = random.choice(words)
guessed_alpha = []


def draw():
    GAME_WIN.fill(white)

    display_alpha = ""
    for letter in word:
        if letter in guessed_alpha:
            display_alpha += letter + " "
        else:
            display_alpha += "_ "
    text = word_font.render(display_alpha, True, red)
    GAME_WIN.blit(text, [470, 270])

    for letter in letters:
        x, y, alphabet, visible = letter
        if visible:
            pygame.draw.circle(GAME_WIN, red, (x, y), RADIUS, 3)
            alphabet_text = alphabet_font.render(alphabet, True, black)
            GAME_WIN.blit(alphabet_text, [x - alphabet_text.get_width() / 2, y - alphabet_text.get_height() / 2])
    GAME_WIN.blit(images[hangmanstatus], (100, 150))
    pygame.display.update()


def display_msg(message):
    pygame.time.delay(1000)
    GAME_WIN.fill(white)
    text = word_font.render(message, 1, black)
    GAME_WIN.blit(text, (SCREENWIDTH / 2 - text.get_width() / 2, SCREENHEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def welcome():
    exit_game = False
    hangman_poster = pygame.image.load('hangman.jpeg')
    hangman_icon = pygame.image.load('hangman-icon.jpeg')
    while not exit_game:
        GAME_WIN.fill((180, 180, 180))
        text_screen("Press Space To Play", red, 500, 350)
        GAME_WIN.blit(hangman_poster, (0, 10))
        GAME_WIN.blit(hangman_icon, (10, 220))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def game_loop():
    exit_game = False
    global hangmanstatus
    while not exit_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, alphabet, visible = letter
                    if visible:
                        DIST = math.sqrt((x - mouse_x) ** 2 + (y - mouse_y) **2)
                        if DIST < RADIUS:
                            letter[3] = False
                            guessed_alpha.append(alphabet)
                            if alphabet not in word:
                                hangmanstatus += 1
        draw()
        won = True
        for letter in word:
            if letter not in guessed_alpha:
                won = False
                break

        if won:
            display_msg("You WON!")
            break

        if hangmanstatus == 6:
            display_msg("YOU ARE HANGED!")
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    pygame.quit()
    sys.exit()


welcome()