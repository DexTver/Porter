from file_with_functions import *
from random import randrange

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 200

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


forklift, box_game, level_x, level_y = generate_level(load_level('map.txt'))
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
    pygame.display.flip()

pygame.quit()
