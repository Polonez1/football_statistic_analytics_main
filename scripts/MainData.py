import pandas as pd
import numpy as np

from SQL import get_data, ssh_sql_connector
from Processing import add_columns
from Calculate.models import SkellamDistribution

# from Calculate import Models


class GeneralData:

    def __init__(self, seasons):
        self.SQL = ssh_sql_connector.SQL_connector()
        self.seasons: list = seasons
        self.fixtures_data = self.fixture_data()

    def standigs_data(self) -> pd.DataFrame:
        data_list = []
        for season in self.seasons:
            df = get_data.get_standings_data(sqlengine=self.SQL, season=season)
            df = add_columns.add_average_goals(df=df)
            data_list.append(df)

        dff = pd.concat(data_list)
        return dff

    def fixture_data(self) -> pd.DataFrame:
        df: pd.DataFrame = get_data.get_fixtures_data(sqlengine=self.SQL)
        dff = df.loc[df["league_season"].isin(self.seasons)]
        dff = add_columns.add_goals_string_result(dff)

        return dff

    def expand_data_by_model(self, model):
        """skellam"""
        fixtures = self.fixtures_data
        leagues = set(fixtures["league_name"])
        seasons = set(fixtures["league_season"])
        zero_inf_values = np.arange(0, 0.21, 0.01).tolist()
        dff = []
        for season in seasons:
            for league in leagues:
                for z in zero_inf_values:
                    print(season, league, z)
                    selectet_model = model(
                        data=fixtures, zero_inf=float(z), season=season, league=league
                    )
                    df = selectet_model.create_result_data()
                    df["zero_inf_koef"] = z
                    df["league"] = league
                    df["season"] = season
                    dff.append(df)
        data_csv: pd.DataFrame = pd.concat(dff)
        return data_csv


if "__main__" == __name__:
    data_object = GeneralData(seasons=[2020, 2021, 2022])
