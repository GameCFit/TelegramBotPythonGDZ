import telebot
from telebot import types

import sqlite3

botKey = ""

RU_8CLASS_BARHNEW = "https://reshak.ru/reshebniki/russkijazik/8/barh_new/images1/"
AL_7CLASS_MAKARICHEV = "https://reshak.ru/reshebniki/algebra/7/makarichev/images/"
AL_8CLASS_MAKARICHEV2 = "https://reshak.ru/reshebniki/algebra/8/makarichev2/images1/"
PHY_8CLASS_PYRUSHKIN = "https://reshak.ru/reshebniki/fizika/8/perishkin/images1/paragraph/"
GEOM_789CLASS_ATANASYAN = "https://reshak.ru/reshebniki/geometriya/7/atanasyan/images1/"
OB_7CLASS_BOGOLYBOV = "https://reshak.ru/reshebniki/obshestvo/7/bogolubov/images1/"
OB_8CLASS_BOGOLYBOV = "https://reshak.ru/reshebniki/obshestvo/8/bogolubov/images1/"
HIS_7CLASS_ARSENTEV = "https://reshak.ru/reshebniki/istoria/7/arsentev/images1/"
HIS_8CLASS_ARSENTEV = "https://reshak.ru/reshebniki/istoria/8/arsentev/images1/"
EN_8CLASS_KOMAROVA = "https://reshator.me/otvety/8-klass-komarova/"

bot = telebot.TeleBot(botKey)


# bot.send_message(5102896022, "Пошёл нах)")

@bot.message_handler()
def handle_text(message):
    print(message.chat.id, message.text)
    if message.chat.id != 5102896022:
        if checkSubs(message.chat.id) == True:
            if message.text == "/start":
                connect = sqlite3.connect('users.db')
                cursor = connect.cursor()
                connect.commit()

                people_id = message.chat.id
                cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")

                data = cursor.fetchone()
                if data is None:
                    users_list = [message.chat.id, '8', 'user', 'ru']
                    cursor.execute("INSERT INTO login_id VALUES(?,?,?,?)", users_list)
                    connect.commit()

            openMenu = False
            if message.text == "В глав. меню⬅️":
                openMenu = True

            if message.text == "подписался":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                subscrips = types.KeyboardButton('начать')
                markup.add(subscrips)
                bot.send_message(message.chat.id, f"Нажми на кнопку чтобы начать.", parse_mode='html',
                                 reply_markup=markup)

            if message.text == "/open" or openMenu == True or message.text == 'начать':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                russ = types.KeyboardButton('русский📖')
                algebra = types.KeyboardButton('алгебра🔢')
                physic = types.KeyboardButton('физика(учебник)🧭')
                geometr = types.KeyboardButton('геометрия📐')
                ob = types.KeyboardButton('обществознание🏠')
                history = types.KeyboardButton('история(россии)🏛')
                english = types.KeyboardButton('английский🇬🇧')
                donate = types.KeyboardButton('помощь в разработке💸')
                markup.add(russ, algebra, physic, geometr, ob, history, english, donate)
                bot.send_message(message.chat.id, "Выбирите предмет", parse_mode='html', reply_markup=markup)

            if message.text == "русский📖" or message.text == "алгебра🔢" or message.text == "физика(учебник)🧭" or message.text == "геометрия📐" or message.text == "обществознание🏠" or message.text == "история(россии)🏛" or message.text == "английский🇬🇧":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                grop1 = types.KeyboardButton('5 класс')
                grop2 = types.KeyboardButton('6 класс')
                grop3 = types.KeyboardButton('7 класс')
                grop4 = types.KeyboardButton('8 класс')
                grop5 = types.KeyboardButton('9 класс')
                exitToMenu = types.KeyboardButton('В глав. меню⬅️')
                markup.add(grop1, grop2, grop3, grop4, grop5, exitToMenu)
                bot.send_message(message.chat.id, "Выбирите класс", parse_mode='html', reply_markup=markup)
            if message.text == "русский📖":
                updateDataItem(message.chat.id, "ru")
            elif message.text == "алгебра🔢":
                updateDataItem(message.chat.id, "al")
            elif message.text == "физика(учебник)🧭":
                updateDataItem(message.chat.id, "phy")
            elif message.text == "геометрия📐":
                updateDataItem(message.chat.id, "geom")
            elif message.text == "обществознание🏠":
                updateDataItem(message.chat.id, "ob")
            elif message.text == "история(россии)🏛":
                updateDataItem(message.chat.id, "his")
            elif message.text == "английский🇬🇧":
                updateDataItem(message.chat.id, "en")

            if message.text == "помощь в разработке💸":
                if message.chat.id != 5068616361:
                    bot.send_message(5068616361, "кто-то донат открыл")
                bot.send_message(message.chat.id, "https://www.donationalerts.com/r/gamefit")
            if "класс" in message.text:
                numberClass = message.text[:-6]
                intNumberClass = int(numberClass)
                if intNumberClass < 10 and intNumberClass > 4:
                    connect = sqlite3.connect('users.db')
                    cursor = connect.cursor()
                    connect.commit()
                    cursor.execute(f"UPDATE login_id  SET class = {numberClass} WHERE id = {message.chat.id}")
                    connect.commit()
                    item = returnItem(message.chat.id)
                    if item != "en":
                        bot.send_message(message.chat.id, "Напишите номер вашего задания или параграфа и я пришлю решение.")
                        bot.send_message(message.chat.id, "ПРИМЕР: 'номер 4' или '№4' и я пришлю нужный параграф или номер.")
                    else:
                        bot.send_message(message.chat.id, "Напишите номер страницы и вашего задания и я пришлю решение.")
                        bot.send_message(message.chat.id, "ПРИМЕР: 'стр 16 номер 4' и я пришлю нужный параграф или номер.")
                else:
                    bot.send_sticker(message.chat.id,
                                     "CAACAgIAAxkBAAEIoJhkPqWOCchwrfhXEki_9F5rS7_IPwACdgADwZxgDAf-FiqenQ1SLwQ")
            if "номер" in message.text or "Номер" in message.text or "НОМЕР" in message.text or "№" in message.text:
                if "0" in message.text or "1" in message.text or "2" in message.text or "3" in message.text or "4" in message.text or "5" in message.text or "6" in message.text or "7" in message.text or "8" in message.text or "9" in message.text:
                    item = returnItem(message.chat.id)
                    classNumber = returnClass(message.chat.id)

                    intMassage = 0
                    if item != "en":
                        if "номер" in message.text or "Номер" in message.text or "НОМЕР" in message.text:
                            strMessage = message.text[6:]
                            intMassage = int(strMessage)
                        elif "№" in message.text:
                            strMessage = message.text[1:]
                            intMassage = int(strMessage)
                    strUrl = RU_8CLASS_BARHNEW
                    if item == "ru" and classNumber == 8:
                        strUrl = RU_8CLASS_BARHNEW
                    elif item == "al" and classNumber == 7:
                        strUrl = AL_7CLASS_MAKARICHEV
                    elif item == "al" and classNumber == 8:
                        strUrl = AL_8CLASS_MAKARICHEV2
                    elif item == "phy" and classNumber == 8:
                        strUrl = PHY_8CLASS_PYRUSHKIN
                    elif item == "geom":
                        strUrl = GEOM_789CLASS_ATANASYAN
                    elif item == "ob" and classNumber == 7:
                        strUrl = OB_7CLASS_BOGOLYBOV
                    elif item == "ob" and classNumber == 8:
                        strUrl = OB_8CLASS_BOGOLYBOV
                    elif item == "his" and classNumber == 7:
                        strUrl = HIS_7CLASS_ARSENTEV
                    elif item == "his" and classNumber == 8:
                        strUrl = HIS_8CLASS_ARSENTEV
                    elif item == "en" and classNumber == 8:
                        strUrl = EN_8CLASS_KOMAROVA
                    else:
                        bot.send_sticker(message.chat.id,
                                         "CAACAgIAAxkBAAEIoJhkPqWOCchwrfhXEki_9F5rS7_IPwACdgADwZxgDAf-FiqenQ1SLwQ")
                    if item != "en":
                        bot.send_photo(message.chat.id, f"{strUrl}{intMassage}.png", "А вот и ваше решение!")
                    else:
                        pageNumber = message.text[4:-8]
                        intPageNumber = int(pageNumber)
                        taskNumber = message.text[13:]
                        intTaskNumber = int(taskNumber)
                        bot.send_photo(message.chat.id, f"{strUrl}{intPageNumber}-z-{intTaskNumber}.png", "А вот и ваше решение!")
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            subscrips = types.KeyboardButton('подписался')
            markup.add(subscrips)
            bot.send_message(message.chat.id, f"Подпишись на канал: https://t.me/offgdz", parse_mode='html',
                             reply_markup=markup)

def updateDataItem(id, item):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    connect.commit()
    cursor.execute(f"UPDATE login_id  SET item = '{item}' WHERE id = {id}")
    connect.commit()

def returnClass(id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sqlite_select_query = """SELECT * from login_id"""
    cursor.execute(sqlite_select_query)
    users = cursor.fetchall()
    for user in users:
        if user[0] == id:
            return user[1]

def checkSubs(id):
    my_channel_id = -1001982222820
    statuss = ['creator', 'administrator', 'member']
    for i in statuss:
        if i == bot.get_chat_member(chat_id=my_channel_id, user_id=id).status:
            return True
    return False

def returnItem(id):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    sqlite_select_query = """SELECT * from login_id"""
    cursor.execute(sqlite_select_query)
    users = cursor.fetchall()
    for user in users:
        if user[0] == id:
            return user[3]

bot.polling(none_stop=True, interval=0)
