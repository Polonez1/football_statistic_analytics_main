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


if "__main__" == __name__:
    data = GeneralData(seasons=[2020, 2021, 2022])
    df = data.fixture_data()

    skellam = SkellamDistribution(data=df)
    dff = skellam.create_windrawloss_data()

    print(dff)
