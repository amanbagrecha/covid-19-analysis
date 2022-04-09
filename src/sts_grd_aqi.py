import pandas as pd
import numpy as np
import glob
from utils import read_chirps, s5p_no2_stat
import os
from statsmodels.stats.multicomp import MultiComparison

def formatdf(df):

    dfa = df.loc[df.iloc[:, 0] == "From Date"]
    df = df.iloc[dfa.index[0] :, :]
    df, df.columns = df[1:], df.iloc[0]
    df = df.drop("To Date", axis=1)
    dfc = df.loc[dfa.index[1] :].copy()
    dfc, dfc.columns = dfc[1:], dfc.iloc[0]
    dfc = dfc.dropna(axis=1, how="all")
    dfd = df.loc[df.iloc[:, 0].isnull() == True].index[0]
    dfe = df.loc[: dfd - 1]
    dff = dfe.merge(dfc, on="From Date", how="outer")
    dff["_index"] = pd.to_datetime(dff["From Date"], format="%d-%m-%Y %H:%M")
    dff = dff.replace({"None": np.nan})
    dff = dff.dropna(axis =1, how="all")
    dff = dff.drop("From Date", axis=1)
    return dff


atm = {
    "PM2.5": [30, 60, 90, 120, 250],
    "PM10": [50, 100, 250, 350, 430],
    "NO2": [40, 80, 180, 280, 400],
    "NH3": [200, 400, 800, 1200, 1800],
    "NOx": [40, 80, 180, 280, 400],
    "Ozone": [50, 100, 168, 208, 748],
    "CO": [1, 2, 10, 17, 34],
    "SO2": [40, 80, 380, 800, 1600],
}


def roundoff(func):
    def wrapper(*args, **kwargs):
        return np.rint(func(*args, **kwargs))

    return wrapper


@roundoff
def sub_index(a, b):
    if a <= b[0]:
        return a * 50 / b[0]
    elif a > b[0] and a <= b[1]:
        return 50 + (a - b[0]) * 50 / (b[1] - b[0])
    elif a > b[1] and a <= b[2]:
        return 100 + (a - b[1]) * 100 / (b[2] - b[1])
    elif a > b[2] and a <= b[3]:
        return 200 + (a - b[2]) * 100 / (b[3] - b[2])
    elif a > b[3] and a <= b[4]:
        return 300 + (a - b[3]) * 100 / (b[4] - b[3])
    elif a > b[4]:
        return 400 + (a - b[4]) * 100 / (b[4] - b[3])
    else:
        return np.nan


def aqi(row):
    mylist = [sub_index(row[i], atm[i]) for i in column_list if i != "NO"]
    return max(mylist)


if __name__=='__main__':

    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)
    
    # read ground aqi data
    path_assets = os.path.join(os.pardir, 'assets', 'grd_aqi')
    confInt = 0.99
    # air quality ground station
    c_df = [formatdf(pd.read_excel(i)) for i in glob.glob(os.path.join(path_assets, "*.xlsx"))]
    df_aqi = pd.concat(c_df).set_index("_index")
    column_list = df_aqi.columns
    df_aqi["AQI"] = df_aqi.apply(lambda row: aqi(row), axis=1)
    df_aqi.index.name = None
    df_aqi["mm-dd"] = df_aqi.index.strftime("%m-%d")

    # read rainfall
    df_rainfall = read_chirps()

    # Join rainfall and ground station air quality data
    df_anlys = df_rainfall.join(df_aqi, how="inner")
    df_anlys = df_anlys.loc[df_anlys.precip < 5]


    # add unique id for statistical analysis
    for year in [2019, 2020, 2021]:
        df_anlys.loc[f"{year}-03-24":f"{year}-05-30", "year_class"] = str(year)

    # perform one-way anova
    anova_bool, mean_conf = s5p_no2_stat(df_anlys, "AQI", "2019", "2020", confInt=confInt)

    # if null hypothesis is rejected, perform pairwise tukey-hsd
    if anova_bool:    
        # perform tuckey test
        df_tukey = df_anlys.dropna()
        mc = MultiComparison(df_tukey['AQI'], df_tukey['year_class'])
        print(mc.tukeyhsd(1- confInt).summary())
        
        print(mean_conf)