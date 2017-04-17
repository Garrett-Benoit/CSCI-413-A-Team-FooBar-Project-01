

# Initialize the pygame console window.
pygame.init()
clock = pygame.time.Clock() 

class MainMenu(sgc.Menu): 
    """ 
    Create a subclass for custom functions. 
    """ 
    def __init__(self, **kwargs): 
        super(sgc.Menu,self).__init__(**kwargs) 
        self.start_new_game = False 
        self.replay_1 = False 
        self.replay_2 = False 
        self.replay_3 = False 
        
    # Return a dictionary of functions callable from the menu 
    func_dict = lambda self: {"new_game": self.new_game, 
                              "remove": self.remove, 
                              "replay_1": self.replay_1, 
                              "replay_2": self.replay_2, 
                              "replay_3": self.replay_3} 
                              
    # This function is called when a new game is to be started 
    def new_game(self): 
        self.start_new_game = True 
        
    # This function is called when replay 1 is to be opened 
    def replay_1(self): 
        self.replay_1 = True 
        
    # This function is called when replay 2 is to be opened 
    def replay_2(self): 
        self.replay_2 = True 
    
    # This function is called when replay 3 is to be opened 
    def replay_3(self): 
        self.replay_3 = True 


# Create menu 
main_menu = None 
with open("menu") as menu_file: 
    main_menu = MainMenu(menu=menu_file) 
	
	
# Main function.
def main():
    global main_menu 
    
    # Initialise menu state variables 
    main_menu.start_new_game = False 
    main_menu.replay_1 = False 
    main_menu.replay_2 = False 
    main_menu.replay_3 = False 
    
    # Update display 
    main_menu.add() 
    sgc.update(clock.tick(30)) 
    pygame.display.update() 
    
    # Loop for main menu processing 
    while True: 
        # Check for selected option 
        if main_menu.start_new_game: 
            break 
        elif main_menu.replay_1: 
            break 
        elif main_menu.replay_2: 
            break 
        elif main_menu.replay_3: 
            break 
        
        # Check if window is closed 
        for event in pygame.event.get(): 
            sgc.event(event) 
            if event.type == QUIT: 
                exit() 

        # Update the widgets once for each frame 
        sgc.update(clock.tick(30)) 
        #pygame.display.update() 
        pygame.display.flip() 
    
    # Update display 
    time.sleep(1) 
    main_menu.remove() 
    input_box.add(order = 0) 
    
    # Clear screen 
    screen.fill((0,0,0)) 
    sgc.update(clock.tick(30)) 
    pygame.display.update() 
    
    # process user selection 
    if main_menu.start_new_game: 
        new_game() 
    elif main_menu.replay_1: 
        open_replay(1) 
    elif main_menu.replay_2: 
        open_replay(2) 
    elif main_menu.replay_3: 
        open_replay(3) 
		
		
# Function to reinitialise global variables before returning to main menu 
def reinitialize(): 
    global chosen_replay_filename 
    global chosen_replay_file 

    global maze_is_valid 
    global player_made_decision 
    global show_replay_1 
    global show_replay_2 
    global show_replay_3 
    global start_new_game 
    global game_complete 
    
    global chosen_replay_filename 
    global chosen_replay_file 

    global maze_is_valid 
    global player_made_decision 
    global show_replay_1 
    global show_replay_2 
    global show_replay_3 
    global start_new_game 
    global game_complete 
    
    global door_object
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
    
    chosen_replay_filename = None 
    chosen_replay_file = None 

    maze_is_valid = False 
    player_made_decision = False 
    show_replay_1 = False 
    show_replay_2 = False 
    show_replay_3 = False 
    start_new_game = False 
    game_complete = False 
    
    chosen_replay_filename = None 
    chosen_replay_file = None 

    maze_is_valid = False 
    player_made_decision = False 
    show_replay_1 = False 
    show_replay_2 = False 
    show_replay_3 = False 
    start_new_game = False 
    game_complete = False
    
    door_object = "D" 
    chest_object_closed = "C" 
    chest_object_opened = "O"
    key_object = "K" 
    player_object = "@" 
    simple_enemy_object = "E" 
    smart_enemy_object = "S" 
    chest_combination_1_object = str(random.randint(0, 9)) 
    chest_combination_2_object = str(random.randint(0, 9)) 
    chest_combination_3_object = str(random.randint(0, 9)) 
	
	 # reinitialise then return to main menu
    reinitialize() 
    main() 
	
	 # Print introduction message to the user.
    #print "\nTitle Screen: " 
    print "\nThe Amazing Dungeon " 
  
