import pandas as pd


def add_average_goals(df: pd.DataFrame) -> pd.DataFrame:
    df["goal_avg_GF"] = df["GF"] / df["match_played"]
    df["goal_avg_GA"] = df["GA"] / df["match_played"]

    return df


def add_goals_string_result(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy["goals_result"] = (
        df_copy["goals_home"].astype("int").astype("str")
        + "-"
        + df_copy["goals_away"].astype("int").astype("str")
    )

    return df_copy
