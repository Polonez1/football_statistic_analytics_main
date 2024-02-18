from scipy.stats import poisson
import pandas as pd
import numpy as np


def calculate_poisson_dist(avg: int, range_from: int = 0, range_to: int = 11):
    goals_list = list(range(range_from, range_to))
    data = {
        "goal": goals_list,
        "p": [poisson.pmf(k=goal, mu=avg).round(2) for goal in goals_list],
    }
    df = pd.DataFrame(data)
    return df


def skellam_dist_matrix(avg_1, avg_2):
    distribution_1 = calculate_poisson_dist(avg=avg_1)
    distribution_2 = calculate_poisson_dist(avg=avg_2)
    matrix = np.outer(distribution_1["p"], distribution_2["p"])
    result_df = pd.DataFrame(
        matrix, index=distribution_1["goal"], columns=distribution_2["goal"]
    ).reset_index(drop=True)
    return result_df


def goals_matrix_melt(avg_1, avg_2):
    result_df = skellam_dist_matrix(avg_1=avg_1, avg_2=avg_2)
    result_df_melt = result_df.stack().reset_index()
    result = result_df_melt.rename(
        columns={"level_0": "goal_1", "goal": "goal_2", 0: "prb"}, inplace=False
    )
    result["result_goal"] = (
        result["goal_1"].astype("str") + "-" + result["goal_2"].astype("str")
    )

    return result


def results_distribution_by_skellam(avg_1, avg_2, total):
    df = goals_matrix_melt(avg_1=avg_1, avg_2=avg_2)
    df["exp_counts"] = df["prb"] * total
    df["exp_counts"] = df["exp_counts"].round(0)

    return df


def result_from_skellam_matrix(avg_1, avg_2):
    skellam_matrix = skellam_dist_matrix(avg_1, avg_2)
    goals_range = list(range(0, 11))

    draw = 0
    home_win = 0
    away_win = 0

    for i in goals_range:
        for j in goals_range:
            prb = skellam_matrix.iloc[i, j]
            if i == j:
                draw = draw + prb
            elif i > j:
                home_win = home_win + prb
            elif i < j:
                away_win = away_win + prb

    return pd.DataFrame(
        {
            "result": ["home_win", "draw", "away_win"],
            "prb": [round(home_win, 2), round(draw, 2), round(away_win, 2)],
        }
    )


def over_from_skellam_matrix(avg_1, avg_2, overunder: float = 2.5):
    skellam_matrix = skellam_dist_matrix(avg_1, avg_2)
    goals_range = list(range(0, 11))
    over = 0
    under = 0
    for i in goals_range:
        for j in goals_range:
            prb = skellam_matrix.iloc[i, j]
            if i + j > overunder:
                over = over + prb
            elif i + j < overunder:
                under += prb

    return pd.DataFrame(
        {
            "result": [f"over_{overunder}", f"under_{overunder}"],
            "prb": [round(over, 2), round(under, 2)],
        }
    )


def btts_from_skellam_matrix(avg_1, avg_2):
    skellam_matrix = skellam_dist_matrix(avg_1, avg_2)
    goals_range = list(range(0, 11))
    btts = 0
    nobtts = 0
    for i in goals_range:
        for j in goals_range:
            prb = skellam_matrix.iloc[i, j]
            if i > 0 and j > 0:
                btts += prb
            else:
                nobtts += prb

    return pd.DataFrame(
        {
            "result": [f"btts", f"nobtts"],
            "prb": [round(btts, 2), round(nobtts, 2)],
        }
    )


def team_over_from_skellam_matrix(avg_1, avg_2):
    pass


def asian_handicap_from_skellam_matrix(avg_1, avg_2):
    pass


if "__main__" == __name__:
    df = btts_from_skellam_matrix(avg_1=0.8, avg_2=3.1)
    print(df)
