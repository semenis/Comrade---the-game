import requests
import sys
import os
import pygame
import _thread

spn = 25
import scoreworking

a = scoreworking.downloadscore()
lon, lat = a['current coordinats']
# lon, lat = 13.406888, 52.517481

from desanting import desanting

l = _thread.allocate_lock()  # создаём блокировку


def load():
    delay_ = 17
    from loading import loading
    loading(delay_)
    l.acquire()


_thread.start_new_thread(load, ())
desanting(lon, lat)

while not l.locked():
    pass

size = width, height = (650, 385)
screen = pygame.display.set_mode((size))
pygame.display.flip()
pygame.display.set_icon(pygame.image.load('data/icon.png'))
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("data/wind.mp3")

# Рисуем картинку, загружаемую из только что созданного файла.

# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
import random

running = True
vistrels = []
pygame.mixer.music.play(0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    spnlen = 22
    for i in range(spnlen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        delay = 1000
        pygame.time.wait(delay)
        screen.blit(pygame.image.load('data/mapscash/' + str(i) + 'map.png'), (0, 0))
        wind_power = 10
        coords = (230, 100)
        screen.blit(pygame.image.load('data/parashut.png'),
                    (coords[0] + random.randrange(-wind_power, wind_power),
                     coords[1] + random.randrange(-wind_power, wind_power)))
        pygame.display.flip()
    pygame.display.flip()
    screen.blit(pygame.image.load('data/mapscash/' + str(spnlen - 1) + 'map.png'), (0, 0))

    import scoreworking

    scoreworking.intscorechange(1, 'desanting times')
    inlandtimedelay = 500
    pygame.time.wait(inlandtimedelay)
    running = False
pygame.mixer.music.stop()
from game_play import main

main()
pygame.quit()
