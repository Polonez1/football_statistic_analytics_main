select f.fixture_id,
    f.fixture_date,
    f.league_name,
    f.league_season,
    f.fixture_status_long,
    f.fixture_status_short,
    f.league_round,
    f.teams_home_name,
    f.teams_home_winner,
    f.goals_home,
    f.score_halftime_home,
    f.teams_away_name,
    f.teams_away_winner,
    f.goals_away,
    f.score_halftime_away,
    if(
        f.fixture_status_short <> 'NS',
        case
            when f.goals_home > f.goals_away then 'home_win'
            when f.goals_home < f.goals_away then 'away_win'
            when f.goals_home = f.goals_away then 'draw'
            else null
        end,
        'not played'
    ) as 'result',
    f.teams_away_id,
    f.teams_home_id,
    f.fixture_venue_id
from fixtures f