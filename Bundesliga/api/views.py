import dataclasses
import datetime
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .mixins import BundesligaAPIMixin, ObjectSearchMixin, QueryMixin
from .models import Team, Group, Goal, Match, Result


def _read_file(file_path: str) -> str:
    with open(file_path) as f:
        ret = f.read()
    return ret


# import order team -> group -> match -> goal -> result
class UpdateView(DetailView, BundesligaAPIMixin, ObjectSearchMixin):

    def _add_teams(self):
        teams = self.bl_api.get_all_teams()
        for team in teams:
            team_id = team.get('teamId')
            if not self.exists(Team, team_id=team_id):
                print(f'Adding new team with {team_id=}')
                Team(
                    team_id=team_id,
                    team_name=team.get('teamName'),
                    short_name=team.get('shortName'),
                    team_icon_url=team.get('teamIconUrl'),
                    team_group_name=team.get('teamGroupName'),
                ).save()

    def _add_groups(self):
        groups = self.bl_api.get_all_groups(enrich=True)

        for group in groups:
            group_id = group.get('groupID')
            if not self.exists(Group, group_id=group_id):
                print(f'Adding new group with {group_id=}')
                Group(
                    group_id=group_id,
                    group_name=group.get('groupName'),
                    group_order_id=group.get('groupOrderID'),
                    year=group.get('year'),
                ).save()

    def _add_goals(self, match_id: int, goals: list):
        for goal in goals:
            goal_id = goal.get('goalID')
            if not self.exists(Goal, goal_id=goal_id):
                print(f'Adding new goal with {goal_id=}')
                Goal(
                    goal_id=goal_id,
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
                ).save()

    def _add_results(self, match_id: int, results: list):
        for result in results:
            result_id = result.get("resultID")
            if not self.exists(Result, result_id=result_id):
                print(f'Adding new result with {result_id=}')
                Result(
                    result_id=result.get('resultID'),
                    result_name=result.get('resultName'),
                    points_team_one=result.get('pointsTeam1'),
                    points_team_two=result.get('pointsTeam2'),
                    result_order_id=result.get('resultOrderID'),
                    result_type_id=result.get('resultTypeID'),
                    result_description=result.get('resultDescription'),
                    match_id=match_id,
                ).save()

    def _add_matches(self):
        matches = self.bl_api.get_all_matches_since(self.bl_api.FIRST_RECORDED_YEAR)
        for match in matches:
            match_id = match.get('matchID')

            if not self.exists(Match, match_id=match_id):
                print(f'Adding new match with {match_id=}')

                Match(
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
                ).save()

            self._add_goals(match_id=match_id, goals=match.get('goals'))
            self._add_results(match_id=match_id, results=match.get('matchResults'))

    def get(self, request: HttpRequest, *args, **kwargs) -> Any:
        request_init_time = datetime.datetime.now()
        if self.should_update_db():
            self._add_teams()
            self._add_groups()
            self._add_matches()
        time_taken_s = (datetime.datetime.now() - request_init_time).seconds
        return HttpResponse(f'Download performed. Time taken: {time_taken_s:.2f} seconds')


@dataclasses.dataclass
class UpcomingMatch:
    match_date_time: datetime.datetime
    time_zone: str
    scheduled_start: datetime.timedelta
    team_one_name: str
    team_two_name: str
    team_one_id: int
    team_two_id: int
    t1_img_url: str
    t2_img_url: str
    location: str


class UpcomingMatches(QueryMixin, ListView):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        results = self.run_query(
            sql_filepath='./api/sql/upcoming_matches_for_season.sql',
            league_season=datetime.datetime.now().year - 1
        )
        matches = [UpcomingMatch(*match) for match in results]
        context = {
            'matches': matches
        }
        return render(request, template_name='./api/upcoming_matches.html', context=context)


@dataclasses.dataclass
class TeamSeasonStats:
    wins: int
    draws: int
    losses: int
    wl_ratio: float
    win_percent: float
    team_id: int
    team_name: str
    team_img_url: str


class TeamView(QueryMixin, DetailView):

    def get(self, request: HttpRequest, team_id: int, *args, **kwargs) -> HttpResponse:
        result = self.run_query(
            sql_filepath='./api/sql/team_win_loss.sql',
            team_id=team_id,
            league_season=request.GET.get('season') or datetime.datetime.now().year - 1
        )[0]

        team_stats = TeamSeasonStats(
            wins=result[0],
            draws=result[1],
            losses=result[2],
            wl_ratio=round(result[0] / result[2], 2),
            win_percent=round(result[0] / sum(result[:2]) * 100, 2),
            team_id=result[3],
            team_img_url=result[4],
            team_name=result[5],
        )
        context = {
            'team_stats': team_stats
        }
        return render(request, template_name='./api/team_stats.html', context=context)


@dataclasses.dataclass
class TeamLink():
    team_name: str
    team_icon_url: str
    team_id: int


class TeamsListView(QueryMixin, ListView):

    def get(self, request: HttpRequest, *args, **kwargs):
        query_results = self.run_query(
            sql_filepath='./api/sql/available_teams.sql',
            league_season=request.GET.get('season') or datetime.datetime.now().year - 1
        )
        teams = [TeamLink(*team) for team in query_results]
        if len(query_results) > 0:
            context = {
                'teams': teams
            }
            return render(request, template_name='./api/available_teams.html', context=context)
        return HttpResponse(f"No teams found")


class UpcomingMatchesForTeam(QueryMixin, ListView):

    def get(self, request: HttpRequest, team_id: int, *args, **kwargs) -> HttpResponse:
        query_results = self.run_query(
            sql_filepath='./api/sql/team_upcoming.sql',
            team_id=team_id,
            league_season=datetime.datetime.now().year - 1
        )

        results = [UpcomingMatch(*match) for match in query_results]

        if len(query_results) > 0:
            context = {
                'matches': results
            }
            return render(request, template_name='./api/upcoming_matches.html', context=context)
        return HttpResponse(f"The team has no matches")
