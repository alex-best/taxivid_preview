from aiogram.dispatcher.filters.state import StatesGroup, State


class TripCreation(StatesGroup):
    point_of_departure = State()
    destination_point = State()
