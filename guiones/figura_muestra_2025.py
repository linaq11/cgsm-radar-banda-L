# -*- coding: utf-8 -*-
r"""Figura de la muestra de referencia de 2025 sobre el AOI de la CGSM: los 720 puntos por clase
final, la reserva de validacion (que la muestra no toca) y los bloques de 12 km de la validacion
cruzada. Para la seccion 2.7 del informe de radar (y reutilizable en la tesis).

Fuentes: AVANCE TESIS/MUESTRA_2025/etiquetas_2025.csv (clase_final, lon, lat), pliegues_cv.csv
(bloque12), reserva_validacion.geojson; AOI desde el asset de Earth Engine.
USO: python figura_muestra_2025.py   -> fig_muestra_2025.png
"""
import json
import os

import ee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
from pyproj import Transformer

AQUI = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(AQUI, "..", "AVANCE TESIS", "MUESTRA_2025")
COL = {"agua": "#1f6f78", "vegetacion_flotante": "#d9571e", "manglar_intacto": "#1b7a3e", "manglar_degradado": "#8c6d1f",
       "humedal_herbaceo": "#c9b458", "otro": "#7a7a7a"}
ETQ = {"agua": "Open water", "vegetacion_flotante": "Floating vegetation", "manglar_intacto": "Intact mangrove",
       "manglar_degradado": "Degraded mangrove", "humedal_herbaceo": "Herbaceous wetland", "otro": "Other"}

ee.Initialize(project="basic-buttress-338101")
aoi = ee.FeatureCollection("projects/basic-buttress-338101/assets/AOI_tesis_CGSM_v1").geometry().getInfo()
tr = Transformer.from_crs(4326, 32618, always_xy=True)

def anillos(geom):
    if geom["type"] == "Polygon":
        return [geom["coordinates"][0]]
    return [p[0] for p in geom["coordinates"]]

d = pd.read_csv(os.path.join(M, "etiquetas_2025.csv")).merge(pd.read_csv(os.path.join(M, "pliegues_cv.csv")), on="id")
d["x"], d["y"] = tr.transform(d.lon.values, d.lat.values)
res = json.load(open(os.path.join(M, "reserva_validacion.geojson"), encoding="utf-8"))

fig, ax = plt.subplots(figsize=(8.2, 7.2))
for r in anillos(aoi):
    x, y = tr.transform(*np.array(r).T); ax.plot(x / 1e3, y / 1e3, color="#222222", lw=1.0)
for f in res["features"]:
    for r in anillos(f["geometry"]):
        x, y = tr.transform(*np.array(r).T); ax.fill(x / 1e3, y / 1e3, color="#9fc5e8", alpha=0.45, ec="#2e5090", lw=0.6)
# bloques de 12 km del esquema de validacion cruzada (codigo = floor(x/12km)*10000 + floor(y/12km))
for b in d.bloque12.unique():
    bx, by = divmod(int(b), 10000)
    ax.add_patch(Rectangle((bx * 12, by * 12), 12, 12, fill=False, ec="#aaaaaa", lw=0.4, ls=":"))
for c, g in d.groupby("clase_final"):
    ax.scatter(g.x / 1e3, g.y / 1e3, s=9, color=COL[c], label="%s (%d)" % (ETQ[c], len(g)), linewidths=0)
ax.set_aspect("equal"); ax.set_xlabel("UTM 18N easting (km)"); ax.set_ylabel("northing (km)")
ax.set_xlim(d.x.min() / 1e3 - 4, d.x.max() / 1e3 + 4); ax.set_ylim(d.y.min() / 1e3 - 4, d.y.max() / 1e3 + 4)
ax.legend(fontsize=8, loc="lower left", title="720 reference points, final class", title_fontsize=8, framealpha=0.9)
ax.text(0.99, 0.99, "shaded: validation reserve (not sampled)\ndotted: 12 km blocks of the spatial CV", transform=ax.transAxes, ha="right", va="top", fontsize=8, color="#2e5090")
ax.set_title("2025 reference sample over the CGSM study area", fontsize=11)
fig.tight_layout(); fig.savefig(os.path.join(AQUI, "fig_muestra_2025.png"), dpi=170)
print("fig_muestra_2025.png |", d.clase_final.value_counts().to_dict(), "| bloques:", d.bloque12.nunique())
