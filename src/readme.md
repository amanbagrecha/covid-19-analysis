# How to navigate the code

```python
.
├── dl_2m_temp.py # download 2m temperature from era-5
├── dl_landsat_lst.py # donwload landsat 8 from earth engine
├── dl_rainfall.py # read rainfall from downloaded files
├── dl_rainfall.sh # download data from CHIRPS
├── main.ipynb # analysis and visualization code 
├── readme.md # header
├── sts_grd_aqi.py # executable to perform statistical analysis on AQI
├── sts_s5p_no2.py # executable to perform statistical analysis on NO2 from S5P
├── sts_temp.py # executable to perform statistical analysis on AT and LST
├── test.py # TO-DO write tests
└── utils.py # utility module to import in various scripts
```


Sentinel 5P data is downloaded from earth engine, the script for which can be found [here](https://code.earthengine.google.com/6406ab577a713ae7beaee05a7e550cc2)
MODIS Time Series data is downloaded from earth engine, the script for which can be found [here](https://code.earthengine.google.com/4e83ce0c942dbd0e320ae794be14d264)