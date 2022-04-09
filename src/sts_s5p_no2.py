# perform statistical analysis on s5p no2 data

import pandas as pd
import glob
import os
from utils import s5p_no2_stat, read_chirps

def formatter(filepath):
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df = df.drop(["system:index", ".geo"], axis=1)
    df["tropospheric_NO2_column_number_density"] = (
        df["tropospheric_NO2_column_number_density"] * 1e6
    )
    df.rename(columns={"tropospheric_NO2_column_number_density": "T_NO2"}, inplace=True)
    df = df.set_index("date")
    return df


# read all files in the directory for no2
c_df = [formatter(i) for i in glob.glob("*.csv")]
df_no2 = pd.concat(c_df)
df_no2.index.name = None
df_no2["mm-dd"] = df_no2.index.strftime("%m-%d")

# unique column `year class` to assign values to during covid period

# rainfall 
df_rainfall = read_chirps()

# Join rainfall and satellite NO2 data; remove high intensity rainfall
df_merge = df_rainfall.join(df_no2, how="inner")
df_merge = df_merge.loc[df_merge.precip < 5]

for year in [2019, 2020, 2021]:
    df_merge.loc[f"{year}-03-24":f"{year}-05-30", "year_class"] = str(
        year
    )

s5p_no2_stat(df_merge, "T_NO2", "2019", "2020", 0.99)
