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

# Import the libtcod library and rename.
import libtcodpy as libtcod
import textwrap



################################################################################
# Initialization
################################################################################

SCREEN_WIDTH = 100 # Width of the console window.
SCREEN_HEIGHT = 60 # Height of the console window.
MAP_WIDTH = 100 # Width of the map.
MAP_HEIGHT = 50 # Height of the map.
ROOM_MAX_SIZE = 10 # Maximum size of created rooms.
ROOM_MIN_SIZE = 8 # Minimum size of created room.
MAX_ROOMS = 30 # Maximum number of created rooms.
FOV_ALGO = 0  # Default FOV algorithm in libtcod.
FOV_LIGHT_WALLS = True # Make walls in player character sight visible.
SIGHT_RADIUS = 10 # Default radius for player character sight.
PANEL_HEIGHT = 10 # Height of the panel.
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT # Position for the text on the panel.
MSG_WIDTH = SCREEN_WIDTH # Width of messages displayed in the panel.
MSG_HEIGHT = PANEL_HEIGHT - 1 # Height of messages displayed in the panel.

# Initial player position.
playerx = SCREEN_WIDTH / 2
playery = SCREEN_HEIGHT / 2

# Color Definitions.
color_dark_wall = libtcod.Color(0, 0, 100)
color_light_wall = libtcod.Color(130, 110, 50)
color_dark_ground = libtcod.Color(50, 50, 150)
color_light_ground = libtcod.Color(200, 180, 50)

# Set the font properties of the console window.
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE
                                | libtcod.FONT_LAYOUT_TCOD)

# Initialize the console window.
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                          'CSCI-413-Team-Assignment-01', False)

# Create a new off-screen console window.
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

# Create a new console window for the GUI.
panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)



################################################################################
# Tile Class
################################################################################

class Tile:
    # A tile of the map the properties associated with it.
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        # Set all tiles unexplored at start.
        self.explored = True

        # Tiles that block objects will block sight by default.
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight



################################################################################
# Object Class (Player, Chest, Key, Door)
################################################################################

class Object:
    def __init__(self, x, y, char, name, color, blocks=True):
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color
        self.blocks = blocks

    # Function to move the object on the console window.
    def move(self, dx, dy):
        # Move by the given amount.
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    # Function to draw the object to the console window.
    def draw(self):
        # Only draw if it is in the player character's field of view.
        if libtcod.map_is_in_fov(fov_map, self.x, self.y):
            # Set the color and then draw the character
            # that represents this object at its position.
            libtcod.console_set_default_foreground(con, self.color)
            libtcod.console_put_char(con, self.x, self.y, self.char,
                                     libtcod.BKGND_NONE)

    # Function to clear the object from the console window.
    def clear(self):
        # Erase the called character that represents this object.
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

# Function to place objects on the map.
def place_objects():
    # Total number of placed objects.
    num_placed_objects = 0

    # Randomly place the key on the map.
    while num_placed_objects != 1:
        # Choose random coordinates for the key.
        x = libtcod.random_get_int(0, 0, MAP_WIDTH)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT)

        # Place the key if the tile is not blocked.
        if not is_blocked(x, y):
            # Create a key.
            key = Object(x, y, 'K', 'Key', libtcod.silver, blocks=True)

            objects.append(key)
            num_placed_objects+=1

    # Randomly place the chest on the map.
    while num_placed_objects != 2:
        # Choose random coordinates for the chest.
        x = libtcod.random_get_int(0, 0, MAP_WIDTH)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT)

        # Place the chest if the tile is not blocked.
        if not is_blocked(x, y):
            # Create a chest.
            chest = Object(x, y, 'C', 'Chest', libtcod.gold, blocks=True)

            objects.append(chest)
            num_placed_objects+=1



################################################################################
# Room and Tunnel Creation
################################################################################
class Rect:
    # Function that defines a rectangle (room) on the map.
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    # Function that returns the center coordinates of the room.
    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return (center_x, center_y)

    # Function to detect intersections.
    def intersect(self, other):
        # Returns true if this rectangle intersects with another one.
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

# Function to determine if the coordinate is blocked.
def is_blocked(x, y):
    # Return true for any map tiles.
    if map[x][y].blocked:
        return True

    # Return true for any blocking objects.
    for object in objects:
        if object.blocks and object.x == x and object.y == y:
            return True

    return False

# Function to create a room in the map.
def create_room(room):
    global map

    # Make the tiles in the rectangle passable.
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            map[x][y].blocked = False
            map[x][y].block_sight = False

# Function to create a horizontal tunnel.
def create_h_tunnel(x1, x2, y):
    global map

    for x in range(min(x1, x2), max(x1, x2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False

# Function to create a vertical tunnel.
def create_v_tunnel(y1, y2, x):
    global map

    for y in range(min(y1, y2), max(y1, y2) + 1):
        map[x][y].blocked = False
        map[x][y].block_sight = False



################################################################################
# Map Creation
################################################################################

# Function to create and add tiles to the map.
def make_map():
    global map, player

    map = [[ Tile(True)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]

    # Create the rooms on the map.
    rooms = []
    num_rooms = 0

    for r in range(MAX_ROOMS):
        # Generate a random width and height for each created room.
        w = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        # Generate a random position (within the boundaries of the map)
        # for each created room.
        x = libtcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

        if num_rooms == 0:
            # Create the starting room.
            new_room = Rect(MAP_WIDTH / 2, MAP_HEIGHT / 2, 10, 10)
        else:
            # Create a new, random room.
            new_room = Rect(x, y, w, h)

        failed = False
        # Check the other rooms and see if they intersect with this one.
        for other_room in rooms:
            # Scrap the invalid, intersection filled room.
            if new_room.intersect(other_room):
                failed = True
                break

        # Create the valid, intersections free room.
        if not failed:
            # Draw the room to the map's tiles.
            create_room(new_room)

            # Center coordinates of the new room.
            (new_x, new_y) = new_room.center()

            if num_rooms == 0:
                # Place the player character at the
                # center of the starting room.
                player.x = new_x
                player.y = new_y + 2

            else:
                # Center coordinates of previous room.
                (prev_x, prev_y) = rooms[num_rooms-1].center()

                # Draw a random number that is either 0 or 1.
                if libtcod.random_get_int(0, 0, 1) == 1:
                    # Move horizontally, then vertically.
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    # Move vertically, then horizontally.
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

            # Append the new room to the list.
            rooms.append(new_room)
            num_rooms += 1

    # Add objects to the map.
    #place_objects()



################################################################################
# Rendering
################################################################################

# Function to draw all objects in the list.
def render_all():
    #
    global fov_map, color_dark_wall, color_light_wall
    global color_dark_ground, color_light_ground
    global fov_recompute

    # Recompute FOV if player or map changes.
    if fov_recompute:
        fov_recompute = False
        libtcod.map_compute_fov(fov_map, player.x, player.y, SIGHT_RADIUS,
                                FOV_LIGHT_WALLS, FOV_ALGO)

        # Draw all tiles to the screen.
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = map[x][y].block_sight

                if not visible:
                    # Only draw the object if it has been previously explored.
                    if map[x][y].explored:
                        # Tile is not visible.
                        if wall:
                            libtcod.console_set_char_background(con, x, y,
                                                                color_dark_wall,
                                                                libtcod.BKGND_SET)
                        else:
                            libtcod.console_set_char_background(con, x, y,
                                                                color_dark_ground,
                                                                libtcod.BKGND_SET)
                else:
                    # Tile is visible
                    if wall:
                        libtcod.console_set_char_background(con, x, y,
                                                            color_light_wall,
                                                            libtcod.BKGND_SET )
                    else:
                        libtcod.console_set_char_background(con, x, y,
                                                            color_light_ground,
                                                            libtcod.BKGND_SET )

                    map[x][y].explored = True

    # Draw the player character to the console window.
    for object in objects:
        object.draw()

    # Blit the contents of the new console to the root console.
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    # Prepare to render the GUI panel.
    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the game messages.
    y = 1
    for (line, color) in game_msgs:
        libtcod.console_set_default_foreground(panel, color)
        libtcod.console_print_ex(panel, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1

    # Blit the contents of "panel" to the root console.
    libtcod.console_blit(panel, 0, 0, SCREEN_WIDTH, PANEL_HEIGHT, 0, 0, PANEL_Y)

# Function to display messages in the console window.
def message(new_msg, color = libtcod.white):
    # If the message is too long, split it into multiple lines.
    new_msg_lines = textwrap.wrap(new_msg, MSG_WIDTH)

    for line in new_msg_lines:
        # If the buffer is full, remove the first line.
        if len(game_msgs) == MSG_HEIGHT:
            del game_msgs[0]

        # Add the new line.
        game_msgs.append( (line, color) )



################################################################################
# Character Movement
################################################################################

# Function to handle player character movement.
def handle_keys():
    global fov_recompute

    # Wait for user input.
    key = libtcod.console_wait_for_keypress(True)

    # Toggle fullscreen if the player presses
    # the Enter and Left Alt keys together.
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    # Exit the game if the user presses the Escape key.
    elif key.vk == libtcod.KEY_ESCAPE:
        return True

    # Movement keys.
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        # Move the player character up one position.
        player.move(0, -1)
        fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        # Move the player character down one position.
        player.move(0, 1)
        fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        # Move the player character left one position.
        player.move(-1, 0)
        fov_recompute = True

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        # Move the player character right one position.
        player.move(1, 0)
        fov_recompute = True



################################################################################
# Main Loop
################################################################################

# Create object representing the player character.
player = Object(0, 0, '@', 'player', libtcod.white, blocks=True)

# Define all objects in the console window.
objects = [player]

# Generate the map.
make_map()

#create the list of game messages and their colors, starts empty
game_msgs = []

# Introduction message to the player.
message('Grab the key, open the chest, then find your way out...', libtcod.green)

# Tell the FOV module which tiles block sight.
fov_map = libtcod.map_new(MAP_WIDTH, MAP_HEIGHT)
for y in range(MAP_HEIGHT):
    for x in range(MAP_WIDTH):
        libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight,
                                   not map[x][y].blocked)

fov_recompute = True

while not libtcod.console_is_window_closed():

    # Render the console window.
    render_all()

    # Draw the changes to the console window.
    libtcod.console_flush()

    # Remove the '@' left after the character moves.
    for object in objects:
        object.clear()

    # Exit the game if the player chooses to.
    exit = handle_keys()
    if exit:
        break
