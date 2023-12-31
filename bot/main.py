import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import config
from handlers import start, other, question, menu, trainer
from db import database
from api import get_exam_tree


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Создаем меню для бота
async def set_main_menu(bot: Bot):

    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Вернуться в начало'),
        BotCommand(command='/menu',
                   description='Главное меню'),
        BotCommand(command='/reset',
                   description='Сброс данных')]

    await bot.set_my_commands(main_menu_commands)


# Функция конфигурирования и запуска бота
async def main() -> None:

    # Инициализируем бот и диспетчер
    # мы используем HTML, чтобы избежать проблем с экранированием символов
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    # хранилище данных для состояний пользователей
    # все данные бота, которые мы не сохраняем в БД (к примеру состояния), будут стёрты при перезапуске
    dp = Dispatcher(storage=MemoryStorage())

    # Регистриуем роутеры в диспетчере
    dp.include_router(start.router)
    dp.include_router(question.router)
    dp.include_router(menu.router)
    dp.include_router(trainer.router)
    dp.include_router(other.router)

    # Инициируем пункты меню для бота
    dp.startup.register(set_main_menu)

    # Загружаем данные
    exam_tree = get_exam_tree()
    database.set_exam_tree(exam_tree=exam_tree)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
