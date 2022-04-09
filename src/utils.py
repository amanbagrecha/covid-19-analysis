
import numpy as np
import glob
import pandas as pd
import os
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.formula.api import ols
import xarray as xr


def s5p_no2_stat(df, vardep, st_yr, end_yr, confInt):
    # Ordinary Least Squares (OLS) model
    # compute F statistic and perform one-way anova for all three years
    model = ols(f"{vardep} ~ year_class", data=df.dropna()).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    st_idx = df.loc[df.year_class == st_yr, [f"{vardep}", "mm-dd"]].set_index("mm-dd")
    end_idx = df.loc[df.year_class == end_yr, [f"{vardep}", "mm-dd"]].set_index("mm-dd")
    data = st_idx - end_idx
    data = data.dropna()[f"{vardep}"]
    conf_interval = st.t.interval(alpha=confInt, df=len(data)-1, loc=np.mean(data), scale=st.sem(data))  # or st.norm.interval(alpha=0.99, loc=np.mean(data), scale=st.sem(data))

    if anova_table.loc['year_class', 'PR(>F)' ] < 0.01:
        return True, (data.mean(), conf_interval)
    print("Result not significant. Exiting!")
    return False, ()

def read_chirps():
    # read all files in the directory for rainfall
    rainfall_files = glob.glob(os.path.join(os.pardir, "assets", "rainfall", "*.csv"))
    c_df = [pd.read_csv(i, parse_dates=["time"]).set_index("time") for i in rainfall_files]
    df_rainfall = pd.concat(c_df)

    return df_rainfall

def read_2mtemp():

    _coords = (12.9716, 77.59) # Bengaluru coords
    path_2tmp =  os.path.join(os.pardir, 'assets', '2m_temp')
    ds = xr.open_dataset(os.path.join(path_2tmp, "2mtemperature.nc"))
    ds = ds.sel(longitude=_coords[0], latitude=_coords[1], method='nearest')
    ds = ds.to_dataframe()
    ds.index = ds.index.date
    return ds