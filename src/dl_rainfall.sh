#!/bin/bash

# data downloaded from CHIRPS (https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/) 
# as NETCDF file format. Output file name is the year name.

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR 
cd ..
mkdir tmp 
cd tmp
echo "Downloading CHIRPS data from CHC website"
curl -o '#1.nc' https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_daily/netcdf/p05/chirps-v2.0.[2018-2021].days_p05.nc
echo "Download complete!"