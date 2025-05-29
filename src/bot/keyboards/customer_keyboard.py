from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.enums import CustomerAction, MenuButtons
from bot.keyboards.callbacks import CustomerMenuCallbackFactory, MenuCallbackFactory


def customer_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("Create order", CustomerMenuCallbackFactory(action=CustomerAction.CREATE_ORDER).pack()),
        ("My orders", CustomerMenuCallbackFactory(action=CustomerAction.MY_ORDERS).pack()),
        ("Find traveler", CustomerMenuCallbackFactory(action=CustomerAction.FIND_TRAVELER).pack()),
        ("Back to menu", MenuCallbackFactory(action=MenuButtons.BACK).pack()),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()
