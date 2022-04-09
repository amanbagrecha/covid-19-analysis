# perform statistical analysis on s5p no2 data

import pandas as pd
import glob
from utils import read_chirps, StatisticalTest
import os


def formatter(filepath):
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df = df.drop(["system:index", ".geo"], axis=1)
    df["tropospheric_NO2_column_number_density"] = (
        df["tropospheric_NO2_column_number_density"] * 1e6
    )
    df.rename(columns={"tropospheric_NO2_column_number_density": "T_NO2"}, inplace=True)
    df = df.set_index("date")
    df["mm-dd"] = df.index.strftime("%m-%d")
    return df


if __name__ == "__main__":

    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)

    # read ground aqi data
    path_assets = os.path.join(os.pardir, "assets", "sat_no2_blr")
    sigLevel = 0.01

    # read all files in the directory for no2
    c_df = [formatter(i) for i in glob.glob(os.path.join(path_assets, "*.csv"))]
    df_no2 = pd.concat(c_df)
    # df_no2.index.name = None

    # rainfall
    df_rainfall = read_chirps()

    # Join rainfall and satellite NO2 data; remove high intensity rainfall
    df_merge = df_rainfall.join(df_no2, how="inner")
    df_merge = df_merge.loc[df_merge.precip < 5]

    # unique column `year class` to assign values to during covid period
    for year in [2019, 2020, 2021]:
        df_merge.loc[f"{year}-03-24":f"{year}-05-30", "year_class"] = str(year)

    for param in ["T_NO2"]:
        print(f"statistical analyis for param: {param}")
        myobj = StatisticalTest(param, sigLevel)
        myobj.tukey_test(df_merge)
