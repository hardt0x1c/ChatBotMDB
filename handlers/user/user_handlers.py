from aiogram import types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from config import own_chat_id, admin, company_name
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
import keyboards.user.user_keyboard as kb_user
import keyboards.admin.admin_keyboard as kb_admin
import text.messages as msg
from loader import dp, db, bot
from States.User import User


@dp.message(Command('start'))
async def start(message: types.Message):
    user = db.get_user(message.from_user.id)
    if message.from_user.id == admin:
        start_photo = FSInputFile("addons/photos/start.jpg")
        await message.answer_photo(start_photo, caption=msg.greet)
        await message.answer(msg.help, reply_markup=kb_admin.admin_menu)
    else:
        if user is None:
            db.add_user(message.from_user.id)
            start_photo = FSInputFile("addons/photos/start.jpg")
            await message.answer_photo(start_photo, caption=msg.greet)
            await message.answer(msg.help, reply_markup=kb_user.menu)
        else:
            start_photo = FSInputFile("addons/photos/start.jpg")
            await message.answer_photo(start_photo, caption=msg.greet)
            await message.answer(msg.help, reply_markup=kb_user.menu)


@dp.message(Command('about'))
@dp.message(Text(f'Узнать больше о бренде {company_name}'))
async def about_company(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(msg.about_company, reply_markup=kb_user.back_menu)


@dp.message(Command('site'))
@dp.message(Text(f'Посмотреть сайт {company_name}'))
async def send_site(message: types.Message):
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(msg.site, reply_markup=kb_user.back_menu)


@dp.message(Command('idea'))
@dp.message(Text('Предложить идею улучшения продукта'))
async def send_idea(message: types.Message, state: FSMContext):
    await state.set_state(User.get_idea)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(msg.send_idea, reply_markup=ReplyKeyboardRemove())
    await message.answer('Либо вернуться в главное меню', reply_markup=kb_user.back_menu_inline)


@dp.message(User.get_idea)
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
    await message.answer('Сообщение успешно отправлено. Спасибо за обратную связь!', reply_markup=kb_user.back_menu)


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
    await message.answer(msg.promocode, reply_markup=kb_user.back_menu)


@dp.message(Command('help_service'))
@dp.message(Text('Обратиться в "Службу заботы" с проблемой'))
async def get_help(message: types.Message, state: FSMContext):
    await state.set_state(User.get_problem)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(msg.get_help, reply_markup=kb_user.help_menu)
    await message.answer('Или можете вернуться в главное меню.', reply_markup=kb_user.back_menu_inline)


@dp.message(User.get_problem)
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
    await message.answer(f'Ваше обращение зарегистрировано и передано в отдел качества {company_name}',
                         reply_markup=kb_user.back_menu_inline)


@dp.message(Text('Вернуться в главное меню.'))
async def back_menu(message: types.Message, state: FSMContext):
    if message.from_user.id == admin:
        await state.clear()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await message.answer('Главное меню:', reply_markup=kb_admin.admin_menu)
    else:
        await state.clear()
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await message.answer('Главное меню:', reply_markup=kb_user.menu)


@dp.callback_query(Text('back_menu_inline'))
async def back_menu_inline(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == admin:
        await state.clear()
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await callback.message.answer('Главное меню:', reply_markup=kb_admin.admin_menu)
    else:
        await state.clear()
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id)
        await callback.message.answer('Главное меню:', reply_markup=kb_user.menu)
