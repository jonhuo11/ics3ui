# PConc A3Q3
# ICS3UI-01, Ms Harris
# Jonathan H
# Began: October 30, 2019
# Finished : Nov 7, 2019

'''
Your task, Create a flowchart and IPO chart, then write a program to create the
game of 31 or UNO. Create a trace table on one of your errors. You will be using
at least one card class and some basic graphics in PyGame. Don’t forget
instructions.
'''

# For this question I coded the game of UNO
# This game works with up to 4 players and follows standard UNO rules
# To play this game type in console how many players there should be, and it will start

# If I had more time for this assignment, I would have coded more action cards
# Currently the only action card is the reverse direction card

import pygame, sys, random
from pygame.locals import *

pygame.init()
FONT = pygame.font.SysFont(None, 26)

# Singleton class template for the GameManager
class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

# The game manager class is responsible for keeping track of game state and moving the game from turn to turn
# All game rule logic is placed under the game manager class
# All classes are attached to a game manager (the singleton instance)
class GameManager(metaclass=Singleton):
	def __init__(self, screen_size, players=[], deck=[], objects=[]):
		pygame.display.set_caption("UNO! by Jonathan H")
		self.screen_size = screen_size
		self.players = players

		self.event_text = ""

		# decks
		# the top of the play deck is the first item
		self.play_deck = Deck([])

		self.last_played_card = None
		self.current_player = None
		self.player_increment = 1

		self.done = False
		self.in_game = True
		self.objects = objects
		self.on_load()

	def end_game(self, winner):
		self.in_game = False
		self.event_text = "Player {} has won! Restart to play again".format(self.players.index(winner))

	# called when the game starts
	def start_game(self):
		# Print some welcome text
		print("Welcome to UNO! by Jonathan H")

		self.play_deck = Deck.gen_standard_deck(self)
		self.play_deck.shuffle()

		# ask the user how many players there should be
		print("Press Ctrl+C to exit at any time")
		player_count = int(input("Enter the amount of players (up to 4): "))
		if player_count > 4:
			player_count = 4
			print("Maximum player count is 4, autostarting with 4 players instead")
		elif player_count < 2:
			player_count = 2
			print("Minimum player count is 2, autostarting with 2 players instead")

		# generate the players and deal hands
		self.players = []
		for i in range(player_count):
			player = Player(self, Deck([]))
			self.players.append(player)

			for j in range(7):
				self.draw_top_card(player)

		print("UNO! game initialized with {} players!".format(player_count))

		# set the starting player
		self.current_player = self.players[0]

		self.in_game = True
		self.on_run()

	# calculates the next player based on the last_played_card
	def auto_give_move(self):
		# if there is no last played card, give the move to the first player
		if self.last_played_card == None:
			self.give_move(self.players[0])
		# if the last played card was a regular card, then
		elif type(self.last_played_card) == RegularCard:
			self.give_move(self.players[(self.players.index(self.current_player) + self.player_increment) % len(self.players)])
		elif isinstance(self.last_played_card, ReverseCard):
			self.give_move(self.players[(self.players.index(self.current_player) + self.player_increment) % len(self.players)])

	# called with a player as parameter, gives the specified player the next move
	def give_move(self, pl):
		# player can choose any card from their deck, this code checks if it is legal to play that card
		player = self.players[self.players.index(pl)]
		self.current_player = player

	# draws a card from the top of the deck and give it to the player
	def draw_top_card(self, pl):
		player = self.players[self.players.index(pl)]
		top_card = self.play_deck.cards[0]
		self.play_deck.cards.pop(0)
		player.deck.add_card(top_card)
		print("{} was given to player {}".format(top_card.debug(), self.players.index(pl)))

	def play_card_from(self, card, pl):
		self.last_played_card = card
		player = self.players[self.players.index(pl)]
		player.deck.cards.remove(card)
		self.play_deck.add_card(card)
		if isinstance(card, ActionCard):
			card.do_action()

	def can_play_card(self, card):
		# checks if a specified card can legally be played
		if card == None:
			return False

		# top card is the first card on the play deck
		# if both cards are regular cards, check if the number or color match
		if self.last_played_card == None:
			return True
		elif type(card) == RegularCard and type(self.last_played_card) == RegularCard:
			if card.number == self.last_played_card.number or card.color == self.last_played_card.color:
				return True
		elif (type(card) == RegularCard and isinstance(self.last_played_card, ActionCard)) or (isinstance(card, ActionCard) and type(self.last_played_card) == RegularCard):
			if card.color == self.last_played_card.color or card.color == "*" or self.last_played_card.color == "*":
				return True
		elif (isinstance(card, ActionCard) and isinstance(self.last_played_card, ActionCard)):
			if card.color == self.last_played_card.color or type(card) == type(self.last_played_card):
				return True
		# TODO: add special code for action cards
		return False
	def on_load(self):
		print("Game manager successfully loaded in...")
		self.display = pygame.display.set_mode(self.screen_size)
	def on_run(self):
		while not self.done:
			events = pygame.event.get()

			self.display.fill((255,255,255))

			for e in events:
				if e.type == pygame.QUIT:
					print("User exited, closing game")
					pygame.quit()
					sys.exit()

			if self.in_game:
				if self.last_played_card is not None:
					self.last_played_card.position = (0,0)
					self.last_played_card.render(events)

				# call the render function for the current player
				self.current_player.render(events)

				event_text_surface = FONT.render(self.event_text, False, (0,0,0))
				self.display.blit(event_text_surface, (0, self.screen_size[1]/2))
				player_text_surface = FONT.render("Player" + str(self.players.index(self.current_player)), False, (0,0,0))
				self.display.blit(player_text_surface, (self.screen_size[0]/2, 0))
			else:
				# TODO: game end code
				event_text_surface = FONT.render(self.event_text, False, (0,0,0))
				self.display.blit(event_text_surface, (0, self.screen_size[1]/2))

			pygame.display.flip()

# Player
class Player:
	def __init__(self, gm, deck):
		self.deck = deck
		self.horizontal_render_position = 0

		self.selected = None

		self.gm = gm
		gm.objects.append(self)

	# based on the players deck, check if they can move or not
	def can_move(self):
		can = False
		for card in self.deck.cards:
			if self.gm.can_play_card(card):
				can = True
				break
		if can:
			return True
		else:
			return False

	# show the "hand" (deck of cards) belonging to the specified player
	def render_hand(self, events):
		rel_pos = self.horizontal_render_position
		for card in self.deck.cards:
			ypos = self.gm.screen_size[1] - card.size[1]
			if card == self.selected:
				ypos = (self.gm.screen_size[1] * 0.95) - card.size[1]
			card.position = (rel_pos, ypos)
			card.render(events)
			rel_pos += card.size[0]

	# logic function called for each player during their turn
	def render(self, events):
		# Allow the player to scroll their deck left and right
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.horizontal_render_position += 0.3
		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.horizontal_render_position -= 0.3

		# Check if the player clicked on a card, if this is true then select that card
		for card in self.deck.cards:
			if card.check_click(events):
				if self.selected != card:
					self.selected = card
				else:
					self.selected = None

		# check if a move is possible
		if not self.can_move():
			self.gm.event_text = "No possible moves, press P to draw and pass"

			for e in events:
				if e.type == pygame.KEYDOWN and (e.key == pygame.K_p):
					self.gm.draw_top_card(self)

					self.gm.auto_give_move()
					self.gm.event_text = ""
		else:
			# If the player hits space, try to play the selected card
			for e in events:
				if e.type == pygame.KEYDOWN and (e.key == pygame.K_SPACE or e.key == pygame.K_RETURN):
					if isinstance(self.selected, Card):
						if self.gm.can_play_card(self.selected):
							self.gm.play_card_from(self.selected, self)

							# check for the uno and win event
							if len(self.deck.cards) == 1:
								print("UNO! for player {}".format(self.gm.players.index(self)))
								self.gm.auto_give_move()
								# TODO: display in game alert
							elif len(self.deck.cards) <= 0:
								print("player {} has won!".format(self.gm.players.index(self)))
								# TODO: end the game
								self.gm.end_game(self)
							else:
								self.gm.auto_give_move()

		# draw the deck relative to the horizontal_render_position
		self.render_hand(events)

# Parent class for all card types
class Card:
	standard_size = (75,100)
	def __init__(self, gm, position, size):
		self.position = position
		self.size = size

		self.gm = gm
		gm.objects.append(self)

	# check if the card was clicked
	def check_click(self, events):
		for e in events:
			# if the mouse was clicked, and the click was within the card area
			if e.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()

				# check bounds
				if pos[0] > self.position[0] and pos[0] < self.position[0] + self.size[0]:
					if pos[1] > self.position[1] and pos[1] < self.position[1] + self.size[1]:
						return True
				return False
		return False
	# render function attached to objects that can be drawn
	def render(self, events):
		BLACK = (0,0,0)
		# basic render function to be overriden by children
		pygame.draw.rect(self.gm.display, BLACK, (self.position[0], self.position[1], self.size[0], self.size[1]), 2)
	def debug(self):
		pass

# deck class will be used to represent each player's hand (each player has their own deck of cards during playtime)
# deck class will contain render function that handles drawing cards and the game UI
class Deck:
	def __init__(self, cards):
		# list of cards in the deck (queue data structure)
		# the first element in the queue is the "top" of the deck
		self.cards = cards
	# adds a card to the cards array, with amount
	def add_card(self, card, amt=1, top=True):
		# the top of the deck is the 0th position
		if top:
			for i in range(amt):
				self.cards.insert(0, card)
		else:
			for i in range(amt):
				self.cards.append(card)

	# randomizes deck order
	def shuffle(self):
		random.shuffle(self.cards)

	# function to return a standard UNO deck
	@staticmethod
	def gen_standard_deck(gm):
		deck = Deck([])

		# add standard cards 0-9 for each color
		# add yellow cards
		for i in range(10):
			deck.add_card(RegularCard(gm, (0,0), Card.standard_size, i, "yellow"))
		# add green cards
		for i in range(10):
			deck.add_card(RegularCard(gm, (0,0), Card.standard_size, i, "green"))
		# add red cards
		for i in range(10):
			deck.add_card(RegularCard(gm, (0,0), Card.standard_size, i, "red"))
		# add blue cards
		for i in range(10):
			deck.add_card(RegularCard(gm, (0,0), Card.standard_size, i, "blue"))

		# add reverse cards
		for i in range(2):
			deck.add_card(ReverseCard(gm, (0,0), Card.standard_size, "yellow"))
			deck.add_card(ReverseCard(gm, (0,0), Card.standard_size, "green"))
			deck.add_card(ReverseCard(gm, (0,0), Card.standard_size, "red"))
			deck.add_card(ReverseCard(gm, (0,0), Card.standard_size, "blue"))

		#[print("{} {}".format(card.color, card.number)) for card in deck.cards]
		return deck

# Regular card, number and color
class RegularCard(Card):
	def __init__(self, gm, position, size, number, color):
		super().__init__(gm, position, size)
		self.number = number
		self.color = color

	def render(self, events):
		BLACK = (0,0,0)
		RED = (255,0,0)
		GREEN = (0,255,0)
		YELLOW = (255,255,0)
		BLUE = (0,0,255)

		cl = RED
		if self.color == "red":
			cl = RED
		elif self.color == "green":
			cl = GREEN
		elif self.color == "yellow":
			cl = YELLOW
		elif self.color == "blue":
			cl = BLUE
		elif self.color == "*":
			cl = BLACK

		# draw the card base
		pygame.draw.rect(self.gm.display, cl, (self.position[0], self.position[1], self.size[0], self.size[1]))
		# draw the number on the card
		number_color = BLACK
		if self.color == "*":
			number_color = (0,0,0)
		number_surface = FONT.render(str(self.number), False, number_color)
		self.gm.display.blit(number_surface, (self.position[0] + (0.1 * self.size[0]), self.position[1] + (0.1 * self.size[1])))
	def debug(self):
		return ("{} {}".format(self.number, self.color))

# Special action card, ex: reverse, pick up 2, block turn
# Since each action card performs something unique, attach a callback function so that the action can be customized
class ActionCard(Card):
	def __init__(self, gm, position, size, color):
		super().__init__(gm, position, size)
		self.color = color

	def do_action(self):
		pass

	def render(self, events):
		pass

# Class for reverse card
class ReverseCard(ActionCard):
	def __init__(self, gm, position, size, color):
		super().__init__(gm, position, size, color)

	# go into the game manager and reverse the player_increment
	def do_action(self):
		self.gm.player_increment *= -1
	def render(self, events):
		BLACK = (0,0,0)
		RED = (255,0,0)
		GREEN = (0,255,0)
		YELLOW = (255,255,0)
		BLUE = (0,0,255)

		cl = RED
		if self.color == "red":
			cl = RED
		elif self.color == "green":
			cl = GREEN
		elif self.color == "yellow":
			cl = YELLOW
		elif self.color == "blue":
			cl = BLUE
		elif self.color == "*":
			cl = BLACK

		# draw the card base
		pygame.draw.rect(self.gm.display, cl, (self.position[0], self.position[1], self.size[0], self.size[1]))
		# draw the number on the card
		number_surface = FONT.render("Reverse", False, (0,0,0))
		self.gm.display.blit(number_surface, (self.position[0] + (0.1 * self.size[0]), self.position[1] + (0.1 * self.size[1])))
	def debug(self):
		return "{} {}".format(self.color, "Reverse")

# Code to run the game

gm = GameManager((1000,600))
gm.start_game()

# some old testing code that can be ignored
'''
card1 = RegularCard(gm, (10,50), (75,100), 6, "yellow")
card2 = RegularCard(gm, (90,50), (75,100), 2, "red")
card3 = RegularCard(gm, (90,50), (75,100), 1, "green")
card4 = RegularCard(gm, (90,50), (75,100), 7, "green")
card5 = RegularCard(gm, (90,50), (75,100), 9, "blue")
card6 = RegularCard(gm, (90,50), (75,100), 1, "yellow")
card7 = RegularCard(gm, (90,50), (75,100), 4, "blue")
card8 = RegularCard(gm, (90,50), (75,100), 7, "red")
card9 = RegularCard(gm, (90,50), (75,100), 2, "blue")
deck1 = Deck([card1, card2, card3, card4, card5, card6, card7, card8, card9])
deck2 = Deck([RegularCard(gm, (90,50), (75,100), 2, "blue"), RegularCard(gm, (90,50), (75,100), 2, "red"), RegularCard(gm, (90,50), (75,100), 2, "yellow")])
p1 = Player(gm, deck1)
p2 = Player(gm, deck2)

gm.players.append(p1)
gm.players.append(p2)
gm.current_player = gm.players[0]

gm.on_run()
'''
