# PConc A3Q2
# ICS3UI-01, Ms Harris
# Jonathan H
# Began: Nov 7, 2019
# Finished : Nov 11, 2019

'''
WOW me with your Pygame Sprite knowledge. You may use one I gave you in class
or create your own. Have fun with this one!
'''

# for this question I made a game where you move a chimp to catch bananas and dodge bombs
# if the chimp reaches the edge, it doesnt move anymore
# if a banana or bomb reaches the bottom, it gets respawned up top

# monkey sprite source: http://www.clker.com/cliparts/P/B/P/2/o/F/monkey-hi.png
# bomb sprite source: https://www.wpclipart.com/tools/explosives/dynamite_sticks.png
# banana sprite source: https://www.mariowiki.com/images/1/17/BananaDKCR.png

import pygame, os, random, sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# asset importing from sprites folder
main_folder = os.path.dirname(__file__)
sprites_folder = os.path.join(main_folder, "assets")
FONT = pygame.font.SysFont(None, 40)

# Singleton class template for the GameManager
class Singleton(type):
	_instances = {}
	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
		return cls._instances[cls]

# game manager class
class GameManager(metaclass=Singleton):
    def __init__(self):
        # pygame settings
        pygame.display.set_caption("Jarone the Chimp! by Jonathan H")
        self.window_size = (800, 600)
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.fps = 60

        # load sprites
        self.monkey_sprite = pygame.image.load(os.path.join(sprites_folder, "monkey.png")).convert()
        self.banana_sprite = pygame.image.load(os.path.join(sprites_folder, "banana.png")).convert()
        self.bomb_sprite = pygame.image.load(os.path.join(sprites_folder, "bomb.png")).convert()

        # game settings
        self.running = True
        self.in_game = False

        self.spawn_delay = 800
        self.last_spawn = pygame.time.get_ticks()

        self.score = 0

        self.speed_increment = 0.005
        self.fall_speed_init = 5
        self.fall_speed = 5
        self.player_speed_init = 9

        self.objects = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()

        self.player = Player(self, self.monkey_sprite, (78, 99), (self.window_size[0]/2, self.window_size[1] - 99/2), self.player_speed_init)
        self.objects.add(self.player)

    # runs the app
    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            pygame.event.pump()
            self.update(pygame.event.get())
            pygame.display.flip()
        pygame.exit()
        sys.exit()

    # called on each tick
    def update(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # draw game screen
        if self.in_game:
            self.screen.fill((0,0,0))
            score_txt = FONT.render("Score: {}".format(self.score), False, (255,255,255))
            self.screen.blit(score_txt, (0,0))

            # increase fall speed over time
            self.fall_speed += self.speed_increment
            self.player.speed += self.speed_increment

            # spawn a new banana every x seconds
            if pygame.time.get_ticks() - self.last_spawn >= self.spawn_delay:
                self.spawn_collectible()

            self.objects.update(events)
            self.objects.draw(self.screen)
            self.collectibles.update(events)
            self.collectibles.draw(self.screen)
        # draw menu screen
        else:
            self.screen.fill((0,0,0))

            # show some menu text
            txt = FONT.render("Last score: {}".format(self.score), False, (255,255,255))
            self.screen.blit(txt, (0,0))
            txt = FONT.render("Don't let any bananas drop!", False, (255,255,255))
            self.screen.blit(txt, (0,30))
            txt = FONT.render("Use arrow keys to move Jarone!", False, (255,255,255))
            self.screen.blit(txt, (0,60))
            txt = FONT.render("Press any key to start...", False, (255,255,255))
            self.screen.blit(txt, (0,90))

            for e in events:
                if e.type == pygame.KEYDOWN:
                    # start a new game, reset every counter to original values
                    self.in_game = True
                    self.score = 0
                    self.fall_speed = self.fall_speed_init
                    self.player.speed = self.player_speed_init
                    self.collectibles.empty()

    # spawn next collectible
    def spawn_collectible(self):
        # 25% chance to spawn a bomb
        is_bomb = False
        if bool(random.getrandbits(1)) and bool(random.getrandbits(1)):
            is_bomb = True

        # spawns collectibles randomly at top of screen
        rand_x = int(round(random.randrange(0, self.window_size[0])))
        if is_bomb:
            self.collectibles.add(Bomb(self, self.bomb_sprite, (30, 64), (rand_x, 0), self.fall_speed))
        else:
            self.collectibles.add(Banana(self, self.banana_sprite, (38, 63), (rand_x, 0), self.fall_speed))

        # remember the last spawn time
        self.last_spawn = pygame.time.get_ticks()

# gameobject class
class GameObject(pygame.sprite.Sprite):
    def __init__(self, obj, gm, image, size, position):
        pygame.sprite.Sprite.__init__(obj)
        self.image = pygame.transform.scale(image, size)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.gm = gm
    def update(self, events):
        pass

# player class, inherit from the pygame sprite class
class Player(GameObject):
    def __init__(self, gm, image, size, position, speed):
        super().__init__(self, gm, image, size, position)
        self.speed = speed

    def update(self, events):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed

        # if the player is at the edge of the screen, dont let them move further
        if self.rect.right > self.gm.window_size[0]:
            self.rect.right = self.gm.window_size[0]
        elif self.rect.left < 0:
            self.rect.left = 0

# parent collectible class
# all collectible items inhert from this class (bananas and bombs)
class Collectible(GameObject):
    def __init__(self, gm, image, size, position, speed):
        super().__init__(self, gm, image, size, position)

        self.speed = speed
    def update(self, events):
        self.rect.y += self.speed
	# checks if the collectible has fallen to the ground, returns True/False
    def check_bottom(self):
        if self.rect.top > self.gm.window_size[1] + self.rect.size[1]:
            return True
        return False
# bomb class
class Bomb(Collectible):
    def __init__(self, gm, image, size, position, speed):
        super().__init__(gm, image, size, position, speed)

    def update(self, events):
        super().update(events)

        # if a bomb collides with a player, end the game
        if pygame.sprite.collide_rect(self.gm.player, self):
            self.gm.in_game = False
            self.kill()
        elif self.check_bottom():
            self.kill()

# banana class
class Banana(Collectible):
    def __init__(self, gm, image, size, position, speed):
        super().__init__(gm, image, size, position, speed)

    def update(self, events):
        super().update(events)

        # if a banana collides with the player, add 1 to score and kill it
        if pygame.sprite.collide_rect(self.gm.player, self):
            self.gm.score += 1
            self.kill()
        # if a banana is lost, end the game
        elif self.check_bottom():
            self.gm.in_game = False
            self.kill()

# run the game
game_manager = GameManager()
game_manager.run()
