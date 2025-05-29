from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.enums import MenuButtons, TravelerAction
from bot.keyboards.callbacks import MenuCallbackFactory, TravelerMenuCallbackFactory


def traveler_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("Create trip", TravelerMenuCallbackFactory(action=TravelerAction.CREATE_TRIP).pack()),
        ("Find orders", TravelerMenuCallbackFactory(action=TravelerAction.FIND_ORDERS).pack()),
        ("My responses", TravelerMenuCallbackFactory(action=TravelerAction.MY_RESPONSES).pack()),
        ("Back to menu", MenuCallbackFactory(action=MenuButtons.BACK).pack()),

    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()
