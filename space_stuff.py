# Joe Hausman
# 17.11.01

import pygame
from pygame.locals import *
from math import sqrt
from math import floor
from sys import maxsize

import random

WIDTH = 400
HEIGHT = 600
FRAMERATE = 40

COOLDOWN_MAX = 3
PLAYER_SPEED = 4
PLAYER_BULLET_SPEED = 20
MOVEMENT_MULTIPLIER = 3
SCROLL_INTERVAL = 40

CHEATS = False

black = [0, 0, 0]
white = [255, 255, 255]
red = [255, 0, 0]

WINDOW_SIZE = WIDTH, HEIGHT
BR_COLOR = black


pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()


# a lot of classes =============================================================
# player -----------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
    speed = 0
    x_size = 0
    y_size = 0
    health = 0
    invuln = 0  # invunerability timer
    radius = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('player.png')
        self.rect = self.image.get_rect()

        self.rect.x = 200
        self.rect.y = 500
        self.speed = PLAYER_SPEED
        self.health = 3

        self.x_size = 32
        self.y_size = 32

        self.invuln = 0

        self.radius = 6

    # move x
    def m_x(self, val):
        self.rect.x += val # * speed_multiplier

    # move y
    def m_y(self, val):
        self.rect.y += val

    def get_centx(self):
        offset = self.x_size / 2
        return self.rect.x + offset

    def get_centy(self):
        offset = self.y_size / 2
        return self.rect.y + offset

    def get_top(self):
        return self.rect.y

    def get_bot(self):
        return self.rect.y + self.y_size

    def get_left(self):
        return self.rect.x

    def get_right(self):
        return self.rect.x + self.x_size

    def damage(self):
        if self.invuln == 0:
            self.health -= 1
            self.invuln = 20
            print('ouch')
            self.image = pygame.image.load('player_damage.png')

    def step(self):
        if self.invuln > 0:
            if self.invuln == 1:
                self.image = pygame.image.load('player.png')
            self.invuln -= 1
        if self.health <= 0:
            self.kill()


class PlayerBullet(pygame.sprite.Sprite):
    speed = 0
    x = 0
    y = 0
    hit_timer = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = PLAYER_BULLET_SPEED
        self.rect = pygame.Rect(self.x - 3, self.y - 3, 6, 6)

    def draw(self):
        pygame.draw.circle(screen, white, (self.x, self.y), 3, 0)

    def step(self):
        self.y -= self.speed
        self.rect.move_ip(0, -self.speed)
        if self.y < 0:
            self.kill() # bullet is offscreen


class PBulletGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

class PGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

# enemy ------------------------------------------------------------------------

class Enemy(pygame.sprite.Sprite):
    health = 0
    hit = 0
    step_offset = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy1.png')
        self.rect = self.image.get_rect()
        self.health = 10
        self.hit = 0

        self.rect.x = x
        self.rect.y = y

        self.step_offset = random.randint(0, 19)   # indivitualize activity

    def damage(self):
        self.health -= 1
        self.hit = 2
        self.image = pygame.image.load('enemy1_damage.png')

    def step(self, main_timer, ebg):
        if self.hit > 0:
            if self.hit == 1:
                self.image = pygame.image.load('enemy1.png')
            self.hit -= 1
        if self.health <= 0:
            print("bye")

        if (main_timer % 40) + self.step_offset == 0:    #if main_timer % 80 == 0:
            ebg.add(EnemyBullet_straight(self.rect.x + 16, self.rect.y + 16, 5))
            ebg.add(EnemyBullet_diagonal(self.rect.x + 16, self.rect.y + 16, 1, 5))
            ebg.add(EnemyBullet_diagonal(self.rect.x + 16, self.rect.y + 16, -1, 5))

        if (main_timer % 40) - 20 + self.step_offset == 0:     #if (main_timer % 80) - 40 == 0:
            ebg.add(EnemyBullet_straight(self.rect.x + 16, self.rect.y + 16, 3))
            ebg.add(EnemyBullet_diagonal(self.rect.x + 16, self.rect.y + 16, 1, 3))
            ebg.add(EnemyBullet_diagonal(self.rect.x + 16, self.rect.y + 16, -1, 3))


        self.move(0, 1)

        if self.rect.y > HEIGHT + 50:
            self.kill()


    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Enemy2(pygame.sprite.Sprite):
    health = 0
    hit = 0
    step_offset = 0
    refire = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy2.png')
        self.rect = self.image.get_rect()
        self.health = 10
        self.hit = 0

        self.rect.x = x
        self.rect.y = y

        self.step_offset = random.randint(0, 19)   # indivitualize activity
        self.refire = 0

    def damage(self):
        self.health -= 1
        self.hit = 2
        self.image = pygame.image.load('enemy2_damage.png')

    def step(self, main_timer, ebg):
        if self.hit > 0:
            if self.hit == 1:
                self.image = pygame.image.load('enemy2.png')
            self.hit -= 1
        if self.health <= 0:
            #self.kill()
            print("bye")

        if main_timer % 80 == 0:
            self.refire = 3

        if self.refire > 0 and main_timer % 3 == 0:
            ebg.add(EnemyBullet_straight(self.rect.x + 4, self.rect.y + 16, 10))
            ebg.add(EnemyBullet_straight(self.rect.x + 28, self.rect.y + 16, 10))
            self.refire -= 1

        self.move(0, 1)

        if self.rect.y > HEIGHT + 50:
            self.kill()


    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Enemy3(pygame.sprite.Sprite):
    health = 0
    hit = 0
    step_offset = 0
    refire = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy3.png')
        self.rect = self.image.get_rect()
        self.health = 20
        self.hit = 0

        self.rect.x = x
        self.rect.y = y

        self.step_offset = random.randint(0, 19)   # indivitualize activity
        self.refire = 0

    def damage(self):
        self.health -= 1
        self.hit = 2
        self.image = pygame.image.load('enemy3_damage.png')

    def step(self, main_timer, ebg):
        if self.hit > 0:
            if self.hit == 1:
                self.image = pygame.image.load('enemy3.png')
            self.hit -= 1
        if self.health <= 0:
            print("bye")

        if main_timer % 80 == 0:
            self.refire = 10

        if self.refire > 0:
            # calculate displacements between enemy and player
            disp_x = player.rect.x - self.rect.x
            disp_y = player.rect.y - self.rect.y
            v_x, v_y = unit_vector_scale(disp_x, disp_y, 10) # get a scaled vector

            ebg.add(EnemyBullet_diagonal(self.rect.x + 16, self.rect.y + 16, floor(v_x), floor(v_y)))
            self.refire -= 1

        if self.rect.y > HEIGHT + 50:
            self.kill()

        self.move(0, 1)


    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Enemy4(pygame.sprite.Sprite):
    health = 0
    hit = 0
    step_offset = 0
    refire = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('enemy4.png')
        self.rect = self.image.get_rect()
        self.health = 7
        self.hit = 0

        self.rect.x = x
        self.rect.y = y

        self.step_offset = random.randint(0, 19)   # indivitualize activity

    def damage(self):
        self.health -= 1
        self.hit = 2
        self.image = pygame.image.load('enemy4_damage.png')

    def step(self, main_timer, ebg):
        if self.hit > 0:
            if self.hit == 1:
                self.image = pygame.image.load('enemy4.png')
            self.hit -= 1
        if self.health <= 0:
            print("bye")

        if main_timer % 80 == 0:
            ebg.add(EnemyBullet_straight(self.rect.x + 16, self.rect.y + 16, 10))

        self.move(0, 2)

        if self.rect.y > HEIGHT + 50:
            self.kill()


    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


class EnemyGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

# enemy bullet -----------------------------------------------------------------

class EnemyBullet_straight(pygame.sprite.Sprite):
    speed = 0
    x = 0
    y = 0
    radius = 0

    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.speed = speed
        self.rect = pygame.Rect(self.x - 6, self.y - 6, 12, 12)
        radius = 0

    def draw(self):
        pygame.draw.circle(screen, white, (self.x, self.y), 6, 0)

    def step(self):
        self.y += self.speed
        self.rect.move_ip(0, self.speed)
        if self.y > HEIGHT:
            self.kill()     # bullet is offscreen


class EnemyBullet_diagonal(pygame.sprite.Sprite):
    x = 0
    y = 0
    x_speed = 0
    y_speed = 0
    radius = 0

    def __init__(self, x, y, x_speed, y_speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rect = pygame.Rect(self.x - 6, self.y - 6, 12, 12)
        #print('------ rx: ' + str(self.rect.x))
        #print('------ ry: ' + str(self.rect.y))
        radius = 0

    def draw(self):
        pygame.draw.circle(screen, white, (self.x, self.y), 6, 0)

    def step(self):
        self.y += self.y_speed
        self.x += self.x_speed
        self.rect.move_ip(self.x_speed, self.y_speed)
        if self.y > HEIGHT or self.x > WIDTH or self.x < 0:
            self.kill()     # bullet is offscreen

class EBulletGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

# star -------------------------------------------------------------------------

class Star(pygame.sprite.Sprite):
    speed = 0
    x = 0
    y = 0

    def __init__(self, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed      # MAKE ME RANDOM PLZ
        self.x = x
        self.y = y


    def draw(self):
        pygame.draw.rect(screen, white, (self.x, self.y, 1, 1), 0)

    def step(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.kill()

class StarGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)

# asteroid ---------------------------------------------------------------------

class Asteroid1(pygame.sprite.Sprite):
    # hit = 0
    radius = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('asteroid1.png')
        self.rect = self.image.get_rect()
        self.radius = 16

        self.rect.x = x
        self.rect.y = y

        self.health = 0

    def step(self):
        self.move(0, 4)
        if self.rect.y > HEIGHT + 50:
            self.kill()

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


class Asteroid2(pygame.sprite.Sprite):
    # hit = 0
    radius = 0

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('asteroid2.png')
        self.rect = self.image.get_rect()
        self.radius = 32

        self.rect.x = x
        self.rect.y = y

        self.health = 0

    def step(self):
        self.move(0, 4)
        if self.rect.y > HEIGHT + 50:
            self.kill()

    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y


class AsteroidGroup(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)


# helpers & setup ==============================================================
def load_line(line, newborns, asteroids):
    #print(line)
    idx = 0
    for ch in line:
        if ch == '=':               # stop the level from scrolling
            global unlock           # (later unlocked when all enemies killed)
            unlock = False
            break
        elif ch == '1':
            newborns.append(Enemy(idx * 50, -50))
        elif ch == '2':
            newborns.append(Enemy2(idx * 50, -50))
        elif ch == '3':
            newborns.append(Enemy3(idx * 50, -50))
        elif ch == '4':
            newborns.append(Enemy4(idx * 50, -50))
        elif ch == 'a':
            asteroids.append(Asteroid1(idx * 50, -50))
        elif ch == 'b':
            asteroids.append(Asteroid2(idx * 50, -50))
        elif ch == 'w':     # won the game
            print('Congrats! You won!')
            pygame.quit()
            exit()

        idx += 1

def new_star_row(sg, y):
    new_stars = random.randint(0, 2)
    while new_stars > 0:
        curr = Star(random.randint(0, WIDTH), y, random.randint(1, 6))  # ?? MAX_STAR_SPEED
        sg.add(curr)
        new_stars -= 1

# calculate a scaled unit vector
def unit_vector_scale(x, y, scale):
    magnitude = sqrt(x**2 + y**2)
    unit_x = x / magnitude
    unit_y = y / magnitude
    return unit_x * scale, unit_y * scale

# skip to next level
def skip_level(level_data):
    idx = 0
    for line in level_data:
        idx += 1
        for ch in line:
            if ch == '#':   # comment found
                return idx
    return 0   # tried to skip past last level

player = Player()
pg = PGroup()
pg.add(player)
player_bullets = PBulletGroup()
cooldown = 0


eg = EnemyGroup()
ebg = EBulletGroup()
sg = StarGroup()
astg = AsteroidGroup()

for x in range(0, HEIGHT):
    new_star_row(sg, x)

level_file = open('level.lv', 'r')
level_data = []
for line in level_file:
    # build level in reverse order; more intuitive this way
    level_data.insert(0, line.strip())

unlock = True   # allow the level to scroll
lines_cleared = 0

main_timer = 0      # used to time events

# game loop ====================================================================
while 1:
    clock.tick_busy_loop(FRAMERATE)
    main_timer += 1
    if main_timer >= 160:
        main_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_0 and CHEATS:
                print('level skipped')
                skip_idx = skip_level(level_data)
                level_data = level_data[skip_idx:]
            elif event.key == K_9 and CHEATS:
                print('health set to int max')
                player.health = maxsize


    # handle input -------------------------------------------------------------
    if cooldown > 0:
        cooldown -= 1
    keys = pygame.key.get_pressed()
    speed_multiplier = 1    # ?? GLOBALIZE ME

    if keys[K_LSHIFT]:  # move up
        speed_multiplier = MOVEMENT_MULTIPLIER

    if keys[K_UP] and player.get_top() >= 0:
        player.m_y(-player.speed * speed_multiplier)

    if keys[K_DOWN] and player.get_bot() <= HEIGHT:    # move down
        player.m_y(player.speed * speed_multiplier)

    if keys[K_LEFT] and player.get_left() >= 0:    # move left
        player.m_x(-player.speed * speed_multiplier)

    if keys[K_RIGHT] and player.get_right() <= WIDTH:   # move left
        player.m_x(player.speed * speed_multiplier)

    if keys[K_z] and cooldown == 0:   # shoot
        PlayerBullet(player.rect.x+16, player.rect.y+16).add(player_bullets)
        cooldown = COOLDOWN_MAX


    # load level data (if applicable) ------------------------------------------
    if len(eg) == 0:        # !!!! if all enemies are killed,
        unlock = True       # allow the level to keep scrolling

    if main_timer % SCROLL_INTERVAL == 0:
        if len(level_data) > 0 and unlock:
            newborns = []
            asteroids = []
            load_line(level_data[0], newborns, asteroids)
            lines_cleared += 1
            eg.add(newborns)
            astg.add(asteroids)
            level_data = level_data[1:]     # remove loaded line

    # move everything ----------------------------------------------------------
    for bullet in player_bullets:
        bullet.step()

    for enemy in eg:
        enemy.step(main_timer, ebg)

    for bullet in ebg:
        bullet.step()

    for asteroid in astg:
        asteroid.step()

    player.step()

    # make new random stars
    new_star_row(sg, 0)
    for star in sg:
        star.step()

    # draw everything ----------------------------------------------------------
    screen.fill(BR_COLOR)
    for star in sg:
        star.draw()

    eg.draw(screen)
    for bullet in player_bullets:
        for enemy in eg:
            if bullet.rect.colliderect(enemy.rect):
                enemy.damage()
                player_bullets.remove(bullet)
                if enemy.health <= 0:
                    eg.remove(enemy)

        bullet.draw()

    # check enemy bullet - player collision
    for bullet in ebg:
        if pygame.sprite.collide_circle(player, bullet):
            player.damage()
            ebg.remove(bullet)
        bullet.draw()

    for asteroid in astg:
        if pygame.sprite.collide_circle(player, asteroid):
            player.damage()
        for bullet in player_bullets:
            if bullet.rect.colliderect(asteroid.rect):
                player_bullets.remove(bullet)
        for bullet in ebg:
            if bullet.rect.colliderect(asteroid.rect):
                ebg.remove(bullet)


    if len(pg) < 1:     # the player has died
        print("oopsies")
        pygame.quit()
        exit()

    astg.draw(screen)
    pg.draw(screen)

    pygame.display.flip()
