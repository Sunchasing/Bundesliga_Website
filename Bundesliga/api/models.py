from django.db import models


class Match(models.Model):
    match_id = models.BigIntegerField(primary_key=True)
    match_date_time = models.DateTimeField()
    time_zone_id = models.CharField(max_length=120)
    league_id = models.IntegerField(null=False)
    league_name = models.CharField(max_length=120)
    league_season = models.IntegerField()
    league_shortcut = models.CharField(max_length=32)
    match_date_time_utc = models.DateTimeField()

    group_id = models.BigIntegerField()  # fk to groups
    team_one_id = models.BigIntegerField()  # fk to teams
    team_two_id = models.BigIntegerField()  # fk to teams

    last_update = models.DateTimeField()
    match_is_finished = models.BooleanField(null=True)
    location = models.CharField(max_length=255, null=True)
    number_of_viewers = models.IntegerField(null=True)


class Team(models.Model):
    team_id = models.BigIntegerField(primary_key=True)
    team_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=120)
    team_icon_url = models.URLField()
    team_group_name = models.CharField(max_length=255, null=True)


class Group(models.Model):
    group_id = models.BigIntegerField(primary_key=True)
    group_name = models.CharField(max_length=120)
    group_order_id = models.IntegerField(null=True)
    year = models.IntegerField()


class Result(models.Model):
    result_id = models.BigIntegerField(primary_key=True)
    result_name = models.CharField(max_length=120)
    points_team_one = models.IntegerField()
    points_team_two = models.IntegerField()
    result_order_id = models.IntegerField()
    result_type_id = models.IntegerField()
    result_description = models.CharField(max_length=500, null=True)

    match_id = models.BigIntegerField()  # fk to matches


class Goal(models.Model):
    goal_id = models.BigIntegerField(primary_key=True)
    points_team_one = models.IntegerField(null=True)
    points_team_two = models.IntegerField(null=True)
    match_minute = models.IntegerField(null=True)
    goal_getter_id = models.IntegerField(null=True)
    goal_getter_name = models.CharField(max_length=120, null=True)
    is_penalty = models.BooleanField(default=False)
    is_own_goal = models.BooleanField(default=False)
    is_overtime = models.BooleanField(default=False)
    comment = models.CharField(max_length=500, null=True)

    match_id = models.BigIntegerField()  # fk to matches
