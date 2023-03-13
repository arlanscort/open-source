#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 11:09:23 2023

@author: ana.becker

usar no google colab
"""

import ee
ee.Authenticate()
ee.Initialize()
'''
To authorize access needed by Earth Engine, open the following URL in a web browser and follow the instructions. If the web browser does not start automatically, please manually browse the URL below.

    https://code.earthengine.google.com/client-auth?scopes=https%3A//www.googleapis.com/auth/earthengine%20https%3A//www.googleapis.com/auth/devstorage.full_control&request_id=G0mRWnymtoFu_dz-v67tC2ptoXIl6TY5JCzMTVQTNTk&tc=Vck00pG4ioBmBVEspzhpIXuBLEvudQrg1UHzWSYASoI&cc=oqvsPU5phgRspBsAzSsmPiQxBRM7Lx8cv5Gr-BXTPxQ

The authorization workflow will generate a code, which you should paste in the box below.
Enter verification code: 4/1AWtgzh4Xc_GuI_mB3ZYvnZ9ItQHpdwlSFG77OBwcntY860AH9ZYHAKvY__Y

Successfully saved authorization token.
'''
import pandas as pd

table = pd.read_csv("/content/drive/MyDrive/Import/Estacoes/din_df_estacoes.csv")[['id_estacao','latitude','longitude']]
points = [ee.Geometry.Point(table['longitude'][i],table['latitude'][i]) for i in range(0,len(table))]
feats = [ee.Feature(p, {'estacao': '{}'.format(table['id_estacao'][i])}) for i, p in enumerate(points)]
fc = ee.FeatureCollection(feats)

DEM = ee.Image("USGS/SRTMGL1_003")

# extract points from DEM
reducer = ee.Reducer.first()
data = DEM.reduceRegions(fc, reducer.setOutputs(['elevation']), 30)

# see data
for feat in data.getInfo()['features']:
    print(feat['properties'])

# export as CSV
task = ee.batch.Export.table.toDrive(data, 'pointsDataExtract', 'AltitudePontos', 'AltitudePontos')
task.start()