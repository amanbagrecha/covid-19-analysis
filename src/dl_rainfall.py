import xarray as xr
import os

class readCHIRPS:
  def __init__(self, year, coords, find_path):
    self.year = year
    self.lon = coords[0]
    self.lat = coords[1]
    self.findpath = find_path
  
  def slice_netCDF(self, find_path):
    
    file_path = os.path.join(find_path , f"{self.year}.nc")
    if not os.path.exists(file_path):
      raise Exception(f"{file_path} does not exists")
    
    al_year =  xr.open_dataset()
    lat_lon = al_year.sel( latitude = self.lat, longitude = self.lon, method='nearest')\
                   .sel(time = slice(f"{self.year}-01-01", f"{self.year}-06-30"))

    return lat_lon
  
  def save_netCDF(self, save_path):
    lat_lon = self.slice_netCDF(self.findpath)
    re_df = lat_lon.to_dataframe().reset_index()
    
    save_loc = os.path.join(save_path, f'rainfall_{self.year}.csv')
    if not os.path.exists(save_loc):         
        re_df.to_csv(save_loc, index=False)
    return None

if __name__=='__main__':

    dirname = os.path.dirname(os.path.abspath(__file__))
    os.chdir(dirname)
    
    _range = (2019, 2022) # year we want to read data
    _coords = (77.59, 12.9716) # Bengaluru coords
    path_rainfall = os.path.join(os.pardir, 'tmp')
    path_assets = os.path.join(os.pardir, 'assets', 'rainfall')
    
    if not os.path.exists(path_rainfall):
        raise Exception(f"path {path_rainfall} does not exist")
    if not os.path.exists(path_assets):
        os.mkdir(path_assets)

    for year in range(*_range):
        dl = readCHIRPS(year, _coords, path_rainfall)
        dl.save_netCDF(path_assets)
    