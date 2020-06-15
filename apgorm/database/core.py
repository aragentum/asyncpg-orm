import logging
from typing import Tuple, Any, List

from asyncpg import create_pool
from asyncpg.pool import Pool


class ApgORM:

    def __init__(self, dsn: str, max_inactive_connection_lifetime=300,
                 min_size=1, max_size=100) -> None:
        self.dsn = dsn
        self.max_inactive_connection_lifetime = max_inactive_connection_lifetime
        self.max_size = max_size
        self.min_size = min_size
        self.logger = logging.getLogger(__name__)

    async def init(self, echo=False, loop=None):
        """
        Init PG pool
        """
        self.logger.debug("Initializing PG pool")
        pg_pool: Pool = await create_pool(dsn=self.dsn,
                                          max_inactive_connection_lifetime=self.max_inactive_connection_lifetime,
                                          min_size=self.min_size,
                                          max_size=self.max_size,
                                          loop=loop)

        return Session(pg_pool, echo)


class Session:
    def __init__(self, pg_pool: Pool, echo=False):
        self.echo = echo
        self.pg_pool = pg_pool
        self.logger = logging.getLogger(__name__)

    async def fetch(self, sql, *args, **kwargs):
        async with self.pg_pool.acquire() as connection:
            return await connection.fetch(sql, *args, **kwargs)

    async def execute(self, sql, *args, **kwargs):
        async with self.pg_pool.acquire() as connection:
            return await connection.execute(sql, *args, **kwargs)

    async def close(self):
        self.logger.debug("Closing PG pool")
        await self.pg_pool.close()


class BaseColumnType:
    columnName: str

    def __eq__(self, value):
        """
        Overload operator ==
        """
        return f"{self.columnName} = %s", [value]


class String(BaseColumnType):
    def __init__(self, column_name, length: int = 100):
        self.length = 100
        self.columnName = column_name


class Integer(BaseColumnType):
    def __init__(self, column_name):
        self.columnName = column_name


class BaseModel:
    __tablename__: str

    def query(self, session):
        return self.__query(session, self)

    class __query:
        def __init__(self, session, model):
            self.model = model
            self.session: Session = session
            self.logger = logging.getLogger(__name__)

        async def where(self, where_clauses: Tuple[str, List[Any]]):
            condition, params = where_clauses

            # replace %s to $n
            condition = condition % tuple([f"${i}" for i in range(1, len(params) + 1)])

            # build sql query
            sql = """SELECT * FROM "%s" WHERE %s""" % (self.model.__tablename__, condition)

            if self.session.echo:
                self.logger.debug("%s; %s" % (sql, params))
            return await self.session.fetch(sql, *params)
