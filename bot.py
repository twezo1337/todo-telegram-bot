import telebot
import json
from telebot import types
import setting
import datetime
from datetime import timedelta
import weather as wt
import scrapping as sc
import music as ms

bot = telebot.TeleBot(setting.TOKEN) #Создаем бота

current_status = 'wait_hello'

name = ''
age = 0
date = ''
task = ''
W_CITY = 'Красноярск'

help = '''Наш бот умеет:
/help - справочник по командам бота
/todo - добавить задачу
/show - показать задачу
/showall - посмотреть все задачи
/clear - удалить все задачи
/clear-date - удалить задачи на дату
/clear-task - удалить задачу
/get-weather - показать погоду
/generator - рандомные цитаты или мемы
'''

todos = {}

def read_data():
    global todos
    f = open('data.json', 'r', encoding='utf-8')
    todos = json.load(f)
    f.close()

def save_data():
    f = open('data.json', 'w', encoding='utf-8')
    json.dump(todos, f, ensure_ascii=False)
    f.close()

def add_tasks(date, task, id):
    if id in todos:
        usertask = todos[id]
        if date in usertask:
            usertask[date].append(task)
        else:
            usertask[date] = []
            usertask[date].append(task)
    else:
        usertask = {}
        usertask[date] = [task]
        todos[id] = usertask

    save_data()

def show_date(id, date):
    msg = ''
    if id in todos:
        usertasks = todos[id]
        if date in usertasks:
            msg += f'Задачи на {date}:\n' + '\n'.join(todos[id][date])
        else:
            msg += 'Задач на эту дату нет!'
    else:
        msg += 'У вас нет задач!'

    return msg

def get_main_menu(buttons):
    btns = []
    for button in buttons:
        btns.append(telebot.types.KeyboardButton(f'{button}'))
    
    keyboard = telebot.types.ReplyKeyboardMarkup()
    if len(btns) == 10:
        keyboard = telebot.types.ReplyKeyboardMarkup().row(btns[0], btns[1]).row(btns[2], btns[3]).row(btns[4], btns[5]).row(btns[6], btns[7]).add(btns[8]).add(btns[9])
    else:
        for btn in btns:
            keyboard.add(btn)
    
    return keyboard

def get_inline_buttons(buttons):
    btns = []
    for button in buttons:
        btns.append(telebot.types.InlineKeyboardButton(f'{button}', callback_data=f'{button}'))
        
    keyboard = telebot.types.InlineKeyboardMarkup()
    for btn in btns:
        keyboard.add(btn)

    return keyboard

def clear_tusk_ondate(id, date):
    global todos
    del todos[id][date]
    save_data()

def clear_tusk(id, date, task):
    global todos
    todos_temp = todos[id][date]
    todos_temp.remove(task)
    todos[id][date] = todos_temp
    save_data()

read_data()

@bot.message_handler(regexp='Рандомный трек')
@bot.message_handler(commands=['rand-music'])
def random_track_handler(message):
    '''
    music_name = ms.get_random_music()
    music = open(f'{music_name}.mp3', 'rb')
    bot.send_audio(message.chat.id, music)
    music.close()
    '''
    bot.send_message(message.chat.id, 'https://www.youtube.com/watch?v=18dvncX80h8')

@bot.message_handler(regexp='Генератор')
@bot.message_handler(commands=['generator'])
def generator_handler(message):
    inline_buttons = ['Мем', 'Анекдот', 'Цитата']
    bot.send_message(message.chat.id, 'Выбрать:', reply_markup=get_inline_buttons(inline_buttons))

@bot.message_handler(regexp='Погода')
@bot.message_handler(commands=['get-weather']) #/Погода Москва
def get_weather_handler(message):
    global W_CITY
    date_command = message.text.split(maxsplit = 1)
    W_CITY = date_command[1]

    inline_buttons = ['На сегодня', 'На завтра', 'На 5 дней']
    bot.send_message(message.chat.id, 'Введите дату задачи', reply_markup=get_inline_buttons(inline_buttons))

@bot.message_handler(commands=['start'])
def start_handler(message):
    keyboard_buttons = ['📝 Добавить_задачу', '🗑 Удалить_задачи_на_дату', '📅 Показать_на_дату',
                        '🗑 Удалить_все_задачи', '🗂 Показать_задачи', '🗑 Удалить_задачу', 'Погода',
                        'Генератор', 'Рандомный трек', '📖 Помощь']

    bot.send_message(message.chat.id, 'Привет!', reply_markup=get_main_menu(keyboard_buttons))

@bot.message_handler(regexp='Показать_задачи')
@bot.message_handler(commands=['showall'])
def show_handler(message):
    id = str(message.chat.id)
    msg = 'Все ваши задачи\n'

    if id in todos:
        usertasks = todos[id]
        for date in usertasks:
            msg += f'\n{date}:\n' 
            for tasks in usertasks[date]:
                msg += f'{tasks}\n'
    else:
        msg += 'У вас нет задач!'

    bot.send_message(message.chat.id, msg)

@bot.message_handler(regexp='Показать_на_дату')
@bot.message_handler(commands=['show']) #/show 10.10.2023
def show_handler(message):
    global current_status
    date_command = message.text.split(maxsplit = 1)

    if len(date_command) == 2:
        id = str(message.chat.id)
        date = date_command[1]
        msg = show_date(id, date)
        bot.send_message(message.chat.id, msg)
    else:
        id = str(message.chat.id)
        inline_buttons = []
        if id in todos:
            for date in todos[id]:
                inline_buttons.append(date)
        
        bot.send_message(message.chat.id, 'Введите дату, для просмотра задач', reply_markup=get_inline_buttons(inline_buttons))
        current_status = 'wait_date_task'

@bot.message_handler(regexp='Удалить_задачи_на_дату')
@bot.message_handler(commands=['clear_date']) #/show 10.10.2023
def show_handler(message):
    global current_status
    date_command = message.text.split(maxsplit = 1)

    if len(date_command) == 2:
        id = str(message.chat.id)
        date = date_command[1]

        clear_tusk_ondate(id, date)

        bot.send_message(message.chat.id, 'Дата успешно удалена!')
    else:
        id = str(message.chat.id)
        btns = []
        i = 1
        if id in todos:
            for date in todos[id]:
                btns.append(telebot.types.InlineKeyboardButton(f'{i}.{date}', callback_data=f'{i}.{date}'))
                i += 1

        keyboard = telebot.types.InlineKeyboardMarkup()
        for btn in btns:
            keyboard.add(btn)

        bot.send_message(message.chat.id, 'Введите дату, для удаления', reply_markup=keyboard)
        current_status = 'wait_date_for_delete'

@bot.message_handler(commands=['cleartusk']) #/show 10.10.2023
def show_handler(message):
    global current_status
    date_command = message.text.split(maxsplit = 2)
    
    if len(date_command) == 3:
        date = date_command[1]
        task = date_command[2]
        id = str(message.chat.id)
        clear_tusk(id, date, task)
        msg = f'Задача {task} на {date} успешно удалена!'
    else:
        id = str(message.chat.id)
        btns = []
        i = 1
        if id in todos:
            for date in todos[id]:
                btns.append(telebot.types.InlineKeyboardButton(f'{i}-{date}', callback_data=f'{i}-{date}'))
                i += 1

        keyboard = telebot.types.InlineKeyboardMarkup()
        for btn in btns:
            keyboard.add(btn)

        bot.send_message(message.chat.id, 'Введите дату', reply_markup=keyboard)
        current_status = 'wait_date_for_tusk'

@bot.message_handler(regexp='Добавить_задачу')
@bot.message_handler(commands=['todo']) #/todo 6.10.2023 Купить еды
def todo_handler(message):
    global current_status
    todo_command = message.text.split(maxsplit = 2)

    if len(todo_command) == 3:
        date = todo_command[1]
        task = todo_command[2]
        id = str(message.chat.id)
    
        add_tasks(date, task, id)

        msg = f'Задача "{task}" успешно добавлена на {date}'
        bot.send_message(message.chat.id, msg)
    else:
        inline_buttons = ['Сегодня', 'Завтра', 'Послезавтра']
        bot.send_message(message.chat.id, 'Введите дату задачи', reply_markup=get_inline_buttons(inline_buttons))
        current_status = 'wait_date'

@bot.message_handler(commands=['help']) 
def help_handler(message):
    btns = ['hello', 'HELLO']
    bot.send_message(message.chat.id, help, reply_markup=get_main_menu(btns))

@bot.message_handler(content_types=['text']) #декоратор
def echo_message(message):
    global current_status, name, age, date, task

    if current_status == 'wait_hello':
        bot.send_message(message.chat.id, 'Привет! А как тебя зовут?')
        current_status = 'wait_name'
    elif current_status == 'wait_name':
        name = message.text
        bot.send_message(message.chat.id, f'Здравствуй, {name}! А сколько тебе лет?')
        current_status = 'wait_age'
    elif current_status == 'wait_age':
        age = int(message.text)
        bot.send_message(message.chat.id, f'Тебе {age} {name}, а мне 99 лет')
        current_status = 'wait_hello'
    elif current_status == 'wait_date':
        date = message.text
        bot.send_message(message.chat.id, 'Введите задачу')
        current_status = 'wait_task'
    elif current_status == 'wait_task':
        task = message.text 
        add_tasks(date, task, str(message.chat.id))
        bot.send_message(message.chat.id, f'Задача {task} успешно добавлена на {date}!')
    elif current_status == 'wait_date_task':
        id = str(message.chat.id)
        msg = show_date(id, message.text)
        bot.send_message(message.chat.id, msg)
    elif current_status == 'wait_date_for_delete':
        id = str(message.chat.id)
        date = message.text
        clear_tusk_ondate(id, date)
        bot.send_message(message.chat.id, 'Дата успешно удалена!')
    elif current_status == 'wait_date_for_tusk':
        date = message.text
        current_status = 'wait_tusk_for_tusk'
    elif current_status == 'wait_tusk_for_tusk':
        id = str(message.chat.id)
        bot.send_message(message.chat.id, 'успешно!')
    
@bot.callback_query_handler(func=lambda call: call.data == 'Мем')
@bot.callback_query_handler(func=lambda call: call.data == 'Анекдот')
@bot.callback_query_handler(func=lambda call: call.data == 'Цитата')
def get_forecast(call):
    if call.data == 'Мем':
        bot.send_photo(call.message.chat.id, sc.get_random_meme())
    elif call.data == 'Анектод':
        bot.send_message(call.message.chat.id, sc.get_random_anekdot())
    elif call.data == 'Цитата':
        bot.send_message(call.message.chat.id, sc.get_random_quote())

@bot.callback_query_handler(func=lambda call: call.data == 'На сегодня')
@bot.callback_query_handler(func=lambda call: call.data == 'На завтра')
@bot.callback_query_handler(func=lambda call: call.data == 'На 5 дней')
def get_forecast(call):
    if call.data == 'На сегодня':
        bot.send_message(call.message.chat.id, wt.get_forecast_for_day(W_CITY, 'Сегодня'))
    elif call.data == 'На завтра':
        bot.send_message(call.message.chat.id, wt.get_forecast_for_day(W_CITY, 'Завтра'))
    elif call.data == 'На 5 дней':
        bot.send_message(call.message.chat.id, wt.get_5days_weather(W_CITY))


@bot.callback_query_handler(func=lambda call: True)
def date_buttons_handler(call):
    global date, current_status, task

    if call.data == 'Сегодня':
        date = datetime.datetime.now().strftime('%d.%m.%Y') 
        bot.send_message(call.message.chat.id, 'Напишите задачу')
        current_status = 'wait_task'
    elif call.data == 'Завтра':
        date = datetime.datetime.now() + timedelta(days=1)
        date = date.strftime('%d.%m.%Y')
        bot.send_message(call.message.chat.id, 'Напишите задачу')
        current_status = 'wait_task'
    elif call.data == 'Послезавтра':
        date = datetime.datetime.now() + timedelta(days=2)
        date = date.strftime('%d.%m.%Y')
        bot.send_message(call.message.chat.id, 'Напишите задачу')
        current_status = 'wait_task'
    else:
        id = str(call.message.chat.id)
        i = 1
        date_for_delete = ''

        if id in todos:
            for datee in todos[id]:
                if call.data == datee:
                    msg = show_date(id, call.data)
                    bot.send_message(call.message.chat.id, msg)
                if call.data == f'{i}.{datee}':
                    date_for_delete = datee
                if call.data == f'{i}-{datee}':
                    date = datee
                    btns = []

                    if id in todos:
                        if date in todos[id]:
                            for tusk in todos[id][date]:
                                btns.append(telebot.types.InlineKeyboardButton(f'{tusk}', callback_data=f'{tusk}'))

                    keyboard = telebot.types.InlineKeyboardMarkup()
                    for btn in btns:
                        keyboard.add(btn)
                    bot.send_message(call.message.chat.id, 'Введите задачу', reply_markup=keyboard)

                    current_status = 'wait_tusk_for_tusk'
                    
                i += 1

            if date_for_delete != '':
                clear_tusk_ondate(id, date_for_delete)
                bot.send_message(call.message.chat.id, 'Дата успешно удалена!')

        if id in todos:
            if date in todos[id]:
                for tusk in todos[id][date]:
                    if call.data == tusk:
                        task = tusk
                        clear_tusk(str(call.message.chat.id), date, task)
                        bot.send_message(call.message.chat.id, 'Задача успешно удалена!')
        

bot.polling(non_stop=True)

