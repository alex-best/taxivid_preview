from aiogram import types
from aiogram.dispatcher import FSMContext
import aiohttp

from loader import dp, settings
from buttons.keyboard import current_location
from states.trip import TripCreation


@dp.message_handler(commands=['start'], state='*')
async def start_command(msg: types.Message, state: FSMContext):
    await types.ChatActions.typing(2)

    if not await state.get_state():
        await state.finish()

    await msg.answer('Привет! Давай не будем лишний раз тратить время, чтобы сравнить цены на такси нажми на /trip.')

    async with aiohttp.ClientSession() as session:
        request_data = {
            'id': msg.from_user.id,
            'username': msg.from_user.username,
            'first_name': msg.from_user.first_name,
            'last_name': msg.from_user.last_name
        }
        await session.post(f'{settings.api_url}/api/v1/telegram_user/', json=request_data)


@dp.message_handler(commands=['help'], state='*')
async def help_command(msg: types.Message, state: FSMContext):
    await types.ChatActions.typing(2)

    if not await state.get_state():
        await state.finish()

    await msg.answer("""/trip — создание новой поездки. Нажми на это команду, чтобы сравнить такси.""")


@dp.message_handler(commands=['trip'], state='*')
async def trip_command(msg: types.Message, state: FSMContext):
    await types.ChatActions.typing(2)

    if not await state.get_state():
        await state.finish()

    await msg.answer("""Отправь точку отправления. Для этого нажми на скрепку в нижнем левом углу и выбери в меню пункт "Геопозиция".""", reply_markup=current_location)
    await TripCreation.first()
