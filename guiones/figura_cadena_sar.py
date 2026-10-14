# -*- coding: utf-8 -*-
"""Cadena de procesamiento SAR del avance de radar, por sensor, en ingles (Figura 2).

Convencion de la semana 5 (De Luca et al. 2021; Yordanov y Brovelli 2021): flujo vertical
por etapas, cada etapa abierta en tres columnas, una por sensor (NISAR, ALOS-2, Sentinel-1),
productos intermedios a la izquierda con sus conteos y barras de software a la derecha.
Cubre solo las etapas 1 a 3 del metodo (Figura 1): adquisicion, calibracion radiometrica,
promediado espacial y conversion a dB, geometria por pasada y extraccion en los puntos.
Las cifras son las del informe (Tabla 1 y texto).

USO
    python figura_cadena_sar.py      -> fig_cadena_sar.png
"""
import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "fig_cadena_sar.png")

GRIS = "#555555"
AZUL = "#2e5090"
MONO = "DejaVu Sans Mono"
COL = {"NISAR": ("#f6b26b", "#fdf1e4"), "ALOS-2": ("#b4a7d6", "#f0edf6"), "Sentinel-1": ("#93c47d", "#eaf3e5")}
NEG = "#1a1a1a"

W = 6.3
AX0, AX1 = 0.02, 1.22          # productos
X0, X1 = 1.38, 5.62            # etapas
TX = [5.70, 5.89, 6.08]        # barras de software
TW = 0.13
TAM = 6.0
LH = 0.105
SEP = 0.13
ANCHO = 27                     # caracteres por linea dentro de cada columna de sensor

fig = plt.figure(figsize=(W, 9.0))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.axis("off")
TEXTOS = []
SENS = ["NISAR", "ALOS-2", "Sentinel-1"]
CW = (X1 - X0) / 3


def etapa(y_top, titulo, celdas, comun=None):
    """celdas: dict sensor -> lista de lineas; comun: texto que aplica a los tres sensores."""
    lineas = {s: [ln for it in celdas[s] for ln in textwrap.wrap(it, ANCHO, subsequent_indent=" ")] for s in SENS}
    n = max(len(v) for v in lineas.values())
    com = textwrap.wrap(comun, 92) if comun else []
    alto = 0.17 + 0.05 + LH * n + (0.03 + LH * len(com) if com else 0) + 0.05
    y0 = y_top - alto
    for k, s in enumerate(SENS):
        xa = X0 + k * CW
        ax.add_patch(Rectangle((xa, y0), CW, alto, fc=COL[s][1], ec=GRIS, lw=0.6))
        ax.add_patch(Rectangle((xa, y_top - 0.17), CW, 0.17, fc=COL[s][0], ec=GRIS, lw=0.6))
        y = y_top - 0.17 - 0.04
        for j, ln in enumerate(lineas[s]):
            TEXTOS.append(ax.text(xa + 0.05, y, ("• " if not ln.startswith(" ") else "  ") + ln.strip(), ha="left", va="top", fontsize=TAM, color=NEG))
            y -= LH
    # titulo de la etapa sobre las tres columnas
    ax.add_patch(Rectangle((X0, y_top - 0.17), X1 - X0, 0.17, fc="none", ec=GRIS, lw=0.6))
    ax.text((X0 + X1) / 2, y_top - 0.085, titulo, ha="center", va="center", fontsize=6.8, fontweight="bold", color=NEG,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=GRIS, lw=0.5))
    if com:
        y = y0 + 0.05 + LH * len(com)
        ax.add_patch(Rectangle((X0, y0 + 0.02), X1 - X0, LH * len(com) + 0.04, fc="white", ec=GRIS, lw=0.4, ls=(0, (1, 1.5))))
        for ln in com:
            TEXTOS.append(ax.text(X0 + 0.05, y, ln, ha="left", va="top", fontsize=TAM, color=AZUL))
            y -= LH
    return y0, (y_top + y0) / 2


def producto(y, titulo, cuerpo):
    n = cuerpo.count("\n") + 1
    alto = 0.2 + 0.1 * n
    for k in (2, 1, 0):
        ax.add_patch(FancyBboxPatch((AX0 + 0.03 * k, y - alto / 2 + 0.03 * k), AX1 - AX0 - 0.06, alto,
                                    boxstyle="round,pad=0.0,rounding_size=0.03", fc="white" if k else "#f4f4f4", ec=GRIS, lw=0.6))
    ax.text((AX0 + AX1) / 2 - 0.03, y + alto / 2 - 0.045, titulo, ha="center", va="top", fontsize=6.4, fontweight="bold", color=NEG)
    ax.text((AX0 + AX1) / 2 - 0.03, y + alto / 2 - 0.16, cuerpo, ha="center", va="top", fontsize=5.5, color=NEG, linespacing=1.15)
    ax.add_patch(FancyArrowPatch((X0, y), (AX1, y), arrowstyle="-|>", mutation_scale=7, lw=0.7, color=GRIS, shrinkA=0.5, shrinkB=0.5))


def bajar(y_base):
    for k in range(3):
        xc = X0 + (k + 0.5) * CW
        ax.add_patch(FancyArrowPatch((xc, y_base), (xc, y_base - SEP), arrowstyle="-|>", mutation_scale=8, lw=0.9, color=NEG, shrinkA=0.5, shrinkB=0.5))
    return y_base - SEP


YT = 8.95
ax.text((AX0 + AX1) / 2, YT, "Intermediate products", ha="center", va="top", fontsize=6.8, fontweight="bold", color=GRIS)
ax.text((X0 + X1) / 2, YT, "SAR processing chain per sensor (stages 1 to 3 of Figure 1)", ha="center", va="top", fontsize=6.8, fontweight="bold", color=GRIS)
ax.text((TX[0] + TX[-1] + TW) / 2, YT, "Software", ha="center", va="top", fontsize=6.8, fontweight="bold", color=GRIS)

# cabecera de sensores
YT_ET = YT - 0.16
y = YT_ET
for k, s in enumerate(SENS):
    xa = X0 + k * CW
    ax.add_patch(Rectangle((xa, y - 0.17), CW, 0.17, fc=COL[s][0], ec=GRIS, lw=0.6))
    ax.text(xa + CW / 2, y - 0.085, s, ha="center", va="center", fontsize=7.2, fontweight="bold", color=NEG)
y -= 0.17 + 0.08
Y1 = y

b, c = etapa(y, "1 · Acquisition and selection", {
    "NISAR": ["L2 GCOV, L-band, HH + HV, 10 m, 12-day repeat", "Inventory in the CMR catalogue; remote clip of the site window with earthaccess + h5py", "Beta and Provisional collections, both kept and labelled"],
    "ALOS-2": ["PALSAR-2 ScanSAR L2.2, L-band, HH + HV, 25 m; 14-day orbit cycle, observed every 28 days per path", "Earth Engine collection of JAXA ScanSAR L2.2", "Paths 138, 139, 140 (Málaga); 10 passes over the CGSM, 7 complete"],
    "Sentinel-1": ["GRD IW, C-band, VV + VH, 10 m, 6 to 12-day repeat", "Earth Engine collection COPERNICUS/S1_GRD", "Orbits 48 and 142 (Málaga); 77 and 142 (CGSM)"],
}, comun="Only passes that cover the whole site box are kept; track, pass direction and local hour recorded for every scene (inventory of 11 Sep 2026, updated 7 Oct)")
producto(c, "Scenes and passes", "NISAR 45 scenes (24 + 21)\nALOS-2: 39 + 7 passes\nSentinel-1: 89 + 119 passes")

y = bajar(b)
b, c = etapa(y, "2 · Radiometric calibration (one contract per sensor)", {
    "NISAR": ["Product is γ⁰ with radiometric terrain correction", "σ⁰ = γ⁰ × rtcGammaToSigmaFactor (grid shipped in the product)", "Incidence angle grid read from the product"],
    "ALOS-2": ["Product is 16-bit DN, orthorectified", "σ⁰ = 10·log10(DN²) − 83 dB (JAXA calibration constant)", "Mosaic per pass and path"],
    "Sentinel-1": ["As ingested by Earth Engine (Sentinel-1 Toolbox): thermal noise removal, radiometric calibration, terrain correction with SRTM 30 m", "σ⁰ in dB; no terrain flattening, no speckle filter"],
}, comun="Sensors are never mixed and tracks are never mixed within a sensor: geometry alone shifts the level by 0.5 to 1 dB (Table 3)")
Y2 = b
producto(c, "σ⁰ per scene", "linear power, native grid\nco-pol and cross-pol")

y = bajar(b)
Y3T = y
b, c = etapa(y, "3 · Reference points, spatial averaging, dB and extraction", {
    "NISAR": ["3 × 3 mean in power at the sample points", "5 × 5 block mean (50 m) for the map", "10·log10 → dB; HH − HV"],
    "ALOS-2": ["Native 25 m pixel at the points", "10·log10 → dB; HH − HV"],
    "Sentinel-1": ["Native 10 m pixel at the points", "VV, VH in dB; VV − VH"],
}, comun="400 random points per class (mangrove = WorldCover 2021 ∩ GMW 2020; forest, herbaceous wetland, water from WorldCover); median per class and pass → per-pass tables (stages 4 to 9 of Figure 1)")
Y3 = b
producto(c, "Per-pass class tables", "σ⁰ in dB per sensor, track,\npass and class; HH − HV")

barras = [("earthaccess · h5py · numpy", Y1, Y3, "#f9cb9c"), ("Earth Engine Python API", Y1, Y3, "#b6d7a8"), ("pandas · scipy", Y3T, Y3, "#9fc5e8")]
for (nombre, yt, yb, col), x in zip(barras, TX):
    ax.add_patch(Rectangle((x, yb), TW, yt - yb, fc=col, ec=GRIS, lw=0.5, alpha=0.9))
    ax.text(x + TW / 2, yt - 0.05, nombre, ha="center", va="top", fontsize=5.4, color=NEG, rotation=90)

pie = ("Arrows into the left column: the product each stage writes. Dotted boxes in blue: rules common to the three sensors. "
       "Scripts: 16_inventario_nisar, 17_descargar_nisar, 18/23/24_nisar_recorte, 20_nisar_incidencia (NISAR); alos2_marea_malaga, cgsm_temporada (ALOS-2); "
       "s1_marea_malaga, cgsm_temporada (Sentinel-1); perfil_pacifico_24, doble_rebote_incidencia, mapa_doble_rebote (extraction and map).")
ax.text(AX0, Y3 - 0.1, "\n".join(textwrap.wrap(pie, 150)), fontsize=5.4, color=GRIS, va="top", linespacing=1.25)
fondo = Y3 - 0.48
alto_total = YT + 0.05 - fondo
ax.set_ylim(fondo, YT + 0.05)
fig.set_size_inches(W, alto_total)
ax.set_position([0, 0, 1, 1])
fig.canvas.draw()
rend = fig.canvas.get_renderer()
for t in TEXTOS:
    bb = t.get_window_extent(rend)
    x1 = bb.x1 / fig.dpi
    lim = X1 - 0.03
    # cada columna de sensor termina en su propio borde
    x0 = bb.x0 / fig.dpi
    k = int((x0 - X0) // CW) if x0 >= X0 else 0
    lim = X0 + (k + 1) * CW - 0.03 if t.get_color() != AZUL else X1 - 0.03
    if x1 > lim:
        print("DESBORDA %.2f in: %s" % (x1 - lim, t.get_text()[:50]))
fig.savefig(SALIDA, dpi=300)
print("ok %s  (%.2f x %.2f in)" % (SALIDA, W, alto_total))
