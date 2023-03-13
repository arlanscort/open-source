#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:07:06 2023

@author: ana.becker
"""
############ Configurações ############

exec(open('src/_packages.py').read())


############ Leitura dos dados ############

# só rodar em caso de novos dados/estações
exec(open('src/read_chuvas_simepar.py').read()) #simepar
exec(open('src/read_nc.py').read()) #jaxa
exec(open('src/read_nc_noaa.py').read()) #cpc


# gerando dataframes horárias, diárias e mensais com todas as fontes de dados inclusas

exec(open('src/readData.py').read())


############ Gráficos ############

exec(open('src/[Scatterplot] Dispersão.py').read())
exec(open('src/[Boxplot] Chuva.py').read())
exec(open('src/[Lineplot] Chuva.py').read())
exec(open('src/[Hyetographs] Chuva.py').read())

############ Índices ############

# Cálculo dos índices para o dataframe
exec(open('src/[Calc] Indices.py').read())
# Mapas com os resultados dos índices
exec(open('src/[Geo] Indices.py').read())
