'''

    guess_who.py Created by Jonathan H, ZhiShu, Kyle, Hossein, and Jonathan B

    This is a 2 player guess who game. The other player should look away when it is not their turn.

    Some notes about the game:
    - to type into a text field, make sure you click on it first and wait for the caret to appear
    - our board is 8*3 instead of 4*6, works out to 24 characters

'''


import json
import os
import pygame
import sys
import random
from enum import Enum

pygame.init()
pygame.mixer.init()


# Singleton class template
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# enum of scenes
class Scenes(Enum):
    IN_GAME = 1
    IN_MENU = 2
    IN_HELP = 3
    IN_OPTIONS = 4


# enum of stages in the turn
class TurnStages(Enum):
    OUT_OF_SCENE = 1
    CHOOSING = 2
    ASKING = 3
    RESPONDING = 4
    FLIPPING = 5
    WIN = 6


class GameManager(metaclass=Singleton):
    # static variables linking to assets
    asset_folder = "assets"

    def __init__(self):
        # essential settings for pygame runtime
        self.window_size = (1200, 800)
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.fps = 60

        # game settings and variables
        self.running = True
        self.scene = Scenes.IN_MENU

        # textboxes
        self.status_text = TextBox("", 30, (0, self.window_size[1] * 0.2), self.screen, False, True, 50, "", "")
        self.status_text_2 = TextBox("", 30, (0, self.window_size[1] * 0.25), self.screen, False, True, 50, "", "")
        self.ask_text = TextBox("", 30, (0, self.window_size[1] * 0.92), self.screen, True, True, 50, "Enter question or guess: ", "")
        self.response_text = TextBox("", 30, (0, self.window_size[1] * 0.5), self.screen, True, True, 50, "Enter response: ", "")

        # turn settings
        self.turn = None
        self.turn_stage = TurnStages.OUT_OF_SCENE
        self.turn_timer = None  # TODO: hook up a pygame timer
        self.turn_data = False  # json data that is propagated to the next turn
        self.winner = None

        # player boards
        self.player1 = None
        self.player2 = None

        # celebs group
        self.celebs_group = pygame.sprite.Group()
        self.celebs_group_2 = pygame.sprite.Group()

    # on game execution
    def on_run(self):
        self.on_start()
        while self.running:
            self.clock.tick(self.fps)
            pygame.event.pump()
            self.update(pygame.event.get())
            pygame.display.flip()
        pygame.quit()
        sys.exit()

    # on initialization
    def on_start(self):
        pass

    # called when a new game starts
    def on_new_game(self):
        self.celebs_group.empty()
        self.celebs_group_2.empty()
        self.turn_data = False

        celebs = GameManager.load_celeb_assets(self)
        celebs2 = GameManager.load_celeb_assets(self)
        board = Board.gen_board(self, celebs[0], celebs[1], (3, 8))
        board2 = Board.gen_board(self, celebs2[0], celebs2[1], (3, 8))
        self.player1 = board
        self.player2 = board2

        # add the celebs to the sprite group
        for col in self.player1.board:
            for item in col:
                self.celebs_group.add(item[0])
        for col in self.player2.board:
            for item in col:
                self.celebs_group_2.add(item[0])

        r1 = self.player1.board[random.randint(0, len(self.player1.board) - 1)][
            random.randint(0, len(self.player1.board[0]) - 1)]
        r2 = self.player2.board[random.randint(0, len(self.player1.board) - 1)][
            random.randint(0, len(self.player1.board[0]) - 1)]
        self.player1.selected = r1[0]
        self.player2.selected = r2[0]

        # set the current player to have the turn
        self.turn = self.player1
        self.turn_stage = TurnStages.CHOOSING
        nm = ""
        if self.turn == self.player1:
            nm = "Player 1"
        else:
            nm = "Player 2"
        self.scene = Scenes.IN_GAME

        # reset text positions and content
        self.status_text.coords = (0, self.window_size[1] * 0.88)
        self.status_text_2.coords = (0, self.window_size[1] * 0.25)
        self.status_text_2.set_text("")
        self.status_text.set_text("{}'s turn to ask a question".format(nm))
        self.ask_text.set_text("", "Enter question or guess: ")
        self.response_text.set_text("", "Enter response: ")

    # while in game
    def update(self, events):
        # exit if the user quits
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False

        # clear the scene
        self.screen.fill((0, 0, 0))

        # render based on what scene it is
        if self.scene == Scenes.IN_GAME:
            self.in_game(events)
        elif self.scene == Scenes.IN_MENU:
            self.in_menu(events)
        elif self.scene == Scenes.IN_HELP:
            self.in_help(events)

    # in main menu scene
    def in_menu(self, events):
        self.screen.fill((0, 170, 255))
        myfont = pygame.font.SysFont("Impact", 110)
        secondfont = pygame.font.SysFont("Impact", 50)
        BLACK = (0, 0, 0)
        label = myfont.render("﻿Game Rules", 12, BLACK)
        first_line = myfont.render("Guess Who?", 12, (255, 10, 0))
        second_line = secondfont.render("Play!", 12, (BLACK))
        third_line = secondfont.render("Instructions", 12, (BLACK))
        pygame.draw.rect(self.screen, (255, 10, 0), (520, 397, 120, 70))
        pygame.draw.rect(self.screen, (255, 10, 0), (445, 487, 280, 70))
        self.screen.blit(first_line, (300, 200))
        self.screen.blit(second_line, (530, 400))
        self.screen.blit(third_line, (460, 490))
        pygame.display.update()
        self.clock.tick(self.fps)  # Clock
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                c = 460
                d = 490
                if c < mouse[0] < c + 300 and d < mouse[1] < d + 80:
                    self.scene = Scenes.IN_HELP
                elif 520 < mouse[0] < (520 + 120) and 397 < mouse[1] < (397 + 70):
                    # START THE GAME!!!!
                    self.on_new_game()

    # in help scene
    def in_help(self, events):
        blue = (0, 170, 255)

        # create the basic window/screen and a title/caption
        # default is a black background
        self.screen.fill((60, 60, 60))
        # pick a font you have and set its size
        myfont = pygame.font.SysFont("Impact", 18)
        secondfont = pygame.font.SysFont("Impact", 48)
        # apply it to text on a label
        label = secondfont.render("﻿Game Rules:", 12, blue)
        first_line = myfont.render("1. This is a game of guessing and process of elimination. ", 12, blue)
        second_line = myfont.render("2. This is a 2 player or 2 team game. No more and no less. ", 12, blue)
        third_line = myfont.render(
            "3. Each player is shown 24 cards on the screen. Each card is different and is a picture of a celebrity (The cards for both players are the same).  ",
            12, blue)
        fourth_line = myfont.render("4. Each player picks one character from the existing characters.", 12, blue)
        fifth_line = myfont.render(
            "5. Player 1 starts asking a question about a facial feature of the other player's character.", 12, blue)
        sixth_line = myfont.render(
            "6. If Player 1 asks a question about Player 2's character, and the character matches the question, Player 1 flips every character that doesn’t match the question. ",
            12, blue)
        sixth_line2 = myfont.render("If the character does not match, Player 1 flips all the cards with said feature.",
                                    12,
                                    blue)
        seventh_line = myfont.render(
            "7. Now, it is Player 2's turn. Player 1 looks away from the screen and player 2 starts asking questions about Player 1's character.",
            12, blue)
        eighth_line = myfont.render("8. Repeat step 6 for Player 2", 12, blue)
        ninth_line = myfont.render(
            "9. The players are allowed to ask about facial features (eg.Hair color, eye color, skin color, glasses and etc.), nationality, but you may not ask the name of the character.",
            12, blue)
        tenth_line = myfont.render(
            "10. When you have determined the identity of the character, you may guess their name. The player who guesses the right character FIRST, wins the game.",
            12, blue)
        back_button = secondfont.render("Back", 13, blue)
        # put the label object on the screen at point x=100, y=100
        self.screen.blit(label, (0, 70))
        self.screen.blit(first_line, (0, 150))
        self.screen.blit(second_line, (0, 200))
        self.screen.blit(third_line, (0, 250))
        self.screen.blit(fourth_line, (0, 300))
        self.screen.blit(fifth_line, (0, 350))
        self.screen.blit(sixth_line, (0, 400))
        self.screen.blit(sixth_line2, (15, 450))
        self.screen.blit(seventh_line, (0, 500))
        self.screen.blit(eighth_line, (0, 550))
        self.screen.blit(ninth_line, (0, 600))
        self.screen.blit(tenth_line, (0, 650))
        self.screen.blit(back_button, (1000, 680))

        for event in events:
            # exit conditions --> windows titlebar x click
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                a = 1000
                b = 680
                if a < mouse[0] < a + 127 and b < mouse[1] < b + 200:
                    self.scene = Scenes.IN_MENU

    # in game scene
    def in_game(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                self.scene = Scenes.IN_MENU

        '''
            Steps for each turn:
            1. Allow current player to ask the other player a question (type into text box, showing board)
            2. Allow other player to answer the current player's question (type into text box, hide board)
            3. Give the current player time to flip down eliminated characters
            4. Switch the turn to the next player
            
            Use enums from TurnStage to determine which state the turn currently is in
        '''

        other = None
        other_name = ""
        nm = ""
        if self.turn == self.player1:
            self.player1.update(events)
            other = self.player2
            other_name = "Player 2"
            nm = "Player 1"
        else:
            self.player2.update(events)
            other = self.player1
            other_name = "Player 1"
            nm = "Player 2"

        # render based on turn
        if self.turn_stage == TurnStages.OUT_OF_SCENE:
            # TODO: what happens when there is no turn going on
            pass

        elif self.turn_stage == TurnStages.WIN:
            TextBox.show_text("{} has guessed {} correctly and won the game!".format(self.winner, other.selected.name), 40, (0, 500), self.screen)
            TextBox.show_text("Press ENTER to return to the menu", 40,(0, 600), self.screen)
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    self.scene = Scenes.IN_MENU

        # choosing the celebrity
        elif self.turn_stage == TurnStages.CHOOSING:
            # randomly select a chosen celebrity for each player
            if self.turn_data:
                TextBox.show_text("Player 2's randomly selected secret celebrity: {}".format(self.player2.selected.name), 40, (0, 200), self.screen)
                TextBox.show_text("Press ENTER to begin the game!", 40, (0, 700), self.screen)
            else:
                TextBox.show_text("Player 1's randomly selected secret celebrity: {}".format(self.player1.selected.name), 40, (0, 200), self.screen)
                TextBox.show_text("Press ENTER to continue to player 2", 40, (0, 700), self.screen)

            TextBox.show_text("Remember your character and don't tell the other player!", 40, (0, 500), self.screen)

            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    if self.turn_data:
                        self.turn_stage = TurnStages.ASKING
                    else:
                        self.turn_data = True

        # draw the board in the back, and a textbox for the player to enter the question
        elif self.turn_stage == TurnStages.ASKING:
            # update (check clicks) depending on which player's turn it is

            # box to type in question or guess character
            # check if return was pressed, if it was then move to the next turn
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    # check if the entered text matches the name of the other person's character
                    if other.selected != None and self.ask_text.text.lower() == other.selected.name.lower():

                        # the game has ended
                        # empty the sprite groups and load the main menu
                        self.winner = nm
                        self.turn_stage = TurnStages.WIN

                    else:
                        # set the turn to responding, update the status text
                        self.turn_stage = TurnStages.RESPONDING

                        # update status texts
                        self.status_text.coords = (0, 0.2)
                        self.status_text.set_text("{}'s turn to respond to the question below:".format(other_name))
                        self.status_text_2.set_text(self.ask_text.text)

                        # clear question text
                        self.response_text.set_text("", "Enter response: ")

            self.ask_text.update(events)
            self.status_text.update(events)

            # draw the board
            if self.turn == self.player1:
                self.celebs_group.draw(self.screen)
                self.celebs_group.update(events)
            else:
                self.celebs_group_2.draw(self.screen)
                self.celebs_group_2.update(events)

        # let the other player respond, hide the board
        elif self.turn_stage == TurnStages.RESPONDING:
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    # pass the message back to the turn's player and update texts
                    self.status_text.set_text("{}'s turn to flip down eliminated celebrities. Press RETURN to end your turn.".format(nm))
                    self.status_text_2.set_text(self.response_text.text, "{}'s response to your question: ".format(other_name))
                    self.status_text.coords = (0, self.window_size[1] * 0.88)
                    self.status_text_2.coords = (0, self.window_size[1] * 0.93)
                    self.turn_stage = TurnStages.FLIPPING

            self.status_text.update(events)
            self.status_text_2.update(events)
            self.response_text.update(events)

        # show the response on the screen, and allow the player to freely flip down characters
        elif self.turn_stage == TurnStages.FLIPPING:
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    # if the player ends, then switch turns to the next player
                    self.turn = self.player1 if self.turn == self.player2 else self.player2
                    self.turn_stage = TurnStages.ASKING

                    # reset text positions and content
                    self.status_text.coords = (0, self.window_size[1] * 0.88)
                    self.status_text_2.coords = (0, self.window_size[1] * 0.25)
                    self.status_text.set_text("{}'s turn to ask a question".format(other_name))
                    self.status_text_2.set_text("", "")
                    self.ask_text.set_text("", "Enter question or guess: ")
                    self.response_text.set_text("", "Enter response: ")

            # draw the board
            if self.turn == self.player1:
                self.celebs_group.draw(self.screen)
                self.celebs_group.update(events)
            else:
                self.celebs_group_2.draw(self.screen)
                self.celebs_group_2.update(events)

            # draw the text
            self.status_text.update(events)
            self.status_text_2.update(events)

    # loads celebrity images from file folder asset_folder
    @staticmethod
    def load_celeb_assets(gm):
        with open("data.json") as data:
            celeb_data = json.load(data)
            celebs = []

            # load the cardback
            try:
                cardback = pygame.image.load(
                    os.path.join(GameManager.asset_folder, celeb_data["cardback"]["img"])).convert()
            except pygame.error as msg:
                print(msg)
                raise SystemExit(msg)

            # loop through the celeb data and load images into classes based on the metadata
            for celeb in celeb_data["celebs"]:
                try:
                    img = pygame.image.load(os.path.join(GameManager.asset_folder, celeb["img"])).convert()
                    celebs.append(Celebrity(gm, celeb["name"], img, Board.image_size, (0, 0)))
                except pygame.error as msg:
                    print(msg)
                    raise SystemExit(msg)

            output = (celebs, cardback)
            return output


# board class to store player board data in a 2d array
class Board:
    # the size of a standard guess who board
    image_size = (128, 196)
    board_size = (6, 4)

    def __init__(self, gm, cardback, board=[], selected=None):
        self.gm = gm
        # board is a 2d array of celebrities
        self.board = board
        self.selected = selected

        # image to show when card is flipped
        self.cardback = cardback

    # called every frame, draws the cards
    def update(self, events):

        # check if each card was clicked
        for col in self.board:
            for item in col:
                celeb = item[0]
                if celeb.is_clicked(events):
                    item[1] = not item[1]
                    celeb.image = pygame.transform.scale(self.cardback, Board.image_size)
                # flip back if clicked again
                else:
                    if item[1]:
                        celeb.image = pygame.transform.scale(celeb.celeb_image, Board.image_size)

    # helper function to get the celebrity at the coordinate, returns [celeb, flip_status]
    def get_at(self, coords):
        return self.board[coords[0]][coords[1]]

    # function to flip down (sets flip_status to false)
    def flip_at(self, coords):
        # inverts
        self.board[coords[0]][coords[1]][1] = not self.board[coords[0]][coords[1]][1]

    # generates a standard guess who board with the given size and celebrities
    # each celebrity is packed with a boolean that represents its flip status
    @staticmethod
    def gen_board(gm, celebs, card_back, size=(6, 4)):
        # standard board size is 6*4
        c = 0
        board = []
        for y in range(size[1]):
            row = []
            for x in range(size[0]):
                if c < len(celebs):
                    row.append([celebs[c], True])
                    c += 1
                else:
                    print("error: not enough celebrities for given board size")
                    # TODO: end
            board.append(row)

        # reverse the rows and columns to match x,y
        board1 = []
        for i in range(size[0]):
            col = []
            for row in board:
                col.append(row[i])
            board1.append(col)

        # set the position of every image in the board
        for i in range(len(board1)):
            col = board1[i]
            for j in range(len(col)):
                item = col[j]
                item[0].rect.left = j * Board.image_size[0]
                item[0].rect.top = i * Board.image_size[1]

        return Board(gm, card_back, board1)


# celebrity class, stores images as a sprite and links with the name
class Celebrity(pygame.sprite.Sprite):
    def __init__(self, gm, name, image, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.gm = gm
        self.celeb_image = image
        self.image = pygame.transform.scale(self.celeb_image, size)
        self.rect = self.image.get_rect()
        self.rect.center = position

        # name of the celebrity
        self.name = name

    # called every frame
    def update(self, events):
        TextBox.show_text(str(self.name), 22, self.rect.topleft, self.gm.screen)

    # function that returns true/false depending on if the celebrity card was clicked
    def is_clicked(self, events):
        # if the mouse was clicked, and the click was within the card area
        if TextBox.is_click_event(events):
            pos = pygame.mouse.get_pos()

            # check bounds
            if self.rect.left < pos[0] < self.rect.right:
                if self.rect.top < pos[1] < self.rect.top + self.rect.height:
                    return True
        return False

    def debug(self):
        print(self.name, self.image)


# class for editable text box
class TextBox:
    def __init__(self, text, font_size, coords, surface, editable=False, show=True, limit=30, prefix="", suffix=""):
        self.prefix = prefix
        self.suffix = suffix
        self.font = pygame.font.SysFont(None, font_size)
        self.text = text
        self.text_obj = None
        self.set_text(self.text)  # use set_text to update text, do not directly modify text
        self.coords = coords
        self.surface = surface

        # determine if the text box is clicked on, has "focus"
        self.has_focus = False
        self.limit = limit
        self.editable = editable
        self.show = show

    # set text
    def set_text(self, text, prefix=None, suffix=None):
        if prefix is not None:
            self.prefix = prefix
        if suffix is not None:
            self.suffix = suffix
        self.text = text
        self.text_obj = self.font.render(self.prefix + self.text + self.suffix, False, (0, 0, 0))

    def update(self, events):
        if self.show:
            # check clicks first
            if TextBox.is_click_event(events):
                if self.is_mouse_inbounds():
                    self.has_focus = True
                else:
                    self.has_focus = False

            # allow edits if editable, otherwise just render the text
            if self.editable:
                if self.has_focus:
                    # check if keys are typed
                    for e in events:
                        if e.type == pygame.KEYDOWN:
                            if e.key == pygame.K_BACKSPACE:
                                self.text = self.text[:-1]
                            else:
                                if len(self.text) < self.limit and e.key != pygame.K_RETURN:
                                    self.text += e.unicode

                            # render the updated text
                            self.set_text(self.text)

            size = self.font.size(self.prefix + self.text + self.suffix)
            pygame.draw.rect(self.surface, (255, 255, 255), (self.coords, (size[0] + 10, size[1] + 10)))
            self.surface.blit(self.text_obj, self.coords)

            # show caret if focused
            if self.has_focus and self.editable:
                pygame.draw.rect(self.surface, (0, 0, 0), ((self.coords[0] + self.font.size(self.prefix + self.text)[0], self.coords[1]), (2, size[1])))

    @staticmethod
    def is_click_event(events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONUP:
                return True
        return False

    def is_mouse_inbounds(self):
        pos = pygame.mouse.get_pos()

        # check bounds
        size = self.font.size(self.prefix + self.text + self.suffix)
        if self.coords[0] < pos[0] < self.coords[0] + size[0] + 10:
            if self.coords[1] < pos[1] < self.coords[1] + size[1] + 10:
                return True
        return False

    def is_clicked(self, events):
        if TextBox.is_click_event(events) and self.is_mouse_inbounds():
            return True
        return False

    # helper method for showing text
    @staticmethod
    def show_text(text, font_size, coords, surface):
        font = pygame.font.SysFont(None, font_size)
        txt = font.render(text, False, (0, 0, 0))
        # calculate size of background needed
        text_size = font.size(text)
        pygame.draw.rect(surface, (255, 255, 255), (coords, text_size))
        surface.blit(txt, coords)


# running code
game_manager = GameManager()
game_manager.on_run()
