import pygame
from pygame import mixer

import random
import math

pygame.init()

display = pygame.display.set_mode((800, 600))
background = pygame.load('images/game_background.png')

pygame.display.set_caption('Test Game')
start_game = pygame.image.load('images/startup.png')
pygame.display.set_icon(start_game)

player_icon = pygame.image.load('images/player.png')
player_icon_flip = pygame.transform.flip(player_icon, True, False)
player_x = 370
player_y = 480
player_x_change = 0

enemy_icon = []
enemy_icon_flip = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_squad_size = 7

for i in range(enemy_squad_size):
    enemy_icon.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.5)
    enemy_y_change.append(20)

for i in enemy_icon:
    enemy_image = pygame.image.load('enemy.png')
    enemy_icon_flip.append(pygame.transform.flip(enemy_image, True, False))

dagger = pygame.image.load('images/dagger.png')
dagger_x = 0
dagger_y = 480
dagger_x_change = 0
dagger_y_change = 1
dagger_state = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 22)
text_x = 10
text_y = 10

game_over_font = pygame.font.Font('freesansbold.ttf', 42)


def display_score(x, y):
    player_score = font.render("HITS: " + str(score), True, (255, 0, 255))
    screen.blit(player_score, (x, y))


def game_over_text():
    game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 255))
    screen.blit(game_over_text, (260, 250))


def player(x, y):
    if player_x_change == -0.3:
        screen.blit(player_icon, (x, y))
    else:
        screen.blit(player_icon_flip, (x, y))


def enemy(x, y, i):
    if enemy_x_change[i] == 0.3:
        screen.blit(enemy_icon[i], (x, y))
    else:
        screen.blit(enemy_icon_flip[i], (x, y))


def throw_dagger():
    global dagger_state
    dagger_state = "throw"
    screen.blit(dagger, (x + 16, y + 10))


def collision(enemy_x, enemy_y, dagger_x, dagger_y):
    distance = math.sqrt((math.pow(enemy_x - dagger_x, 2)) + 
                         (math.pow(enemy_y - bullet_y, 2)))
    return True if distance < 27 else False


game_in_play = True
while game_in_play:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_in_play = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.3
            if event.key == pygame.K_SPACE:
                if dagger_state == "ready":
                    dagger_x = player_x
                    throw_dagger(dagger_x, dagger_y)
                    dagger_sound = mixer.Sound('sound_fx/sfx_shoot.wav')
                    dagger_sound.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(enemy_squad_size):
        if enemy_y[i] > 440:
            for j in range(enemy_squad_size):
                enemy_y[j] = 2000
            game_over_text()
            break
        
        enemy_x[i] += enemy_x_change[i]

        if enemy_x <= 0:
            enemy_x_change[i] = 0.3
            enemy_y[i] += enemy_y_change[i]
            if enemy_x_change[i] == 0.3:
                print(enemy_x[i])
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -0.3
            enemy_y[i] += enemy_y_change[i]

        collision_event = collision(enemy_x[i], enemy_y[i], dagger_x, dagger_y)
        if collision_event:
            explosion_sound = mixer.Sound('sound_fx/sfx_explosion.wav')
            explosion_sound.play()
            dagger_y = 480
            dagger_state = "ready"
            score += 1

            if score == 50:
                win_music = mixer.Sound('sound_fx/sfx_win.wav')
                win_music.play()
            
        enemy(enemy_x[i], enemy_y[i], i)
    
    if dagger_y <= 0:
        dagger_y = 480
        dagger_state = "ready"
    if dagger_state == "throw":
        throw_dagger(dagger_x, dagger_y)
        dagger_y -= dagger_y_change

    player(player_x, player_y)
    display_score(text_x, text_y)
    pygame.display.update()
