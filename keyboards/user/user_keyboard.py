from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from config import company_name


menu = [
    [KeyboardButton(text=f'Узнать больше о бренде {company_name}', callback_data='about'),
     KeyboardButton(text=f'Посмотреть сайт {company_name}', callback_data='site'),
     KeyboardButton(text='Предложить идею улучшения продукта', callback_data='send_idea')],
    [KeyboardButton(text='Принять участие в создании новых продуктов', callback_data='new_products'),
     KeyboardButton(text='Получить промокод на скидку в Ozon', callback_data='ozon'),
     KeyboardButton(text='Обратиться в "Службу заботы" с проблемой', callback_data='help_service')]
]
menu = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)

back_menu = [
    [KeyboardButton(text='Вернуться в главное меню.')]
]
back_menu = ReplyKeyboardMarkup(keyboard=back_menu, resize_keyboard=True)

back_menu_inline = [
    [InlineKeyboardButton(text='Вернуться в главное меню.', callback_data='back_menu_inline')]
]
back_menu_inline = InlineKeyboardMarkup(inline_keyboard=back_menu_inline)

help_menu = [
    [KeyboardButton(text='Пришел вскрытый товар'),
     KeyboardButton(text='Разбилось масло усьмы')],
    [KeyboardButton(text='Неполный комплект'),
     KeyboardButton(text=f'Не было брендированного скотча {company_name}')],
    [KeyboardButton(text='Другая проблема')]
]
help_menu = ReplyKeyboardMarkup(keyboard=help_menu, resize_keyboard=True)

products = [
    [InlineKeyboardButton(text='Крем для лица', callback_data='face'),
     InlineKeyboardButton(text='Крем для рук', callback_data='hands'),
     InlineKeyboardButton(text='Тушь для ресниц', callback_data='brows')],
    [InlineKeyboardButton(text='Мицелярная вода', callback_data='water'),
     InlineKeyboardButton(text='Сыворотка для роста ресниц', callback_data='brows_up'),
     InlineKeyboardButton(text='Сыворотка для роста волос', callback_data='hair_up')],
    [InlineKeyboardButton(text='Шампунь для роста волос', callback_data='shampoo_hair')]
]
products = InlineKeyboardMarkup(inline_keyboard=products)