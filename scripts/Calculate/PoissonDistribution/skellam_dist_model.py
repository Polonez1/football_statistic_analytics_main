from Calculate.PoissonDistribution import poisson_dist
from Calculate.ModelsDataProcessing import skellam_processing

import pandas as pd
import numpy as np


class SkellamProccesing:

    def __init__(self, data: pd.DataFrame, season: int = None, league: str = None):
        self.league = league
        self.season = season
        self.data = data

        if season is not None:
            self.__filter_by_season()
        if league is not None:
            self.__filter_by_league()

        self.averages = self.__get_averages()
        self.model_params = self.__skellam_params()

    def __filter_by_season(self):
        if self.season is not None:
            self.data = self.data[self.data["league_season"] == self.season]

    def __filter_by_league(self):
        if self.league is not None:
            self.data = self.data[self.data["league_name"] == self.league]

    def __get_averages(self):
        df_agg = self.data.agg(
            {
                "fixture_id": "count",
                "goals_home": "mean",
                "goals_away": "mean",
            }
        )
        return df_agg

    def __skellam_params(self):
        season = self.season
        league = self.league
        averages_copy = self.averages.copy()
        avg_1 = round(averages_copy["goals_home"], 2)
        avg_2 = round(averages_copy["goals_away"], 2)
        total = int(averages_copy["fixture_id"])

        return {
            "avg1": avg_1,
            "avg2": avg_2,
            "total": total,
            "season": season,
            "league": league,
        }

    def __skellam_distribution_data(self):
        skellam_dist = poisson_dist.results_distribution_by_skellam(
            avg_1=self.averages["goals_home"],
            avg_2=self.averages["goals_away"],
            total=self.averages["fixture_id"],
        )
        skellam_dist = skellam_processing.skellam_dist_processing(skellam_dist)
        return skellam_dist

    def __source_distribution_data(self):
        df = skellam_processing.group_fixture_by_goals(self.data, by=["goals_result"])
        df["source"] = "source"

        return df

    def skellam_matrix(self):
        matrix = poisson_dist.skellam_dist_matrix(
            avg_1=self.averages["goals_home"], avg_2=self.averages["goals_away"]
        )

        return matrix

    def create_result_data(self) -> pd.DataFrame:
        fact = self.__source_distribution_data()
        skellam_dist = self.__skellam_distribution_data()

        dff = pd.concat([fact, skellam_dist])

        return dff

    def __create_source_win_data(self, by: list = ["result"]):
        """creted agg data by matches count

        Args:
            by (list, optional): possible by: result, league_name, league_season. Defaults to ['result'].

        Returns:
            _type_: DataFrame
        """
        df = self.data.groupby(by).size().reset_index(name="count")
        df["source"] = "source"
        return df

    def __create_skellam_win_data(self):
        result_skellam = poisson_dist.result_from_skellam_matrix(
            avg_1=self.averages["goals_home"], avg_2=self.averages["goals_away"]
        )
        result_skellam["count"] = round(
            result_skellam["prb"] * self.averages["fixture_id"], 0
        ).astype("int")
        result_skellam["source"] = "skellam dist"

        return result_skellam[["result", "count", "source"]]

    def create_windrawloss_data(self):
        df1 = self.__create_source_win_data()
        df2 = self.__create_skellam_win_data()
        return pd.concat([df1, df2])

    def __create_overunder_source_data(self, over_under: float = 2.5):
        dff = self.data.copy()
        dff["total"] = dff["goals_home"] + dff["goals_away"]
        dff[f"over_under_{over_under}"] = np.where(
            dff["total"] < over_under, f"under_{over_under}", f"over_{over_under}"
        )
        df = dff.groupby(f"over_under_{over_under}").size().reset_index(name="count")
        df["source"] = "source"
        return df

    def __create_overunder_skellam_data(self, over_under: float = 2.5):
        df = poisson_dist.over_from_skellam_matrix(
            avg_1=self.averages["goals_home"], avg_2=self.averages["goals_away"]
        )
        df["count"] = round(df["prb"] * self.averages["fixture_id"], 0).astype("int")
        df["source"] = "skellam dist"
        df = df.rename(columns={"result": f"over_under_{over_under}"}, inplace=False)

        return df[[f"over_under_{over_under}", "count", "source"]]

    def create_overunder_data(self):
        df1 = self.__create_overunder_source_data()
        df2 = self.__create_overunder_skellam_data()
        return pd.concat([df1, df2])
