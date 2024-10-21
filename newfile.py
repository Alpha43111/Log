import os
import telebot
import random
import requests
import time
import json
import re
import math
from random import choice
from time import sleep
from json import loads
from re import findall
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from requests import get, post

API_TOKEN = '7963919324:AAHuSL1llZgAxjHGF5Ni_EsxZTWB0XMEslg' 

bot = telebot.TeleBot(API_TOKEN)


user_log_count = {}
MAX_DAILY_LOGS = 5  
VIP_USER_IDS = [7487633134,2065085129,]

LOG_FILE_PATH = '/storage/emulated/0/logv32.txt'
MAX_LINES = 100

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    user_id = str(message.from_user.id)  
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Dost Kanal", url="https://t.me/swethotmail")
    button2 = types.InlineKeyboardButton("Kanal", url="https://t.me/K4xbinx")
    button3 = types.InlineKeyboardButton("Beni Gruba veya Bir Kanala Ekle", url="https://t.me/Alphaloggbot?startgroup=new")
    markup.add(button1, button2, button3)
    user = message.chat
    user_info = bot.get_chat(user.id)    
    first_name = message.from_user.first_name
    username = message.from_user.username 
    user_id = message.from_user.id 
    bio = user_info.bio
    bot.reply_to(message,f'''Merhaba ben bir log botuyum\nLog çekmek için /logyardim komutuna bak\nBilgi
İsim : {first_name}
Kullanıcı Adı : @{username}
ID : {user_id}
Biyografi : {bio}''', reply_markup=markup)

@bot.message_handler(commands=['logyardim'])
def logyardim(message):
    bot.send_message(message.chat.id, '''İstediğiniz siteden log çekmek için /log komutunu kullanın Örnek :/log netflix.com''')

@bot.message_handler(commands=['log'])
def logg(message):
    try:
        user_id = message.from_user.id

        
        if user_id not in VIP_USER_IDS:
            
            if user_id not in user_log_count:
                user_log_count[user_id] = 0  

            if user_log_count[user_id] >= MAX_DAILY_LOGS:
                bot.reply_to(message, "Günlük log çekme hakkınızı doldurdunuz. Yarın tekrar deneyin.")
                return
            else:
                user_log_count[user_id] += 1

        command_data = message.text.split()

        if len(command_data) < 2:
            bot.reply_to(message, "Lütfen bir site adı girin. Örnek: /log netflix.com")
            return

        site_name = command_data[1]

        with open(LOG_FILE_PATH, 'r') as file:
            lines = file.readlines()

        matching_lines = [line.strip() for line in lines if site_name in line]

        if not matching_lines:
            bot.reply_to(message, f"'{site_name}' içeren hiçbir kayıt bulunamadı.")
            return

        num_lines = len(matching_lines)
        if num_lines >= MAX_LINES:
            selected_line_count = MAX_LINES
        else:
            selected_line_count = math.ceil(num_lines * 0.4)

        selected_lines = random.sample(matching_lines, selected_line_count)
        output_file_path = f"{site_name}_logs.txt"

        with open(output_file_path, 'w') as output_file:
            output_file.write("\n".join(selected_lines))

        with open(output_file_path, 'rb') as file_to_send:
            bot.send_document(message.chat.id, file_to_send)

        os.remove(output_file_path)

    except FileNotFoundError:
        bot.reply_to(message, "Log dosyası bulunamadı.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {e}")

bot.polling()
