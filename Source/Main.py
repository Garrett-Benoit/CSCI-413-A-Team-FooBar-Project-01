"""
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
"""

################################################################################
# Imports
################################################################################

import os
import sys
import math
import pydoc
import inspect
import pygame
import pygame.mixer
from pygame.locals import *
import sgc
from sgc.locals import *
import random
import time
import heapq
import ast
import json
import firebase
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from firebase import jsonutil

################################################################################
# Set up the sound system
################################################################################

# Iinitialize the mixer
pygame.mixer.init()

# Load sounds and set volumes
background_sound = pygame.mixer.Sound("Sounds/background_sound.wav")
background_sound.set_volume(0.2)
go_sound = pygame.mixer.Sound("Sounds/go_sound.wav")
go_sound.set_volume(0.3)
pain_sound = pygame.mixer.Sound("Sounds/pain_sound.wav")
pain_sound.set_volume(0.5)
die_sound = pygame.mixer.Sound("Sounds/die_sound.wav")
die_sound.set_volume(1)
game_over_sound = pygame.mixer.Sound("Sounds/game_over_sound.wav")
game_over_sound.set_volume(1)
grab_key_sound = pygame.mixer.Sound("Sounds/grab_key_sound.wav")
grab_key_sound.set_volume(0.8)
open_chest_sound = pygame.mixer.Sound("Sounds/open_chest_sound.wav")
open_chest_sound.set_volume(0.8)
open_door_sound = pygame.mixer.Sound("Sounds/open_door_sound.wav")
open_door_sound.set_volume(0.8)
treasure_sound = pygame.mixer.Sound("Sounds/treasure_sound.wav")
treasure_sound.set_volume(0.8)
unlock_door_sound = pygame.mixer.Sound("Sounds/unlock_door_sound.wav")
unlock_door_sound.set_volume(1)
use_combo_sound = pygame.mixer.Sound("Sounds/use_combo_sound.wav")
use_combo_sound.set_volume(1)
use_marker_sound = pygame.mixer.Sound("Sounds/use_marker_sound.wav")
use_marker_sound.set_volume(1)


################################################################################
# Initialization
################################################################################

# Get the address to the firebase server which stores information for each user.
firebase = firebase.FirebaseApplication(
    'https://team-foobar-maze-generator.firebaseio.com/', None)
# Key used in encrypting the database information.
key_database_lower = 'abcdefghijklmnopqrstuvwxyz'
key_database_upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
key_database_digit = '0123456789'
# Key value for the Caesar Cipher encryption algorithm.
key_caesar_cipher = 5
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

cell_margin = 5  # Pre-defined space between cells.
cell_colors = (255, 255, 255), (0, 0, 0)  # RBG values representing cell colors.
player_object = "@"  # Symbol representing the player character.
player_object_color = (255, 255, 255)  # Color of the player character.
player_object_position = [0, 0]  # Position of the player character.
chest_object_closed = "C"  # Symbol representing the closed chest.
chest_object_opened = "O"  # Symbol representing the opened chest.
chest_object_color = (255, 255, 255)  # Color of the chest.
chest_object_position = [0, 0]  # Position of the chest.
key_object = "K"  # Symbol representing the key.
key_object_color = (255, 255, 255)  # Color of the key.
key_object_position = [0, 0]  # Position of the key.
door_object = "D"  # Symbol representing the door.
door_object_color = (255, 255, 255)  # Color of the door.
door_object_position = [0, 0]  # Position of the door.
simple_enemy_object = "E"  # Symbol representing the simple enemy.
simple_enemy_object_color = (255, 0, 0)  # Color of the simple enemy.
simple_enemy_object_position = [0, 0]  # Position of the simple enemy.
smart_enemy_object = "S"  # Symbol representing the smart enemy.
smart_enemy_object_color = (255, 0, 0)  # Color of the smart enemy.
smart_enemy_object_position = [0, 0]  # Position of the smart enemy.
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
object_size = 35  # Size of all objects drawn to the console window.
player_grabbed_key = False
player_used_key = False
player_used_marker = False
player_unlocked_chest = False
player_opened_chest = False
chest_combination = (chest_combination_1_object +
                     chest_combination_2_object +
                     chest_combination_3_object)
maze_is_valid = False
player_username = ""
player_is_authenticated = False
player_made_decision = False
player_game_moves = 0
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
input_box = sgc.InputBox((600, 35), label="",
                         default="Input here, output console...")
input_box.config(pos=(0, 599))
input_box.add(order=0)


################################################################################
# Main
################################################################################

def main():
    """
    Main function.
    """
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
    global marked_tile_list
    global player_used_marker
    global maze_is_valid
    global game_complete
    global exit_game
    global player_is_authenticated
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

    # Call the function to handle the login/signup of the player.
    # show_login_signup_screen()

    # Loop that determines manages the game states.
    while not exit_game:
        # Call the function to handle the player choices at the title screen.
        show_title_screen()

        # Cue the background music that will indefinitely loop
        background_sound.play(-1)

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
        marked_tile_list = []
        player_grabbed_key = False
        player_used_key = False
        player_used_marker = False
        player_unlocked_chest = False
        player_opened_chest = False
        maze_is_valid = False
        player_is_authenticated = False
        player_made_decision = False
        show_replay_1 = False
        show_replay_2 = False
        show_replay_3 = False
        start_new_game = False
        game_complete = False


################################################################################
# Game States
################################################################################

def show_login_signup_screen():
    """
    Function to handle player choices on the login screen.
    """
    global grid
    global player_username
    global player_is_authenticated
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
    pygame.display.set_caption("Login/Signup Screen")

    # Print authentication message to the user.
    print "\nLogin/Signup Screen: "
    print "\nPlease choose one of the following options:"
    print "1. login"
    print "2. signup"
    print "3. exit"

    i = 0  # Variable used as a counter for the following loop.
    login_attempt = False  # Variable used to determine if the user chose to login.
    signup_attempt = False  # Variable used to determine if the user chose to signup.
    temp_username = ""  # Variable used to store the username entered by the user.
    temp_password = ""  # Variable used to store the password entered by the user.
    temp_email = ""  # Variable used to store the email entered by the user.

    # Continue running until the player chooses
    # a valid option or closes the window.
    while player_is_authenticated == False:
        # Iterate through all of the events gathered from pygame.
        for event in pygame.event.get():
            sgc.event(event)
            if event.type == GUI:
                # Print user input string to the output console window.
                input_string = event.text
                if login_attempt and i == 2:
                    print_input("********")
                elif signup_attempt and i == 3:
                    print_input("********")
                else:
                    print_input(input_string)

                if i == 0:
                    if input_string == "login":
                        # .
                        login_attempt = True
                    elif input_string == "signup":
                        # .
                        signup_attempt = True
                    elif input_string == "exit":
                        # Exit the game if user chooses to.
                        exit_game = True
                        player_is_authenticated = True
                        player_made_decision = True
                    elif input_string == "":
                        # Print error message if user input is empty.
                        print "Output: Please enter a command."
                    else:
                        # Not even close to a valid command or contains some
                        # form of misspelling or incorrect input
                        # (numbers, special characters, etc.).
                        print "Output: Please enter a valid command."
                elif i == 1:
                    # Store the entered username.
                    temp_username = input_string
                elif i == 2:
                    if login_attempt == True:
                        # Store the entered password.
                        temp_password = input_string
                    elif signup_attempt == True:
                        # Store the entered email address.
                        temp_email = input_string
                elif i == 3:
                    # Store the entered password.
                    temp_password = input_string

                if login_attempt == True:
                    if i == 0:
                        # Print a message informing the
                        # user to input their username.
                        print "Output: Please enter your username: "

                        # Increment the value of i.
                        i = i + 1
                    elif i == 1:
                        # Print a message informing the
                        # user to input their password.
                        print "Output: Please enter your password: "

                        # Increment the value of i.
                        i = i + 1
                    elif i == 2:
                        # Get the encrypted username from the server.
                        result = firebase.get('/users', temp_username)

                        # Determine if the username exists on the server.
                        if result != None:
                            # Get the password from the server and decrypt it.
                            decrypted_password = database_decrypt(
                                key_caesar_cipher, result['password'])

                            # Determine if the passwords match.
                            if temp_password == decrypted_password:
                                # The player has been successfully authenticated.
                                player_is_authenticated = True

                                # Set player_username to logged in user
                                player_username = temp_username
                                save_replays()
                                # tempfunction()

                                # Print out a message informing the user that
                                # they have been successfully logged in.
                                print "Output: Authentication successful.\n" \
                                      + "\tYou have been successfully logged in."

                                # Print out the top moves from the leader board.
                                update_top10(0)

                                # Print new lines for spacing.
                                print "\n\n"
                            # The password does not match the username.
                            else:
                                print "Output: Authentication Error." \
                                      + " Incorrect password."
                        # The username does not exist.
                        else:
                            print "Output: Authentication Error." \
                                  + " Incorrect username."

                        # Reset values and variables used in the
                        # loop and print out an authentication
                        # message if the player is not authenticated.
                        if player_is_authenticated == False:
                            # Reset the values of variables used in the loop.
                            i = 0
                            login_attempt = False
                            signup_attempt = False
                            temp_username = ""
                            temp_password = ""
                            temp_email = ""

                            # Print new lines for spacing.
                            print "\n\n"

                            # Print authentication message to the user.
                            print "\nLogin/Signup Screen: "
                            print "\nPlease choose one of the following options:"
                            print "1. login"
                            print "2. signup"
                            print "3. exit"
                elif signup_attempt == True:
                    if i == 0:
                        # Print a message informing the
                        # user to input a username.
                        print "Output: Please enter a username: "

                        # Increment the value of i.
                        i = i + 1
                    elif i == 1:
                        # Print a message informing the
                        # user to input an email address.
                        print "Output: Please enter an email address: "

                        # Increment the value of i.
                        i = i + 1
                    elif i == 2:
                        # Print a message informing the
                        # user to input a password.
                        print "Output: Please enter a password: "

                        # Increment the value of i.
                        i = i + 1
                    elif i == 3:
                        # Determine if the username exists on the server.
                        if (firebase.get('/users', temp_username)) == None:

                            # If the password returns a valid input.
                            if password_check(temp_password):

                                # Encrypt the entered password before storing.
                                encrypted_password = database_encrypt(
                                    key_caesar_cipher, temp_password)

                                # Create the account if it does not already exist.
                                if firebase.put('/users/', temp_username,
                                                {'email': temp_email,
                                                 'password': encrypted_password}):
                                    # The player has been successfully authenticated.
                                    player_is_authenticated = True

                                    # Set player_username to logged in user
                                    player_username = temp_username
                                    save_replays()
                                    # tempfunction()

                                    # Print out a message informing the user
                                    # that they have successfully signed up.
                                    print "Output: Authentication successful.\n" \
                                          + "\tYou have successfully signed up."

                                    # Print new lines for spacing.
                                    print "\n\n"
                                # The account already exists.
                                else:
                                    print "Output: Authentication Error." \
                                          + " Existing account detected."

                        # The username already exists.
                        else:
                            print "Output: Authentication Error." \
                                  + " Existing username detected."

                        # Reset values and variables used in the
                        # loop and print out an authentication
                        # message if the player is not authenticated.
                        if player_is_authenticated == False:
                            # Reset the values of variables used in the loop.
                            i = 0
                            login_attempt = False
                            signup_attempt = False
                            temp_username = ""
                            temp_password = ""
                            temp_email = ""

                            # Print new lines for spacing.
                            print "\n\n"

                            # Print authentication message to the user.
                            print "\nLogin/Signup Screen: "
                            print "\nPlease choose one of the following options:"
                            print "1. login"
                            print "2. signup"
                            print "3. exit"

                # Clear the contents of the InputBox if it is clicked on.
                if event.widget is input_box:
                    clear()

        # Clear the contents of the screen.
        screen.fill((0, 0, 0))
        # Call the function to draw the maze and the objects inside.
        draw_screen(screen)
        # Update the InputText widget.
        sgc.update(1)
        # Update the console window to show changes.
        pygame.display.update()


def password_check(password_input):
    # Character counters
    """
    Function to check password for valid input
    :param password_input: input password to check validity of
    :return: help strings for invalid password or valid for good password
    """
    lower_case_letters_count = 0
    upper_case_letters_count = 0
    numbers_count = 0

    # Check if password is 8 characters in length
    if len(password_input) < 8:
        print "Password must be at least 8 characters long."
    else:
        # Password validity variables
        valid_upper = False
        valid_lower = False
        valid_digit = False

        # Loop through each character and check for validity.
        for character in password_input:
            if character.isdigit():
                numbers_count += 1
            elif character.islower():
                lower_case_letters_count += 1
                print lower_case_letters_count
            elif character.isupper():
                upper_case_letters_count += 1

        # Check for lower case count
        if lower_case_letters_count > 0:
            valid_lower = True
        else:
            print "No lower case letters in password"

        # Check for upper case count
        if upper_case_letters_count > 0:
            valid_upper = True
        else:
            print "No upper case letters in password"

        # Check for digit count
        if numbers_count > 0:
            valid_digit = True
        else:
            print "No numbers in password"

        # If all counts are valid
        if valid_upper & valid_lower & valid_digit:
            print "Good password"
            print "Lower case count: " + str(lower_case_letters_count)
            print "Upper case count: " + str(upper_case_letters_count)
            print "Number count: " + str(numbers_count)
            return True


def update_top10(new_move_value):
    # Print out the top 10 moves of the leaderboard.
    print "\nTop 10 Moves Leaderboard: "

    # Get the top moves from the leader board.
    leaderboard_moves = firebase.get('/leaderboard', None)

    if new_move_value != 0:
        leaderboard_moves[player_username] = new_move_value

    sorted_items = sorted(leaderboard_moves, key=lambda x: leaderboard_moves[x])

    for index, value in enumerate(sorted_items):
        if index < 10:
            print ("#") + str(index + 1) , ("{} : {}".format(value, leaderboard_moves[value]))
            firebase.put('/leaderboard', value, leaderboard_moves[value])

def save_replays():
    """
    Function to get the 3 most recent replays and save them
    both locally in game files and remotely on Firebase.
    """

    # Variable for timestamp comparison.
    timestamps = []
    local_replays = []
    local_replay_values = []

    # Fetch replay 1 from the local game files.
    open_chosen_replay_file(1)
    if chosen_replay_file != None:
        if not chosen_replay_file.closed:
            replay1_name = str(chosen_replay_filename[:-4])
            replay1 = chosen_replay_file.read()
            if (replay1_name != None) and (replay1 != None):
                local_replays.append(replay1_name)
                local_replay_values.append(replay1)

        close_chosen_replay_file()

    # Fetch replay 2 from the local game files.
    open_chosen_replay_file(2)
    if chosen_replay_file != None:
        if not chosen_replay_file.closed:
            replay2_name = str(chosen_replay_filename[:-4])
            replay2 = chosen_replay_file.read()

            if (replay2_name != None) and (replay2 != None):
                local_replays.append(replay2_name)
                local_replay_values.append(replay2)

        close_chosen_replay_file()

    # Fetch replay 3 from the local game files.
    open_chosen_replay_file(3)
    if chosen_replay_file != None:
        if not chosen_replay_file.closed:
            replay3_name = str(chosen_replay_filename[:-4])
            replay3 = chosen_replay_file.read()

            if (replay3_name != None) and (replay3 != None):
                local_replays.append(replay3_name)
                local_replay_values.append(replay3)

        close_chosen_replay_file()

    # Fetch replays from Firebase.
    firebase_replays = firebase.get('/replays/' + player_username, None)

    # Combine local and remote replays into one array.
    if firebase_replays != None:
        for key, value in firebase_replays.iteritems():
            local_replays.append(key)
            local_replay_values.append(value)

    # Iterate through all 6 replays and parse the timestamp out.
    for index, item in enumerate(local_replays):
        if isinstance(local_replays[index], str):
            timestamps.append(int(filter(str.isdigit, local_replays[index])))
        elif isinstance(local_replays[index], unicode):
            timestamps.append(int(filter(unicode.isdigit, local_replays[index])))

    # Sort the replays in order.
    sorted_timestamps = sorted(timestamps, reverse = True)
    sorted_replays = sorted(local_replays, reverse = True)
    sorted_replay_values = sorted(local_replay_values, reverse = True)

    # Iterate through the timestamps and remove duplicates.
    for index, item in enumerate(sorted_timestamps):
        if (index + 1) < len(sorted_timestamps):
            if sorted_timestamps[index] == sorted_timestamps[index + 1]:
                sorted_timestamps.pop(index + 1)
                sorted_replays.pop(index + 1)
                sorted_replay_values.pop(index + 1)

    '''for index, timestamp in enumerate(sorted_timestamps):
        if index < 3:
            print sorted_replays[index]'''

    if len(sorted_replays) == 1:
        firebase.put('/replays/', player_username,
                     {sorted_replays[0]: sorted_replay_values[0]})
    elif len(sorted_replays) == 2:
        firebase.put('/replays/', player_username,
                     {sorted_replays[0]: sorted_replay_values[0],
                      sorted_replays[1]: sorted_replay_values[1]})
    elif len(sorted_replays) == 3:
        firebase.put('/replays/', player_username,
                     {sorted_replays[0]: sorted_replay_values[0],
                      sorted_replays[1]: sorted_replay_values[1],
                      sorted_replays[2]: sorted_replay_values[2]})
        ######Test Loop For Printing Results######


def show_title_screen():
    """
    Function to handle player choices on the title screen.
    """
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
                    print "Output: Please enter a valid command."

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


def open_new_game():
    """
    Function to start a new game.
    """
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

def print_introduction_message():
    """
    Function to print out an introduction message.
    """
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
    print "5. help (bring up a help prompt)"
    print "6. quit (back to title screen)"
    print "\nTo see this message again, enter the help command. Good luck!"


def help():
    """
    Function to print out directions and a list of commands.
    """
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
    print "5. help (bring up this help prompt)"
    print "6. quit (back to title screen)"


def print_input(input):
    """
    Function to get user input from the input text
    :param input: input to print
    """
    print "\nInput: " + input


def print_go_error():
    """
    Function to print error message for invalid go.
    """
    print "Output: Invalid move command..."


def print_input_error():
    """
    Function to print error message for invalid input.
    """
    print "Output: Invalid input. Command not recognized..."


def clear():
    """
    Function to clear user input from the InputText.
    """
    input_box.text = ""


################################################################################
# File Input/Output
################################################################################


def manage_log_files():
    """
    Function to manage the number of log files in the directory.
    """
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


def manage_replay_files():
    """
    Function to manage the number of replay files in the directory.
    """
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


def open_log_file():
    """
    Function to open the log file.
    """
    global log_file
    global log_filename

    # Open the log file in write mode.
    log_file = open(log_filename, "wb")


def open_replay_file():
    """
    Function to open the replay file.
    """
    global replay_file
    global replay_filename

    # Open the replay file in write mode.
    replay_file = open(replay_filename, "wb")


def open_chosen_replay_file(number):
    """
    Function to open the replay file chosen by the user.
    :param number: replay number to open
    """
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


def write_to_log_file(string):
    """
    Function to write to the log file.
    :param string: string to write log file
    """
    global log_file

    # Write the string to the log file.
    log_file.write(string + "\n")

    # Update the changes to the log file.
    log_file.flush()


def write_to_replay_file(string):
    """
    Function to write to the replay file.
    :param string: string to write to replay file
    """
    global replay_file
    global key_caesar_cipher
    global chosen_encryption_algorithm

    # Write the string to the replay file.
    # Encrypt string before writing to the replay file.
    if (chosen_encryption_algorithm == "1"):
        replay_file.write(caesar_cipher_encrypt(string, key_caesar_cipher) + "\n")
    else:
        replay_file.write(string + "\n")

    # Update the changes to the replay file.
    replay_file.flush()


def close_log_file():
    """
    Function to close the opened log file.
    """
    global log_file

    # Close the log file.
    log_file.close()


def close_replay_file():
    """
    Function to close the opened replay file.
    """
    global replay_file

    # Close the replay file.
    replay_file.close()


def close_chosen_replay_file():
    """
    Function to close the chosen replay file.
    """
    global chosen_replay_file

    # Close the chosen replay file.
    chosen_replay_file.close()


################################################################################
# ENCRYPTION ALGORITHMS
################################################################################


def database_encrypt(n, plaintext):
    #
    """
    Function to encrypt the database
    :param n:
    :param plaintext: text to encrypt
    :return: encrypted database
    """
    result = ''

    #
    for l in plaintext:
        # If character is lower case
        if l.islower():
            try:
                #
                i = (key_database_lower.index(l) + n) % 26
                #
                result += key_database_lower[i]
            #
            except ValueError:
                #
                result += l
        # If character is upper case
        elif l.isupper():
            try:
                #
                i = (key_database_upper.index(l) + n) % 26
                #
                result += key_database_upper[i]
            #
            except ValueError:
                #
                result += l
        # If character is a digit
        elif l.isdigit():
            try:
                #
                i = (key_database_digit.index(l) + n) % 10
                #
                result += key_database_digit[i]
            #
            except ValueError:
                #
                result += l
    #
    return result


def database_decrypt(n, ciphertext):
    #
    """
    Function to decrypt the database
    :param n:
    :param ciphertext: text to decrypt
    :return: decrypted database
    """
    result = ''

    #
    for l in ciphertext:
        # If character is lower case
        if l.islower():
            try:
                #
                i = (key_database_lower.index(l) - n) % 26
                #
                result += key_database_lower[i]
            #
            except ValueError:
                #
                result += l
        # If character is upper case
        elif l.isupper():
            try:
                #
                i = (key_database_upper.index(l) - n) % 26
                #
                result += key_database_upper[i]
            #
            except ValueError:
                #
                result += l
        # If character is a digit
        elif l.isdigit():
            try:
                #
                i = (key_database_digit.index(l) - n) % 10
                #
                result += key_database_digit[i]
            #
            except ValueError:
                #
                result += l
    #
    return result


# Give more descriptive names for all variables, keep to the formatting you see
# in this file, and add descriptive comments!
# The following code is in a poor state., clean it up!



#
a_ordinal = ord('a')
#
z_ordinal = ord('z')
#
chosen_encryption_algorithm = "1"


def caesar_cipher_encrypt(text, key):
    """
    Function that implements the Caesar Cipher encryption algorithm
    :param text: text to be encrypted
    :param key: encryption key applied to text
    :return: encrypted text
    """
    # Convert to ASCI representation.
    clist = [ord(x) for x in text]
    #
    cipher = list()

    #
    for x in clist:
        #
        if (x >= a_ordinal and x <= z_ordinal):
            # Shift the character.
            new_char = x + key

            # Shift character is more than last character, cycle back to A.
            if (new_char > z_ordinal):
                # Subtract 1 to avoid cases where z and a conflict.
                c = a_ordinal + (new_char - z_ordinal - 1)

                #
                cipher.append(chr(c))

            #
            else:
                #
                cipher.append(chr(new_char))
        #
        else:
            #
            cipher.append(chr(x))
    # Return...
    return ''.join(cipher)


def caesar_cipher_decrypt(text, key):
    # Why is this variable named differently than clist in the above function?
    # Do they provide different functionality?
    """
    Function to decrpyt the Caesar Cipher encrypted text.
    :param text: text to be decrypted
    :param key: decryption key applied to text
    :return: decrypted text
    """
    cipher = [ord(x) for x in text]

    # What the hell is a cleat?
    cleat_text = list()

    #
    for x in cipher:
        #
        if (x >= a_ordinal and x <= z_ordinal):
            #
            new_char = x - key

            #
            if (new_char < a_ordinal):
                #
                print("C: %d" % (a_ordinal - new_char))

                # Add 1 to adjust cycle again.
                c = z_ordinal - (a_ordinal - new_char) + 1

                #
                cleat_text.append(chr(c))
            else:
                #
                cleat_text.append(chr(new_char))
        else:
            #
            cleat_text.append(chr(x))
    #
    return ''.join(cleat_text)


#######################################
# AES Encryption (Complex encryption) #

class AES(object):
    # AES Functions for a single block

    # Valid key sizes
    key_size = dict(SIZE_128=16, SIZE_192=24, SIZE_256=32)

    # Rijndael S-box
    sbox = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
            0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
            0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
            0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
            0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
            0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
            0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
            0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
            0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
            0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
            0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
            0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
            0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
            0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
            0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
            0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
            0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
            0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
            0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
            0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
            0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
            0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
            0x54, 0xbb, 0x16]

    # Rijndael Inverted S-box
    rsbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
             0x9e, 0x81, 0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
             0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54,
             0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
             0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
             0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72, 0xf8,
             0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
             0x65, 0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
             0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab,
             0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
             0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
             0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91, 0x11, 0x41,
             0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
             0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
             0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d,
             0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
             0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
             0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
             0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 0x60,
             0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
             0x93, 0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
             0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b,
             0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
             0x21, 0x0c, 0x7d]

    def get_sbox_value(self, num):
        """
        Function to retrieve a given s-box value.
        :param num: index of s-box value
        :return: s-box value
        """
        return self.sbox[num]

    def get_sbox_invert(self, num):
        """
        Function to retrieve a given Inverted S-Box Value.
        :param num: index of inverted s-box value
        :return: inverted s-box value
        """
        return self.rsbox[num]

    def rotate(self, word):
        """
        Function to perform Rijndael's key schedule rotate operation
        :param word: word to be rotated
        :return: rotated word
        """
        return word[1:] + word[:1]

    # Rijndael Rcon
    Rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36,
            0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97,
            0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72,
            0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66,
            0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04,
            0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d,
            0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
            0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61,
            0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a,
            0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
            0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc,
            0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5,
            0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a,
            0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d,
            0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c,
            0xd8, 0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35,
            0x6a, 0xd4, 0xb3, 0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4,
            0xd3, 0xbd, 0x61, 0xc2, 0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc,
            0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb, 0x8d, 0x01, 0x02, 0x04, 0x08,
            0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a,
            0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3, 0x7d,
            0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2,
            0x9f, 0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74,
            0xe8, 0xcb]

    def get_rcon_value(self, num):
        """
        Function to retrieve a given Rcon Value
        :param num: index of Rcon value
        :return: Rcon value
        """
        return self.Rcon[num]

    def core(self, word, iteration):
        """
        Function to rotate a word and apply s-box substitution
        :param word: word to be modified
        :param iteration: loop variable
        :return: modified word
        """
        # Key schedule core
        # rotate the 32-bit word 8 bits to the left
        word = self.rotate(word)

        # apply S-Box substitution on all 4 parts of the 32-bit word
        for i in range(4):
            word[i] = self.get_sbox_value(word[i])

            # XOR the output of the rcon operation with i to the first part
            # (leftmost) only
            word[0] = word[0] ^ self.get_rcon_value(iteration)
            return word

    def expand_key(self, key, size, expanded_key_size):

        """
        Function to expand the key
        :param key: key to be expanded
        :param size: expansion size
        :param expanded_key_size: final size of the expanded key
        :return: expanded key
        """
        # Rijndael's key expansion
        # Current expanded key_size, in bytes
        current_size = 0
        rcon_iteration = 1
        expanded_key = [0] * expanded_key_size

        # Set the 16, 24, 32 bytes of the expanded key to the input key
        for j in range(size):
            expanded_key[j] = key[j]
        current_size += size

        while current_size < expanded_key_size:
            # Assign the previous 4 bytes to the temporary value t
            t = expanded_key[current_size - 4: current_size]

            # Every 16, 24, 32 bytes we apply the core schedule to t
            # and increment rcon_iteration afterwards
            if current_size % size == 0:
                t = self.core(t, rcon_iteration)
                rcon_iteration += 1

            # For 256-bit keys, we add an extra sbox to the calculation
            if size == self.key_size["SIZE_256"] and ((current_size % size) % 16):
                for l in range(4): t[l] = self.get_sbox_value(t[l])

            # We XOR t with the four-byte block 16, 24, 32 bytes before the new
            # expanded key. This becomes the next four bytes in the expanded key
            for m in range(4):
                expanded_key[current_size] = expanded_key[current_size - size] ^ \
                                             t[m]
                current_size += 1
        return expanded_key

    def add_round_key(self, state, round_key):
        """
        Function to add a round key
        :param state:
        :param round_key: key added to the state
        :return: state
        """
        # Adds (XORs) the round key to the state
        for i in range(16):
            state[i] ^= round_key[i]
        return state

    def create_round_key(self, expanded_key, round_key_pointer):
        """
        Function to create a round key from the given expanded key
        and the position within the expanded key.
        :param expanded_key: given expanded key
        :param round_key_pointer:
        :return: round key
        """
        round_key = [0] * 16
        for i in range(4):
            for j in range(4):
                round_key[j * 4 + i] = expanded_key[round_key_pointer + i * 4 + j]
        return round_key

    def galois_multiplication(self, a, b):
        """
        Function to perform Galois multiplication
        :param a: 8-bit character
        :param b: 8-bit character
        :return: product of a x b
        """
        p = 0
        for counter in range(8):
            if b & 1: p ^= a
            hi_bit_set = a & 0x80
            a <<= 1
            # keep a 8 bit
            a &= 0xFF
            if hi_bit_set:
                a ^= 0x1b
            b >>= 1
        return p

    #
    # substitute all the values from the state with the value in the SBox
    # using the state value as index for the SBox
    #
    def sub_bytes(self, state, is_inv):
        """
        Function to substitute all the values from the state
        with the value in the s-box using the state value
        as index for the s-box.
        :param state: given state
        :param is_inv: bool value to tell if it is inverted or not
        :return: state
        """
        if is_inv:
            getter = self.get_sbox_invert
        else:
            getter = self.get_sbox_value
        for i in range(16): state[i] = getter(state[i])
        return state

    def shift_rows(self, state, is_inv):
        """
        Function to iterate over the 4 rows and call shift_row() with that row
        :param state: state to be shifted
        :param is_inv: bool value to tell if it is inverted or not
        :return: shifted state
        """
        for i in range(4):
            state = self.shift_row(state, i * 4, i, is_inv)
        return state

    def shift_row(self, state, state_pointer, nbr, is_inv):
        """
        Function that shifts the row to the left by 1 each iteration
        :param state: state to be shifted
        :param state_pointer:
        :param nbr: number for loop variable
        :param is_inv: bool value to tell if it is inverted or not
        :return: shifted state
        """
        for i in range(nbr):
            if is_inv:
                state[state_pointer:state_pointer + 4] = \
                    state[state_pointer + 3:state_pointer + 4] + \
                    state[state_pointer:state_pointer + 3]
            else:
                state[state_pointer:state_pointer + 4] = \
                    state[state_pointer + 1:state_pointer + 4] + \
                    state[state_pointer:state_pointer + 1]
        return state

    def mix_columns(self, state, is_inv):
        """
        Function to perform Galois multiplication of the 4x4 matrix.
        :param state: state to mixed (multiplied)
        :param is_inv: bool value to tell if it is inverted or not
        :return: mixed state
        """
        # iterate over the 4 columns
        for i in range(4):
            # construct one column by slicing over the 4 rows
            column = state[i:i + 16:4]

            # apply the mix_column on one column
            column = self.mix_column(column, is_inv)

            # put the values back into the state
            state[i:i + 16:4] = column

        return state

    def mix_column(self, column, is_inv):
        """
        Function to perform galois multiplication of 1 column of the 4x4 matrix
        :param column: column to mix
        :param is_inv: bool value to tell if it is inverted or not
        :return: mixed column
        """
        if is_inv:
            mult = [14, 9, 13, 11]
        else:
            mult = [2, 1, 1, 3]
        cpy = list(column)
        g = self.galois_multiplication

        column[0] = g(cpy[0], mult[0]) ^ g(cpy[3], mult[1]) ^ \
                    g(cpy[2], mult[2]) ^ g(cpy[1], mult[3])
        column[1] = g(cpy[1], mult[0]) ^ g(cpy[0], mult[1]) ^ \
                    g(cpy[3], mult[2]) ^ g(cpy[2], mult[3])
        column[2] = g(cpy[2], mult[0]) ^ g(cpy[1], mult[1]) ^ \
                    g(cpy[0], mult[2]) ^ g(cpy[3], mult[3])
        column[3] = g(cpy[3], mult[0]) ^ g(cpy[2], mult[1]) ^ \
                    g(cpy[1], mult[2]) ^ g(cpy[0], mult[3])
        return column

    def aes_round(self, state, round_key):
        """
        Function that applies the 4 operations of the forward round in sequence.
        :param state: state to perform operations on
        :param round_key: round key added to the state
        :return: state with performed operations applied
        """
        state = self.sub_bytes(state, False)
        state = self.shift_rows(state, False)
        state = self.mix_columns(state, False)
        state = self.add_round_key(state, round_key)
        return state

    def aes_inv_round(self, state, round_key):
        """
        Function that applies the 4 operations of the inverse round in sequence.
        :param state: state to perform operations on
        :param round_key: round key added to the state
        :return: state with performed operations applied.
        """
        state = self.shift_rows(state, True)
        state = self.sub_bytes(state, True)
        state = self.add_round_key(state, round_key)
        state = self.mix_columns(state, True)
        return state

    def aes_main(self, state, expanded_key, nbr_rounds):
        """
        Function to perform the initial operations, the standard round,
        and the final operations of the forward aes, creating
        a round key for each round.
        :param state: state to be modified
        :param expanded_key: expanded key to apply to state
        :param nbr_rounds: number of rounds
        :return: modified state
        """
        state = self.add_round_key(state, self.create_round_key(expanded_key, 0))
        i = 1
        while i < nbr_rounds:
            state = self.aes_round(state,
                                   self.create_round_key(expanded_key, 16 * i))
            i += 1
        state = self.sub_bytes(state, False)
        state = self.shift_rows(state, False)
        state = self.add_round_key(state,
                                   self.create_round_key(expanded_key, 16 * nbr_rounds))
        return state

    def aes_inv_main(self, state, expanded_key, nbr_rounds):
        """
        Function to perform the initial operations, the standard round,
        and the final operations of the inverse aes, creating
        a round key for each round.
        :param state: state to be modified
        :param expanded_key: expanded key to apply to state
        :param nbr_rounds: number of rounds
        :return: modified state
        """
        state = self.add_round_key(state,
                                   self.create_round_key(expanded_key, 16 * nbr_rounds))
        i = nbr_rounds - 1
        while i > 0:
            state = self.aes_inv_round(state,
                                       self.create_round_key(expanded_key, 16 * i))
            i -= 1
        state = self.shift_rows(state, True)
        state = self.sub_bytes(state, True)
        state = self.add_round_key(state, self.create_round_key(expanded_key, 0))
        return state

    def encrypt(self, input, key, size):
        """
        Function that encrypts a 128 bit input block against the given key of size specified
        :param input: input string to encrypt
        :param key: encryption key
        :param size: size of the key
        :return: encrypted string
        """
        output = [0] * 16

        # the number of rounds
        nbr_rounds = 0

        # the 128 bit block to encode
        block = [0] * 16

        # set the number of rounds
        if size == self.key_size["SIZE_128"]:
            nbr_rounds = 10
        elif size == self.key_size["SIZE_192"]:
            nbr_rounds = 12
        elif size == self.key_size["SIZE_256"]:
            nbr_rounds = 14
        else:
            return None

        # the expanded key_size
        expanded_key_size = 16 * (nbr_rounds + 1)

        # Set the block values, for the block:
        # a0,0 a0,1 a0,2 a0,3
        # a1,0 a1,1 a1,2 a1,3
        # a2,0 a2,1 a2,2 a2,3
        # a3,0 a3,1 a3,2 a3,3
        # the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3
        #
        # iterate over the columns
        for i in range(4):
            # iterate over the rows
            for j in range(4):
                block[(i + (j * 4))] = input[(i * 4) + j]

        # expand the key into an 176, 208, 240 bytes key
        # the expanded key
        expanded_key = self.expand_key(key, size, expanded_key_size)

        # encrypt the block using the expanded_key
        block = self.aes_main(block, expanded_key, nbr_rounds)

        # unmap the block again into the output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k * 4) + l] = block[(k + (l * 4))]
        return output

    def decrypt(self, input, key, size):
        """
        Function that decrypts a 128 bit input block against the given key of size specified
        :param input: input string to decrypt
        :param key: decryption key
        :param size: size of the key
        :return: decrypted string
        """
        output = [0] * 16

        # the number of rounds
        nbr_rounds = 0

        # the 128 bit block to decode
        block = [0] * 16

        # set the number of rounds
        if size == self.key_size["SIZE_128"]:
            nbr_rounds = 10
        elif size == self.key_size["SIZE_192"]:
            nbr_rounds = 12
        elif size == self.key_size["SIZE_256"]:
            nbr_rounds = 14
        else:
            return None

        # the expanded key_size
        expanded_key_size = 16 * (nbr_rounds + 1)

        # Set the block values, for the block:
        # a0,0 a0,1 a0,2 a0,3
        # a1,0 a1,1 a1,2 a1,3
        # a2,0 a2,1 a2,2 a2,3
        # a3,0 a3,1 a3,2 a3,3
        # the mapping order is a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3

        # iterate over the columns
        for i in range(4):
            # iterate over the rows
            for j in range(4):
                block[(i + (j * 4))] = input[(i * 4) + j]

        # expand the key into an 176, 208, 240 bytes key
        expanded_key = self.expand_key(key, size, expanded_key_size)

        # decrypt the block using the expanded_key
        block = self.aes_inv_main(block, expanded_key, nbr_rounds)

        # unmap the block again into the output
        for k in range(4):
            # iterate over the rows
            for l in range(4):
                output[(k * 4) + l] = block[(k + (l * 4))]
        return output


class AESModeOfOperation(object):
    """
    This class handles AES with plaintext consisting of multiple blocks.

    Choice of block encoding modes:  OFB (Output Feedback),
    CFB (Cipher Feedback), CBC (Cipher Block Chaining)
    """
    aes = AES()

    # structure of supported modes of operation
    modeOfOperation = dict(OFB=0, CFB=1, CBC=2)

    # converts a 16 character string into a number array
    def convert_string(self, string, start, end, mode):
        if end - start > 16: end = start + 16
        if mode == self.modeOfOperation["CBC"]:
            ar = [0] * 16
        else:
            ar = []

        i = start
        j = 0
        while len(ar) < end - start:
            ar.append(0)
        while i < end:
            ar[j] = ord(string[i])
            j += 1
            i += 1
        return ar

    def encrypt(self, string_in, mode, key, size, IV):
        """
        Function to perform Mode of Operation Encryption.
        :param string_in: input string
        :param mode: mode of type modeOfOperation
        :param key: a hex key of the bit length size
        :param size: the bit length of the key
        :param IV: the 128-bit hex Initialization Vector
        :return: Mode of encryption, length of string_in, encrypted string
        """
        if len(key) % size:
            return None
        if len(IV) % 16:
            return None

        # the AES input/output
        plaintext = []
        input = [0] * 16
        output = []
        ciphertext = [0] * 16

        # the output cipher string
        cipher_out = []

        # char first_round
        first_round = True
        if string_in != None:
            for j in range(int(math.ceil(float(len(string_in)) / 16))):
                start = j * 16
                end = j * 16 + 16
                if end > len(string_in):
                    end = len(string_in)
                plaintext = self.convert_string(string_in, start, end, mode)

                # print 'PT@%s:%s' % (j, plaintext)
                if mode == self.modeOfOperation["CFB"]:
                    if first_round:
                        output = self.aes.encrypt(IV, key, size)
                        first_round = False
                    else:
                        output = self.aes.encrypt(input, key, size)

                    for i in range(16):
                        if len(plaintext) - 1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output) - 1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext) - 1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]

                    for k in range(end - start):
                        cipher_out.append(ciphertext[k])
                    input = ciphertext

                elif mode == self.modeOfOperation["OFB"]:
                    if first_round:
                        output = self.aes.encrypt(IV, key, size)
                        first_round = False
                    else:
                        output = self.aes.encrypt(input, key, size)

                    for i in range(16):
                        if len(plaintext) - 1 < i:
                            ciphertext[i] = 0 ^ output[i]
                        elif len(output) - 1 < i:
                            ciphertext[i] = plaintext[i] ^ 0
                        elif len(plaintext) - 1 < i and len(output) < i:
                            ciphertext[i] = 0 ^ 0
                        else:
                            ciphertext[i] = plaintext[i] ^ output[i]

                    for k in range(end - start):
                        cipher_out.append(ciphertext[k])
                    input = output

                elif mode == self.modeOfOperation["CBC"]:
                    for i in range(16):
                        if first_round:
                            input[i] = plaintext[i] ^ IV[i]
                        else:
                            input[i] = plaintext[i] ^ ciphertext[i]

                    # print 'IP@%s:%s' % (j, input)
                    first_round = False
                    ciphertext = self.aes.encrypt(input, key, size)

                    # always 16 bytes because of the padding for CBC
                    for k in range(16):
                        cipher_out.append(ciphertext[k])

        return mode, len(string_in), cipher_out

    def decrypt(self, cipher_in, original_size, mode, key, size, IV):
        """
        Function to perform the Mode of Operation Decryption.
        :param cipher_in: encrypted string
        :param original_size: the unencrypted string length - required for CBC
        :param mode: mode of type modeOfOperation
        :param key: a number array of the bit length size
        :param size: the bit length of the key
        :param IV: the 128-bit number array Initialization Vector
        :return: decrypted plain text
        """
        # cipher_in = unescCtrlChars(cipher_in)
        if len(key) % size:
            return None
        if len(IV) % 16:
            return None

        # the AES input/output
        ciphertext = []
        input = []
        output = []
        plaintext = [0] * 16

        # the output plain text character list
        chr_out = []

        # char first_round
        first_round = True
        if cipher_in != None:
            for j in range(int(math.ceil(float(len(cipher_in)) / 16))):
                start = j * 16
                end = j * 16 + 16
                if j * 16 + 16 > len(cipher_in):
                    end = len(cipher_in)
                ciphertext = cipher_in[start:end]

                if mode == self.modeOfOperation["CFB"]:
                    if first_round:
                        output = self.aes.encrypt(IV, key, size)
                        first_round = False
                    else:
                        output = self.aes.encrypt(input, key, size)

                    for i in range(16):
                        if len(output) - 1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext) - 1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output) - 1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]

                    for k in range(end - start):
                        chr_out.append(chr(plaintext[k]))
                    input = ciphertext

                elif mode == self.modeOfOperation["OFB"]:
                    if first_round:
                        output = self.aes.encrypt(IV, key, size)
                        first_round = False
                    else:
                        output = self.aes.encrypt(input, key, size)

                    for i in range(16):
                        if len(output) - 1 < i:
                            plaintext[i] = 0 ^ ciphertext[i]
                        elif len(ciphertext) - 1 < i:
                            plaintext[i] = output[i] ^ 0
                        elif len(output) - 1 < i and len(ciphertext) < i:
                            plaintext[i] = 0 ^ 0
                        else:
                            plaintext[i] = output[i] ^ ciphertext[i]

                    for k in range(end - start):
                        chr_out.append(chr(plaintext[k]))
                    input = output

                elif mode == self.modeOfOperation["CBC"]:
                    output = self.aes.decrypt(ciphertext, key, size)

                    for i in range(16):
                        if first_round:
                            plaintext[i] = IV[i] ^ output[i]
                        else:
                            plaintext[i] = input[i] ^ output[i]
                    first_round = False

                    if original_size is not None and original_size < end:
                        for k in range(original_size - start):
                            chr_out.append(chr(plaintext[k]))
                    else:
                        for k in range(end - start):
                            chr_out.append(chr(plaintext[k]))
                    input = ciphertext

        return "".join(chr_out)


def append_pkcs7_padding(s):
    """
    Function to return s padded to a multiple of 16-bytes by PKCS7 padding.
    :param s: string to apply padding to
    :return: padded string
    """
    numpads = 16 - (len(s) % 16)
    return s + numpads * chr(numpads)


def strip_pkcs7_padding(s):
    """
    Function to return s stripped of PKCS7 padding
    :param s: string to strip
    :return: stripped string
    """
    if len(s) % 16 or not s:
        raise ValueError("String of len %d can't be PCKS7-padded" % len(s))
    numpads = ord(s[-1])

    if numpads > 16:
        raise ValueError("String ending with %r can't be PCKS7-padded" % s[-1])
    return s[:-numpads]


def encrypt_data(key, data, mode=AESModeOfOperation.modeOfOperation["CBC"]):
    """
    Function to encrypt data using the key.
    The key should be a string of bytes.
    :param key: string of bytes
    :param data: data to encrypt
    :param mode: mode of operation of aes encryption
    :return: cipher string prepended with the initialization vector (iv)
    """
    key = map(ord, key)
    if mode == AESModeOfOperation.modeOfOperation["CBC"]:
        data = append_pkcs7_padding(data)

    keysize = len(key)
    assert keysize in AES.key_size.values(), 'invalid key size: %s' % keysize

    # Create a new initialization vector (iv) using random data
    iv = [ord(i) for i in os.urandom(16)]
    moo = AESModeOfOperation()
    (mode, length, ciph) = moo.encrypt(data, mode, key, keysize, iv)

    # With padding, the original length does not need to be known. It's a bad
    # idea to store the original message length.
    # prepend the initialization vector (iv).

    return ''.join(map(chr, iv)) + ''.join(map(chr, ciph))


def decrypt_data(key, data, mode=AESModeOfOperation.modeOfOperation["CBC"]):
    """
    Function to decrypt data using key.
    Key should be a string of bytes.
    Data should have the initialization vector (iv) prepended
    as a string of ordinal values.
    :param key: string of bytes
    :param data: data to decrypt
    :param mode: mode of operation of aes decryption
    :return: decrypted data
    """
    key = map(ord, key)
    keysize = len(key)
    assert keysize in AES.key_size.values(), 'invalid key size: %s' % keysize

    # iv is first 16 bytes
    iv = map(ord, data[:16])
    data = map(ord, data[16:])
    moo = AESModeOfOperation()
    decr = moo.decrypt(data, None, mode, key, keysize, iv)

    if mode == AESModeOfOperation.modeOfOperation["CBC"]:
        decr = strip_pkcs7_padding(decr)
    return decr


def generate_random_key(keysize):
    """
    Function to generate a key from random data of length keysize
    :param keysize: size of the key
    :return: key as a string of bytes
    """
    if keysize not in (16, 24, 32):
        emsg = 'Invalid keysize, %s. Should be one of (16, 24, 32).'
        raise ValueError, emsg % keysize

    return os.urandom(keysize)


def test_str(cleartext, keysize=16, mode_name="CBC"):
    """Function to test AES with random key, choice of mode."""
    print 'Random key test', 'Mode:', mode_name
    print 'cleartext:', cleartext
    key = generate_random_key(keysize)
    print 'Key:', [ord(x) for x in key]
    mode = AESModeOfOperation.modeOfOperation[mode_name]
    cipher = encrypt_data(key, cleartext, mode)
    print 'Cipher:', [ord(x) for x in cipher]
    decr = decrypt_data(key, cipher, mode)
    print 'Decrypted:', decr


# How to use AES Encryption in main
'''
if __name__ == "__main__":
    moo = AESModeOfOperation()
    cleartext = "This is a test with several blocks!"
    cypherkey = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
    iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
    mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"],
            cypherkey, moo.aes.key_size["SIZE_128"], iv)
    print 'm=%s, ol=%s (%s), ciph=%s' % (mode, orig_len, len(cleartext), ciph)
    decr = moo.decrypt(ciph, orig_len, mode, cypherkey,
            moo.aes.key_size["SIZE_128"], iv)
    print decr
    test_str(cleartext, 16, "CBC")
'''

"""
cleartext will be the replay file we are encrypting.
Set the cypherkey and inspection vector.
Choose mode of encryption operation and encrypt
Print the data if you would like to check the work
Decrpypt
And the test_str call (test function)
"""


# End AES Encryption (Complex Encryption)

################################################################################
# Replay
################################################################################

def open_replay(number):
    """
    Function to open and play the replay to the user.
    :param number: replay number
    :return:
    """
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
    global key_caesar_cipher

    # Open the chosen replay file.
    open_chosen_replay_file(number)

    # Set the caption for the console window.
    if number == 1:
        pygame.display.set_caption("Replay 1: " + str(chosen_replay_filename[7:-4]))
    elif number == 2:
        pygame.display.set_caption("Replay 2: " + str(chosen_replay_filename[7:-4]))
    elif number == 3:
        pygame.display.set_caption("Replay 3: " + str(chosen_replay_filename[7:-4]))

    # Read each line of the encrypted chosen replay file and store into a list.
    encrypted_lines_list = chosen_replay_file.readlines()

    # Remove the first line from the chosen replay file and store it.
    encryption_algorithm_key = encrypted_lines_list[0].strip()

    # Decrypt the file if it was encrypted
    # using an encryption algorithm.
    if (encryption_algorithm_key == ("1" or "2" or "3")):
        # If the file was encrypted using the Caesar Cipher
        # encryption algorithm, then decrypt the file using
        # the Caesar Cipher decryption algorithm.
        if encryption_algorithm_key == "1":
            # Remove the first line which contains the
            # value representing the chosen algorithm.
            del encrypted_lines_list[0]

            # Decrypt the remaining lines and store into a list.
            chosen_replay_file_list = [caesar_cipher_decrypt(x, key_caesar_cipher)
                                       for x in encrypted_lines_list]
        # If the file was encrypted using the <insert algorithm name here>
        # encryption algorithm, then decrypt the file using
        # the <insert algorithm name here> decryption algorithm.
        elif encryption_algorithm_key == "2":
            # Remove the first line which contains the
            # value representing the chosen algorithm.
            del encrypted_lines_list[0]

            # Decrypt the remaining lines and store into a list.
            # chosen_replay_file_list = [algorithm_name_decrypt(x, key_algorithm_name)
            # for x in encrypted_lines_list]
        # If the file was encrypted using the <insert algorithm name here>
        # encryption algorithm, then decrypt the file using
        # the <insert algorithm name here> decryption algorithm.
        elif encryption_algorithm_key == "3":
            # Remove the first line which contains the
            # value representing the chosen algorithm.
            del encrypted_lines_list[0]

            # Decrypt the remaining lines and store into a list.
            # chosen_replay_file_list = [algorithm_name_decrypt(x, key_algorithm_name)
            # for x in encrypted_lines_list]

        # Close the opened chosen replay file after reading is complete.
        close_chosen_replay_file()

        # Set the grid equal to the same grid in the chosen replay file.
        grid = ast.literal_eval(chosen_replay_file_list[0])
        # Remove the grid from the chosen replay file list.
        del chosen_replay_file_list[0]

        # Set the object positions equal to the same
        # object positions in the chosen replay file.
        object_position_dictionary = ast.literal_eval(chosen_replay_file_list[0])
        # Remove the object position dictionary from the chosen replay file list.
        del chosen_replay_file_list[0]

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

        # Variable used as a counter for the following loop.
        i = 0
        # Continue running until the player completes the game or closes the window.
        while game_complete == False:
            if i <= len(chosen_replay_file_list):
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
                    for z in range(len(marked_tile_list)):
                        # Fill in the marked tiles with the color red.
                        screen.fill((255, 0, 0), get_cell_rect(marked_tile_list[z],
                                                               screen))
                ################################################################

                # Update the InputText widget.
                sgc.update(1)
                # Update the console window to show changes.
                pygame.display.update()

            # Exit the loop if all commands in the list have been executed.
            if i > len(chosen_replay_file_list):
                game_complete = True

            # Increment the value of i by 1.
            i = i + 1
        # Pause for 7 seconds before terminating the program.
        time.sleep(7)

        # Print new lines for spacing.
        print "\n\n"

        # Exit the current scope and back to the
        # loop that controls the game state.
        return

    # There is an error with the first line of the replay file,
    # so print an error message and don't mess with anything.
    else:
        # Print new lines for spacing.
        print "\n\n"

        # Piece the exception message together for printing.
        exception_message = (str(time.strftime("%H-%M-%S")) + ": Error: "
                             + "Incorrect encryption algorithm key"
                             + " \n\t\t\tIgnoring your feeble "
                             + "attempts to crash the game and continuing.")
        # Print the exception to the log file.
        write_to_log_file(exception_message)


################################################################################
# Rendering
################################################################################

def generate_maze_recursive_backtracker():
    # Size of the maze.
    """
    Function that generates a random maze using the Recursive Backtracker algorithm.
    """
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


def generate_maze_binary_tree():
    # Size of the maze.
    """
    Function that generates a random maze using the Binary Tree algorithm.
    """
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


def reset_maze():
    """
    Function to reset the maze back to its original state.
    """
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


def check_maze_for_validity_player_door():
    """
    Function to test the maze for validity by checking
    the path from the player to the door object.
    :return: 0 if the maze is valid, 1 if the maze is invalid
    """
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


def check_maze_for_validity_player_key():
    """
    Function to test the maze for validity by checking
    the path from the player to the key object.
    :return: 0 if the maze if valid, 1 if the maze is invalid
    """
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


def check_maze_for_validity_player_chest():
    """
    Function to test the maze for validity by checking
    the path from the player to the chest object.
    :return: 0 if the maze is valid, 1 if the maze is invalid
    """
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


def draw_screen(screen):
    """
    Function to draw the screen.
    :param screen: screen to draw
    """
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
        for z in range(len(marked_tile_list)):
            if is_object_visible(marked_tile_list[z][0], marked_tile_list[z][1]):
                # Fill in the marked tiles with the color red.
                screen.fill((255, 0, 0), get_cell_rect(marked_tile_list[z], screen))

    # Call the function to draw the player character object.
    draw_player_object(player_object, screen)'''
    ############################################################################


def is_object_visible(object_position_x, object_position_y):
    """
    Function to determine if the given object is within the field of view.
    :param object_position_x: object's x coordinate
    :param object_position_y: object's y coordinate
    :return: bool value
    """
    for i in range(len(visible_object_list)):
        if object_position_x == visible_object_list[i][0] and \
                        object_position_y == visible_object_list[i][1]:
            return True

    return False


def get_visible_object_list():
    """
    Function to store object coordinates that are within the field of view.
    """
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


def get_cell_rect(coordinates, screen):
    """
    Function to draw the container of the objects.
    :param coordinates:
    :param screen:
    :return:
    """
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


def draw_door_object(door_object, screen):
    """
    Function to draw the door object to the console window.
    :param door_object: door object to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the door object.
    rect = door_object.get_rect()
    # Receive the center of the door object.
    rect.center = get_cell_rect(door_object_position, screen).center
    # Draw the door object image.
    screen.blit(door_object, rect)


def draw_closed_chest_object(chest_object_closed, screen):
    """
    Function to draw the closed chest object to the console window.
    :param chest_object_closed: chest object to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the closed chest object.
    rect = chest_object_closed.get_rect()
    # Receive the center of the closed chest object.
    rect.center = get_cell_rect(chest_object_position, screen).center
    # Draw the closed chest object image.
    screen.blit(chest_object_closed, rect)


def draw_opened_chest_object(chest_object_opened, screen):
    """
    Function to draw the opened chest object to the console window.
    :param chest_object_opened: chest object to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the opened chest object.
    rect = chest_object_opened.get_rect()
    # Receive the center of the opened chest object.
    rect.center = get_cell_rect(chest_object_position, screen).center
    # Draw the opened chest object image.
    screen.blit(chest_object_opened, rect)


def draw_key_object(key_object, screen):
    """
    Function to draw the key object to the console window.
    :param key_object: key object to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the key object.
    rect = key_object.get_rect()
    # Receive the center of the key object.
    rect.center = get_cell_rect(key_object_position, screen).center
    # Draw the key object image.
    screen.blit(key_object, rect)


def draw_player_object(player_object, screen):
    """
    Function to draw the player character object to the console window.
    :param player_object: player object to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the player object.
    rect = player_object.get_rect()
    # Receive the center of the player object.
    rect.center = get_cell_rect(player_object_position, screen).center
    # Draw the player object image.
    screen.blit(player_object, rect)


def draw_simple_enemy_object(simple_enemy_object, screen):
    """
    Function to draw the simple enemy object to the console window.
    :param simple_enemy_object: simple enemy object to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the simple enemy object.
    rect = simple_enemy_object.get_rect()
    # Receive the center of the simple enemy object.
    rect.center = get_cell_rect(simple_enemy_object_position, screen).center
    # Draw the simple enemy object image.
    screen.blit(simple_enemy_object, rect)


def draw_smart_enemy_object(smart_enemy_object, screen):
    """
    Function to draw the smart enemy object to the console window.
    :param smart_enemy_object: smart enemy object to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the smart enemy object.
    rect = smart_enemy_object.get_rect()
    # Receive the center of the smart enemy object.
    rect.center = get_cell_rect(smart_enemy_object_position, screen).center
    # Draw the smart enemy object image.
    screen.blit(smart_enemy_object, rect)


def draw_chest_combination_1_object(chest_combination_1_object, screen):
    """
    Function to draw the chest combination 1 object to the console window.
    :param chest_combination_1_object: combination to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the chest_combination_1 object.
    rect = chest_combination_1_object.get_rect()
    # Receive the center of the chest_combination_1 object.
    rect.center = get_cell_rect(chest_combination_1_object_position, screen).center
    # Draw the chest_combination_1 object image.
    screen.blit(chest_combination_1_object, rect)


def draw_chest_combination_2_object(chest_combination_2_object, screen):
    """
    Function to draw the chest combination 2 object to the console window.
    :param chest_combination_2_object: combination to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the chest_combination_2 object.
    rect = chest_combination_2_object.get_rect()
    # Receive the center of the chest_combination_2 object.
    rect.center = get_cell_rect(chest_combination_2_object_position, screen).center
    # Draw the chest_combination_2 object image.
    screen.blit(chest_combination_2_object, rect)


def draw_chest_combination_3_object(chest_combination_3_object, screen):
    """
    Function to draw the chest combination 3 object to the console window.
    :param chest_combination_3_object: combination to draw
    :param screen: screen to draw on
    """
    # Return the size and offset of the chest_combination_3 object.
    rect = chest_combination_3_object.get_rect()
    # Receive the center of the chest_combination_3 object.
    rect.center = get_cell_rect(chest_combination_3_object_position, screen).center
    # Draw the chest_combination_3 object image.
    screen.blit(chest_combination_3_object, rect)


################################################################################
# Object Placement
################################################################################

def generate_random_object_positions():
    """
    Function to generate random start positions for
    the player, chest, key, door, and enemy objects.
    """
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


def generate_optimal_object_positions():
    """
    Function to generate random positions for the objects on the optimal path.
    """
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


def position_is_object(x, y):
    # Return True for the player object.
    """
    Function to determine if the coordinate is blocked by an object.
    :param x: object's x coordinate
    :param y: object's y coordinate
    :return: bool value if coordinate is blocked
    """
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


def position_is_wall(x, y):
    """
    Function to determine if the coordinate is blocked by a wall.
    :param x: wall x coordinate
    :param y: wall y coordinate
    :return: bool value if coordinate is blocked by wall
    """
    # Return True for the wall object.
    if grid[y][x] == 0:
        return True

    return False


def reset_object_positions_and_state_conditions():
    """
    Function that resets the position of the player
    and confiscates all gathered items.
    """
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

def handle_input():
    """
    Function to handle player character movement.
    :return: nothing to return
    """
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
    global marked_tile_list
    global player_used_marker
    global game_complete
    global chosen_encryption_algorithm
    global player_game_moves

    # Reset player's moves to zero.
    player_game_moves = 0

    # Manage the number of replay files.
    manage_replay_files()

    # Create a string equal to the current time for the replay file.
    replay_filename = time.strftime("Replay_%m-%d-%y_%H-%M-%S.txt")

    # Open the replay file.
    open_replay_file()

    # Store all necessary information into the replay file.
    # Key representing the encryption algorithm used.
    write_to_replay_file(chosen_encryption_algorithm)
    # Grid containing the positions of all walls and floors in the maze.
    write_to_replay_file(str(grid))
    # Dictionary containing the starting positions of all objects in the grid.
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
                for z in range(len(marked_tile_list)):
                    # Fill in the marked tiles with the color red.
                    screen.fill((255, 0, 0), get_cell_rect(marked_tile_list[z],
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

    # Update the users replays remotely.
    save_replays()

    # Exit the current scope and back to the loop that controls the game state.
    return


################################################################################
# Character Actions
################################################################################

def go(dx, dy):
    global player_game_moves
    """
    Function to move the player character object through the maze.
    :param dx: player x coordinate
    :param dy: player y coordinate
    """
    # Call the function to reset the game if the player character
    # is in the same coordinate as either enemy.
    if player_object_position == simple_enemy_object_position \
            or player_object_position == smart_enemy_object_position:
        # Print out an message informing the user that they lost.
        print "Output: The enemy grabbed you! Your stuff was confiscated "
        print "\tand you were returned to where you started. "
        print "\tYou will have to try your luck again...\n"
        # Play the die sound
        die_sound.play()
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
            # Play the sound for going
            go_sound.play()
            # Increment player moves.
            player_game_moves = player_game_moves + 1
        else:
            # Print out an error for the invalid move.
            print_go_error()
            # Play the pain sound for running into wall
            pain_sound.play()

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


def go_length(direction, length):
    """
    Function to move the player character object through
    the maze for the number of times they specify.
    :param direction: direction to move player
    :param length: distance to move player
    """
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


def use_marker():
    """
    Function to use the marker.
    """
    global marked_tile_list
    global player_used_marker

    # Change the value of player_used_marker to True. It is used in the
    # draw_screen function to determine when to start drawing the marker.
    player_used_marker = True
    # Play the sound for using the marker
    use_marker_sound.play()

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


def grab_key():
    """
    Function to grab the key.
    """
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
        # Play the sound for grabbing the key
        grab_key_sound.play()
    else:
        # Inform the player that the key is not within their reach.
        print "Output: The key is not within reach..." \
              "\nTry looking for something key-shaped."

    # Call the function to move the enemies.
    move_simple_enemy()
    move_smart_enemy()


def unlock_chest(user_input_combination):
    """
    Function to unlock the chest.
    :param user_input_combination: combination the user inputs
    """
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
                # Play the sound for using the combo
                # to eventually open the chest
                use_combo_sound.play()
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


def open_chest():
    """
    Function to open the chest.
    """
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
                # Play the sound for opening the chest
                open_chest_sound.play()
                # Play the treasure sound
                treasure_sound.play()
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


def use_key():
    """
    Function to use the key.
    """
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
            # Play the sound for unlocking the door (using the key)
            unlock_door_sound.play()
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


def open_door():
    """
    Function to open the door.
    """
    # Needed to change their properties.
    global door_object
    global door_object_position
    global player_opened_chest
    global game_complete
    global player_game_moves

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
            # Play sound for opening the door
            open_door_sound.play()
            # Congratulate the player on completing the game.
            print "\n\nCongratulations! You have escaped!"
            # Stop the background music
            background_sound.stop()
            # Play the congratulatory game over sound
            game_over_sound.play()
            # Call function to update top 10 moves if needed.
            print "Number of moves made: ", player_game_moves
            print "\n\n"
            update_top10(player_game_moves)
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


def player_next_to_object(x, y, a, b):
    """
    Function that returns true if the player character
    object is located next to another object.
    :param x: player x coordinate
    :param y: player y coordinate
    :param a: object x coordinate
    :param b: object y coordinate
    :return: bool value if player is next to an object
    """
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

def move_simple_enemy():
    """
    Function to move the simple enemy object in a random direction.
    """
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


def move_smart_enemy():
    """
    Function to move the smart enemy in a direction towards the player.
    """
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

    # print cost_so_far

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


def respawn_smart_enemy():
    """
    Function to reset the smart enemy object position.
    """
    global smart_enemy_object_position

    # Reset the smart enemy object's position.
    smart_enemy_object_position = [object_position_dictionary['smart enemy'][0],
                                   object_position_dictionary['smart enemy'][1]]


################################################################################
# Path-finding (A* algorithm, Breadth-first search, and Depth-first search)
################################################################################

class SquareGrid:
    """
    Class used to make a graph object for the algorithm.
    """

    def __init__(self, width, height):
        """
        Initialize the parameters.
        :param width: width of grid
        :param height: height of grid
        """
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        """
        Function to determine if the neighbors are in bounds.
        :param id: neighbor id
        :return: bool value if neighbor is in bounds
        """
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        """
        Function to determine if an element is valid.
        :param id: element id
        :return: bool value if element is valid
        """
        return id not in self.walls

    def neighbors(self, id):
        """
        Function to find the neighbors.
        :param id: id of item to find neighbors for
        :return: resultant list of neighbors
        """
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0: results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid, object):
    """
    Subclass used to access the cost function.
    """

    def __init__(self, width, height):
        """
        Function to initialize grid with weights
        :param width: width of grid
        :param height: height of grid
        """
        super(GridWithWeights, self).__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        """
        Function used to calculate the cost to move from from_node to to_node.
        :param from_node: node to move from
        :param to_node: node to move to
        :return: cost of moving from node to node
        """
        return self.weights.get(to_node, 1)


class PriorityQueue:
    """
    Class that associates each item with a priority.
    """

    def __init__(self):
        """
        Function to initialize.
        """
        self.elements = []

    def empty(self):
        """
        Function to empty priority queue
        :return:
        """
        return len(self.elements) == 0

    def put(self, item, priority):
        """
        Function to put item in priority queue
        :param item: item to put
        :param priority: priority queue
        """
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        """
        Function to get priority queue
        :return: priority queue elements
        """
        return heapq.heappop(self.elements)[1]


def heuristic(a, b):
    """
    Function used to heuristic
    :param a:
    :param b:
    :return:
    """
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


# Function that implements the A* algorithm.
# Parameters:
#   1) graph - the graph we will search.
#   2) start - the starting location (character location at start).
#   3) goal - the ending location (door location at start).
def a_star_search(graph, start, goal):
    """
    Function that implements the A* algorithm.
    :param graph: the graph we will search
    :param start: the starting location (character location at start)
    :param goal: the ending location (door location at start).
    :return: where we came from and how much it has cost us
    """
    # Initialize variables.
    frontier = PriorityQueue()  # Expanding queue that keeps track of the path.
    came_from = {}  # Dictionary that maps the coordinates to the cost.
    cost_so_far = {}  # Dictionary that maps the coordinates to the cost.

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


def is_valid(point, grid):
    """
    Function to check the validity of a point before it is added as a neighbor.
    :param point: point to check validity of
    :param grid: grid that contains the point
    :return: bool value if point is valid
    """
    # Check if the point of the grid is out of range or is a wall.
    if (point[0] > 14) or (point[1] > 14) or (grid[point[0]][point[1]] == 0):
        return False
    else:
        return True


def add_neighbours(point, neighbours_list, visited_list, grid, dict):
    """
    Function to add all the neighbors of the selected point to the stack (list).
    :param point: point to check neighbors of
    :param neighbours_list: list of neighbors of point
    :param visited_list: list of visited
    :param grid: grid we are using
    :param dict: dictionary of points
    :return: nothing to return
    """
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
            add_to_dictionary(dict, point, neighbor_point_4)
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


def add_to_dictionary(dictionary, parent, child):
    """
    Dictionary used to print the success path after it has been generated.
    :param dictionary: dictionary we are adding to
    :param parent:
    :param child:
    """
    p_l = map(str, parent)
    c_l = map(str, child)
    p_l = ','.join(p_l)
    c_l = ','.join(c_l)
    dictionary[c_l] = p_l


def depth_first_search(start_point, end_point, graph, dict):
    """
    Function that implements the main logic of the DFS algorithm.
    :param start_point: starting point
    :param end_point: ending point
    :param graph: graph we are using
    :param dict: dictionary to add neighbors to
    """
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


def breath_first_search(start_point, end_point, graph, dict):
    """
    Function that contains the main logic of the BFS algorithm.
    :param start_point: starting point
    :param end_point: ending point
    :param graph: graph we are using
    :param dict: dictionary to add neighbors to
    """
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


def draw_hierarchy(dict, point):
    """
    Function to add the locations at the end to the list (stack).
    :param dict: dictionary of points
    :param point: location to add
    :return: list
    """
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


'''
def perform_search():
    """
    Function that uses both searching algorithms to find all available paths.
    """
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
