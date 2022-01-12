SELECT SUM(wins) AS wins, SUM(draws) AS draws, SUM(losses) AS losses, ratios.team_id, t.team_icon_url, t.team_name
FROM (
         SELECT CASE WHEN res < 0 THEN COUNT(res) ELSE 0 END AS losses,
                CASE WHEN res > 0 THEN COUNT(res) ELSE 0 END AS wins,
                CASE WHEN res = 0 THEN COUNT(res) ELSE 0 END AS draws,
                team_results.team_id
         FROM (
                  SELECT r.result_id, m.match_id, MAX(r.result_order_id), (r.points_team_one - r.points_team_two) AS res, team_one_id AS team_id
                  FROM api_result r
                           JOIN api_match m ON m.match_id = r.match_id
                  WHERE m.team_one_id = {team_id}
                    AND m.league_season = {league_season}
                  GROUP BY m.match_id, r.result_id, res
                  UNION
                  SELECT r.result_id, m.match_id, MAX(r.result_order_id), (r.points_team_two - r.points_team_one) AS res, team_two_id
                  FROM api_result r
                           JOIN api_match m
                                ON m.match_id = r.match_id
                  WHERE m.team_two_id = {team_id}
                    AND m.league_season = {league_season}
                  GROUP BY m.match_id, r.result_id, res
              ) team_results
         GROUP BY team_results.res, team_results.team_id
     ) ratios
JOIN api_team t ON t.team_id = ratios.team_id
group by t.team_icon_url, t.team_name, ratios.team_id