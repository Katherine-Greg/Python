import telebot
from telebot import types 


bot = telebot.TeleBot('2010721761:AAGdOL8FicLqL9Q5Yqi_SvebxkKu4Wr05ec')

STATUS = 0

back_to_name = types.InlineKeyboardMarkup()
back_to_name.add(types.InlineKeyboardButton(text = 'Назад', callback_data = 'back_to_name'))

back_to_age = types.InlineKeyboardMarkup()
back_to_age.add(types.InlineKeyboardButton(text = 'Назад', callback_data = 'back_to_age'))

back_to_sex = types.InlineKeyboardMarkup()
back_to_sex.add(types.InlineKeyboardButton(text = 'Назад', callback_data = 'back_to_sex'))

back_to_menu = types.InlineKeyboardMarkup()
back_to_menu.add(types.InlineKeyboardButton(text = 'Назад', callback_data = 'back_to_menu'))

user = {}
userdata = {}

def check_age(a):
    try:
        int(a)
    except:
        return False
    return int(a) > 0


@bot.message_handler(commands = ['start'])
def start_command(msg):
    bot.send_message(msg.from_user.id, "Имя?")
    bot.register_next_step_handler(msg, get_name)

def get_name(msg):
    userdata.clear()
    if(len(msg.text) >= 2 and len(msg.text) <= 20):
        userdata['name'] = msg.text
        bot.send_message(msg.from_user.id, "Возраст?", reply_markup =  back_to_name)
        bot.register_next_step_handler(msg, get_age)   
    else:
        bot.send_message(msg.chat.id, "Введите имя заново", reply_markup = back_to_name) 
        bot.register_next_step_handler(msg, get_name)

def get_age(msg):
    if(check_age(msg.from_user)):
        userdata['age'] = msg.text
        bot.send_message(msg.from_user.id, "Пол?", reply_markup = back_to_age)
        bot.register_next_step_handler(msg, get_sex)
    else:
        bot.send_message(msg.from_user.id, "Введите возраст заново", reply_markup = back_to_name)
        bot.register_next_step_handler(msg, get_age)

def get_sex(msg):
    if(msg.text.replace(' ', '').lower() in set(['м', 'ж'])):    
        userdata['sex'] = msg.text.replace(' ', '').lower()
        user[msg.chat.id] = userdata
        bot.send_message(msg.from_user.id, "Выберите пункт меню: ?", reply_markup = back_to_sex)
        bot.register_next_step_handler(msg, menu)
        print(user)
    else:
        bot.send_message(msg.from_user.id, "Введите пол заново", reply_markup = back_to_age)
        bot.register_next_step_handler(msg, get_sex)

def menu(msg):
    menu = types.InlineKeyboardMarkup()
    info = types.InlineKeyboardButton(text = 'Ваша информация', callback_data = 'info')
    settings = types.InlineKeyboardButton(text = 'Настройки', callback_data = 'settings')
    end = types.InlineKeyboardButton(text='Exit', callback_data='exit')
    menu.add(settings, info, end)
    while STATUS != 1:
        bot.send_message(msg.from_user.id, "\nChoose a punkt: ", reply_markup = back_to_sex, reply_markup = info, reply_markup = settings, reply_markup = end)
        if STATUS == 7:
            bot.register_next_step_handler(msg, get_info)
        elif STATUS == 6:
            bot.register_next_step_handler(msg, get_settings)
    

def get_settings(msg):
    bot.send_message(msg.from_user.id, "Choose thing to change: ", reply_markup = back_to_name, reply_markup = back_to_age, reply_markup = back_to_sex, reply_markup = back_to_menu)

def get_info(msg):
    bot.send_message("\nИмя: ", userdata['name'], "\n", userdata['age'], "\n", userdata['sex'], reply_markup = back_to_menu)

@bot.callback_query_handler(func = lambda call: True)
def process_callback_button(call, STATUS):
    if call.data == 'back_to_name': 
        start_command(call)
        return STATUS == 0
    elif call.data == 'back_to_age':
        get_age(call)
        return STATUS == 0
    elif call.data == 'back_to_sex':
        get_sex(call)
        return STATUS == 0
    elif call.data == 'back_to_menu':
        menu(call)
        return STATUS == 0 
    elif call.data == 'info':
        return STATUS == 7
    elif call.data == 'settings':
        return STATUS == 6
    elif call.data == 'exit':
        return STATUS == 1



bot.polling()    