SELECT team_name, team_icon_url, team_id
FROM api_team
JOIN api_match am ON am.team_one_id = team_id
WHERE am.league_season = {league_season}