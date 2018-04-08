def downloadscore():
    with open('data/score') as file:
        a = eval(file.readline())
        return a


def intscorechange(change=0, name='kills'):
    with open('data/score') as file:
        a = eval(file.readline())
    a[name] += change
    with open('data/score', 'w') as file:
        file.write(str(a))


def scoresetvalue(value, name):
    with open('data/score') as file:
        a = eval(file.readline())
    a[name] = value
    with open('data/score', 'w') as file:
        file.write(str(a))
