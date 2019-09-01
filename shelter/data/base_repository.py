from contextlib import asynccontextmanager


class BaseGinoRepository:
    def __init__(self, gino_engine):
        self._engine = gino_engine

    @asynccontextmanager
    async def transaction(self):
        async with self._engine.acquire() as connection:
            async with connection.transaction():
                yield
