from Calculate.PoissonDistribution import poisson_dist
from Calculate.ModelsDataProcessing import skellam_processing

import pandas as pd


class SkellamDistribution:

    def __init__(self, data: pd.DataFrame, season: int = None, league: str = None):
        self.data = data
        self.league = league
        self.season = season
        self.averages = self.__get_averages()
        self.model_params = self.__skellam_params()
        self.SKELLAM_RESULT: pd.DataFrame = self.__skellam_distribution_data()
        self.SOURCE_RESULT: pd.DataFrame = self.__source_distribution_data()
        self.RESULT_DATA: pd.DataFrame = self.__create_full_data()

        if season is not None:
            self.__filter_by_season()
        if league is not None:
            self.__filter_by_league()

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

    def __create_full_data(self):
        fact = self.__source_distribution_data()
        skellam_dist = self.__skellam_distribution_data()

        dff = pd.concat([fact, skellam_dist])

        return dff
