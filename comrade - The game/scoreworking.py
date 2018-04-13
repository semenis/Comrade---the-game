# Возвращает весь текущий score в виде словаря
def downloadscore():
    with open('data/score') as file:
        data = eval(file.readline())
        return data


# Изменяет на значение change заданное значение score (Внимание, только числовые значения), change так же может быть отрицателен
def intscorechange(change=0, name='kills'):
    with open('data/score') as file:
        data = eval(file.readline())
    data[name] += change
    with open('data/score', 'w') as file:
        file.write(str(data))


# Задает значение value заданному score. Value - любой, но следите за совместимостью.
def scoresetvalue(value, name):
    with open('data/score') as file:
        data = eval(file.readline())
    data[name] = value
    with open('data/score', 'w') as file:
        file.write(str(data))


# Сбрасывает score до начального состояния
def clearscore():
    with open('data/score', 'w') as file:
        file.write(str(
            {'kills': 0, 'desanting times': 0, 'rang': 'comrade robot', 'exp': 0, 'current coordinats': (13.406888,
                                                                                                         52.517694)}) + '\n#При изменении количества значений, измените значения по умолчанию в scoreworking.py')
