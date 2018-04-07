import requests
import sys
import os
import pygame

sloy = ('map', 'sat', 'skl')
spns = [25,13,9,5,3,2,1.3,1.2,1,0.7,0.5,0.25,0.17,0.1,0.05,0.03,0.01,0.008,0.006,0.004,0.002,0.001]

def desanting(lon, lat):
    def map_generator(lon, lat, spn, file_name):
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

        def load_image(response):
            map_file = 'data/mapscash/'+str(file_name)+"map.png"
            try:
                with open(map_file, "wb") as file:
                    file.write(response.content)
                return map_file
            except IOError as ex:
                print("Ошибка записи временного файла:", ex)
                sys.exit(2)
        load_image(map_request())
    for i in range(len(spns)):
        map_generator(lon,lat,spns[i],i)