from main import *

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 200


def menu_screen():
    but_1 = Button(50, 50)
    but_2 = Button(50, 50)
    but_3 = Button(50, 50)
    but_4 = Button(50, 50)
    but_5 = Button(50, 50)
    but_6 = Button(50, 50)
    but_7 = Button(50, 50)
    but_8 = Button(50, 50)
    but_9 = Button(50, 50)
    but_10 = Button(50, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((167, 216, 255))

        but_1.draw(105, 300, '1', game, True, 'map1.txt')
        but_2.draw(160, 300, '2', game, True, 'map2.txt')
        but_3.draw(215, 300, '3', game, True, 'map3.txt')
        but_4.draw(270, 300, '4', game, True, 'map4.txt')
        but_5.draw(325, 300, '5', game, True, 'map5.txt')
    pygame.display.flip()


menu_screen()

pygame.quit()
