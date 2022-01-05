# Generated by Django 4.0.1 on 2022-01-05 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('goal_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('points_team_one', models.IntegerField()),
                ('points_team_two', models.IntegerField()),
                ('match_minute', models.IntegerField()),
                ('goal_getter_id', models.IntegerField()),
                ('goal_getter_name', models.CharField(max_length=120)),
                ('is_penalty', models.BooleanField()),
                ('is_own_goal', models.BooleanField()),
                ('is_overtime', models.BooleanField()),
                ('comment', models.CharField(default='', max_length=500)),
                ('match_id', models.BigIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('group_name', models.CharField(max_length=120)),
                ('group_order_id', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('match_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('match_date_time', models.DateTimeField()),
                ('time_zone_id', models.CharField(max_length=120)),
                ('league_id', models.IntegerField()),
                ('league_name', models.CharField(max_length=120)),
                ('league_season', models.CharField(max_length=120)),
                ('league_shortcut', models.CharField(max_length=32)),
                ('match_date_time_utc', models.DateTimeField()),
                ('group_id', models.BigIntegerField()),
                ('team_one_id', models.BigIntegerField()),
                ('team_two_id', models.BigIntegerField()),
                ('last_update', models.DateTimeField()),
                ('match_is_finished', models.BooleanField(default=False)),
                ('location', models.CharField(default=None, max_length=255)),
                ('number_of_viewers', models.IntegerField(default=None)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('result_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('result_name', models.CharField(max_length=120)),
                ('points_team_one', models.IntegerField()),
                ('points_team_two', models.IntegerField()),
                ('result_order_id', models.IntegerField()),
                ('result_type_id', models.IntegerField()),
                ('result_description', models.CharField(max_length=500)),
                ('goal_id', models.BigIntegerField()),
                ('match_id', models.BigIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=120)),
                ('team_icon_url', models.URLField()),
                ('team_group_name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]