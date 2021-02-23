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
cong_sound = pygame.mixer.Sound('data/congratulations.wav')


def print_text(message, x, y, font_color=(0, 0, 0), font_type='data/calibri.ttf', font_size=25):
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


def remake_image(im_name):
    im = Image.open(im_name)
    pixels = im.load()
    x, y = im.size

    for i in range(x):
        for j in range(y):
            r, g, b = pixels[i, j]
            r, g, b = r // 3, g // 3, (b + 255) // 2
            pixels[i, j] = r, g, b

    im.save(f'data/{im_name}')


class Button:
    def __init__(self, but_width, but_height, active_clr=(23, 204, 58), inactive_clr=(13, 162, 58),
                 size_of=25):
        self.width = but_width
        self.height = but_height
        self.active_clr = active_clr
        self.inactive_clr = inactive_clr
        self.size_of = size_of

    def draw(self, x, y, message, action=None, term=False, level=None, inactive=True):
        global correct_level
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height and inactive:
            pygame.draw.rect(screen, self.active_clr, (x, y, self.width, self.height))

            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(200)
                if action == game:
                    if level is None:
                        action(correct_level)
                        if term:
                            terminate()
                    else:
                        action(level)
                        if term:
                            terminate()
                elif action is not None:
                    action()
                    if term:
                        terminate()
        else:
            pygame.draw.rect(screen, self.inactive_clr, (x, y, self.width, self.height))

        print_text(message, x + 7, y + 10, font_size=self.size_of)


class ImButton:
    def __init__(self, but_width, but_height, active_im, inactive_im):
        self.width = but_width
        self.height = but_height
        self.active_im = load_image(active_im)
        self.inactive_im = load_image(inactive_im)

    def draw(self, x, y, action=None, term=False, level=None, inactive=True):
        global correct_level
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed(3)
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height and inactive:
            screen.blit(self.active_im, (x, y))

            if click[0] == 1:
                pygame.mixer.Sound.play(button_sound)
                pygame.time.delay(200)
                if action == game:
                    if level is None:
                        action(correct_level)
                        if term:
                            terminate()
                    else:
                        action(level)
                        if term:
                            terminate()
                elif action is not None:
                    action()
                    if term:
                        terminate()
        else:
            screen.blit(self.inactive_im, (x, y))


class Info(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('how_to_play.png')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


def show_info():
    start_group = pygame.sprite.Group()
    Info(start_group)
    running = True

    close_but = Button(90, 45, size_of=30)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        start_group.draw(screen)
        close_but.draw(400, 445, 'CLOSE', menu_screen, term=True)
        pygame.display.flip()


class Menu(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('crate_texture.jpg')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


def menu_screen():
    start_group = pygame.sprite.Group()
    Menu(start_group)
    but_1 = Button(50, 50, size_of=35)
    but_2 = Button(50, 50, size_of=35)
    but_3 = Button(50, 50, size_of=35)
    but_4 = Button(50, 50, size_of=35)
    but_5 = Button(50, 50, size_of=35)
    but_6 = Button(50, 50, size_of=35)
    but_7 = Button(50, 50, size_of=35)
    but_8 = Button(50, 50, size_of=35)
    but_9 = Button(50, 50, size_of=35)
    but_10 = Button(50, 50, size_of=35)
    info_but = ImButton(50, 50, 'active_info.jpg', 'inactive_info.jpg')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        start_group.draw(screen)

        print_text('Porter', 175, 100, (255, 255, 255), 'Data/main_font.ttf', 50)
        print_text('Уровень:', 160, 200, (255, 255, 255), font_size=50)
        but_1.draw(115, 250, ' 1', game, True, 'map1.txt')
        but_2.draw(170, 250, ' 2', game, True, 'map2.txt')
        but_3.draw(225, 250, ' 3', game, True, 'map3.txt')
        but_4.draw(280, 250, ' 4', game, True, 'map4.txt')
        but_5.draw(335, 250, ' 5', game, True, 'map5.txt')
        but_6.draw(115, 305, ' 6', game, True, 'map6.txt')
        but_7.draw(170, 305, ' 7', game, True, 'map7.txt')
        but_8.draw(225, 305, ' 8', game, True, 'map8.txt')
        but_9.draw(280, 305, ' 9', game, True, 'map9.txt')
        but_10.draw(335, 305, '10', game, True, 'map10.txt')
        info_but.draw(440, 440, show_info)

        pygame.display.flip()
        clock.tick(FPS)


class Finish(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.image = load_image('after_level.jpg')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


def finish_screen():
    global start_tick, finish_tick, correct_level
    start_group = pygame.sprite.Group()
    Finish(start_group)
    seconds = (finish_tick - start_tick) // 1000
    minutes = seconds // 60
    seconds = str(seconds % 60)

    rerun_but = Button(80, 40)
    menu_but = Button(80, 40)
    next_but = Button(80, 40)
    wr_obl = correct_level[3:correct_level.index('.')]
    if int(wr_obl) < 10:
        next_level = f'map{int(wr_obl) + 1}.txt'
    else:
        final_sreen()

    if len(seconds) == 1:
        seconds = '0' + seconds
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        start_group.draw(screen)

        print_text('Поздравляем, вы прошли', 40, 100, (255, 255, 255), font_size=40)
        print_text('уровень!', 190, 150, (255, 255, 255), font_size=40)
        print_text(f'Вы справились за: {minutes}:{seconds}', 65, 200, (255, 255, 255), font_size=40)

        rerun_but.draw(125, 350, 'Rerun', game, True)
        menu_but.draw(210, 350, 'Menu', menu_screen, True)
        next_but.draw(295, 350, ' Next', game, True, next_level)

        pygame.display.flip()
        clock.tick(FPS)


def final_sreen():
    global start_tick, finish_tick, correct_level
    start_group = pygame.sprite.Group()
    Finish(start_group)
    seconds = (finish_tick - start_tick) // 1000
    minutes = seconds // 60
    seconds = str(seconds % 60)

    rerun_but = Button(80, 40)
    menu_but = Button(80, 40)

    if len(seconds) == 1:
        seconds = '0' + seconds
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        start_group.draw(screen)

        print_text('Поздравляем, вы прошли', 40, 100, (255, 255, 255), font_size=40)
        print_text('уровень!', 190, 150, (255, 255, 255), font_size=40)
        print_text(f'Вы справились за: {minutes}:{seconds}', 55, 200, (255, 255, 255), font_size=40)
        print_text('Это был последний', 95, 250, (255, 255, 255), font_size=40)
        print_text('уровень.', 190, 300, (255, 255, 255), font_size=40)

        rerun_but.draw(167, 350, 'Rerun', game, True)
        menu_but.draw(252, 350, 'Menu', menu_screen, True)

        pygame.display.flip()
        clock.tick(FPS)


class Pause(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        pygame.image.save(screen, 'pause_im.jpg')
        remake_image('pause_im.jpg')
        self.image = load_image('pause_im.jpg')
        os.remove('pause_im.jpg')
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()


def pause_screen():
    global start_tick
    start_pause_tick = pygame.time.get_ticks()
    start_group = pygame.sprite.Group()
    Pause(start_group)

    pause_button = ImButton(43, 43, 'active_pause.jpg', 'inactive_pause.jpg')
    rerun_button = ImButton(43, 43, 'active_rerun.jpg', 'inactive_rerun.jpg')
    menu_button = Button(70, 43)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                start_tick += pygame.time.get_ticks() - start_pause_tick
                pygame.mixer.Sound.play(button_sound)
                return
        start_group.draw(screen)

        print_text('Press any key...', 120, 400, (255, 255, 255), 'Data/main_font.ttf', 40)

        pause_button.draw(3, 3, inactive=False)
        rerun_button.draw(49, 3, game)
        menu_button.draw(95, 3, 'Menu', menu_screen)

        pygame.display.flip()
        clock.tick(FPS)


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
        if self.rect.x in range(finish_coords[0] - 5,
                                finish_coords[0] + 13) and self.rect.y in range(
            finish_coords[1] - 5, finish_coords[1] + 13) and not self.finishing:
            print('Congratulations!')
            self.finishing = True
            finish_tick = pygame.time.get_ticks()
            pygame.image.save(screen, "after_level.jpg")
            remake_image('after_level.jpg')
            os.remove('after_level.jpg')
            pygame.mixer.Sound.play(cong_sound)
            finish_screen()
            terminate()


def generate_level(level):
    global finish_coords
    new_player, box_object, x, y = None, None, None, None
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
    # добавим границу слева и сверху
    for y in range(len(level)):
        Tile('container_1', -1, y)
    for x in range(len(level[y])):
        Tile('container_1', x, -1)
    return new_player, box_object, x, y


def game(map_name='map0.txt'):
    global forklift, box_game, tile_width, tile_height, crate, all_sprites, containers_group
    global tile_images, forklift_group, box_group, box_image, start_tick, correct_level
    font = pygame.font.Font('Data/main_font.ttf', 50)
    finish_tick = 0

    forklift = None
    box_game = None

    correct_level = map_name

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

    box_image = load_image('box.png')

    forklift, box_game, level_x, level_y = generate_level(load_level(map_name))

    pause_button = ImButton(43, 43, 'active_pause.jpg', 'inactive_pause.jpg')
    rerun_button = ImButton(43, 43, 'active_rerun.jpg', 'inactive_rerun.jpg')
    menu_button = Button(70, 43)

    start_tick = pygame.time.get_ticks()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                forklift_group.update()
                sp = pygame.key.get_pressed()
                if sp[pygame.K_p] or sp[pygame.K_F9]:
                    pygame.mixer.Sound.play(button_sound)
                    pause_screen()
                if sp[pygame.K_F5]:
                    pygame.mixer.Sound.play(button_sound)
                    game(correct_level)

        screen.fill((160, 160, 160))

        all_sprites.draw(screen)
        box_group.draw(screen)
        forklift_group.update()
        forklift_group.draw(screen)

        pause_button.draw(3, 3, pause_screen)
        rerun_button.draw(49, 3, game, term=True, level=correct_level)
        menu_button.draw(95, 3, 'Menu', menu_screen, term=True)

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
        time_render = font.render(f'{minutes}:{seconds}', True, (13, 162, 58))
        screen.blit(time_render, (410, 5))
        pygame.display.flip()


menu_screen()

pygame.quit()
