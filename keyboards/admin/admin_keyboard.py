from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from config import company_name


admin_menu = [
    [KeyboardButton(text=f'Узнать больше о бренде {company_name}', callback_data='about'),
     KeyboardButton(text=f'Посмотреть сайт {company_name}', callback_data='site'),
     KeyboardButton(text='Предложить идею улучшения продукта', callback_data='send_idea')],
    [KeyboardButton(text='Принять участие в создании новых продуктов', callback_data='new_products'),
     KeyboardButton(text='Получить промокод на скидку в Ozon', callback_data='ozon'),
     KeyboardButton(text='Обратиться в "Службу заботы" с проблемой', callback_data='help_service')],
    [KeyboardButton(text='Админ-панель')]
]
admin_menu = ReplyKeyboardMarkup(keyboard=admin_menu, resize_keyboard=True)

admin_panel = [
    [KeyboardButton(text='Рассылка'),
     KeyboardButton(text='Статистика')],
    [KeyboardButton(text='Вернуться в главное меню.')]
]
admin_panel = ReplyKeyboardMarkup(keyboard=admin_panel, resize_keyboard=True)