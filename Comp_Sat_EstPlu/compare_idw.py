#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:38:24 2023

@author: ana.becker
"""
# Funções
#%%
def distance_matrix(x0, y0, x1, y1):
    """ Make a distance matrix between pairwise observations.
    Note: from <http://stackoverflow.com/questions/1871536> 
    """
    
    obs = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T

    d0 = np.subtract.outer(obs[:,0], interp[:,0])
    d1 = np.subtract.outer(obs[:,1], interp[:,1])
    
    # calculate hypotenuse
    return np.hypot(d0, d1)
def simple_idw(x, y, z, xi, yi, power=1):
    """ Simple inverse distance weighted (IDW) interpolation 
    Weights are proportional to the inverse of the distance, so as the distance
    increases, the weights decrease rapidly.
    The rate at which the weights decrease is dependent on the value of power.
    As power increases, the weights for distant points decrease rapidly.
    """
    
    dist = distance_matrix(x,y, xi,yi)

    # In IDW, weights are 1 / distance
    weights = 1.0/(dist+1e-12)**power

    # Make weights sum to one
    weights /= weights.sum(axis=0)

    # Multiply the weights for each interpolated point by all observed Z-values
    return np.dot(weights.T, z)

# Dados do satélite
#%%



times = xr.open_dataset('data/dados-processados/gsmap-nrt/201901.nc').time.to_dataframe().reset_index(drop=True)
f = 'data/dados-processados/gsmap-nrt/201901.nc'


# Realiza a leitura dos diversos arquivos .nc tendo como argumento o diretório e salva como csv
# def read_nc (path):
#     nc_files = glob.glob(os.path.join(path,"*.nc"))
#     df_file = pd.DataFrame()
psat = pd.DataFrame()
      
#     for i in range(len(times)):
#         print('time '+ str(times.time[i]) )
#         for f in nc_files:
            #poc
xr_nc = xr.open_dataset(f).prate.to_dataframe().reset_index()
df_time = xr_nc.loc[xr_nc['time'] == times.time[40]]  
df_file = pd.concat([df_file,df_time])
psat = pd.concat([psat,df_file])
    
    
#read_nc('data/dados-processados/gsmap-now')
#read_nc('data/dados-processados/gsmap-nrt')






    
    
x = psat.lon
y = psat.lat
z = psat.prate
xi = psat.lon.unique()
yi = psat.lat.unique()


nx, ny = psat.lon.nunique(), psat.lat.nunique() 
xi = np.linspace(x.min(), x.max(), nx)
yi = np.linspace(y.min(), y.max(), ny)

# generate grid 
xi, yi = np.meshgrid(xi, yi)

# colapse grid into 1D
xi, yi = xi.flatten(), yi.flatten()

# Calculate IDW
grid1 = simple_idw(x, y, z, xi, yi, power=2)
grid1 = grid1.reshape((ny, nx))

plt.figure(figsize=(15,10))
plt.imshow(
    grid1,
    extent=(x.min(), x.max(), y.min(), y.max()),
    cmap='rainbow',
    #interpolation='gaussian',
    origin="lower")
plt.colorbar()
plt.title("")




# Dados do Simepar
#%%


############ Estações do simepar ############
sim = pd.read_csv('data/estacoes.csv')[['codigo','latitude','longitude']]
sim.reset_index(drop=True, inplace=True)


path = os.getcwd()+'/data/Chuvas-simepar'
csv_files = glob.glob(os.path.join(path, "*.csv"))
psim = pd.DataFrame()
for f in csv_files:
    df_est = pd.read_csv(f)
    df_est['codigo'] = f.split("/")[-1].split("_")[0]
    psim = pd.concat([psim,df_est])    
psim['codigo'] = psim['codigo'].astype(int)


psim = psim.set_index('codigo').join(sim.set_index('codigo'), on='codigo', how='left')
psim.reset_index(inplace=True)


for i in range(len(times)):
    psim_i = psim[psim['datahora']==psim['datahora'][i]]
    x = psim_i.longitude
    y = psim_i.latitude
    z = psim_i.chuva_mm
    xi = psat.lon.unique()
    yi = psat.lat.unique()
    
    nx, ny = psat.lon.nunique(), psat.lat.nunique() 
    xi = np.linspace(x.min(), x.max(), nx)
    yi = np.linspace(y.min(), y.max(), ny)
    
    # generate grid 
    xi, yi = np.meshgrid(xi, yi)
    
    # colapse grid into 1D
    xi, yi = xi.flatten(), yi.flatten()
    
    # Calculate IDW
    grid2 = simple_idw(x, y, z, xi, yi, power=2)
    grid2 = grid2.reshape((ny, nx))
    
    plt.figure(figsize=(15,10))
    plt.imshow(
        grid2,
        extent=(x.min(), x.max(), y.min(), y.max()),
        cmap='rainbow',
        #interpolation='gaussian',
        origin="lower")
    plt.colorbar()


(grid1-grid2).max()


plt.figure(figsize=(15,10))
plt.imshow(
    grid1-grid2,
    extent=(x.min(), x.max(), y.min(), y.max()),
    cmap='rainbow',
    interpolation='gaussian',
    origin="lower")
plt.colorbar()