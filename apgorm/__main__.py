import asyncio
import logging

from apgorm.database.core import ApgORM
from apgorm.database.model import User
from apgorm.settings import PG_URL

pg_orm = ApgORM(PG_URL)


async def main():
    session = await pg_orm.init(echo=True)
    logger = logging.getLogger(__name__)

    user1 = await User().query(session).where(User.username == "test")
    logger.info(user1)

    user2 = await User().query(session).where(User.id == 2)
    logger.info(user2)

    await session.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
