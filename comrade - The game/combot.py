from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup
import time
import os
import requests
import config

bot_token = config.telegram_bot_api_key

reply_keyboard = [['/score', '/rules'], ['/quests', '/up_my_rang'], ['/GPS']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

quests = ['kills', 'desanting times', 'exp']
points = [1, 5, 20, 50, 100, 500, 1000, 5000]

rangs = {0: 'comrade robot', 10: 'Private', 30: 'Ensign', 50: 'Lieutenant', 100: 'Commandante', 500: 'Captain',
         2000: 'Red Army General', 5000: 'Marshall with Lenin orden'}


def finder(long_lan):
    geocoder_request = "http://geocode-maps.yandex.ru/1.x/?geocode={0}&format=json".format(long_lan)

    # Выполняем запрос.
    response = None
    try:
        response = requests.get(geocoder_request)
        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()

            # Получаем первый топоним из ответа геокодера.
            # Согласно описанию ответа он находится по следующему пути:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            # Полный адрес топонима:
            # print(toponym)
            ret = toponym['metaDataProperty']['GeocoderMetaData']['text']

            # print(ret)
            return (ret)
        else:
            return ("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
    except:
        return ("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")


# Определяем функцию-обработчик сообщений.
# У нее два параметра, сам бот и класс updater, принявший сообщение.
def echo(bot, update):
    # У объекта класса Updater есть поле message, являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str), отсылающий ответ пользователю, от которого получено сообщение.
    update.message.reply_text("Я получил сообщение \"" + update.message.text + '"')


def main():
    # Создаем объект updater. Вместо слова "TOKEN" надо разместить полученнй от @BotFather токен
    updater = Updater(bot_token)

    # Получаем из него диспетчер сообщений.
    dp = updater.dispatcher

    # Создаем обработчик сообщений типа Filters.text из описанной выше функции echo()
    # Таким образом после регистрации обработчика в диспетчере,
    # эта функция будет вызываться при получении сообщения с типом "текст", т.е. текстовых сообщений.
    text_handler = MessageHandler(Filters.text, echo)

    # Регистрируем обработчик в диспетчере.
    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("score", score))
    dp.add_handler(CommandHandler("rules", rules))
    dp.add_handler(CommandHandler("quests", quests_))
    dp.add_handler(CommandHandler("up_my_rang", up_my_rang))
    dp.add_handler(CommandHandler("GPS", gps))
    # Запускаем цикл приема и обработки сообщений.
    updater.start_polling()

    # Ждем завершения приложения. (например, получение сигнала SIG_TERM при нажатии клавиш Ctrl+C)
    updater.idle()


def start(bot, update):
    update.message.reply_text("Добро пожаловать в игру, Comrade! Объяснить тебе немного правил?", reply_markup=markup)


def score(bot, update):
    try:
        import scoreworking
        a = scoreworking.downloadscore()
        update.message.reply_text("Вы убили " + str(a['kills']) + " врагов.")
        update.message.reply_text("Вы десантировались " + str(a['desanting times']) + " раз.")
        update.message.reply_text("Ваш ранг " + str(a['rang']))
    except Exception as e:
        update.message.reply_text("Ошибка {} в штабе командования, шшш...".format(e))
        time.sleep(3)
        update.message.reply_text("АААА!!!ХПХПХП")


def rules(bot, update):
    update.message.reply_text(
        "Ваша задача десантироваться на вражескую территорию и передвигаясь по карте, уничтожить врагов коммунизма, играя за гиганского робота. Вперед к победе, Comrade!\nДля управления роботом используйте стрелочки, мышь. Для стрельбы - кнопка мыши.")


def quests_(bot, update):
    update.message.reply_text('Ваши текущие квесты:')
    for i in quests:
        import scoreworking
        a = scoreworking.downloadscore()
        kolvo = a[i]
        print(kolvo)
        c = []
        global points
        target = 0
        for j in points:
            if kolvo < j:
                c.append(j)
            try:
                target = min(c)
            except:
                pass
        if target != 0:
            update.message.reply_text(i + ' ' + str(target) + '\nОсталось ' + str(target - kolvo))


def up_my_rang(bot, update):
    import scoreworking
    a = scoreworking.downloadscore()
    update.message.reply_text('Ваш текущий ранг: ' + a['rang'])
    exp = a['exp']
    update.message.reply_text('Ваш опыт: ' + str(exp))
    c = []
    for i in rangs.keys():
        if exp > i:
            c.append(i)
    update.message.reply_text('Вы заслуживаете ранг: ' + rangs[max(c)])
    scoreworking.scoresetvalue(rangs[max(c)], 'rang')
    with open('data/lvlup.mp3', 'rb') as file:
        # print(file)
        print(bot.send_voice(update.message.chat.id, file))


def gps(bot, update):
    import scoreworking
    a = scoreworking.downloadscore()

    coords = a['current coordinats']

    update.message.reply_text('Последник раз вы замечены в : ' + str(coords))
    try:

        bot.send_venue(update.message.chat.id, latitude=coords[1], longitude=coords[0], title='Coords',
                       address=finder(str(coords[0]) + ',' + str(coords[1])))
    except Exception as e:
        print(e)


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
