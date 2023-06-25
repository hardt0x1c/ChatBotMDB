from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from config import admin
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from loader import dp, bot, db
from States.Admin import Admin
import keyboards.admin.admin_keyboard as kb_admin
import keyboards.user.user_keyboard as kb_user


@dp.message(Text('Админ-панель'))
async def admin_panel(message: types.Message):
    if message.from_user.id == admin:
        await message.answer('Выберите действие:', reply_markup=kb_admin.admin_panel)
    else:
        await message.answer('У вас недостаточно прав.', reply_markup=kb_user.back_menu)


@dp.message(Text('Рассылка'))
async def send_spam(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        await state.set_state(Admin.admin_spam)
        await message.answer('Текст будет отправлен всем пользователям бота.', reply_markup=ReplyKeyboardRemove())
        await message.answer('Напиши текст рассылки', reply_markup=kb_user.back_menu_inline)
    else:
        await message.answer('У вас недостаточно прав.', reply_markup=kb_user.back_menu)


@dp.message(Admin.admin_spam)
async def start_spam(message: types.Message, state: FSMContext):
    message_for_spam = message.text
    users = db.get_users()
    counter = 0
    for i in range(len(users)):
        await bot.send_message(users[i][0], message_for_spam)
        counter += 1
    await message.answer(f'Рассылка завершена. Количество адресатов: {counter}', reply_markup=kb_user.back_menu)
    await state.clear()


@dp.message(Text('Статистика'))
async def send_stats(message: types.Message):
    if message.from_user.id == admin:
        count = len(db.get_users())
        await message.answer(f'Количество подписчиков: {count}', reply_markup=kb_user.back_menu)
    else:
        await message.answer('У вас недостаточно прав.', reply_markup=kb_user.back_menu)
