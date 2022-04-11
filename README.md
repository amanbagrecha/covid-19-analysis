# Temporal Analysis of Covid-19 and its Impact on Environment 

Analysing imapact of covid-19 on air quality and land temperature using satellite data.

Solution document can be found [here](https://www.notion.so/Spatio-Temporal-Analysis-of-Covid-19-on-Environment-4f3e688110564e3cb59fd7d2cc710789)

## Objective
We investigate and quantify changes in pollutant and aerosol (NO2) levels across Bengaluru, India as a result of covid-19 lockdown and also perceive implications of reduced emissions. Further investigate if changes in atmospheric pollutant have impacted temperature. To do so, we would compare and contrast ground measurements and remotely sensed observations between March 2020 - May 2020 with those over the same months in 2019 and 2021.

![temporal-analyis-Page-2 drawio_](https://user-images.githubusercontent.com/76432265/162664595-33577437-8e0e-4ac9-949a-5d096eb67523.svg)


## Variables investigated

- Air
- Temperature
- Rainfall

## Key outcomes

- Air quality improved as a result of the lockdown. Moreover the effect seems to have lasted for another year.
- Year 2021 was cooler than 2020 and 2019 as consequence of pandemic.
- Near identical condition are necessary to ascertain the difference in various atmospheric parameter are not a coincidence but in fact because of decline in anthropogenic activity during lockdown. To ascertain this, we undertake measures to control for precipitation.
- In case of LST,  a single point statistic cannot be representative of entire region due to natural variability.

## documents
- [analysis code](https://github.com/amanbagrecha/covid-19-analysis/blob/main/src/main.ipynb)
- [summary document](https://www.notion.so/Summary-15e874544bb9478a8273529882e5e5b5)
- [solution document](https://www.notion.so/Temporal-Analysis-of-Covid-19-and-its-Impact-on-Environment-4f3e688110564e3cb59fd7d2cc710789)

## 🛠️ Dataset in use
- [CPCB](https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/data) **—** Daily Air Quality data for Silk Board Station
- [CHIRPS](https://chc.ucsb.edu/data/chirps) - Daily Rainfall data at 5566m resolution
- [Sentinel-5P TROPOMI NO2](https://sentinel.esa.int/de/web/sentinel/user-guides/sentinel-5p-tropomi)   **—** Daily Tropospheric vertical column NO2  data at 7 x 3.5km resolution
- [MODIS LST product MOD11A1](https://lpdaac.usgs.gov/products/mod11a1v061/) **—** Daily Land Surface Temperature at 1km  resolution
- [Landsat 8 Collection 2 Level 2](https://www.usgs.gov/landsat-missions/landsat-collection-2-level-2-science-products) **—** 16-day Land Surface Temperature at 30m resolution
- [ERA-5 Single Level 2-m Temperature](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview) - Hourly 2m  Air Temperature at 0.25° resolution

## 🏁 Libraries in use
- statsmodel
- pandas, geopandas
- numpy
- matplotlib, seaborn
 - rasterio, xarray

# 📋 Further modification that can be done.
- Use of Air temperature measurement (from IMD AWS) to quantify the relationship with satellite based measurements.
- Look at traffic condition (number of accidents reported, number of vehicle purchases) or noise pollution levels as a result of drop in air quality. Verify if cause of air/noise pollution is traffic or industry or something else.
- Control for other meteorological parameters: fires, storm.
- Model ground-measurements (AQI) with satellite data to provide insights at higher spatial and temporal resolution.

