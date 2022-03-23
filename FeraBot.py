import telebot
from telebot import types
import datetime
import requests
import random
import time


# constants
token = '5271242337:AAEYourhpVneeXorK_00_btpAxwOT1wPP58'
HELP = '''
*Техническое:*
/start – начать сначала.
/help – отобразить справку.
/botver – версия бота и список изменений.
/menu – отобразить все команды кнопками.\n
*Развлечения:*
/repeat – повторять за тобой.
/rps – поиграть со мной в "Камень, ножницы, бумагу".
/fish – создать текст-рыбу.\n
*Информация*
/date – узнать дату и время.
/course – узнать курс валют.\n
*Fera Antitilt:*
/game – выбрать игру.
/teams – определить, кто с кем играет.
/killer – выбрать убийцу для DBD.
/brawl – случайный пик для BS.
/league – напомнить Солику о клубной лиге.'''
current_bot_version = 'v0\.5'
START = f'Привет! Я бот Фера, и вот что я умею:\n{HELP}'
link = '[здесь](https://www\.pythonanywhere\.com/user/magistar2280/shares/723b78b6749b4c48bafb99f68bd2b9be)'
NEW_VERSION = f'Бот обновлён до версии *{current_bot_version}*\!\nСмотри список изменений {link}\.'
bot = telebot.TeleBot(token)
months = dict(zip(range(1, 13), ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']))
names_feraantitilt_members = dict(zip(['Фера', "Маг", "Соля", "Петя"], ['Ферой', "Магом", "Солей", "Петей"]))
weekdays = {
    0: 'понедельник',
    1: 'вторник',
    2: 'среда',
    3: 'четверг',
    4: 'пятница',
    5: 'субббота',
    6: 'воскресенье',
}
minutes_endings = {
    0: 'минут',
    1: 'минуту',
    2: 'минуты'
}
seconds_endings = {
    0: 'секунд',
    1: 'секунду',
    2: 'секунды'
}
ids = {
    848383407: 'Солик',
    1351555452: 'Фера',
    1327237491: 'Петя'
}


# vars
repeat_status = False
buttons_was_active = False
rps_is_active = False
last_timing = {}


def get_moscow_time() -> datetime:
    delta = datetime.timedelta(hours=3, minutes=0)
    return datetime.datetime.now(datetime.timezone.utc) + delta, (datetime.datetime.now(datetime.timezone.utc) + delta).weekday()

nowt, nowm = get_moscow_time()
print(f'{nowt.hour}:{nowt.minute} Бот запущен.')

def choose_players():
    players = ['Петя', 'Фера', 'Маг', 'Соля']
    player1 = random.choice(players)
    del players[players.index(player1)]
    if player1 == 'Маг' or player1 == 'Петя':
        player2 = random.choice(['Фера', 'Соля'])
    elif player1 == 'Фера' or player1 == 'Соля':
        player2 = random.choice(['Маг', 'Петя'])
    del players[players.index(player2)]
    team1, team2 = [player1, player2], players
    return team1, team2

def similar_symbols(s):
    st = []
    for i in range(0,len(s)):
        if s[i] != s[i-1]:
            st.append(s[i])
    return "".join(st)

def rps_from_buttons(message):
    global rps_is_active
    user_input = message.text.lower()
    paper = 'бумага'
    if user_input in ["камень", paper, "ножницы"]:
        user_action = str(user_input)
        computer_action = random.choice(["камень", paper, "ножницы"])
        if user_action == computer_action:
            result = 'У нас ничья!'
            if user_action == paper:
                computer_action = 'бумагу'
            bot.send_message(message.chat.id, f'Мы оба выбрали {computer_action}!\n{result}')
        else:
            if user_action == "камень":
                if computer_action == "ножницы":
                    result = 'Ты выиграл меня.'
                else:
                    computer_action = 'бумагу'
                    result ="Я выиграл!"
            elif user_action == "бумага":
                user_action = 'бумагу'
                if computer_action == "камень":
                    result = 'Ты выиграл меня.'
                else:
                    result ="Я выиграл!"
            elif user_action == "ножницы":
                if computer_action == "бумага":
                    result = 'Ты выиграл меня.'
                    computer_action = 'бумагу'
                else:
                    result ="Я выиграл!"
            bot.send_message(message.chat.id, f'Ты выбрал {user_action}, а я {computer_action}.\n{result}')


# commands

@bot.message_handler(commands=["announceupdate"])
def announce_update(message):
    announcers = [268039219, 848383407, 1351555452, 1327237491]
    for id in announcers:
        bot.send_message(id, NEW_VERSION, parse_mode='MarkdownV2', disable_web_page_preview = True)


@bot.message_handler(commands=["start"])
def start(message):
    global repeat_status
    global buttons_was_active
    repeat_status = False
    buttons_was_active = False
    bot.send_message(message.chat.id, START, parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(commands=["league"])
def league_solix(message):
    global last_timing
    global now_timing
    global repeat_status
    if repeat_status:
        bot.send_message(message.chat.id, '/league')
    else:
        if message.chat.id == 848383407:
            bot.send_message(message.chat.id, 'Ты шо дурак, сам себе напоминаешь?')
        else:
            now_timing = time.perf_counter()
            if message.chat.id not in last_timing:
                last_timing[message.chat.id] = 0
            if now_timing - last_timing[message.chat.id] < 600:
                left_timing = 600 - int(now_timing - last_timing[message.chat.id])
                mins = left_timing // 60
                secs = left_timing % 60
                if 10 <= mins <= 19:
                    mins = f'{mins} {minutes_endings[0]}'
                elif mins == 0:
                    mins = ''
                elif str(mins)[-1] in ['2', '3', '4']:
                    mins = f'{mins} {minutes_endings[2]}'
                elif str(mins)[-1] == '1':
                    mins = f'{mins} {minutes_endings[1]}'
                else:
                    mins = f'{mins} {minutes_endings[0]}'
                if 10 <= secs <= 19:
                    secs = f' {secs} {seconds_endings[0]}'
                elif str(secs)[-1] in ['2', '3', '4']:
                    secs = f' {secs} {seconds_endings[2]}'
                elif str(secs)[-1] == '1':
                    secs = f' {secs} {seconds_endings[1]}'
                elif secs == 0:
                    secs = ''
                else:
                    secs = f' {secs} {seconds_endings[0]}'
                bot.send_message(message.chat.id, f'Напоминать можно не чаще, чем раз в 10 минут.\nТы сможешь ещё раз напомнить Солику о клубной лиге только через {mins}{secs}.')
            else:
                bot.send_message(message.chat.id, 'Хорошо! Уже напоминаю Солику о клубной лиге!')
                bot.send_message(848383407, 'Солик! По просьбе кого-то из людей, Фера напоминает тебе, что надо сыграть в клубную лигу! Не забудь, что ты должен зайти и позвать кого-то к себе в команду. Ты можешь сделать это в чате в Бравле, а если там все оффлайн, то в дискорд-сервере. Старайся играть раньше, чтобы было с кем сыграть.')
                last_timing[message.chat.id] = time.perf_counter()

@bot.message_handler(commands=["botver"])
def botver(message):
    global repeat_status
    global current_bot_version
    if repeat_status:
        bot.send_message(message.chat.id, '/botver')
    else:
        link = '[здесь](https://www\.pythonanywhere\.com/user/magistar2280/shares/723b78b6749b4c48bafb99f68bd2b9be)'
        bot.send_message(message.chat.id, f'Текущая версия бота: *{current_bot_version}*\nСписок изменений можно посмотреть {link}\.', parse_mode='MarkdownV2', disable_web_page_preview = True)

@bot.message_handler(commands=["brawl"])
def brawl(message):
    global repeat_status
    if repeat_status:
        bot.send_message(message.chat.id, '/brawl')
    else:
        list_brawlers = 'Шелли Нита Кольт Булл Джесси Брок Динамайк Бо Тик 8-бит Эмз Сту Эль-Примо Барли Поко Роза Рико Дэррил Пенни Карл Джеки Пайпер Пэм Фрэнк Биби Беа Нани Эдгар Грифф Гром Мортис Тара Джин Макс Спраут Байрон Скуик Ворон Леон Амбер Мэг Спайк Сэнди Гэйл Вольт Колетт Лу Белль Базз Эш Лола Фэнг Ева'.split() + ['Мистер П.', 'Генерал Гавс']
        picked_brawlers = random.sample(list_brawlers, 3)
        bot.send_message(message.chat.id, f'Вот вам пик для победы в Brawl Stars: {picked_brawlers[0]}, {picked_brawlers[1]} и {picked_brawlers[2]}.\nСамый лучший!'.replace('..', '.'))

@bot.message_handler(commands=["killer"])
def killer(message):
    global repeat_status
    global ids
    player = None
    if repeat_status:
        bot.send_message(message.chat.id, '/killer')
    else:
        if message.chat.id in ids:
            player = ids[message.chat.id]
        else:
            player == None
        if message.chat.id == 848383407:
            killer = random.choice(['Свинья', 'Доктор', 'Палач', 'Легион', 'Немезис', 'Охотник', 'Призрак', 'Медсестра', 'Деревенщина', 'Охотница'])
        elif message.chat.id == 1351555452:
            killer = random.choice(['Охотник', 'Призрак', 'Медсестра', 'Деревенщина', 'Тень', 'Каннибал', 'Гоуст Фейс', 'Дух', 'Немезис', 'Охотница'])
        elif message.chat.id == 1327237491:
            killer = random.choice(["охотник", "охотница", "призрак", "деревенщина", "медсестра", "ведьма", "дух", "легион", "чума", "они", "палач", "мор", "художница"]).capitalize()
        else:
            killer = None
        if killer == None:
            bot.send_message(message.chat.id, 'Я тебя не знаю, напиши моему создателю.')
        else:
            bot.send_message(message.chat.id, f'Так, а ты у нас, значит, {player}, да?\nЧто ж, сегодня твой убийца – {killer}.')

@bot.message_handler(commands=["teams"])
def teams(message):
    global repeat_status
    if repeat_status:
        bot.send_message(message.chat.id, '/teams')
    else:
        team1, team2 = choose_players()
        msg_text = f'{team1[0]} играет с {names_feraantitilt_members[team1[1]]}.\n{team2[0]} играет с {names_feraantitilt_members[team2[1]]}.'
        bot.send_message(message.chat.id, msg_text)

@bot.message_handler(commands=["game"])
def game(message):
    global repeat_status
    if repeat_status:
        bot.send_message(message.chat.id, '/game')
    else:
        game_choice = 'Сегодня команда Fera Antitilt играет в ' + random.choice(['дбд', 'сидж', 'кс', 'таблетоп', 'фолл гайз', 'паммел пати']) + '. Так Фера сказал!'
        bot.send_message(message.chat.id, game_choice)

@bot.message_handler(commands=["fish"])
def fish(message):
    global repeat_status
    if repeat_status:
        bot.send_message(message.chat.id, '/fish')
    else:
        random_number = random.randint(10, 99)
        mes = message.text.split()
        if len(mes) >= 2:
            temp = mes[1]
            for i in '.,?/\\':
                if i in temp:
                    temp = temp.replace(i, '')
            mes = int(temp)
            if not isinstance(mes, int):
                bot.send_message(message.chat.id, f'Введи команду с длиной текста (количеством слов).\nНапример: /fish {random_number}')
            else:
                first_reply = requests.get('https://raw.githubusercontent.com/danakt/russian-words/master/russian.txt')
                second_reply = requests.get('https://raw.githubusercontent.com/danakt/russian-words/master/russian_surnames.txt')
                russian_words = first_reply.content.decode('cp1251')
                russian_surnames = second_reply.content.decode('cp1251')
                list_words = russian_words.splitlines()
                list_surnames = russian_surnames.splitlines()
                list_all = list_words + list_surnames
                mesg_text = random.choice(list_all)
                for i in range(mes-1):
                    temp_int = random.randint(0, len(list_all))
                    mesg_text = (mesg_text + ' ' + list_all[temp_int])
                mesg_text += '.'
                mesg_text = mesg_text[:1].upper() + mesg_text[1:]
                bot.send_message(message.chat.id, mesg_text)
        else:
            bot.send_message(message.chat.id, f'Введи команду с длиной текста (количеством слов).\nНапример: /fish {random_number}')

@bot.message_handler(commands=["help"])
def help(message):
    global repeat_status
    if repeat_status:
        bot.send_message(message.chat.id, '/help')
    else:
        bot.send_message(message.chat.id, HELP, parse_mode='Markdown')

@bot.message_handler(commands=["rps"])
def rps(message):
    global repeat_status
    global rps_is_on
    global buttons_was_active
    global rps_is_active
    tag = False
    if repeat_status:
        bot.send_message(message.chat.id, '/rps')
    else:
        user_input = message.text.lower().split()
        paper = 'бумага'
        if message.text == '/rps':
            bot.send_message(message.chat.id, 'Напиши команду и затем свой выбор:\n/rps камень, /rps ножницы или /rps бумага.')
        else:
            if not user_input == ['/rps']:
                if user_input[1] in ["камень", paper, "ножницы"]:
                    user_action = str(user_input[1])
                    computer_action = random.choice(["камень", paper, "ножницы"])
                    if user_action == computer_action:
                        result = 'У нас ничья!'
                        if user_action == paper:
                            computer_action = 'бумагу'
                        bot.send_message(message.chat.id, f'Мы оба выбрали {computer_action}!\n{result}')
                    else:
                        if user_action == "камень":
                            if computer_action == "ножницы":
                                result = 'Ты выиграл меня.'
                            else:
                                computer_action = 'бумагу'
                                result ="Я выиграл!"
                        elif user_action == "бумага":
                            user_action = 'бумагу'
                            if computer_action == "камень":
                                result = 'Ты выиграл меня.'
                            else:
                                result ="Я выиграл!"
                        elif user_action == "ножницы":
                            if computer_action == "бумага":
                                result = 'Ты выиграл меня.'
                                computer_action = 'бумагу'
                            else:
                                result ="Я выиграл!"
                        bot.send_message(message.chat.id, f'Ты выбрал {user_action}, а я {computer_action}.\n{result}')
                else: tag = True
            if tag:
                if buttons_was_active:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = ["Камень", "Ножницы", "Бумага"]
                    item2 = ["Назад к развлечениям"]
                    markup.add(*item1).add(*item2)
                    bot.send_message(message.chat.id,'Выбери своё действие.\nТакже ты можешь написать команду /rps, и затем свой выбор:\n/rps камень, /rps ножницы или /rps бумага.',reply_markup=markup)
                    rps_is_active = True
                else: bot.send_message(message.chat.id, 'Напиши команду и затем свой выбор:\n/rps камень, /rps ножницы или /rps бумага.')

@bot.message_handler(commands=["menu"])
def button(message):
    global repeat_status
    global buttons_was_active
    if repeat_status:
        bot.send_message(message.chat.id, '/menu')
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        row1 = ["Техническое", "Развлечения"]
        row2 = ["Информация", "Fera Antitilt"]
        row3 = ['Скрыть кнопки']
        markup.add(*row1).add(*row2).add(*row3)
        bot.send_message(message.chat.id,'Меню открыто.',reply_markup=markup)
        buttons_was_active = True

@bot.message_handler(commands=["button-clear"])
def button_clear(message):
    global buttons_was_active
    buttons_was_active = False
    bot.send_message(message.chat.id, "Кнопки скрыты.\nЧтобы снова показать кнопки, напиши /menu.", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')


@bot.message_handler(commands=["course"])
def course(message):
    global repeat_status
    if repeat_status:
        bot.send_message(message.chat.id, '/course')
    else:
        course_data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        usd_course = course_data['Valute']['USD']['Value']
        eur_course = course_data['Valute']['EUR']['Value']
        bot.send_message(message.chat.id, f'Курс валют сегодня:\n1 USD = {usd_course} RUB.\n1 EUR = {eur_course} RUB.')

@bot.message_handler(commands=["repeat"])
def repeat(message):
    global repeat_status
    global buttons_was_active
    rs_2 = repeat_status
    if isinstance(message.text, str) and message.text == "/repeat" and buttons_was_active:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Прекратить повторять")
        markup.add(item1)
        bot.send_message(message.chat.id,'Теперь я буду за тобой повторять! Если хочешь, чтобы я перестал это делать, напиши /stop',reply_markup=markup)
    if rs_2:
        bot.send_message(message.chat.id, 'Я уже повторяю за тобой! Если хочешь, чтобы я перестал это делать, напиши /stop')
    else:
        if not buttons_was_active:
            bot.send_message(message.chat.id,'Теперь я буду за тобой повторять! Если хочешь, чтобы я перестал это делать, напиши /stop')
        repeat_status = True

@bot.message_handler(commands=["stop"])
def repeat_process(message):
    global repeat_status
    global buttons_was_active
    rs_2 = repeat_status
    if not rs_2:
        bot.send_message(message.chat.id, 'Ты что, я ещё не повторюшка! Если хочешь, чтобы я за тобой повторял, напиши /repeat')
    else:
        bot.send_message(message.chat.id, 'Ладно! Больше не буду за тобой повторять! Если хочешь, чтобы я снова за тобой повторял, напиши /repeat')
        repeat_status = False
        if buttons_was_active:
            button(message)

@bot.message_handler(commands=["date"])
def date(message):
    global repeat_status
    if repeat_status:
        bot.send_message(message.chat.id,'/date')
    else:
        now, weekday = get_moscow_time()
        if len(str(now.hour)) == 1:
            hour = '0' + str(now.hour)
        else:
            hour = now.hour
        if len(str(now.minute)) == 1:
            minute = '0' + str(now.minute)
        else:
            minute = now.minute
        bot.send_message(message.chat.id, f'Конечно! Фера всегда подскажет дату и время!\nСегодня {weekdays[weekday]}, {now.day} {months[now.month]} {now.year} года.\nСейчас в Москве {hour}:{minute}.')


# bot_functions
@bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"])
def echo(message):
    global buttons_was_active
    global rps_is_active
    naxui = False
    if isinstance(message.text, str) and not repeat_status:
        technical_row1 = ["Начать сначала", "Список команд"]
        technical_row2 = ['Версия бота и список изменений', 'Назад']
        fun_row1 = ['"Камень, ножницы, бумага"', 'Текст-рыба']
        fun_row2 = ["\"Повторюшка\"", 'Назад']
        info_row1 = ["Дата и время", "Курс валют"]
        info_row2 = ['Назад']
        feraantitilt_row1 = ["Выбрать игру", 'Определить команды']
        feraantitilt_row2 = ['Напомнить Солику о клубной лиге', 'Пик для Brawl Stars']
        feraantitilt_row3 = ['Выбрать убийцу', 'Назад']
        if message.text == "Техническое":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(*technical_row1).add(*technical_row2)
            bot.send_message(message.chat.id,'Меню "Техническое" открыто.',reply_markup=markup)
            buttons_was_active = True
        elif message.text == "Развлечения" or message.text == 'Назад к развлечениям':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(*fun_row1).add(*fun_row2)
            bot.send_message(message.chat.id,'Меню "Развлечения" открыто.',reply_markup=markup)
            buttons_was_active = True
            rps_is_active = False
        elif message.text == "Информация":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(*info_row1).add(*info_row2)
            bot.send_message(message.chat.id,'Меню "Информация" открыто.',reply_markup=markup)
            buttons_was_active = True
        elif message.text == "Fera Antitilt":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(*feraantitilt_row1).add(*feraantitilt_row2).add(*feraantitilt_row3)
            bot.send_message(message.chat.id,'Меню "Fera Antitilt" открыто.',reply_markup=markup)
            buttons_was_active = True
        elif message.text == "Назад":
            button(message)
        elif message.text == 'Текст-рыба':
            fish(message)
        elif message.text == "Курс валют":
            course(message)
        elif message.text == "Начать сначала":
            start(message)
        elif message.text == "Версия бота и список изменений":
            botver(message)
        elif message.text == "Скрыть кнопки":
            button_clear(message)
        elif message.text == "Дата и время":
            date(message)
        elif message.text == "Определить команды":
            teams(message)
        elif message.text == 'Выбрать убийцу':
            killer(message)
        elif message.text == 'Пик для Brawl Stars':
            brawl(message)
        elif message.text == '"Камень, ножницы, бумага"':
            buttons_was_active = True
            rps(message)
        elif message.text == "Напомнить Солику о клубной лиге":
            league_solix(message)
        elif (message.text == 'Камень' or message.text == 'Ножницы' or message.text == 'Бумага') and rps_is_active:
            rps_from_buttons(message)
        elif message.text == "\"Повторюшка\"":
            buttons_was_active = True
            repeat(message)
            bot.send_message(message.chat.id, "Перехожу в режим повторюшки...", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Прекратить повторять")
            markup.add(item1)
            bot.send_message(message.chat.id,'Теперь я буду за тобой повторять! Если хочешь, чтобы я перестал это делать, напиши /stop',reply_markup=markup)
        elif message.text == "Список команд":
            help(message)
        elif message.text == "Выбрать игру":
            game(message)
        else:
            message_for_checking = similar_symbols(message.text)
            if 'фера' in message_for_checking.lower():
                bot.send_message(message.chat.id, 'Ты написал моё имя! Да, я глазастый!')
            elif 'привет' in message_for_checking.lower():
                bot.send_message(message.chat.id, random.choice(['Привет.', 'И тебе привет.', 'Здарова.', 'ку']))
            else:
                for one in ["пошёл", "пошел", "иди", 'пашол', "пашел", "пашёл", "poshel", 'idi', 'pashol', 'пшел', 'пшол', 'пшёл', 'pschel', 'pschol', 'pshol', 'poshol']:
                    for two in ["нахуй", "на хуй", "в пизду", 'впизду', 'нах', 'nahui', 'nah', 'v pizdu', 'vpizdu', 'нахрен', 'на хрен', 'na hren', 'na hui', 'nahren', 'нахер', 'на хер', 'na her', 'naher', 'в жопу', 'вжопу', 'v zhopu', 'vzhopu']:
                        for three in ['', ' ', ' ты ', '-ка ты ', ' ка ты ', ' блять ']:
                            if one + three + two in message_for_checking.lower().strip() or two + three + one in message_for_checking.lower().strip():
                                bot.send_message(message.chat.id, random.choice(['Нет, я не буду этого делать.', "Взаимно.", "ок", "Кто обзывается – тот сам так и называется!"]))
                                naxui = True
                                nowt, nowm = get_moscow_time()
                                print(f'{nowt.hour}:{nowt.minute} Я ответил как надо на:', message.text)
                                break
                        if naxui: break
                    if naxui: break
                if not naxui:
                    nowt, nowm = get_moscow_time()
                    print(f'{nowt.hour}:{nowt.minute} Unknown:', message.text)
                    bot.send_message(message.chat.id, 'К сожалению, я ещё слишком молод и мало чему научен, поэтому не могу понять это сообщение :(\nЧтобы узнать то, что я умею, напиши /help\nА если ты слишком недоволен, что я не умею то, что ты хочешь, то напиши моему создателю!')
    elif isinstance(message.text, str) and repeat_status and message.text == "Прекратить повторять":
        repeat_process(message)
    else:
        if repeat_status:
            if isinstance(message.text, str):
                if 'фера' in message.text.lower():
                    bot.send_message(message.chat.id, 'Ты написал моё имя! Да, я глазастый!')
                else:
                    bot.send_message(message.chat.id, message.text)
            else:
                bot.send_message(message.chat.id, 'Прости, но я пока что не умею присылать такое с моей стороны :(')
        else:
            bot.send_message(message.chat.id, 'К сожалению, я ещё слишком молод и мало чему научен, поэтому не могу понять это сообщение :(\nЧтобы узнать то, что я умею, напиши /help\nА если ты слишком недоволен, что я не умею то, что ты хочешь, то напиши моему создателю!')

while True:
    try:
        bot.polling()
    except Exception as e:
        print(e)
        nowt, nowm = get_moscow_time()
        print(f'{nowt.hour}:{nowt.minute} Бот перезапущен из-за ошибки.')
        continue
