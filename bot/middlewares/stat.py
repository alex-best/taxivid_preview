from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types

from loader import settings
from loader import amplitude_session as session


class StatMiddleware(BaseMiddleware):

    async def on_post_process_message(self, message: types.Message, results, data: dict):
        if command := data.get('command'):
            event_type = f'command_{command.command}'
            request_data = {
                'api_key': settings.amplitude_key,
                'events': [
                    {
                        'user_id': message.from_user.id,
                        'event_properties': {
                            'product': 'taxivid'
                        },
                        'event_type': event_type,
                        'user_propertixes': {
                            'first_name': message.from_user.first_name,
                            'last_name': message.from_user.last_name,
                            'username': message.from_user.username,
                            'locale': message.from_user.language_code
                        }
                    }
                ]
            }
            await session.post(settings.amplitude_url, json=request_data)

    async def on_post_process_callback_query(self, callback_query, results, data: dict):
        action_type = callback_query.data.split('_')[0]
        event_type = f'inline_button_{action_type}'
        request_data = {
            'api_key': settings.amplitude_key,
            'events': [
                {
                    'user_id': callback_query.from_user.id,
                    'event_properties': {
                        'product': 'taxivid'
                    },
                    'event_type': event_type,
                    'user_propertixes': {
                        'first_name': callback_query.from_user.first_name,
                        'last_name': callback_query.from_user.last_name,
                        'username': callback_query.from_user.username,
                        'locale': callback_query.from_user.language_code
                    }
                }
            ]
        }
        await session.post(settings.amplitude_url, json=request_data)
