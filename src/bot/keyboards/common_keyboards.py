
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.enums import UserType
from bot.keyboards.callbacks import UserTypeCallbackFactory


def role_selector_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("I am a customer", UserTypeCallbackFactory(user_type=UserType.CUSTOMER).pack()),
        ("I am a traveler", UserTypeCallbackFactory(user_type=UserType.TRAVELER).pack()),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()
