from aiogram import types, utils
from aiogram.dispatcher import FSMContext
import aiohttp
from aiogram.dispatcher.filters import Text

from loader import dp, settings, messages
from states.trip import TripCreation
from buttons.keyboard import current_location
from buttons.inline import get_trip_card_buttons


@dp.message_handler(content_types=('location', 'venue'), state=TripCreation.point_of_departure)
async def get_point_of_departure(msg: types.Message, state: FSMContext):
    await msg.answer('Отправь точку назначения.', reply_markup=current_location)
    await state.update_data(point_of_departure=msg.location)
    await TripCreation.next()


async def _get_geocode(session, location):
    async with session.get(settings.geocode_url.format(
            longitude=location.longitude,
            latitude=location.latitude
    )) as response:
        response = await response.json()
        return response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']


async def _get_maxim(session, latitude1, longitude1, latitude2, longitude2) -> int:
    url = 'https://cabinet.taximaxim.ru/Services/Public.svc/api/CLAPP_IOS/v1/order/price/calculate'
    json = {
        "route": [
            {
                "location": {
                    "longitude": longitude1,
                    "latitude": latitude1
                }
            },
            {
                "location": {
                    "longitude": longitude2,
                    "latitude": latitude2
                }
            }
        ]
    }
    query = {
        'platform': 'CLAPP_IOS',
        'city': 133,
        'udid': 'bbfaeaae37b9d1094e69dd2d87b1333cb6fae39f'
    }

    async with session.post(url, json=json, params=query) as response:
        response = await response.json()
        return response['Price']


async def _get_yandex(session, latitude1, longitude1, latitude2, longitude2) -> int:
    url = 'https://tc.mobile.yandex.net/3.0/routestats?block_id=default'
    json = {
        "route": [
            [
                longitude1,
                latitude1
            ],
            [
                longitude2,
                latitude2
            ]
        ]
    }
    async with session.post(url, json=json) as response:
        response = await response.json()
        return int(response['service_levels'][0]['price'].replace('руб.', ''))


async def _get_citymobil(session, latitude1, longitude1, latitude2, longitude2) -> int:
    url = 'https://widget.city-mobil.ru/c-api'
    json = {
        "method": "getprice",
        "ver": "4.59.0",
        "phone_os": "widget",
        "os_version": "web mobile-web",
        "latitude": latitude1,
        "longitude": longitude1,
        "del_latitude": latitude2,
        "del_longitude": longitude2,
        "options": [],
        "payment_type": [
            "cash"
        ],
        "tariff_group": [
            2
        ],
        "source": "O",
        "hurry": 1
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://city-mobil.ru',
        'Accept-Language': 'ru',
        'Host': 'widget.city-mobil.ru'
    }
    async with session.post(url, json=json, headers=headers) as response:
        response = await response.json()
        return response['prices'][0]['price']


async def _get_uber(session, latitude1, longitude1, latitude2, longitude2) -> int:
    url = 'https://uc.taxi.yandex.net/3.0/routestats?block_id=default'
    json = {
        'route': [
            [
                longitude1,
                latitude1
            ],
            [
                longitude2,
                latitude2
            ]
        ]
    }
    async with session.post(url, json=json) as response:
        response = await response.json()
        return int(response['service_levels'][0]['price'].replace('руб.', ''))


@dp.message_handler(content_types=('location', 'venue'), state=TripCreation.destination_point)
async def get_destination_point(msg: types.Message, state: FSMContext):
    await types.ChatActions.typing()
    await state.update_data(destination_point=msg.location)
    coordinates = await state.get_data()
    await state.finish()

    async with aiohttp.ClientSession() as session:
        coor = (
            coordinates['point_of_departure'].latitude, coordinates['point_of_departure'].longitude,
            coordinates['destination_point'].latitude, coordinates['destination_point'].longitude,
        )
        point_of_departure = await _get_geocode(session, coordinates['point_of_departure'])
        destination_point = await _get_geocode(session, coordinates['destination_point'])
        maxim = await _get_maxim(session, *coor)
        yandex = await _get_yandex(session, *coor)
        citymobil = await _get_citymobil(session, *coor)
        uber = await _get_uber(session, *coor)

    await msg.answer_photo(
        settings.static_map_url.format(
            longitude1=coordinates['point_of_departure'].longitude,
            latitude1=coordinates['point_of_departure'].latitude,
            longitude2=coordinates['destination_point'].longitude,
            latitude2=coordinates['destination_point'].latitude,
        ),
        messages['trip_card'].format(
            point_of_departure=point_of_departure,
            destination_point=destination_point
        ),
        reply_markup=get_trip_card_buttons(
            maxim=maxim,
            yandex=yandex,
            citymobil=citymobil,
            uber=uber,
            latitude1=coordinates['point_of_departure'].latitude,
            longitude1=coordinates['point_of_departure'].longitude,
            latitude2=coordinates['destination_point'].latitude,
            longitude2=coordinates['destination_point'].longitude
        )
    )


@dp.message_handler(state=(TripCreation.point_of_departure, TripCreation.destination_point))
async def get_destination_point(msg: types.Message):
    await msg.answer('Отправьте геолокацию. Для этого нажми на скрепку в нижнем левом углу и выбери в меню пункт "Геопозиция".')


async def throttled(query, **_):
    await query.answer('Не так быстро 😓', show_alert=True)


@dp.callback_query_handler(Text(startswith='refresh'))
@dp.throttled(throttled, rate=60)
async def refresh_prices(query: types.CallbackQuery):
    _, location1, location2 = query.data.split('_')
    latitude1, longitude1 = tuple(map(float, location1.split(',')))
    latitude2, longitude2 = tuple(map(float, location2.split(',')))

    async with aiohttp.ClientSession() as session:
        maxim = await _get_maxim(session, latitude1, longitude1, latitude2, longitude2)
        yandex = await _get_yandex(session, latitude1, longitude1, latitude2, longitude2)
        citymobil = await _get_citymobil(session, latitude1, longitude1, latitude2, longitude2)
        uber = await _get_uber(session, latitude1, longitude1, latitude2, longitude2)

    try:
        await query.message.edit_reply_markup(get_trip_card_buttons(
                maxim=maxim,
                yandex=yandex,
                citymobil=citymobil,
                uber=uber,
                latitude1=latitude1,
                longitude1=longitude1,
                latitude2=latitude2,
                longitude2=longitude2
            ))
    except utils.exceptions.MessageNotModified:
        await query.answer('Стоимость поездки не изменилась.')
    else:
        await query.answer('Успех!')
