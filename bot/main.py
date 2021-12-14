from aiogram import types

import loader
from loader import bot, settings


async def on_startup(dp):
    await bot.send_message(settings.admin, '<b>I\'m ready</b>')
    await bot.set_my_commands([
        types.BotCommand(command='trip', description='Новая поездка 🚕'),
        types.BotCommand(command='help', description='Помощь 🆘'),
    ])


async def on_shutdown(dp):
    await bot.send_message(settings.admin, '<b>I will be back</b>')
    await loader.amplitude_session.close()


def main():
    from aiogram import executor

    from handlers import dp
    from middlewares.stat import StatMiddleware

    dp.middleware.setup(StatMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
