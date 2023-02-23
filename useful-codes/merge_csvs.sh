# Created by Arlan Scortegagna. feb/2023

#!/bin/bash

awk 'NR == 1 || FNR > 1' chuva-estacoes/chuva_estacoes_*.csv > chuva-estacoes/chuva_estacoes_2016_2022.csv
