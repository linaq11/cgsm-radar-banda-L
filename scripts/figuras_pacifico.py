# -*- coding: utf-8 -*-
"""Figuras de mapa para el informe de radar, Bahía de Málaga (ingles).

fig_malaga_radar.png     composiciones NISAR (R = HH, G = HV, B = HH-HV) de una escena
                         ascendente y una descendente cercanas en fecha, con el contorno
                         del manglar de consenso, y el mapa de diferencia HH entre ambas
fig_malaga_referencia.png coberturas WorldCover 2021 y acuerdo WorldCover / GMW
"""
import glob
import io
import os

import ee
import h5py
import numpy as np
import requests
from PIL import Image
from pyproj import Transformer
from scipy.ndimage import uniform_filter, zoom
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR = r"D:\TESIS_DATACUBE\NISAR_PACIFICO"
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
CAJA = [-77.40, 3.80, -77.10, 4.10]
ESCENAS = {"A": "NISAR_MALAGA_20251202_A004.h5", "D": "NISAR_MALAGA_20251204_D087.h5"}
PASO = 3   # submuestreo de pixeles para la figura (30 m)


def db(a):
    out = np.full(a.shape, np.nan, dtype="float32")
    ok = np.isfinite(a) & (a > 0)
    out[ok] = 10.0 * np.log10(a[ok])
    return out


def leer(nombre):
    with h5py.File(os.path.join(DIR, nombre), "r") as h:
        gr = h[GRUPO]
        xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
        fac = gr["rtcGammaToSigmaFactor"][:]
        hh = db(uniform_filter(np.nan_to_num(gr["HHHH"][:] * fac), 3))
        hv = db(uniform_filter(np.nan_to_num(gr["HVHV"][:] * fac), 3))
        epsg = int(h.attrs["epsg"])
    return xc, yc, hh, hv, epsg


# ---------------------------------------------------------------- recorte comun a la caja
def ventana(xc, yc, epsg):
    t = Transformer.from_crs("EPSG:4326", "EPSG:%d" % epsg, always_xy=True)
    xs, ys = zip(*[t.transform(lon, lat) for lon in (CAJA[0], CAJA[2]) for lat in (CAJA[1], CAJA[3])])
    i0, i1 = np.searchsorted(xc, [min(xs), max(xs)])
    j1, j0 = len(yc) - np.searchsorted(yc[::-1], [min(ys), max(ys)])
    return slice(j0, j1), slice(i0, i1)


datos = {}
for k, n in ESCENAS.items():
    xc, yc, hh, hv, epsg = leer(n)
    sj, si = ventana(xc, yc, epsg)
    datos[k] = dict(hh=hh[sj, si][::PASO, ::PASO], hv=hv[sj, si][::PASO, ::PASO], x=xc[si][::PASO], y=yc[sj][::PASO], epsg=epsg)
    print(k, n, datos[k]["hh"].shape, flush=True)


def rgb(d):
    def esc(a, lo, hi):
        return np.clip((a - lo) / (hi - lo), 0, 1)
    r, g, b = esc(d["hh"], -20, -2), esc(d["hv"], -26, -8), esc(d["hh"] - d["hv"], 2, 12)
    im = np.dstack([r, g, b]); im[~np.isfinite(d["hh"])] = 1
    return im


# ---------------------------------------------------------------- mascara de consenso desde Earth Engine, en la malla de la figura
ee.Initialize(project="basic-buttress-338101")
caja = ee.Geometry.Rectangle(CAJA)
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
consenso = wc.eq(95).And(gmw)
ref = datos["A"]
x0, x1, y0, y1 = float(ref["x"][0]), float(ref["x"][-1]), float(ref["y"][-1]), float(ref["y"][0])
region = ee.Geometry.Rectangle([x0, y0, x1, y1], "EPSG:%d" % ref["epsg"], False)
dims = "%dx%d" % (len(ref["x"]), len(ref["y"]))


def png_ee(img, vis):
    url = img.getThumbURL(dict(vis, region=region, dimensions=dims, crs="EPSG:%d" % ref["epsg"], format="png"))
    return np.array(Image.open(io.BytesIO(requests.get(url, timeout=300).content)).convert("RGBA"))


mask_png = png_ee(consenso.selfMask(), {"min": 0, "max": 1, "palette": ["000000", "ffffff"]})
mangle = mask_png[:, :, 3] > 0
print("mascara consenso en la malla:", mangle.shape, "| fraccion manglar %.1f %%" % (100 * mangle.mean()), flush=True)

# ---------------------------------------------------------------- figura 1: composiciones y diferencia
ext = [x0 / 1000, x1 / 1000, y0 / 1000, y1 / 1000]
fig, axes = plt.subplots(1, 3, figsize=(16, 5.6))
for ax, k, tit in zip(axes[:2], ["A", "D"], ["(a) Ascending track 004, 2 Dec 2025, 05:46 local, incidence ≈ 42°",
                                             "(b) Descending track 087, 4 Dec 2025, 18:29 local, incidence ≈ 35°"]):
    ax.imshow(rgb(datos[k]), extent=ext, interpolation="nearest")
    ax.contour(np.linspace(ext[0], ext[1], mangle.shape[1]), np.linspace(ext[3], ext[2], mangle.shape[0]), mangle.astype(float), levels=[0.5], colors="#ffff00", linewidths=0.5)
    ax.set_title(tit, fontsize=9.5); ax.set_xlabel("UTM 18N easting (km)"); ax.set_ylabel("northing (km)")
# diferencia HH (A - D), reproyectada por simple recorte comun (misma malla UTM y mismo paso)
hA, hD = datos["A"]["hh"], datos["D"]["hh"]
n = min(hA.shape[0], hD.shape[0]); m = min(hA.shape[1], hD.shape[1])
dif = hA[:n, :m] - hD[:n, :m]
im = axes[2].imshow(dif, extent=ext, cmap="RdBu_r", vmin=-4, vmax=4, interpolation="nearest")
axes[2].contour(np.linspace(ext[0], ext[1], mangle.shape[1]), np.linspace(ext[3], ext[2], mangle.shape[0]), mangle.astype(float), levels=[0.5], colors="k", linewidths=0.5)
axes[2].set_title("(c) HH difference, ascending − descending (dB)", fontsize=9.5); axes[2].set_xlabel("UTM 18N easting (km)")
fig.colorbar(im, ax=axes[2], fraction=0.046, pad=0.02, label="dB")
fig.suptitle("NISAR GCOV σ⁰ over Bahía de Málaga: R = HH, G = HV, B = HH − HV; yellow/black outline = mangrove (WorldCover ∩ GMW)", fontsize=10.5)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_malaga_radar.png"), dpi=170)
print("fig_malaga_radar.png", flush=True)

# ---------------------------------------------------------------- figura 2: referencia
clases = wc.remap([80, 95, 10, 90, 30, 40, 50, 60, 20], [1, 2, 3, 4, 5, 5, 6, 5, 5], 0)
pal = ["ffffff", "2166ac", "1b7837", "66a61e", "b8860b", "d9d9d9", "762a83"]
wc_png = png_ee(clases, {"min": 0, "max": 6, "palette": pal})
acuerdo = wc.eq(95).add(gmw.multiply(2))   # 0 ninguno, 1 solo WC, 2 solo GMW, 3 ambos
ac_png = png_ee(acuerdo.selfMask(), {"min": 1, "max": 3, "palette": ["fdae61", "abd9e9", "1b7837"]})
fig, axes = plt.subplots(1, 2, figsize=(12, 5.6))
axes[0].imshow(wc_png, extent=ext); axes[0].set_title("(a) WorldCover 2021 classes", fontsize=10)
axes[0].legend(handles=[Patch(color="#2166ac", label="Water"), Patch(color="#1b7837", label="Mangrove"), Patch(color="#66a61e", label="Tree cover"),
                        Patch(color="#b8860b", label="Herbaceous wetland"), Patch(color="#d9d9d9", label="Grass, crops, bare"), Patch(color="#762a83", label="Built-up")],
               fontsize=7.5, loc="lower left")
axes[1].imshow(np.ones_like(ac_png[:, :, :3]) * 255, extent=ext); axes[1].imshow(ac_png, extent=ext)
axes[1].set_title("(b) Mangrove extent: WorldCover 2021 vs Global Mangrove Watch 2020", fontsize=10)
axes[1].legend(handles=[Patch(color="#1b7837", label="Both (5,326 ha) – reference class"), Patch(color="#fdae61", label="WorldCover only (2,250 ha)"), Patch(color="#abd9e9", label="GMW only (680 ha)")],
               fontsize=7.5, loc="lower left")
for ax in axes:
    ax.set_xlabel("UTM 18N easting (km)"); ax.set_ylabel("northing (km)")
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_malaga_referencia.png"), dpi=170)
print("fig_malaga_referencia.png", flush=True)
