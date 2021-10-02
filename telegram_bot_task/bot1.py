import telebot
from telebot import types 

bot = telebot.TeleBot('2010721761:AAGdOL8FicLqL9Q5Yqi_SvebxkKu4Wr05ec')

user = {}
userdata = {}

menu = types.InlineKeyboardMarkup()
info = types.InlineKeyboardButton(text = 'Ваша информация', callback_data = 'info')
settings = types.InlineKeyboardButton(text = 'Настройки', callback_data = 'settings')
menu.add(settings, info)

back_to_name = types.InlineKeyboardMarkup()
back_to_name.add(types.InlineKeyboardButton(text = 'Назад', callback_data = 'back_to_name'))

back_to_age = types.InlineKeyboardMarkup()
back_to_age.add(types.InlineKeyboardButton(text = 'Назад', callback_data = 'back_to_age'))

back_to_menu = types.InlineKeyboardMarkup()
back_to_menu.add(types.InlineKeyboardButton(text = 'Назад', callback_data = 'back_to_menu'))


def check_age(a):
    try:
        int(a)
    except:
        return False
    return int(a) >= 0

@bot.message_handler(commands=['start'])
def start_command(msg):
    bot.send_message(msg.chat.id, "Имя?")
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
    if(check_age(msg.text)):
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
        bot.send_message(msg.from_user.id, "Выберите пункт меню: ?", reply_markup=menu)
        bot.register_next_step_handler(msg, get_menu)
        print(user)
    else:
        bot.send_message(msg.from_user.id, "Введите пол заново", reply_markup = back_to_age)
        bot.register_next_step_handler(msg, get_sex)

def get_menu(msg):
    bot.send_message(msg.from_user.id, "MENU", reply_markup = menu)

def get_settings(msg):
    choose = types.InlineKeyboardMarkup()
    name = types.InlineKeyboardButton(text = 'name', callback_data = 'back_to_name')
    age = types.InlineKeyboardButton(text = 'age', callback_data = 'back_to_age')
    sex = types.InlineKeyboardButton(text = 'sex', callback_data = 'back_to_sex')
    choose.add(name, age, sex, back_to_menu)
    bot.send_message(msg.from_user.id, "Choose thing to change: ", reply_markup = choose)

def get_info(msg):
    bot.send_message(msg.from_user.id, "\nИмя: " + userdata.get(msg.from_user.id)['name'] + "\n" + userdata.get(msg.from_user.id)['age'] + "\n" + userdata.get(msg.from_user.id)['sex'], reply_markup = back_to_menu)


@bot.callback_query_handler(func = lambda call: True)
def callback_handler(call):
    if call.data == 'back_to_age':
        bot.register_next_step_handler(call.message, get_age)
    elif call.data == 'back_to_name':
        bot.register_next_step_handler(call.message, start_command)
    elif call.data == 'back_to_menu':
        bot.register_next_step_handler(call.message, get_menu)
    elif call.data == 'back_to_sex':
        bot.register_next_step_handler(call.message, get_sex)
    elif call.data == 'settings':
        get_settings(call)
    elif call.data == 'info':
        get_info(call)



bot.polling(none_stop=True, interval=0)