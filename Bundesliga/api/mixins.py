from typing import Final
from datetime import datetime as _dt


from Bundesliga_sdk.api import BundesligaAPI


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
    