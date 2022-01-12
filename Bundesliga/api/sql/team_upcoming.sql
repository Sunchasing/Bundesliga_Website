SELECT m.match_date_time                                  AS match_date,
       m.time_zone_id                                     AS tz,
       (m.match_date_time_utc - NOW() AT TIME ZONE 'UTC') AS scheduled_start,
       t1.team_name                                       AS team_one,
       t2.team_name                                       AS team_two,
       m.team_one_id                                      AS t1_id,
       m.team_two_id                                      AS t2_id,
       t1.team_icon_url                                   AS t1_img,
       t2.team_icon_url                                   AS t2_img,
       m.location                                         AS loc

FROM api_match m
         INNER JOIN api_team t1 ON t1.team_id = m.team_one_id
         INNER JOIN api_team t2 ON t2.team_id = m.team_two_id
         INNER JOIN api_group g ON g.group_id = m.group_id

WHERE m.league_season = {league_season}
  AND m.match_is_finished = false
  AND m.match_date_time_utc
    > NOW()
  AND (m.team_one_id = {team_id}
   OR m.team_two_id = {team_id})
