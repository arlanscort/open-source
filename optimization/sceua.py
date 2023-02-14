'''
Shuffled Complex Evolution - University of Arizona (SCE-UA)
Duan, 1992 (https://doi.org/10.1029/91WR02985)
Implementacao em Python por Arlan Scortegagna, junho de 2022
Tendo o objetivo de reproduzir o codigo oficial em Matlab (https://www.mathworks.com/matlabcentral/fileexchange/7671-shuffled-complex-evolution-sce-ua-method)
'''

import numpy as np

def cceua(C, m, q, beta, alpha, fobj, UB, LB, n):
    
    # Loop de selecao de pais para compor os subcomplexos B (controlado por beta)
    for b in range(beta):
        
        # Selecao de pais
        L = [0]
        for i in range(q-1):
            for iter in range(1000):
                lpos = int(np.floor(m + 0.5 - np.sqrt((m+0.5)**2 - m*(m+1)*np.random.rand())))
                if ~np.isin(lpos, L):
                    break
            L.append(lpos)
        B = C[L,:]
        
        # Loop de evolucao dos subcomplexos (controlado por alpha)
        for a in range(alpha):
            B = B[np.argsort(B[:,-1])]
            
            # Nelder & Mead
            g = np.mean(B[:q-1,:-1], axis=0)
            uq = B[-1,:-1]
            f_uq = B[-1,-1]
            r = 2*g - uq
            if np.any(r > UB) or np.any(r < LB):
                r = LB + np.random.rand(n)*(UB - LB)
            f_r = fobj(r)
            if f_r <= f_uq:
                B[-1,:-1] = r
                B[-1,-1] = f_r
            else:
                c = (g + uq)/2
                f_c = fobj(c)
                if f_c <= f_uq:
                    B[-1,:-1] = c
                    B[-1,-1] = f_c
                else:
                    z = LB + np.random.rand(n)*(UB - LB)
                    B[-1,:-1] = z
                    B[-1,-1] = fobj(z)
        
        # Retorna ao simplex no complexo
        C[L,:] = B[:,:]
        C = C[np.argsort(C[:,-1])]
    
    return C

def executar(fobj, UB, LB, k, t_max, m=None, q=None, beta=None, alpha=None, seed=None):

    # Ajustes
    fobj.counter = 0
    if seed is not None:
        np.random.seed(seed)
    n = len(UB)
    UB = np.asarray(UB)
    LB = np.asarray(LB)
    if m is None:
        m = 2*n + 1
    if q is None:
        q = n + 1
    if alpha is None:
        alpha = 1
    if beta is None:
        beta = 2*n + 1
    P = [2*(m+1-i)/(m*(m+1)) for i in range(1, m+1)]
    minimos = []
    
    # Inicializacao
    t = 0
    s = k*m
    D = np.empty((s, n+1))
    for i in range(s):
        D[i,:-1] = (UB-LB)*np.random.rand(n) + LB
        D[i,-1] = fobj(D[i,:-1])
    D = D[np.argsort(D[:,-1])]
    minimos.append(D[0,-1])
    
    # Loop principal
    while (t < t_max):
        t+=1

        # Loop nos complexos
        for i in range(1, k+1):
            I = [i+k*(j-1)-1 for j in range(1, m+1)]
            D[I,:] = cceua(D[I,:], m, q, beta, alpha, fobj, UB, LB, n)
        D = D[np.argsort(D[:,-1])]
        minimos.append(D[0,-1])
    return D, fobj.counter, minimos