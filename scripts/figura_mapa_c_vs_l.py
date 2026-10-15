# -*- coding: utf-8 -*-
"""Redibuja la Figura 15 (ΔHH de NISAR frente a ΔVV de Sentinel-1) con contornos de cobertura y leyenda.

PROPÓSITO
    Hacer distinguible el manglar (contorno) del bosque de control (atenuado) en el mapa de las dos bandas.
DATOS
    mapa_doble_rebote_50m.tif (banda 1 ΔHH, banda 4 clase) y mapa_s1_alto_bajo_50m.tif (banda 1 ΔVV),
    ya calculados por mapa_doble_rebote.py y mapa_doble_rebote_s1.py. No recalcula nada.
MÉTODO
    Mismo color y escala que antes (RdBu_r, ±2 dB). Manglar a todo color con contorno verde oscuro;
    bosque de control atenuado sin contorno (demasiado fragmentado); leyenda y rótulos de sectores.
SALIDAS
    fig_mapa_c_vs_l.png (reemplaza la versión anterior sin contornos)
USO
    python figura_mapa_c_vs_l.py
LIMITACIÓN
    Los contornos se trazan sobre la malla de 50 m, así que el borde es escalonado a esa resolución.
"""
import importlib.util
import os

os.environ["PROJ_DATA"] = os.path.join(importlib.util.find_spec("rasterio").submodule_search_locations[0], "proj_data")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from scipy.ndimage import binary_closing

AQUI = os.path.dirname(os.path.abspath(__file__))
VERDE, MARRON = "#0b4d3a", "#7a4a1d"
SECTORES = [1205e3, 1190e3]

with rasterio.open(os.path.join(AQUI, "mapa_doble_rebote_50m.tif")) as src:
    d_hh, cl = src.read(1), src.read(4).astype(int)
    x0, y0 = src.transform.c, src.transform.f
with rasterio.open(os.path.join(AQUI, "mapa_s1_alto_bajo_50m.tif")) as src:
    d_vv = src.read(1)
ny, nx = d_hh.shape
ext = [x0 / 1000, (x0 + nx * 50) / 1000, (y0 - ny * 50) / 1000, y0 / 1000]
xc = (x0 + (np.arange(nx) + 0.5) * 50) / 1000
yc = (y0 - (np.arange(ny) + 0.5) * 50) / 1000
X, Y = np.meshgrid(xc, yc)
man = binary_closing(cl == 1, iterations=1).astype(float)
bos = binary_closing(cl == 2, iterations=1).astype(float)

fig, axs = plt.subplots(1, 2, figsize=(11, 5.4), constrained_layout=True)
for ax, (tit, a) in zip(axs, (("L-band, NISAR D083: ΔHH, high − low river level (dB)", d_hh),
                               ("C-band, Sentinel-1 orbit 142: ΔVV, same date groups (dB)", d_vv))):
    ax.imshow(np.where(np.isin(cl, [1, 2]), np.nan, 0.0), extent=ext, cmap="Greys", vmin=-1, vmax=1, alpha=0.18, interpolation="nearest")
    ax.imshow(np.where(cl == 2, a, np.nan), extent=ext, cmap="RdBu_r", vmin=-2, vmax=2, alpha=0.3, interpolation="nearest")
    im = ax.imshow(np.where(cl == 1, a, np.nan), extent=ext, cmap="RdBu_r", vmin=-2, vmax=2, interpolation="nearest")
    ax.contour(X, Y, man, levels=[0.5], colors=[VERDE], linewidths=0.55)
    for yy in SECTORES:
        ax.axhline(yy / 1000, color="#333333", lw=0.7, ls=":")
    ax.set_title(tit, fontsize=10.5)
    ax.set_xlabel("UTM 18N easting (km)"); ax.set_ylabel("northing (km)"); ax.tick_params(labelsize=8)
    ax.set_aspect("equal")
for ax in axs:
    ax.text(ext[0] + 0.6, 1205.4, "north", ha="left", va="bottom", fontsize=7.5, color="#333333")
    ax.text(ext[0] + 0.6, 1197.5, "centre", ha="left", va="center", fontsize=7.5, color="#333333")
    ax.text(ext[0] + 0.6, 1189.6, "south", ha="left", va="top", fontsize=7.5, color="#333333")
cb = fig.colorbar(im, ax=axs, shrink=0.75, pad=0.01)
cb.set_label("dB, median of high-level minus median of low-level passes")
leyenda = [Line2D([0], [0], color=VERDE, lw=1.4, label="mangrove (outlined, full colour)"),
           Patch(facecolor="#f2b8b0", edgecolor="#bbbbbb", label="dry forest control (faded colours)"),
           Patch(facecolor="#d9d9d9", edgecolor="none", label="other covers"),
           Line2D([0], [0], color="#333333", lw=0.9, ls=":", label="sectors: north, centre, south (Table 11)")]
axs[1].legend(handles=leyenda, loc="lower left", fontsize=7.5, frameon=True, framealpha=0.9)
fig.suptitle("Co-polar change between high and low Magdalena River level, 50 m", fontsize=11)
fig.savefig(os.path.join(AQUI, "fig_mapa_c_vs_l.png"), dpi=160)
print("ok fig_mapa_c_vs_l.png")
