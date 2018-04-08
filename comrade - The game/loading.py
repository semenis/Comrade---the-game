import pygame
import os
import time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def loading(delay):
    pygame.init()
    size = width, height = (830, 385)
    speed = 200
    screen = pygame.display.set_mode(size)
    pygame.display.set_icon(pygame.image.load('data/icon.png'))
    screen.fill((0, 0, 0))

    pygame.mixer.init()
    pygame.mixer.music.load("data/ost.mp3")
    pygame.mixer.music.play(0)

    redworld = load_image('redworld.png')

    image = load_image('has100.png')
    running = True
    rect = image.get_rect()
    coords = [width // 2 - rect.w // 2, 0]
    center = (width // 2, height // 2)

    image1 = image
    agle = 0

    ID_TIMER = 10
    pygame.time.set_timer(ID_TIMER, 20)
    rotating = False

    start = time.time()
    print(start)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ID_TIMER:
                if coords[1] < (height // 2 - rect.h // 2) and not rotating:
                    coords[1] += 1

                else:
                    rotating = True
                    image1 = pygame.transform.rotate(image, agle)
                    rect1 = image1.get_rect()
                    coords = (center[0] - rect1.width // 2, center[1] - rect1.height // 2)
                    agle += 1
                    if agle >= 359:
                        agle = 0
                    # Не работает нормально
                    # Приделал костыль

        screen.fill((0, 0, 0))
        screen.blit(redworld, (0, 0))
        screen.blit(image1, coords)
        if time.time() - start > delay:
            running = False
        # print("Loading data"+random.randint(1, 3)*'.')
        pygame.display.flip()

    pygame.quit()
# loading(1500)
