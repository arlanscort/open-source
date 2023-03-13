#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 10:16:59 2023

@author: ana.becker
"""
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import os
import glob
import xarray as xr
import datetime as dt
from datetime import timedelta
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors
import plotly.express as px
import plotly.graph_objects as go



cores_plotly =  [   
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'   # blue-teal
    ]





