import numpy as np
import random

def generate_grid(n):
    '''
    generate n x n grid
    '''

    def to_val(i, j):
        return i * n + j

    adj = {}

    for i in range(n):
        for j in range(n):
            adj[to_val(i,j)] = {}

    for i in range(1,n-1):
        for j in range(1,n-1):
            val = to_val(i, j)
            for nei in [to_val(i-1, j), to_val(i+1, j), to_val(i, j-1), to_val(i, j+1)]:
                adj[val][nei] = 1
                adj[nei][val] = 1
    
    high = n * n - 1
    for i in range(0,n-1,2):
        adj[i][i+1] = 1
        adj[i+1][i] = 1

        adj[i*n][(i+1)*n] = 1
        adj[(i+1)*n][i*n] = 1

        adj[high-i][high-i-1] = 1
        adj[high-i-1][high-i] = 1

        adj[high-i*n][high-(i+1)*n] = 1
        adj[high-(i+1)*n][high-i*n] = 1

    return adj

    # adj = {
    #     0: {1: 1, 4: 1},
    #     1: {0: 1, 5: 1},
    #     2: {3: 1, 6: 1},
    #     3: {2: 1, 7: 1},
    #     4: {0: 1, 5: 1},
    #     5: {1: 1, 4: 1, 6: 1, 9: 1},
    #     6: {2: 1, 5: 1, 7: 1, 10: 1},
    #     7: {3: 1, 6: 1},
    #     8: {9: 1, 12: 1},
    #     9: {5: 1, 8: 1, 10: 1, 13: 1},
    #     10: {6: 1, 9: 1, 11: 1, 14: 1},
    #     11: {10: 1, 15: 1},
    #     12: {8: 1, 13: 1},
    #     13: {9: 1, 12: 1},
    #     14: {10: 1, 15: 1},
    #     15: {11: 1, 14: 1}
    # }    