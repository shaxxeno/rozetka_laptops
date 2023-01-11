import logging
from aiogram import Bot, Dispatcher, executor, types
from asyncscraping import get_products
from aiofiles import os

from config import BOT_API


def post_to_telegram():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_API)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['get_file'])
    async def get_file(message: types.Message):
        await bot.send_message(message.from_user.id, f'Готую чоколад...(Мирного рішення не буде)')
        file = await get_products(
            'https://rozetka.com.ua/notebooks/c80004/goods_with_promotions=promotion/')
        await bot.send_document(document=open(file, 'rb'), chat_id=message.chat.id)
        await os.remove(file)

    executor.start_polling(dp, skip_updates=True)


def main():
    post_to_telegram()


if __name__ == '__main__':
    main()
