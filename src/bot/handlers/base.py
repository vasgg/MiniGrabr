from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.internal.lexicon import text
from bot.internal.enums import MenuButtons, UserType
from bot.keyboards.callbacks import MenuCallbackFactory, UserTypeCallbackFactory
from bot.keyboards.common_keyboards import role_selector_kb
from bot.keyboards.customer_keyboard import customer_kb
from bot.keyboards.traveler_keyboards import traveler_kb
from database.models import User

router = Router()


@router.message(CommandStart())
async def start_message(message: Message, state: FSMContext) -> None:
    msg = await message.answer(
        text=text["start_reply"],
        reply_markup=role_selector_kb(),
    )
    await state.update_data(main_menu_message_id=msg.message_id)


@router.callback_query(MenuCallbackFactory.filter())
async def menu_handler(
    call: CallbackQuery,
    callback_data: MenuCallbackFactory,
) -> None:
    await call.answer()
    match callback_data.action:
        case MenuButtons.BACK:
            await call.message.edit_text(
                text=text["start_reply"],
                reply_markup=role_selector_kb(),
            )


@router.callback_query(UserTypeCallbackFactory.filter())
async def role_selector_handler(
    call: CallbackQuery,
    callback_data: UserTypeCallbackFactory,
    user: User,
) -> None:
    await call.answer()
    match callback_data.user_type:
        case UserType.CUSTOMER:
            user.mode = UserType.CUSTOMER
            await call.message.edit_text(
                text=text["customer_reply"], reply_markup=customer_kb()
            )
        case UserType.TRAVELER:
            user.mode = UserType.TRAVELER
            await call.message.edit_text(
                text=text["traveler_reply"], reply_markup=traveler_kb()
            )
