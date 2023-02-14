'''
Created by Arlan Scortegagna, jan/2022
Process operational realtime archives from JAXA'S FTP (/now)
Crops interest area and save them into NetCDF format
'''

#%%
from multiprocessing import Pool, cpu_count
import pandas as pd
import xarray as xr
import gzip
import glob
import numpy as np
from functools import partial
import time


#%%
lat = np.arange(59.95, -60.00, -0.1)
lon = np.arange(0.05, 360, 0.1)
def converte_gsmap_now(arq_nome, lat_min, lat_max, lon_min, lon_max):
    f = gzip.GzipFile(arq_nome)
    data = np.frombuffer(f.read(), dtype=np.float32).reshape([1200, 3600, 1])
    date = arq_nome.split('/')[-1].split('.')[1]
    hour = arq_nome.split('/')[-1].split('.')[2]
    time = pd.to_datetime(f'{date}{hour}')
    da = xr.DataArray(
        data = data,
        dims = ['lat', 'lon', 'time'],
        coords = [lat, lon, [time]],
        name = 'prate',
        )
    da['lon'] = da['lon'] - 360
    mask_lat = (da.lat >= lat_min) & (da.lat <= lat_max)
    mask_lon = (da.lon >= lon_min) & (da.lon <= lon_max)
    da_interesse = da.where(mask_lat & mask_lon, drop=True)
    # da_interesse = da.sel(lat=slice(lat_min, lat_max), lon=slice(lon_min, lon_max)) nao funciona pois lat eh descrente
    return da_interesse


#%%
if __name__ == '__main__':
    
    #%% Area de interesse
    lat_min = -28
    lat_max = -21
    lon_min = -56
    lon_max = -46
    
    periodos = pd.period_range('2022-12', '2022-12', freq='M')
    
    for periodo in periodos:
        print(f'Processando {periodo}')
        
        tc_ini = time.time()
        
        arqs = glob.glob(f'dados-brutos/now/half_hour/{periodo.year}/{periodo.month:02d}/**/*.gz', recursive=True)
        
        arq_nome = arqs[0]
        
        n = cpu_count()
        pool = Pool(cpu_count())
        funcao = partial(converte_gsmap_now, lat_min=lat_min, lat_max=lat_max, lon_min=lon_min, lon_max=lon_max)
        das = pool.map(funcao, arqs)
        da = xr.concat(das, dim='time').sortby('time')
        da.to_netcdf(f'dados-processados/{periodo.year}{periodo.month:02d}.nc')

        tc_fim = time.time()