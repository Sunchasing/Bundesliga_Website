from datetime import datetime as _dt
from typing import List, Final

from requests import Session


class BundesligaAPI:
    BASE_URL: Final[str] = "https://api.openligadb.de/"
    TEAMS_ENDPOINT: Final[str] = "getavailableteams"
    MATCHES_ENDPOINT: Final[str] = "getmatchdata"
    GROUPS_ENDPOINT: Final[str] = "getavailablegroups"
    LEAGUE: Final[str] = 'bl1'
    FIRST_RECORDED_YEAR: Final[int] = 2002

    def __init__(self):
        self._session: Session = Session()
        self.current_year: int = _dt.now().year

    def get_all_teams(self):
        ret = []
        present_teams = set()  # O(1) id search
        for year in range(self.FIRST_RECORDED_YEAR, self.current_year + 1):
            res = self.get_teams_for_year(year)
            for team in res:
                team_id = team['teamId']
                if team_id not in present_teams:
                    present_teams.add(team_id)
                    ret.append(team)
        return ret

    def get_teams_for_year(self, year: int = None):
        year = year or self.current_year

        endpoint = self.build_url([self.TEAMS_ENDPOINT, self.LEAGUE, str(year)])
        resp = self._session.get(url=endpoint).json()

        # Check if we hve a good response instead of 404 (comes as dict, meaning we have invalid year)
        if isinstance(resp, list):
            return resp
        return []

    def get_all_groups(self, enrich: bool = False):
        ret = []
        for year in range(self.FIRST_RECORDED_YEAR, self.current_year + 1):
            ret.extend(self.get_groups_for_year(year, enrich=enrich))
        return ret

    def get_groups_for_year(self, year: int = None, enrich: bool = False):
        year = year or self.current_year

        endpoint = self.build_url([self.GROUPS_ENDPOINT, self.LEAGUE, str(year)])
        resp = self._session.get(url=endpoint).json()

        # Check if we hve a good response instead of 404 (comes as dict, meaning we have invalid year)
        if isinstance(resp, list):
            if enrich:
                for group in resp:
                    group['year'] = year
            return resp
        return []

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
