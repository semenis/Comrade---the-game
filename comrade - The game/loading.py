import pygame
import os
import random

def load_image(name, colorkey = None):
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

pygame.init()
size = width,height = (830,385)
speed = 200
screen = pygame.display.set_mode(size);
screen.fill((0,0,0));
redworld = load_image('redworld.png');


image = load_image('has100.png');
running = True;
coords = [365, -300]

image1 = image
agle = 0 


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False;
    if coords[1]<120:
        pygame.time.wait(5)
        coords[1] += 1
    else:
        pygame.time.wait(5)
        image1 = pygame.transform.rotate(image, agle)
        agle+=1
        if agle>=359:
            agle = 0
        #image = pygame.transform.rotate(image,1)
        #Не работает нормально 
        #Приделал костыль
    screen.fill((0, 0, 0));
    screen.blit(redworld,(0,0))
    screen.blit(image1,coords)
    print("Loading data"+random.randint(1,3)*'.')
   # print(coords)
    pygame.display.flip();
pygame.quit();
