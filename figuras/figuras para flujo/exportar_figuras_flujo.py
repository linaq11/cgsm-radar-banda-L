# -*- coding: utf-8 -*-
"""Exporta siete imágenes reales para el diagrama de flujo: una pasada de NISAR (HH), una de
ALOS-2 (HH), una de Sentinel-1 (VV) sobre la caja de la CGSM, y cuatro recortes Sentinel-2 en
color verdadero (1,5 km de lado) centrados en puntos reales de cada cobertura: agua abierta,
humedal herbáceo y manglar desde la muestra 2025 (confianza alta, sin borde), y bosque de
control desde la malla de clases a 50 m. Escribe también FUENTES.txt con fecha y origen.

USO: python exportar_figuras_flujo.py      (Earth Engine autenticado; NISAR desde D:)
"""
import os
import io
import h5py
import numpy as np
import pandas as pd
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

# caja de la CGSM en lon/lat desde la malla de 50 m
with rasterio.open(os.path.join(RADAR, "mapa_doble_rebote_50m.tif")) as src:
    b = src.bounds
    cl = src.read(4)
    # píxel de bosque con más bosque alrededor (ventana de 41 x 41 a 50 m, 2 km de lado)
    from scipy.ndimage import uniform_filter
    bosque = (cl == 2).astype(float)
    vecindad = uniform_filter(bosque, size=41, mode="constant")
    vecindad[cl != 2] = -1
    i_b, j_b = np.unravel_index(np.argmax(vecindad), vecindad.shape)
    bx, by = src.xy(i_b, j_b)
    print("bosque: %.0f %% de bosque en 2 km alrededor" % (100 * vecindad[i_b, j_b]))
tr = Transformer.from_crs("EPSG:32618", "EPSG:4326", always_xy=True)
x0, y0 = tr.transform(b.left, b.bottom)
x1, y1 = tr.transform(b.right, b.top)
caja = ee.Geometry.Rectangle([x0, y0, x1, y1])
blon, blat = tr.transform(bx, by)


def guardar_png(url, nombre):
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    open(os.path.join(AQUI, nombre), "wb").write(r.content)
    print("ok", nombre, len(r.content) // 1024, "kB")


# 1. NISAR HH desde el h5 local
with h5py.File(H5, "r") as h:
    g = h["science/LSAR/GCOV/grids/frequencyA"]
    hh = g["HHHH"][:] * g["rtcGammaToSigmaFactor"][:]
bb = 4
ny, nx = (hh.shape[0] // bb) * bb, (hh.shape[1] // bb) * bb
hh = 10 * np.log10(np.nanmean(np.where(np.isfinite(hh[:ny, :nx]), hh[:ny, :nx], np.nan).reshape(ny // bb, bb, nx // bb, bb), axis=(1, 3)))
plt.imsave(os.path.join(AQUI, "01_NISAR_HH_D083_2025-10-29.png"), hh, cmap="gray", vmin=-25, vmax=-3)
fuentes.append("01_NISAR_HH_D083_2025-10-29.png: NISAR L2 GCOV, traza D083, 29-oct-2025, sigma0 HH en dB (-25 a -3), 40 m, caja de la CGSM.")
print("ok NISAR")

# 2. Sentinel-1 VV, una pasada descendente de la órbita 142
s1 = (ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(caja).filter(ee.Filter.eq("instrumentMode", "IW"))
      .filter(ee.Filter.eq("relativeOrbitNumber_start", 142)).filterDate("2026-01-05", "2026-01-20").sort("system:time_start"))
im = ee.Image(s1.first())
fecha = ee.Date(im.get("system:time_start")).format("YYYY-MM-dd").getInfo()
url = im.select("VV").clip(caja).getThumbURL({"min": -25, "max": -3, "dimensions": 1400, "region": caja, "format": "png"})
guardar_png(url, "02_Sentinel1_VV_D142_%s.png" % fecha)
fuentes.append("02_Sentinel1_VV_D142_%s.png: COPERNICUS/S1_GRD, IW, órbita relativa 142, VV en dB (-25 a -3), caja de la CGSM." % fecha)

# 3. ALOS-2 HH, una fecha de ScanSAR
al = ee.ImageCollection("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR").filterBounds(caja).filterDate("2025-10-01", "2026-10-01").sort("system:time_start")
fechas = sorted(set(ee.List(al.aggregate_array("system:time_start")).map(lambda t: ee.Date(t).format("YYYY-MM-dd")).getInfo()))
area_caja = caja.area(1).getInfo()
for fecha in fechas:                      # primera fecha cuyo mosaico cubre la caja completa
    mismo_dia = al.filterDate(fecha, ee.Date(fecha).advance(1, "day"))
    cubierto = ee.Image.constant(1).updateMask(mismo_dia.select("HH").mosaic().mask()).multiply(ee.Image.pixelArea()) \
        .reduceRegion(ee.Reducer.sum(), caja, 500, maxPixels=1e9).getInfo()["constant"]
    print("ALOS-2", fecha, "cobertura %.1f %%" % (100 * cubierto / area_caja))
    if cubierto / area_caja >= 0.99:
        break
db = mismo_dia.select("HH").mosaic().pow(2).log10().multiply(10).subtract(83)
url = db.clip(caja).getThumbURL({"min": -25, "max": -3, "dimensions": 1400, "region": caja, "format": "png"})
guardar_png(url, "03_ALOS2_HH_ScanSAR_%s.png" % fecha)
fuentes.append("03_ALOS2_HH_ScanSAR_%s.png: JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR, HH calibrado con sigma0 = 10 log10(DN^2) - 83 dB (-25 a -3), caja de la CGSM; mosaico de las escenas de esa fecha." % fecha)

# 4-7. recortes Sentinel-2 en color verdadero de 2025
pts = pd.read_csv(os.path.join(RADAR, "clave_muestra2025_puntos.csv"))
pts = pts[pts.borde_final == "no"].copy()
pts["conf"] = pts.confianza.str[0].astype(int)
sel = {}
for c in ["agua", "humedal_herbaceo", "manglar_intacto"]:
    s = pts[pts.clase_final == c].sort_values(["conf", "id"], ascending=[False, True]).iloc[0]
    sel[c] = (float(s.lon), float(s.lat), int(s.id), s.confianza)
sel["bosque_control"] = (blon, blat, None, "malla de clases a 50 m, clase 2 (bosque de WorldCover fuera del área de estudio)")


def mascara(im):
    scl = im.select("SCL")
    return im.updateMask(scl.neq(3).And(scl.neq(8)).And(scl.neq(9)).And(scl.neq(10)).And(scl.neq(11)))


s2 = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(caja).filterDate("2025-01-01", "2026-01-01")
      .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 30)).map(mascara).select(["B4", "B3", "B2"]).median())
nombres = {"agua": "04_agua_abierta", "humedal_herbaceo": "05_humedal_herbaceo", "manglar_intacto": "06_manglar", "bosque_control": "07_bosque_control"}
for c, (lon, lat, pid, conf) in sel.items():
    reg = ee.Geometry.Point([lon, lat]).buffer(750).bounds()
    url = s2.clip(reg).getThumbURL({"min": 0, "max": 2500, "gamma": 1.2, "dimensions": 600, "region": reg, "format": "png"})
    nombre = "%s_S2_2025_%.4f_%.4f.png" % (nombres[c], lon, lat)
    guardar_png(url, nombre)
    fuentes.append("%s: Sentinel-2 SR armonizado, mediana 2025 sin nubes, color verdadero B4-B3-B2, 1,5 km de lado centrado en %.5f, %.5f (%s)." % (
        nombre, lon, lat, "punto %d de la muestra 2025, %s" % (pid, conf) if pid else conf))

open(os.path.join(AQUI, "FUENTES.txt"), "w", encoding="utf-8").write(
    "Imágenes reales para el diagrama de flujo del informe de radar. Generadas con exportar_figuras_flujo.py.\n\n" + "\n".join(fuentes) + "\n")
print("listo")
