from telebot import *

def make_menu_keyboard(role_id: int) -> telebot.types.ReplyKeyboardMarkup:
    if role_id == 1:
        return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(
            telebot.types.KeyboardButton("Просмотр личной статистики"),
            telebot.types.KeyboardButton("Прохождение опроса"))

    elif role_id == 2:
        return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(
            telebot.types.KeyboardButton("Просмотр личной статистики"),
            telebot.types.KeyboardButton("Прохождение опроса"),
            telebot.types.KeyboardButton("Посмотреть созданные опросы"),
            telebot.types.KeyboardButton("Создать опрос"))

    elif role_id == 3:
        return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(
            telebot.types.KeyboardButton("Просмотр личной статистики"),
            telebot.types.KeyboardButton("Прохождение опроса"),
            telebot.types.KeyboardButton("Посмотреть созданные опросы"),
            telebot.types.KeyboardButton("Создать опрос"),
            telebot.types.KeyboardButton("Посмотреть общую статистику"),
            telebot.types.KeyboardButton("Квешн-мейкеры"),
            telebot.types.KeyboardButton("Удалить опрос"))

    elif role_id == 4:
        return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(
            telebot.types.KeyboardButton("Просмотр личной статистики"),
            telebot.types.KeyboardButton("Прохождение опроса"),
            telebot.types.KeyboardButton("Просмотреть созданные опросы"),
            telebot.types.KeyboardButton("Создать опрос"),
            telebot.types.KeyboardButton("Просмотреть общую статистику"),
            telebot.types.KeyboardButton("Персонал"),
            telebot.types.KeyboardButton("Удалить опрос"))
