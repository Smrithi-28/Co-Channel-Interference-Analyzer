import math

def calculate_si(N, n, i0):
    si = (3 * N) ** (n / 2) / i0
    si_db = 10 * math.log10(si)
    return round(si, 3), round(si_db, 3)