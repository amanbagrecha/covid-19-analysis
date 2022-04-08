
import numpy as np
import glob
import pandas as pd
import os
import scipy.stats as st
import statsmodels.api as sm
from statsmodels.formula.api import ols



def s5p_no2_stat(df, vardep, st_yr, end_yr, confInt):
    # Ordinary Least Squares (OLS) model
    model = ols(f"{vardep} ~ year_class", data=df.dropna()).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)

    st_idx = df.loc[df.year_class == st_yr, [f"{vardep}", "mm-dd"]].set_index("mm-dd")
    end_idx = df.loc[df.year_class == end_yr, [f"{vardep}", "mm-dd"]].set_index("mm-dd")
    data = st_idx - end_idx
    data = data.dropna()[f"{vardep}"]
    conf_int = st.t.interval(
        alpha=confInt, df=len(data) - 1, loc=np.mean(data), scale=st.sem(data)
    )
    print('############################################################')
    print(f"Mean= {data.mean():.4}; conf_interval = {conf_int}")
    print(f"ANOVA table: {anova_table}")
    return None


def read_chirps():
    # read all files in the directory for rainfall
    rainfall_files = glob.glob(os.path.join(os.pardir, "assets", "rainfall", "*.csv"))
    c_df = [pd.read_csv(i, parse_dates=["time"]).set_index("time") for i in rainfall_files]
    df_rainfall = pd.concat(c_df)

    return df_rainfall