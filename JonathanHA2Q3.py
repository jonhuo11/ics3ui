# ICS3UI-01 for Ms. Harris
# PConc A2Q#3
# Jonathan Huo
# Began: Sept 30, 2019
# Finished: Oct 3, 2019
'''
Please create a flowchart, and 2 or more functions, using random to create something
impressive with turtle. Once your teacher has briefly checked your flowchart AND given a check
mark in her class documentation, you should create this program using turtle and random. It
should be something small on the appropriate background (School GP please) thats similar, but
totally different from any of the examples in class or the ones in the reading materials.
Exception: You may use the random function below for star, if we do this in
class (it will earn a level 3)
'''

# Import the turtle, math, and random libraries
from turtle import *
import math
import random

# Set the screensize
setup(1000,800)

# A list of locations where flowers have previously been spawned
# Used to check for collisions later
flower_x_locations = []

# Function to draw a single flow. Takes a location, size, and petal angle
def draw_flower(location, size, angle):
	# Make a new turtle and hide its pointer. Set the speed to 5 for faster drawing speed
	turt = Turtle()
	turt.ht()
	turt.speed(5)

	# Draw the stem of the flower
	# Go to the flower location, pick up the pen while moving there
	turt.penup()
	# Go to the location of the stem
	turt.goto((location[0] + size/2 - (0.1 * size), location[1]))
	turt.pendown()

	# Set the color to the stem color
	turt.color("green", "lime")
	# Begin filling the stem in
	turt.begin_fill()

	# Tell the turtle to look south
	turt.seth(270)
	# Repeat twice, since the box has 4 sides and the loop defines a single 90 degree turn
	for i in range(2):
		# Draw the stem to be twice as long as the petal length (size)
		turt.forward(size * 2)
		# Make a 90 turn
		turt.left(90)
		# Make the width of the stem 10% the petal length (size)
		turt.forward(size * 0.1)
		# Turn 90 again
		turt.left(90)
	turt.end_fill()

	# Draw the petals of the sunflower
	# Move to the location, pick up the pen while doing so
	turt.penup()
	turt.goto(location)
	turt.pendown()
	# Look east (right)
	turt.seth(0)
	# Set the line color to brown, fill color to yellow
	turt.color("brown","yellow")
	# Begin filling in the petals
	turt.begin_fill()

	# Keep drawing petals until the turtle makes a full circle
	while True:
		# Make the petals as long as the size parameter
		turt.forward(size)
		# Align the petals at the specified petal angle
		turt.left(angle)
		# If the turtle has drawn a full circle of petals, then stop drawing more petals
		# Checks if the current turtle position is the same as the initial turtle position using distance
		if math.hypot(turt.pos()[0] - location[0], turt.pos()[1] - location[1]) < 10:
			break

	turt.end_fill()

	# Let the user know that a flower has been fully drawn
	print("A sunflower has bloomed!")

# Function to randomly generate flowers at different locations
def generate_flower():
	# Generate a random flower size, but has the same angle
	size = random.randint(50,70)
	angle = 108.4
	# Gets the window dimensions to know the spawnable areas
	sc = (window_width(), window_height())

	# This checks for collision conflicts with previously spawned flowers
	random_x = 0
	conflict = True
	while conflict:
		# Assume there is no conflict
		conflict = False
		# Generate a random x position for the flower
		random_x = random.randint(-sc[0]/2 + size, sc[0]/2 - size)
		# Check generated x position with previous x positions to see if there is a collision
		for location in flower_x_locations:
			# Using the distance between two points, check if there is a collision and if there is then find a new spawn point
			if abs(random_x - location) < size:
				conflict = True
	# Add the spawn location to the list of previous spawnpoints
	flower_x_locations.append(random_x)
	# Draw the new flower
	draw_flower((random_x, -sc[1]/2 + size*2), size, angle)

# Create a blue sky and green grass background and then draw a sun in the sky
bgcolor("cyan2")

# Draw a green grass field at the bottom of the screen
ht()
# Go to the corner and draw a rectangle, fill it with green
penup()
goto(-1000, -350)
seth(0)
pendown()
color("forest green")
begin_fill()
# Draw a rectangle to represent the grass field
forward(2000)
right(90)
forward(50)
right(90)
forward(2000)
right(90)
forward(50)
end_fill()

# Go to the place where the sun should be drawn and then draw a yellow circle
penup()
goto(-300, 300)
pendown()
color("gold")
begin_fill()
circle(50)
end_fill()

# Draws 10 flowers at random locations
for i in range(10):
	generate_flower()

# Tells the program to wait until user input to quit
input("Press any key to exit...")
