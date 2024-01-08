import os
import random

from bd import answer_links, article_links

from datetime import date
from dotenv import load_dotenv
from telegram import ParseMode, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


load_dotenv()
secret_token = os.getenv('TOKEN_RCK')

updater = Updater(token=secret_token)


def wake_up(update, context):
    """Функция именного приветствия при старте бота"""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Cколько дней до волшебства']],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Дорогой друг {name}! Тебя приветствует бережливый бот РЦК Удмуртии!',
        reply_markup=button,
        )


def days_from():
    """Функция расчета кол-ва дней до нового года"""
    new_year = date(2024, 1, 1)
    today = date.today()
    days_from = new_year-today
    return days_from


def until_new_year(update, context):
    """Функция отправки кол-ва дней до НГ """
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Новогодние задачки', 'Лучшие статьи уходящего года']],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Не грусти, {name}! До Нового 2024 года осталось всего то меньше {days_from().days} дней ...',
        reply_markup=button
        )


def new_article(update, context):
    """Функция отправки ссылки на статью """
    article = random.choice(article_links)
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Новогодние задачки', 'Cколько дней до волшебства'],
        ['Лучшие статьи уходящего года', 'Как вступить в Нац проект']],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{name}, держи ссылку на отличную статью - {article}',
        parse_mode=ParseMode.HTML,
        reply_markup=button
        )


def answer(update, context):
    """Функция ответа задачкой на текстовое сообщение или при нажатии кнопки <задачка> """
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Новогодние задачки', 'Cколько дней до волшебства'],
        ['Лучшие статьи уходящего года', 'Как вступить в Нац проект']],
        resize_keyboard=True)
    answer = random.choice(answer_links)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{name}, {answer}',
        reply_markup=button,
        )


def nazproect(update, context):
    """Функция отправки контакта РЦК для консультации по Нац проекту"""
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['Новогодние задачки', 'Cколько дней до волшебства'],
        ['Лучшие статьи уходящего года', 'Как вступить в Нац проект']],
        resize_keyboard=True)
    telefon = '+7 (3412) 78-50-90'
    Email = 'rck@umcluster.ru'
    context.bot.send_message(
        chat_id=chat.id,
        text=f'{name}, позвони в офис РЦК Удмуртии по номеру {telefon} или напиши по адресу: {Email}',
        reply_markup=button,
        )


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text('Cколько дней до волшебства'), until_new_year))
updater.dispatcher.add_handler(MessageHandler(Filters.text('Как вступить в Нац проект'), nazproect))
updater.dispatcher.add_handler(MessageHandler(Filters.text('Новогодние задачки'), answer))
updater.dispatcher.add_handler(MessageHandler(Filters.text('Лучшие статьи уходящего года'), new_article))
updater.dispatcher.add_handler(MessageHandler(Filters.text, answer))

updater.start_polling(poll_interval=3.00)
updater.idle()
