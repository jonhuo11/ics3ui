'''

	README by @jonhuo11

		There are sound effects! Turn on your audio.

		GameManager.run() is the starting point for this program, contains the mainloop

		Put code for testing inside of GameManager.update(), this is called every tick

'''


import pygame, random, os, sys
from enum import Enum
from pygame.locals import *

pygame.init()
pygame.mixer.init()

class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

class GameManager(metaclass=Singleton):

	# global static variables for convenience
	screen_size = (1000, 600)
	font = pygame.font.SysFont(None, 30)
	asset_folder = os.path.join(os.path.dirname(__file__), "assets")

	def __init__(self):
		# pygame initialization
		self.display = pygame.display.set_mode(GameManager.screen_size)
		self.clock = pygame.time.Clock()
		self.objects = pygame.sprite.Group()

		# sound effect
		self.move_sound = pygame.mixer.Sound(os.path.join(GameManager.asset_folder, "movesound.wav"))

		# CustomDie(dimensions, position)
		self.board = None
		self.die = CustomDie(tuple(round(i * 0.25) for i in GameManager.screen_size), (GameManager.screen_size[0] - (GameManager.screen_size[0] * 0.2), GameManager.screen_size[1] * 0.5))
		self.objects.add(self.die)

		# players
		self.blue = Player(self, PlayerColors.BLUE, 0)
		self.red = Player(self, PlayerColors.RED, 0)

		self.objects.add(self.blue)
		self.objects.add(self.red)

		# game state variables
		self.running = True
		self.in_game = True
		self.turn = self.blue # defines which players turn it is
		self.winner = None

	# runs the program
	def run(self):
		pygame.event.pump()
		self.start(pygame.event.get())

		# gameloop
		while self.running:
			self.clock.tick(60)
			pygame.event.pump()
			self.update(pygame.event.get())
			pygame.display.flip()

		pygame.exit()
		sys.exit()

	# start
	def start(self, events):
		self.board = Board.generate_board(self, 6)

		# set the players starting tiles
		self.blue.move_to_tile(36)
		self.red.move_to_tile(36)

	# update
	def update(self, events):
		for e in events:
			if e.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		# main game logic code

		# while in game...
		if self.in_game:
			# update
			self.objects.update(events)

			# if the player presses the space button, roll the dice
			for e in events:
				if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
					roll = self.die.random()
					# move the player how many tiles they rolled
					self.move_player(roll)

					# set the next player to have the current turn
					self.turn = self.blue if self.turn != self.blue else self.red

			# draw
			self.board.update(events)
			self.objects.draw(self.display)

			# info text rendering
			self.show_text("It is {} player's turn".format(self.turn.name), (GameManager.screen_size[0] - (GameManager.screen_size[0] * 0.3), GameManager.screen_size[1] * 0.3))
			self.show_text("Press space to roll dice", (GameManager.screen_size[0] - (GameManager.screen_size[0] * 0.3), GameManager.screen_size[1] * 0.75))

			pygame.time.delay(50)
		else:
			self.show_text("Player {} has won".format(self.winner.name), (GameManager.screen_size[0] - (GameManager.screen_size[0] * 0.3), GameManager.screen_size[1] * 0.1))

	# function for moving the player x tiles, can be forward or backward
	def move_player(self, amt):
		# starting and ending ids
		start = self.turn.on.id
		end = start - amt

		# if the player moves onto the end tile, end the game
		if end <= self.board.end.id:
			self.turn.move_to_tile(self.board.end.id)
			self.winner = self.turn
			self.in_game = False
		elif end >= self.board.start.id:
			end = self.board.start.id
		# check if the tile has a connection
		elif len(self.board.get_tile(end).links) > 0:
			self.turn.move_to_tile(self.board.get_tile(end).links[0][0].id)
		# if nothing special, move amt forward
		else:
			self.turn.move_to_tile(end)

		# play the move sound
		self.move_sound.play()

	# helper function for drawing text
	def show_text(self, text, pos):
		self.display.blit(GameManager.font.render(text, False, (0,0,0)), pos)

# enum of connection types
class LinkTypes(Enum):
	REGULAR = 0
	LADDER = 1
	SNAKE = 2

# tiles on the board
# snakes, ladders, and links are represented by pointers
class Tile:
	def __init__(self, gm, id, position, size, color, links):
		self.game_manager = gm
		self.id = id
		self.position = position
		self.size = size
		self.color = color
		# links is an array of tuples containing tiles that can be travelled to from that tile
		# (tile, type) type is a string defining link type
		self.links = links

	# returns the center of the tile
	def get_center(self):
		return (self.position[0] + self.size[0]//2, self.position[1] + self.size[1]//2)

	# update render function draws the tile on the board
	def update(self):
		# draw the board at the position, at the same size, with the color
		self.render()

	def render(self):
		# draw the background of the tile
		pygame.draw.rect(self.game_manager.display, self.color, (self.position, self.size))

		# draw the id of the tile so it is numbered
		self.game_manager.display.blit(GameManager.font.render(str(self.id), False, (0,0,0)), (self.position[0], self.position[1]))

# this class represents the gameboard
# gameboard is made up of tiles with a connection to each other
class Board(metaclass=Singleton):
	def __init__(self, gm, tiles, start, end):
		self.game_manager = gm

		# tiles is an array of tile objects
		self.tiles = tiles

		# start and end tiles so you can check if someone has won
		self.start = start
		self.end = end

	# update function calls the render function on each tile in the board
	def update(self, events):
		# fill the screen with white background
		self.game_manager.display.fill((255,255,255))

		# draw all tiles
		for tile in self.tiles:
			tile.update()

		# draw all connections between tiles
		for tile in self.tiles:
			for link in tile.links:
				# if it is a snake, draw a snake
				if link[1] == LinkTypes.SNAKE:
					pygame.draw.line(self.game_manager.display, (204,0,0), tile.get_center(), link[0].get_center(), 10)
				# if it is a ladder, draw a ladder
				elif link[1] == LinkTypes.LADDER:
					pygame.draw.line(self.game_manager.display, (0, 153, 0), tile.get_center(), link[0].get_center(), 10)

	# get a tile from id
	def get_tile(self, id):
		for t in self.tiles:
			if t.id == id:
				return t
		return None

	# generate a snakes and ladder board with the given amount of tiles
	# add random connections between boards, only 30% of tiles have connections
	@staticmethod
	def generate_board(gm, length):
		# list of tiles to be added to the board
		tiles = []
		last_tile = None
		# tile ids to be assigned
		ids = 1

		# loop through and create width * height board, each tile is spaced out evenly
		# compare width and height of the screen to find smaller one, then use that to size the board square
		dimension = GameManager.screen_size[0] if GameManager.screen_size[0] < GameManager.screen_size[1] else GameManager.screen_size[1]
		for y in range(0, dimension, dimension//length):
			for x in range(0, dimension, dimension//length):
				new_tile = Tile(gm, ids, (x, y), (dimension//length, dimension//length), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), [])
				tiles.append(new_tile)
				ids += 1

		# randomly create snakes and ladder connections between tiles
		max_links = round(0.3 * (len(tiles)/2))
		# list of tiles that were not already chosen
		unchosen = tiles.copy()[1:-1]
		random.shuffle(unchosen)
		for i in range(max_links):
			a = unchosen.pop()
			b = unchosen.pop()
			# check which tile out of a and b is first
			first = a if a.id > b.id else b
			other = a if first is b else b
			# 50% chance of creating a snake, 50% chance of creating a ladder
			# create a snake
			if not bool(random.getrandbits(1)):
				other.links.append((first, LinkTypes.SNAKE))
			# create a ladder
			else:
				first.links.append((other, LinkTypes.LADDER))

		# return a new board with the given tiles
		return Board(gm, tiles, tiles[len(tiles) - 1], tiles[0])

# enum of player colors
class PlayerColors(Enum):
	BLUE = 0
	RED = 1

# class to hold player data
class Player(pygame.sprite.Sprite):
	asset_folder = os.path.join(os.path.dirname(__file__), "assets")

	def __init__(self, gm, color, on):
		self.game_manager = gm

		# decide which sprite to use depending on what color the player is
		image = pygame.image.load(os.path.join(Player.asset_folder, "blueavatar.png"))
		if color == PlayerColors.BLUE:
			image = pygame.image.load(os.path.join(Player.asset_folder, "blueavatar.png"))
			self.name = "blue"
		elif color == PlayerColors.RED:
			self.name = "red"
			image = pygame.image.load(os.path.join(Player.asset_folder, "redavatar.png"))

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(image, (int(GameManager.screen_size[0] * 0.05), int(GameManager.screen_size[1] * 0.05)))
		self.rect = self.image.get_rect()

		# set the player's tile they are on
		self.on = on
		if self.on != None and self.on != 0:
			self.rect.center = self.on.get_center()

	# called on each game update
	def update(self, events):
		pass

	# move the player to a coordinate
	def move_to_tile(self, id):
		self.on = self.game_manager.board.get_tile(id)
		self.rect.center = self.on.get_center()

# @jonhuo11
# Made slight modification to dice class to fix a bug with image asset importation

# This is a die class created by ICS3U-02 2018-19, Teacher Ms. Harris
# This is a whole class one day (exploded into 4 days assignment) - formative
# Shell added by Ms. Harris (Teacher) April 7/10
# Modifications:
# Apr. 8/19 - Number 9 Added by Ziv, Sowad, and Victor
# Apr. 15/19 - Number 3 Added by Karan, Ciara, and Thomas
# 2019/04/16 - Ziv - fixed up implementation
# added 7-9 Sri, Simha, Karan
# May 8/19 - Sri - addressed problems mentioned below
class DieClass(pygame.sprite.Sprite):
	# small modification added to fix sprite imports
	asset_folder = os.path.join(os.path.dirname(__file__), "assets")

	# Initialize class
	def __init__(self, dimensions, position):
		super().__init__()
		# Transforming and applying images
		self.one_image = pygame.image.load(os.path.join(DieClass.asset_folder, "one.png"))
		self.two_image = pygame.image.load(os.path.join(DieClass.asset_folder, "two.png"))
		self.three_image = pygame.image.load(os.path.join(DieClass.asset_folder, "three.png"))
		self.four_image = pygame.image.load(os.path.join(DieClass.asset_folder, "four.png"))
		self.five_image = pygame.image.load(os.path.join(DieClass.asset_folder, "five.png"))
		self.six_image = pygame.image.load(os.path.join(DieClass.asset_folder, "six.png"))
		self.seven_image = pygame.image.load(os.path.join(DieClass.asset_folder, "seven.png"))
		self.eight_image = pygame.image.load(os.path.join(DieClass.asset_folder, "eight.png"))
		self.nine_image = pygame.image.load(os.path.join(DieClass.asset_folder, "nine.png"))

		self.one_image = pygame.transform.scale(self.one_image, dimensions)
		self.two_image = pygame.transform.scale(self.two_image, dimensions)
		self.three_image = pygame.transform.scale(self.three_image, dimensions)
		self.four_image = pygame.transform.scale(self.four_image, dimensions)
		self.five_image = pygame.transform.scale(self.five_image, dimensions)
		self.six_image = pygame.transform.scale(self.six_image, dimensions)
		self.seven_image = pygame.transform.scale(self.seven_image, dimensions)
		self.eight_image = pygame.transform.scale(self.eight_image, dimensions)
		self.nine_image = pygame.transform.scale(self.nine_image, dimensions)

		self.image = self.one_image

		self.rect = self.image.get_rect()
		self.rect.center = position

	#Change dice object to a random number 1-10
	def random(self):
		choice = random.choice(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"])
		if choice == "one":
			self.one()
		if choice == "two":
			self.two()
		if choice == "three":
			self.three()
		if choice == "four":
			self.four()
		if choice == "five":
			self.five()
		if choice == "six":
			self.six()
		if choice == "seven":
			self.seven()
		if choice == "eight":
			self.eight()
		if choice == "nine":
			self.nine()

	# get values and draw the one
	def one(self):
		self.image = self.one_image
	# get values and draw the two
	def two(self):
		self.image = self.two_image
	# get values and draw the three
	def three(self):
		self.image = self.three_image
   # get values and draw the four
	def four(self):
		self.image = self.four_image
   # get values and draw the five
	def five(self):
		self.image = self.five_image
   # get values and draw the six
	def six(self):
		self.image = self.six_image
   # get values and draw the seven
	def seven(self):
		self.image = self.seven_image
   # get values and draw the eight
	def eight(self):
		self.image = self.eight_image
   # get values and draw the nine
	def nine(self):
		self.image = self.nine_image
	#Set position of die
	def set_position(self, x, y):
		self.rect.center = [x,y]

	# update function
	def update(self, *args):
		pass

# some modifications to the dice class
# makes it so that the roll also returns a number
class CustomDie(DieClass):

	# overrides the random method
	def random(self):
		choice = random.randint(1,10)
		if choice == 1:
			self.one()
		if choice == 2:
			self.two()
		if choice == 3:
			self.three()
		if choice == 4:
			self.four()
		if choice == 5:
			self.five()
		if choice == 6:
			self.six()
		if choice == 7:
			self.seven()
		if choice == 8:
			self.eight()
		if choice == 9:
			self.nine()

		return choice

# code to run the game
game_manager = GameManager()
game_manager.run()
