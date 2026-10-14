# -*- coding: utf-8 -*-
"""Figura 1 del informe: diseño analítico del estudio en seis filas, esquemático, con dos
miniaturas reales (recorte HH de NISAR y malla de clases a 50 m). Nada ilustrativo ni inventado.

USO: python figura_diseno.py   -> fig_diseno_estudio.png
Lee: D:\\TESIS_DATACUBE\\NISAR\\NISAR_AOI_20251029_083_4.h5 y mapa_doble_rebote_50m.tif.
"""
import os
import h5py
import numpy as np
os.environ["PROJ_DATA"] = os.path.join(os.path.dirname(__import__("rasterio").__file__), "proj_data")
import rasterio
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.colors import ListedColormap

AQUI = os.path.dirname(os.path.abspath(__file__))
H5 = r"D:\TESIS_DATACUBE\NISAR\NISAR_AOI_20251029_083_4.h5"
G = "science/LSAR/GCOV/grids/frequencyA"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7})
COL = {"manglar": "#1b7a3a", "bosque": "#b9a66b", "humedal": "#8fcf9a", "agua": "#3b6fb6"}

fig = plt.figure(figsize=(10, 8.2))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_axis_off()


def fila(y0, y1, n, titulo):
    ax.add_patch(FancyBboxPatch((1.5, y0), 97, y1 - y0, boxstyle="round,pad=0,rounding_size=1", fc="#f7f7f7", ec="#666666", lw=0.8))
    ax.add_patch(plt.Circle((4.5, y1 - 2.6), 1.6, color="#333333"))
    ax.text(4.5, y1 - 2.6, str(n), color="white", ha="center", va="center", fontsize=8, fontweight="bold")
    ax.text(7.5, y1 - 2.6, titulo, ha="left", va="center", fontsize=9.5, fontweight="bold")


def caja(x, y, w, h, texto, fs=7, fc="white"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.8", fc=fc, ec="#888888", lw=0.6))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs, linespacing=1.35)


def flecha_h(x0, x1, y):
    ax.annotate("", xy=(x1, y), xytext=(x0, y), arrowprops=dict(arrowstyle="-|>", lw=0.8, color="#444444"))


def flecha_v(x, y0, y1):
    ax.annotate("", xy=(x, y1), xytext=(x, y0), arrowprops=dict(arrowstyle="-|>", lw=1.0, color="#333333"))


# ---------- 1. datos de entrada (y 72-99)
fila(72, 99, 1, "Input data")
caja(3, 74, 36, 20, "", fc="#ffffff")
ax.text(21, 92.3, "SAR series (Table 1)", ha="center", fontsize=7.5, fontweight="bold")
with h5py.File(H5, "r") as h:
    g = h[G]
    hh = g["HHHH"][:] * g["rtcGammaToSigmaFactor"][:]
b = 10; ny, nx = (hh.shape[0] // b) * b, (hh.shape[1] // b) * b
hh = 10 * np.log10(np.nanmean(np.where(np.isfinite(hh[:ny, :nx]), hh[:ny, :nx], np.nan).reshape(ny // b, b, nx // b, b), axis=(1, 3)))
a1 = fig.add_axes([0.045, 0.80, 0.10, 0.10])
a1.imshow(hh, cmap="gray", vmin=-25, vmax=-3, aspect="auto"); a1.set_xticks([]); a1.set_yticks([])
for sp in a1.spines.values(): sp.set_linewidth(0.5)
ax.text(9, 75.2, "NISAR, L band (HH, HV)\nGCOV, 21 + 24 scenes\nquicklook: D083, 29 Oct 2025", ha="center", va="bottom", fontsize=6.2, linespacing=1.3)
caja(19, 80.5, 9, 8, "ALOS-2\nPALSAR-2\nL band\n(HH, HV)", fs=6.5, fc="#eeeeee")
caja(29, 80.5, 9, 8, "Sentinel-1\nGRD\nC band\n(VV, VH)", fs=6.5, fc="#eeeeee")
ax.text(28.5, 78.2, "ALOS-2 and Sentinel-1 served by\nGoogle Earth Engine; NISAR by CMR", ha="center", va="top", fontsize=6, color="#444444")

caja(41, 74, 27, 20, "")
ax.text(54.5, 92.3, "Reference covers", ha="center", fontsize=7.5, fontweight="bold")
ax.text(54.5, 83.5, "WorldCover 2021 (10 m)\nGlobal Mangrove Watch v3 (2020)\nmangrove = agreement of both\n\n2025 reference sample of the thesis\n(720 points, six classes)", ha="center", va="center", fontsize=6.6, linespacing=1.4)

caja(70, 74, 28.5, 20, "")
ax.text(84.2, 92.3, "Hydrological forcing", ha="center", fontsize=7.5, fontweight="bold")
ax.text(84.2, 83.5, "Tide at pass time, DIMAR table\nand harmonic prediction (Málaga)\n\n30-day rain, ERA5-Land (CGSM)\n\nMagdalena River level at Remolino,\nIDEAM hourly (CGSM)", ha="center", va="center", fontsize=6.6, linespacing=1.4)
flecha_v(50, 72, 70.3)

# ---------- 2. preprocesamiento (y 57-70)
fila(55.5, 70, 2, "SAR preprocessing")
xs = [3, 22, 41, 60, 79]; w = 18
tx = ["Radiometric calibration\nper sensor:\nNISAR γ⁰ RTC → σ⁰ with the\nproduct factor; ALOS-2 JAXA\nconstant; Sentinel-1 as in\nEarth Engine (no speckle filter)",
      "Separation by track or\norbit and acquisition\ngeometry (up to 1.4 dB\nbetween NISAR tracks)",
      "Spatial averaging\n(3 × 3 in NISAR, native\npixel in ALOS-2 and\nSentinel-1) and dB",
      "Extraction at the shared\nsample points, keeping\nlocal time and\nincidence angle",
      "Per-pass median per\nclass and mangrove −\nforest difference"]
for k, (x, s) in enumerate(zip(xs, tx)):
    caja(x, 56.5, w, 8.5, s, fs=6.3)
    if k < 4:
        flecha_h(x + w, xs[k + 1], 60.75)
flecha_v(50, 55.5, 53.8)

# ---------- 3. muestreo (y 40-53.5)
fila(40, 53.5, 3, "Cover sampling")
with rasterio.open(os.path.join(AQUI, "mapa_doble_rebote_50m.tif")) as src:
    cl = src.read(4)
a3 = fig.add_axes([0.035, 0.415, 0.11, 0.08])
cm = ListedColormap(["#ffffff", COL["manglar"], COL["bosque"], COL["humedal"], COL["agua"]])
a3.imshow(np.where(np.isfinite(cl), cl, 0), cmap=cm, vmin=-0.5, vmax=4.5, interpolation="nearest", aspect="auto")
a3.set_xticks([]); a3.set_yticks([])
for sp in a3.spines.values(): sp.set_linewidth(0.5)
ax.text(9, 40.5, "CGSM class grid at 50 m", ha="center", fontsize=6)
for k, (c, n) in enumerate([("agua", "Open water"), ("humedal", "Herbaceous wetland"), ("manglar", "Mangrove"), ("bosque", "Forest control (not flooded)")]):
    ax.add_patch(Rectangle((19 + k * 19, 46.5), 2.2, 2.2, fc=COL[c], ec="none"))
    ax.text(22 + k * 19, 47.6, n, va="center", fontsize=6.8)
ax.plot([19, 94], [45, 45], color="#aaaaaa", lw=0.5, ls="--")
ax.text(56.5, 42.6, "400 points per class and site, stratified draw in Earth Engine (seed 42), shared by the three sensors.\n"
        "Only passes covering the whole site box; the CGSM forest control is drawn outside the study area.", ha="center", va="center", fontsize=6.3, linespacing=1.4)
flecha_v(50, 40, 38.3)

# ---------- 4. forzante (y 31-38)
fila(31, 38, 4, "Forcing assigned to\neach pass")
caja(30, 31.8, 31, 5.4, "Bahía de Málaga\ntide height at pass time (series interpolated to the hour)", fs=6.5)
caja(64, 31.8, 34.5, 5.4, "Ciénaga Grande de Santa Marta\n30-day antecedent rain, then Magdalena River level", fs=6.5)
flecha_v(50, 31, 29.3)

# ---------- 5. pruebas (y 17-29)
fila(17, 29, 5, "Analytical tests")
xs = [21, 41, 61, 81]; w = 17.5
tx = ["Rule fixed before the data:\nmangrove co-pol rises with\nthe forcing, forest does not",
      "High − low forcing difference\nwithin each track and\nSpearman correlation",
      "Robustness: incidence terciles,\ntemporal dependence,\nproduct version (Beta, Prov.)",
      "Interpretation key C vs L\non the 720-point sample\n(JM separability, thresholds)"]
for k, (x, s) in enumerate(zip(xs, tx)):
    caja(x, 18.5, w, 9, s, fs=6.3)
flecha_v(50, 17, 15.3)

# ---------- 6. productos (y 3-15)
fila(3, 15, 6, "Products")
xs = [21, 41, 61, 81]
tx = ["Backscatter comparison\nbetween bands and covers\n(Tables 2 to 10)",
      "Interpretation key with\nmeasured thresholds\n(Tables 11 to 14)",
      "Signal map at 50 m in L and\nC band, both sites\n(Tables 15, 16)",
      "Optical check with\nDynamic World flooded\nvegetation"]
for x, s in zip(xs, tx):
    caja(x, 4.5, 17.5, 9, s, fs=6.3)

out = os.path.join(AQUI, "fig_diseno_estudio.png")
fig.savefig(out, dpi=220)
print("ok", out)
