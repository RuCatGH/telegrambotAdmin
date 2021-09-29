import logging
import config
from aiogram import Bot, Dispatcher, executor, types
from filters import IsAdminFilter

API_TOKEN = config.TOKEN

#log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

# activate filters
dp.filters_factory.bind(IsAdminFilter)

# ban command (admins only!)
@dp.message_handler(is_admin=True, commands=["ban"], commands_prefix="!/")
async def cmd_ban(message: types.Message):
  if not message.reply_to_message:
    await message.reply("Эта команда должна быть ответом на сообщение!")
    return

  await message.bot.delete_message(chat_id=config.GROUP_ID, message_id=message.message_id)
  await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.reply_to_message.from_user.id)

  await message.reply_to_message.reply("Этот пользователь забанен!!!")


# delete message new chat member
@dp.message_handler(content_types=["new_chat_member"])
async def delete_message (message:types.Message):
    await message.delete()

# delete message with words плохое слово
@dp.message_handler()
async def filter_messages (message: types.Message):
    if "плохое слово" in message.text:
        await message.delete()

# start polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
