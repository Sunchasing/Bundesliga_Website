from datetime import datetime as _dt
from typing import List

from requests import Session


class BundesligaAPI:
    BASE_URL = "https://api.openligadb.de/"
    TEAMS_ENDPOINT = "getavailableteams"
    MATCHES_ENDPOINT = "getmatchdata"
    LEAGUE = 'bl1'

    def __init__(self):
        self._session: Session = Session()
        self.current_year: int = _dt.now().year

    def get_all_teams(self, year: int = None):
        year = year or self.current_year

        endpoint = self.build_url([self.TEAMS_ENDPOINT, self.LEAGUE, str(year)])
        resp = self._session.get(url=endpoint)

        return resp.json()

    def get_all_matches_for_current_season(self):
        endpoint = self.build_url([self.MATCHES_ENDPOINT, self.LEAGUE, str(self.current_year)])
        resp = self._session.get(url=endpoint)
        return resp.json()

    def get_all_matches_since(self, since=(_dt.now().year - 1)):
        ret = []
        for year in range(since, self.current_year + 1):
            endpoint = self.build_url([self.MATCHES_ENDPOINT, self.LEAGUE, str(year)])
            resp = self._session.get(url=endpoint)
            ret.extend(resp.json())

        return ret

    def build_url(self, url_parts: List[str]) -> str:
        return f'{self.BASE_URL}{"/".join(url_parts)}'
