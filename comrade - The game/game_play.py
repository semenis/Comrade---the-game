import sys
import requests
import pygame
import os
import math
import copy
import threading

def map_request(lon, lat, layer, spn):
    try:
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": ",".join([str(lon), str(lat)]),
            "spn": ",".join([str(spn), str(spn)]),
            "l": layer,
            "size": '650,385'
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


def write_image(response):
    map_file = "data/map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
        return map_file
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)


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


class Everything(pygame.sprite.Sprite):
    def __init__(self, *group, coors, images, loading=True):
        super().__init__(*group)
        self.frames = []
        self.current_frame = 0
        if loading:
            for image in images:
                self.frames.append(load_image(image))
        else:
            for image in images:
                self.frames.append(image)
        self.copy_images = self.frames[:]
        self.image = self.frames[self.current_frame]
        self.rect = self.frames[self.current_frame].get_rect()
        self.rect.x = coors[0]
        self.rect.y = coors[1]

    def destroy_itself(self):
        self.kill()

    def resize_images(self, cell_size):
        for frame in range(len(self.frames)):
            self.frames[frame] = pygame.transform.scale(self.frames[frame], (cell_size - 1, cell_size - 1))
        self.copy_images = self.frames[:]
        self.rect.h = cell_size
        self.rect.w = cell_size

    def update_frame(self):
        self.current_frame += 1
        if len(self.frames) <= self.current_frame:
            self.current_frame = 0
        self.image = self.frames[self.current_frame]


class Hero(Everything):
    def __init__(self, *group, bullets, center, coors, surface, size, lon, lat, layer, spn):
        self.CONST_SPEED = 2
        self.direction = 0
        self.center = center
        self.size = size
        images = ["Hero/" + file for file in os.listdir("data/Hero")]
        self.bullets = bullets
        self.pressed = False

        self.response = None
        self.surface = surface
        self.lon = lon
        self.lat = lat
        self.layer = layer
        self.spn = spn
        self.response = map_request(self.lon, self.lat, self.layer, self.spn)
        write_image(self.response)
        self.location = load_image("map.png")

        super().__init__(*group, coors=coors, images=images, loading=True)
        self.old_rect = copy.deepcopy(self.rect)

    def fire(self):
        Bullet(self.bullets, coors=(self.rect.x + self.rect.w//2, self.rect.y + self.rect.h//2), direction=self.direction)

    def players_control(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.pressed = pygame.K_UP
            elif event.key == pygame.K_DOWN:
                self.pressed = pygame.K_DOWN
            elif event.key == pygame.K_LEFT:
                self.pressed = pygame.K_LEFT
            elif event.key == pygame.K_RIGHT:
                self.pressed = pygame.K_RIGHT

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.fire()

        elif event.type == pygame.MOUSEMOTION:
            self.direction = -int(math.degrees(math.atan2(self.rect.center[1] - event.pos[1],
                                                          self.rect.center[0] - event.pos[0]))) + 90

            self.image = pygame.transform.rotate(self.copy_images[self.current_frame], self.direction)
            rect1 = self.image.get_rect()

            old_center = ((self.rect.x + self.rect.w // 2), (self.rect.y + self.rect.h // 2))
            new_center = ((self.rect.x + rect1.w // 2), (self.rect.y + rect1.h // 2))
            coors = (
            self.old_rect.x - (new_center[0] - old_center[0]), self.old_rect.y - (new_center[1] - old_center[1]))
            self.rect.x = coors[0]
            self.rect.y = coors[1]
            self.motion = False

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                self.pressed = False

    def update(self):
        if self.pressed in [pygame.K_UP, pygame.K_DOWN]:
            delta_x = int(round(math.cos(math.radians(self.direction + 90)))) * self.CONST_SPEED
            delta_y = int(round(math.sin(math.radians(self.direction + 90)))) * self.CONST_SPEED
        elif self.pressed in [pygame.K_RIGHT, pygame.K_LEFT]:
            delta_x = int(round(math.cos(math.radians(self.direction)))) * self.CONST_SPEED
            delta_y = int(round(math.sin(math.radians(self.direction)))) * self.CONST_SPEED
        else:
            delta_x, delta_y = 0, 0

        if self.pressed == pygame.K_RIGHT:
            # self.lon += math.cos(math.radians(self.direction)) * self.CONST_SPEED * 0.0001
            # self.lat -= math.sin(math.radians(self.direction)) * self.CONST_SPEED * 0.0001
            self.old_rect.x += delta_x
            self.old_rect.y -= delta_y

            self.rect.x += delta_x
            self.rect.y -= delta_y
            # changed = True

        elif self.pressed == pygame.K_LEFT:
                self.old_rect.x -= delta_x
                self.old_rect.y += delta_y

                self.rect.x -= delta_x
                self.rect.y += delta_y

        elif self.pressed == pygame.K_UP:
            self.old_rect.x += delta_x
            self.old_rect.y -= delta_y
            self.rect.x += delta_x
            self.rect.y -= delta_y

        elif self.pressed == pygame.K_DOWN:
            self.old_rect.x += delta_x
            self.old_rect.y += delta_y

            self.rect.x += delta_x
            self.rect.y += delta_y

        BORDER = 30
        CONST_CHANGE = 0.0003
        changed = False
        if self.rect.x < BORDER:
            self.lon -= CONST_CHANGE
            changed = True

        elif self.rect.right > self.size[0] - BORDER:
            self.lon += CONST_CHANGE
            changed = True

        elif self.rect.y < BORDER:
            self.lat += CONST_CHANGE
            changed = True

        elif self.rect.bottom > self.size[1] - BORDER:
            self.lat -= CONST_CHANGE
            changed = True

        if changed and self.pressed:
            self.response = map_request(self.lon, self.lat, self.layer, self.spn)
            write_image(self.response)
            self.location = load_image("map.png")
            self.rect.x, self.rect.y = self.center[0] - self.rect.w//2, self.center[1] - self.rect.h//2
            # self.rect.right = self.rect.x + self.rect.w
            # self.rect.bottom = self.rect.y + self.rect.h
            self.old_rect = copy.deepcopy(self.rect)

    def render(self):
        self.surface.blit(self.location, (0, 0))
        self.surface.blit(self.image, self.rect)


class Loot(Everything):
    def __init__(self):
        pass


class Enemy(Everything):
    def __init__(self):
        pass


class Bullet(Everything):
    def __init__(self, *group, coors, direction):
        self.CONST_SPEED = 10
        self.direction = direction
        self.images = ['Weapon/Bullet.png']
        super().__init__(group, coors=coors, images=self.images, loading=True)
        self.image = pygame.transform.rotate(self.image, self.direction)

    def update(self):
        delta_x = -int(round(math.cos(math.radians(self.direction + 90)))) * self.CONST_SPEED
        delta_y = -int(round(math.sin(math.radians(self.direction + 90)))) * self.CONST_SPEED
        self.rect.x -= delta_x
        self.rect.y += delta_y


class Game_play:
    def __init__(self, size, surface, lon, lat, layer, spn):
        self.pressed = False
        self.enemies = []
        self.all_sprites = pygame.sprite.Group()
        self.surface = surface
        self.center = (size[0]//2, size[1]//2)

        self.Bullets = pygame.sprite.Group()
        self.Units = pygame.sprite.Group()
        self.hero = Hero(self.all_sprites, self.Units, center=self.center, bullets=self.Bullets, coors=(self.center[0] - 50, self.center[1] - 50),
                         surface=surface, size=size, lon=lon, lat=lat, layer=layer, spn=spn)


    def hero_updater(self):
        self.hero.update()

    def Bullets_update(self):
        for bullet in self.Bullets:
            bullet.update()

    def event_tracker(self, event):
        self.hero.players_control(event)

    def update(self, event):
        self.threading_update = [threading.Thread(target=self.event_tracker(event)),
                                 threading.Thread(target=self.hero_updater),
                                 threading.Thread(target=self.Bullets_update)]
        for i in self.threading_update:
            i.start()
        for i in self.threading_update:
            i.join()


    def render(self):
        self.hero.render()
        self.all_sprites.draw(self.surface)
        self.Bullets.draw(self.surface)

def main():
    size = width, height = (650, 385)
    screen = pygame.display.set_mode(size)
    pygame.display.set_icon(pygame.image.load('data/icon.png'))

    spn = 0.001
    lon, lat = 13.406888, 52.517694
    layer = ('map', 'sat', 'skl')
    game = Game_play(size, screen, lon, lat, layer[1], spn)
    TIMER_ID = 10
    pygame.time.set_timer(TIMER_ID, 20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit(0)

            game.update(event)
        game.render()
        pygame.display.flip()


if __name__ == '__main__':
    main()
