import pandas as pd


class Handy:

    def create_sample_df(self):
        df = pd.read_csv('../data/sample_df.csv')
        return df
