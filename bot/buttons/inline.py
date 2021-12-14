from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from furl import furl

from loader import settings


def _get_yandex_url(latitude1, longitude1, latitude2, longitude2) -> str:
    url = furl('https://3.redirect.appmetrica.yandex.com/route?level=50&ref=yoursiteru&appmetrica_tracking_id=1178268795219780156')
    url.args['start-lat'] = latitude1
    url.args['start-lon'] = longitude1
    url.args['end-lat'] = latitude2
    url.args['end-lon'] = longitude2
    return url.url


def _get_maxim_url(latitude1, longitude1, latitude2, longitude2) -> str:
    url = furl(f'{settings.redirect_url}/maxim/')
    url.args['start-lat'] = latitude1
    url.args['start-lon'] = longitude1
    url.args['end-lat'] = latitude2
    url.args['end-lon'] = longitude2
    return url.url


def _get_citymobil_url(latitude1, longitude1, latitude2, longitude2) -> str:
    url = furl(f'{settings.redirect_url}/citymobil/')
    url.args['start-lat'] = latitude1
    url.args['start-lon'] = longitude1
    url.args['end-lat'] = latitude2
    url.args['end-lon'] = longitude2
    return url.url


def get_trip_card_buttons(
        maxim: int,
        yandex: int,
        citymobil: int,
        uber: int,
        latitude1,
        longitude1,
        latitude2,
        longitude2
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f'Яндекс GO {yandex} ₽', url=_get_yandex_url(latitude1, longitude1, latitude2, longitude2))
        ],
        [
            InlineKeyboardButton(text=f'Uber {uber} ₽', url=settings.uber_redirect_url)
        ],
        [
            InlineKeyboardButton(text=f'Ситимобил {citymobil} ₽', url=_get_citymobil_url(latitude1, longitude1, latitude2, longitude2))
        ],
        [
            InlineKeyboardButton(text=f'Maxim {maxim} ₽', url=_get_maxim_url(latitude1, longitude1, latitude2, longitude2))
        ],
        [
            InlineKeyboardButton(
                text='🔄 Обновить цены',
                callback_data=f'refresh_{latitude1},{longitude1}_{latitude2},{longitude2}'
            )
        ],
    ])
