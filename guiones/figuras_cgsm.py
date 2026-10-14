# -*- coding: utf-8 -*-
"""Figuras de mapa para el informe de radar, Ciénaga Grande de Santa Marta (inglés).

fig_cgsm_radar.png       composiciones NISAR (R = HH, G = HV, B = HH-HV) de dos pasadas de la
                         traza descendente 083 de la misma versión del producto (Beta), una con
                         el río Magdalena alto (4-dic-2025, 2,67 m en Remolino) y otra con el río
                         más bajo (9-ene-2026, 1,69 m), con el contorno del manglar de consenso y
                         del AOI, y el mapa de diferencia de HH entre ambas. Las pasadas con el
                         río más bajo (0,9 a 1,2 m) son de la colección Provisional y no se
                         restan para no mezclar el cambio de calibración.
fig_cgsm_referencia.png  coberturas WorldCover 2021 y acuerdo WorldCover / GMW dentro del AOI.
"""
import io
import json
import os

import ee
import h5py
import numpy as np
import requests
from PIL import Image
from pyproj import Transformer
from scipy.ndimage import uniform_filter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR = r"D:\TESIS_DATACUBE\NISAR"
if not os.path.isdir(DIR):
    raise SystemExit("ABORTA: D: desmontado")
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
EPSG = 32618
ESCENAS = {"alto": ("NISAR_AOI_20251204_083_4.h5", "4 Dec 2025, river level 2.67 m"),
           "bajo": ("NISAR_AOI_20260109_083_4.h5", "9 Jan 2026, river level 1.69 m")}
PASO = 6   # submuestreo para la figura (60 m)
AOI_GEOJSON = r"C:\LINA\UNAL 2626-1\AVANCE TESIS\AOI\AOI_tesis_CGSM_v1.geojson"


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
        hh = db(uniform_filter(np.nan_to_num(gr["HHHH"][:] * fac), 3))[::PASO, ::PASO]
        hv = db(uniform_filter(np.nan_to_num(gr["HVHV"][:] * fac), 3))[::PASO, ::PASO]
    return dict(hh=hh, hv=hv, x=xc[::PASO], y=yc[::PASO])


datos = {k: leer(n) for k, (n, _) in ESCENAS.items()}
for k, d in datos.items():
    print(k, d["hh"].shape, flush=True)
ref = datos["alto"]
x0, x1, y0, y1 = float(ref["x"][0]), float(ref["x"][-1]), float(ref["y"][-1]), float(ref["y"][0])
ext = [x0 / 1000, x1 / 1000, y0 / 1000, y1 / 1000]

# contorno del AOI en UTM
gj = json.load(open(AOI_GEOJSON, encoding="utf-8"))
anillo = gj["features"][0]["geometry"]["coordinates"][0]
t = Transformer.from_crs("EPSG:4326", f"EPSG:{EPSG}", always_xy=True)
ax_aoi, ay_aoi = zip(*[t.transform(lon, lat) for lon, lat in anillo])
ax_aoi, ay_aoi = np.array(ax_aoi) / 1000, np.array(ay_aoi) / 1000


def rgb(d):
    def esc(a, lo, hi):
        return np.clip((a - lo) / (hi - lo), 0, 1)
    im = np.dstack([esc(d["hh"], -20, -2), esc(d["hv"], -26, -8), esc(d["hh"] - d["hv"], 2, 12)])
    im[~np.isfinite(d["hh"])] = 1
    return im


# máscaras desde Earth Engine en la malla de la figura
ee.Initialize(project="basic-buttress-338101")
aoi = ee.Geometry(gj["features"][0]["geometry"])
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = (ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3")
       .filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0))
consenso = wc.eq(95).And(gmw)
region = ee.Geometry.Rectangle([x0, y0, x1, y1], f"EPSG:{EPSG}", False)
dims = "%dx%d" % (len(ref["x"]), len(ref["y"]))


def png_ee(img, vis):
    url = img.clip(aoi).getThumbURL(dict(vis, region=region, dimensions=dims, crs=f"EPSG:{EPSG}", format="png"))
    return np.array(Image.open(io.BytesIO(requests.get(url, timeout=300).content)).convert("RGBA"))


mangle = png_ee(consenso.selfMask(), {"min": 0, "max": 1, "palette": ["000000", "ffffff"]})[:, :, 3] > 0
print("manglar de consenso en la malla: %.1f %%" % (100 * mangle.mean()), flush=True)
cx, cy = np.linspace(ext[0], ext[1], mangle.shape[1]), np.linspace(ext[3], ext[2], mangle.shape[0])

# áreas dentro del AOI (ha)
acuerdo = wc.eq(95).add(gmw.multiply(2))            # 1 solo WC, 2 solo GMW, 3 ambos
areas = (ee.Image.pixelArea().divide(1e4).addBands(acuerdo)
         .reduceRegion(ee.Reducer.sum().group(1, "c"), aoi, 30, maxPixels=1e10).getInfo()["groups"])
ha = {g["c"]: g["sum"] for g in areas}
print("ha: ambos %.0f | solo WC %.0f | solo GMW %.0f" % (ha.get(3, 0), ha.get(1, 0), ha.get(2, 0)), flush=True)

# ---------------------------------------------------------------- figura 1
fig, axes = plt.subplots(1, 3, figsize=(17, 5.4))
for ax, k, letra in zip(axes[:2], ["alto", "bajo"], "ab"):
    ax.imshow(rgb(datos[k]), extent=ext, interpolation="nearest")
    ax.contour(cx, cy, mangle.astype(float), levels=[0.5], colors="#ffff00", linewidths=0.4)
    ax.plot(ax_aoi, ay_aoi, color="white", lw=1.0)
    ax.set_title(f"({letra}) Descending track 083, {ESCENAS[k][1]}, 18:27 local", fontsize=9.5)
    ax.set_xlabel("UTM 18N easting (km)"); ax.set_ylabel("northing (km)")
hA, hB = datos["alto"]["hh"], datos["bajo"]["hh"]
n, m = min(hA.shape[0], hB.shape[0]), min(hA.shape[1], hB.shape[1])
dif = hA[:n, :m] - hB[:n, :m]
im = axes[2].imshow(dif, extent=ext, cmap="RdBu_r", vmin=-3, vmax=3, interpolation="nearest")
axes[2].contour(cx, cy, mangle.astype(float), levels=[0.5], colors="k", linewidths=0.4)
axes[2].plot(ax_aoi, ay_aoi, color="k", lw=1.0)
axes[2].set_title("(c) HH difference, high river − lower river (dB)", fontsize=9.5); axes[2].set_xlabel("UTM 18N easting (km)")
fig.colorbar(im, ax=axes[2], fraction=0.046, pad=0.02, label="dB")
dm = dif[mangle[:n, :m] & np.isfinite(dif)]
print("diferencia HH sobre manglar: mediana %.2f dB, p25 %.2f, p75 %.2f, n %d" % (np.median(dm), np.percentile(dm, 25), np.percentile(dm, 75), dm.size), flush=True)
fig.suptitle("NISAR GCOV σ⁰ over the Ciénaga Grande de Santa Marta (Beta collection): R = HH, G = HV, B = HH − HV; "
             "yellow/black outline = mangrove (WorldCover ∩ GMW); white/black line = study area", fontsize=10)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_cgsm_radar.png"), dpi=170)
print("fig_cgsm_radar.png", flush=True)

# ---------------------------------------------------------------- figura 2
clases = wc.remap([80, 95, 10, 90, 30, 40, 50, 60, 20], [1, 2, 3, 4, 5, 5, 6, 5, 5], 0)
pal = ["ffffff", "2166ac", "1b7837", "66a61e", "b8860b", "d9d9d9", "762a83"]
wc_png = png_ee(clases, {"min": 0, "max": 6, "palette": pal})
ac_png = png_ee(acuerdo.selfMask(), {"min": 1, "max": 3, "palette": ["fdae61", "abd9e9", "1b7837"]})
fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))
axes[0].imshow(np.ones_like(wc_png[:, :, :3]) * 255, extent=ext); axes[0].imshow(wc_png, extent=ext)
axes[0].set_title("(a) WorldCover 2021 classes inside the study area", fontsize=10)
axes[0].legend(handles=[Patch(color="#2166ac", label="Water"), Patch(color="#1b7837", label="Mangrove"), Patch(color="#66a61e", label="Tree cover (dry forest, control)"),
                        Patch(color="#b8860b", label="Herbaceous wetland"), Patch(color="#d9d9d9", label="Grass, crops, bare"), Patch(color="#762a83", label="Built-up")],
               fontsize=7.5, loc="lower left")
axes[1].imshow(np.ones_like(ac_png[:, :, :3]) * 255, extent=ext); axes[1].imshow(ac_png, extent=ext)
axes[1].set_title("(b) Mangrove extent: WorldCover 2021 vs Global Mangrove Watch 2020", fontsize=10)
axes[1].legend(handles=[Patch(color="#1b7837", label=f"Both ({ha.get(3, 0):,.0f} ha) – reference class"),
                        Patch(color="#fdae61", label=f"WorldCover only ({ha.get(1, 0):,.0f} ha)"),
                        Patch(color="#abd9e9", label=f"GMW only ({ha.get(2, 0):,.0f} ha)")], fontsize=7.5, loc="lower left")
for ax in axes:
    ax.plot(ax_aoi, ay_aoi, color="k", lw=1.0)
    ax.set_xlabel("UTM 18N easting (km)"); ax.set_ylabel("northing (km)")
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_cgsm_referencia.png"), dpi=170)
print("fig_cgsm_referencia.png", flush=True)
