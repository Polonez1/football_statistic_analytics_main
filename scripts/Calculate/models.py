# from Calculate.PoissonDistribution import poisson_dist
# from Calculate.ModelsDataProcessing import skellam_processing
from Calculate.PoissonDistribution.skellam_dist_model import SkellamProccesing
import pandas as pd
import numpy as np


class SkellamDistribution(SkellamProccesing):

    def __init__(self, data: pd.DataFrame, season: int = None, league: str = None):
        super().__init__(data, season, league)

    def skellam_matrix(self):
        return super().skellam_matrix()

    def create_result_data(self) -> pd.DataFrame:
        return super().create_result_data()

    def create_windrawloss_data(self):
        return super().create_windrawloss_data()

    def create_overunder_data(self):
        return super().create_overunder_data()
