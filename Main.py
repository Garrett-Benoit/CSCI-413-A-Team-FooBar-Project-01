################################################################################
# Header
################################################################################
# Date Started:     2 (February) / 11 (Saturday) / 2017 (Fall)
# Date Completed:   2 (February) / 15 (Wednesday) / 2017 (Fall)
# School:           McNeese State University
# Class:            Computer Science 413-A - Software Engineering II 
# Professor:        Dr. Kevin Cherry
# Team:             FooBar
# Members:          Taylor Venissat (Team Leader), Phuong Ho, Chance Johnson, 
#                   Garrett Benoit, and Zackary Hermsen.
# Assignment:       Team-Programming-Assignment-01
# Language:         Python
# Tools:            Pygame (Library), Microsoft Visual Studios (IDE).



################################################################################
# Imports
################################################################################

import pygame
from pygame.locals import *
import sgc
from sgc.locals import *
import random



################################################################################
# Initialization
################################################################################

cell_margin = 5 # Pre-defined space between cells.
cell_colors = (255, 255, 255), (0, 0, 0) # RBG values representing cell colors.
player_object = "@" # Symbol representing the player character.
player_object_color = (255, 255, 255) # Color of the player character.
player_object_position = [0, 0] # Position of the player character.
chest_object = "C" # Symbol representing the chest.
chest_object_opened = "O" # Symbol representing the opened chest.
chest_object_color = (255, 255, 255) # Color of the chest.
chest_object_position = [0, 0] # Position of the chest.
key_object = "K" # Symbol representing the key.
key_object_color = (255, 255, 255) # Color of the key.
key_object_position = [0, 0] # Position of the key.
door_object = "D" # Symbol representing the door.
door_object_color = (255, 255, 255) # Color of the door.
door_object_position = [0, 0] # Position of the door.
# Symbol representing the first chest combination.
chest_combination_1_object = str(random.randint(0, 9))
# Color of the chest_combination_1_object.
chest_combination_1_object_color = (0, 0, 0)
# Position of the chest_combination_1_object.
chest_combination_1_object_position = [0, 0]
# Symbol representing the second chest combination.
chest_combination_2_object = str(random.randint(0, 9))
# Color of the chest_combination_2_object.
chest_combination_2_object_color = (0, 0, 0)
# Position of the chest_combination_2_object.
chest_combination_2_object_position = [0, 0]
# Symbol representing the third chest combination.
chest_combination_3_object = str(random.randint(0, 9))
# Color of the chest_combination_3_object.
chest_combination_3_object_color = (0, 0, 0)
# Position of the chest_combination_3_object.
chest_combination_3_object_position = [0, 0]
object_size = 35 # Size of all objects drawn to the console window.
player_grabbed_key = False
player_used_key = False
player_used_marker = False
player_unlocked_chest = False
player_opened_chest = False
chest_combination = (chest_combination_1_object + 
                     chest_combination_2_object + 
                     chest_combination_3_object)
game_complete = False

# A 15x15 Grid representing the game object positions.
'''grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]'''

# Static maze used for testing.
grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Dictionary that holds object positions.
object_position_dictionary = {}

# List to hold the marked tile coordinates.
marked_tile_list = []

# List to hold the open tile coordinates.
open_coordinates_list = []

# List to hold the coordinates of tiles within the player field of view.
fov_tile_list = []
# List to hold the color of the tiles within the player field of view.
fov_tile_color_list = []

# Initialize the pygame console window.
pygame.init()

# Set the caption for the console window.
pygame.display.set_caption("Team-FooBar-Programming-Assignment-01")

# Create a surface to draw on.
screen = sgc.surface.Screen((600, 635))

# Create and place an input box on the console window.
input_box = sgc.InputBox((600, 35), label = "", 
                         default = "Input here, output console...")
input_box.config(pos = (0, 599))
input_box.add(order = 0)



################################################################################
# Main
################################################################################

# Main function.
def main():
    global player_object
    global chest_object
    global key_object
    global door_object
    global chest_combination_1_object
    global chest_combination_2_object
    global chest_combination_3_object

    # Randomly generate the maze using the Depth-first search algorithm.
    generate_maze_depth_first_search()

    # Draw colors to fill the cells of the grid.
    #screen.fill(cell_colors[1])

    # Create and define the door object.
    door_object = pygame.font.Font(None, object_size).render(
                                     door_object, False, door_object_color)

    # Create and define the chest object.
    chest_object = pygame.font.Font(None, object_size).render(
                                     chest_object, False, chest_object_color)

    # Create and define the key object.
    key_object = pygame.font.Font(None, object_size).render(
                                     key_object, False, key_object_color)

    # Create and define the player object.
    player_object = pygame.font.Font(None, object_size).render(
                                     player_object, False, player_object_color)

    # Create and define the chest_combination_1 object.
    chest_combination_1_object = pygame.font.Font(None, object_size).render(
                                     chest_combination_1_object, False, 
                                     chest_combination_1_object_color)
    
    # Create and define the chest_combination_2 object.
    chest_combination_2_object = pygame.font.Font(None, object_size).render(
                                     chest_combination_2_object, False, 
                                     chest_combination_2_object_color)
    
    # Create and define the chest_combination_3 object.
    chest_combination_3_object = pygame.font.Font(None, object_size).render(
                                     chest_combination_3_object, False, 
                                     chest_combination_3_object_color)

    # Place the objects on the grid.
    generate_random_object_positions()

    # Print out introductory message.
    print_introduction_message()

    # Call the function to handle player input.
    handle_input()



################################################################################
# Text Processing
################################################################################

# Function to print out an introduction message.
def print_introduction_message():
    print "\nIntroduction: "
    print "\nWelcome to Python-Text-Based-Maze-Game! (catchy name, huh?)"
    print "\nYour goal is to escape this maze. In order to do so, you must: "
    print "1) Grab the key (used to unlock the door)"
    print "2) Open the chest"
    print "3) Open the door"
    print "\nWhile you are attempting to escape, two enemies will be trying "
    print "to capture you. If they catch you, they will drag you back to "
    print "where you started and confiscate all of your items. "
    print "The following is a list of available commands. "
    print "\nCommand List: "
    print "1. go <forward, right, back, left> <number>"
    print "2. grab <key>"
    print "3. open <chest, door>"
    print "4. use <key, marker>"
    print "5. help"
    print "6. print <maze> (For development)"
    print "\nTo see this message again, enter the help command. Good luck!"

# Function to print out directions and a list of commands.
def help():
    print "Objectives: "
    print "1) Grab the key (used to unlock the door)"
    print "2) Open the chest"
    print "3) Open the door"
    print "\nCommand List: "
    print "1. go <forward, right, back, left> <number>"
    print "2. grab <key>"
    print "3. open <chest, door>"
    print "4. use <key, marker>"
    print "5. help"

# Function to get user input from the InputText.
def print_input(input):
    print "\nInput: " + input

# Function to print error message for invalid go.
def print_go_error():
    print "Output: Invalid move command..."

# Function to print error message for invalid input.
def print_input_error():
    print "Output: Invalid input. Command not recognized..." 

# Function to clear user input from the InputText.
def clear():
    input_box.text = ""



################################################################################
# Rendering
################################################################################

# Function that generates a random maze using the Depth-first search algorithm.
def generate_maze_depth_first_search():
    # Size of the maze.
    maze_width = len(grid) - 1
    maze_height = len(grid) - 1

    # 4 directions in the maze (down, right, up, left)
    destination_x = [0, 1, 0, -1]
    destination_y = [-1, 0, 1, 0]

    # Stack that stores coordinates in the maze. 
    # Starts at a random set of coordinates.
    coordinates_stack = [(random.randint(1, maze_width - 1), 
              random.randint(1, maze_height - 1))]

    # Loop until every set of coordinates have been visited.
    while len(coordinates_stack) > 0:
        # Set the current coordinates equal to the 
        # coordinates at the top of the stack.
        (current_x, current_y) = coordinates_stack[-1]
        
        # Destroy the wall at this coordinates.
        grid[current_x][current_y] = 1
        #grid[current_y][current_x] = 1

        # List that contains available neighbors.
        neighbors_list = []

        # Calculate how many neighbors that the current coordinates has.
        for i in range(4):
            # Set the new coordinates equal to the current coordinates
            # plus the adjacent coordinates in a random direction.
            new_x = current_x + destination_x[i]
            new_y = current_y + destination_y[i]

            # Continue if the new coordinates are in the range of the maze.
            if new_x > 0 and new_x < maze_width \
                and new_y > 0 and new_y < maze_height:
                # If the new coordinates is a wall, check for neighbors.
                if grid[new_x][new_y] == 0:
                    # Counter variable for the number of neighbors.
                    counter = 0
                    # Iterate through all 4 directions.
                    for j in range(4):
                        # Set the new coordinates.
                        temporary_x = new_x + destination_x[j]
                        temporary_y = new_y + destination_y[j]

                        # Continue if the new coordinates
                        # are in the range of the maze.
                        if temporary_x > 0 and temporary_x < maze_width \
                            and temporary_y > 0 and temporary_y < maze_height:
                            # Determine if there is a neighbor here.
                            if grid[temporary_x][temporary_y] == 1: 
                                # No neighbor exists at this coordinates.
                                counter += 1
                    # The new coordinates has only one
                    # neighbor (the old coordinates).
                    if counter == 1:
                        # Add the direction of the neighbor to the list.
                        neighbors_list.append(i)

        # 1 or more neighbors available, randomly select one and move.
        if len(neighbors_list) > 0:
            # Choose a random unvisited neighbor.
            random_neighbor = neighbors_list[random.randint(
                0, len(neighbors_list) - 1)]

            # Set the current coordinates equal to the destination coordinates.
            current_x += destination_x[random_neighbor]
            current_y += destination_y[random_neighbor]

            # Push the current coordinates to the stack.
            coordinates_stack.append((current_x, current_y))

        # 0 neighbors available, dead end. Pop the previous 
        # coordinates from the stack and attempt to continue.
        else: 
            # Pop the top coordinates off the stack.
            coordinates_stack.pop()

# Function to draw the maze.
def draw_maze(screen):
    # Color the walls of the grid.
    for x in range(len(grid)):
        for y in range(len(grid)):
            # Fill in the color of the grid walls.
            screen.fill(cell_colors[grid[y][x]], get_cell_rect((x, y), screen))

    # Change the color of the marked tiles if any exist.
    if player_used_marker == True:
        i = 0
        while i < len(marked_tile_list):
            # Fill in the marked tiles with the color red.
            screen.fill((255, 0, 0), get_cell_rect(marked_tile_list[i], screen))
            i = i + 1

    '''# Draw only the tiles that are in the field of view of the player character.
    i = len(fov_tile_list) - 1
    while i >= 0:
        fov_tile_list_string = str(fov_tile_list[i])

        fov_tile_list_substrings = fov_tile_list_string.split(", ")
        screen.fill((255, 255, 255), get_cell_rect(fov_tile_list[i], screen))
        i = i - 1'''

# Function to draw the container of the objects.
def get_cell_rect(coordinates, screen):
    # Set row, column equal to the passed parameters.
    row, column = coordinates
    # Set the width of the cell to the width of the 
    # screen divided by the length of the grid.
    cell_width = screen.get_width() / len(grid)
    # Calculate the adjusted width.
    adjusted_width = cell_width - cell_margin
    # Draw the rectangle that representing the game.
    return pygame.Rect(row * cell_width + cell_margin / 2,
                       column * cell_width + cell_margin / 2,
                       adjusted_width, adjusted_width)

# Function to store field of view tiles and colors.
def get_fov_tile_coordinates():
    global fov_tile_list

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Clear the contents of the fov_tile_list.
    fov_tile_list = []
    # Clear the contents of the fov_tile_color_list.
    fov_tile_color_list = []

    fov_tile_list.append((x - 2, y - 2))
    fov_tile_list.append((x - 1, y - 2))
    # Show the tile if it is not a wall and is in the range of the grid.
    if x > 0 and x < len(grid) and y - 2 > 0 and y - 2 < len(grid):
        if grid[x][y - 2] == 1:
            fov_tile_list.append((x, y - 2))
    fov_tile_list.append((x + 1, y - 2))
    fov_tile_list.append((x + 2, y - 2))
    fov_tile_list.append((x - 2, y - 1))
    fov_tile_list.append((x + 2, y - 1))
    # Show the tile if it is not a wall and is in the range of the grid.
    if x - 2 > 0 and x - 2 < len(grid) and y > 0 and y < len(grid):
        if grid[x - 2][y] == 1:
            fov_tile_list.append((x - 2, y))
    # Show the tile if it is not a wall and is in the range of the grid.
    if x + 2 > 0 and x + 2 < len(grid) and y > 0 and y < len(grid):
        if grid[x + 2][y] == 1:
            fov_tile_list.append((x + 2, y))
    fov_tile_list.append((x - 2, y + 1))
    fov_tile_list.append((x + 2, y + 1))
    fov_tile_list.append((x - 2, y + 2))
    fov_tile_list.append((x - 1, y + 2))
    # Show the tile if it is not a wall and is in the range of the grid.
    if x > 0 and x < len(grid) and y + 2 > 0 and y + 2 < len(grid):
        if grid[x][y + 2] == 1:
            fov_tile_list.append((x, y + 2))
    fov_tile_list.append((x + 1, y + 2))
    fov_tile_list.append((x + 2, y + 2))

# Function to draw the door object to the console window.
def draw_door_object(door_object, screen):
    # Return the size and offset of the door object.
    rect = door_object.get_rect()
    # Receive the center of the door object.
    rect.center = get_cell_rect(door_object_position, screen).center
    # Draw the door object image.
    screen.blit(door_object, rect)

# Function to draw the chest object to the console window.
def draw_chest_object(chest_object, screen):
    # Return the size and offset of the chest object.
    rect = chest_object.get_rect()
    # Receive the center of the chest object.
    rect.center = get_cell_rect(chest_object_position, screen).center
    # Draw the chest object image.
    screen.blit(chest_object, rect)

# Function to draw the key object to the console window.
def draw_key_object(key_object, screen):
    # Return the size and offset of the key object.
    rect = key_object.get_rect()
    # Receive the center of the key object.
    rect.center = get_cell_rect(key_object_position, screen).center
    # Draw the key object image.
    screen.blit(key_object, rect)
    
# Function to draw the player character object to the console window.
def draw_player_object(player_object, screen):
    # Return the size and offset of the player object.
    rect = player_object.get_rect()
    # Receive the center of the player object.
    rect.center = get_cell_rect(player_object_position, screen).center
    # Draw the player object image.
    screen.blit(player_object, rect)

# Function to draw the chest combination 1 object to the console window.
def draw_chest_combination_1_object(chest_combination_1_object, screen):
    # Return the size and offset of the chest_combination_1 object.
    rect = chest_combination_1_object.get_rect()
    # Receive the center of the chest_combination_1 object.
    rect.center = get_cell_rect(chest_combination_1_object_position, screen).center
    # Draw the chest_combination_1 object image.
    screen.blit(chest_combination_1_object, rect)

# Function to draw the chest combination 2 object to the console window.
def draw_chest_combination_2_object(chest_combination_2_object, screen):
    # Return the size and offset of the chest_combination_2 object.
    rect = chest_combination_2_object.get_rect()
    # Receive the center of the chest_combination_2 object.
    rect.center = get_cell_rect(chest_combination_2_object_position, screen).center
    # Draw the chest_combination_2 object image.
    screen.blit(chest_combination_2_object, rect)

# Function to draw the chest combination 3 object to the console window.
def draw_chest_combination_3_object(chest_combination_3_object, screen):
    # Return the size and offset of the chest_combination_3 object.
    rect = chest_combination_3_object.get_rect()
    # Receive the center of the chest_combination_3 object.
    rect.center = get_cell_rect(chest_combination_3_object_position, screen).center
    # Draw the chest_combination_3 object image.
    screen.blit(chest_combination_3_object, rect)


################################################################################
# Object Placement
################################################################################

# Function to generate a random position for the player character to start at.
def generate_random_object_positions():
    global player_object_position
    global chest_object_position
    global key_object_position
    global door_object_position
    global chest_combination_1_object_position
    global chest_combination_2_object_position
    global chest_combination_3_object_position

    # Variable representing the number of objects on the grid.
    number_of_objects = 0
    
    while number_of_objects != 1:
        # Generate a random x and y coordinate for the object position.
        randomx = random.randint(1, len(grid) - 1)
        randomy = random.randint(1, len(grid) - 1)

        if not position_is_occupied(randomx, randomy):
            # Set the player object position equal to the random x and y values.
            player_object_position[0] = randomx 
            player_object_position[1] = randomy

            # Add the player object position to the dictionary.
            object_position_dictionary['player'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1


    while number_of_objects != 2:
        # Generate a random x and y coordinate for the object position.
        randomx = random.randint(1, len(grid) - 1)
        randomy = random.randint(1, len(grid) - 1)

        if not position_is_occupied(randomx, randomy):
            # Set the chest object position equal to the random x and y values.
            chest_object_position[0] = randomx 
            chest_object_position[1] = randomy
            
            # Add the chest object position to the dictionary.
            object_position_dictionary['chest'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

    while number_of_objects != 3:
        # Generate a random x and y coordinate for the object position.
        randomx = random.randint(1, len(grid) - 1)
        randomy = random.randint(1, len(grid) - 1)

        if not position_is_occupied(randomx, randomy):
            # Set the key object position equal to the random x and y values.
            key_object_position[0] = randomx 
            key_object_position[1] = randomy

            # Add the key object position to the dictionary.
            object_position_dictionary['key'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

    while number_of_objects != 4:
        # Generate a random x and y coordinate for the object position.
        randomx = random.randint(1, len(grid) - 1)
        randomy = random.randint(1, len(grid) - 1)

        if not position_is_occupied(randomx, randomy):
            # Set the door object position equal to the random x and y values.
            door_object_position[0] = randomx 
            door_object_position[1] = randomy

            # Add the door object position to the dictionary.
            object_position_dictionary['door'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

    while number_of_objects != 5:
        # Generate a random x and y coordinate for the object position.
        randomx = random.randint(1, len(grid) - 1)
        randomy = random.randint(1, len(grid) - 1)

        if grid[randomx][randomy] == 0:
            # Set the chest_combination_1 object position 
            # equal to the random x and y values.
            chest_combination_1_object_position[0] = randomx 
            chest_combination_1_object_position[1] = randomy

            # Add the chest_combination_1 object position to the dictionary.
            object_position_dictionary['chest combination 1'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

    while number_of_objects != 6:
        # Generate a random x and y coordinate for the object position.
        randomx = random.randint(1, len(grid) - 1)
        randomy = random.randint(1, len(grid) - 1)

        if (grid[randomx][randomy] == 0 and grid[randomx][randomy] 
            != chest_combination_1_object_position):
            # Set the chest_combination_2 object position 
            # equal to the random x and y values.
            chest_combination_2_object_position[0] = randomx 
            chest_combination_2_object_position[1] = randomy

            # Add the chest_combination_2 object position to the dictionary.
            object_position_dictionary['chest combination 2'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

    while number_of_objects != 7:
        # Generate a random x and y coordinate for the object position.
        randomx = random.randint(1, len(grid) - 1)
        randomy = random.randint(1, len(grid) - 1)

        if (grid[randomx][randomy] == 0 and grid[randomx][randomy] 
            != chest_combination_1_object_position and grid[randomx][randomy] 
            != chest_combination_2_object_position):
            # Set the chest_combination_3 object position 
            # equal to the random x and y values.
            chest_combination_3_object_position[0] = randomx 
            chest_combination_3_object_position[1] = randomy

            # Add the chest_combination_3 object position to the dictionary.
            object_position_dictionary['chest combination 3'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

# Function to determine if the coordinate is blocked by an object or wall.
def position_is_occupied(x, y):
    # Return True for the wall object.
    if grid[x][y] == 0:
        return True
    # Return True for the player object.
    elif x == player_object_position[0] and y == player_object_position[1]:
        return True
    # Return True for the chest object.
    elif x == chest_object_position[0] and y == chest_object_position[1]:
        return True
    # Return True for the key object.
    elif x == key_object_position[0] and y == key_object_position[1]:
        return True
    # Return True for the door object.
    elif x == door_object_position[0] and y == door_object_position[1]:
        return True
 
    return False



################################################################################
# Player Input
################################################################################
  
# Function to handle player character movement.
def handle_input():
    while game_complete == False:
        for event in pygame.event.get():
            sgc.event(event)
            if event.type == GUI:
                # Print user input string to the output console window. 
                input_string = event.text.lower()
                print_input(input_string)
                # Print the objects and list of commands for the help command.
                if input_string == "help":
                    help()
                # Possible user input for the go <Direction> command.
                elif input_string == "go forward":
                    go(0, -1)
                elif input_string == "go right":
                    go(1, 0)
                elif input_string == "go back":
                    go(0, 1)
                elif input_string == "go left":
                    go(-1, 0)
                elif input_string == "go chest":
                    print "Output: A chest is for opening, not going." \
                          "\nTry going in a direction instead."
                elif input_string == "go key":
                elif input_string == "go door":
                elif input_string == "go wall":
                elif input_string == "go marker":
                # Possible user input for the grab <Object> command.
                elif input_string == "grab forward":
                elif input_string == "grab right":
                elif input_string == "grab back":
                elif input_string == "grab left":
                elif input_string == "grab chest":
                elif input_string == "grab key":
                    if player_grabbed_key:
                        # Inform the player that they already have the key.
                    else:
                        grab_key()
                elif input_string == "grab door":
                elif input_string == "grab wall":
                elif input_string == "grab marker":
                # Possible user input for the open <Object> command.
                elif input_string == "open forward":
                elif input_string == "open right":
                elif input_string == "open back":
                elif input_string == "open left":
                elif input_string == "open chest":
                    open_chest()
                elif input_string == "open key":
                elif input_string == "open door":
                    open_door()
                elif input_string == "open wall":
                elif input_string == "open marker":
                # Possible user input for the use <Object> command.
                elif input_string == "use forward":
                elif input_string == "use right":
                elif input_string == "use back":
                elif input_string == "use left":
                elif input_string == "use chest":
                elif input_string == "use key":
                    use_key()
                elif input_string == "use door":
                elif input_string == "use wall":
                elif input_string == "use marker":
                    use_marker()
                else:
                    # Parse the string into substrings and store into a list.
                    input_substring_list = input_string.split(" ")

                    # Check if the first substring is equal to "go".
                    if input_substring_list[0] == "go":
                        # Check if the second substring is equal to "forward".
                        if input_substring_list[1] == "forward":
                            # If the third substring is a digit, call the go() 
                            # command the number of times the digit specifies.
                            if input_substring_list[2].isdigit(): 
                                i = 0
                                while i < int(input_substring_list[2]):
                                    go(0, -1)
                                    i = i + 1
                            # Incorrect third substring.
                            else:
                                print_input_error()
                        # Check if the second substring is equal to "right".
                        elif input_substring_list[1] == "right":
                            # If the third substring is a digit, call the go() 
                            # command the number of times the digit specifies.
                            if input_substring_list[2].isdigit(): 
                                i = 0
                                while i < int(input_substring_list[2]):
                                    go(1, 0)
                                    i = i + 1
                            # Incorrect third substring.
                            else:
                                print_input_error()
                        # Check if the second substring is equal to "back".
                        elif input_substring_list[1] == "back":
                            # If the third substring is a digit, call the go() 
                            # command the number of times the digit specifies.
                            if input_substring_list[2].isdigit(): 
                                i = 0
                                while i < int(input_substring_list[2]):
                                    go(0, 1)
                                    i = i + 1
                            # Incorrect third substring.
                            else:
                                print_input_error()
                        # Check if the second substring is equal to "left".
                        elif input_substring_list[1] == "left":
                            # If the third substring is a digit, call the go() 
                            # command the number of times the digit specifies.
                            if input_substring_list[2].isdigit(): 
                                i = 0
                                while i < int(input_substring_list[2]):
                                    go(-1, 0)
                                    i = i + 1
                            # Incorrect third substring.
                            else:
                                print_input_error()
                        # Incorrect second substring.
                        else:
                            print_input_error()
                    elif input_substring_list[0] == "use":
                        if input_substring_list[1].isdigit():
                            unlock_chest(input_substring_list[1])
                        else:
                            print_input_error()
                    # Not even close to a valid command or contains some 
                    # form of misspelling or incorrect input 
                    # (numbers, special characters, etc.).
                    else:
                        print_input_error()

                # Clear the contents of the InputBox if it is clicked on.
                if event.widget is input_box:
                    clear()

            # Possible user input using the arrow keys.
            if event.type == KEYDOWN:
                # Store the key press event.
                key = event.key
                # Move the player character object up if the up arrow key was 
                # pressed and if there are no objects blocking the path.
                if key == K_UP:
                    go(0, -1)
                # Move the player character object right if the right arrow key 
                # was pressed and if there are no objects blocking the path.
                elif key == K_RIGHT:
                    go(1, 0)
                # Move the player character object down if the down arrow key 
                # was pressed and if there are no objects blocking the path.
                elif key == K_DOWN:
                    go(0, 1)
                # Move the player character object left if the left arrow key 
                # was pressed and if there are no objects blocking the path.
                elif key == K_LEFT:
                    go(-1, 0)
            # Quit the game if the user closes the window.
            elif event.type == QUIT:
                return

        # Call the function to retrieve tiles in the 
        # field of view and store them into a list.
        get_fov_tile_coordinates()
        # Call the function to draw the maze.
        draw_maze(screen)
        # Call the function to draw the door object.
        draw_door_object(door_object, screen)
        # Call the function to draw the chest object.
        draw_chest_object(chest_object, screen)
        if not player_grabbed_key:
            # Call the function to draw the key object.
            draw_key_object(key_object, screen)
        # Call the function to draw the player character object.
        draw_player_object(player_object, screen)
        # Call the function to draw the chest_combination_1 object.
        draw_chest_combination_1_object(chest_combination_1_object, screen)
        # Call the function to draw the chest_combination_2 object.
        draw_chest_combination_2_object(chest_combination_2_object, screen)
        # Call the function to draw the chest_combination_3 object.
        draw_chest_combination_3_object(chest_combination_3_object, screen)
        # Update the InputText widget.
        sgc.update(1)
        # Update the console window to show changes.
        pygame.display.update()



################################################################################
# Character Actions
################################################################################

# Function to move the player character object through the maze.
def go(dx, dy):
    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Set nx and ny equal to the new player character object position.
    nx = x + dx
    ny = y + dy

    # Change the player character object position if the new position 
    # is in the game window and the cell is not pre-occupied.
    if (nx > 0 and nx < len(grid) and ny > 0 and ny < len(grid) and \
        grid[ny][nx]):
            # Check if the chest object is placed on the destination tile.
            if (nx == chest_object_position[0] 
                and ny == chest_object_position[1]):
                # Print out an error for the invalid move.
                print_go_error()
            # Check if the key object is placed on the destination tile.
            elif (nx == key_object_position[0] 
                  and ny == key_object_position[1]):
                # Print out an error for the invalid move.
                print_go_error()
            # Check if the door object is placed on the destination tile.
            elif (nx == door_object_position[0] 
                  and ny == door_object_position[1]):
                # Print out an error for the invalid move.
                print_go_error()
            # No objects placed on the destination tile.
            else:
                player_object_position[0] = nx
                player_object_position[1] = ny
    else:
        # Print out an error for the invalid move.
        print_go_error()

# Function to use the marker.
def use_marker():
    global marked_tile_list
    global player_used_marker

    # Change the value of player_used_marker to True. It is used in the 
    # draw_maze function to determine when to start drawing the marker.
    player_used_marker = True

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Clear the contents of the marked_tile_list.
    marked_tile_list = []

    # Add the tile coordinates to the marked_tile_list.
    if grid[x][y] == 1:
        marked_tile_list.append((x, y))
    if grid[x - 1][y - 1] == 1:
        marked_tile_list.append((x - 1, y - 1))
    if grid[x][y - 1] == 1:
        marked_tile_list.append((x, y - 1))
    if grid[x + 1][y - 1] == 1:
        marked_tile_list.append((x + 1, y - 1))
    if grid[x - 1][y] == 1:
        marked_tile_list.append((x - 1, y))
    if grid[x + 1][y] == 1:
        marked_tile_list.append((x + 1, y))
    if grid[x - 1][y + 1] == 1:
        marked_tile_list.append((x - 1, y + 1))
    if grid[x][y + 1] == 1:
        marked_tile_list.append((x, y + 1))
    if grid[x + 1][y + 1] == 1:
        marked_tile_list.append((x + 1, y + 1))

# Function to grab the key.
def grab_key():
    # Needed to change their properties.
    global key_object_position
    global player_grabbed_key
    global key_object_color

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Set x and y equal to the current key object position.
    a = key_object_position[0]
    b = key_object_position[1]

    if player_next_to_object(x, y, a, b):
        # Inform the player that they have picked up the key.
        print "Output: You have picked up the key!"
        # Set the key object position to [0, 0].
        key_object_position[0] = 0
        key_object_position[1] = 0
        # Set player_grabbed_key equal to True.
        player_grabbed_key = True
    else:
        # Inform the player that the key is not within their reach.
        print "Output: The key is not within reach..."

# Function to unlock the chest.
def unlock_chest(user_input_combination):    
    # Needed to change their properties.
    global player_unlocked_chest

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Set x and y equal to the current chest object position.
    a = chest_object_position[0]
    b = chest_object_position[1]

    if player_next_to_object(x, y, a, b):
        if player_unlocked_chest:
            # Inform the player that they have 
            # already unlocked the chest.
            print "Output: You have already unlocked the chest."
        else:
            if user_input_combination == chest_combination:
                # Inform the player that they have unlocked up the chest.
                print "Output: You have unlocked the chest!"
                # Set player_unlocked_chest equal to True.
                player_unlocked_chest = True
            else:
                # Inform the player that the combination is incorrect.
                print "Output: incorrect combination..."
    else:
        # Inform the player that the chest is not within their reach.
        print "Output: The chest is not within reach..."

# Function to open the chest.
def open_chest():
    # Needed to change their properties.
    global chest_object
    global chest_object_position
    global player_opened_chest

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Set x and y equal to the current chest object position.
    a = chest_object_position[0]
    b = chest_object_position[1]

    if player_next_to_object(x, y, a, b):
        if player_opened_chest:
            # Inform the player that they have 
            # already opened the chest.
            print "Output: You have already opened the chest."
        else:
            if player_unlocked_chest:
                # Inform the player that they have opened up the chest.
                print "Output: You have opened the chest!"
                # Set the chest object character to 'O'.
                chest_object = pygame.font.Font(None, object_size).render(
                                                chest_object_opened, False, 
                                                chest_object_color)
                # Set player_grabbed_chest equal to True.
                player_opened_chest = True
            else:
                # Inform the player that the combination is incorrect.
                print "Output: You must enter the correct combination to "
                print "unlock the chest before you can open it."
    else:
        # Inform the player that the chest is not within their reach.
        print "Output: The chest is not within reach..."

# Function to use the key.
def use_key():
    # Needed to change their properties.
    global door_object_position
    global player_used_key

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Set x and y equal to the current door object position.
    a = door_object_position[0]
    b = door_object_position[1]

    if player_next_to_object(x, y, a, b):
        if player_used_key:
            # Inform the player that they have already 
            # used the key to unlock the door.
            print "You have already unlocked the door."
        elif player_grabbed_key:
            # Inform the player that they have unlocked the door.
            print "Output: You have unlocked the door!"
            # Set player_used_key equal to True.
            player_used_key = True
        else:
            # Inform the player that they need the key to unlocked the door.
            print ("Output: You must grab the " 
                    "key before you can use it.")
    else:
        # Inform the player that the door is not within their reach.
        print "Output: The door is not within reach..."

# Function to open the door.
def open_door():
    # Needed to change their properties.
    global door_object
    global door_object_position
    global player_opened_chest
    global game_complete

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Set x and y equal to the current door object position.
    a = door_object_position[0]
    b = door_object_position[1]

    if player_next_to_object(x, y, a, b):
        if player_used_key and player_opened_chest:
            # Inform the player that they have opened the door.
            print "Output: You have opened the door!"
            # Congratulate the player on completing the game.
            print "\n\nCongratulations! You have escaped!\n\n"
            # Set game_complete equal to True.
            game_complete = True
        elif player_used_key and not player_opened_chest:
            # Inform the player that they need to open the 
            # chest before they can open the door.
            print ("Output: You must open the chest "
                    "before you can open the door.")
        elif player_grabbed_key and player_opened_chest:
            # Inform the player that they need to use the 
            # key before they can open the door.
            print ("Output: You must use the key "
                    "before you can open the door.")
        elif player_grabbed_key and not player_opened_chest:
            # Inform the player that they need to use the 
            # key before they can open the door.
            print ("Output: You must use the key and open the "
                    "chest before you can open the door.")
        elif not player_grabbed_key and player_opened_chest:
            # Inform the player that they need to use the 
            # key before they can open the door.
            print ("Output: You must grab and use the key "
                    "before you can open the door.")
        else:
            # Inform the player that they need to find 
            # the key before they can open the door.
            print ("Output: You must grab and use the key and open " 
                    "the chest before you can open the door.")
    else:
        # Inform the player that the door is not within their reach.
        print "Output: The door is not within reach..."

# Function that returns true if the player character 
# object is located next to another object.
def player_next_to_object(x, y, a, b):
    # Check the location that the player character object currently is.
    if x == a and y == b:
        return True
    # Check the location above and to the left of the player character object.
    elif x - 1 == a and y - 1 == b:
        return True
    # Check the location directly above the player character object.
    elif x == a and y - 1 == b:
        return True
    # Check the location above and to the right of the player character object.
    elif x + 1 == a and y - 1 == b:
        return True
    # Check the location to the left of the player character object.
    elif x - 1 == a and y == b:
        return True
    # Check the location to the right of the player character object.
    elif x + 1 == a and y == b:
        return True
    # Check the location below and to the left of the player character object.
    elif x - 1 == a and y + 1 == b:
        return True
    # Check the location directly below the player character object.
    elif x == a and y + 1 == b:
        return True
    # Check the location below and to the right of the player character object.
    elif x + 1 == a and y + 1 == b:
        return True
    
    # Return False if the player is not located directly next to an object.
    return False



# Executes the main function.
if __name__ == "__main__":
    # Call function main.
    main()
    # Exit the console window.
    pygame.quit()