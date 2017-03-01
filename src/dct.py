from __future__ import division
import numpy as np
import itertools

def dct(N=8):
    dct_matrix = np.zeros((N,N), dtype=np.float64)
    for i, j in itertools.product(range(N), range(N)):
        val = 0
        if i == 0:
            val = 1/np.sqrt(N)
        else:
            val = np.sqrt(2/N)*np.cos(  (np.pi*(2*j+1)*i)/(2*N) ) 
            
        dct_matrix[i,j] = val
        
    return dct_matrix
        
def dct_weights():
    return np.kron(dct(),dct()).astype(np.float32)


def quantization_matrix(quality_factor=50):
    Tb = np.array([16,11,10,16,24,40,51,61,
                    12,12,14,19,26,57,60,55,
                    14,13,16,24,40,57,69,56,
                    14,17,22,29,51,87,80,62,
                    18,22,37,56,68,109,103,77,
                    24,35,55,64,81,104,113,92,
                    49,64,78,87,103,121,120,101,
                    72,92,95,98,112,100,103,99])
            
    if quality_factor<50:
         S = 5000/quality_factor
    else:
         S = 200 - 2*quality_factor
                
    Ts = np.floor((S*Tb+50) / 100).astype(np.float32)

    return Ts