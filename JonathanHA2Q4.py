# ICS3UI-01 for Ms. Harris
# PConc A2Q#4
# Jonathan Huo
# Began: Sept 25, 2019
# Finished: Sept 26, 2019
'''
Using your knowledge of Pygame, create a landscape (grass, a house, trees, sky with either
sun and cloud or moon and stars) and anything else you want to add.
'''

# Import the pygame library and some essential files
import pygame
from pygame.locals import *
# Import the random library
import random
# Import the base64 and IO library for image processing
import base64
import io

# Initialize all the pygame modules
pygame.init()
# Initialize the display with size 500x500, no flags, and a depth of 32
DISPLAY = pygame.display.set_mode((500, 500), 0, 32)

# Variables to store the RGB tuples of commonly used colors, this is for simplicity
white = (255,255,255)
blue = (0,255,255)
green = (0, 128, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
brown = (165, 42, 42)
black = (0,0,0)

# Fill the background with white
DISPLAY.fill(white)

# A function to contain all the code for drawing the background
def background():
    # Draw the sky as a light blue rectangle
    pygame.draw.rect(DISPLAY, blue, (0, 0, 500, 450))

    # Draw a house, made up of a square body and a triangle roof
    # Draw the red square body
    pygame.draw.rect(DISPLAY, red, (190, 275, 250, 200))
    # Draw a brown roof, which is a triangle using three points
    pygame.draw.polygon(DISPLAY, brown, ((150, 275), (480, 275), (315, 200)))
    # Draw a brown door, which is a rectangle
    pygame.draw.rect(DISPLAY, brown, (250, 350, 75, 100))
    # Draw a doorknob, which is a black circle
    pygame.draw.circle(DISPLAY, black, (310, 400), 7)
    # Draw a square window, which is a rectangle
    pygame.draw.rect(DISPLAY, blue, (350, 350, 60, 60))

    # Draw the ground as a green rectangle
    pygame.draw.rect(DISPLAY, green, (0, 450, 500, 50))
    # Draw the sun as a yellow circle in the top left corner
    pygame.draw.circle(DISPLAY, yellow, (60, 50), 40)

    # Draw 2 clouds in the sky as 3 circles grouped together
    # Three circles combine to form one cloud. Having 3 circles gives the cloud more shape
    pygame.draw.circle(DISPLAY, white, (110,70), 30)
    pygame.draw.circle(DISPLAY, white, (110 + 35,70), 25)
    pygame.draw.circle(DISPLAY, white, (110 - 35,70), 25)
    pygame.draw.circle(DISPLAY, white, (370, 50), 30)
    pygame.draw.circle(DISPLAY, white, (370 + 35, 50), 25)
    pygame.draw.circle(DISPLAY, white, (370 - 35, 50), 25)

    # Draw blades of grass on the bottom of the screen as lines
    # Grass blades are spaced out by 6px
    for x in range(0, 500, 5):
        # Each blade is offset by a random number to give realism for a level
        pygame.draw.line(DISPLAY, green, (x, 450), (x, 420 + random.randint(0,15)), 3)

# Draw the background
background()

# Load an image of a plane (stored as base 64 data) using the base64 and io modules
image = """
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAEnElEQVR4nO2Wa1BUZRjH/+fsnnP27C67gKwiAoLcckGMQldmEcZQZ0xH0iK1shzHstIm1Myh0QE1iUEkFS85TI4wVIRkgFmN1qiTlyFGVFTwsqyQoQuI4sLezu6+bx8c08xRaMhP/D69t+f5/9/LPPMCgwwyyH2YkRExxuTUtAxeEHwGIiEvCOqctes2R0Y/k9ingLkLl39dVnOCxicYZg2EgfyCzSWWztte/4BhkX0K4AXRd01BSUvFjyfd6S/PWQ6AMSQZp56qbzDPzpj3bn/Ep81IX2i5eYfmF+6s6ZfrkPCYlOK9Rzx155rpl3u+OmJqveE+UVt/lRcEsa85gkPC4mrPNNmar3XQUdGxqY9bK3t4wNrd1eqSPAp9/PiJSYbnwrRqBZubm7sJlLLJE1OmTJ48ZWaPzR5otzu6AnRDR9psvd2glNyL53hBlb+1+GBgUHDQsWPH68p271j9OAPyhwd4QaH20wWFXrl2C5ycRaC/iA+WvL+ek7MI0OnQ0tKKir2VaLdcR3V1NbLXbvim3XJ9lUwu5+QymXzegsVrYuPG6DVqBS5dOHs6bfLUV609VqvZbDZ1dXY0A6AP6jEPdkZFRD2b81lROQTtqPLS4i3GlEnpEyaMj3LYHZAkBziOgyiqINm7MSk5ES6nC5JbAiEElFAwLAue58FzPAil8Ho9d+cAUEJQUlp6efu2ouyrZlPFvVP728Brr89/Ly+/oLC8cv/JjbnZS9OmTlu0aPHSTI3Wj/F4KTpu94JhGPj6KMDJWVAKEEpBCb3fpnfblFJQUBACUFC0mJpgungOrc1NeCVjDgghDevX5WQ2nm84zCiVKu3mLUXFcQmJxpUrVnx0/OihcgA0Nv75l16YkfGJPt4wLnDoEPhplDjT0AQPK0IpCnA57SCEghIvGIaFJLnAcTzsth4Iogoq9d1SQrwE1eW7EB6lR8zosYiMGAmtigdx2+nWwrwVjDElLSM0LDziu2/Ldkgup/XBKxFVPsM3fPF9W3iwjgkd5ot3FsxFnGEK9GMScbO9DW63BJlMDoZlQbxeCKISHrcEnheg1viC0nvXTcEA4Dk5/LRq6Px94Ojtbt+5ddPH/3gDj0JUaUYMD41M1gWGJvR0d0pR0TGxkdH66RQQHE4nJKcTFBRyjodCoYBCIYIBXJcbG37wuF29hFA3K4OTl7G9hLitXTc7/zRduXLhRtsfZyml3icaeBRKtSYkfdH6ekbwCVAKPCKDfenPB6qOMq7Oxk7L9XrTpcb9Toetoy+5+m1g6IiICcaZi3fzmuGjvR4vLM2nDp05WpnVe/vGqf5vpR8GOF7wSZ3+xqdjkmYssbk8MvPF07X1v5Zn3bKYD/8X4X4Z0I81zJz11rJtvMo/pOn82cbfDpSubjOfq8JDRWXA0foNCf4wK2/fnpo6ujK3pCV6rHEBwzD/Kt//C+OSUmZX/VJnLSr9qcOQOj2TlcmFpyIcGDQiKu/z7fuqDtbeeXHW/GyOH5jPyRNRqlR+q7LWbDr2+4U7b76dWSgq1bqnIgwAIWERCWUV1aeXrcrZpfEdEvrUhAcZZBAAfwEF7OG8FFqpewAAAABJRU5ErkJggg==
"""
# Load the base64 image into pygame
plane = pygame.image.load(io.BytesIO(base64.b64decode(image)))
# Variable to store the x position of the plane
plane_x = 0

# Runs the pygame event loop until a quit event is detected, then the program exits
done = False
while not done:
    # Iterate through each event in the event queue and see if a QUIT event occurred
    for event in pygame.event.get():
        # If a QUIT event occurs, then exit pygame and the program
        if event.type == pygame.QUIT:
            done = True
    # Level 4 animation
    # Draw a plane flying across in the sky randomly
    # Keep refreshing a piece of the sky so that the drawing from the previous frame is covered.
    pygame.draw.rect(DISPLAY, blue, (0, 105, 500, 90))
    # Draw the plane moving
    DISPLAY.blit(plane, (plane_x,130))
    # Update the plane's x position, if it goes out of the window, make it come back after a random amount of time
    if (plane_x > 500):
        plane_x = random.randint(-800,-100)
    else:
        # In normal circumstances, just keep moving the plane to the right
        plane_x += 0.05

    # Refresh the pygame display window
    pygame.display.update()
