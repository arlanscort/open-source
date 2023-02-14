'''
Ant Lion Optimizer (ALO) - Mirjalili (2015)
https://doi.org/10.1016/j.advengsoft.2015.01.010
Implementacao Python a partir do codigo oficial em Matlab, disponivel em https://seyedalimirjalili.com/alo
Implementação Python - Scortegagna, jun/2022
'''

#%% Imports
import numpy as np

#%% Funcoes
def roulette(weights):
    # Selecao aleatoria por roleta
    # Obs: a forma como esta implementado no Matlab tem problemas para valores negativos da funcao objetivo
    cumsum = np.cumsum(weights)
    p = np.random.random()*cumsum[-1]
    idx_selected = np.nan
    for i in range(len(cumsum)):
        if cumsum[i] > p:
            idx_selected = i
            break
    if np.isnan(idx_selected):
        idx_selected = 0

    return idx_selected

def random_walk(dim, UB, LB, X_antlion, t, t_max):
    # Passeio aleatorio das formigas em torno da formiga-leao selecionada
    # 1 - Atribuir o raio de reducao progressiva do espaco de busca
    if t > t_max*(0.95):
        I = 1 + (10**6)*(t/t_max)
    elif t > t_max*(0.90):
        I = 1 + (10**5)*(t/t_max)
    elif t > t_max*(0.75):
        I = 1 + (10**4)*(t/t_max)
    elif t > t_max*(0.5):
        I = 1 + (10**3)*(t/t_max)
    elif t > t_max*(0.1):
        I = 1 + (10**2)*(t/t_max)
    else:
        I = 1
    
    # 2 - Mover o espaco de busca e atribuir aleatoriam um quadrante em torno da formiga-leao (armadilha)
    # Obs: a forma como essa parte foi implementada permite violar o espaco de busca definido
    if np.random.random() < 0.5:
        LB_t = X_antlion + LB/I
    else:
        LB_t = X_antlion - LB/I
    if np.random.random() >= 0.5:
        UB_t = X_antlion + UB/I
    else: 
        UB_t = X_antlion - UB/I
    
    # 3 - Executar o passeio aleatorio
    RW = []
    for i in range(dim):
        R = (np.random.random((t_max,1)) > 0.5).astype(int)
        R_ = 2*R-1
        R__ = np.insert(R_, 0, 0, axis=0)
        X = np.cumsum(R__, axis=0)
        # Normalizar
        a = X.min()
        b = X.max()
        c = LB_t[:,i]
        d = UB_t[:,i]
        X_norm = ((X-a)*(d-c))/(b-a) + c
        RW.append(X_norm)
    RW = np.concatenate(RW, axis=1)

    return RW

#%% ALO
def alo(fobj, UB, LB, n, t_max, seed=None):
    
    # Ajustes
    if seed is not None:
        np.random.seed(seed)
    dim = len(UB)
    UB = np.asarray(UB).reshape(1, -1)
    LB = np.asarray(LB).reshape(1, -1)
    
    # Inicializacao - primeira iteracao
    t = 1
    X_antlions = (UB - LB)*np.random.random((dim, n)).T + LB    
    X_ants = (UB - LB)*np.random.random((dim, n)).T + LB
    F_antlions = np.apply_along_axis(fobj, 1, X_antlions)
    X_antlions = X_antlions[F_antlions.argsort(),:]
    F_antlions = np.sort(F_antlions)
    sorted_antlion_fitness = F_antlions.copy() # !!! sorted_antlion_fitness nao eh reordenado !!!
    X_elite_antlion = X_antlions[0,:].copy()
    f_elite_antlion = F_antlions[0].copy()
    
    X_geracoes = [X_antlions.copy()]
    F_geracoes = [F_antlions.copy()]
    print(f'Iteracao {t}/{t_max} - f_elite = {f_elite_antlion}')

    # Loop principal - demais iteracoes
    while(t < t_max):
        t += 1

        # Aplicar os passeios aleatorios
        for i in range(n):            
            idx_selected = roulette(1/sorted_antlion_fitness) # ?!
            RA = random_walk(dim, UB, LB, X_antlions[idx_selected,:], t, t_max)
            RE = random_walk(dim, UB, LB, X_elite_antlion, t, t_max) # !!! sorted_antlion_fitness nao eh reordenado !!!
            X_ants[i,:] = (RA[t-1,:] + RE[t-1,:])/2
        
        # Ajustar formigas que violaram o espaco de busca e calcular a aptidao
        X_ants = np.clip(X_ants, LB, UB)
        F_ants = np.apply_along_axis(fobj, 1, X_ants)

        # Concatenar e selecionar os melhores
        X_combined = np.concatenate((X_antlions, X_ants), axis=0)
        F_combined = np.concatenate((sorted_antlion_fitness, F_ants)) # !!! sorted_antlion_fitness nao eh reordenado !!!
        X_antlions = X_combined[F_combined.argsort()[:n],:]
        F_antlions = np.sort(F_combined)[:n]
        
        # Atualizar a elite
        if F_antlions[0].item() < f_elite_antlion:
            X_elite_antlion = X_antlions[0].copy()
            f_elite_antlion = F_antlions[0].item()
            
        # Mantem a elite na populacao
        # Obs: Essa parte parece redundante...
        X_antlions[0] = X_elite_antlion.copy()
        F_antlions[0] = f_elite_antlion
        
        X_geracoes.append(X_antlions.copy())
        F_geracoes.append(F_antlions.copy())
        print(f'Iteracao {t}/{t_max} - f_elite = {f_elite_antlion}')

    return X_elite_antlion, f_elite_antlion, X_geracoes, F_geracoes