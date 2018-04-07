import requests
import sys
import os
import pygame


spn = 25
lon, lat = 13.406888, 52.517481

from desanting import desanting

#При тестировании запустить один раз и закомментить, оно все скачает и норм
#TODO добавить "import loading" в параллельный процесс, пока качаются картинки...
desanting(lon,lat)

size = width,height = (650,385)
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
        screen.blit(pygame.image.load('data/mapscash/'+str(i)+'map.png'), (0, 0))
        screen.blit(pygame.image.load('data/parashut.png'), (230+random.randrange(-5,5),100+random.randrange(-5,5)))
        pygame.display.flip()
    pygame.display.flip()
    screen.blit(pygame.image.load('data/mapscash/' + str(spnlen-1) + 'map.png'), (0, 0))
    pygame.time.wait(500)
    running = False
from game_play import main
main()
pygame.quit()
