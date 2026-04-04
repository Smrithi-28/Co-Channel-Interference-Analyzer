import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

# 🔷 hex → pixel
def hex_to_pixel(q, r, size):
    x = size * (3/2 * q)
    y = size * (np.sqrt(3) * (r + q/2))
    return x, y

# 🔷 draw hex
def draw_hex(ax, x, y, size, color, label, fontsize, highlight=False):
    angles = np.linspace(0, 2*np.pi, 7)
    x_hex = x + size * np.cos(angles)
    y_hex = y + size * np.sin(angles)

    ax.fill(
        x_hex, y_hex,
        edgecolor='black',
        linewidth=3 if highlight else 1,
        facecolor=color
    )

    ax.text(x, y, str(label),
            ha='center', va='center',
            fontsize=fontsize, weight='bold')

# 🔷 (i, j)
def get_ij(N):
    mapping = {
        1:(1,0),
        3:(1,1),
        4:(2,0),
        7:(2,1),
        9:(3,0),
        12:(2,2),
        13:(3,1)
    }
    return mapping.get(N, None)

# 🔷 cluster shapes
def get_cluster(N):

    if N == 1:
        return [(0,0)]

    elif N == 3:
        return [(0,0),(1,0),(0,1)]

    elif N == 4:
        return [(0,0),(1,0),(1,-1),(0,1)]

    elif N == 7:
        return [
            (0,0),
            (1,0),(0,1),(-1,1),
            (-1,0),(0,-1),(1,-1)
        ]

    elif N == 9:
        return [
            (0,0),(1,0),(2,0),
            (0,1),(1,1),(2,1),
            (0,2),(1,2),(2,2)
        ]

    elif N == 12:
        return [
            (0,0),
            (1,0),(2,0),
            (0,1),(1,1),(2,1),
            (0,2),(1,2),
            (-1,1),(-1,0),
            (1,-1),(0,-1)
        ]

    elif N == 13:
        return [
            (0,0),
            (1,0),(2,0),(3,0),
            (0,1),(1,1),(2,1),
            (0,2),(1,2),
            (-1,1),(-1,0),
            (1,-1),(0,-1)
        ]

# 🔷 MAIN
def generate_grid(N, i0):

    ij = get_ij(N)
    if ij is None:
        raise ValueError("Invalid N")

    i, j = ij
    cluster = get_cluster(N)

    fig, ax = plt.subplots(figsize=(10,10))
    size = 1

    colors = plt.cm.Set3.colors

    # 🔥 font size
    if N <= 7:
        fs = 10
    elif N <= 9:
        fs = 8
    else:
        fs = 5

    # 🔥 reduce clusters for large N
    if N <= 7:
        cluster_range = 2
    else:
        cluster_range = 1

    # 🔥 tile clusters
    for u in range(-cluster_range, cluster_range + 1):
        for v in range(-cluster_range, cluster_range + 1):

            shift_q = u * i + v * (-j)
            shift_r = u * j + v * (i + j)

            cluster_color = colors[(u*5 + v) % len(colors)]

            for idx, (q, r) in enumerate(cluster):

                Q = q + shift_q
                R = r + shift_r

                x, y = hex_to_pixel(Q, R, size)

                label = idx + 1

                # 🔥 REMOVE boundary for N=12,13
                if N in [12, 13]:
                    highlight = False
                else:
                    highlight = (u == 0 and v == 0)

                if label == 1:
                    draw_hex(ax, x, y, size, 'red', label, fs, highlight)
                else:
                    draw_hex(ax, x, y, size, cluster_color, label, fs, highlight)

    ax.set_aspect('equal')
    ax.axis('off')

    plt.savefig('static/plot.png', bbox_inches='tight', dpi=150)
    plt.close()