from django.http import HttpResponse
import telebot
from telebot import types
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import User, Course, Group, Student
from .markups import *
from django.db.models import F

bot = telebot.TeleBot(settings.BOT_TOKEN)
@csrf_exempt
def web_hook_view(request):
    if request.method == 'POST':
        bot.process_new_updates([telebot.types.Update.de_json(request.body.decode('utf-8'))])
    return HttpResponse('ok')


@bot.message_handler(commands=['start'])
def start_message(message):
    try:
        User.objects.get(user_id=message.from_user.id, tg_username=message.from_user.username)
    except Exception as e:
        User.objects.create(user_id=message.from_user.id, tg_username=message.from_user.username)
    courses = Course.objects.all() 
    markups = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    if courses:
        for course in courses:
            markup = KeyboardButton(course.title)
            markups.add(markup)
    text = f'Assalomu aleykum <b>{message.from_user.first_name}</b> \n' \
           'O\'quv markazimizning yordamchi telegram botiga xush kelibsiz!'\
            'Ushbu bot orqali siz kurslarimiz haqida ma\'lumot olishingiz va unga yozilishingiz mumkin\n\n' ,

    msg = bot.send_message(message.from_user.id, text, parse_mode="html", reply_markup=markups)
    bot.register_next_step_handler(msg, groups)

def groups(message):
    coursetitle = message.text
    groups = Group.objects.filter(course_title__title = coursetitle)
    markups = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    try:
        for group in groups:
            markup = KeyboardButton(group.name)
            markups.add(markup)
            msg = bot.send_message(message.from_user.id,"Ushbu yo\'nalishda bizda quyidagi guruhlar mavjud👇:", parse_mode="html", reply_markup=markups)
            bot.register_next_step_handler(msg, group_data)

    except Exception as e:
        print(e)            

def group_data(message):
    groupname = message.text
    text_data = Group.objects.filter(name = groupname).get()
    markups = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m_text =f'<b>Kurs</b>: {text_data.name} \n'\
            f'<b>O\'rganiladigan texnologiyalar</b>: {text_data.technologies}\n'\
            f'<b>O\'qituvchisi</b> {text_data.mentor } \n'\
            f'<b>Vaqti</b>: {text_data.time}\n'\
            f'<b>Kunlari</b>: {text_data.weekdays}\n'\
            f'<b>Narxi</b>: {text_data.price} so\'m'

    try:
        markup = KeyboardButton("Kursga yozilish")
        markups.add(markup)
        msg = bot.send_message(message.from_user.id,m_text, parse_mode="html", reply_markup=markups)
        # bot.register_next_step_handler(msg, groups)
            
    except Exception as e:
        print(e) 

def write_name(message):
    username = message.text
    print(type(username))
    if isinstance(username, str):
        print(message.text)
        try:
            user = User.objects.get(user_id=message.from_user.id)
            Student.objects.create(user=user, name=username)
        except Exception as e:
            print(e)
                

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    if message.text == "Kursga yozilish":
        hideBoard = types.ReplyKeyboardRemove() 
        m_text = "Iltimos <i>Ism Familyangizni</i> quyidagi ko'rinishda kiriting👇: \n\n"\
                    "<b>Aliyev Vali</b>"
        msg = bot.send_message(message.from_user.id,m_text, parse_mode="html", reply_markup=hideBoard)
        bot.register_next_step_handler(msg, write_name)
        


