from django.db import models


class Match(models.Model):
    match_id = models.BigIntegerField(primary_key=True)
    match_date_time = models.DateTimeField()
    time_zone_id = models.CharField(max_length=120)
    league_id = models.IntegerField(null=False)
    league_name = models.CharField(max_length=120)
    league_season = models.CharField(max_length=120)
    league_shortcut = models.CharField(max_length=32)
    match_date_time_utc = models.DateTimeField()

    group_id = models.BigIntegerField()
    team_one_id = models.BigIntegerField()
    team_two_id = models.BigIntegerField()

    last_update = models.DateTimeField()
    match_is_finished = models.BooleanField(default=False)
    location = models.CharField(max_length=255, default=None)
    number_of_viewers = models.IntegerField(default=None)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


class Team(models.Model):
    team_id = models.BigIntegerField(primary_key=True)
    team_name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=120)
    team_icon_url = models.URLField()
    team_group_name = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


class Group(models.Model):
    group_id = models.BigIntegerField(primary_key=True)
    group_name = models.CharField(max_length=120)
    group_order_id = models.IntegerField(null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


class Result(models.Model):
    result_id = models.BigIntegerField(primary_key=True)
    result_name = models.CharField(max_length=120)
    points_team_one = models.IntegerField()
    points_team_two = models.IntegerField()
    result_order_id = models.IntegerField()
    result_type_id = models.IntegerField()
    result_description = models.CharField(max_length=500)

    goal_id = models.BigIntegerField()
    match_id = models.BigIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)


class Goal(models.Model):
    goal_id = models.BigIntegerField(primary_key=True)
    points_team_one = models.IntegerField()
    points_team_two = models.IntegerField()
    match_minute = models.IntegerField()
    goal_getter_id = models.IntegerField()
    goal_getter_name = models.CharField(max_length=120)
    is_penalty = models.BooleanField()
    is_own_goal = models.BooleanField()
    is_overtime = models.BooleanField()
    comment = models.CharField(max_length=500, default='')

    match_id = models.BigIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
