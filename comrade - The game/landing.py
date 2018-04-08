import requests
import sys
import os
import pygame
import _thread

spn = 25
lon, lat = 13.406888, 52.517481

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

# Рисуем картинку, загружаемую из только что созданного файла.

# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
import random

running = True
vistrels = []

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
        screen.blit(pygame.image.load('data/parashut.png'),
                    (230 + random.randrange(-wind_power, wind_power), 100 + random.randrange(-wind_power, wind_power)))
        pygame.display.flip()
    pygame.display.flip()
    screen.blit(pygame.image.load('data/mapscash/' + str(spnlen - 1) + 'map.png'), (0, 0))
    pygame.time.wait(500)
    running = False
from game_play import main

main()
pygame.quit()
