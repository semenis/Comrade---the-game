import requests, sys, os
import pygame

spn = 25
lon, lat = 13.406888, 52.517481
sloy = ('map', 'sat', 'skl')


def map_request():
    try:
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "spn": ",".join([str(spn), str(spn)]),
            "l": sloy[1],
            "size":'650,385'
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        return response
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)

def load_image():
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
        return map_file
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

import random
def resize(spn,lon,lat, event):
    if event.key == pygame.K_PAGEUP:
        if spn * 1.8 > 90:
            spn = 90
        elif spn < 1:
            spn *= 3
        else:
            spn = spn * 1.8
    elif event.key == pygame.K_PAGEDOWN and spn*0.5 >= 0:
        if 0.0001 < spn < 1:
            spn *= 0.6
        elif spn > 1:
            spn *= 0.9
        else:
            spn = 0.0001
    l1 = random.randrange(-2,2)
    l2 = random.randrange(-2,2)
    lon = lon * (100-l1/100) / 100
    lat = lat * (100-l2/100) / 100
    print(spn)
    return (spn,lon,lat)

response = map_request()
map_file = load_image()
size = width,height = (650,385)
screen = pygame.display.set_mode((size))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()

running = True
changed = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            spn,lon,lat = resize(spn,lon,lat, event)
        response = map_request()
        map_file = load_image()
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.draw.circle(screen, (255,255,255), (325,193), 40)
        pygame.draw.circle(screen, (220, 220, 220), (325, 193), 37)
        pygame.display.flip()
        pygame.time.wait(5)



pygame.quit()
# Удаляем за собой файл с изображением.
os.remove(map_file)