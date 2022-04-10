import cdsapi
import os

if __name__ == '__main__':
    
    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)
    path_2tmp = os.path.join(os.pardir, 'assets', '2m_temp')
    
    if not os.path.exists(path_2tmp):
        os.mkdir(path_2tmp)
    
    c = cdsapi.Client()
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
            'time': '05:00',
            'area': [
                14, 77, 12,
                79,
            ],
        },
        os.path.join(path_2tmp, '2mtemperature.nc'))