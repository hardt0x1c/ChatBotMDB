import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from config import bot_token, own_chat_id, admin, company_name
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Text
import keyboards as kb
import messages as msg
import db_handlers as db


logging.basicConfig(level=logging.INFO)
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher()


class States(StatesGroup):
    get_idea = State()
    get_problem = State()
    admin_spam = State()


@dp.message(Command('start'))
async def start(message: types.Message):
    user = db.get_user(db.cursor, message.from_user.id)
    if message.from_user.id == admin:
        start_photo = FSInputFile("addons/photos/start.jpg")
        await message.answer_photo(start_photo, caption=msg.greet)
        await message.answer(msg.help, reply_markup=kb.admin_menu)
    else:
        if user is None:
            db.add_user(db.conn, db.cursor, message.from_user.id)
            start_photo = FSInputFile("addons/photos/start.jpg")
            await message.answer_photo(start_photo, caption=msg.greet)
            await message.answer(msg.help, reply_markup=kb.menu)


@dp.message(Text('Админ-панель'))
async def admin_panel(message: types.Message):
    if message.from_user.id == admin:
        await message.answer('Выберите действие:', reply_markup=kb.admin_panel)
    else:
        await message.answer('У вас недостаточно прав.', reply_markup=kb.back_menu)


@dp.message(Text('Рассылка'))
async def send_spam(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        await state.set_state(States.admin_spam)
        await message.answer('Текст будет отправлен всем пользователям бота.', reply_markup=ReplyKeyboardRemove())
        await message.answer('Напиши текст рассылки', reply_markup=kb.back_menu_inline)
    else:
        await message.answer('У вас недостаточно прав.', reply_markup=kb.back_menu)


@dp.message(States.admin_spam)
async def start_spam(message: types.Message, state: FSMContext):
    message_for_spam = message.text
    users = db.get_users(db.cursor)
    counter = 0
    for i in range(len(users)):
        await bot.send_message(users[i][0], message_for_spam)
        counter += 1
    await message.answer(f'Рассылка завершена. Количество адресатов: {counter}', reply_markup=kb.back_menu)
    await state.clear()


@dp.message(Text('Статистика'))
async def send_stats(message: types.Message):
    if message.from_user.id == admin:
        count = len(db.get_users(db.cursor))
        await message.answer(f'Количество подписчиков: {count}', reply_markup=kb.back_menu)
    else:
        await message.answer('У вас недостаточно прав.', reply_markup=kb.back_menu)


@dp.message(Command('about'))
@dp.message(Text(f'Узнать больше о бренде {company_name}'))
async def about_company(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(msg.about_company, reply_markup=kb.back_menu)


@dp.message(Command('site'))
@dp.message(Text(f'Посмотреть сайт {company_name}'))
async def send_site(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(msg.site, reply_markup=kb.back_menu)


@dp.message(Command('idea'))
@dp.message(Text('Предложить идею улучшения продукта'))
async def send_idea(message: types.Message, state: FSMContext):
    await state.set_state(States.get_idea)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(msg.send_idea, reply_markup=kb.ReplyKeyboardRemove())
    await message.answer('Либо вернуться в главное меню', reply_markup=kb.back_menu_inline)


@dp.message(States.get_idea)
async def save_idea(message: types.Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    user_message = message.text
    await bot.send_message(chat_id=own_chat_id, text=f"Идея по улучшению продукта от пользователя:\n\n"
                                                              f"Имя: {first_name}\n"
                                                              f"Фамилия: {last_name}\n"
                                                              f"Username: {username}\n"
                                                              f"ID: {user_id}\n"
                                                              f"Сообщение: {user_message}")
    await state.clear()
    await message.answer('Сообщение успешно отправлено. Спасибо за обратную связь!', reply_markup=kb.back_menu)


@dp.message(Command('new_products'))
@dp.message(Text('Принять участие в создании новых продуктов'))
async def send_poll(message: types.Message):
    options = [
        'Крем для лица',
        'Крем для рук',
        'Тушь для ресниц',
        'Мицелярная вода',
        'Сыворотка для роста ресниц',
        'Сыворотка для роста волос',
        'Шампунь для роста волос'
    ]
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer_poll(msg.send_poll, options, is_anonymous=False)


@dp.message(Command('promocode'))
@dp.message(Text('Получить промокод на скидку в Ozon'))
async def send_code(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(msg.promocode, reply_markup=kb.back_menu)


@dp.message(Command('help_service'))
@dp.message(Text('Обратиться в "Службу заботы" с проблемой'))
async def get_help(message: types.Message, state: FSMContext):
    await state.set_state(States.get_problem)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(msg.get_help, reply_markup=kb.help_menu)
    await message.answer('Или можете вернуться в главное меню.', reply_markup=kb.back_menu_inline)


@dp.message(States.get_problem)
async def save_problem(message: types.Message, state: FSMContext):
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username
    user_message = message.text
    await bot.send_message(chat_id=own_chat_id, text=f"Проблема от пользователя:\n\n"
                                                     f"Имя: {first_name}\n"
                                                     f"Фамилия: {last_name}\n"
                                                     f"Username: {username}\n"
                                                     f"ID: {user_id}\n"
                                                     f"Сообщение: {user_message}")
    await state.clear()
    await message.answer(f'Ваше обращение зарегистрировано и передано в отдел качества {company_name}', reply_markup=kb.back_menu_inline)


@dp.message(Text('Вернуться в главное меню.'))
async def back_menu(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        await state.clear()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await message.answer('Главное меню:', reply_markup=kb.admin_menu)
    else:
        await state.clear()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await message.answer('Главное меню:', reply_markup=kb.menu)


@dp.callback_query(Text('back_menu_inline'))
async def back_menu_inline(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == admin:
        await state.clear()
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await callback.message.answer('Главное меню:', reply_markup=kb.admin_menu)
    else:
        await state.clear()
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await callback.message.answer('Главное меню:', reply_markup=kb.menu)


async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())