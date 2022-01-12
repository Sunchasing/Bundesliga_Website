from datetime import datetime as _dt
from typing import Final

from django.db import connection

from Bundesliga_sdk.api import BundesligaAPI
from api.utils import _read_file


class BundesligaAPIMixin:
    bl_api: Final[BundesligaAPI] = BundesligaAPI()
    threshold_s: Final[int] = 10 * 60  # 10min
    last_update: _dt = None

    def should_update_db(self):
        now = _dt.now()
        if not self.last_update:
            self.last_update = now
            return True
        if (now - self.last_update).seconds > self.threshold_s:
            self.last_update = now
            return True
        return False


class ObjectSearchMixin:

    def exists(self, model: type, **fields) -> bool:
        try:
            model.objects.get(**fields)
            return True
        except:
            return False


class QueryMixin:

    def is_nil_result(self, result: tuple) -> bool:
        for elem in result:
            if elem != None:
                return False
        return True

    def format_query(self, sql_filepath: str, **kwargs) -> str:
        query = _read_file(sql_filepath)
        return query.format(**kwargs)

    def run_query(self, sql_filepath: str, all: bool = True, **kwargs):
        sql_query = self.format_query(sql_filepath, **kwargs)
        with connection.cursor() as cur:
            cur.execute(sql_query)
            results = cur.fetchall() if all else cur.fetchone()

        return results
