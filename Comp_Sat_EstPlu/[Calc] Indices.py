#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:44:27 2023

@author: ana.becker
"""
def classifica(prate, psim):
    if (prate == 0 and psim ==0):
        return 'h'
    if (prate != 0 and psim !=0):
        return 'cn'
    if (prate != 0 and psim ==0):
        return 'fa'
    if (prate == 0 and psim !=0):
        return 'm'
    
def ACC(h,cn,fa,m):
    total = h+cn+fa+m
    return (h+cn)/total

def POD(h,cn,fa,m):
    return h/(h+m)
Para a análise de desempenho e validação dos desenvolvimentos deste projeto, foram selecionadas 36 estações de referência no estado do Paraná. 
def FAR(h,cn,fa,m):
    return fa/(fa+h)

def HSS(h,cn,fa,m):
    total = h+cn+fa+m
    hr = (((h+m)*(h+fa))+((cn+m)*(cn+fa)))/total
    return (h+cn-hr)/(total-hr)

def BIAS(h,cn,fa,m):
    return (h+fa)/(h+m)
    
psim = psim.reset_index()[['hordatahora','codigo','precipitacao(mm)']].rename({'hordatahora': 'time', 'precipitacao(mm)': 'chuva'}, axis='columns')
psim['fonte']= 'Simepar'

for j in [0.05,0.5,1]:
    psat_todos = pd.read_csv(f'csv/[TimeSpace]gsmap-nrt-{j}mm.csv')
    psat_todos = psat_todos[['time','codigo','chuva_time']].rename({ 'chuva_time': 'chuva'}, axis='columns')
    psat_todos['fonte']= 'JAXA'
    
    
    df = pd.concat([psat_todos, psim]).set_index(['time','codigo']).pivot(columns='fonte',values='chuva').dropna()
    df.reset_index(inplace=True)
    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
    df['caso']=None 
    df['caso']= df.apply(lambda x: classifica(x['JAXA'], x['Simepar']), axis=1)
    contagem = pd.DataFrame(df.groupby(['codigo','caso']).size())
    contagem.reset_index(inplace=True)
    contagem = contagem.pivot_table(values = 0, index = 'codigo', columns = 'caso')
    contagem['ACC'] = contagem.apply(lambda x: ACC(x['h'], x['cn'], x['fa'], x['m']), axis=1)
    contagem['POD'] = contagem.apply(lambda x: POD(x['h'], x['cn'], x['fa'], x['m']), axis=1)
    contagem['FAR'] = contagem.apply(lambda x: FAR(x['h'], x['cn'], x['fa'], x['m']), axis=1)
    contagem['HSS'] = contagem.apply(lambda x: HSS(x['h'], x['cn'], x['fa'], x['m']), axis=1)
    contagem['BIAS'] = contagem.apply(lambda x: BIAS(x['h'], x['cn'], x['fa'], x['m']), axis=1)
    contagem.to_csv(f'csv/indices_[TimeSpace]-{j}mm.csv')



# for j in [0.05,0.5,1]:
#     df = pd.read_csv(f'csv/indices_[TimeSpace]-{j}mm.csv')
#     print(df.mean(axis = 0, skipna = False))