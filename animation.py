import math
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D

def animate_path(adj, path, pos=None, interval=300, repeat=False, layout="auto", seed=42):
    G = nx.Graph()
    for u, nbrs in adj.items():
        G.add_node(u)
        for v in nbrs.keys():
            G.add_edge(u, v)

    if not path or any(n not in G for n in path):
        raise ValueError("All nodes in 'path' must exist in the graph and path must be non-empty.")

    if pos is None:
        nodes = list(G.nodes())
        ints_0_to_Nm1 = (
            all(isinstance(n, int) for n in nodes)
            and set(nodes) == set(range(len(nodes)))
        )

        def grid_positions(N):
            s = int(math.isqrt(N))
            if s * s != N:
                raise ValueError("Grid layout needs a perfect square number of nodes.")
            return {i: (i % s, -(i // s)) for i in range(N)}

        if layout == "grid":
            pos = grid_positions(len(nodes))
        elif layout == "spring":
            pos = nx.spring_layout(G, seed=seed)
        else:
            if ints_0_to_Nm1 and int(math.isqrt(len(nodes))) ** 2 == len(nodes):
                pos = grid_positions(len(nodes))
            else:
                pos = nx.spring_layout(G, seed=seed)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="lightgray", width=1.5)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color="#d6eaff", edgecolors="#4a6fa5", linewidths=1.0, node_size=500)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=9)
    ax.axis("off")

    path_line = Line2D([], [], lw=3, color="C1")
    curr_dot, = ax.plot([], [], "o", ms=10, color="C3")
    curr_seg = Line2D([], [], lw=4, alpha=0.6, color="C2")
    ax.add_line(path_line)
    ax.add_line(curr_seg)

    xs = [pos[n][0] for n in path]
    ys = [pos[n][1] for n in path]

    def init():
        path_line.set_data([], [])
        curr_dot.set_data([], [])
        curr_seg.set_data([], [])
        curr_seg.set_visible(False)
        return path_line, curr_dot, curr_seg

    def update(k):
        path_line.set_data(xs[:k+1], ys[:k+1])

        curr_dot.set_data([xs[k]], [ys[k]])

        if k > 0:
            curr_seg.set_data([xs[k-1], xs[k]], [ys[k-1], ys[k]])
            curr_seg.set_visible(True)
        else:
            curr_seg.set_visible(False)

        ax.set_title(f"Step {k}: {path[k]}", fontsize=12)
        return path_line, curr_dot, curr_seg

    frames = range(len(path))
    ani = FuncAnimation(
        fig, update, frames=frames, init_func=init,
        interval=interval, blit=True, repeat=repeat
    )
    plt.show()

    return ani
