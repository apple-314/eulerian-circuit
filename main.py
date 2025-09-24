from animation import animate_path

import copy

class Graph:
    def __init__(self, adj):
        self.adj = copy.deepcopy(adj)
        self.nodes = adj.keys()
        self.save = adj

    def deg(self, node):
        return len(self.adj[node])
    
    def cycle_dfs(self, start, sofar):
        cur = sofar[-1]
        if cur == start and len(sofar) > 1:
            return sofar
        
        for nei in self.adj[cur]:
            if nei in sofar and not (len(sofar) > 2 and nei == start):
                continue

            val = self.cycle_dfs(start, sofar + [nei])
            if val != -1:
                return val
        
        return -1

    def detect_cycle(self, start):
        cycle_nodes = self.cycle_dfs(start, [start]) # includes start twice
        n = len(cycle_nodes)
        
        edges = []
        for i in range(n-1):
            edges.append([cycle_nodes[i], cycle_nodes[i+1]])
        
        return edges
    
    def find_cc(self, start):
        q = [start]
        ct  = 0
        
        vis = {start: 1}

        while (ct < len(q)):
            cur = q[ct]
            done = False
            for nei in self.adj[cur]:
                if nei not in vis:
                    vis[nei] = 1
                    q.append(nei)
            
            ct += 1

        return vis.keys()

    def delete_edges(self, edges):
        for edge in edges:
            v1, v2 = edge
            del self.adj[v1][v2]
            del self.adj[v2][v1]

    def restore(self):
        self.adj = copy.deepcopy(self.save)

class Solver:
    def __init__(self, graph):
        self.graph = graph

    def solve_rec(self, start):
        if self.graph.deg(start) == 0:
            return [start]

        cycle_edges = self.graph.detect_cycle(start)
        cycle_nodes = [item[0] for item in cycle_edges]

        ans = []
        self.graph.delete_edges(cycle_edges)
        sofar = []
        for node in cycle_nodes:
            if node not in sofar:
                ans.extend(self.solve_rec(node))

                cc = self.graph.find_cc(node)
                sofar.extend(cc)
        ans.append(cycle_nodes[0]) # complete cycle
        return ans

    def solve(self, start):
        ans = self.solve_rec(start)
        self.graph.restore()
        return ans

# small example
# adj = {
#     0: {1:1, 3:1},
#     1: {0:1, 2:1},
#     2: {1:1, 3:1},
#     3: {0:1, 2:1}
# }

# big example
adj = {
    0: {1: 1, 4: 1},
    1: {0: 1, 5: 1},
    2: {3: 1, 6: 1},
    3: {2: 1, 7: 1},
    4: {0: 1, 5: 1},
    5: {1: 1, 4: 1, 6: 1, 9: 1},
    6: {2: 1, 5: 1, 7: 1, 10: 1},
    7: {3: 1, 6: 1},
    8: {9: 1, 12: 1},
    9: {5: 1, 8: 1, 10: 1, 13: 1},
    10: {6: 1, 9: 1, 11: 1, 14: 1},
    11: {10: 1, 15: 1},
    12: {8: 1, 13: 1},
    13: {9: 1, 12: 1},
    14: {10: 1, 15: 1},
    15: {11: 1, 14: 1}
}

g = Graph(adj)
s = Solver(g)

path = s.solve(0)
print(path)

animate_path(adj, path)