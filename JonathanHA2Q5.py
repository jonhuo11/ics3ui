# ICS3UI-01 for Ms. Harris
# PConc A2Q#5
# Jonathan Huo
# Began: Sept 26, 2019
# Finished: Sept 30, 2019
'''
WOW me with your Pygame knowledge. Create a flowchart and then write a program that
uses any valid function not already used in this assignment.
'''

'''
For this question, I am going to make a whackamole game. The user has
15 seconds to whack as many moles as possible (by clicking).

The python function I am using in this game is the sorted() function. I am going to take
the user's scores and then sort them in order from highest to lowest. This function is
used on line 155.

Note that I am choosing not to store past scores in a separate text file because that would
create security problems. Not all users want a new file created on their system, and some
systems do not give permission for my program to do so. This means that the game will reset
past scores every time it is closed. So to test my feature keep the game open and play a few rounds!
'''

# Import the pygame library and some essential files
import pygame
from pygame.locals import *
# Import the random and math library
import random
import math
# Import the base64 and IO library for image processing
import base64
import io

# Initialize all the pygame modules
pygame.init()
# Give our game window a title
pygame.display.set_caption("WHACKAMOLE by Jonathan H")
# Initialize the display with size 1000x1000, no flags, and a depth of 32
DISPLAY = pygame.display.set_mode((1000, 1000), 0, 32)

# Variables to store the RGB tuples of commonly used colors, this is for simplicity
white = (255,255,255)
blue = (0,255,255)
green = (0, 128, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
brown = (165, 42, 42)
black = (0,0,0)

# Store the image of the mole sprite as a base64 string so we dont need a separate file
mole_image = '''
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
'''
# Load the string into an image using the python IO and base64 modules
mole_loaded = pygame.image.load(io.BytesIO(base64.b64decode(mole_image)))
# Create a comic sans font with font size 60
comic_sans = pygame.font.SysFont("Comic Sans MS", 40)
# Mole spawnpoint coordinates. Black circles are drawn here.
mole_spawns = [
    (166, 166), (499, 166), (832, 166),
    (166, 499), (499, 499), (832, 499),
    (166, 832), (499, 832), (832, 832)
]
# The radius of the black circles to draw.
spawn_size = 75
# The current position of the mole stored as a tuple (x,y)
current_mole_pos = mole_spawns[random.randint(0, len(mole_spawns) - 1)]
# A variable to keep track of the current score this round
score = 0
# An array to keep track of scores from past rounds. This is not stored on the filesystem, it resets every time game is closed.
# We will fill this with some empty scores to avoid an index out of range error.
scores = ["-1:::Empty", "-1:::Empty", "-1:::Empty"]

# A variable that stores the time limit that the user has to score points.
max_time = 15
# start_time is used by the program to keep track of when new rounds are started so we can calculate time elapsed
start_time = 0
# Keeps track of the name the user typed in
name = ""

# This function draws the menu background. Called when game is in the menu screen
def menu_background():
    DISPLAY.fill(blue)
    # Some description text and instructions
    DISPLAY.blit(comic_sans.render("WHACKAMOLE by Jonathan H", False, red), (30,20))
    DISPLAY.blit(comic_sans.render("PRESS ENTER TO PLAY!", False, brown), (30,70))
    DISPLAY.blit(comic_sans.render("Click as many moles as you can in 15 seconds.", False, brown), (30,120))
    DISPLAY.blit(comic_sans.render("TOP 3 SCORES:", False, green), (30,175))

    # Next three lines display the top three high scores that are stored in the scores array
    # Note this resets when the game is closed, so keep it running
    # Use the split() function to separate the score and the name into an array
    # The first element of this array is the score, second is the name
    score1 = scores[0].split(":::")
    score2 = scores[1].split(":::")
    score3 = scores[2].split(":::")
    DISPLAY.blit(comic_sans.render("1) " + score1[1] + ", " + score1[0], False, black), (30,220))
    DISPLAY.blit(comic_sans.render("2) " + score2[1] + ", " + score2[0], False, black), (30,290))
    DISPLAY.blit(comic_sans.render("3) " + score3[1] + ", " + score3[0], False, black), (30,360))
# This function draws the ingame background. Called when the game is running
def background():
    DISPLAY.fill(blue)
    # Draw a black circle at every possible mole spawn point
    for spawn in mole_spawns:
        pygame.draw.circle(DISPLAY, black, spawn, spawn_size)

# Some state variables to keep track of what state the game is in
# If done is true, then the game has been exited and the window is closed
done = False
# in_game decides which screen to show
# If in_game is true, then the game screen is shown. If not then the menu screen is shown
in_game = False
# Initialize the start_time variable
start_time = pygame.time.get_ticks()

# While done is false, the game will run. Setting done to true will close the window.
# Basically the main game loop
while not done:
    # Get an array of all pygame events that have happened this tick/cycle
    # The program looks for keypress and other events in this array later
    events = pygame.event.get()

    # If in_game is true, then render the game scene
    if in_game:
        # Get the time elapsed since starting the round
        time_passed = (pygame.time.get_ticks() - start_time) / 1000
        # If the time passed is more than the maximum time allowed
        if time_passed > max_time:
            DISPLAY.fill(blue)
            # Draw the score, game over, and name entry text boxes
            DISPLAY.blit(comic_sans.render("TIME LEFT: 0" + "     SCORE: " + str(score), False, red), (30,20))
            DISPLAY.blit(comic_sans.render("GAME OVER!", False, red), (340, 260))
            DISPLAY.blit(comic_sans.render("NAME: " + name + "_", False, red), (5, 300))

            # Check if a noteworthy event occurred
            for e in events:
                # Record keypresses
                if e.type == pygame.KEYDOWN:
                    # If enter is pressed, submit the score and go to the main menu
                    if e.key == pygame.K_RETURN:
                        # Add the new score and the username to the scores array
                        # We separate scores/username with a few colons so we know where to split it later
                        # If the user did not input a name, set name to Anonymous
                        if (len(name) < 1):
                            name = "Anonymous"
                        scores.append(str(score) + ":::" + name)

                        # This is where the sorted() function is used
                        # I use the sorted() function to sort high scores in order from highest to lowest
                        # The sorted() function works on strings as well, so the scores are sorted alphabetically
                        # Since numbers are sorted before letters, this system works
                        # Make sure to reverse the sorted array so it is ordered correctly
                        # I separated the score from the name using colons and we split them later when printing out scores
                        scores = sorted(scores, reverse=True)

                        # Reset the variables used to track score/username since the round ended
                        name = ""
                        score = 0

                        # Change in_game to false, so the game goes to the menu screen
                        in_game = False
                    # If the delete key is pressed, remove the last character from name
                    elif e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        # If a regular key is pressed, add it to the name unless the name is longer than 15 characters already
                        if(len(name) < 15):
                            # e.unicode returns a unicode version of the typed character
                            name += e.unicode
        # Draw the regular in game scene
        else:
            background()
            # Draw the timer and score text
            DISPLAY.blit(comic_sans.render("TIME LEFT: " + str(round(max_time - time_passed, 1)) + "     SCORE: " + str(score), False, red), (30,20))
            # Draw the mole sprite at its current position
            DISPLAY.blit(mole_loaded, (current_mole_pos[0]-70, current_mole_pos[1]-130))
            # If the mouse is pressed, check if the mole was clicked
            if pygame.mouse.get_pressed()[0]:
                # Gets the mouse position (x,y) at the time of the click
                mouse_pos = pygame.mouse.get_pos()
                # If the distance from the click point to the mole's location is less than the radius of the black circle then the mole was whacked
                # Uses math.hypot() to solve the pythagorean theorem which gives the distance between two points
                if math.hypot(mouse_pos[0] - current_mole_pos[0], mouse_pos[1] - current_mole_pos[1]) < spawn_size:
                    # Creates a copy of the mole spawns array without the last spawn point so no duplicate spawns occur
                    others = mole_spawns.copy()
                    others.remove(current_mole_pos)
                    # Pick a random new spawn
                    current_mole_pos = others[random.randint(0, len(others) - 1)]
                    # Increase score by 1
                    score += 1
    # If in_game is false, then load the menu screen
    else:
        # Draws the menu background
        menu_background()
        # Checks for noteworthy events
        for e in events:
            # If the enter key is pressed, then load into a new round!
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    # Set in_game to true and reset the timer
                    in_game = True
                    start_time = pygame.time.get_ticks()
    # Searches for a quit event to see if the game should be exited
    for e in events:
        if e.type == pygame.QUIT:
            done = True
    # Updates the game display window
    pygame.display.update()
# When the program finishes, exit() the application
exit()
