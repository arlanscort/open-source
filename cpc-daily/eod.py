#%% 
import numpy as np 

#%% 
with open ('PRCP_CU_GAUGE_V1.0GLB_0.50deg_EOD.lnx') as f:
    data = np.fromfile(f.read())
    
    
    # .reshape([1200, 3600, 1])
# %%
