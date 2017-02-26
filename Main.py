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
player_object_color = (255, 0, 0) # Color of the player character.
player_object_position = [0, 0] # Position of the player character.
chest_object = "C" # Symbol representing the chest.
chest_object_opened = "O" # Symbol representing the opened chest.
chest_object_color = (255, 0, 0) # Color of the chest.
chest_object_position = [0, 0] # Position of the chest.
key_object = "K" # Symbol representing the key.
key_object_removed = "" # Symbol used to remove the key.
key_object_color = (255, 0, 0) # Color of the key.
key_object_position = [0, 0] # Position of the key.
door_object = "D" # Symbol representing the door.
door_object_color = (255, 0, 0) # Color of the door.
door_object_position = [0, 0] # Position of the door.
object_size = 35 # Size of all objects drawn to the console window.
player_used_marker = False
player_grabbed_key = False
player_used_key = False
player_opened_chest = False
game_complete = False

# Grid representing the game object positions.
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
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Initialize the pygame console window.
pygame.init()

# Set the caption for the console window.
pygame.display.set_caption("Team-FooBar-Programming-Assignment-01")

# Create a surface to draw on.
screen = sgc.surface.Screen((600, 600))

# Create and place an input box on the console window.
input_box = sgc.InputBox((600, 30), label = "", 
                         default = "Input here, output console...")
input_box.config(pos = (0,562))
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

    # Draw colors to fill the cells of the grid.
    screen.fill(cell_colors[1])

    # Create and define the door object.
    door_object = pygame.font.Font(None, object_size).render(
                                     door_object, False, door_object_color)

    # Create and define the chest object.
    chest_object = pygame.font.Font(None, object_size).render(
                                     chest_object, False, chest_object_color)

    # Create and define the key object.
    key_object = pygame.font.Font(None, object_size).render(
                                     key_object, False, key_object_color)

    # Create and define the player character object.
    player_object = pygame.font.Font(None, object_size).render(
                                     player_object, False, player_object_color)

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
    print ("\nIntroduction: Grab the key, open the chest, "
            "then find your way out...\n")

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

# Function to draw the maze.
def draw_maze(screen):
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            screen.fill(cell_colors[grid[column][row]],
                        get_cell_rect((row, column), screen))

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



################################################################################
# Object Placement
################################################################################

# Function to generate a random position for the player character to start at.
def generate_random_object_positions():
    global player_object_position
    global chest_object_position
    global key_object_position

    # Variable representing the number of objects on the grid.
    number_of_objects = 0
    
    while number_of_objects != 1:
        # Generate a random x value.
        randomx = random.randint(1, 15)
        # Generate a random y value.
        randomy = random.randint(1, 14)

        if not is_object_blocked(randomx, randomy):
            # Set the player object position equal to the random x and y values.
            player_object_position[0] = randomx 
            player_object_position[1] = randomy
            number_of_objects += 1


    while number_of_objects != 2:
        # Generate a random x value.
        randomx = random.randint(1, 15)
        # Generate a random y value.
        randomy = random.randint(1, 14)

        if not is_object_blocked(randomx, randomy):
            # Set the chest object position equal to the random x and y values.
            chest_object_position[0] = randomx 
            chest_object_position[1] = randomy
            number_of_objects += 1

    while number_of_objects != 3:
        # Generate a random x value.
        randomx = random.randint(1, 15)
        # Generate a random y value.
        randomy = random.randint(1, 14)

        if not is_object_blocked(randomx, randomy):
            # Set the key object position equal to the random x and y values.
            key_object_position[0] = randomx 
            key_object_position[1] = randomy
            number_of_objects += 1

    while number_of_objects != 4:
        # Generate a random x value.
        randomx = random.randint(1, 15)
        # Generate a random y value.
        randomy = random.randint(1, 14)

        if not is_object_blocked(randomx, randomy):
            # Set the door object position equal to the random x and y values.
            door_object_position[0] = randomx 
            door_object_position[1] = randomy
            number_of_objects += 1

# Function to determine if the coordinate is blocked by an object or wall.
def is_object_blocked(x, y):
    # Return True for the map tile.
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
                # Possible user input for the go <Direction> command.
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
                # Possible user input for the grab <Object> command.
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
                        # Inform the player that they already have the key.
                        print "Output: You already have the key."
                    else:
                        grab_key()
                elif input_string == "grab door":
                    print "Output: "
                elif input_string == "grab wall":
                    print "Output: "
                elif input_string == "grab marker":
                    print "Output: "
                # Possible user input for the open <Object> command.
                elif input_string == "open forward":
                    print "Output: "
                elif input_string == "open right":
                    print "Output: "
                elif input_string == "open back":
                    print "Output: "
                elif input_string == "open left":
                    print "Output: "
                elif input_string == "open chest":
                    open_chest()
                elif input_string == "open key":
                    print "Output: "
                elif input_string == "open door":
                    open_door()
                elif input_string == "open wall":
                    print "Output: "
                elif input_string == "open marker":
                    print "Output: "
                # Possible user input for the use <Object> command.
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
                    use_key()
                elif input_string == "use door":
                    print "Output: "
                elif input_string == "use wall":
                    print "Output: "
                elif input_string == "use marker":
                    use_marker()
                # Not even close to a valid command or contains some form of 
                # misspelling or incorrect input (numbers, special characters, etc.).
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

        # Call the function to draw the maze.
        draw_maze(screen)
        # Call the function to draw the door object.
        draw_door_object(door_object, screen)
        # Call the function to draw the chest object.
        draw_chest_object(chest_object, screen)
        # Call the function to draw the key object.
        draw_key_object(key_object, screen)
        # Call the function to draw the player character object.
        draw_player_object(player_object, screen)
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
    if (nx >= 0 and nx < len(grid) and ny >= 0 and ny < len(grid[0]) and \
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
    global player_used_marker
    global cell_colors

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    if player_used_marker:
        # Reset the RBG values representing object colors.
        cell_colors = (255, 255, 255), (0, 0, 0)
        player_used_marker = False
    else:
        cell_colors = (255, 0, 0), (255, 0, 0)
        player_used_marker = True

    '''grid[x - 1][y - 1] = (255, 0 , 0)
    grid[x ][y - 1] = (255, 0 , 0)
    grid[x + 1][y - 1] = (255, 0 , 0)
    grid[x - 1][y] = (255, 0 , 0)
    grid[x + 1][y] = (255, 0 , 0)
    grid[x - 1][y + 1] = (255, 0 , 0)
    grid[x][y + 1] = (255, 0 , 0)
    grid[x + 1][y + 1] = (255, 0 , 0)'''

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
        # Set the character of the key to "".
        key_object = pygame.font.Font(None, object_size).render(
                                        key_object_removed, False, 
                                        key_object_color)
        # Set player_grabbed_key equal to True.
        player_grabbed_key = True
    else:
        # Inform the player that the key is not within their reach.
        print "Output: The key is not within reach..."

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
            # Inform the player that they have picked up the chest.
            print "Output: You have opened the chest!"
            # Set the chest object character to 'O'.
            chest_object = pygame.font.Font(None, object_size).render(
                                            chest_object_opened, False, 
                                            chest_object_color)
            # Set player_grabbed_chest equal to True.
            player_opened_chest = True
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
        # Inform the player that the chest is not within their reach.
        print "Output: The door is not within reach..."

# Function that returns true if the player character 
# object is located next to another object.
def player_next_to_object(x, y, a, b):
    # Check the location above and to the left of the player character object.
    if x - 1 == a and y - 1 == b:
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
