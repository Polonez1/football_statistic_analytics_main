from PoissonDistribution import poisson_dist

import pandas as pd


class SkellamDistribution:

    def __init__(self, data: pd.DataFrame, season: int = None, league: str = None):
        self.data = data
        self.league = league
        self.season = season

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
