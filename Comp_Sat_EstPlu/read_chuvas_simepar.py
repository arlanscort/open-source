# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


# lendo dados das estacoes
#%%
path = os.getcwd()+'/data/Chuvas-simepar'
csv_files = glob.glob(os.path.join(path, "*.csv"))
psim = pd.DataFrame()
for f in csv_files:
    df_est = pd.read_csv(f, skiprows = 1)
    df_est['codigo'] = f.split("/")[-1].split(".")[0]
    psim = pd.concat([psim,df_est])    
psim['codigo'] = psim['codigo'].astype(int)


# lendo e inserindo as coordenadas do inventário das estacoes
#%%
inv_est = pd.read_csv('data/estacoes.csv')[['codigo','latitude','longitude']]
# para o join funcionar, a coluna de interesse deve ser setada como index
psim = psim.set_index('codigo').join(inv_est.set_index('codigo'), on='codigo', how='left')


