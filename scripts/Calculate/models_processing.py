import pandas as pd
import numpy as np


def expand_data_by_skellam(self, data, model):
    """skellam"""
    leagues = set(data["league_name"])
    seasons = set(data["league_season"])
    zero_inf_values = np.arange(0, 0.21, 0.01).tolist()
    dff = []
    for season in seasons:
        for league in leagues:
            for z in zero_inf_values:
                print(season, league, z)
                selectet_model = model(
                    data=data, zero_inf=float(z), season=season, league=league
                )
                df = selectet_model.create_result_data()
                df["zero_inf_koef"] = z
                df["league"] = league
                df["season"] = season
                dff.append(df)
    expanded_data: pd.DataFrame = pd.concat(dff)
    return expanded_data
