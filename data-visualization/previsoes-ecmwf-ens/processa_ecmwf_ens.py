#%%
import pandas as pd
import xarray  as xr
import glob
import plotly.graph_objects as go


#%% Balsa de Guaratuba
#latitude = -25.86
#longitude = -48.57
#nome = 'Guaratuba'
#emissao = '2022-11-29'

#%% Curitiba 
latitude = -25.4
longitude = -49.2
nome = 'Curitiba'
emissao = '2022-02-17'
dir = '../../temp-data' # Diretorio contendo os gribs da previsao

#%% Processa os arquivos da previsao
l_cf = []
l_pf = []
for arq in glob.glob(f'{dir}/{emissao}/*'):
    print(arq)

    # Membro controle (cf)
    ds = xr.open_dataset(arq, engine='cfgrib', filter_by_keys={'numberOfPoints':7296, 'dataType':'cf'}, backend_kwargs={'indexpath':''})
    da = ds['tp']
    da_xy = da.sel(latitude = latitude, longitude = longitude, method='nearest')
    l_cf.append(da_xy)
    
    # Membros do conjunto (pf)
    ds = xr.open_dataset(arq, engine='cfgrib', filter_by_keys={'numberOfPoints':7296, 'dataType':'pf'}, backend_kwargs={'indexpath':''})
    da = ds['tp']
    da_xy = da.sel(latitude = latitude, longitude = longitude, method='nearest')
    l_pf.append(da_xy)

df_cf = xr.concat(l_cf, 'valid_time').to_dataframe().reset_index()
df_pf = xr.concat(l_pf, 'valid_time').to_dataframe().reset_index()
df = pd.concat([df_cf, df_pf], axis=0).sort_values('valid_time')

df['tp'] = df['tp']*1000
df_pivotado = df.pivot(index='valid_time', columns='number', values='tp').round(1)
df_pivotado.to_csv('dados.csv')

#%%
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_pivotado.index, y=df_pivotado[1], legendgroup='Conjunto', name='Conjunto', line=dict(color='darkgray', width=1)))
for i in range(2, 51):
    fig.add_trace(go.Scatter(x=df_pivotado.index, y=df_pivotado[i], legendgroup='Conjunto', showlegend=False, line=dict(color='darkgray', width=1)))
fig.add_trace(go.Scatter(x=df_pivotado.index, y=df_pivotado[0], name='Controle', legendrank=2, line=dict(color='blue', width=2)))
fig.add_trace(go.Scatter(x=df_pivotado.index, y=df_pivotado.median(axis=1), name='Mediana', legendrank=1, line=dict(color='red', width=2)))
fig.update_layout(
    title = f'Previsão de chuva para {nome} de {df_pivotado.index[0]:%Y-%m-%d %H:%M} a {df_pivotado.index[-1]:%Y-%m-%d %H:%M} emitida em {emissao}',
    width=1400, height=700,
    margin=dict(l=20, r=20, t=50, b=20),
    yaxis = dict(
        title_text = 'Acumulado (mm)'
    ),
    xaxis=dict(
        title_text='Data',
        tickvals=pd.date_range(df_pivotado.index[0], df_pivotado.index[-1], freq='D'),
    )
)
fig.write_html(f'prev_{nome}_{df_pivotado.index[0]:%Y%m%dT%H%M}_{df_pivotado.index[-1]:%Y%m%dT%H%M}.html')
# %%
