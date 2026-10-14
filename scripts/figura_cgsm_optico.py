# -*- coding: utf-8 -*-
"""Genera la comparación óptica y radar de las dos adquisiciones NISAR de la Figura 9 del informe
(CGSM).

La figura combina Sentinel-2 en color natural (B4, B3, B2) e infrarrojo color (B8, B4, B3) con
las composiciones NISAR de las mismas fechas, 4 de diciembre de 2025 y 9 de enero de 2026.
Sentinel-2 usa COPERNICUS/S2_SR_HARMONIZED y la mediana de las adquisiciones dentro de 10 días
de cada fecha NISAR, enmascaradas con Cloud Score+ (cs >= 0,60). Además de la figura, el script
calcula el NDVI mediano del manglar de consenso y la proporción de agua abierta dentro del área
de estudio.

SALIDAS
- fig_cgsm_optico_radar.png
- cgsm_optico_resumen.csv

USO
    python figura_cgsm_optico.py
"""
import io
import json
import os

import ee
import h5py
import numpy as np
import pandas as pd
import requests
from PIL import Image
from pyproj import Transformer
from scipy.ndimage import uniform_filter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR = r"D:\TESIS_DATACUBE\NISAR"
CACHE = os.path.join(AQUI, "cache_cgsm_radar_fig.npz")
RESUMEN = os.path.join(AQUI, "cgsm_optico_resumen.csv")
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
EPSG = 32618
PASO = 6
AOI_GEOJSON = r"C:\LINA\UNAL 2626-1\AVANCE TESIS\AOI\AOI_tesis_CGSM_v1.geojson"
FECHAS = {"alto": ("NISAR_AOI_20251204_083_4.h5", "2025-12-04", "4 Dec 2025, river level 2.67 m"),
          "bajo": ("NISAR_AOI_20260109_083_4.h5", "2026-01-09", "9 Jan 2026, river level 1.69 m")}
COMBOS = {"rgb": ({"bands": ["B4", "B3", "B2"], "min": [150, 250, 350], "max": [1800, 1800, 1800]},
                  "Sentinel-2 natural colour (B4, B3, B2)"),
          "cir": ({"bands": ["B8", "B4", "B3"], "min": [200, 150, 250], "max": [5000, 2000, 2000]},
                  "Sentinel-2 colour infrared (B8, B4, B3)")}


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


def rgb_radar(d):
    def esc(a, lo, hi):
        return np.clip((a - lo) / (hi - lo), 0, 1)
    im = np.dstack([esc(d["hh"], -20, -2), esc(d["hv"], -26, -8), esc(d["hh"] - d["hv"], 2, 12)])
    im[~np.isfinite(d["hh"])] = 1
    return im


if os.path.exists(CACHE):
    z = np.load(CACHE)
    radar = {k: dict(hh=z[k + "_hh"], hv=z[k + "_hv"], x=z["x"], y=z["y"]) for k in FECHAS}
    print("radar desde la copia en C:", flush=True)
elif os.path.isdir(DIR):
    radar = {k: leer(v[0]) for k, v in FECHAS.items()}
    np.savez_compressed(CACHE, x=radar["alto"]["x"], y=radar["alto"]["y"],
                        **{k + "_" + b: radar[k][b] for k in radar for b in ("hh", "hv")})
    print("radar leído de D: y copiado a C:", flush=True)
else:
    raise SystemExit("ABORTA: D: desmontado y sin copia del radar en C:")
gx, gy = radar["alto"]["x"], radar["alto"]["y"]
x0, x1, y0, y1 = float(gx[0]), float(gx[-1]), float(gy[-1]), float(gy[0])
ext = [x0 / 1000, x1 / 1000, y0 / 1000, y1 / 1000]

gj = json.load(open(AOI_GEOJSON, encoding="utf-8"))
t = Transformer.from_crs("EPSG:4326", f"EPSG:{EPSG}", always_xy=True)
ax_aoi, ay_aoi = zip(*[t.transform(lon, lat) for lon, lat in gj["features"][0]["geometry"]["coordinates"][0]])
ax_aoi, ay_aoi = np.array(ax_aoi) / 1000, np.array(ay_aoi) / 1000

ee.Initialize(project="basic-buttress-338101")
aoi = ee.Geometry(gj["features"][0]["geometry"])
region = ee.Geometry.Rectangle([x0, y0, x1, y1], f"EPSG:{EPSG}", False)
dims = "%dx%d" % (len(gx), len(gy))
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = (ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3")
       .filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0))
consenso = wc.eq(95).And(gmw)


def png_ee(img, vis, cache):
    ruta = os.path.join(AQUI, cache)
    if os.path.exists(ruta):
        return np.array(Image.open(ruta).convert("RGBA"))
    url = img.getThumbURL(dict(vis, region=region, dimensions=dims, crs=f"EPSG:{EPSG}", format="png"))
    im = Image.open(io.BytesIO(requests.get(url, timeout=600).content)).convert("RGBA")
    im.save(ruta)
    return np.array(im)


mangle = png_ee(consenso.clip(aoi).selfMask(), {"min": 0, "max": 1, "palette": ["000000", "ffffff"]},
                "cache_cgsm_mangle.png")[:, :, 3] > 0
cx, cy = np.linspace(ext[0], ext[1], mangle.shape[1]), np.linspace(ext[3], ext[2], mangle.shape[0])

csp = ee.ImageCollection("GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED")
optico, filas = {}, (pd.read_csv(RESUMEN).to_dict("records") if os.path.exists(RESUMEN) else [])
for k, (_, fecha, _) in FECHAS.items():
    f = ee.Date(fecha)
    col = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(region)
           .filterDate(f.advance(-10, "day"), f.advance(11, "day")).linkCollection(csp, ["cs"]))
    med = col.map(lambda im: im.updateMask(im.select("cs").gte(0.60))).median()
    for c, (vis, _) in COMBOS.items():
        optico[(k, c)] = png_ee(med, vis, f"cache_cgsm_s2_{k}_{c}.png")
        print("óptico", k, c, flush=True)
    if not any(r["pass"] == fecha for r in filas):
        dias = sorted(set(col.aggregate_array("system:time_start").map(
            lambda ms: ee.Date(ms).format("YYYY-MM-dd")).getInfo()))
        ndvi = med.normalizedDifference(["B8", "B4"]).rename("ndvi")
        mndwi = med.normalizedDifference(["B3", "B11"]).rename("mndwi")
        n = ndvi.updateMask(consenso).reduceRegion(
            ee.Reducer.median().combine(ee.Reducer.count(), "", True), aoi, 20, maxPixels=1e10).getInfo()
        agua = (ee.Image.pixelArea().divide(1e6).updateMask(mndwi.gt(0))
                .reduceRegion(ee.Reducer.sum(), aoi, 20, maxPixels=1e10).getInfo()["area"])
        valido = (ee.Image.pixelArea().divide(1e6).updateMask(mndwi.mask())
                  .reduceRegion(ee.Reducer.sum(), aoi, 20, maxPixels=1e10).getInfo()["area"])
        filas.append({"pass": fecha, "s2_dates": " ".join(dias), "n_s2_dates": len(dias),
                      "ndvi_mangrove_median": round(n["ndvi_median"], 3), "mangrove_px_20m": n["ndvi_count"],
                      "open_water_km2": round(agua, 1), "valid_area_km2": round(valido, 1)})
pd.DataFrame(filas).to_csv(RESUMEN, index=False)

fig, axes = plt.subplots(2, 3, figsize=(17.5, 10.2))
for i, k in enumerate(("alto", "bajo")):
    for j, (c, (_, titulo)) in enumerate(COMBOS.items()):
        a = axes[i, j]
        a.imshow(np.ones_like(optico[(k, c)][:, :, :3]) * 255, extent=ext); a.imshow(optico[(k, c)], extent=ext)
        a.set_title(f"{titulo}, ±10 days of {FECHAS[k][2].split(',')[0]}", fontsize=9.5)
    b = axes[i, 2]
    b.imshow(rgb_radar(radar[k]), extent=ext, interpolation="nearest")
    b.set_title(f"NISAR (R = HH, G = HV, B = HH − HV), {FECHAS[k][2]}", fontsize=9.5)
    for ax in axes[i]:
        ax.contour(cx, cy, mangle.astype(float), levels=[0.5], colors="#ffff00", linewidths=0.4)
        ax.plot(ax_aoi, ay_aoi, color="white", lw=1.0)
        ax.set_xlabel("UTM 18N easting (km)"); ax.set_ylabel("northing (km)")
fig.suptitle("Optical and L-band views of the CGSM on the two dates of Figure 7; yellow outline = mangrove (WorldCover ∩ GMW), white line = study area", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_cgsm_optico_radar.png"), dpi=150)
print("FIGURA: fig_cgsm_optico_radar.png", flush=True)
