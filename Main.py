################################################################################
# Header
################################################################################
# Date Started:     2 (February) / 18 (Saturday) / 2017 (Fall)
# School:           McNeese State University
# Class:            Computer Science 413-A - Software Engineering II
# Professor:        Dr. Kevin Cherry
# Team:             FooBar
# Members:          Taylor Venissat (Team Leader), Phuong Ho, Chance Johnson,
#                   Garrett Benoit, and Zackary Hermsen.
# Assignment:       Team-Programming-Assignment-01
# Language:         Python
# Tools:            Pygame (Library), Microsoft Visual Studios (IDE).

import pygame
from pygame.locals import *
import sgc
from sgc.locals import *
import random

resolution = (600, 600)
cell_margin = 10
cell_colors = (255, 255, 255), (0, 0, 0)
player_object = "@"
player_object_color = (255, 0, 0)
player_object_position = [0, 0]
chest_object = "C"
chest_object_opened = "O"
chest_object_color = (255, 0, 0)
chest_object_position = [0, 0]
key_object = "K"
key_object_removed = ""
key_object_color = (255, 0, 0)
key_object_position = [0, 0]
door_object = "D"
door_object_color = (255, 0, 0)
door_object_position = [8, 8]
object_size = 35
player_grabbed_key = False
player_used_key = False
player_opened_chest = False
game_complete = False

grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

pygame.init()

pygame.display.set_caption("Team-FooBar-Programming-Assignment-01")

screen = sgc.surface.Screen((600, 600))

input_box = sgc.InputBox((600, 30), label = "", 
                         default = "Input here, output console...")
input_box.config(pos = (0,562))
input_box.add(order = 0)

def main():
    global player_object
    global chest_object
    global key_object
    global door_object

    screen.fill(cell_colors[1])

    player_object = pygame.font.Font(None, object_size).render(
                                     player_object, False, player_object_color)

    chest_object = pygame.font.Font(None, object_size).render(
                                     chest_object, False, chest_object_color)

    key_object = pygame.font.Font(None, object_size).render(
                                     key_object, False, key_object_color)

    door_object = pygame.font.Font(None, object_size).render(
                                     door_object, False, door_object_color)

    generate_random_object_positions()

    while game_complete == False:
        for event in pygame.event.get():
            sgc.event(event)
            if event.type == GUI:
                input_string = event.text.lower()
                print input_string
                if input_string == "go forward":
                    go(0, -1)
                elif input_string == "go right":
                    go(1, 0)
                elif input_string == "go back":
                    go(0, 1)
                elif input_string == "go left":
                    go(-1, 0)
                elif input_string == "grab key":
                    grab_key()
                elif input_string == "open chest":
                    open_chest()
                elif input_string == "open door":
                    open_door()
                elif input_string == "use key":
                    use_key()

                if event.widget is input_box:
                    input_box.text = ""

            if event.type == KEYDOWN:
                key = event.key
                if key == K_UP:
                    go(0, -1)
                elif key == K_RIGHT:
                    go(1, 0)
                elif key == K_DOWN:
                    go(0, 1)
                elif key == K_LEFT:
                    go(-1, 0)
            elif event.type == QUIT:
                return

        draw_maze(screen)
        draw_player_object(player_object, screen)
        draw_chest_object(chest_object, screen)
        draw_key_object(key_object, screen)
        draw_door_object(door_object, screen)

        sgc.update(1)
        pygame.display.update()


def draw_maze(screen):
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            screen.fill(cell_colors[grid[column][row]],
                        get_cell_rect((row, column), screen))

def get_cell_rect(coordinates, screen):
    row, column = coordinates
    cell_width = screen.get_width() / len(grid)
    adjusted_width = cell_width - cell_margin
    return pygame.Rect(row * cell_width + cell_margin / 2,
                       column * cell_width + cell_margin / 2,
                       adjusted_width, adjusted_width)

def draw_player_object(player_object, screen):
    rect = player_object.get_rect()
    rect.center = get_cell_rect(player_object_position, screen).center
    screen.blit(player_object, rect)

def draw_chest_object(chest_object, screen):
    rect = chest_object.get_rect()
    rect.center = get_cell_rect(chest_object_position, screen).center
    screen.blit(chest_object, rect)

def draw_key_object(key_object, screen):
    rect = key_object.get_rect()
    rect.center = get_cell_rect(key_object_position, screen).center
    screen.blit(key_object, rect)

def draw_door_object(door_object, screen):
    rect = door_object.get_rect()
    rect.center = get_cell_rect(door_object_position, screen).center
    screen.blit(door_object, rect)

def generate_random_object_positions():
    global player_object_position
    global chest_object_position
    global key_object_position

    number_of_objects = 0
    
    while number_of_objects != 1:
        randomx = random.randint(1, 15)
        randomy = random.randint(1, 14)

        if not is_object_blocked(randomx, randomy):
            player_object_position = [randomx, randomy]
            number_of_objects += 1


    while number_of_objects != 2:
        randomx = random.randint(1, 15)
        randomy = random.randint(1, 14)

        if not is_object_blocked(randomx, randomy):
            chest_object_position = [randomx, randomy]
            number_of_objects += 1

    while number_of_objects != 3:
        randomx = random.randint(1, 15)
        randomy = random.randint(1, 14)

        if not is_object_blocked(randomx, randomy):
            key_object_position = [randomx, randomy]
            number_of_objects += 1

def is_object_blocked(x, y):
    if grid[x][y] == 0:
        return True
    elif [x, y] == player_object_position:
        return True
    elif [x, y] == chest_object_position:
        return True
    elif [x, y] == key_object_position:
        return True
    elif [x, y] == door_object_position:
        return True
 
    return False

def go(dx, dy):
    x, y = player_object_position
    nx, ny = x + dx, y + dy

    if (nx >= 0 and nx < len(grid) 
        and ny >= 0 and ny < len(grid[0]) and \
        grid[ny][nx]):
            player_object_position[0] = nx
            player_object_position[1] = ny

def grab_key():
    global key_object_position
    global player_grabbed_key
    global key_object_color

    x, y = player_object_position
    a, b = key_object_position

    if player_next_to_object(x, y, a, b):
        key_object_position = [0, 0]
        key_object = pygame.font.Font(None, object_size).render(
                                      key_object_removed, False, 
                                      key_object_color)
        player_grabbed_key = True

def open_chest():
    global chest_object
    global chest_object_position
    global player_opened_chest

    x, y = player_object_position
    a, b = chest_object_position

    if player_next_to_object(x, y, a, b):
        chest_object = pygame.font.Font(None, object_size).render(
                                        chest_object_opened, False, 
                                        chest_object_color)
        player_opened_chest = True

def use_key():
    global door_object_position
    global player_used_key

    x, y = player_object_position
    a, b = door_object_position

    if player_next_to_object(x, y, a, b):
        if player_grabbed_key and player_opened_chest:
            player_used_key = True

def open_door():
    global door_object
    global door_object_position
    global player_opened_chest
    global game_complete

    x, y = player_object_position
    a, b = door_object_position

    if player_next_to_object(x, y, a, b):
        if player_used_key:
            game_complete = True

def player_next_to_object(x, y, a, b):
    if x - 1 == a and y - 1 == b:
        return True
    elif x == a and y - 1 == b:
        return True
    elif x + 1 == a and y - 1 == b:
        return True
    elif x - 1 == a and y == b:
        return True
    elif x + 1 == a and y == b:
        return True
    elif x - 1 == a and y + 1 == b:
        return True
    elif x == a and y + 1 == b:
        return True
    elif x + 1 == a and y + 1 == b:
        return True

    return False

if __name__ == "__main__":
    main()
    pygame.quit()

