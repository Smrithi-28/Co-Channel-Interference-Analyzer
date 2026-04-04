import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import math

# Valid cluster sizes
VALID_N = [1, 3, 4, 7, 9, 12]

def generate_sir_graph(n, i0, selected_N=None):
    """
    Generates S/I vs Cluster Size graph.
    Highlights the selected_N with a red dot.
    """

    sir_db = []
    for N in VALID_N:
        si = (3 * N) ** (n / 2) / i0
        sir_db.append(10 * math.log10(si))

    plt.figure(figsize=(6,4))
    plt.plot(VALID_N, sir_db, marker='o', label="S/I Curve")
    
    # Highlight the selected N if provided
    if selected_N in VALID_N:
        idx = VALID_N.index(selected_N)
        plt.plot(VALID_N[idx], sir_db[idx], 'ro', label=f"Selected N={selected_N}")
    
    plt.xlabel("Cluster Size (N)")
    plt.ylabel("S/I (dB)")
    plt.title("S/I vs Cluster Size")
    plt.grid()
    plt.legend()

    # Save the plot
    plt.savefig("static/sir_plot.png", bbox_inches='tight', dpi=150)
    plt.close()

    return "static/sir_plot.png"