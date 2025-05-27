from dataclasses import dataclass

from aiogram.filters.state import State, StatesGroup


class States(StatesGroup):
    traveler_mode = State()
    sender_mode = State()
    rename_account = State()
    new_order_draft = State()
    change_order_name = State()
    change_order_budget = State()
    change_order_description = State()
    add_funds_to_balance = State()
    delete_published_order = State()
    traveler_appl_charge = State()
    traveler_appl_days = State()
    traveler_appl_message = State()
    traveler_send_message = State()
    sender_send_message = State()


@dataclass(slots=True)
class OrderFields:
    name: str | None
    description: str | None
    price: str | None
    from_where: str | None
    to: str | None
    when: str | None
    size: str | None
    weight: str | None
