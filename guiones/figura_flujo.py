# -*- coding: utf-8 -*-
"""Diagrama del flujo de trabajo del avance de radar, en ingles, para el informe.

Sigue la convencion vista en clase (semana 5: De Luca et al. 2021, Yordanov y Brovelli
2021): flujo vertical por etapas, cada etapa con las operaciones que ejecuta, los
productos intermedios a la izquierda con sus conteos y el software a la derecha con
barras que marcan en que etapas interviene. Al pie de cada etapa, en monoespaciada
azul, los guiones de RADAR/ (los numerados, de AVANCE TESIS/PUBLICACION_GEE/) que la
ejecutan. Las cifras son las del informe.

Esta pensado para la pagina: md_a_word.py inserta las figuras a 6,3 pulgadas de ancho,
de modo que la figura se dibuja a ese ancho y con letra de 6,8 pt para que se imprima
tal cual. La altura se calcula del texto y se avisa si supera lo que cabe en una
pagina carta con margenes de 2,5 cm (unas 8,4 pulgadas con leyenda).

USO
    python figura_flujo.py             -> fig_flujo_trabajo.png (resumen: una linea por etapa, Figura 1)
    python figura_flujo.py --detalle   -> fig_flujo_trabajo_detalle.png (todas las operaciones, anexo)
"""
import os
import sys
import textwrap

DETALLE = "--detalle" in sys.argv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "fig_flujo_trabajo_detalle.png" if DETALLE else "fig_flujo_trabajo.png")

GRIS = "#555555"
AZUL = "#2e5090"
MONO = "DejaVu Sans Mono"
CAB = {"data": "#f6b26b", "pre": "#f9cb9c", "ref": "#b6d7a8", "proc": "#93c47d", "test": "#6fa8dc",
       "rob": "#9fc5e8", "key": "#b4a7d6", "val": "#d9d2e9"}
CUERPO = {"data": "#fdf1e4", "pre": "#fdf3ea", "ref": "#eef6ea", "proc": "#eaf3e5", "test": "#e8f0f8",
          "rob": "#edf3f9", "key": "#f0edf6", "val": "#f5f3f8"}

# geometria en pulgadas (1 unidad de eje = 1 pulgada)
W = 6.3
AX0, AX1 = 0.02, 1.4         # productos intermedios
X0, X1 = 1.58, (5.66 if DETALLE else 6.22)   # etapas (sin barras de software en el resumen)
TX = [5.74, 5.93, 6.12]      # barras de software
TW = 0.13
ANCHO = 90 if DETALLE else 74   # caracteres por linea de vineta
TAM = 6.3 if DETALLE else 7.6
TEXTOS = []               # lineas de vineta, para medir desbordes
LH = 0.113 if DETALLE else 0.14   # alto de linea
SEP = 0.13 if DETALLE else 0.16   # separacion entre etapas
ALTO_MAX = 8.4

fig = plt.figure(figsize=(W, 9.0))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.axis("off")


def envolver(texto):
    return textwrap.wrap(texto, width=ANCHO, subsequent_indent="  ")


def etapa(y_top, titulo, items, tipo, scripts=None, resumen=None):
    if not DETALLE:
        items, scripts = [resumen], None
    lineas = []
    for it in items:
        if it.startswith("::"):
            lineas.append(("sub", it[2:]))
        else:
            for k, ln in enumerate(envolver(it)):
                lineas.append(("li" if k == 0 else "cont", ln))
    alto = 0.18 + 0.05 + LH * len(lineas) + (0.15 if scripts else 0.05)
    y0 = y_top - alto
    ax.add_patch(Rectangle((X0, y0), X1 - X0, alto, fc=CUERPO[tipo], ec=GRIS, lw=0.7))
    ax.add_patch(Rectangle((X0, y_top - 0.18), X1 - X0, 0.18, fc=CAB[tipo], ec=GRIS, lw=0.7))
    ax.text((X0 + X1) / 2, y_top - 0.09, titulo, ha="center", va="center", fontsize=7.6, fontweight="bold", color="#1a1a1a")
    y = y_top - 0.18 - 0.04
    for tipo_ln, ln in lineas:
        if tipo_ln == "sub":
            ax.text(X0 + 0.07, y, ln, ha="left", va="top", fontsize=TAM, fontweight="bold", color=AZUL)
        elif tipo_ln == "li":
            TEXTOS.append(ax.text(X0 + 0.07, y, "• " + ln, ha="left", va="top", fontsize=TAM, color="#1a1a1a"))
        else:
            TEXTOS.append(ax.text(X0 + 0.07, y, "  " + ln.strip(), ha="left", va="top", fontsize=TAM, color="#1a1a1a"))
        y -= LH
    if scripts:
        ax.text(X1 - 0.06, y0 + 0.035, scripts, ha="right", va="bottom", fontsize=5.4, color=AZUL, family=MONO)
    return y0, (y_top + y0) / 2


def producto(y, titulo, cuerpo, punteado=False):
    n = cuerpo.count("\n") + 1
    alto = 0.2 + 0.105 * n
    for k in (2, 1, 0):
        ax.add_patch(FancyBboxPatch((AX0 + 0.03 * k, y - alto / 2 + 0.03 * k), AX1 - AX0 - 0.06, alto,
                                    boxstyle="round,pad=0.0,rounding_size=0.03", fc="white" if k else "#f4f4f4",
                                    ec=GRIS, lw=0.6, ls=(0, (2, 2)) if punteado else "-"))
    ax.text((AX0 + AX1) / 2 - 0.03, y + alto / 2 - 0.045, titulo, ha="center", va="top", fontsize=6.6, fontweight="bold", color="#1a1a1a")
    ax.text((AX0 + AX1) / 2 - 0.03, y + alto / 2 - 0.165, cuerpo, ha="center", va="top", fontsize=5.7, color="#1a1a1a", linespacing=1.15)
    ax.add_patch(FancyArrowPatch((X0, y), (AX1, y), arrowstyle="-|>", mutation_scale=7, lw=0.7, color=GRIS, shrinkA=0.5, shrinkB=0.5))


def bajar(y_base, ls="-"):
    ax.add_patch(FancyArrowPatch(((X0 + X1) / 2, y_base), ((X0 + X1) / 2, y_base - SEP), arrowstyle="-|>",
                                 mutation_scale=8, lw=0.9, color="#1a1a1a" if ls == "-" else GRIS, ls=ls, shrinkA=0.5, shrinkB=0.5))
    return y_base - SEP


# ------------------------------------------------------------------ cabecera
YT = 8.95
ax.text((AX0 + AX1) / 2, YT, "Intermediate products", ha="center", va="top", fontsize=6.8, fontweight="bold", color=GRIS)
ax.text((X0 + X1) / 2, YT, "Processing stages (Python and Google Earth Engine, no SNAP)", ha="center", va="top", fontsize=6.8, fontweight="bold", color=GRIS)
if DETALLE:
    ax.text((TX[0] + TX[-1] + TW) / 2, YT, "Software", ha="center", va="top", fontsize=6.8, fontweight="bold", color=GRIS)

# ------------------------------------------------------------------ etapas
y = YT - 0.16
Y1 = y
b, c = etapa(y, "1 · Data access", [
    "NISAR L2 GCOV (HH, HV, 10 m): CMR inventory, remote clip of the site window",
    "ALOS-2 ScanSAR L2.2 (HH, HV, 25 m) and Sentinel-1 GRD (VV, VH, 10 m) in Earth Engine",
    "Land cover, ERA5-Land and Sentinel-2 in Earth Engine; tide and river tables as CSV",
    "Only passes that cover the whole site box are kept (inventory of 11 Sep 2026)",
], "data", resumen="NISAR GCOV clipped from the NASA archive; ALOS-2, Sentinel-1, land cover, ERA5-Land and Sentinel-2 from Earth Engine; tide and river tables", scripts="16_inventario_nisar · 17_descargar_nisar · 18/23/24_nisar_recorte · nivel_ideam_descarga")
producto(c, "Scenes and passes", "NISAR 45 scenes (24 + 21)\nALOS-2: 39 + 7 passes\nSentinel-1: 89 + 119 passes")

y = bajar(b)
b, c = etapa(y, "2 · Pre-processing and calibration (one contract per sensor)", [
    "NISAR: γ⁰ RTC to σ⁰ with rtcGammaToSigmaFactor, incidence grid, 3 × 3 mean, dB",
    "ALOS-2: σ⁰ = 10·log10(DN²) − 83 (JAXA), mosaic per pass and path; path 47 unused",
    "Sentinel-1 as ingested (orbit, thermal noise, calibration, terrain correction), dB",
    "Track, direction, local hour and incidence kept per pass; tracks never mixed",
], "pre", resumen="σ⁰ in dB per sensor with one calibration contract each; track, direction, hour and incidence kept per pass", scripts="18_nisar_recorte_remoto · 20_nisar_incidencia · alos2_marea_malaga · s1_marea_malaga")
Y2 = b
producto(c, "σ⁰ stacks in dB", "per sensor, pass and track\nco-pol, cross-pol, co − cross")

y = bajar(b)
Y3 = y
b, c = etapa(y, "3 · Reference covers and sampling design", [
    "Mangrove = pixels in both WorldCover 2021 and GMW 2020; others from WorldCover",
    "400 random points per class, drawn once for the three sensors; ~1,200 for terciles",
    "CGSM forest taken from the cube box: the dry forest lies outside the study area",
], "ref", resumen="Mangrove = WorldCover 2021 ∩ GMW 2020; 400 random points per class, the same for the three sensors", scripts="perfil_pacifico_24 · doble_rebote_incidencia · figuras_cgsm · figuras_pacifico")
producto(c, "Sample points", "1,600 per site (4 × 400)\n3,644 for the tercile test")

y = bajar(b)
b, c = etapa(y, "4 · Hydrological forcing at the time of each pass", [
    "Málaga: tide from DIMAR 2026; 2025 from a harmonic fit to UHSLC 085 (RMSE 0.15 m)",
    "CGSM: 30-day ERA5-Land rain, then Magdalena River level at Remolino, at the pass hour",
], "proc", resumen="Tide (Málaga) or river level and rain (CGSM) at the hour of each pass", scripts="mareas_buenaventura · mareas_dimar_a_serie · marea_vs_radar · cgsm_nivel_rio")
Y4 = b
producto(c, "Forcing series", "one value per pass:\ntide (m), rain (mm), level (m)")

y = bajar(b)
b, c = etapa(y, "5 · Per-pass class statistics", [
    "Median σ⁰ per class and pass (co-pol, cross-pol, difference); sd between dates per track",
    "Mangrove minus forest per pass removes the seasonal moisture shared by all covers",
], "proc", resumen="Median σ⁰ per class and pass; mangrove minus forest removes shared seasonal moisture", scripts="perfil_pacifico_24 · marea_vs_radar · cgsm_temporada")
producto(c, "Per-pass tables", "Tables 2–3 · Figure 5\nCSV per sensor and site")

y = bajar(b)
b, c = etapa(y, "6 · Hydrological test (reading rule fixed a priori)", [
    "Per track: median of passes above minus below the median forcing; Spearman ρ and p",
    "Double-bounce expectation: co-pol and co − cross rise; cross-pol and forest do not",
    "Three sensors in Málaga; NISAR D083 and Sentinel-1 in the CGSM; two-pass difference",
    "Result: L-band responds in HH and HH − HV at both sites; C-band does not",
], "test", resumen="Rule fixed a priori: high minus low forcing per track, Spearman ρ; L-band responds in HH, C-band does not", scripts="marea_vs_radar · s1_marea_malaga · alos2_marea_malaga · cgsm_temporada · cgsm_nivel_rio · figura_cgsm_optico")
producto(c, "Test results", "Tables 4–9\nFigures 6, 8–9, 10–13")

y = bajar(b)
b, c = etapa(y, "7 · Robustness and limits", [
    "Incidence terciles within each track: the response holds in all six",
    "Temporal dependence: lag-1 autocorrelation, effective n (Pyper, Peterman), corrected p",
    "Independent recalculation of Table 4; Beta versus Provisional confound declared (CGSM)",
], "rob", resumen="Incidence terciles, temporal autocorrelation (effective n), independent recalculation, confounds declared", scripts="doble_rebote_incidencia · autocorrelacion_temporal · auditoria_calculos.md")
producto(c, "Corrected statistics", "Table 10 · Figure 7\naudit note of 16 Sep 2026")

y = bajar(b)
b, c = etapa(y, "8 · Interpretation key by cover and mechanism", [
    "Signature of each CGSM cover in both bands: co-pol vs co − cross, median of passes",
    "Floating vegetation of 2025 from its optical signature, checked in 17 NISAR scenes",
    "Key tested on the 720 points of the 2025 sample: signatures, JM per pair, rule matrix",
    "Thresholds rewritten from the sample; rule decides 606 of 720, 68 % agreement (resubstitution)",
], "key", resumen="Signatures per cover in both bands; key tested on the 720 points of the 2025 sample and rewritten", scripts="figura_clave · nisar_flotante · clave_vs_muestra2025 · md_a_word")
producto(c, "Key and report", "Tables 11 to 14 · Figure 14\nAvance_proyecto_radar.docx")

y = bajar(b, ls="--")
b, c = etapa(y, "9 · Spatial map and optical check; pending items", [
    "50 m map, high minus low river level; Dynamic World, 54 clear dates, ΔDW vs ΔHH",
    "Pending: INVEMAR level in the wetland; D083 passes of one version; test sample",
], "val", resumen="50 m map of high minus low river level; Dynamic World check; INVEMAR levels and test sample pending", scripts="mapa_doble_rebote · corroboracion_dw")
Y9 = b
producto(c, "Map and optical check", "Tables 15–16 · Figures 15–18\nmapa_doble_rebote_50m.tif", punteado=False)

# ------------------------------------------------------------------ software
barras = [("Earth Engine Python API", Y1, Y4, "#b6d7a8"), ("earthaccess · h5py", Y1, Y2, "#f9cb9c"),
          ("pandas · scipy · matplotlib", Y3, Y9, "#9fc5e8")] if DETALLE else []
for (nombre, yt, yb, col), x in zip(barras, TX):
    ax.add_patch(Rectangle((x, yb), TW, yt - yb, fc=col, ec=GRIS, lw=0.5, alpha=0.9))
    ax.text(x + TW / 2, yt - 0.05, nombre, ha="center", va="top", fontsize=5.4, color="#1a1a1a", rotation=90)

pie = ("Arrows into the left column: the product each stage writes to disk. Blue monospace text: scripts in RADAR/ "
       "(numbered ones in AVANCE TESIS/PUBLICACION_GEE/) that run the stage. Dashed arrow: stage with pending items."
       if DETALLE else
       "Arrows into the left column: the product each stage writes. Dashed arrow: stage 9 still has pending items (stage 8 too: an independent test sample). "
       "The SAR processing chain of stages 1 to 3 is Figure 2; the scripts of each stage are listed in Annex A.")
ax.text(AX0, Y9 - 0.1, "\n".join(textwrap.wrap(pie, 150)), fontsize=5.6, color=GRIS, va="top", linespacing=1.25)
fondo = Y9 - 0.38
alto_total = YT + 0.05 - fondo
ax.set_ylim(fondo, YT + 0.05)
fig.set_size_inches(W, alto_total)
ax.set_position([0, 0, 1, 1])
fig.canvas.draw()
rend = fig.canvas.get_renderer()
desb = []
for t in TEXTOS:
    bb = t.get_window_extent(rend)
    xr = bb.x1 / fig.dpi
    if xr > X1 - 0.04:
        desb.append((round(xr - (X1 - 0.04), 2), t.get_text()[:60]))
for d in desb:
    print("DESBORDA %.2f in: %s" % d)
fig.savefig(SALIDA, dpi=300)
print("ok %s  (%.2f x %.2f in)" % (SALIDA, W, alto_total))
if alto_total > ALTO_MAX:
    print("AVISO: la figura mide %.2f in de alto; en la pagina caben %.1f" % (alto_total, ALTO_MAX))
