# -*- coding: utf-8 -*-
"""Figura 1 en seis columnas (diseño de Lina) armada solo con archivos reales de `figuras para flujo`:
recortes de los tres radares, cuatro recortes Sentinel-2 SWIR por cobertura, las dos series del
forzante y los tres mapas de producto. Las cajas de texto se dibujan aquí. Nada generado.

USO: python figura_diseno_h.py  -> fig_diseno_estudio_h.png
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(AQUI, "figuras para flujo")
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7})

fig = plt.figure(figsize=(16, 7.2))
gs = fig.add_gridspec(1, 6, left=0.006, right=0.994, top=0.985, bottom=0.01, wspace=0.06, width_ratios=[1.05, 1, 1.05, 1.15, 1, 1.2])
P = [fig.add_subplot(gs[0, i]) for i in range(6)]


def panel(ax, n, titulo):
    ax.set_axis_off()
    ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.02", fc="#fafafa", ec="#555555", lw=0.9, transform=ax.transAxes))
    ax.add_patch(Rectangle((0, 0.92), 1, 0.08, fc="#e6e6e6", ec="none", transform=ax.transAxes))
    ax.add_patch(plt.Circle((0.09, 0.96), 0.035, color="#333333", transform=ax.transAxes))
    ax.text(0.09, 0.96, str(n), color="white", ha="center", va="center", fontsize=9, fontweight="bold", transform=ax.transAxes)
    ax.text(0.57, 0.96, titulo, ha="center", va="center", fontsize=9, fontweight="bold", transform=ax.transAxes, linespacing=1.1)


def imagen(ax, ruta, x, y, w, h):
    im = plt.imread(os.path.join(F, ruta))
    a = ax.inset_axes([x, y, w, h])
    a.imshow(im, aspect="equal"); a.set_anchor("C")
    a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values():
        s.set_linewidth(0.5)
    return a


def caja(ax, y, h, texto, fs=7.2):
    ax.add_patch(FancyBboxPatch((0.07, y), 0.86, h, boxstyle="round,pad=0.01,rounding_size=0.02", fc="#f0f0f0", ec="#777777", lw=0.6, transform=ax.transAxes))
    ax.text(0.5, y + h / 2, texto, ha="center", va="center", fontsize=fs, transform=ax.transAxes, linespacing=1.3)


def flecha(ax, y0, y1):
    ax.annotate("", xy=(0.5, y1), xytext=(0.5, y0), xycoords="axes fraction", arrowprops=dict(arrowstyle="-|>", lw=0.8, color="#444444"))


titulos = ["Datos de entrada", "Preprocesamiento SAR", "Muestreo por coberturas", "Asignación del\nforzante hidrológico", "Pruebas analíticas", "Productos"]
for i, t in enumerate(titulos):
    panel(P[i], i + 1, t)

# 1. datos de entrada
P[0].text(0.07, 0.885, "Imágenes SAR", fontweight="bold", fontsize=8, transform=P[0].transAxes)
for k, (f, lab) in enumerate([("01_NISAR_HH_D083_2025-10-29.png", "NISAR\nBanda L (HH, HV)\nD083, 29-oct-2025"),
                              ("03_ALOS2_HH_ScanSAR_2025-12-02.png", "ALOS-2 PALSAR-2\nBanda L (HH, HV)\nScanSAR, 2-dic-2025"),
                              ("02_Sentinel1_VV_D142_2026-01-09.png", "Sentinel-1\nBanda C (VV, VH)\nórbita 142, 9-ene-2026")]):
    y = 0.70 - k * 0.19
    imagen(P[0], f, 0.03, y - 0.01, 0.50, 0.19)
    P[0].text(0.58, y + 0.085, lab, va="center", fontsize=7, transform=P[0].transAxes, linespacing=1.3)
P[0].plot([0.07, 0.93], [0.29, 0.29], color="#999999", lw=0.6, ls="--", transform=P[0].transAxes)
P[0].text(0.07, 0.25, "Datos auxiliares", fontweight="bold", fontsize=8, transform=P[0].transAxes)
P[0].text(0.09, 0.21, "• Coberturas globales\n   (WorldCover 2021, GMW)\n• Forzantes hidrológicos\n   (marea, lluvia, nivel del río)\n• Muestra de referencia 2025\n• Dynamic World",
          va="top", fontsize=7, transform=P[0].transAxes, linespacing=1.45)

# 2. preprocesamiento
ys = [0.74, 0.57, 0.40, 0.23, 0.06]
tx = ["Calibración radiométrica\npor sensor", "Conversión a σ⁰ (NISAR: factor\ndel producto; ALOS-2: constante\nde JAXA; Sentinel-1: Earth Engine)",
      "Separación por traza\ny geometría de adquisición", "Promediado espacial\ny conversión a dB", "Extracción de retrodispersión\nen puntos de muestreo"]
for k, (y, s) in enumerate(zip(ys, tx)):
    caja(P[1], y + 0.015, 0.10, s)
    if k < 4:
        flecha(P[1], y + 0.015, ys[k + 1] + 0.115)

# 3. muestreo
for k, (f, lab) in enumerate([("04_agua_abierta_swir_S2_2025.png", "Agua abierta"), ("05_humedal_herbaceo_swir_S2_2025.png", "Humedal herbáceo"),
                              ("06_manglar_swir_S2_2025.png", "Manglar"), ("07_bosque_control_swir_S2_2025.png", "Bosque no inundable\n(control)")]):
    y = 0.715 - k * 0.195
    imagen(P[2], f, 0.05, y - 0.005, 0.44, 0.19)
    P[2].text(0.50, y + 0.09, lab, va="center", fontsize=7.5, transform=P[2].transAxes, linespacing=1.3)
P[2].plot([0.07, 0.93], [0.115, 0.115], color="#999999", lw=0.6, ls="--", transform=P[2].transAxes)
P[2].text(0.5, 0.06, "Sentinel-2 SWIR 2025, 1,5 km de lado.\n400 puntos por clase, compartidos\nentre sensores", ha="center", va="center", fontsize=6.8, transform=P[2].transAxes, linespacing=1.3)

# 4. forzante
imagen(P[3], "11_marea_malaga_ene2026.png", 0.03, 0.47, 0.94, 0.44)
imagen(P[3], "12_nivel_rio_lluvia_cgsm.png", 0.03, 0.06, 0.94, 0.42)

# 5. pruebas
ys = [0.70, 0.49, 0.28, 0.07]
tx = ["Comparación de condiciones\nalto − bajo del forzante\n(dentro de cada traza)", "Correlación de Spearman\npor pasada",
      "Análisis de robustez\n(ángulo de incidencia, dependencia\ntemporal, versión del producto)", "Clave de interpretación\nde la respuesta C frente a L\n(muestra 2025, 720 puntos)"]
for k, (y, s) in enumerate(zip(ys, tx)):
    caja(P[4], y + 0.02, 0.12, s)
    if k < 3:
        flecha(P[4], y + 0.02, ys[k + 1] + 0.14)

# 6. productos
for k, (f, lab) in enumerate([("09_mapa_cambio_50m_dHH_viridis.png", "Cambio ΔHH, nivel alto − bajo del río (dB)"),
                              ("08_mapa_senal_50m_HH_viridis.png", "Mapa de señal a 50 m (σ⁰ HH, dB)"),
                              ("10_dynamic_world_clases.png", "Contraste con Dynamic World")]):
    y = 0.63 - k * 0.30
    P[5].text(0.5, y + 0.265, lab, ha="center", va="center", fontsize=7.2, fontweight="bold", transform=P[5].transAxes)
    imagen(P[5], f, 0.05, y, 0.90, 0.25)

for i in range(1, 6):
    P[i].annotate("", xy=(0.0, 0.5), xytext=(-0.07, 0.5), xycoords=P[i].transAxes, arrowprops=dict(arrowstyle="-|>", lw=1.6, color="#333333"))
out = os.path.join(AQUI, "fig_diseno_estudio_h.png")
fig.savefig(out, dpi=220)
print("ok", out)
