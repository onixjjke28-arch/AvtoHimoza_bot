import os
import telebot
from flask import Flask, request

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Простейшее расписание
free_days = ["9 сентября (вторник)", "11 сентября (четверг)", "13 сентября (суббота)"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для записи на автохимчистку.\nНапиши: Когда свободные дни?")

@bot.message_handler(func=lambda msg: msg.text.lower() == "когда свободные дни?")
def show_days(message):
    text = "Свободные дни:\n" + "\n".join(free_days)
    bot.reply_to(message, text)

@bot.message_handler(func=lambda msg: msg.text in free_days)
def book_day(message):
    day = message.text
    if day in free_days:
        free_days.remove(day)
        bot.reply_to(message, f"Вы записаны на {day} ✅")
        bot.send_message(123456789, f"Клиент записался на {day}")  # замени на свой chat_id

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.stream.read().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://YOUR-APP-NAME.onrender.com/' + TOKEN)
    return "Hello!", 200
