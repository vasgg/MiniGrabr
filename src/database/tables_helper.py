from sqlalchemy.ext.asyncio import AsyncEngine
import asyncio

from database.db import get_db
from database.models import Base


async def create_or_drop_db(engine: AsyncEngine, create: bool = True):
    async with engine.begin() as conn:
        if create:
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)
        else:
            await conn.run_sync(Base.metadata.drop_all)


def run_main():
    db = get_db()
    asyncio.run(create_or_drop_db(db.engine))


if __name__ == "__main__":
    run_main()
