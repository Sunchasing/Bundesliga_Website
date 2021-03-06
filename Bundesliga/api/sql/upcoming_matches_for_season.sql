SELECT
       m.match_date_time                                  AS match_date,
       m.time_zone_id                                     AS tz,
       (m.match_date_time_utc - NOW() AT TIME ZONE 'UTC') AS scheduled_start,
       t1.team_name                                       AS team_one,
       t2.team_name                                       AS team_two,
       t1.team_id                                         AS team_one_id,
       t2.team_id                                         AS team_two_id,
       t1.team_icon_url                                   AS t1_img_url,
       t2.team_icon_url                                   AS t2_img_url,
       m.location                                         AS loc

FROM api_match m
         INNER JOIN api_team t1 ON t1.team_id = m.team_one_id
         INNER JOIN api_team t2 ON t2.team_id = m.team_two_id
         INNER JOIN api_group g ON g.group_id = m.group_id
WHERE m.league_season = {league_season}
    AND m.match_is_finished = false
    AND m.match_date_time_utc > NOW() AT TIME ZONE 'UTC'
ORDER BY scheduled_start
