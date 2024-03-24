import pandas as pd


from SQL import get_data, ssh_sql_connector
from Processing import add_columns
from Calculate.models import SkellamDistribution

# from Calculate import Models


class GeneralData:

    def __init__(self, seasons):
        self.SQL = ssh_sql_connector.SQL_connector()
        self.seasons: list = seasons

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

    def expand_result_data_by_model(self, model: object) -> pd.DataFrame:
        """_summary_

        Args:
            model (str): SkellamDist
        """
        df = model.data
        leagues = set(df["league_name"])
        seasons = set(df["league_season"])

        data = []
        for league in leagues:
            for season in seasons:
                model_select = model
                dff = model_select.create_result_data()
                dff["league"] = league
                dff["season"] = season
                data.append(dff)

        return pd.concat(data)


if "__main__" == __name__:
    data = GeneralData(seasons=[2020, 2021, 2022])
    df = data.fixture_data()

    model = SkellamDistribution(data=df, zero_inf=0.05)
    df = data.expand_result_data_by_model(model=model)

    # df = data.expand_result_data_by_model(model="SkellamDist")

    # df.to_csv("data.csv")
    # print(df)
