# MODDED SKIER PROGRAM
# DONE BY ELIOT TROOP
"""

This program used to be a skier game. I transformed it into a bad Minecraft 2d scroller.
It works fairly well, but the sounds only work intermittently because only one sound can be playing at once.
I have tried to make some of the glitches go away, but the blocks take long enough to load that it just doesn't work well.
Mod 1: Added a large repository of background music
Mod 2: Added acceleration and deceleration.
Mod 3: Moved controls from arrows to WASD
Mod 4: Added stone as floor, magma blocks to deal damage, iron, diamonds, enchant multiplier, and furnace to actually aquire stuff.
Mod 5: Changed skier to Steve
Mod 6: Added health
Mod 7: Added sound effects for everything.
Mod 8: Changed movement speed left and right.
Mod 9: Minimal slowdown when taking damage.
Mod 10: Added a sound efect global mute to allow for optional bacground music.
"""
# Skier program

import pygame, sys, random

mutesoundeffects = True  # Change to true to allow sound effects to play.
# different images for the steve depending on his direction
pygame.mixer.init()  # MOD
backgroundMusic = [pygame.mixer_music.load("11.mp3"),
                   pygame.mixer_music.load("13.mp3"),
                   pygame.mixer_music.load("Blocks.mp3"),
                   pygame.mixer_music.load("Cat.mp3"),
                   pygame.mixer_music.load("Chirp.mp3"),
                   pygame.mixer_music.load("Clark.mp3"),
                   pygame.mixer_music.load("Danny.mp3"),
                   pygame.mixer_music.load("Dry Hands.mp3"),
                   pygame.mixer_music.load("Far.mp3"),
                   pygame.mixer_music.load("Haggstrom.mp3"),
                   pygame.mixer_music.load("Key.mp3"),
                   pygame.mixer_music.load("Living Mice.mp3"),
                   pygame.mixer_music.load("Mall.mp3"),
                   pygame.mixer_music.load("Mellohi.mp3"),
                   pygame.mixer_music.load("Mice On Venus.mp3"),
                   pygame.mixer_music.load("Minecraft.mp3"),
                   pygame.mixer_music.load("Oxygane.mp3"),
                   pygame.mixer_music.load("Stal.mp3"),
                   pygame.mixer_music.load("Strad.mp3"),
                   pygame.mixer_music.load("Subwoofer Lullaby.mp3"),
                   pygame.mixer_music.load("Sweden.mp3"),
                   pygame.mixer_music.load("Ward.mp3"),
                   pygame.mixer_music.load("Wet Hands.mp3"),
                   pygame.mixer_music.load("Where Are We Now.mp3")]
backgroundMusicNames = ["11.mp3",  # MOD
                        "13.mp3",
                        "Blocks.mp3",
                        "Cat.mp3",
                        "Chirp.mp3",
                        "Clark.mp3",
                        "Danny.mp3",
                        "Dry Hands.mp3",
                        "Far.mp3",
                        "Haggstrom.mp3",
                        "Key.mp3",
                        "Living Mice.mp3",
                        "Mall.mp3",
                        "Mellohi.mp3",
                        "Mice On Venus.mp3",
                        "Minecraft.mp3",
                        "Oxygane.mp3",
                        "Stal.mp3",
                        "Strad.mp3",
                        "Subwoofer Lullaby.mp3",
                        "Sweden.mp3",
                        "Ward.mp3",
                        "Wet Hands.mp3",
                        "Where Are We Now.mp3"]

baseSpeed = 0  # Allows the speed to be modified


# class for the Skier sprite
class SkierClass(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("character.png")  # MOD
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.angle = 0

    def turn(self, direction):
        # load new image and change speed when the steve turns
        self.angle = self.angle + direction
        if self.angle < -3:  self.angle = -3
        if self.angle > 3:  self.angle = 3
        center = self.rect.center
        self.image = pygame.image.load("character.png")  # MOD
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle * 4 * (baseSpeed / 20), 10 + abs(baseSpeed) - abs(self.angle) * 2]  # Increased base speed from 6 to 10

        return speed

    def move(self, speed):
        # move the steve right and left
        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20:  self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620

    # class for obstacle sprites (trees and flags)


class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self)
        self.image_file = image_file
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False

    def update(self):
        global speed
        self.rect.centery -= speed[1]
        if self.rect.centery < -32:
            self.kill()


# create one "screen" of obstacles: 640 x 640
# use "blocks" of 64 x 64 pixels, so objects aren't too close together
locations = []


def create_map():
    speed = [0, 0]

    global obstacles

    row = 0
    col = 0
    locations = []
    for i in range(100):  # FIlls every space with a random block

        location = [col * 64 + 32, row * 64 + 640]  # center x, y for obstacle
        row += 1
        if (row == 10):
            col += 1
            row = 0
        if not (location in locations):  # prevent 2 obstacles in the same place
            locations.append(location)
            randy = random.randint(0, 10000)
            if (randy >= 0 and randy <= 9200):  # Stone 92%
                type = "stone"
            elif randy > 9200 and randy <= 9600:  # Magma 4%
                type = "magma"
            elif randy > 9600 and randy <= 9650:  # Diamond .5%
                type = "diamond"
            elif randy > 9650 and randy <= 9870:  # Iron 2.2%
                type = "iron"
            elif randy > 9870 and randy < 9950:  # Furnace .8%
                type = "furnace"
            else:  # Enchant .5%
                type = "enchant"
            if type == "stone":
                img = "stone.png"
            elif type == "magma":
                img = "magma.png"
            elif type == "diamond":
                img = "diamond_ore.png"  # This whole block sets the type.
            elif type == "iron":
                img = "iron_ore.png"
            elif type == "furnace":
                img = "furnace.png"
            elif type == "enchant":
                img = "enchant.png"
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)
    row = 0
    col = 0

    speed = [steve.angle * 5, 10 + abs(baseSpeed - 0.5) - abs(steve.angle) * 2]


# redraw the screen, including all sprites
def animate():
    screen.fill([255, 255, 255])
    obstacles.draw(screen)
    screen.blit(steve.image, steve.rect)
    screen.blit(score_text, [0, 0])
    screen.blit(diamondImage, [0, 20])  # MOD
    screen.blit(diamondCount, [32, 28])  # MOD
    screen.blit(ironImage, [0, 50])  # MOD
    screen.blit(ironCount, [32, 58])  # MOD
    screen.blit(enchantImage, [0, 80])  # MOD
    screen.blit(enchantCount, [32, 88])  # MOD

    pygame.display.flip()


# initialize everything
pygame.init()
ironore = 0

iron = 0  # MOD
diamondore = 0
diamond = 0
ironoreImage = pygame.image.load("iron.png")
diamondoreImage = pygame.image.load("diamond.png")  # MOD
diamondImage = pygame.image.load("diamond.png")
ironImage = pygame.image.load("iron.png")
enchantImage = pygame.image.load("enchantIcon.png")
enchant = 0
furnace = 0

randomee = random.randrange(0, 23)
pygame.mixer_music.load(backgroundMusicNames[random.randint(0, 24) ])  # MOD ''''''

pygame.mixer_music.play()
health = 20  # MOD
dead = False  # MOD
# damage = [pygame.mixer_music.load("hit1.ogg"), pygame.mixer_music.load("hit2.ogg"),pygame.mixer_music.load("hit3.ogg")]
screen = pygame.display.set_mode([640, 640])
clock = pygame.time.Clock()
speed = [2, 6]
obstacles = pygame.sprite.Group()  # group of obstacle objects
steve = SkierClass()
map_position = 0
points = 0
create_map()  # create one screen full of obstacles
font = pygame.font.Font(None, 36)
map_loop = 1
# main Pygame event loop
running = True
while running and not dead:
    clock.tick(30)

    for event in pygame.event.get():

        if event.type == pygame.QUIT: running = False

        if event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_a:  # A turns left
                speed = steve.turn(-1)
            elif event.key == pygame.K_d:  # D turns right
                speed = steve.turn(1)

    steve.move(speed)  # move the steve (left or right)
    map_position += speed[1]  # scroll the obstacles
    # create a new block of obstacles at the bottom
    if map_position >= 640:

        baseSpeed += 0.5 #Allows for the game to get consistently arder until it's unplayable.
        pygame.time.delay(50)
        create_map()
        map_position = 16

        # speed = [steve.angle * 5, 10 + abs(baseSpeed) - abs(steve.angle) * 2]  # Keeps speed updating

    # check for what block the player is on.
    hit = pygame.sprite.spritecollide(steve, obstacles, False)

    if hit:
        if hit[0].type == "stone" and not hit[0].passed:
            for i in range(4):
                pygame.time.delay(3)
                rondo = random.randint(0, 5)
                if not mutesoundeffects:
                    if (rondo == 0):
                        pygame.mixer_music.load("stone1.ogg")
                    elif rondo == 1:
                        pygame.mixer_music.load("stone2.ogg")
                    elif rondo == 1:
                        pygame.mixer_music.load("stone3.ogg")  # MOD
                    elif rondo == 1:
                        pygame.mixer_music.load("stone4.ogg")
                    else:
                        pygame.mixer_music.load("stone5.ogg")

                    pygame.mixer_music.play()
        elif hit[0].type == "magma" and not hit[0].passed:  # crashed into tree
            health -= 1
            if (health == 0):
                dead = True
            rondo = random.randint(0, 2)
            if not mutesoundeffects:
                if (rondo == 0):
                    pygame.mixer_music.load("hit1.ogg")
                elif rondo == 1:
                    pygame.mixer_music.load("hit2.ogg")  # MOD
                else:
                    pygame.mixer_music.load("hit3.ogg")

                pygame.mixer_music.play()
            steve.image = pygame.image.load("character.png")  # crash image
            animate()
            pygame.time.delay(10)
            steve.image = pygame.image.load("character.png")  # resume skiing
            steve.angle = 0
            speed = [0, 6 + baseSpeed]
            hit[0].passed = True
        elif hit[0].type == "diamond" and not hit[0].passed:
            diamondore += 1
            if not mutesoundeffects:
                 pygame.mixer_music.load("pop.ogg")  # MOD
                 pygame.mixer_music.play()
            hit[0].passed = True
            print diamondore
        elif hit[0].type == "iron" and not hit[0].passed:
            ironore += 1
            if not mutesoundeffects:
                 pygame.mixer_music.load("pop.ogg")  # MOD
                 pygame.mixer_music.play()
            hit[0].passed = True
            print ironore
        elif hit[0].type == "enchant" and not hit[0].passed:
            enchant += 1
            if not mutesoundeffects:
                 pygame.mixer_music.load("pop.ogg")  # MOD
                 pygame.mixer_music.play()
            hit[0].passed = True
            print enchant
        elif hit[0].type == "furnace" and not hit[0].passed:
            furnace += 1
            rondo = random.randint(0, 5)
            if not mutesoundeffects:
                if (rondo == 0):
                    pygame.mixer_music.load("fire_crackle1.ogg")
                elif rondo == 1:
                    pygame.mixer_music.load("fire_crackle2.ogg")
                elif rondo == 1:
                    pygame.mixer_music.load("fire_crackle3.ogg")  # MOD
                elif rondo == 1:
                    pygame.mixer_music.load("fire_crackle4.ogg")
                else:
                    pygame.mixer_music.load("fire_crackle5.ogg")
                pygame.mixer_music.play()
                pygame.mixer_music.load("pop.ogg")
                pygame.mixer_music.play()
            hit[0].image = pygame.image.load("lit_furnace.png")
            hit[0].passed = True
            diamond = diamondore * (float(enchant) / 2)
            iron = ironore * (float(enchant) / 2)
            print furnace

    obstacles.update()
    score_text = font.render("Health: " + str(health), 1, (0, 0, 0))
    diamondCount = font.render(str(int(diamond)), 1, (0, 0, 0))  # MOD
    ironCount = font.render(str(int(iron)), 1, (0, 0, 0))  # MOD
    enchantCount = font.render(str(float(enchant) / 2), 1, (0, 0, 0))  # MOD
    print speed[1]
    animate()

pygame.quit()
