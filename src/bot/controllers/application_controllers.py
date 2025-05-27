from typing import Literal

import arrow
from sqlalchemy import Result, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.internal.enums import UserType
from database.models import Application


async def create_application(
    order_id: int,
    customer_id: int,
    traveler_id: int,
    completion_days: int,
    message: str,
    session: AsyncSession,
) -> None:
    new_application = Application(
        order_id=order_id,
        customer_id=customer_id,
        traveler_id=traveler_id,
        completion_days=completion_days,
        message=message,
    )
    session.add(new_application)


async def get_applications(
    session: AsyncSession,
    mode: Literal["all", "by_customer", "by_worker", "by_order", "rest_applications"],
    customer_id: int = None,
    traveler_id: int = None,
    order_id: int = None,
    application_id: int = None,
):
    match mode:
        case "all":
            query = select(Application).filter(Application.is_active)
        case "by_customer":
            query = select(Application).filter(
                Application.customer_id == customer_id, Application.is_active
            )
        case "by_worker":
            query = select(Application).filter(
                Application.traveler_id == traveler_id, Application.is_active
            )
        case "by_order":
            query = select(Application).filter(
                Application.order_id == order_id, Application.is_active
            )
        case "rest_applications":
            query = select(Application).filter(
                Application.order_id == order_id,
                Application.id != application_id,
                Application.is_active,
            )
    result = await session.execute(query)
    applications = result.scalars().all()
    return applications


async def get_active_application(
    session,
    mode: Literal["by_app_id", "by_order_id"],
    application_id: int = None,
    order_id: int = None,
) -> Application:
    match mode:
        case "by_app_id":
            query = select(Application).filter(
                Application.id == application_id, Application.is_active
            )
        case "by_order_id":
            query = select(Application).filter(
                Application.order_id == order_id, Application.is_active
            )
        case _:
            raise ValueError(f"Unknown mode: {mode}")
    result: Result = await session.execute(query)
    application = result.scalar()
    return application


async def get_application(
    session,
    mode: Literal["by_app_id", "by_order_id"],
    application_id: int = None,
    order_id: int = None,
) -> Application:
    match mode:
        case "by_app_id":
            query = select(Application).filter(Application.id == application_id)
        case "by_order_id":
            query = select(Application).filter(Application.order_id == order_id)
        case _:
            raise ValueError(f"Unknown mode: {mode}")
    result: Result = await session.execute(query)
    application = result.scalar()
    return application


def get_applications_list_string(
    mode: UserType, applications: list, orders: list = None
) -> str:
    text = ""
    orders_dict = {order.id: order for order in orders}
    for application in sorted(applications, key=lambda x: x.id, reverse=True):
        created_at = arrow.get(application.created_at)
        match mode:
            case UserType.TRAVELER:
                text += (
                    f"🔼 <b>Заявка id{application.id}</b> · <i>создана {created_at.humanize(locale='ru')}</i>\n"
                    f"🌐 к заказу <b>id{application.order_id} · {orders_dict[application.order_id].name}</b>\n"
                    f"💎 <b>{application.fee}₽</b> · <i>стоимость работы</i>\n"
                    f"⏳ <b>{application.completion_days}</b> · <i>срок выполнения в днях</i>\n\n"
                )
            case UserType.CUSTOMER:
                text += (
                    f"🔼 <b>Заявка id{application.id}</b> к вашему заказу <b>id{application.order_id}</b>\n"
                    f"🌐 <b>{orders_dict[application.order_id].name}</b> · "
                    f"<i>Бюджет</i> <b>{orders_dict[application.order_id].budget}₽</b>\n"
                    f"🕛 <i>созданa {created_at.humanize(locale='ru')}</i>\n"
                    f"💎 <i>стоимость работы</i> · <b>{application.fee}₽</b>\n"
                    f"⏳ <i>срок выполнения в днях</i> · <b>{application.completion_days}</b>\n"
                    f"📝 <i>сообщение</i> · <b>{application.message}</b>\n\n"
                )
    if len(text) == 0:
        text = "🌐 Пока нет активных заявок"
    return text


async def get_projects_list_string(
    mode: UserType, applications: list, orders: list
) -> str:
    text = ""
    orders_dict = {order.id: order for order in orders}
    for application in sorted(applications, key=lambda x: x.id, reverse=True):
        created_at = arrow.get(application.created_at)
        match mode:
            case UserType.TRAVELER:
                text += (
                    f"🌐 <b>{orders_dict[application.order_id].name}</b>\n"
                    f"🔼 <b>Заявка id{application.id}</b> · <i>создана {created_at.humanize(locale='ru')}</i>\n"
                    f"💎 <b>{application.fee}₽</b> · <i>стоимость работы</i>\n"
                    f"⏳ <b>{application.completion_days}</b> · <i>срок выполнения в днях</i>\n\n"
                )
            case UserType.CUSTOMER:
                text += (
                    f"🔼 <b>Заявка id{application.id}</b> к вашему заказу\n"
                    f"🌐 <b>{orders_dict[application.order_id].name}</b> · "
                    f"<i>Бюджет</i> <b>{orders_dict[application.order_id].budget}₽</b>\n"
                    f"🕛 <i>созданa {created_at.humanize(locale='ru')}</i>\n"
                    f"💎 <i>стоимость работы</i> · <b>{application.fee}₽</b>\n"
                    f"⏳ <i>срок выполнения в днях</i> · <b>{application.completion_days}</b>\n"
                    f"📝 <i>сообщение</i> · <b>{application.message}</b>\n\n"
                )
    if len(text) == 0:
        text = "🌐 Пока нет активных проектов"
    return text


async def del_application(application_id: int, session: AsyncSession) -> None:
    query = delete(Application).filter(Application.id == application_id)
    await session.execute(query)


async def toggle_application_activeness(
    application_id: int, session: AsyncSession
) -> None:
    await session.execute(
        update(Application)
        .filter(Application.id == application_id)
        .values(is_active=func.not_(Application.is_active))
    )
