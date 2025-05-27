from typing import Literal

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.internal.enums import Crud, MenuButton, OrderAction, UserType
from bot.keyboards.callbacks import CrudCallbackFactory, MenuButtonsCallbackFactory, OrderActionCallbackFactory, \
    OrderInfoCallbackFactory, \
    SendMessageCallbackFactory, UserTypeCallbackFactory
from database.models import Order, User


def role_selector_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for text, callback in [
        ("I am a customer", UserTypeCallbackFactory(user_type=UserType.CUSTOMER).pack()),
        ("I am a traveler", UserTypeCallbackFactory(user_type=UserType.TRAVELER).pack()),
    ]:
        kb.button(text=text, callback_data=callback)
    kb.adjust(1)
    return kb.as_markup()


def get_orders_kb(
    orders: list[Order],
    mode: UserType,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for order in sorted(orders, key=lambda x: x.id, reverse=True):
        match mode:
            case UserType.CUSTOMER:
                kb.button(
                    text=f"➡️ id{order.id} · {order.name}",
                    callback_data=OrderInfoCallbackFactory(user_type=UserType.CUSTOMER, order_id=order.id).pack()
                )
            case UserType.TRAVELER:
                kb.button(
                    text=f"➡️ id{order.id} · {order.name}",
                    callback_data=OrderInfoCallbackFactory(user_type=UserType.TRAVELER, order_id=order.id).pack()
                )
    kb.button(text="← close", callback_data=MenuButtonsCallbackFactory(button=MenuButton.CLOSE).pack())
    kb.adjust(1)
    return kb.as_markup()


def get_order_actions_keyboard(
    order_id: int,
    mode: UserType,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    match mode:
        case UserType.CUSTOMER:
            kb.button(
                text='delete order',
                callback_data=CrudCallbackFactory(
                    user_type=UserType.CUSTOMER, action=Crud.DELETE, entity_id=order_id).pack()
            )
        case UserType.TRAVELER:
            kb.button(
                text='Sender',
                callback_data=OrderActionCallbackFactory(
                    action=OrderAction.SHOW_SENDER, order_id=order_id).pack()
            )
            kb.button(
                text='take order',
                callback_data=OrderActionCallbackFactory(
                    action=OrderAction.TAKE, order_id=order_id).pack()
            )
    kb.button(text="← close", callback_data=MenuButtonsCallbackFactory(button=MenuButton.CLOSE).pack())
    kb.adjust(1)
    return kb.as_markup()


close_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="← close",
                callback_data=MenuButtonsCallbackFactory(button=MenuButton.CLOSE).pack()
            ),
        ]
    ]
)


account_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="💳 Пополнить баланс", callback_data="user_balance"
            ),
            InlineKeyboardButton(text="💵 Вывод средств", callback_data="withdraw"),
        ],
        [
            InlineKeyboardButton(
                text="📝 Изменить публичное имя", callback_data="rename_account"
            ),
        ],
        [
            InlineKeyboardButton(text="← Закрыть", callback_data="close"),
        ],
    ]
)


def delete_record_keyboad(
    mode: Literal["draft", "order", "application"], record_id: int = None
) -> InlineKeyboardMarkup:
    buttons = []
    match mode:
        case "draft":
            buttons.append(
                [
                    InlineKeyboardButton(text="⌫ Отмена", callback_data="сlose"),
                    InlineKeyboardButton(
                        text="❌ Удалить", callback_data="confirm_delete_draft"
                    ),
                ]
            )
        case "order":
            buttons.append(
                [
                    InlineKeyboardButton(text="⌫ Отмена", callback_data="close"),
                    InlineKeyboardButton(
                        text="❌ Удалить",
                        callback_data=f"delete_published_order:{record_id}",
                    ),
                ]
            )
        case "application":
            buttons.append(
                [
                    InlineKeyboardButton(text="⌫ Отмена", callback_data="close"),
                    InlineKeyboardButton(
                        text="❌ Удалить",
                        callback_data=f"fl_delete_application:{record_id}",
                    ),
                ]
            )
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_answer_keyboard(
    application_id: int,
    mode: UserType,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Answer",
        callback_data=SendMessageCallbackFactory(
            user_type=mode, application_id=application_id
        ).pack(),
    )
    kb.button(text="← close", callback_data=MenuButtonsCallbackFactory(button=MenuButton.CLOSE).pack())
    kb.adjust(1)
    return kb.as_markup()


async def get_back_to_menu_and_pay_buttons(
    user: User,
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Main menu",
        callback_data=MenuButtonsCallbackFactory(button=MenuButton.MAIN_MENU, user_type=user.mode).pack()
    )
    kb.adjust(1)
    return kb.as_markup()
