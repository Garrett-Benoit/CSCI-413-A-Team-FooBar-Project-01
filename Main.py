################################################################################
# Header
################################################################################
# Date Started:     2 (February) / 11 (Saturday) / 2017 (Fall)
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

import os
import sys
import pygame
from pygame.locals import *
import sgc
from sgc.locals import *
import random
import time
import heapq
import ast



################################################################################
# Initialization
################################################################################

# Create a string equal to the current time for the log file.
log_filename = time.strftime("Log_%m-%d-%y_%H-%M-%S.txt")
# Declare a log file variable for global use.
log_file = None
# Declare a replay file variable for global use.
replay_file = None
# Declare a chosen replay filename variable for global use.
chosen_replay_filename = None
# Declare a chosen replay file variable for global use.
chosen_replay_file = None

cell_margin = 5 # Pre-defined space between cells.
cell_colors = (255, 255, 255), (0, 0, 0) # RBG values representing cell colors.
player_object = "@" # Symbol representing the player character.
player_object_color = (255, 255, 255) # Color of the player character.
player_object_position = [0, 0] # Position of the player character.
chest_object_closed = "C" # Symbol representing the closed chest.
chest_object_opened = "O" # Symbol representing the opened chest.
chest_object_color = (255, 255, 255) # Color of the chest.
chest_object_position = [0, 0] # Position of the chest.
key_object = "K" # Symbol representing the key.
key_object_color = (255, 255, 255) # Color of the key.
key_object_position = [0, 0] # Position of the key.
door_object = "D" # Symbol representing the door.
door_object_color = (255, 255, 255) # Color of the door.
door_object_position = [0, 0] # Position of the door.
simple_enemy_object = "E" # Symbol representing the simple enemy.
simple_enemy_object_color = (255, 0, 0) # Color of the simple enemy.
simple_enemy_object_position = [0, 0] # Position of the simple enemy.
smart_enemy_object = "S" # Symbol representing the smart enemy.
smart_enemy_object_color = (255, 0, 0) # Color of the smart enemy.
smart_enemy_object_position = [0, 0] # Position of the smart enemy.
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
maze_is_valid = False
player_made_decision = False
show_replay_1 = False
show_replay_2 = False
show_replay_3 = False
start_new_game = False
game_complete = False
exit_game = False

# A 15x15 Grid representing the game object positions.
grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Dictionary that holds object positions.
object_position_dictionary = {}

# List to hold the marked tile coordinates.
marked_tile_list = []

# List to hold the coordinates of tiles within the player field of view.
visible_object_list = []

# Initialize the pygame console window.
pygame.init()

# Set the caption for the console window.
pygame.display.set_caption("")

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
    global chest_object_closed
    global chest_object_opened
    global key_object
    global door_object
    global simple_enemy_object
    global smart_enemy_object
    global chest_combination_1_object
    global chest_combination_2_object
    global chest_combination_3_object
    global maze_is_valid
    global exit_game
    global player_made_decision
    global show_replay_1
    global show_replay_2
    global show_replay_3
    global start_new_game

    # Create and define the door object.
    door_object = pygame.font.Font(None, object_size).render(
                                     door_object, False, door_object_color)
                
    # Create and define the closed chest object.
    chest_object_closed = pygame.font.Font(None, object_size).render(
                                        chest_object_closed, False, 
                                        chest_object_color)
       
    # Create and define the opened chest object.
    chest_object_opened = pygame.font.Font(None, object_size).render(
                                    chest_object_opened, False, 
                                    chest_object_color)

    # Create and define the key object.
    key_object = pygame.font.Font(None, object_size).render(
                                     key_object, False, key_object_color)

    # Create and define the player object.
    player_object = pygame.font.Font(None, object_size).render(
                                     player_object, False, player_object_color)

    # Create and define the simple enemy object.
    simple_enemy_object = pygame.font.Font(None, object_size).render(
                                     simple_enemy_object, False, 
                                     simple_enemy_object_color)

    # Create and define the smart enemy object.
    smart_enemy_object = pygame.font.Font(None, object_size).render(
                                     smart_enemy_object, False, 
                                     smart_enemy_object_color)

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
    
    # Loop that determines manages the game states.
    while not exit_game:
        # Call the function to handle the player choices at the title screen.
        show_title_screen()

        # Reset the maze before continuing.
        reset_maze()
        # Clear the contents of the screen.
        screen.fill((0, 0, 0))
        # Update the console window to show changes.
        pygame.display.update()
        
        # Open replay 1, the oldest replay.
        if show_replay_1 == True:
            open_replay(1)
        # Open replay 2, the middle-aged replay.
        elif show_replay_2 == True:
            open_replay(2)
        # Open replay 3, the youngest replay.
        elif show_replay_3 == True:
            open_replay(3)
        # Start a new game.
        elif start_new_game == True:
            open_new_game()

        # Reset the state of player 
        # decisions and game conditions.
        player_grabbed_key = False
        player_used_key = False
        player_used_marker = False
        player_unlocked_chest = False
        player_opened_chest = False
        maze_is_valid = False
        player_made_decision = False
        show_replay_1 = False
        show_replay_2 = False
        show_replay_3 = False
        start_new_game = False
        game_complete = False



################################################################################
# Game States
################################################################################

# Function to handle player choices on the title screen.
def show_title_screen():
    global grid
    global player_made_decision
    global start_new_game
    global show_replay_1
    global show_replay_2
    global show_replay_3
    global exit_game

    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    # Set the caption for the console window.
    pygame.display.set_caption("Title Screen")

    # Print introduction message to the user.
    print "\nTitle Screen: "
    print "\nPlease choose one of the following options:"  
    print "1. open new game"
    print "2. open replay <1, 2, 3>"
    print "3. exit"

    # Continue running until the player chooses
    # a valid option or closes the window.
    while player_made_decision == False:
        # Iterate through all of the events gathered from pygame.
        for event in pygame.event.get():
            sgc.event(event)
            if event.type == GUI:
                # Print user input string to the output console window. 
                input_string = event.text.lower()
                print_input(input_string)

                # Print error message if user input is empty.
                if input_string == "":
                    print "Output: Please enter a command."
                # Get a decision from the user.
                elif input_string == "open new game":
                    start_new_game = True
                    player_made_decision = True
                elif input_string == "open replay 1":
                    # Number of replay files.
                    number_of_replay_files = 0

                    # Get filenames and store into a temporary list.
                    temp_filenames_list = []
                    temp_filenames_list = os.listdir(os.getcwd())

                    # Count the number of replay files in the temporary list.
                    for temp_filename in temp_filenames_list:
                        if temp_filename[:7] == "Replay_":
                            number_of_replay_files = number_of_replay_files + 1

                    # If the replay file exists...
                    if number_of_replay_files > 0:
                        show_replay_1 = True
                        player_made_decision = True
                    # If the replay file does not exist...
                    else:
                        print "Output: Chosen replay file does not exist." \
                                "\nHow about starting a new game?"
                elif input_string == "open replay 2":
                    # Number of replay files.
                    number_of_replay_files = 0

                    # Get filenames and store into a temporary list.
                    temp_filenames_list = []
                    temp_filenames_list = os.listdir(os.getcwd())

                    # Count the number of replay files in the temporary list.
                    for temp_filename in temp_filenames_list:
                        if temp_filename[:7] == "Replay_":
                            number_of_replay_files = number_of_replay_files + 1

                    # If the replay file exists...
                    if number_of_replay_files > 1:
                        show_replay_2 = True
                        player_made_decision = True
                    # If the replay file does not exist...
                    else:
                        print "Output: Chosen replay file does not exist." \
                                "\nHow about starting a new game?"
                elif input_string == "open replay 3":
                    # Number of replay files.
                    number_of_replay_files = 0

                    # Get filenames and store into a temporary list.
                    temp_filenames_list = []
                    temp_filenames_list = os.listdir(os.getcwd())

                    # Count the number of replay files in the temporary list.
                    for temp_filename in temp_filenames_list:
                        if temp_filename[:7] == "Replay_":
                            number_of_replay_files = number_of_replay_files + 1

                    # If the replay file exists...
                    if number_of_replay_files > 2:
                        show_replay_3 = True
                        player_made_decision = True
                    # If the replay file does not exist...
                    else:
                        print "Output: Chosen replay file does not exist." \
                                "\nHow about starting a new game?"
                elif input_string == "exit":
                    exit_game = True
                    player_made_decision = True
                else:
                    # Not even close to a valid command or contains some 
                    # form of misspelling or incorrect input 
                    # (numbers, special characters, etc.).
                    print "Please enter a valid command."

                # Clear the contents of the InputBox if it is clicked on.
                if event.widget is input_box:
                    clear()

        # Clear the contents of the screen.
        screen.fill((0, 0, 0))
        # Call the function to draw the maze and the objects inside.
        draw_screen(screen)
        # Set the title of the game and the names of team members on the screen.
        default_font_1 = pygame.font.SysFont("None", 45)
        default_font_2 = pygame.font.SysFont("None", 25)
        label_1 = default_font_1.render("Python-Text-Based-Maze-Game", 
                                    1, (255, 255, 255))
        label_2 = default_font_2.render("Taylor Venissat, Phuong Ho, Chance Johnson,", 
                                    1, (255, 255, 255))
        label_3 = default_font_2.render("Garrett Benoit, and Zackary Hermsen", 
                                    1, (255, 255, 255))
        # Draw the labels onto the screen.
        screen.blit(label_1, (70, 120))
        screen.blit(label_2, (110, 175))
        screen.blit(label_3, (140, 200))
        # Update the InputText widget.
        sgc.update(1)
        # Update the console window to show changes.
        pygame.display.update()

# Function to start a new game.
def open_new_game():
    global maze_is_valid

    # Set the caption for the console window.
    pygame.display.set_caption("New Game")

    # Variable used to keep track of the number of attempts.
    current_number_of_attempts = 0
    # Variable used to keep track of the number of switches.
    number_of_switches = 0
    # Variable used to keep track of the number iterations.
    total_number_of_attempts = 0
    # Keep generating a random maze until it is valid.
    while not maze_is_valid:
        # Generate the maze randomly using the Recursive
        # Backtracker algorithm. If it fails four times,
        # switch and use the Binary Tree algorithm.
        if current_number_of_attempts < 4:
            # Reset the maze.
            reset_maze()

            # Generate the maze using the 
            # Recursive Backtracker algorithm.
            generate_maze_recursive_backtracker()

            # Code to break the maze generation 
            # and test the number of switches.
            '''for x in range(len(grid)):
                for y in range(len(grid)):
                    if current_number_of_attempts < 4:
                        grid[7][x] = 0
                        grid[y][7] = 0'''

            # Place the player, door, chest, and
            # key objects randomly on the grid.
            generate_random_object_positions()

            # Test the validity of the maze.
            if check_maze_for_validity_player_door() == 0:
                if check_maze_for_validity_player_key() == 0:
                    if check_maze_for_validity_player_chest() == 0:
                        # Place the chest combination objects along the 
                        # optimal path and the enemies near the door.
                        generate_optimal_object_positions()

                        # Print to log file that the maze successfully
                        # generated along with the number of times it 
                        # took and the maze generation algorithm used.
                        write_to_log_file(str(time.strftime("%H-%M-%S")) \
                                            + ": Maze successfully generated " \
                                            + "using the " \
                                            + "Recursive Backtracker\n " \
                                            + "\t\t\talgorithm after " \
                                            + "switching " \
                                            + str(number_of_switches) \
                                            + " time(s) and " \
                                            + str(total_number_of_attempts + 1) \
                                            + " attempt(s)") 

                        # Set the boolean to True and exit 
                        # the loop. The maze is valid.
                        maze_is_valid = True
        # Generate the maze randomly using the Binary Tree algorithm.
        # If it fails four times, switch and use the Recursive Backtracker 
        # algorithm.
        elif current_number_of_attempts < 8:
            # Reset the maze.
            reset_maze()

            # Generate the maze using the Binary Tree algorithm.
            generate_maze_binary_tree()

            # Code to break the maze generation 
            # and test the number of switches.
            '''for x in range(len(grid)):
                for y in range(len(grid)):
                    if current_number_of_attempts < 8:
                        grid[7][x] = 0
                        grid[y][7] = 0'''

            # Place the player, door, chest, and
            # key objects randomly on the grid.
            generate_random_object_positions()

            # Test the validity of the maze.
            if check_maze_for_validity_player_door() == 0:
                if check_maze_for_validity_player_key() == 0:
                    if check_maze_for_validity_player_chest() == 0:
                        # Place the chest combination objects along the 
                        # optimal path and the enemies near the door.
                        generate_optimal_object_positions()

                        # Print to log file that the maze successfully 
                        # generated along with the number of times it 
                        # took and the maze generation algorithm used.
                        write_to_log_file(str(time.strftime("%H-%M-%S")) \
                                            + ": Maze successfully generated " \
                                            + "using the " \
                                            + "Binary Tree\n " \
                                            + "\t\t\talgorithm after " \
                                            + "switching " \
                                            + str(number_of_switches) \
                                            + " time(s) and " \
                                            + str(total_number_of_attempts + 1) \
                                            + " attempt(s)") 

                        # Set the boolean to True and exit 
                        # the loop. The maze is valid.
                        maze_is_valid = True
        # Increment current_number_of_attempts every attempt.
        current_number_of_attempts = current_number_of_attempts + 1
        # Increment total_number_of_attempts every attempt.
        total_number_of_attempts = total_number_of_attempts + 1

        if current_number_of_attempts >= 8:
            # If the maze cannot be generated within 8 tries, set
            # current_number_of_attempts equal to 0 and start again.
            current_number_of_attempts = 0

        # Increment number_of_switches every 4 attempts.
        if current_number_of_attempts % 4 == 0:
            number_of_switches = number_of_switches + 1

    # Print out introduction message.
    print_introduction_message()

    # Call the function to handle player input.
    handle_input()



################################################################################
# Text Processing
################################################################################

# Function to print out an introduction message.
def print_introduction_message():
    print "\n\n\nIntroduction: "
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
    print "1. go <forward, up, north, right, east, back, down, " \
    "south, left, west> <number>"
    print "2. grab <key>"
    print "3. open <chest, door>"
    print "4. use <key, marker, 123>"
    print "5. help"
    print "6. quit (back to title screen)"
    print "\nTo see this message again, enter the help command. Good luck!"

# Function to print out directions and a list of commands.
def help():
    print "Objectives: "
    print "1) Grab the key (used to unlock the door)"
    print "2) Open the chest"
    print "3) Open the door"
    print "\nCommand List: "
    print "1. go <forward, up, north, right, east, back, down, " \
    "south, left, west> <number>"
    print "2. grab <key>"
    print "3. open <chest, door>"
    print "4. use <key, marker, 123>"
    print "5. help"
    print "6. quit (back to title screen)"

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
# File Input/Output
################################################################################

# Function to manage the number of log files in the directory.
def manage_log_files():
    # List to store all filenames in the current working directory.
    general_filenames_list = []
    # List to store the filenames for log files.
    log_filenames_list = []

    # Get the list of all directory filenames.
    general_filenames_list = os.listdir(os.getcwd())

    # Iterate through the general_filenames_list and store each
    # log file's filename into the log_filenames_list.
    for log_filename in general_filenames_list:
        if log_filename[:4] == "Log_":
            log_filenames_list.append(log_filename)

    # Variable to store the number of log files.
    number_of_log_files = len(log_filenames_list)

    # Delete all except the 3 most recent log files.
    if number_of_log_files > 2:
        for i in range(number_of_log_files - 2):
            # Remove the log file from the hard drive.
            os.remove(log_filenames_list[i])

# Function to manage the number of replay files in the directory.
def manage_replay_files():
    # List to store all filenames in the current working directory.
    general_filenames_list = []
    # List to store the filenames for replay files.
    replay_filenames_list = []

    # Get the list of all directory filenames.
    general_filenames_list = os.listdir(os.getcwd())

    # Iterate through the general_filenames_list and store each
    # replay file's filename into the replay_filenames_list.
    for replay_filename in general_filenames_list:
        if replay_filename[:7] == "Replay_":
            replay_filenames_list.append(replay_filename)

    # Variable to store the number of replay files.
    number_of_replay_files = len(replay_filenames_list)

    # Delete all except the 3 most recent replay files.
    if number_of_replay_files > 2:
        for i in range(number_of_replay_files - 2):
            # Remove the replay file from the hard drive.
            os.remove(replay_filenames_list[i])

# Function to open the log file.
def open_log_file():
    global log_file
    global log_filename

    # Open the log file in write mode.
    log_file = open(log_filename, "wb")

# Function to open the replay file.
def open_replay_file():
    global replay_file
    global replay_filename

    # Open the replay file in write mode.
    replay_file = open(replay_filename, "wb")

# Function to open the replay file chosen by the user.
def open_chosen_replay_file(number):
    global chosen_replay_file
    global chosen_replay_filename
    
    # List to store all filenames in the current working directory.
    general_filenames_list = []
    # List to store the filenames for replay files.
    replay_filenames_list = []

    # Get the list of all directory filenames.
    general_filenames_list = os.listdir(os.getcwd())

    # Iterate through the general_filenames_list and store each
    # replay file's filename into the replay_filenames_list.
    for replay_filename in general_filenames_list:
        if replay_filename[:7] == "Replay_":
            replay_filenames_list.append(replay_filename)

    if number == 1 and len(replay_filenames_list) > 0:
        # Set the chosen replay filename.
        chosen_replay_filename = replay_filenames_list[0]
        # Open the chosen replay file in write mode.
        chosen_replay_file = open(chosen_replay_filename, "rb")
    elif number == 2 and len(replay_filenames_list) > 1:
        # Set the chosen replay filename.
        chosen_replay_filename = replay_filenames_list[1]
        # Open the chosen replay file in write mode.
        chosen_replay_file = open(chosen_replay_filename, "rb")
    elif number == 3 and len(replay_filenames_list) > 2:
        # Set the chosen replay filename.
        chosen_replay_filename = replay_filenames_list[2]
        # Open the chosen replay file in write mode.
        chosen_replay_file = open(chosen_replay_filename, "rb")

# Function to write to the log file.
def write_to_log_file(string):
    global log_file

    # Write the string to the log file.
    log_file.write(string + "\n")
    # Update the changes to the log file.
    log_file.flush()

# Function to write to the replay file.
def write_to_replay_file(string):
    global replay_file

    # Write the string to the replay file.
    replay_file.write(string + "\n")
    # Update the changes to the replay file.
    replay_file.flush()

# Function to close the opened log file.
def close_log_file():
    global log_file

    # Close the log file.
    log_file.close()

# Function to close the opened replay file.
def close_replay_file():
    global replay_file

    # Close the replay file.
    replay_file.close()

# Function to close the chosen replay file.
def close_chosen_replay_file():
    global chosen_replay_file

    # Close the chosen replay file.
    chosen_replay_file.close()



################################################################################
# Replay
################################################################################

# Function to open and play the replay to the user.
def open_replay(number):
    global grid
    global object_position_dictionary
    global player_object_position
    global chest_object_position
    global key_object_position
    global door_object_position
    global simple_enemy_object_position
    global smart_enemy_object_position
    global chest_combination_1_object_position
    global chest_combination_2_object_position
    global chest_combination_3_object_position
    global game_complete

    # Declare the game incomplete.
    game_complete = False

    # Open the chosen replay file.
    open_chosen_replay_file(number)

    # Set the caption for the console window.
    if number == 1:
        pygame.display.set_caption("Replay 1: " + str(chosen_replay_filename))
    elif number == 2:
        pygame.display.set_caption("Replay 2: " + str(chosen_replay_filename))
    elif number == 3:
        pygame.display.set_caption("Replay 3: " + str(chosen_replay_filename))

    # Read the chosen replay file and store into a list.
    chosen_replay_file_list = chosen_replay_file.readlines()

    # Close the opened chosen replay file after reading is complete.
    close_chosen_replay_file()

    # Set the grid equal to the same grid in the chosen replay file.
    grid = ast.literal_eval(chosen_replay_file_list[0])

    # Set the object positions equal to the same 
    # object positions in the chosen replay file.
    object_position_dictionary = ast.literal_eval(chosen_replay_file_list[1])

    player_object_position = \
    [object_position_dictionary['player'][0],
    object_position_dictionary['player'][1]]

    chest_object_position = \
    [object_position_dictionary['chest'][0],
    object_position_dictionary['chest'][1]]

    key_object_position = \
    [object_position_dictionary['key'][0],
    object_position_dictionary['key'][1]]

    door_object_position = \
    [object_position_dictionary['door'][0],
    object_position_dictionary['door'][1]]

    simple_enemy_object_position = \
    [object_position_dictionary['simple enemy'][0],
    object_position_dictionary['simple enemy'][1]]

    smart_enemy_object_position = \
    [object_position_dictionary['smart enemy'][0],
    object_position_dictionary['smart enemy'][1]]

    chest_combination_1_object_position = \
    [object_position_dictionary['chest combination 1'][0],
    object_position_dictionary['chest combination 1'][1]]

    chest_combination_2_object_position = \
    [object_position_dictionary['chest combination 2'][0],
    object_position_dictionary['chest combination 2'][1]]

    chest_combination_3_object_position = \
    [object_position_dictionary['chest combination 3'][0],
    object_position_dictionary['chest combination 3'][1]]

    # Print out the introduction message.
    print_introduction_message()

    # Draw the maze and the objects within it.
    draw_screen(screen)
    draw_player_object(player_object, screen)
    draw_closed_chest_object(chest_object_closed, screen)
    draw_key_object(key_object, screen)
    draw_door_object(door_object, screen)
    draw_simple_enemy_object(simple_enemy_object, screen)
    draw_smart_enemy_object(smart_enemy_object, screen)
    draw_chest_combination_1_object(chest_combination_1_object, screen)
    draw_chest_combination_2_object(chest_combination_2_object, screen)
    draw_chest_combination_3_object(chest_combination_3_object, screen)
    # Update the InputText widget.
    sgc.update(1)
    # Update the console window to show changes.
    pygame.display.update()

    # Continue running until the player completes the game or closes the window.
    while game_complete == False:
        i = 2
        while i < len(chosen_replay_file_list):
            # Pause for 3 seconds before executing the next step/command.
            time.sleep(3)

            # Print user input string to the output console window.
            # .rstrip() strips all whitespace from the input string.
            input_string = chosen_replay_file_list[i].rstrip()

            print_input(input_string)

            # Print error message if user input is empty.
            if input_string == "":
                print "Output: You aren't even trying, are you?" \
                        "\nTry entering actual text next time."
            # Print the objects and list of commands for the help command.
            elif input_string == "help":
                help()                    
            # Go back to the title screen if the player chooses to.
            elif input_string == "quit":
                game_complete = True
            # Possible user input for the go <Direction> command.
            elif input_string == "go forward" or input_string == "go up" \
            or input_string == "go north":
                go(0, -1)
            elif input_string == "go right" or input_string == "go east":
                go(1, 0)
            elif input_string == "go back" or input_string == "go down" \
            or input_string == "go south":
                go(0, 1)
            elif input_string == "go left" or input_string == "go west":
                go(-1, 0)
            elif input_string == "go chest":
                print "Output: A chest is for opening, not going." \
                        "\nTry going in a direction instead."
            elif input_string == "go key":
                print "Output: A key is for grabbing and/or using, not going." \
                        "\nTry going in a direction instead."
            elif input_string == "go door":
                print "Output: A door is for opening, not going." \
                        "\nTry going in a direction instead."
            elif input_string == "go wall":
                print "Output: You can't go into a wall. Are you even trying?"
            elif input_string == "go marker":
                print "Output: A marker is for using, not going." \
                        "\nTry going in a direction instead."
            # Possible user input for the grab <Object> command.
            elif input_string == "grab forward":
                print "Output: Forward is for going, not grabbing." \
                        "\nTry grabbing when a key is near."
            elif input_string == "grab right":
                print "Output: Right is for going, not grabbing." \
                        "\nTry grabbing when a key is near."
            elif input_string == "grab back":
                print "Output: Back is for going, not grabbing." \
                        "\nTry grabbing when a key is near."
            elif input_string == "grab left":
                print "Output: Left is for going, not grabbing." \
                        "\nTry grabbing when a key is near."
            elif input_string == "grab chest":
                print "Output: A chest is for opening, not grabbing." \
                        "\nTry grabbing when a key is near."
            elif input_string == "grab key":
                if player_grabbed_key:
                    # Inform the player that they already have the key.
                    print "Output: You already have the key." \
                            "\nNow you can use it for something, " \
                            "like unlocking a door maybe?"
                else:
                    grab_key()
            elif input_string == "grab door":
                print "Output: A door is for opening, not grabbing." \
                        "\nTry grabbing when a key is near."
            elif input_string == "grab wall":
                print "Output: You can't grab a wall." \
                        "\nWell, I guess you could, but it's not helpful." \
                        "\nTry grabbing when a key is near."
            elif input_string == "grab marker":
                print "Output: A marker is for using, not grabbing." \
                        "\nTry grabbing when a key is near."
            # Possible user input for the open <Object> command.
            elif input_string == "open forward":
                print "Output: Forward is for going, not opening." \
                        "\nTry opening when a door is near."
            elif input_string == "open right":
                print "Output: Right is for going, not opening." \
                        "\nTry opening when a door is near."
            elif input_string == "open back":
                print "Output: Back is for going, not opening." \
                        "\nTry opening when a door is near."
            elif input_string == "open left":
                print "Output: Left is for going, not opening." \
                        "\nTry opening when a door is near."
            elif input_string == "open chest":
                open_chest()
            elif input_string == "open key":
                print "Output: A key is for grabbing and/or using, " \
                        "not opening. \nTry opening when a door is near."
            elif input_string == "open door":
                open_door()
            elif input_string == "open wall":
                print "Output: You can try to open a wall, " \
                        "but it won't be helpful."
            elif input_string == "open marker":
                print "Output: A marker is for using, not opening." \
                        "\nTry opening when a door is near."
            # Possible user input for the use <Object> command.
            elif input_string == "use forward":
                print "Output: Forward is for going, not using." \
                        "\nTry using a key when a door is near."
            elif input_string == "use right":
                print "Output: Right is for going, not using." \
                        "\nTry using a key when a door is near."
            elif input_string == "use back":
                print "Output: Back is for going, not using." \
                        "\nTry using a key when a door is near."
            elif input_string == "use left":
                print "Output: Left is for going, not using." \
                        "\nTry using a key when a door is near."
            elif input_string == "use chest":
                print "Output: A chest is for unlocking and opening, " \
                        "not using. \nTry using a combination on the chest " \
                        "instead."
            elif input_string == "use key":
                use_key()
            elif input_string == "use door":
                print "Output: A door is for opening, not using." \
                        "\nTry using a key when a door is near."
            elif input_string == "use wall":
                print "Output: You can try to use a wall, " \
                        "but it's not helpful to you."
            elif input_string == "use marker":
                use_marker()
            else:
                # Parse the string into substrings and store into a list.
                input_substring_list = input_string.split(" ")

                # If the string has 3 substrings, attempt to parse it.
                if len(input_substring_list) == 3:
                    # Check if the first substring is equal to "go".
                    if input_substring_list[0] == "go" and \
                        input_substring_list[1].isalpha() and \
                        input_substring_list[2].isdigit():
                        go_length(input_substring_list[1], 
                                    input_substring_list[2])
                    else:
                        print_input_error()
                # If the string has 3 substrings, attempt to parse it.
                elif len(input_substring_list) == 2:
                    # Check if the first substring is equal to "use".
                    if input_substring_list[0] == "use":
                        if input_substring_list[1].isdigit():
                            unlock_chest(input_substring_list[1])
                        else:
                            print_input_error()
                    else:
                        print_input_error()
                # Not even close to a valid command or contains some 
                # form of misspelling or incorrect input 
                # (numbers, special characters, etc.).
                else:
                    print_input_error()

            # Clear the contents of the screen.
            screen.fill((0, 0, 0))
            # Get objects within the field of view and store them into a list.
            get_visible_object_list()
            # Call the function to draw the maze and the objects inside.
            draw_screen(screen)

            ################################################################
            ### Comment out this code to enable the field of view system.###
            draw_player_object(player_object, screen)
            if not player_opened_chest:
                draw_closed_chest_object(chest_object_closed, screen)
            else:
                draw_opened_chest_object(chest_object_opened, screen)
            draw_key_object(key_object, screen)
            draw_door_object(door_object, screen)
            draw_simple_enemy_object(simple_enemy_object, screen)
            draw_smart_enemy_object(smart_enemy_object, screen)
            draw_chest_combination_1_object(chest_combination_1_object, screen)
            draw_chest_combination_2_object(chest_combination_2_object, screen)
            draw_chest_combination_3_object(chest_combination_3_object, screen)

            if player_used_marker == True:
                for i in range(len(marked_tile_list)):
                    # Fill in the marked tiles with the color red.
                    screen.fill((255, 0, 0), get_cell_rect(marked_tile_list[i], 
                                                            screen))
            ################################################################

            # Update the InputText widget.
            sgc.update(1)
            # Update the console window to show changes.
            pygame.display.update()

            i = i + 1
        game_complete = True
    # Pause for 7 seconds before terminating the program.
    time.sleep(7)

    # Print new lines for spacing.
    print "\n\n"

    # Exit the current scope and back to the loop that controls the game state.
    return



################################################################################
# Rendering
################################################################################

# Function that generates a random maze using the Recursive Backtracker algorithm.
def generate_maze_recursive_backtracker():
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
        grid[current_y][current_x] = 1

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
                if grid[new_y][new_x] == 0:
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
                            if grid[temporary_y][temporary_x] == 1: 
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

# Function that generates a random maze using the Binary Tree algorithm.
def generate_maze_binary_tree():
    # Size of the maze.
    maze_width = len(grid) - 1
    maze_height = len(grid) - 1
    
    y = 1
    # Iterate through each row of the maze.
    while y < maze_height + 1:

        x = 1
        # Iterate through each column of the maze.
        while x < maze_height + 1:
            # Set the value of direction randomly to 0 or 1.
            direction = random.randint(0, 1)

            # Carve passage North.
            if direction == 1:

                # Carve out the current position.
                grid[y][x] = 1
                
                # Carve out the position above.
                grid[y - 1][x] = 1
                                
            # Carve passage West.
            elif direction == 0:
                # Carve out the current position.
                grid[y][x] = 1
                # Carve out the next position to the left.
                grid[y][x - 1] = 1

            # Increment x.
            x = x + 2

        # Increment y.
        y = y + 2

    # Carve out the first column and row of the maze.
    i = 1
    while i < len(grid) - 1:
        # Carve out first column of the maze.
        grid[i][1] = 1
        # Carve out first row of the maze.
        grid[1][i] = 1
        i = i + 1

    # Block in the bounds of the maze.
    for y in range(len(grid)):
        # Block first column.
        grid[y][0] = 0

    for x in range(len(grid)):
        # Block first row.
        grid[0][x] = 0
    
    for y in range(len(grid)):
        # Block last column.
        grid[len(grid) - 1][y] = 0

    for x in range(len(grid)):
        # Block last row.
        grid[x][len(grid) - 1] = 0

# Function to reset the maze back to its original state.
def reset_maze():
    global grid

    # Reset the grid.
    grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Function to test the maze for validity by checking 
# the path from the player to the door object.
def check_maze_for_validity_player_door():
    # Create a test grid, which will be used in the A* algorithm 
    # to test the maze to ensure that the player can reach the door.
    test_grid = GridWithWeights(len(grid), len(grid))

    # Traverse the grid to grab all of the wall locations.
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            if grid[column][row] == 0:
                wall = (row, column)
                # Add the wall locations to the graph's list of walls.
                test_grid.walls.append(wall)

    # The current position of the player.
    start = (player_object_position[0], player_object_position[1])
    # The current position of the door.
    goal = (door_object_position[0], door_object_position[1])
    # Get dictionaries mapping positions using the A* search algorithm.
    came_from, cost_so_far = a_star_search(test_grid, start, goal)

    # Check all possible coordinates to see if the door object 
    # is in the optimal path. If it is, then the maze is valid.
    for coordinates in came_from.iteritems():
        if ((coordinates[0][0], coordinates[0][1]) == 
            (door_object_position[0], door_object_position[1])):
            # Return 0, the maze is valid.
            return 0

    # Return 1, the maze is invalid.
    return 1

# Function to test the maze for validity by checking 
# the path from the player to the key object.
def check_maze_for_validity_player_key():
    # Create a test grid, which will be used in the A* algorithm 
    # to test the maze to ensure that the player can reach the key.
    test_grid = GridWithWeights(len(grid), len(grid))

    # Traverse the grid to grab all of the wall locations.
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            if grid[column][row] == 0:
                wall = (row, column)
                # Add the wall locations to the graph's list of walls.
                test_grid.walls.append(wall)

    # The current position of the player.
    start = (player_object_position[0], player_object_position[1])
    # The current position of the key.
    goal = (key_object_position[0], key_object_position[1])
    # Get dictionaries mapping positions using the A* search algorithm.
    came_from, cost_so_far = a_star_search(test_grid, start, goal)

    # Check all possible coordinates to see if the key object 
    # is in the optimal path. If it is, then the maze is valid.
    for coordinates in came_from.iteritems():
        if ((coordinates[0][0], coordinates[0][1]) == 
            (key_object_position[0], key_object_position[1])):
            # Return 0, the maze is valid.
            return 0

    # Return 1, the maze is invalid.
    return 1

# Function to test the maze for validity by checking 
# the path from the player to the chest object.
def check_maze_for_validity_player_chest():
    # Create a test grid, which will be used in the A* algorithm 
    # to test the maze to ensure that the player can reach the chest.
    test_grid = GridWithWeights(len(grid), len(grid))

    # Traverse the grid to grab all of the wall locations.
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            if grid[column][row] == 0:
                wall = (row, column)
                # Add the wall locations to the graph's list of walls.
                test_grid.walls.append(wall)

    # The current position of the player.
    start = (player_object_position[0], player_object_position[1])
    # The current position of the chest.
    goal = (chest_object_position[0], chest_object_position[1])
    # Get dictionaries mapping positions using the A* search algorithm.
    came_from, cost_so_far = a_star_search(test_grid, start, goal)

    # Check all possible coordinates to see if the chest object 
    # is in the optimal path. If it is, then the maze is valid.
    for coordinates in came_from.iteritems():
        if ((coordinates[0][0], coordinates[0][1]) == 
            (chest_object_position[0], chest_object_position[1])):
            # Return 0, the maze is valid.
            return 0

    # Return 1, the maze is invalid.
    return 1

# Function to draw the screen.
def draw_screen(screen):
    ############################################################################
    ######### Comment out this code to enable the field of view system.#########
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            screen.fill(cell_colors[grid[column][row]],
                        get_cell_rect((row, column), screen))
    ############################################################################

    

    ############################################################################
    ######### Comment out this code to disable the field of view system.########
    '''# Color the visible objects of the grid.
    for i in range(len(visible_object_list)):
        # Only draw the tile if it is in the range of the grid.
        if visible_object_list[i][0] >= 0 and \
            visible_object_list[i][0] < len(grid) and \
            visible_object_list[i][1] >= 0 and \
            visible_object_list[i][1] < len(grid):
            if grid[visible_object_list[i][1]][visible_object_list[i][0]] == 0:
                # Fill the wall object with the color white.
                screen.fill((255, 255, 255), \
                    get_cell_rect((visible_object_list[i][0], 
                                   visible_object_list[i][1]), screen))

    # Call the function to draw the door object if visible.
    if is_object_visible(door_object_position[0], door_object_position[1]):
        draw_door_object(door_object, screen)

    if is_object_visible(chest_object_position[0], chest_object_position[1]):
        # Draw the closed chest if the chest has not been opened and is visible.
        if not player_opened_chest:
            # Call the function to draw the closed chest object if visible.
            draw_closed_chest_object(chest_object_closed, screen)
        # Draw the opened chest if the chest has been opened and is visible.
        else:
            # Call the function to draw the opened chest object if visible.
            draw_opened_chest_object(chest_object_opened, screen)
            
    # Call the function to draw the key object if visible.
    if is_object_visible(key_object_position[0], key_object_position[1]):
        if not player_grabbed_key:
            draw_key_object(key_object, screen)

    # Call the function to draw the simple enemy object if visible.
    if is_object_visible(simple_enemy_object_position[0], 
    simple_enemy_object_position[1]):
        draw_simple_enemy_object(simple_enemy_object, screen)

    # Call the function to draw the smart enemy object if visible.
    if is_object_visible(smart_enemy_object_position[0], 
    smart_enemy_object_position[1]):
        draw_smart_enemy_object(smart_enemy_object, screen)
            
    # Call the function to draw the chest_combination_1 object if visible.
    if is_object_visible(chest_combination_1_object_position[0], \
        chest_combination_1_object_position[1]):
        draw_chest_combination_1_object(chest_combination_1_object, screen)
        
    # Call the function to draw the chest_combination_2 object if visible.
    if is_object_visible(chest_combination_2_object_position[0], \
        chest_combination_2_object_position[1]):
        draw_chest_combination_2_object(chest_combination_2_object, screen)
        
    # Call the function to draw the chest_combination_3 object if visible.
    if is_object_visible(chest_combination_3_object_position[0], \
        chest_combination_3_object_position[1]):
        draw_chest_combination_3_object(chest_combination_3_object, screen)

    # Change the color of the visible marked tiles if any exist.
    if player_used_marker == True:
        for i in range(len(marked_tile_list)):
            if is_object_visible(marked_tile_list[i][0], marked_tile_list[i][1]):
                # Fill in the marked tiles with the color red.
                screen.fill((255, 0, 0), get_cell_rect(marked_tile_list[i], screen))

    # Call the function to draw the player character object.
    draw_player_object(player_object, screen)'''
    ############################################################################

# Function to determine if the given object is within the field of view.
def is_object_visible(object_position_x, object_position_y):
    for i in range(len(visible_object_list)):
        if object_position_x == visible_object_list[i][0] and \
            object_position_y == visible_object_list[i][1]:
            return True

    return False

# Function to store object coordinates that are within the field of view.
def get_visible_object_list():
    global visible_object_list

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Clear the contents of the visible_object_list.
    visible_object_list = []

    # Tiles that are within 1 square from the player character object.
    if x >= 0 and x < len(grid) and y >= 0 and y < len(grid):
        visible_object_list.append((x, y))
    if x - 1 >= 0 and x - 1 < len(grid) and y - 1 >= 0 and y - 1 < len(grid):
        visible_object_list.append((x - 1, y - 1))
    if x >= 0 and x < len(grid) and y - 1 >= 0 and y - 1 < len(grid):
        visible_object_list.append((x, y - 1))
    if x + 1 >= 0 and x + 1 < len(grid) and y - 1 >= 0 and y - 1 < len(grid):
        visible_object_list.append((x + 1, y - 1))
    if x - 1 >= 0 and x - 1 < len(grid) and y >= 0 and y < len(grid):
        visible_object_list.append((x - 1, y))
    if x + 1 >= 0 and x + 1 < len(grid) and y >= 0 and y < len(grid):
        visible_object_list.append((x + 1, y))
    if x - 1 >= 0 and x - 1 < len(grid) and y + 1 >= 0 and y + 1 < len(grid):
        visible_object_list.append((x - 1, y + 1))
    if x >= 0 and x < len(grid) and y + 1 >= 0 and y + 1 < len(grid):
        visible_object_list.append((x, y + 1))
    if x + 1 >= 0 and x + 1 < len(grid) and y + 1 >= 0 and y + 1 < len(grid):
        visible_object_list.append((x + 1, y + 1))
        
    # Tiles that are within 2 squares from the player character object. 
    if x - 1 >= 0 and x + 1 < len(grid) and y - 2 >= 0 and y - 2 < len(grid):
        if grid[y - 1][x] == 1:
            visible_object_list.append((x - 1, y - 2))
            visible_object_list.append((x, y - 2))
            visible_object_list.append((x + 1, y - 2))
    if x + 2 >= 0 and x + 2 < len(grid) and y - 1 >= 0 and y + 1 < len(grid):
        if grid[y][x + 1] == 1:
            visible_object_list.append((x + 2, y - 1))
            visible_object_list.append((x + 2, y))
            visible_object_list.append((x + 2, y + 1))
    if x - 1 >= 0 and x + 1 < len(grid) and y + 2 >= 0 and y + 2 < len(grid):
        if grid[y + 1][x] == 1:
            visible_object_list.append((x - 1, y + 2))
            visible_object_list.append((x, y + 2))
            visible_object_list.append((x + 1, y + 2))
    if x - 2 >= 0 and x - 2 < len(grid) and y - 1 >= 0 and y + 1 < len(grid):
        if grid[y][x - 1] == 1:
            visible_object_list.append((x - 2, y - 1))
            visible_object_list.append((x - 2, y))
            visible_object_list.append((x - 2, y + 1))

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

# Function to draw the closed chest object to the console window.
def draw_closed_chest_object(chest_object_closed, screen):
    # Return the size and offset of the closed chest object.
    rect = chest_object_closed.get_rect()
    # Receive the center of the closed chest object.
    rect.center = get_cell_rect(chest_object_position, screen).center
    # Draw the closed chest object image.
    screen.blit(chest_object_closed, rect)

# Function to draw the opened chest object to the console window.
def draw_opened_chest_object(chest_object_opened, screen):
    # Return the size and offset of the opened chest object.
    rect = chest_object_opened.get_rect()
    # Receive the center of the opened chest object.
    rect.center = get_cell_rect(chest_object_position, screen).center
    # Draw the opened chest object image.
    screen.blit(chest_object_opened, rect)

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

# Function to draw the simple enemy object to the console window.
def draw_simple_enemy_object(simple_enemy_object, screen):
    # Return the size and offset of the simple enemy object.
    rect = simple_enemy_object.get_rect()
    # Receive the center of the simple enemy object.
    rect.center = get_cell_rect(simple_enemy_object_position, screen).center
    # Draw the simple enemy object image.
    screen.blit(simple_enemy_object, rect)

# Function to draw the smart enemy object to the console window.
def draw_smart_enemy_object(smart_enemy_object, screen):
    # Return the size and offset of the smart enemy object.
    rect = smart_enemy_object.get_rect()
    # Receive the center of the smart enemy object.
    rect.center = get_cell_rect(smart_enemy_object_position, screen).center
    # Draw the smart enemy object image.
    screen.blit(smart_enemy_object, rect)

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

# Function to generate random start positions for
# the player, chest, key, door, and enemy objects.
def generate_random_object_positions():
    global player_object_position
    global chest_object_position
    global key_object_position
    global door_object_position
    global simple_enemy_object_position
    global smart_enemy_object_position

    # Variable representing the number of objects on the grid.
    number_of_objects = 0
    
    while number_of_objects != 1:
        # Generate a random x and y coordinate for the object position.
        randomx = random.randint(1, len(grid) - 1)
        randomy = random.randint(1, len(grid) - 1)

        if not position_is_wall(randomx, randomy) and \
            not position_is_object(randomx, randomy):
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

        if not position_is_wall(randomx, randomy) and \
            not position_is_object(randomx, randomy):
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

        if not position_is_wall(randomx, randomy) and \
            not position_is_object(randomx, randomy):
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

        if not position_is_wall(randomx, randomy) and \
            not position_is_object(randomx, randomy):
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

        if not position_is_wall(randomx, randomy) and \
            not position_is_object(randomx, randomy):
            # Set the simple enemy object position 
            # equal to the random x and y values.
            simple_enemy_object_position[0] = randomx 
            simple_enemy_object_position[1] = randomy

            # Add the simple enemy object position to the dictionary.
            object_position_dictionary['simple enemy'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

    while number_of_objects != 6:
        # Generate a random x and y coordinate for the object position.
        randomx = random.randint(1, len(grid) - 1)
        randomy = random.randint(1, len(grid) - 1)

        if not position_is_wall(randomx, randomy) and \
            not position_is_object(randomx, randomy):
            # Set the smart enemy object position 
            # equal to the random x and y values.
            smart_enemy_object_position[0] = randomx 
            smart_enemy_object_position[1] = randomy

            # Add the smart enemy object position to the dictionary.
            object_position_dictionary['smart enemy'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

# Function to generate random positions for the objects on the optimal path.
def generate_optimal_object_positions():
    global chest_combination_1_object_position
    global chest_combination_2_object_position
    global chest_combination_3_object_position

    # Variable representing the number of objects on the grid.
    number_of_objects = 0

    # Create a test grid, which will be used in the A* algorithm 
    # to generate a list for the rest of the object placement.
    test_grid = GridWithWeights(len(grid), len(grid))

    # Traverse the grid to grab all of the wall locations.
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            if grid[column][row] == 0:
                wall = (row, column)
                # Add the wall locations to the graph's list of walls.
                test_grid.walls.append(wall)

    # The starting location of the player.
    start = (player_object_position[0], player_object_position[1])
    # The position of the door, or the exit condition.
    goal = (door_object_position[0], door_object_position[1])
    # Get dictionaries mapping positions using the A* search algorithm.
    came_from, cost_so_far = a_star_search(test_grid, start, goal)

    # List that contains all possible coordinates located in the optimal path.
    optimal_path_coordinates_list = []

    # Store all possible coordinates into the optimal_path_coordinates_list.
    for coordinates, cost in cost_so_far.iteritems():
        if cost > 0 and not position_is_object(coordinates[0], coordinates[1]):
            optimal_path_coordinates_list.append(coordinates)

    while number_of_objects != 1:
        # Generate a random x and y coordinate for the object position.
        temp = random.randint(0, len(optimal_path_coordinates_list) - 1)
        x = optimal_path_coordinates_list[temp][0]
        y = optimal_path_coordinates_list[temp][1]

        # Instantiate the neighbor_wall_coordinates_list.
        neighbor_wall_coordinates_list = []

        # Add the tile coordinates to the neighbor_wall_coordinates_list.
        if grid[y - 1][x - 1] == 0:
            neighbor_wall_coordinates_list.append((x - 1, y - 1))
        if grid[y - 1][x] == 0:
            neighbor_wall_coordinates_list.append((x, y - 1))
        if grid[y - 1][x + 1] == 0:
            neighbor_wall_coordinates_list.append((x + 1, y - 1))
        if grid[y][x - 1] == 0:
            neighbor_wall_coordinates_list.append((x - 1, y))
        if grid[y][x + 1] == 0:
            neighbor_wall_coordinates_list.append((x + 1, y))
        if grid[y + 1][x - 1] == 0:
            neighbor_wall_coordinates_list.append((x - 1, y + 1))
        if grid[y + 1][x] == 0:
            neighbor_wall_coordinates_list.append((x, y + 1))
        if grid[y + 1][x + 1] == 0:
            neighbor_wall_coordinates_list.append((x + 1, y + 1))

        # Get a random position in neighbor_wall_coordinates_list.
        temp = random.randint(0, len(neighbor_wall_coordinates_list) - 1)
        
        # Set randomx, and randomy to the randomly picked coordinates.
        randomx = neighbor_wall_coordinates_list[temp][0]
        randomy = neighbor_wall_coordinates_list[temp][1]

        if position_is_wall(randomx, randomy) and \
            not position_is_object(randomx, randomy):
            # Set the chest_combination_1 object position 
            # equal to the random x and y values.
            chest_combination_1_object_position[0] = randomx 
            chest_combination_1_object_position[1] = randomy

            # Add the chest_combination_1 object position to the dictionary.
            object_position_dictionary['chest combination 1'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

    while number_of_objects != 2:    
        # Generate a random x and y coordinate for the object position.
        temp = random.randint(0, len(optimal_path_coordinates_list) - 1)
        x = optimal_path_coordinates_list[temp][0]
        y = optimal_path_coordinates_list[temp][1]

        # Instantiate the neighbor_wall_coordinates_list.
        neighbor_wall_coordinates_list = []

        # Add the tile coordinates to the neighbor_wall_coordinates_list.
        if grid[y - 1][x - 1] == 0:
            neighbor_wall_coordinates_list.append((x - 1, y - 1))
        if grid[y - 1][x] == 0:
            neighbor_wall_coordinates_list.append((x, y - 1))
        if grid[y - 1][x + 1] == 0:
            neighbor_wall_coordinates_list.append((x + 1, y - 1))
        if grid[y][x - 1] == 0:
            neighbor_wall_coordinates_list.append((x - 1, y))
        if grid[y][x + 1] == 0:
            neighbor_wall_coordinates_list.append((x + 1, y))
        if grid[y + 1][x - 1] == 0:
            neighbor_wall_coordinates_list.append((x - 1, y + 1))
        if grid[y + 1][x] == 0:
            neighbor_wall_coordinates_list.append((x, y + 1))
        if grid[y + 1][x + 1] == 0:
            neighbor_wall_coordinates_list.append((x + 1, y + 1))

        # Get a random position in neighbor_wall_coordinates_list.
        temp = random.randint(0, len(neighbor_wall_coordinates_list) - 1)
        
        # Set randomx, and randomy to the randomly picked coordinates.
        randomx = neighbor_wall_coordinates_list[temp][0]
        randomy = neighbor_wall_coordinates_list[temp][1]

        if position_is_wall(randomx, randomy) and \
            not position_is_object(randomx, randomy):
            # Set the chest_combination_2 object position 
            # equal to the random x and y values.
            chest_combination_2_object_position[0] = randomx 
            chest_combination_2_object_position[1] = randomy

            # Add the chest_combination_2 object position to the dictionary.
            object_position_dictionary['chest combination 2'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

    while number_of_objects != 3:    
        # Generate a random x and y coordinate for the object position.
        temp = random.randint(0, len(optimal_path_coordinates_list) - 1)
        x = optimal_path_coordinates_list[temp][0]
        y = optimal_path_coordinates_list[temp][1]

        # Instantiate the neighbor_wall_coordinates_list.
        neighbor_wall_coordinates_list = []

        # Add the tile coordinates to the neighbor_wall_coordinates_list.
        if grid[y - 1][x - 1] == 0:
            neighbor_wall_coordinates_list.append((x - 1, y - 1))
        if grid[y - 1][x] == 0:
            neighbor_wall_coordinates_list.append((x, y - 1))
        if grid[y - 1][x + 1] == 0:
            neighbor_wall_coordinates_list.append((x + 1, y - 1))
        if grid[y][x - 1] == 0:
            neighbor_wall_coordinates_list.append((x - 1, y))
        if grid[y][x + 1] == 0:
            neighbor_wall_coordinates_list.append((x + 1, y))
        if grid[y + 1][x - 1] == 0:
            neighbor_wall_coordinates_list.append((x - 1, y + 1))
        if grid[y + 1][x] == 0:
            neighbor_wall_coordinates_list.append((x, y + 1))
        if grid[y + 1][x + 1] == 0:
            neighbor_wall_coordinates_list.append((x + 1, y + 1))

        # Get a random position in neighbor_wall_coordinates_list.
        temp = random.randint(0, len(neighbor_wall_coordinates_list) - 1)
        
        # Set randomx, and randomy to the randomly picked coordinates.
        randomx = neighbor_wall_coordinates_list[temp][0]
        randomy = neighbor_wall_coordinates_list[temp][1]

        if position_is_wall(randomx, randomy) and \
            not position_is_object(randomx, randomy):
            # Set the chest_combination_3 object position
            # equal to the random x and y values.
            chest_combination_3_object_position[0] = randomx 
            chest_combination_3_object_position[1] = randomy

            # Add the chest_combination_3 object position to the dictionary.
            object_position_dictionary['chest combination 3'] = randomx, randomy

            # Increment the number of placed objects.
            number_of_objects += 1

# Function to determine if the coordinate is blocked by an object.
def position_is_object(x, y):
    # Return True for the player object.
    if x == player_object_position[0] and y == player_object_position[1]:
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
    # Return True for the simple enemy object.
    elif x == simple_enemy_object_position[0] and \
        y == simple_enemy_object_position[1]:
        return True
    # Return True for the smart enemy object.
    elif x == smart_enemy_object_position[0] and \
        y == smart_enemy_object_position[1]:
        return True
    # Return True for the first chest combination object.
    elif x == chest_combination_1_object_position[0] and \
        y == chest_combination_1_object_position[1]:
        return True
    # Return True for the second chest combination object.
    elif x == chest_combination_2_object_position[0] and \
        y == chest_combination_2_object_position[1]:
        return True
    # Return True for the third chest combination object.
    elif x == chest_combination_3_object_position[0] and \
        y == chest_combination_3_object_position[1]:
        return True
 
    return False

# Function to determine if the coordinate is blocked by a wall.
def position_is_wall(x, y):
    # Return True for the wall object.
    if grid[y][x] == 0:
        return True
 
    return False

# Function that resets the position of the player 
# and confiscates all gathered items.
def reset_object_positions_and_state_conditions():
    # Global variables used to store objective states. 
    global player_grabbed_key
    global player_used_key
    global player_used_marker
    global player_unlocked_chest
    global player_opened_chest
    # Global variables used to store object positions.  
    global player_object_position
    global key_object_position
    global simple_enemy_object_position
    global smart_enemy_object_position

    # Reset all objective states.
    player_grabbed_key = False
    player_used_key = False
    player_used_marker = False
    player_unlocked_chest = False
    player_opened_chest = False

    # Reset all object positions. 
    player_object_position = [object_position_dictionary['player'][0], 
    object_position_dictionary['player'][1]]

    key_object_position = [object_position_dictionary['key'][0],
    object_position_dictionary['key'][1]]

    simple_enemy_object_position = [object_position_dictionary['simple enemy'][0],
    object_position_dictionary['simple enemy'][1]]

    smart_enemy_object_position = [object_position_dictionary['smart enemy'][0],
    object_position_dictionary['smart enemy'][1]]



################################################################################
# Player Input
################################################################################

# Function to handle player character movement.
def handle_input():
    global replay_filename
    global player_object
    global chest_object_closed
    global chest_object_opened
    global key_object
    global door_object
    global simple_enemy_object
    global smart_enemy_object
    global chest_combination_1_object
    global chest_combination_2_object
    global chest_combination_3_object
    global player_made_decision
    global game_complete

    # Reset the state of player 
    # decisions and game conditions.
    player_grabbed_key = False
    player_used_key = False
    player_used_marker = False
    player_unlocked_chest = False
    player_opened_chest = False
    game_complete = False

    # Manage the number of replay files.
    manage_replay_files()

    # Create a string equal to the current time for the replay file.
    replay_filename = time.strftime("Replay_%m-%d-%y_%H-%M-%S.txt")

    # Open the replay file.
    open_replay_file()

    # Store all necessary information into the replay file.
    write_to_replay_file(str(grid))
    write_to_replay_file(str(object_position_dictionary))

    # Continue running until the player completes the game or closes the window.
    while game_complete == False:
        # Begin the try block to catch all exceptions
        # that may occur while accepting user input.
        try:
            # Iterate through all of the events gathered from pygame.
            for event in pygame.event.get():
                sgc.event(event)
                if event.type == GUI:
                    # Print user input string to the output console window. 
                    input_string = event.text.lower()
                    print_input(input_string)

                    # Write the input to the replay file.
                    write_to_replay_file(input_string)

                    # Print error message if user input is empty.
                    if input_string == "":
                        print "Output: You aren't even trying, are you?" \
                              "\nTry entering actual text next time."
                    # Print the objects and list of commands for the help command.
                    elif input_string == "help":
                        help()
                    # Go back to the title screen if the player chooses to.
                    elif input_string == "quit":
                        game_complete = True
                    # Possible user input for the go <Direction> command.
                    elif input_string == "go forward" or input_string == "go up" \
                    or input_string == "go north":
                        go(0, -1)
                    elif input_string == "go right" or input_string == "go east":
                        go(1, 0)
                    elif input_string == "go back" or input_string == "go down" \
                    or input_string == "go south":
                        go(0, 1)
                    elif input_string == "go left" or input_string == "go west":
                        go(-1, 0)
                    elif input_string == "go chest":
                        print "Output: A chest is for opening, not going." \
                              "\nTry going in a direction instead."
                    elif input_string == "go key":
                        print "Output: A key is for grabbing and/or using, not going." \
                              "\nTry going in a direction instead."
                    elif input_string == "go door":
                        print "Output: A door is for opening, not going." \
                              "\nTry going in a direction instead."
                    elif input_string == "go wall":
                        print "Output: You can't go into a wall. Are you even trying?"
                    elif input_string == "go marker":
                        print "Output: A marker is for using, not going." \
                              "\nTry going in a direction instead."
                    # Possible user input for the grab <Object> command.
                    elif input_string == "grab forward":
                        print "Output: Forward is for going, not grabbing." \
                              "\nTry grabbing when a key is near."
                    elif input_string == "grab right":
                        print "Output: Right is for going, not grabbing." \
                              "\nTry grabbing when a key is near."
                    elif input_string == "grab back":
                        print "Output: Back is for going, not grabbing." \
                              "\nTry grabbing when a key is near."
                    elif input_string == "grab left":
                        print "Output: Left is for going, not grabbing." \
                              "\nTry grabbing when a key is near."
                    elif input_string == "grab chest":
                        print "Output: A chest is for opening, not grabbing." \
                              "\nTry grabbing when a key is near."
                    elif input_string == "grab key":
                        if player_grabbed_key:
                            # Inform the player that they already have the key.
                            print "Output: You already have the key." \
                                  "\nNow you can use it for something, " \
                                  "like unlocking a door maybe?"
                        else:
                            grab_key()
                    elif input_string == "grab door":
                        print "Output: A door is for opening, not grabbing." \
                              "\nTry grabbing when a key is near."
                    elif input_string == "grab wall":
                        print "Output: You can't grab a wall." \
                              "\nWell, I guess you could, but it's not helpful." \
                              "\nTry grabbing when a key is near."
                    elif input_string == "grab marker":
                        print "Output: A marker is for using, not grabbing." \
                              "\nTry grabbing when a key is near."
                    # Possible user input for the open <Object> command.
                    elif input_string == "open forward":
                        print "Output: Forward is for going, not opening." \
                              "\nTry opening when a door is near."
                    elif input_string == "open right":
                        print "Output: Right is for going, not opening." \
                              "\nTry opening when a door is near."
                    elif input_string == "open back":
                        print "Output: Back is for going, not opening." \
                              "\nTry opening when a door is near."
                    elif input_string == "open left":
                        print "Output: Left is for going, not opening." \
                              "\nTry opening when a door is near."
                    elif input_string == "open chest":
                        open_chest()
                    elif input_string == "open key":
                        print "Output: A key is for grabbing and/or using, " \
                                "not opening. \nTry opening when a door is near."
                    elif input_string == "open door":
                        open_door()
                    elif input_string == "open wall":
                        print "Output: You can try to open a wall, " \
                              "but it won't be helpful."
                    elif input_string == "open marker":
                        print "Output: A marker is for using, not opening." \
                              "\nTry opening when a door is near."
                    # Possible user input for the use <Object> command.
                    elif input_string == "use forward":
                        print "Output: Forward is for going, not using." \
                              "\nTry using a key when a door is near."
                    elif input_string == "use right":
                        print "Output: Right is for going, not using." \
                              "\nTry using a key when a door is near."
                    elif input_string == "use back":
                        print "Output: Back is for going, not using." \
                              "\nTry using a key when a door is near."
                    elif input_string == "use left":
                        print "Output: Left is for going, not using." \
                              "\nTry using a key when a door is near."
                    elif input_string == "use chest":
                        print "Output: A chest is for unlocking and opening, " \
                              "not using. \nTry using a combination on the chest " \
                              "instead."
                    elif input_string == "use key":
                        use_key()
                    elif input_string == "use door":
                        print "Output: A door is for opening, not using." \
                              "\nTry using a key when a door is near."
                    elif input_string == "use wall":
                        print "Output: You can try to use a wall, " \
                              "but it's not helpful to you."
                    elif input_string == "use marker":
                        use_marker()
                    else:
                        # Parse the string into substrings and store into a list.
                        input_substring_list = input_string.split(" ")

                        # If the string has 3 substrings, attempt to parse it.
                        if len(input_substring_list) == 3:
                            # Check if the first substring is equal to "go".
                            if input_substring_list[0] == "go" and \
                                input_substring_list[1].isalpha() and \
                                input_substring_list[2].isdigit():
                                go_length(input_substring_list[1], 
                                          input_substring_list[2])
                            else:
                                print_input_error()
                        # If the string has 3 substrings, attempt to parse it.
                        elif len(input_substring_list) == 2:
                            # Check if the first substring is equal to "use".
                            if input_substring_list[0] == "use":
                                if input_substring_list[1].isdigit():
                                    unlock_chest(input_substring_list[1])
                                else:
                                    print_input_error()
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

            # Clear the contents of the screen.
            screen.fill((0, 0, 0))
            # Get objects within the field of view and store them into a list.
            get_visible_object_list()
            # Call the function to draw the maze and the objects inside.
            draw_screen(screen)

            ####################################################################
            ##### Comment out this code to enable the field of view system.#####
            draw_player_object(player_object, screen)
            if not player_opened_chest:
                draw_closed_chest_object(chest_object_closed, screen)
            else:
                draw_opened_chest_object(chest_object_opened, screen)
            draw_key_object(key_object, screen)
            draw_door_object(door_object, screen)
            draw_simple_enemy_object(simple_enemy_object, screen)
            draw_smart_enemy_object(smart_enemy_object, screen)
            draw_chest_combination_1_object(chest_combination_1_object, screen)
            draw_chest_combination_2_object(chest_combination_2_object, screen)
            draw_chest_combination_3_object(chest_combination_3_object, screen)

            if player_used_marker == True:
                for i in range(len(marked_tile_list)):
                    # Fill in the marked tiles with the color red.
                    screen.fill((255, 0, 0), get_cell_rect(marked_tile_list[i], 
                                                           screen))
            ####################################################################

            # Update the InputText widget.
            sgc.update(1)
            # Update the console window to show changes.
            pygame.display.update()
        # End the catch block and print the exception 
        # (if one occurred) to the log file and continue.
        except:
            # Store the exception.
            e = sys.exc_info()[0]
            # Piece the exception message together for printing.
            exception_message = (str(time.strftime("%H-%M-%S")) + ": Error: "
                                 + str(e) + " \n\t\t\tIgnoring your feeble " 
                                 + "attempts to crash the game and continuing.")
            # Print the exception to the log file.
            write_to_log_file(exception_message)

    # Close the opened replay file.
    close_replay_file()

    # Exit the current scope and back to the loop that controls the game state.
    return



################################################################################
# Character Actions
################################################################################

# Function to move the player character object through the maze.
def go(dx, dy):
    # Call the function to reset the game if the player character 
    # is in the same coordinate as either enemy.
    if player_object_position == simple_enemy_object_position \
        or player_object_position == smart_enemy_object_position:
        # Print out an message informing the user that they lost.
        print "Output: The enemy grabbed you! Your stuff was confiscated "
        print "\tand you were returned to where you started. "
        print "\tYou will have to try your luck again...\n"
        # Reset the locations of all objects and state conditions.
        reset_object_positions_and_state_conditions()
    # Continue if the player has not been caught yet.
    else:
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
                player_object_position[0] = nx
                player_object_position[1] = ny
        else:
            # Print out an error for the invalid move.
            print_go_error()

        # Call the function to move the enemies.
        move_simple_enemy()
        move_smart_enemy()

    # Call the function to reset the game if the player character 
    # is in the same coordinate as either enemy.
    if player_object_position == simple_enemy_object_position \
        or player_object_position == smart_enemy_object_position:
        # Print out an message informing the user that they lost.
        print "Output: The enemy grabbed you! Your stuff was confiscated "
        print "\tand you were returned to where you started. "
        print "\tYou will have to try your luck again...\n"
        # Reset the locations of all objects and state conditions.
        reset_object_positions_and_state_conditions()

# Function to move the player character object through 
# the maze for the number of times they specify.
def go_length(direction, length):
    # Check if the second substring is equal to "forward".
    if direction == "forward" or direction == "up" or direction == "north":
        # Variable used as a counter.
        i = 0
        while i < int(length):
            # Break out of the loop if the destination coordinates are occupied.
            if position_is_wall(player_object_position[0], 
                                   player_object_position[1] - 1):
                # Print out an error for the invalid move.
                print_go_error()
                break
            # Call the go command.
            go(0, -1)
            # Increment the counter.
            i = i + 1
    # Check if the second substring is equal to "right".
    elif direction == "right" or direction == "east":
        # Variable used as a counter.
        i = 0
        while i < int(length):
            # Break out of the loop if the destination coordinates are occupied.
            if position_is_wall(player_object_position[0] + 1, 
                                    player_object_position[1]):
                # Print out an error for the invalid move.
                print_go_error()
                break
            # Call the go command.
            go(1, 0)
            # Increment the counter.
            i = i + 1
    # Check if the second substring is equal to "back".
    elif direction == "back" or direction == "down" or direction == "south":
        # Variable used as a counter.
        i = 0
        while i < int(length):
            # Break out of the loop if the destination coordinates are occupied.
            if position_is_wall(player_object_position[0], 
                                    player_object_position[1] + 1):
                # Print out an error for the invalid move.
                print_go_error()
                break
            # Call the go command.
            go(0, 1)
            # Increment the counter.
            i = i + 1
    # Check if the second substring is equal to "left".
    elif direction == "left" or direction == "west":
        # Variable used as a counter.
        i = 0
        while i < int(length):
            # Break out of the loop if the destination coordinates are occupied.
            if position_is_wall(player_object_position[0] - 1, 
                                    player_object_position[1]):
                # Print out an error for the invalid move.
                print_go_error()
                break
            # Call the go command.
            go(-1, 0)
            # Increment the counter.
            i = i + 1
    # Incorrect direction substring.
    else:
        print_input_error()

# Function to use the marker.
def use_marker():
    global marked_tile_list
    global player_used_marker

    # Change the value of player_used_marker to True. It is used in the 
    # draw_screen function to determine when to start drawing the marker.
    player_used_marker = True

    # Set x and y equal to the current player character object position.
    x = player_object_position[0]
    y = player_object_position[1]

    # Clear the contents of the marked_tile_list.
    marked_tile_list = []

    # Add the tile coordinates to the marked_tile_list.
    if grid[y][x] == 0:
        marked_tile_list.append((x, y))
    if grid[y - 1][x - 1] == 0:
        marked_tile_list.append((x - 1, y - 1))
    if grid[y - 1][x] == 0:
        marked_tile_list.append((x, y - 1))
    if grid[y - 1][x + 1] == 0:
        marked_tile_list.append((x + 1, y - 1))
    if grid[y][x - 1] == 0:
        marked_tile_list.append((x - 1, y))
    if grid[y][x + 1] == 0:
        marked_tile_list.append((x + 1, y))
    if grid[y + 1][x - 1] == 0:
        marked_tile_list.append((x - 1, y + 1))
    if grid[y + 1][x] == 0:
        marked_tile_list.append((x, y + 1))
    if grid[y + 1][x + 1] == 0:
        marked_tile_list.append((x + 1, y + 1))

    # Call the function to move the enemies.
    move_simple_enemy()
    move_smart_enemy()

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
        print "Output: You have picked up the key!" \
              "\nI hear they make doors easier to open..."
        # Set the key object position to [0, 0].
        key_object_position[0] = 0
        key_object_position[1] = 0
        # Set player_grabbed_key equal to True.
        player_grabbed_key = True
    else:
        # Inform the player that the key is not within their reach.
        print "Output: The key is not within reach..." \
              "\nTry looking for something key-shaped."

    # Call the function to move the enemies.
    move_simple_enemy()
    move_smart_enemy()

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
            print "Output: You have already unlocked the chest, " \
                  "no need to be redundant."
        else:
            if user_input_combination == chest_combination:
                # Inform the player that they have unlocked up the chest.
                print "Output: You have unlocked the chest!" \
                      "\nNow maybe it can be opened..."
                # Set player_unlocked_chest equal to True.
                player_unlocked_chest = True
            else:
                # Inform the player that the combination is incorrect.
                print "Output: incorrect combination..."
    else:
        # Inform the player that the chest is not within their reach.
        print "Output: The chest is not within reach..." \
              "\nTry looking for something chest-shaped."

    # Call the function to move the enemies.
    move_simple_enemy()
    move_smart_enemy()

# Function to open the chest.
def open_chest():
    # Needed to change their properties.
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
            print "Output: You have already opened the chest, " \
                  "no need to be redundant."
        else:
            if player_unlocked_chest:
                # Inform the player that they have opened up the chest.
                print "Output: You have opened the chest!" \
                      "\nNow maybe the door can be opened..."

                # Set player_grabbed_chest equal to True.
                player_opened_chest = True
            else:
                # Inform the player that the combination is incorrect.
                print "Output: You must enter the correct combination to " \
                      "unlock the chest before you can open it."
    else:
        # Inform the player that the chest is not within their reach.
        print "Output: The chest is not within reach..." \
              "\nTry looking for something chest-shaped."

    # Call the function to move the enemies.
    move_simple_enemy()
    move_smart_enemy()

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
            print "You have already unlocked the door, maybe now it will open."
        elif player_grabbed_key:
            # Inform the player that they have unlocked the door.
            print "Output: You have unlocked the door!" \
                  "\nThe key wasn't so useless after all!"
            # Set player_used_key equal to True.
            player_used_key = True
        else:
            # Inform the player that they need the key to unlocked the door.
            print "Output: This door is locked. " \
                  "\nMaybe a key could unlock it..."
    else:
        # Inform the player that the door is not within their reach.
        print "Output: The door is not within reach..." \
              "\nTry looking for something door-shaped."

    # Call the function to move the enemies.
    move_simple_enemy()
    move_smart_enemy()

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
            print "Output: You haven't opened the chest. " \
                  "\nMaybe you should open it first."
        elif player_grabbed_key and player_opened_chest:
            # Inform the player that they need to use the 
            # key before they can open the door.
            print "Output: A key can sometimes be " \
                  "used to open doors."
        elif player_grabbed_key and not player_opened_chest:
            # Inform the player that they need to use the 
            # key before they can open the door.
            print "Output: There's a chest somewhere around here. " \
                  "\nMaybe it will be worth your while to open it first."
        elif not player_grabbed_key and player_opened_chest:
            # Inform the player that they need to use the 
            # key before they can open the door.
            print "Output: Congrats, you found the door. " \
                  "\nMaybe you should use the key."
        else:
            # Inform the player that they need to find 
            # the key and chest before they can open the door.
            print "Output: There's a key and a chest somewhere around here..." \
                  "\nMaybe you could go find them and then come back."
    else:
        # Inform the player that the door is not within their reach.
        print "Output: The door is not within reach..." \
              "\nTry looking for something door-shaped."

    # Call the function to move the enemies.
    move_simple_enemy()
    move_smart_enemy()

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

 

################################################################################
# Enemies
################################################################################

# Function to move the simple enemy object in a random direction.
def move_simple_enemy():    
    global simple_enemy_object_position

    # Call the function to reset the game if the player character 
    # is in the same coordinate as either enemy.
    if player_object_position == simple_enemy_object_position \
        or player_object_position == smart_enemy_object_position:
        # Print out an message informing the user that they lost.
        print "Output: The enemy grabbed you! Your stuff was confiscated "
        print "\tand you were returned to where you started. "
        print "\tYou will have to try your luck again...\n"
        # Reset the locations of all objects and state conditions.
        reset_object_positions_and_state_conditions()

    # Set x and y equal to the simple enemy object position.
    x = simple_enemy_object_position[0]
    y = simple_enemy_object_position[1]

    direction = random.randint(1, 4)

    # Set nx and ny equal to the new simple enemy object position.
    if direction == 1:
        # Move the simple enemy object position one coordinate North.
        nx = x
        ny = y - 1
    elif direction == 2:
        # Move the simple enemy object position one coordinate East.
        nx = x + 1
        ny = y
    elif direction == 3:
        # Move the simple enemy object position one coordinate South.
        nx = x
        ny = y + 1
    elif direction == 4:
        # Move the simple enemy object position one coordinate West.
        nx = x - 1
        ny = y

    # Change the simple enemy object position if the new position 
    # is in the game window and the cell is not pre-occupied.
    if (nx > 0 and nx < len(grid) and ny > 0 and ny < len(grid) and \
        grid[ny][nx]):
            simple_enemy_object_position[0] = nx
            simple_enemy_object_position[1] = ny

    # Call the function to reset the game if the player character 
    # is in the same coordinate as either enemy.
    if player_object_position == simple_enemy_object_position \
        or player_object_position == smart_enemy_object_position:
        # Print out an message informing the user that they lost.
        print "Output: The enemy grabbed you! Your stuff was confiscated "
        print "\tand you were returned to where you started. "
        print "\tYou will have to try your luck again...\n"
        # Reset the locations of all objects and state conditions.
        reset_object_positions_and_state_conditions()

# Function to move the smart enemy in a direction towards the player.
def move_smart_enemy():
    global smart_enemy_object_position

    # Call the function to reset the game if the player character 
    # is in the same coordinate as either enemy.
    if player_object_position == simple_enemy_object_position \
        or player_object_position == smart_enemy_object_position:
        # Print out an message informing the user that they lost.
        print "Output: The enemy grabbed you! Your stuff was confiscated "
        print "\tand you were returned to where you started. "
        print "\tYou will have to try your luck again...\n"
        # Reset the locations of all objects and state conditions.
        reset_object_positions_and_state_conditions()
    
    # Create a test grid to use with the A* algorithm.
    test_grid = GridWithWeights(15, 15)

    # Traverse the grid to grab all of the wall locations.
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            if grid[column][row] == 0:
                wall = (row, column)
                # Add the wall locations to the graph's list of walls.
                test_grid.walls.append(wall)

    # The location of the smart enemy.
    start = (smart_enemy_object_position[0], smart_enemy_object_position[1])
    # The location of the player.
    goal = (player_object_position[0], player_object_position[1])

    # Get dictionaries mapping positions using the A* search algorithm.
    came_from, cost_so_far = a_star_search(test_grid, start, goal)

    # Loop through cost_so_far until we find the next position to go to.
    for coordinates, cost in cost_so_far.iteritems():
        if cost == 1:
            nx, ny = coordinates
            break

    #print cost_so_far
        
    '''# The current location of the smart enemy.
    start = (smart_enemy_object_position[0], smart_enemy_object_position[1])
    # The current location of the player.
    goal = (player_object_position[0], player_object_position[1])

    # The DFS calling.
    dict = {}
    depth_first_search(start, goal, grid, dict)
    goal_path_list = draw_hierarchy(dict, goal)

    # The BFS calling.
    dict1 = {}
    breath_first_search(start, goal, grid, dict1)
    goal_path_list1 = draw_hierarchy(dict1, goal)

    if len(goal_path_list) == 1:
        next_coordinates = goal_path_list[0]
    else:
        next_coordinates = goal_path_list[-2]'''

    # Change the simple enemy object position if the new position 
    # is in the game window and the cell is not pre-occupied.
    if (nx > 0 and nx < len(grid) and ny > 0 and ny < len(grid) and \
        grid[ny][nx]):
            smart_enemy_object_position[0] = nx
            smart_enemy_object_position[1] = ny

    # Call the function to reset the game if the player character 
    # is in the same coordinate as either enemy.
    if player_object_position == simple_enemy_object_position \
        or player_object_position == smart_enemy_object_position:
        # Print out an message informing the user that they lost.
        print "Output: The enemy grabbed you! Your stuff was confiscated "
        print "\tand you were returned to where you started. "
        print "\tYou will have to try your luck again...\n"
        # Reset the locations of all objects and state conditions.
        reset_object_positions_and_state_conditions()

    '''# Variable that store the enemy location.
    smart_enemy_location = (smart_enemy_object_position[0], 
                                smart_enemy_object_position[1])
    # Variable that store the current location.
    player_location = (player_object_position[0], 
                                player_object_position[1])

    # Call the a_star_search algorithm to get the next position to move to.
    test_grid = GridWithWeights(15, 15) # Test grid.

    # Traverse the grid to grab all of the wall locations
    for row in xrange(len(grid)):
        for column in xrange(len(grid[0])):
            if grid[column][row] == 0:
                wall = (row, column)
                # Add the wall locations to the graph's list of walls
                test_grid.walls.append(wall)

    # The location of the smart enemy.
    start = (smart_enemy_object_position[0], smart_enemy_object_position[1])
    # The position of the player.
    goal = (player_object_position[0], player_object_position[1])

    came_from, cost_so_far = a_star_search(test_grid, start, goal)

    # Execute search algorithm 1.
    A1, cost_so_far = a_star_search(grid, smart_enemy_location, player_location)

    # Execute search algorithm 2.
    A2, cost_so_far = a_star_search(grid, smart_enemy_location, player_location)

    # Execute search algorithm 3.
    A3, cost_so_far = a_star_search(grid, smart_enemy_location, player_location)

    # Compare the 3 search algorithms for equality.
    if A1 == A2:
        if A2 == A3:
            # All search algorithms match.
            smart_enemy_object_position[0] = A1[0]
            smart_enemy_object_position[1] = A1[1]
        elif A1 != A3:
            # A3 does not match.
            smart_enemy_object_position[0] = A1[0]
            smart_enemy_object_position[1] = A1[1]
        else:
            # Logic error, re-spawn enemy.
            respawn_smart_enemy()
    elif A1 == A3:
        # A2 does not match.
        smart_enemy_object_position[0] = A1[0]
        smart_enemy_object_position[1] = A1[1]
    elif A2 == A3:
        # A1 does not match.
        smart_enemy_object_position[0] = A2[0]
        smart_enemy_object_position[1] = A2[1]
    else:
        # No two algorithms match, re-spawn enemy.
        respawn_smart_enemy()'''

# Function to reset the smart enemy object position.
def respawn_smart_enemy():
    global smart_enemy_object_position

    # Reset the smart enemy object's position.
    smart_enemy_object_position = [object_position_dictionary['smart enemy'][0],
    object_position_dictionary['smart enemy'][1]]



################################################################################
# Path-finding (A* algorithm, Breath-first search, and Depth-first search)
################################################################################

# Class used to make a graph object for the algorithm.
class SquareGrid:
    # Initialize the parameters.
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    # Function to determine if the neighbors are in bounds.
    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    # Function to determine if an element is valid.
    def passable(self, id):
        return id not in self.walls

    # Function to find the neighbors.
    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0: results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

# Subclass used to access the cost function.
class GridWithWeights(SquareGrid, object):
    # Function to...
    def __init__(self, width, height):
        super(GridWithWeights, self).__init__(width, height)
        self.weights = {}

    # Function used to calculate the cost to move from from_node to to_node.
    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

# Class that associates each item with a priority.
class PriorityQueue:
    # Function to...
    def __init__(self):
        self.elements = []

    # Function to...
    def empty(self):
        return len(self.elements) == 0
    
    # Function to...
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    # Function to...
    def get(self):
        return heapq.heappop(self.elements)[1]

# Function used to..
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

# Function that implements the A* algorithm.
# Parameters: 
#   1) graph - the graph we will search.
#   2) start - the starting location (character location at start).
#   3) goal - the ending location (door location at start).
def a_star_search(graph, start, goal):
    # Initialize variables.
    frontier = PriorityQueue() # Expanding queue that keeps track of the path.
    came_from = {} # Dictionary that maps the coordinates to the cost.
    cost_so_far = {} # Dictionary that maps the coordinates to the cost.

    # Set variables.
    frontier.put(start, 0)
    came_from[start] = None
    cost_so_far[start] = 0

    # Loop until the frontier queue is empty.
    while not frontier.empty():
        # Get the current element of the queue.
        current = frontier.get()

        # Break if the current element is the goal.
        if current == goal:
            break

        # Iterate through the neighbors in the graph at the current location.
        for next in graph.neighbors(current):
            # Assign the new cost.
            new_cost = cost_so_far[current] + graph.cost(current, next)

            # If the current element is not in the current dictionary
            # or the new cost is less than the current cost, then...
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                # The cost of the next element is the current cost.
                cost_so_far[next] = new_cost
                # Set the priority equal to the sum of the new cost and 
                # the heuristic of the goal and next locations.
                priority = new_cost + heuristic(goal, next)
                # Put the next element in the queue.
                frontier.put(next, priority)
                # Set the dictionary element to the current element.
                came_from[next] = current

    # Return came_from and cost_so_far.
    return came_from, cost_so_far



# Class used for...
class Cls(object):
    def __repr__(self):
        os.system('cls')
        return ''

# Function to check the validity of a point before it is added as a neighbor.
def is_valid(point, grid):
    # Check if the point of the grid is out of range or is a wall.
    if (point[0] > 14) or (point [1] > 14)  or (grid[point[0]][point[1]] == 0):
        return False
    else:
        return True

# Function to add all the neighbors of the selected point to the stack (list).
def add_neighbours(point, neighbours_list, visited_list, grid, dict):
    # Return if the point is null.
    if point == []:
        return

    # Define the neighbor points.
    neighbor_point_1 = [point[0] + 1, point[1]]
    neighbor_point_2 = [point[0] - 1, point[1]]
    neighbor_point_3 = [point[0], point[1] + 1]
    neighbor_point_4 = [point[0], point[1] - 1]

    # Check the validity of each neighbor and then add them to the stack (list).
    if is_valid(neighbor_point_4, grid):
        if not visited_list.__contains__(neighbor_point_4):
            neighbours_list.append(neighbor_point_4)
            add_to_dictionary(dict,point,neighbor_point_4)
    if is_valid(neighbor_point_3, grid):
        if not visited_list.__contains__(neighbor_point_3):
            neighbours_list.append(neighbor_point_3)
            add_to_dictionary(dict, point, neighbor_point_3)
    if is_valid(neighbor_point_2, grid):
        if not visited_list.__contains__(neighbor_point_2):
            neighbours_list.append(neighbor_point_2)
            add_to_dictionary(dict, point, neighbor_point_2)
    if is_valid(neighbor_point_1, grid):
        if not visited_list.__contains__(neighbor_point_1):
            neighbours_list.append(neighbor_point_1)
            add_to_dictionary(dict, point, neighbor_point_1)
    visited_list.append(point)

# Dictionary used to print the success path after it has been generated.
def add_to_dictionary(dictionary,parent,child):
    p_l = map(str, parent)
    c_l = map(str,child)
    p_l = ','.join(p_l)
    c_l = ','.join(c_l)
    dictionary[c_l] = p_l

# Function that implements the main logic of the DFS algorithm.
def depth_first_search(start_point, end_point, graph, dict):
    # List of neighbors.
    neighbours_list = [[]]
    # List of visited nodes.
    visited_list = [[]]

    # Add neighbors after they have been validated.
    add_neighbours(start_point, neighbours_list, visited_list, graph, dict)
    # Remove...
    neighbours_list.remove([])
    # Remove...
    visited_list.remove([])

    # Loop until the desired location is not found.
    while (not visited_list.__contains__(end_point)):
        # Break if the length of neighbors_list is equal to 0.
        if len(neighbours_list) == 0:
            break
        # Set the value of point equal to the top element of the stack.
        point = neighbours_list.pop()
        add_neighbours(point, neighbours_list, visited_list, graph, dict)

# Function that contains the main logic of the BFS algorithm.
def breath_first_search(start_point, end_point, graph, dict):
    neighbours_list = [[]]
    visited_list = [[]]
    add_neighbours(start_point, neighbours_list, visited_list, graph, dict)
    neighbours_list.remove([])
    visited_list.remove([])

    # Loop until the desired location is not found.
    while (not visited_list.__contains__(end_point)):
        if len(neighbours_list) == 0:
            break
        old_list = neighbours_list
        neighbours_list = [[]]
        neighbours_list.remove([])
        # Here, all of the children are traversed level-by-level.
        for a in old_list:
            add_neighbours(a, neighbours_list, visited_list, graph, dict)

# Function to add the locations at the end to the list (stack).
def draw_hierarchy(dict, point):
    list = []
    p_l = map(str, point)
    p_l = ','.join(p_l)
    list.append(p_l)

    # Using the dictionary the success path is added to the stack.
    for a in range(len(dict)):
        try:
            if list.__contains__(dict[p_l]):
                continue
            list.append(dict[p_l])
            p_l = dict[p_l]
        except:
            break
    return list

'''# Function that uses both searching algorithms to find all available paths.
def perform_search():
    # The starting location of the player.
    start = (player_object_position[1], player_object_position[0])
    # The position of the door, or the exit condition.
    goal = (door_object_position[1], door_object_position[0])
    # The position of the key.
    key = (key_object_position[1], key_object_position[0])
    # The position of the chest.
    chest = (chest_object_position[1], chest_object_position[0])

    # The DFS calling.
    dict = {}
    depth_first_search(start, key, grid, dict)
    key_path_list = draw_hierarchy(dict, key)
    depth_first_search(key, chest, grid, dict)
    chest_path_list = draw_hierarchy(dict, chest)
    depth_first_search(chest, goal, grid, dict)
    goal_path_list = draw_hierarchy(dict, goal)

    # The BFS calling.
    dict1 = {}
    breath_first_search(start, key, grid, dict1)
    key_path_list1 = draw_hierarchy(dict1, key)
    breath_first_search(key, chest, grid, dict)
    chest_path_list1 = draw_hierarchy(dict1, chest)
    breath_first_search(chest, goal, grid, dict1)
    goal_path_list1 = draw_hierarchy(dict1, goal)'''



################################################################################
# Start
################################################################################
# Executes the main function.
if __name__ == "__main__":
    # Manage the log files.
    manage_log_files()
    # Open the log file.
    open_log_file()
    # Call function main.
    main()
    # Close the log file.
    close_log_file()
    # Exit the console window.
    pygame.quit()
