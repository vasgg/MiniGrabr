from aiogram.filters.callback_data import CallbackData

from bot.internal.enums import Crud, MenuButton, OrderAction, UserType


class MenuButtonsCallbackFactory(CallbackData, prefix="menu"):
    button: MenuButton
    user_type: UserType | None = None


class CrudCallbackFactory(CallbackData, prefix="crud"):
    user_type: UserType
    action: Crud
    entity_id: int


class UserTypeCallbackFactory(CallbackData, prefix="user_type"):
    user_type: UserType


class OrderInfoCallbackFactory(CallbackData, prefix="order_info"):
    user_type: UserType
    order_id: int


class OrderActionCallbackFactory(CallbackData, prefix="order_action"):
    action: OrderAction
    order_id: int


class SendMessageCallbackFactory(CallbackData, prefix="send_message"):
    user_type: UserType
    application_id: int
