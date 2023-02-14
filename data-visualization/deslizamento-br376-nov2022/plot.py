#%%
import aquisicao
import pandas as pd
import plotly.graph_objects as go


# %%
_, _, voc = aquisicao.api_simepar_horaria('2022-11-25T00:00:00', '2022-12-01T00:00:00', [25494905], [7])
_, _, salto = aquisicao.api_simepar_horaria('2022-11-25T00:00:00', '2022-12-01T00:00:00', [25484859], [7])


#%%
voc['datahora'] = pd.to_datetime(voc['datahora'], utc=True) - pd.Timedelta(3, 'H')
voc = pd.Series(index=voc['datahora'].values, data=voc['leitura'].values).sort_index()
voc = voc.loc['2022-11-26':].cumsum()

fig = go.Figure()
fig.add_trace(go.Scatter(x=voc.index, y=voc, line=dict(color='blue', width=1.5), showlegend = False))
fig.add_vline(x=pd.Timestamp('2022-11-28T15:20:00'), line_width=1.5, line_dash="dash", line_color="orange")
fig.add_vline(x=pd.Timestamp('2022-11-28T19:20:00'), line_width=3, line_dash="dash", line_color="red")
fig.add_trace(go.Scatter(
    x=[pd.Timestamp('2022-11-28T13:00:00'), pd.Timestamp('2022-11-28T20:15:00')],
    y=[200, 350],
    mode = "text",
    text=["Início dos deslizamentos - 15:20", "Deslizamento principal - 19:20"],
    textposition=["bottom left", "bottom right"],
    showlegend = False,
))
fig.update_layout(
    title = f'Chuva na Estação do Simepar "Vossoroca" - 15km de distância do acidente',
    width=1400, height=700,
    margin=dict(l=20, r=20, t=50, b=20),
    yaxis = dict(
        title_text = 'Total Acumulado (mm)'
    ),
    xaxis=dict(
        title_text='Data e Hora (BRT)',
        tickvals=pd.date_range('2022-11-26T00:00:00', '2022-12-01T00:00:00', freq='12H'),
    )
)

fig.write_image(f'voc.jpeg')


#%%
salto['datahora'] = pd.to_datetime(salto['datahora'], utc=True) - pd.Timedelta(3, 'H')
salto = pd.Series(index=salto['datahora'].values, data=salto['leitura'].values).sort_index()
salto = salto.loc['2022-11-26':].cumsum()

fig = go.Figure()
fig.add_trace(go.Scatter(x=salto.index, y=salto, line=dict(color='blue', width=1.5), showlegend = False))
fig.add_vline(x=pd.Timestamp('2022-11-28T15:20:00'), line_width=1.5, line_dash="dash", line_color="orange")
fig.add_vline(x=pd.Timestamp('2022-11-28T19:20:00'), line_width=3, line_dash="dash", line_color="red")
fig.add_trace(go.Scatter(
    x=[pd.Timestamp('2022-11-28T13:00:00'), pd.Timestamp('2022-11-28T20:15:00')],
    y=[200, 350],
    mode = "text",
    text=["Início dos deslizamentos - 15:20", "Deslizamento principal - 19:20"],
    textposition=["bottom left", "bottom right"],
    showlegend = False,
))
fig.update_layout(
    title = f'Chuva na Estação do Simepar "Salto do Meio" - 9km de distância do acidente',
    width=1400, height=700,
    margin=dict(l=20, r=20, t=50, b=20),
    yaxis = dict(
        title_text = 'Total Acumulado (mm)'
    ),
    xaxis=dict(
        title_text='Data e Hora (BRT)',
        tickvals=pd.date_range('2022-11-26T00:00:00', '2022-12-01T00:00:00', freq='12H'),
    )
)

fig.write_image(f'salto.jpeg')
# %%
