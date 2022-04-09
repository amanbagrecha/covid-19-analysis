import glob
import pandas as pd
import os
import statsmodels.api as sm
from statsmodels.formula.api import ols
import xarray as xr
from statsmodels.stats.multicomp import MultiComparison


class StatisticalTest:
    """
    param: parameter which needs to be tested (statistically)
    sigLevel: significance level for analysis
    
    =========================================
    This class is used to perform statistical test
    we perform one-way anova for 2019-2021 data
    if the p-value is less than the significance level, 
    we reject the null hypothesis, and perform tukey test
    =========================================
    """
    
    def __init__(self, param, sigLevel=0.01) -> None:
        self.param = param
        self.sigLevel = sigLevel

    def printer(self, anova_table):
        print("=" * 50)
        print(anova_table)
        print("=" * 50)
        if anova_table.loc["year_class", "PR(>F)"] < self.sigLevel:
            return True
        print("Results not significant. Accept null hypothesis!")
        return False

    def anova_test(self, df):
        # Ordinary Least Squares (OLS) model
        # compute F statistic and perform one-way anova for all three years
        df = df.dropna(subset=[self.param, "year_class"])
        model = ols(f"{self.param} ~ year_class", data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=1)
        return self.printer(anova_table)

    def tukey_test(self, df):
        # if null hypothesis is rejected, perform pairwise tukey-hsd
        anova_bool = self.anova_test(df)
        if anova_bool:
            df = df.dropna(subset=["year_class", self.param])
            mc = MultiComparison(df[self.param], df["year_class"])
            print(mc.tukeyhsd(self.sigLevel).summary())

            return None

        return None

def read_chirps():
    # read all files in the directory for rainfall
    rainfall_files = glob.glob(os.path.join(os.pardir, "assets", "rainfall", "*.csv"))
    c_df = [
        pd.read_csv(i, parse_dates=["time"]).set_index("time") for i in rainfall_files
    ]
    df_rainfall = pd.concat(c_df)
    return df_rainfall


def read_2mtemp():

    _coords = (77.59, 12.9716)  # Bengaluru coords
    path_2tmp = os.path.join(os.pardir, "assets", "2m_temp")
    ds = xr.open_dataset(os.path.join(path_2tmp, "2mtemperature.nc"))
    ds = ds.sel(longitude=_coords[0], latitude=_coords[1], method="nearest")
    ds = ds.to_dataframe()
    ds.index = ds.index.date
    return ds