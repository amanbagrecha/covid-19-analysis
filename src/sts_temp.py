import pandas as pd
import numpy as np
import glob
import os
from statsmodels.stats.multicomp import MultiComparison

from utils import read_chirps, s5p_no2_stat, read_2mtemp


# LAND SURFACE TEMPERATURE FILES READING...
def formatter(filepath):
    df = pd.read_csv(filepath, parse_dates=["date"]).set_index("date")
    df["ST_B10_mean"] = df["ST_B10_mean"].replace({-9999: np.nan})
    df = df.drop(["system:index", ".geo"], axis=1)
    df["mm-dd"] = df.index.strftime("%m-%d")
    return df


class StatisticalTest:
    def __init__(self, param, st_year, ed_year, confInt=0.99) -> None:
        self.param = param
        self.styear = st_year
        self.edyear = ed_year
        self.confInt = confInt

    def anova_test(self, df):
        return s5p_no2_stat(
            df, self.param, self.styear, self.edyear, confInt=confInt
        )

    def tukey_test(self, df):
        # if null hypothesis is rejected, perform pairwise tukey-hsd
        anova_bool, mean_conf = self.anova_test(df)
        if anova_bool:
            df_tukey = df.dropna()
            mc = MultiComparison(df_tukey[self.param], df_tukey["year_class"])
            print(mc.tukeyhsd(1 - self.confInt).summary())
            print(mean_conf)
            return None
        print("Null hypothesis is accepted, no need to perform pairwise tukey-hsd")
        return None


if __name__ == "__main__":

    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)

    # read ground aqi data
    path_2temp = os.path.join(os.pardir, "assets", "2m_temp")
    path_lst = os.path.join(os.pardir, "assets", "modis_lst")
    confInt = 0.99

    # LAND SURFACE TEMPERATURE FILES READING
    c_df = [formatter(i) for i in glob.glob(os.path.join(path_lst, "*.csv"))]
    df_lst = pd.concat(c_df)

    # AIR TEMPERATURE FILES READING...
    df_2temp = read_2mtemp()
    # RAINFALL FILES READING...
    df_rainfall = read_chirps()

    df_join = df_rainfall[["precip"]].join(df_2temp).join(df_lst)
    df_join["precip_past"] = df_join["precip"].shift(1)
    df_join["precip_past2"] = df_join["precip"].shift(2)

    df_anlys = df_join.loc[
        (df_join.precip < 5) & (df_join.precip_past < 5) & (df_join.precip_past2 < 5)
    ]

    for year in [2019, 2020, 2021]:
        df_anlys.loc[f"{year}-03-24":f"{year}-05-30", "year_class"] = str(year)

    for param in ["t2m", "ST_B10_mean"]:
        myobj = StatisticalTest(param, '2019', '2021', confInt)
        myobj.tukey_test(df_anlys)