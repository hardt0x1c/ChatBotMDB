import asyncio


async def main():
    # Запуск бота
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    # Удалишь - будет рак яичек
    print('Бот запущен. Кодер: TG:@hardt0x1c')
    # Импорт хендлеров
    from loader import bot, db
    from handlers import dp
    # Создание БД
    db.create_database()
    # Запуск функции main
    asyncio.run(main())