# -*- coding: utf-8 -*-
"""Versiones en falso color de las siete imágenes del flujo (mismas escenas y puntos que
exportar_figuras_flujo.py).

Radar: compuesto RGB dual-pol, R = copolar (dB), G = cruzada (dB), B = copolar − cruzada (dB),
       con estiramiento fijo por canal. Manglar y bosque salen amarillo-verdosos, el agua azul oscuro
       y el humedal herbáceo violeta o azul según su lámina de agua.
Óptico (Sentinel-2, mediana 2025): infrarrojo B8-B4-B3 (vegetación roja) y SWIR B11-B8-B4
       (agua azul, vegetación verde, suelo rosado).

USO: python exportar_falso_color.py
"""
import os
import h5py
import numpy as np
import requests
os.environ["PROJ_DATA"] = os.path.join(os.path.dirname(__import__("rasterio").__file__), "proj_data")
import rasterio
from pyproj import Transformer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import ee

AQUI = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.dirname(AQUI)
H5 = r"D:\TESIS_DATACUBE\NISAR\NISAR_AOI_20251029_083_4.h5"
ee.Initialize(project="basic-buttress-338101")
fuentes = []

with rasterio.open(os.path.join(RADAR, "mapa_doble_rebote_50m.tif")) as src:
    b = src.bounds
tr = Transformer.from_crs("EPSG:32618", "EPSG:4326", always_xy=True)
x0, y0 = tr.transform(b.left, b.bottom)
x1, y1 = tr.transform(b.right, b.top)
caja = ee.Geometry.Rectangle([x0, y0, x1, y1])

# rangos del estiramiento (dB) por canal: copolar, cruzada, diferencia
R_CO, R_X, R_D = (-22, -4), (-30, -10), (3, 14)


def guardar_png(url, nombre):
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    open(os.path.join(AQUI, nombre), "wb").write(r.content)
    print("ok", nombre, len(r.content) // 1024, "kB")


def estirar(a, lo, hi):
    return np.clip((a - lo) / (hi - lo), 0, 1)


# 1. NISAR en falso color
with h5py.File(H5, "r") as h:
    g = h["science/LSAR/GCOV/grids/frequencyA"]
    fac = g["rtcGammaToSigmaFactor"][:]
    hh, hv = g["HHHH"][:] * fac, g["HVHV"][:] * fac
bb = 4


def agg(a):
    ny, nx = (a.shape[0] // bb) * bb, (a.shape[1] // bb) * bb
    return np.nanmean(np.where(np.isfinite(a[:ny, :nx]), a[:ny, :nx], np.nan).reshape(ny // bb, bb, nx // bb, bb), axis=(1, 3))


hh, hv = 10 * np.log10(agg(hh)), 10 * np.log10(agg(hv))
rgb = np.dstack([estirar(hh, *R_CO), estirar(hv, *R_X), estirar(hh - hv, *R_D)])
rgb[~np.isfinite(hh)] = 0
plt.imsave(os.path.join(AQUI, "01_NISAR_falsocolor_D083_2025-10-29.png"), rgb)
fuentes.append("01_NISAR_falsocolor_D083_2025-10-29.png: NISAR GCOV D083 29-oct-2025, RGB = HH (%d a %d dB), HV (%d a %d), HH−HV (%d a %d), 40 m." % (R_CO + R_X + R_D))
print("ok NISAR")


def rgb_gee(co, x, nombre, fuente):
    im = ee.Image.cat(co.unitScale(*R_CO), x.unitScale(*R_X), co.subtract(x).unitScale(*R_D)).clamp(0, 1).rename(["R", "G", "B"])
    url = im.clip(caja).getThumbURL({"min": 0, "max": 1, "dimensions": 1400, "region": caja, "format": "png"})
    guardar_png(url, nombre)
    fuentes.append(fuente)


# 2. Sentinel-1 VV/VH
s1 = ee.Image((ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(caja).filter(ee.Filter.eq("instrumentMode", "IW"))
               .filter(ee.Filter.eq("relativeOrbitNumber_start", 142)).filterDate("2026-01-05", "2026-01-20").sort("system:time_start")).first())
rgb_gee(s1.select("VV"), s1.select("VH"), "02_Sentinel1_falsocolor_D142_2026-01-09.png",
        "02_Sentinel1_falsocolor_D142_2026-01-09.png: Sentinel-1 GRD órbita 142, 9-ene-2026, RGB = VV, VH, VV−VH con los mismos rangos.")

# 3. ALOS-2 HH/HV del 2-dic-2025
al = ee.ImageCollection("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR").filterBounds(caja).filterDate("2025-12-02", "2025-12-03")


def db(band):
    return al.select(band).mosaic().pow(2).log10().multiply(10).subtract(83)


rgb_gee(db("HH"), db("HV"), "03_ALOS2_falsocolor_ScanSAR_2025-12-02.png",
        "03_ALOS2_falsocolor_ScanSAR_2025-12-02.png: ALOS-2 ScanSAR 2-dic-2025, RGB = HH, HV, HH−HV (σ⁰ = 10 log10(DN²) − 83), mismos rangos.")

# 4-7. Sentinel-2 en infrarrojo y SWIR
puntos = {"04_agua_abierta": (-74.5456, 10.7390), "05_humedal_herbaceo": (-74.5833, 10.8964),
          "06_manglar": (-74.4683, 10.7144), "07_bosque_control": (-74.1997, 11.0740)}


def mascara(im):
    scl = im.select("SCL")
    return im.updateMask(scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11)))


s2 = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(caja).filterDate("2025-01-01", "2026-01-01")
      .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30)).map(mascara).median())
for nombre, (lon, lat) in puntos.items():
    reg = ee.Geometry.Point([lon, lat]).buffer(750).bounds()
    for tag, bandas, mx in [("infrarrojo", ["B8", "B4", "B3"], [4500, 2500, 2500]), ("swir", ["B11", "B8", "B4"], [3500, 4500, 2500])]:
        url = s2.select(bandas).clip(reg).getThumbURL({"min": 0, "max": mx, "gamma": 1.1, "dimensions": 600, "region": reg, "format": "png"})
        f = "%s_%s_S2_2025.png" % (nombre, tag)
        guardar_png(url, f)
        fuentes.append("%s: Sentinel-2 mediana 2025, bandas %s, 1,5 km centrado en %.4f, %.4f." % (f, "-".join(bandas), lon, lat))

with open(os.path.join(AQUI, "FUENTES.txt"), "a", encoding="utf-8") as fh:
    fh.write("\nVersiones en falso color (exportar_falso_color.py):\n" + "\n".join(fuentes) + "\n")
print("listo")
