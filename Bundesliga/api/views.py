import datetime
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView

from .mixins import BundesligaAPIMixin, ObjectSearchMixin
from .models import Team, Group, Goal, Match, Result


# import order team -> group -> match -> goal -> result
class UpdateView(DetailView, BundesligaAPIMixin, ObjectSearchMixin):

    def _add_teams(self):
        teams = self.bl_api.get_all_teams()
        for team in teams:
            if not self.exists(Team, team_id=team.get('teamId')):
                print(f'Adding new team with ID={team.get("teamId")}')
                new_team = Team(
                    team_id=team.get('teamId'),
                    team_name=team.get('teamName'),
                    short_name=team.get('shortName'),
                    team_icon_url=team.get('teamIconUrl'),
                    team_group_name=team.get('teamGroupName'),
                )
                new_team.save()

    def _add_groups(self):
        groups = self.bl_api.get_all_groups(enrich=True)

        for group in groups:
            if not self.exists(Group, group_id=group.get('groupID')):
                print(f'Adding new group with ID={group.get("groupID")}')
                new_group = Group(
                    group_id=group.get('groupID'),
                    group_name=group.get('groupName'),
                    group_order_id=group.get('groupOrderID'),
                    year=group.get('year'),
                )
                new_group.save()

    def _add_goals(self, match_id: int, goals: list):
        for goal in goals:
            if not self.exists(Goal, goal_id=goal.get('goalID')):
                print(f'Adding new goal with ID={goal.get("goalID")}')
                new_goal = Goal(
                    goal_id=goal.get('goalID'),
                    points_team_one=goal.get('scoreTeam1'),
                    points_team_two=goal.get('scoreTeam2'),
                    match_minute=goal.get('matchMinute'),
                    goal_getter_id=goal.get('goalGetterID'),
                    goal_getter_name=goal.get('goalGetterName'),
                    is_penalty=goal.get('isPenalty'),
                    is_own_goal=goal.get('isOwnGoal'),
                    is_overtime=goal.get('isOvertime'),
                    comment=goal.get('comment'),
                    match_id=match_id,
                )
                new_goal.save()

    def _add_results(self, match_id: int, results: list):
        for result in results:
            if not self.exists(Result, result_id=result.get("resultID")):
                print(f'Adding new result with ID={result.get("resultID")}')
                new_result = Result(
                    result_id=result.get('resultID'),
                    result_name=result.get('resultName'),
                    points_team_one=result.get('pointsTeam1'),
                    points_team_two=result.get('pointsTeam2'),
                    result_order_id=result.get('resultOrderID'),
                    result_type_id=result.get('resultTypeID'),
                    result_description=result.get('resultDescription'),
                    match_id=match_id,
                )
                new_result.save()

    def _add_matches(self):
        matches = self.bl_api.get_all_matches_since(self.bl_api.FIRST_RECORDED_YEAR)
        for match in matches:
            match_id = match.get('matchID')

            if not self.exists(Match, match_id=match.get('matchID')):
                print(f'Adding new match with ID={match.get("matchID")}')

                new_match = Match(
                    match_id=match_id,
                    match_date_time=match.get('matchDateTime'),
                    time_zone_id=match.get('timeZoneID'),
                    league_id=match.get('leagueId'),
                    league_name=match.get('leagueName'),
                    league_season=match.get('leagueSeason'),
                    league_shortcut=match.get('leagueShortcut'),
                    match_date_time_utc=match.get('matchDateTimeUTC'),
                    group_id=match.get('group').get('groupID'),
                    team_one_id=match.get('team1').get('teamId'),
                    team_two_id=match.get('team2').get('teamId'),
                    last_update=match.get('lastUpdateDateTime'),
                    match_is_finished=match.get('matchIsFinished'),
                    location=match.get('location'),
                    number_of_viewers=match.get('numberOfViewers'),
                )
                new_match.save()
            self._add_goals(match_id=match_id, goals=match.get('goals'))
            self._add_results(match_id=match_id, results=match.get('matchResults'))

    def get(self, request: HttpRequest, *args, **kwargs) -> Any:
        time = datetime.datetime.now()

        if self.should_update_db():
            self._add_teams()
            self._add_groups()
            self._add_matches()

        return HttpResponse(f'time taken:{datetime.datetime.now() - time}')
