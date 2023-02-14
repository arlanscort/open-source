'''
Created by Arlan Scortegagna, jan/2022
Download multiple folders from JAXA`s FTP
'''

import pandas as pd
import subprocess
from functools import partial
from multiprocessing import Pool, cpu_count

def aquisicao_gsmap_mes(ref):
    url = f'ftp://hokusai.eorc.jaxa.jp/now/half_hour/{ref.year}/{ref.month:02d}'
    # -nc : no clobber
    cmd = f"wget -r -nc --tries=3 --ftp-user='rainmap' --ftp-password='Niskur+1404' {url}"
    subprocess.run([cmd], shell=True)
    return 0

if __name__ == '__main__':
    
    refs = pd.period_range('2022-01', '2022-12', freq='M')
    # n = cpu_count()
    n = 16
    pool = Pool(cpu_count())
    funcao = partial(aquisicao_gsmap_mes)
    resultado = pool.map(funcao, refs)