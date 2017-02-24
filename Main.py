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
    print_introduction_message()

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
                elif input_string == "go chest":
                    print "Output: "
                elif input_string == "go key":
                    print "Output: "
                elif input_string == "go door":
                    print "Output: "
                elif input_string == "go wall":
                    print "Output: "
                elif input_string == "go marker":
                    print "Output: "
                elif input_string == "grab forward":
                    print "Output: "
                elif input_string == "grab right":
                    print "Output: "
                elif input_string == "grab back":
                    print "Output: "
                elif input_string == "grab left":
                    print "Output: "
                elif input_string == "grab chest":
                    print "Output: "
                elif input_string == "grab key":
                    if player_grabbed_key:
                        print "Output: You already have the key."
                    else:
                        grab_key()
                elif input_string == "grab door":
                    print "Output: "
                elif input_string == "grab wall":
                    print "Output: "
                elif input_string == "grab marker":
                    print "Output: "
                elif input_string == "open forward":
                    print "Output: "
                elif input_string == "open right":
                    print "Output: "
                elif input_string == "open back":
                    print "Output: "
                elif input_string == "open left":
                    print "Output: "
                elif input_string == "open chest":
                    if player_opened_chest:
                        print "Output: You have already opened the chest."
                    else:
                        open_chest()
                elif input_string == "open key":
                    print "Output: "
                elif input_string == "open door":
                    open_door()
                elif input_string == "open wall":
                    print "Output: "
                elif input_string == "open marker":
                    print "Output: "
                elif input_string == "use forward":
                    print "Output: "
                elif input_string == "use right":
                    print "Output: "
                elif input_string == "use back":
                    print "Output: "
                elif input_string == "use left":
                    print "Output: "
                elif input_string == "use chest":
                    print "Output: "
                elif input_string == "use key":
                    if player_used_key:
                        print "You have already unlocked the door."
                    else:
                        use_key()
                elif input_string == "use door":
                    print "Output: "
                elif input_string == "use wall":
                    print "Output: "
                elif input_string == "use marker":
                    use_marker()
                else:
                    print_input_error()

                if event.widget is input_box:
                    clear()

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

def print_introduction_message():
    print ("\nIntroduction: Grab the key, open the chest, "
            "then find your way out...\n")

def print_input(input):
    print "\nInput: " + input

def print_go_error():
    print "Output: Invalid move command..."

def print_input_error():
    print "Output: Invalid input. Command not recognized..." 

def clear():
    input_box.text = ""

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
        print "Output: You have picked up the key!"
        key_object_position = [0, 0]
        key_object = pygame.font.Font(None, object_size).render(
                                      key_object_removed, False, 
                                      key_object_color)
        player_grabbed_key = True
    else:
        print "Output: The key is not within reach..."

def open_chest():
    global chest_object
    global chest_object_position
    global player_opened_chest

    x, y = player_object_position
    a, b = chest_object_position

    if player_next_to_object(x, y, a, b):
        print "Output: You have opened the chest!"
        chest_object = pygame.font.Font(None, object_size).render(
                                        chest_object_opened, False, 
                                        chest_object_color)
        player_opened_chest = True
    else:
        print "Output: The chest is not within reach..."

def use_key():
    global door_object_position
    global player_used_key

    x, y = player_object_position
    a, b = door_object_position

    if player_next_to_object(x, y, a, b):
        if player_grabbed_key and player_opened_chest:
            print "Output: You have unlocked the door!"
            player_used_key = True
        elif player_grabbed_key and not player_opened_chest:
            print ("Output: You must open the chest "
                   "before you can open the door.")
        else:
            print ("Output: You must grab the "
                   "key before you can use it.")
    else:
        print "Output: the door is not within reach..."

def open_door():
    global door_object
    global door_object_position
    global player_opened_chest
    global game_complete

    x, y = player_object_position
    a, b = door_object_position

    if player_next_to_object(x, y, a, b):
        if player_used_key:
            print "Output: You have opened the door!"
            print "\n\nCongratulations! You have escaped!\n\n"
            game_complete = True
        elif player_grabbed_key and player_opened_chest:
            print ("Output: You have to use the key "
                    "before you can open the door.")
        elif player_grabbed_key and not player_opened_chest:
            print ("Output: You must open the chest "
                    "before you can open the door.")
        else:
            print ("Output: You must grab the key and open " 
                    "the chest before you can open the door.")
    else:
        print "Output: The door is not within reach..."

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

