import cdsapi
import os
import xarray as xr


c = cdsapi.Client()
save_path = os.path.join(os.pardir, 'tmp')
c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            '2m_temperature'
        ],
        'year': ['2019', '2020', '2021'],
        'month': ['01', '02', '03', '04', '05', '06'],
        'day': [
            '01', '02', '03',
            '04', '05', '06',
            '07', '08', '09',
            '10', '11', '12',
            '13', '14', '15',
            '16', '17', '18',
            '19', '20', '21',
            '22', '23', '24',
            '25', '26', '27',
            '28', '29', '30',
        ],
        'time': '12:00',
        'area': [
            14, 77, 12,
            79,
        ],
    },
    os.path.join(save_path, '2mtemperature.nc'))


if __name__ == '__main__':
    
    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)
    
    _coords = (12.9716, 77.59) # Bengaluru coords
    
    path_2tmp = os.path.join(os.pardir, 'tmp')
    path_assets = os.path.join(os.pardir, 'assets', '2m_temp')
    ds = xr.open_dataset(os.path.join(path_2tmp, "./2mtemperature.nc"))
    ds = ds.sel(longitude=_coords[0], latitude=_coords[1], method='nearest')
    ds = ds.to_dataframe()
    ds.index = ds.index.date

    if not os.path.exists(path_assets):
        os.mkdir(path_assets)

    ds.to_csv(os.path.join(save_path , "2mtemperature.csv"))