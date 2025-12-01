import pandas as pd
import numpy as np
from typing import Tuple

def difficulty(s: str, root: int) -> Tuple[float, float]:
    df = pd.read_csv(s, header=None, sep=r'\s+')
    
    nodes = sorted(set(df[0].astype(int).tolist() + df[1].astype(int).tolist()))
    n = len(nodes)
    
    r1, r2, r3, r4, r5 = classes(s) # Используется функция из task01
    
    l = np.zeros((5, n)) 
    
    for j, node in enumerate(nodes):
        l[0, j] = sum(r1[j]) 
        l[1, j] = sum(r2[j]) 
        l[2, j] = sum(r3[j]) 
        l[3, j] = sum(r4[j])  
        l[4, j] = sum(r5[j])  
    
    # Расчёт энтропии
    H_total = 0.0
    max_links = n - 1  
    
    for j in range(n): 
        H_element = 0.0
        for i in range(5): 
            if l[i, j] > 0:
                P = l[i, j] / max_links
                H_partial = -P * np.log2(P)
                H_element += H_partial
        H_total += H_element
    
    # Нормализация по эталонной мере
    k = 5 
    c = 1 / (np.e * np.log(2))
    H_ref = c * n * k
    
    # Нормированная сложность
    h_normalized = H_total / H_ref
    
    return (H_total, h_normalized)

difficulty("./ult.csv", 0)
