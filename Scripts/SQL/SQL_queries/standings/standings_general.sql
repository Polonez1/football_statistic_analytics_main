with cte_table as (
    select s.season,
        s.rank as 'rank',
        s.team_name,
        s.all_played as 'match_played',
        s.all_win as 'win',
        s.all_draw as 'draw',
        s.all_lose as 'lose',
        s.all_goals_for as 'GF',
        s.all_goals_against as 'GA',
        s.points,
        if(ls.team_name is null, True, False) as 'from_previous_league',
        s.description as 'standings',
        'total' as 'dim_home_away_total',
        s.team_id,
        s.league_id,
        s.stats_id,
        concat(s.stats_id, '-', 0) as 'unique_stats_id'
    from standings s
        left outer join (
            select team_id,
                team_name
            from standings
            where season = { season } - 1
        ) ls on s.team_id = ls.team_id
    where s.season = { season }
    union all
    select s.season,
        s.rank as 'rank',
        s.team_name,
        s.home_played as 'match_played',
        s.home_win as 'win',
        s.home_draw as 'draw',
        s.home_lose as 'lose',
        s.home_goals_for as 'GF',
        s.home_goals_against as 'GA',
        s.points,
        if(ls.team_name is null, True, False) as 'from_previous_league',
        s.description as 'standings',
        'home' as 'dim_home_away_total',
        s.team_id,
        s.league_id,
        s.stats_id,
        concat(s.stats_id, '-', 1) as 'unique_stats_id'
    from standings s
        left outer join (
            select team_id,
                team_name
            from standings
            where season = { season } - 1
        ) ls on s.team_id = ls.team_id
    where s.season = { season }
    union all
    select s.season,
        s.rank as 'rank',
        s.team_name,
        s.away_played as 'match_played',
        s.away_win as 'win',
        s.away_draw as 'draw',
        s.away_lose as 'lose',
        s.away_goals_for as 'GF',
        s.away_goals_against as 'GA',
        s.points,
        if(ls.team_name is null, True, False) as 'from_previous_league',
        s.description as 'standings',
        'away' as 'dim_home_away_total',
        s.team_id,
        s.league_id,
        s.stats_id,
        concat(s.stats_id, '-', 2) as 'unique_stats_id'
    from standings s
        left outer join (
            select team_id,
                team_name
            from standings
            where season = { season } - 1
        ) ls on s.team_id = ls.team_id
    where s.season = { season }
)
select *
from cte_table t