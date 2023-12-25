from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup)

rp_button = [
    [KeyboardButton(text="Ovqat qo'shish"),
     KeyboardButton(text="Ovqatlarni ko'rish")
     ],
]
main_rp = ReplyKeyboardMarkup(keyboard=rp_button, resize_keyboard=True)
