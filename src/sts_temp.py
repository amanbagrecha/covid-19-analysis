import pandas as pd
import numpy as np
import glob
import os

from utils import read_chirps, StatisticalTest, read_2mtemp
pd.options.mode.chained_assignment = None 


# LAND SURFACE TEMPERATURE FILES READING...
def formatter(filepath):
    df = pd.read_csv(filepath)
    df.index = pd.to_datetime(df['date'], format = '%d-%m-%Y')
    df.loc[:,"ST_B10_mean"] = df["ST_B10_mean"].replace({-9999: np.nan})
    df = df.drop(["system:index", ".geo", "date", "ST_B10_min", "ST_B10_max"], axis=1)
    df.loc[:, "mm-dd"] = df.index.strftime("%m-%d")
    return df


if __name__ == "__main__":

    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)

    # read ground aqi data
    path_2temp = os.path.join(os.pardir, "assets", "2m_temp")
    path_lst = os.path.join(os.pardir, "assets", "modis_lst")
    sigLevel = 0.01

    # LAND SURFACE TEMPERATURE FILES READING
    c_df = [formatter(i) for i in glob.glob(os.path.join(path_lst, "*.csv"))]
    df_lst = pd.concat(c_df)

    # AIR TEMPERATURE FILES READING...
    df_2temp = read_2mtemp()
    # RAINFALL FILES READING...
    df_rainfall = read_chirps()

    df_join = df_rainfall[["precip"]].join(df_2temp).join(df_lst)
    df_join.loc[:,"precip_past"] = df_join["precip"].shift(1)
    df_join.loc[:,"precip_past2"] = df_join["precip"].shift(2)

    df_anlys = df_join.loc[
        (df_join.precip < 5) & (df_join.precip_past < 5)# & (df_join.precip_past2 < 5)
    ]

    # covid-19 timeframe is from mar 24 to may 30
    for year in [2019, 2020, 2021]:
        df_anlys.loc[f"{year}-03-24":f"{year}-05-30", "year_class"] = str(year)

    for param in ["t2m", "ST_B10_mean"]:
        print(f"statistical analyis for param: {param}")
        myobj = StatisticalTest(param, sigLevel)
        myobj.tukey_test(df_anlys)
        