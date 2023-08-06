from logging import getLogger
from typing import Mapping, Optional, Union

from bffpostgres.utils import import_from_module
from .utils import Con, create_db_pool

logger = getLogger(__name__)


class DBRequest:
    def __init__(self, pool: Con, operations):
        self.pool = pool
        self.operations = operations

    async def __call__(self, **kwargs):
        if isinstance(self.operations, dict):
            return {k: await v(self.pool, **kwargs) for k, v in self.operations.items()}
        return await self.operations(self.pool, **kwargs)


class PostgresApi:
    def __init__(self, pool: Con):
        self.pool = pool

    @classmethod
    async def create(cls, spec: Optional[Mapping[str, Union[str, Mapping]]], **kwargs):
        pool = await create_db_pool(**kwargs)
        api = cls(pool)
        api.set_api_methods(spec)
        return api

    async def stop(self):
        await self.pool.close()

    def set_api_methods(self, spec: Optional[Mapping[str, Union[str, Mapping]]]):
        for name, val in spec.items():
            if isinstance(val, dict):
                for k, v in val.items():
                    val[k] = import_from_module(v)
            if isinstance(val, str):
                val = import_from_module(val)
            setattr(self, name, DBRequest(self.pool, val))
