# -*- coding: utf-8 -*-
"""Primer perfil de retrodispersion NISAR sobre Bahia de Malaga: mediana de HH, HV y
HH-HV (dB, sigma cero) por cobertura de WorldCover 2021 y por escena, con el angulo
de incidencia. Valida ademas los recortes (proyeccion, tamano, cobertura).

Coberturas: manglar (95), agua (80), bosque (10), humedal herbaceo (90).
Puntos: 400 por clase, muestreados en Earth Engine dentro de la caja del recorte.
"""
import glob
import json
import os
import sys

import ee
import h5py
import numpy as np
import pandas as pd
from pyproj import Transformer

DIR = r"D:\TESIS_DATACUBE\NISAR_PACIFICO"
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
CLASES = {95: "manglar", 80: "agua", 10: "bosque", 90: "humedal_herbaceo"}
if not os.path.isdir(DIR):
    sys.exit("ABORTA: D: desmontado")
rutas = sorted(glob.glob(os.path.join(DIR, "NISAR_MALAGA_*.h5")))
print("recortes:", [os.path.basename(r) for r in rutas], flush=True)

# --- puntos por clase desde WorldCover, dentro de la caja del AOI
ee.Initialize(project="basic-buttress-338101")
caja = ee.Geometry.Rectangle([-77.40, 3.80, -77.10, 4.10])
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
pts = wc.stratifiedSample(numPoints=400, classBand="Map", region=caja, scale=10, seed=42,
                          classValues=list(CLASES), classPoints=[400] * len(CLASES), geometries=True, tileScale=4)
feats = pts.getInfo()["features"]
df = pd.DataFrame([dict(lon=f["geometry"]["coordinates"][0], lat=f["geometry"]["coordinates"][1], clase=CLASES[f["properties"]["Map"]])
                   for f in feats if f["properties"]["Map"] in CLASES])

# --- segunda mascara de manglar, independiente: Global Mangrove Watch v3, extension 2020
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3") \
    .filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0).rename("gmw")
wc95 = wc.eq(95)
ha = ee.Image.pixelArea().divide(1e4)
area = {k: v.reduceRegion(ee.Reducer.sum(), caja, 30, maxPixels=1e9).getInfo()["area"]
        for k, v in {"gmw": ha.updateMask(gmw), "wc": ha.updateMask(wc95), "ambos": ha.updateMask(gmw.And(wc95))}.items()}
print("manglar en la caja: GMW 2020 %.0f ha | WorldCover 2021 %.0f ha | en ambos %.0f ha (%.0f %% del GMW, %.0f %% del WC)"
      % (area["gmw"], area["wc"], area["ambos"], 100 * area["ambos"] / area["gmw"], 100 * area["ambos"] / area["wc"]), flush=True)
# puntos donde los dos productos coinciden en manglar, y donde solo uno lo dice
consenso = gmw.And(wc95).rename("m").selfMask()
solo_gmw = gmw.And(wc95.Not()).rename("m").selfMask()
for nombre, mask in (("manglar_gmw_y_wc", consenso), ("manglar_solo_gmw", solo_gmw)):
    fs = mask.stratifiedSample(numPoints=400, classBand="m", region=caja, scale=10, seed=42, geometries=True, tileScale=4).getInfo()["features"]
    df = pd.concat([df, pd.DataFrame([dict(lon=f["geometry"]["coordinates"][0], lat=f["geometry"]["coordinates"][1], clase=nombre) for f in fs])], ignore_index=True)
CLASES = dict(CLASES, **{"manglar_gmw_y_wc": "manglar_gmw_y_wc", "manglar_solo_gmw": "manglar_solo_gmw"})
print("puntos por clase:", df.clase.value_counts().to_dict(), flush=True)


def db(a):
    out = np.full(a.shape, np.nan, dtype="float32")
    m = np.isfinite(a) & (a > 0)
    out[m] = 10.0 * np.log10(a[m])
    return out


filas = []
for r in rutas:
    with h5py.File(r, "r") as h:
        epsg = int(h.attrs["epsg"])
        gr = h[GRUPO]
        xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
        fac = gr["rtcGammaToSigmaFactor"][:]
        hh = db(gr["HHHH"][:] * fac)
        hv = db(gr["HVHV"][:] * fac)
        inc = None
        ri = "science/LSAR/GCOV/metadata/radarGrid/incidenceAngle"
        if ri in h:
            inc = h[ri][:]
            ix, iy = h["science/LSAR/GCOV/metadata/radarGrid/xCoordinates"][:], h["science/LSAR/GCOV/metadata/radarGrid/yCoordinates"][:]
        origen = h.attrs["origen"]
    t = Transformer.from_crs("EPSG:4326", "EPSG:%d" % epsg, always_xy=True)
    ux, uy = t.transform(df.lon.to_numpy(), df.lat.to_numpy())
    i = np.clip(np.searchsorted(xc, ux) - 1, 0, len(xc) - 1)
    j = np.clip(len(yc) - np.searchsorted(yc[::-1], uy) - 1, 0, len(yc) - 1)
    vhh, vhv = hh[j, i], hv[j, i]
    val = np.isfinite(vhh)
    print("%s | EPSG %d | %dx%d px | valido %.1f %% | puntos con valor %d/%d" % (
        os.path.basename(r), epsg, hh.shape[1], hh.shape[0], 100 * np.isfinite(hh).mean(), val.sum(), len(df)), flush=True)
    if inc is not None:
        ang = inc[inc.shape[0] // 2] if inc.ndim == 3 else inc
        ii = np.clip(np.searchsorted(ix, ux) - 1, 0, len(ix) - 1)
        jj = np.clip(len(iy) - np.searchsorted(iy[::-1], uy) - 1, 0, len(iy) - 1)
        vinc = ang[jj, ii]
    else:
        vinc = np.full(len(df), np.nan)
    fecha = os.path.basename(r).split("_")[2]
    for c in CLASES.values():
        m = (df.clase == c).to_numpy() & val
        filas.append(dict(escena=fecha, clase=c, n=int(m.sum()), HH=np.nanmedian(vhh[m]), HV=np.nanmedian(vhv[m]),
                          HHmHV=np.nanmedian((vhh - vhv)[m]), inc=np.nanmedian(vinc[m]),
                          HH_p25=np.nanpercentile(vhh[m], 25), HH_p75=np.nanpercentile(vhh[m], 75)))
out = pd.DataFrame(filas)

# --- Dynamic World: probabilidad de vegetacion inundada y de agua en los mismos puntos,
# con las imagenes de +-10 dias alrededor de cada escena NISAR (el Pacifico es nuboso)
fc = ee.FeatureCollection([ee.Feature(ee.Geometry.Point([float(a), float(b)]), {"clase": c}) for a, b, c in zip(df.lon, df.lat, df.clase)])
dw_filas = []
for fecha in sorted(out.escena.unique()):
    d0 = ee.Date.parse("YYYYMMdd", fecha)
    dw = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filterBounds(caja).filterDate(d0.advance(-10, "day"), d0.advance(11, "day"))
    n = dw.size().getInfo()
    if n == 0:
        print("Dynamic World +-10 dias de %s: sin imagenes" % fecha, flush=True)
        continue
    comp = dw.select(["flooded_vegetation", "water", "trees"]).mean()
    etiq = dw.select("label").reduce(ee.Reducer.mode()).rename("label")
    m = comp.addBands(etiq).reduceRegions(fc, ee.Reducer.first(), 10).getInfo()["features"]
    t = pd.DataFrame([dict(clase=f["properties"]["clase"], fv=f["properties"].get("flooded_vegetation"), agua=f["properties"].get("water"),
                           arboles=f["properties"].get("trees"), label=f["properties"].get("label")) for f in m]).dropna(subset=["fv"])
    for c, g in t.groupby("clase"):
        dw_filas.append(dict(escena=fecha, clase=c, n_dw=int(len(g)), imagenes_dw=n, p_veg_inundada=round(g.fv.mean(), 3),
                             p_agua=round(g.agua.mean(), 3), p_arboles=round(g.arboles.mean(), 3),
                             frac_label_veg_inundada=round((g.label == 2).mean(), 3)))   # label 2 = flooded_vegetation
    print("Dynamic World +-10 dias de %s: %d imagenes, %d puntos con dato" % (fecha, n, len(t)), flush=True)
if dw_filas:
    dwdf = pd.DataFrame(dw_filas)
    out = out.merge(dwdf, on=["escena", "clase"], how="left")
    print("\n== Dynamic World: probabilidad media de vegetacion inundada / agua por clase ==")
    print(dwdf.pivot(index="clase", columns="escena", values="p_veg_inundada").round(2).to_string())
    print("\nfraccion de puntos etiquetados vegetacion inundada:")
    print(dwdf.pivot(index="clase", columns="escena", values="frac_label_veg_inundada").round(2).to_string())
out.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "perfil_pacifico_nisar.csv"), index=False)
print("\n== mediana por clase y escena (dB, sigma cero) ==")
print(out.pivot(index="clase", columns="escena", values="HH").round(1).to_string())
print("\nHV:"); print(out.pivot(index="clase", columns="escena", values="HV").round(1).to_string())
print("\nHH-HV:"); print(out.pivot(index="clase", columns="escena", values="HHmHV").round(1).to_string())
print("\nincidencia mediana por clase:", out.groupby("clase").inc.median().round(1).to_dict())
