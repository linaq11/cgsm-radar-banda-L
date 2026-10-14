# -*- coding: utf-8 -*-
r"""Figura de la prueba de consistencia de la interprete (muestra 2025): matriz de la clase de
referencia (clase_final, criterio v1) frente a la segunda pasada a ciegas, con acuerdo, Wilson y
kappa en el titulo. Solo agregados; nunca ids. Para los limites de la clave del informe de radar.

Requiere la exportacion consistencia/consistencia_2025_n*.csv de la app. Si no existe, avisa y sale.
USO: python figura_consistencia.py   -> fig_consistencia_2025.png
"""
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(AQUI, "..", "AVANCE TESIS", "MUESTRA_2025")
sys.path.insert(0, M)
from importlib import import_module
c36 = import_module("36_consistencia")

ORDEN = ["agua", "vegetacion_flotante", "manglar_intacto", "manglar_degradado", "humedal_herbaceo", "otro"]
ETQ = {"agua": "Water", "vegetacion_flotante": "Floating veg.", "manglar_intacto": "Intact mangrove",
       "manglar_degradado": "Degraded mangrove", "humedal_herbaceo": "Herb. wetland", "otro": "Other"}

fs = sorted(f for f in os.listdir(os.path.join(M, "consistencia")) if re.match(r"consistencia_2025_n\d+_\d{12}\.csv$", f))
if not fs:
    sys.exit("todavia no hay exportacion consistencia_2025_n*.csv")
b = c36.leer("consistencia_2025_n*.csv", c36.Path(M) / "consistencia")
e = pd.read_csv(os.path.join(M, "etiquetas_2025.csv"))
a = pd.DataFrame({"id": e.id, "clase": e.clase_final})
m = a.merge(b, on="id", suffixes=("_1", "_2"))
n = len(m); ok = (m.clase_1 == m.clase_2); lo, hi = c36.wilson(int(ok.sum()), n); k = c36.kappa(m.clase_1, m.clase_2)
ct = pd.crosstab(pd.Categorical(m.clase_1, ORDEN), pd.Categorical(m.clase_2, ORDEN), dropna=False)
fig, ax = plt.subplots(figsize=(6.6, 5.6))
im = ax.imshow(ct.to_numpy(), cmap="Blues")
for i in range(len(ORDEN)):
    for j in range(len(ORDEN)):
        v = ct.to_numpy()[i, j]
        if v:
            ax.text(j, i, str(v), ha="center", va="center", fontsize=10, color="white" if v > ct.to_numpy().max() / 2 else "#1a1a1a")
ax.set_xticks(range(6)); ax.set_yticks(range(6)); ax.set_xticklabels([ETQ[c] for c in ORDEN], rotation=35, ha="right", fontsize=8); ax.set_yticklabels([ETQ[c] for c in ORDEN], fontsize=8)
ax.set_xlabel("second blind pass (same interpreter, written criterion)"); ax.set_ylabel("reference label (clase_final)")
ax.set_title("Interpreter consistency on %d points: agreement %.2f [%.2f–%.2f], kappa %.2f" % (n, ok.mean(), lo, hi, k), fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(AQUI, "fig_consistencia_2025.png"), dpi=170)
print("fig_consistencia_2025.png | n %d acuerdo %.3f [%.3f, %.3f] kappa %.3f" % (n, ok.mean(), lo, hi, k))
