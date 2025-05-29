from aiogram.filters.callback_data import CallbackData

from bot.internal.enums import CustomerAction, MenuButtons, TravelerAction, UserType


class MenuCallbackFactory(CallbackData, prefix="menu"):
    action: MenuButtons


class UserTypeCallbackFactory(CallbackData, prefix="user_type"):
    user_type: UserType


class CustomerMenuCallbackFactory(CallbackData, prefix="customer_menu"):
    action: CustomerAction


class TravelerMenuCallbackFactory(CallbackData, prefix="traveler_menu"):
    action: TravelerAction
