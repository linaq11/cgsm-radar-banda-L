# -*- coding: utf-8 -*-
"""Dos miniaturas de producto para el flujo, con datos reales y la paleta del esquema de Lina:

08_mapa_senal_50m_HH_viridis.png : σ⁰ HH de NISAR a 50 m (mediana de las 6 pasadas de nivel alto,
                                   D083, oct-2025 a ene-2026), viridis de −25 a −5 dB, barra y escala.
09_mapa_cambio_50m_dHH_viridis.png: ΔHH alto − bajo de nivel del río (banda 1 de
                                   mapa_doble_rebote_50m.tif), viridis de −2 a +2 dB, el mapa del informe.
10_dynamic_world_clases.png       : clase modal de Dynamic World V1 en la ventana de nivel alto
                                   (oct-2025 a ene-2026) sobre la caja, en cuatro grupos: agua,
                                   vegetación inundada, vegetación terrestre (árboles, pasto, arbustos,
                                   cultivos), otras (construido, suelo desnudo).

USO: python exportar_productos.py
"""
import os
import io
import glob
import h5py
import numpy as np
import requests
os.environ["PROJ_DATA"] = os.path.join(os.path.dirname(__import__("rasterio").__file__), "proj_data")
import rasterio
from pyproj import Transformer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
import ee

AQUI = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.dirname(AQUI)
NISAR = r"D:\TESIS_DATACUBE\NISAR"
G = "science/LSAR/GCOV/grids/frequencyA"
ALTO = ["20251029", "20251122", "20251204", "20251216", "20251228", "20260109"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
fuentes = []


def agg(a, b=5):
    ny, nx = (a.shape[0] // b) * b, (a.shape[1] // b) * b
    return np.nanmean(np.where(np.isfinite(a[:ny, :nx]), a[:ny, :nx], np.nan).reshape(ny // b, b, nx // b, b), axis=(1, 3))


def escala(ax, ancho_px, m_por_px):
    """Barra 0-5-10 km abajo a la izquierda."""
    x0, y0 = 0.03 * ancho_px, ax.get_ylim()[0] * 0.96
    for k, (a, c) in enumerate([(0, "black"), (5000, "white")]):
        ax.add_patch(plt.Rectangle((x0 + a / m_por_px, y0), 5000 / m_por_px, 0.012 * ax.get_ylim()[0], fc=c, ec="black", lw=0.6))
    for km in (0, 5, 10):
        ax.text(x0 + km * 1000 / m_por_px, y0 - 0.01 * ax.get_ylim()[0], str(km), ha="center", va="bottom", fontsize=7)
    ax.text(x0 + 11500 / m_por_px, y0 - 0.01 * ax.get_ylim()[0], "km", ha="left", va="bottom", fontsize=7)


def mapa(arr, nombre, vmin, vmax, etiqueta, fuente):
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    im = ax.imshow(arr, cmap="viridis", vmin=vmin, vmax=vmax, interpolation="nearest")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.02)
    cb.set_label(etiqueta)
    escala(ax, arr.shape[1], 50)
    fig.savefig(os.path.join(AQUI, nombre), dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    fuentes.append(fuente)
    print("ok", nombre)


# 8. sigma0 HH a 50 m, mediana de las pasadas de nivel alto
pilas = []
for f in ALTO:
    ruta = glob.glob(os.path.join(NISAR, "NISAR_AOI_%s_083*.h5" % f))[0]
    with h5py.File(ruta, "r") as h:
        g = h[G]
        pilas.append(10 * np.log10(agg(g["HHHH"][:] * g["rtcGammaToSigmaFactor"][:])))
hh = np.nanmedian(np.dstack(pilas), axis=2)
mapa(hh, "08_mapa_senal_50m_HH_viridis.png", -25, -5, "σ⁰ HH (dB)",
     "08_mapa_senal_50m_HH_viridis.png: NISAR D083, mediana de las 6 pasadas de nivel alto (29-oct-2025 a 9-ene-2026), σ⁰ HH a 50 m, viridis −25 a −5 dB.")

# 9. dHH alto - bajo, el mapa del informe
with rasterio.open(os.path.join(RADAR, "mapa_doble_rebote_50m.tif")) as src:
    d_hh = src.read(1)
    b = src.bounds
mapa(d_hh, "09_mapa_cambio_50m_dHH_viridis.png", -2, 2, "ΔHH high − low river level (dB)",
     "09_mapa_cambio_50m_dHH_viridis.png: banda 1 de mapa_doble_rebote_50m.tif, ΔHH entre las 6 pasadas de nivel alto y las 8 de nivel bajo, viridis −2 a +2 dB.")

# 10. Dynamic World en cuatro clases
ee.Initialize(project="basic-buttress-338101")
tr = Transformer.from_crs("EPSG:32618", "EPSG:4326", always_xy=True)
x0, y0 = tr.transform(b.left, b.bottom)
x1, y1 = tr.transform(b.right, b.top)
caja = ee.Geometry.Rectangle([x0, y0, x1, y1])
dw = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filterBounds(caja).filterDate("2025-10-01", "2026-02-01").select("label")
# etiquetas DW: 0 water, 1 trees, 2 grass, 3 flooded_vegetation, 4 crops, 5 shrub_and_scrub, 6 built, 7 bare, 8 snow_and_ice
grupo = dw.mode().remap([0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 2, 2, 1, 2, 2, 3, 3, 3])
PAL = ["4a3f7a", "4fb0bf", "8fcf5a", "d9d9d9"]
url = grupo.visualize(min=0, max=3, palette=PAL).clip(caja).getThumbURL({"dimensions": 1400, "region": caja, "format": "png"})
r = requests.get(url, timeout=300); r.raise_for_status()
img = plt.imread(io.BytesIO(r.content))
fig, ax = plt.subplots(figsize=(5.2, 4.6))
ax.imshow(img, interpolation="nearest")
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)
ancho_m = b.right - b.left
escala(ax, img.shape[1], ancho_m / img.shape[1])
ax.legend(handles=[Patch(fc="#" + c, ec="#555555", lw=0.4, label=n) for c, n in zip(PAL, ["Water", "Flooded vegetation", "Terrestrial vegetation", "Other covers"])],
          loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, fontsize=8)
fig.savefig(os.path.join(AQUI, "10_dynamic_world_clases.png"), dpi=220, bbox_inches="tight", facecolor="white")
plt.close(fig)
fuentes.append("10_dynamic_world_clases.png: GOOGLE/DYNAMICWORLD/V1, clase modal de 1-oct-2025 a 31-ene-2026 (ventana de nivel alto), agrupada en agua, vegetación inundada, vegetación terrestre (árboles, pasto, arbustos, cultivos) y otras (construido, suelo desnudo).")
print("ok 10_dynamic_world_clases.png")

with open(os.path.join(AQUI, "FUENTES.txt"), "a", encoding="utf-8") as fh:
    fh.write("\nProductos (exportar_productos.py):\n" + "\n".join(fuentes) + "\n")
print("listo")
