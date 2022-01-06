from aiogram import executor
from aiogram import types


from misc import dp, bot
import handlers
import asyncio
import keyboards

async def set_commands(dispatcher):
    commands = [
        types.BotCommand(command="start", description="Старт")
    ]
    await bot.set_my_commands(commands)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=set_commands)