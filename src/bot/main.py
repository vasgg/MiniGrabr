import logging
from asyncio import run
from bot.handlers.common_handlers import router as common_router
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import settings
from bot.internal.helpers import setup_logs
from bot.internal.notify_admin import on_shutdown, on_startup
from bot.middlewares.auth import AuthMiddleware
from bot.middlewares.logging import LoggingMiddleware
from bot.middlewares.session import DBSessionMiddleware
from bot.middlewares.updates_dumper import UpdatesDumperMiddleware
from database.db import get_db


async def main():
    setup_logs("mini_grabr_bot")
    bot = Bot(
        token=settings.bot.TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    storage = MemoryStorage()
    dispatcher = Dispatcher(
        storage=storage, settings=settings, events_isolation=SimpleEventIsolation()
    )
    db = get_db()
    db_session_middleware = DBSessionMiddleware(db)
    dispatcher.update.outer_middleware(UpdatesDumperMiddleware())
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)
    dispatcher.message.middleware(db_session_middleware)
    dispatcher.callback_query.middleware(db_session_middleware)
    dispatcher.message.middleware(AuthMiddleware())
    dispatcher.callback_query.middleware(AuthMiddleware())
    dispatcher.message.middleware.register(LoggingMiddleware())
    dispatcher.callback_query.middleware.register(LoggingMiddleware())
    dispatcher.include_routers(
        common_router,
    )
    logging.info("minigrabr started")
    await dispatcher.start_polling(bot, skip_updates=True)


def run_main():
    run(main())


if __name__ == "__main__":
    run_main()
