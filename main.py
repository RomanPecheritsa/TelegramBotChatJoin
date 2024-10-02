import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import ChatJoinRequest, Message
from aiogram.filters import Command
from aiogram.methods import DeclineChatJoinRequest
from config import Config, load_config


config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

GROUP_ID = -1002284332063
message_text = "Ссылка на канал http://google.com"


async def get_admin_ids():
    chat_members = await bot.get_chat_administrators(GROUP_ID)
    return [member.user.id for member in chat_members]


@dp.chat_join_request()
async def handle_chat_join_request(join_request: ChatJoinRequest):
    user = join_request.from_user
    if user.is_bot:
        await bot(DeclineChatJoinRequest(chat_id=join_request.chat.id, user_id=user.id))
    else:
        await bot.send_message(user.id, message_text)


@dp.message(Command("set_message"))
async def set_message(msg: Message):
    global message_text
    admin_ids = await get_admin_ids()

    if msg.from_user.id in admin_ids:
        if len(msg.text) > len('/set_message '):
            new_message = msg.text[len('/set_message '):]
            message_text = new_message
            await msg.answer("Сообщение успешно обновлено.")
        else:
            await msg.answer("Пожалуйста, введите новый текст после команды.")
    else:
        await msg.answer("У вас нет прав на изменение текста сообщения.")


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
