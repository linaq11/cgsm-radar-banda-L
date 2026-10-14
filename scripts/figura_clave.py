# -*- coding: utf-8 -*-
"""Genera el espacio de firmas usado para la clave de interpretación de la CGSM.

El eje x representa la retrodispersión copolar (VV en banda C o HH en banda L) y el eje y la
diferencia copolar - cruzada (VV-VH o HH-HV), en dB. Cada cobertura se representa por la mediana
multifecha de las dos variables.

FUENTES
- cgsm_temporada_s1.csv
- cgsm_temporada_nisar.csv
- nisar_flotante.csv

SALIDA
fig_clave_firmas.png

USO
    python figura_clave.py
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
COL = {"agua": "#1f6f78", "flotante": "#d9571e", "humedal_herbaceo": "#c9b458",
       "manglar": "#1b7a3e", "bosque": "#6b6b6b"}
ETQ = {"agua": "Open water", "flotante": "Floating vegetation", "humedal_herbaceo": "Herbaceous wetland",
       "manglar": "Mangrove", "bosque": "Dry forest"}

s1 = pd.read_csv(os.path.join(AQUI, "cgsm_temporada_s1.csv"))
s1 = s1[s1.traza == "D142"].groupby("clase")[["CO", "X", "COmX"]].median()
ni = pd.read_csv(os.path.join(AQUI, "cgsm_temporada_nisar.csv"))
ni = ni[ni.traza == "D"].groupby("clase")[["CO", "X", "COmX"]].median()
fl = pd.read_csv(os.path.join(AQUI, "nisar_flotante.csv"))
fl = fl.groupby("grupo")[["HH", "HV", "HHmHV"]].median().rename(
    columns={"HH": "CO", "HV": "X", "HHmHV": "COmX"})
ni.loc["flotante"] = fl.loc["flotante"]
# en banda C la flotante se mide en el compuesto de dic-2025 (ver nisar_flotante.py)
s1.loc["flotante"] = {"CO": -13.27, "X": -20.74, "COmX": -13.27 + 20.74}

# donde dos clases casi coinciden, cada etiqueta lleva su desplazamiento y su alineacion
OFF = {("C", "agua"): (0, 16, "center"), ("C", "flotante"): (0, 16, "center"),
       ("C", "humedal_herbaceo"): (-14, -34, "right"), ("C", "manglar"): (14, -34, "left"),
       ("C", "bosque"): (10, 18, "left"),
       ("L", "agua"): (0, 16, "center"), ("L", "flotante"): (0, 16, "center"),
       ("L", "humedal_herbaceo"): (0, 16, "center"), ("L", "manglar"): (-14, -34, "right"),
       ("L", "bosque"): (14, -34, "left")}
fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.2), dpi=150)
for ax, (d, tit, banda) in zip(axes, [(s1, "(a) C-band · Sentinel-1 D142, 61 passes", "C"),
                                      (ni, "(b) L-band · NISAR D083, 12 passes", "L")]):
    for c in ("agua", "flotante", "humedal_herbaceo", "manglar", "bosque"):
        if c not in d.index:
            continue
        x, y = d.loc[c, "CO"], d.loc[c, "COmX"]
        dx, dy, ha = OFF[(banda, c)]
        ax.scatter(x, y, s=190, color=COL[c], edgecolor="#14212a", linewidth=1.1, zorder=3)
        ax.annotate("%s\n%.1f / %.1f dB" % (ETQ[c], x, y), (x, y), textcoords="offset points",
                    xytext=(dx, dy), ha=ha, fontsize=8.6, color="#14212a")
    ax.set_xlabel("Co-polarised backscatter (VV or HH, dB)")
    ax.set_ylabel("Co-pol minus cross-pol (dB)")
    ax.set_title(tit, fontsize=10)
    ax.grid(alpha=0.3)
    ax.set_xlim(-24, -5)
    ax.set_ylim(3.5, 13.5)
axes[0].annotate("darker, smoother surface", (-23.4, 12.9), fontsize=8, color="#6b6b6b", va="top")
axes[0].annotate("brighter, canopy volume", (-5.4, 12.9), fontsize=8, color="#6b6b6b", ha="right", va="top")
fig.suptitle("Signature space of the CGSM covers: the two bands separate different pairs of classes", fontsize=11.5)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_clave_firmas.png"))
print("fig_clave_firmas.png")
print(pd.concat({"C (S1 D142)": s1.round(2), "L (NISAR D083)": ni.round(2)}).to_string())
