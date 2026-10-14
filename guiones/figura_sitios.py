# -*- coding: utf-8 -*-
"""Mapa de localización de los dos sitios del trabajo de radar, para la diapositiva
"Diseño comparativo": Bahía de Málaga (régimen mareal) y Ciénaga Grande de Santa Marta
(régimen hidrológico continental), con los sensores usados en cada uno.

Fondo: teselas CartoDB Positron (panel principal) y Esri World Imagery (recuadros), vía
contextily. Salida: fig_sitios_localizacion.png (inglés, como todas las figuras).
"""
import os

import contextily as ctx
import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shapely.geometry import box

import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
IDIOMA = sys.argv[1] if len(sys.argv) > 1 else "en"        # python figura_sitios.py es  -> versión en español
T = {
    "en": {"cgsm": "Ciénaga Grande\nde Santa Marta", "malaga": "Bahía de Málaga",
           "pie": "Caribbean Sea (north) · Pacific Ocean (west)\nBasemap: Esri World Gray Canvas",
           "t_cgsm": "CGSM study area, 2,042 km² (thesis AOI)", "t_malaga": "Bahía de Málaga box, 0.30° × 0.30° (contrast site)",
           "titulo": "Two sites, two flooding regimes, three SAR sensors: comparative design of the L-band flooding test",
           "salida": "fig_sitios_localizacion.png"},
    "es": {"cgsm": "Ciénaga Grande\nde Santa Marta", "malaga": "Bahía de Málaga",
           "pie": "Mar Caribe (norte) · Océano Pacífico (occidente)\nFondo: Esri World Gray Canvas",
           "t_cgsm": "Área de estudio CGSM, 2.042 km² (AOI de la tesis)", "t_malaga": "Caja de Bahía de Málaga, 0,30° × 0,30° (sitio de contraste)",
           "titulo": "Dos sitios, dos regímenes de inundación, tres sensores SAR: diseño comparativo de la prueba de banda L",
           "salida": "fig_sitios_localizacion_es.png"},
}[IDIOMA]
AOI = gpd.read_file(r"C:\LINA\UNAL 2626-1\AVANCE TESIS\AOI\AOI_tesis_CGSM_v1.geojson").to_crs(3857)
MALAGA = gpd.GeoDataFrame(geometry=[box(-77.40, 3.80, -77.10, 4.10)], crs=4326).to_crs(3857)

fig = plt.figure(figsize=(11, 6.2), dpi=170)
ax = fig.add_axes([0.02, 0.04, 0.50, 0.92])
vista = gpd.GeoDataFrame(geometry=[box(-79.5, 1.5, -71.5, 12.6)], crs=4326).to_crs(3857).total_bounds
ax.set_xlim(vista[0], vista[2]); ax.set_ylim(vista[1], vista[3])
ctx.add_basemap(ax, source=ctx.providers.Esri.WorldGrayCanvas, zoom=6, attribution="")   # CartoDB exige clave desde 2026
for gdf, color in ((AOI, "#d9571e"), (MALAGA, "#1f6f78")):
    c = gdf.geometry.iloc[0].centroid
    ax.plot(c.x, c.y, "o", ms=13, mfc=color, mec="white", mew=1.8, zorder=5)
cg, ma = AOI.geometry.iloc[0].centroid, MALAGA.geometry.iloc[0].centroid
# texto sin recuadro: solo un halo blanco fino para que se lea sobre el mapa base
import matplotlib.patheffects as pe
HALO = [pe.withStroke(linewidth=2.6, foreground="white")]
ax.annotate(T["cgsm"], (cg.x, cg.y), xytext=(-40, -70), textcoords="offset points", fontsize=13, ha="right",
            color="#7a2f0c", weight="bold", path_effects=HALO,
            arrowprops=dict(arrowstyle="-", color="#d9571e", lw=1.2), zorder=6)
ax.annotate(T["malaga"], (ma.x, ma.y), xytext=(45, 30), textcoords="offset points", fontsize=13, ha="left",
            color="#0f4a50", weight="bold", path_effects=HALO,
            arrowprops=dict(arrowstyle="-", color="#1f6f78", lw=1.2), zorder=6)
ax.text(0.02, 0.98, "Colombia", transform=ax.transAxes, fontsize=10, va="top", weight="bold", color="#333333")
ax.text(0.02, 0.02, T["pie"],
        transform=ax.transAxes, fontsize=6.5, va="bottom", color="#666666")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_edgecolor("#999999")

# Recuadros con imagen satelital y el contorno de cada sitio.
for k, (gdf, color, titulo) in enumerate(((AOI, "#d9571e", T["t_cgsm"]), (MALAGA, "#1f6f78", T["t_malaga"]))):
    axi = fig.add_axes([0.56, 0.50 - 0.47 * k, 0.42, 0.41])
    b = gdf.total_bounds; dx, dy = (b[2] - b[0]) * 0.25, (b[3] - b[1]) * 0.25
    axi.set_xlim(b[0] - dx, b[2] + dx); axi.set_ylim(b[1] - dy, b[3] + dy)
    ctx.add_basemap(axi, source=ctx.providers.Esri.WorldImagery, zoom=10, attribution="")
    gdf.boundary.plot(ax=axi, color=color, lw=2.2)
    axi.set_title(titulo, fontsize=8.5, color=color, loc="left")
    axi.set_xticks([]); axi.set_yticks([])
    for s in axi.spines.values():
        s.set_edgecolor(color); s.set_linewidth(1.5)
    axi.text(0.01, 0.01, "Esri World Imagery", transform=axi.transAxes, fontsize=6, color="white", va="bottom")

fig.suptitle("Two sites, two flooding regimes, three SAR sensors: comparative design of the L-band flooding test", fontsize=11, y=1.03)
fig.savefig(os.path.join(AQUI, "fig_sitios_localizacion.png"), bbox_inches="tight", facecolor="white")
print("figura: fig_sitios_localizacion.png")
