from file_with_functions import *

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 200

forklift = None

all_sprites = pygame.sprite.Group()
crate = pygame.sprite.Group()
containers_group = pygame.sprite.Group()
forklift_group = pygame.sprite.Group()

tile_width = tile_height = 50

tile_images = {
    'container': load_image('container_1.jpg'),
    'crate': load_image('unnamed.jpg')}

forklift_image = load_image('forklift.png', -1)


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('crate', x, y)
            elif level[y][x] == '#':
                Tile('container', x, y)
            elif level[y][x] == '@':
                Tile('crate', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(crate, all_sprites)
        if tile_type == 'container':
            containers_group.add(self)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(forklift_group, all_sprites)
        self.image = forklift_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

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
            if sp[pygame.K_RIGHT] == 1:
                self.rect.x -= 1
            if sp[pygame.K_UP] == 1:
                self.rect.y += 1
            if sp[pygame.K_DOWN] == 1:
                self.rect.y -= 1


forklift, level_x, level_y = generate_level(load_level('map.txt'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            forklift_group.update()

    screen.fill((160, 160, 160))
    all_sprites.draw(screen)
    forklift_group.update()
    forklift_group.draw(screen)
    pygame.display.flip()

pygame.quit()
