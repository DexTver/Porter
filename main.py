import pygame
import sys
import os
from PIL import Image
from random import randrange

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 200
button_sound = pygame.mixer.Sound('data/button.wav')


def print_text(message, x, y, font_color=(0, 0, 0), font_type='Data/main_font.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    screen.blit(text, (x, y))


def load_image(name, colorkey=0):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey != 0:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((1, 1))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def draw_image_after_finish(im_name):
    im = Image.open(im_name)
    pixels = im.load()
    x, y = im.size

    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            r, g, b = r // 3, g // 3, (b + 255) // 2
            pixels[i, j] = r, g, b

    im.save(f'data/{im_name}')


class Fon(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('after_level.jpg')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


start_group = pygame.sprite.Group()


def pause_screen():
    Fon(start_group)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                game()
                terminate()
        start_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    global finish_coords
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('crate', x, y)
            elif level[y][x] == '#':
                a = randrange(1, 6)
                chosen_container = 'container_' + str(a)
                Tile(chosen_container, x, y)
            elif level[y][x] == '0':
                Tile('crate', x, y)
                box_object = Box(x, y)
            elif level[y][x] == '1':
                Tile('crate', x, y)
                Tile('finish', x, y)
                finish_coords = tile_width * x, tile_height * y
            elif level[y][x] == '@':
                Tile('crate', x, y)
                new_player = Player(load_image('animated_forklift.png'), 4, 1, x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, box_object, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(crate, all_sprites)
        if tile_type == 'container_1' or tile_type == 'container_2' or tile_type == 'container_3' \
                or tile_type == 'container_4' or tile_type == 'container_5':
            containers_group.add(self)
        if tile_type == 'finish':
            all_sprites.add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, pos_x, pos_y):
        super().__init__(forklift_group, all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        sp = pygame.key.get_pressed()
        if sp[pygame.K_LEFT] == 1:
            self.rect.x -= 1
            self.image = self.frames[3]
        if sp[pygame.K_RIGHT] == 1:
            self.rect.x += 1
            self.image = self.frames[1]
        if sp[pygame.K_UP] == 1:
            self.rect.y -= 1
            self.image = self.frames[0]
        if sp[pygame.K_DOWN] == 1:
            self.rect.y += 1
            self.image = self.frames[2]
        if pygame.sprite.spritecollideany(self, containers_group):
            if sp[pygame.K_LEFT] == 1:
                self.rect.x += 1
            if sp[pygame.K_RIGHT] == 1:
                self.rect.x -= 1
            if sp[pygame.K_UP] == 1:
                self.rect.y += 1
            if sp[pygame.K_DOWN] == 1:
                self.rect.y -= 1
        if pygame.sprite.spritecollideany(self, box_group):
            box_group.update()

    def back(self, moving):
        if moving == 'down':
            self.rect.y -= 1
        elif moving == 'up':
            self.rect.y += 1
        elif moving == 'right':
            self.rect.x -= 1
        elif moving == 'left':
            self.rect.x += 1


class Box(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(box_group, all_sprites)
        self.image = box_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.finishing = False

    def update(self):
        global finish_tick
        sp = pygame.key.get_pressed()
        if sp[pygame.K_LEFT] == 1:
            self.rect.x -= 1
        if sp[pygame.K_RIGHT] == 1:
            self.rect.x += 1
        if sp[pygame.K_UP] == 1:
            self.rect.y -= 1
        if sp[pygame.K_DOWN] == 1:
            self.rect.y += 1
        if pygame.sprite.spritecollideany(self, containers_group):
            if sp[pygame.K_LEFT] == 1:
                self.rect.x += 1
                forklift.back('left')
            if sp[pygame.K_RIGHT] == 1:
                self.rect.x -= 1
                forklift.back('right')
            if sp[pygame.K_UP] == 1:
                self.rect.y += 1
                forklift.back('up')
            if sp[pygame.K_DOWN] == 1:
                self.rect.y -= 1
                forklift.back('down')
        if self.rect.x in range(finish_coords[0] - 10,
                                finish_coords[0] + 10) and self.rect.y in range(
            finish_coords[1] - 10, finish_coords[1] + 10) and not self.finishing:
            print('Congratulations!')
            self.finishing = True
            finish_tick = pygame.time.get_ticks()
            pygame.image.save(screen, "after_level.jpg")
            draw_image_after_finish('after_level.jpg')
            pause_screen()
            terminate()


class Button:
    def __init__(self, but_width, but_height, inactive_color, active_color):
        self.width = but_width
        self.height = but_height
        self.inactive_color = inactive_color
        self.active_color = active_color

    def draw(self, x, y, message, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pygame.draw.rect(screen, (23, 204, 58), (x, y, self.width, self.height))

                if click[0] == 1:
                    pygame.mixer.Sound.play(button_sound)
                    pygame.time.delay(500)
                    if action is not None:
                        action()

        else:
            pygame.draw.rect(screen, (13, 162, 58), (x, y, self.width, self.height))


def game(map_name='map.txt'):
    global forklift, box_game, tile_width, tile_height, crate, all_sprites, containers_group
    global tile_images, forklift_group, box_group, box_image
    font = pygame.font.Font('Data/main_font.ttf', 50)
    finish_tick = 0

    forklift = None
    box_game = None

    finish_coords = -1, -1

    all_sprites = pygame.sprite.Group()
    crate = pygame.sprite.Group()
    containers_group = pygame.sprite.Group()
    forklift_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group()

    tile_width = tile_height = 50

    tile_images = {
        'container_1': load_image('container_1.jpg'),
        'container_2': load_image('container_2.jpg'),
        'container_3': load_image('container_3.jpg'),
        'container_4': load_image('container_4.jpg'),
        'container_5': load_image('container_5.jpg'),
        'crate': load_image('fon.jpg'),
        'finish': load_image('crown.png')}

    forklift_image = load_image('forklift.png')
    box_image = load_image('box.png')

    forklift, box_game, level_x, level_y = generate_level(load_level(map_name))
    start_tick = pygame.time.get_ticks()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                forklift_group.update()

        screen.fill((160, 160, 160))
        all_sprites.draw(screen)
        box_group.draw(screen)
        forklift_group.update()
        forklift_group.draw(screen)
        clock.tick(FPS)
        if not finish_tick:
            now_tick = pygame.time.get_ticks()
        else:
            now_tick = finish_tick
        seconds = (now_tick - start_tick) // 1000
        minutes = seconds // 60
        seconds = str(seconds % 60)
        if len(seconds) == 1:
            seconds = '0' + seconds
        time_render = font.render(f'{minutes}:{seconds}', True, pygame.Color('#3574e8'))
        screen.blit(time_render, (410, 5))
        pygame.display.flip()


game()

pygame.quit()
