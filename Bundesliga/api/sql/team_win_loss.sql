SELECT SUM(wins) AS wins, SUM(draws) AS draws, SUM(losses) AS losses
FROM (
         SELECT CASE WHEN res < 0 THEN COUNT(res) ELSE 0 END AS losses,
                CASE WHEN res > 0 THEN COUNT(res) ELSE 0 END AS wins,
                CASE WHEN res = 0 THEN COUNT(res) ELSE 0 END AS draws
         FROM (
                  SELECT r.result_id, m.match_id, MAX(r.result_order_id), (r.points_team_one - r.points_team_two) AS res
                  FROM api_result r
                           JOIN api_match m ON m.match_id = r.match_id
                  WHERE m.team_one_id = {team_id}
                    AND m.league_season = {league_season}
                  GROUP BY m.match_id, r.result_id, res
                  UNION
                  SELECT r.result_id, m.match_id, MAX(r.result_order_id), (r.points_team_two - r.points_team_one) AS res
                  FROM api_result r
                           JOIN api_match m
                                ON m.match_id = r.match_id
                  WHERE m.team_two_id = {team_id}
                    AND m.league_season = {league_season}
                  GROUP BY m.match_id, r.result_id, res
              ) team_results
         GROUP BY team_results.res
     ) ratios