# -*- coding: utf-8 -*-
"""Serie larga de ALOS-2 PALSAR-2 ScanSAR sobre la CGSM, 2014 a 2026, por pasada y clase.

PROPÓSITO
    Extender a toda la serie disponible la prueba hidrológica del informe 1 (resta copolar manglar menos bosque
    frente al nivel del río Magdalena), con un solo producto consistente (JAXA L2.2 ScanSAR, 25 m, HH y HV), sin
    el cambio de versión que confunde la serie NISAR de la CGSM. Sirve a la vez como capa de banda L 2015 a 2025
    para el cubo de la tesis.
MÉTODO
    Mismas regiones y mismos 400 puntos por clase que cgsm_temporada.py (WorldCover 2021 y GMW 2020 sobre el AOI de
    la tesis; bosque seco de control en la caja del cubo, fuera del AOI; semilla 42). Para cada pasada (escenas de un
    mismo path con menos de 5 minutos de separación se funden en mosaico) se exige cobertura del 90 % del AOI y se
    toma la mediana por clase de HH, HV y HH − HV en dB: sigma cero = 10·log10(DN²) − 83 (JAXA), o gamma cero con
    la corrección por incidencia local (banda LIN en centésimas de grado) si RADAR_MAGNITUD=gamma0.
SALIDAS
    alos2_serie_cgsm_inventario.csv   todas las escenas: fecha, path, dirección, cobertura del AOI
    alos2_serie_cgsm.csv              una fila por pasada y clase, igual que cgsm_temporada_alos2.csv
USO
    python alos2_serie_cgsm.py [--solo-inventario]
"""
import os
import sys
GAMMA0 = os.environ.get("RADAR_MAGNITUD", "sigma0").lower() == "gamma0"
SUF = "_gamma0" if GAMMA0 else ""

import ee
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
T0, T1 = "2014-08-01", "2026-12-31"
ee.Initialize(project="basic-buttress-338101")

AOI = ee.FeatureCollection("projects/basic-buttress-338101/assets/AOI_tesis_CGSM_v1").geometry()
CONTROL = ee.Image("projects/basic-buttress-338101/assets/cgsm_datacube_v1/s2/202512").geometry()
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
mascaras = {"manglar": wc.eq(95).And(gmw), "bosque": wc.eq(10), "humedal_herbaceo": wc.eq(90), "agua": wc.eq(80)}
REGION = {"manglar": AOI, "humedal_herbaceo": AOI, "agua": AOI, "bosque": CONTROL}


def puntos():
    pts = []
    for nombre, m in mascaras.items():
        fs = m.rename("m").selfMask().stratifiedSample(numPoints=400, classBand="m", region=REGION[nombre], scale=10, seed=42, geometries=True, tileScale=4).getInfo()["features"]
        pts += [dict(lon=f["geometry"]["coordinates"][0], lat=f["geometry"]["coordinates"][1], clase=nombre) for f in fs]
    df = pd.DataFrame(pts)
    print("puntos:", df.clase.value_counts().to_dict(), flush=True)
    return df, ee.FeatureCollection([ee.Feature(ee.Geometry.Point([r.lon, r.lat]), {"clase": r.clase}) for r in df.itertuples()])


def a_db(im):
    s = im.select(["HH", "HV"]).toFloat().pow(2).log10().multiply(10).add(-83)
    if GAMMA0:
        s = s.subtract(im.select("LIN").multiply(0.01 * np.pi / 180).cos().log10().multiply(10))
    return s.updateMask(im.select("HH").gt(0))


col = ee.ImageCollection("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR").filterBounds(AOI).filterDate(T0, T1).filter(ee.Filter.listContains("Polarizations", "HV"))
meta = col.reduceColumns(ee.Reducer.toList(4), ["system:index", "system:time_start", "PassDirection", "RSP_Path_Number"]).get("list").getInfo()
meta = sorted(meta, key=lambda x: x[1])
pasadas = []
for idx, t0, direccion, orb in meta:
    if pasadas and pasadas[-1]["orb"] == orb and abs(t0 - pasadas[-1]["t0"]) < 5 * 60 * 1000:
        pasadas[-1]["ids"].append(idx)
    else:
        pasadas.append(dict(ids=[idx], t0=t0, direccion=str(direccion)[0].upper(), orb=orb))
print("ALOS-2 ScanSAR sobre el AOI: %d escenas, %d pasadas, %s a %s" % (len(meta), len(pasadas), pd.Timestamp(meta[0][1], unit="ms").date(), pd.Timestamp(meta[-1][1], unit="ms").date()), flush=True)

# 1. Inventario con cobertura del AOI
inv = []
for ps in pasadas:
    img = ee.ImageCollection([a_db(ee.Image("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR/" + i)) for i in ps["ids"]]).mosaic()
    cob = img.select("HH").mask().reduceRegion(ee.Reducer.mean(), AOI, 300, maxPixels=1e9).getInfo().get("HH") or 0
    t_utc = pd.Timestamp(ps["t0"], unit="ms")
    ps["cob"] = cob
    inv.append(dict(escena=ps["ids"][0], n_escenas=len(ps["ids"]), fecha_utc=t_utc, hora_local=(t_utc - pd.Timedelta(hours=5)).strftime("%H:%M"),
                    direccion=ps["direccion"], path=ps["orb"], traza="%s%s" % (ps["direccion"], ps["orb"]), cobertura_aoi=round(cob, 3)))
inv = pd.DataFrame(inv)
inv.to_csv(os.path.join(AQUI, "alos2_serie_cgsm_inventario.csv"), index=False)
inv["anio"] = inv.fecha_utc.dt.year
print("\nPasadas con cobertura >= 90 % del AOI, por año y traza:")
print(pd.crosstab(inv[inv.cobertura_aoi >= 0.9].anio, inv[inv.cobertura_aoi >= 0.9].traza).to_string(), flush=True)
if "--solo-inventario" in sys.argv:
    sys.exit(0)

# 2. Muestreo por pasada y clase
df_pts, fc = puntos()
filas = []
for ps in pasadas:
    if ps["cob"] < 0.9:
        continue
    img = ee.ImageCollection([a_db(ee.Image("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR/" + i)) for i in ps["ids"]]).mosaic()
    t_utc = pd.Timestamp(ps["t0"], unit="ms")
    m = img.reduceRegions(fc, ee.Reducer.first(), 25).getInfo()["features"]
    t = pd.DataFrame([dict(clase=f["properties"]["clase"], co=f["properties"].get("HH"), x=f["properties"].get("HV")) for f in m]).dropna()
    for c, g in t.groupby("clase"):
        filas.append(dict(sensor="ALOS2", escena=ps["ids"][0], fecha_utc=t_utc, traza="%s%s" % (ps["direccion"], ps["orb"]), hora_local=(t_utc - pd.Timedelta(hours=5)).strftime("%H:%M"),
                          clase=c, n=len(g), CO=g.co.median(), X=g.x.median(), COmX=(g.co - g.x).median()))
    print("   %s %s%s | %d puntos" % (t_utc.strftime("%Y-%m-%d %H:%M"), ps["direccion"], ps["orb"], len(t)), flush=True)
    pd.DataFrame(filas).to_csv(os.path.join(AQUI, "alos2_serie_cgsm%s.csv" % SUF), index=False)
print("FIN: alos2_serie_cgsm%s.csv, %d filas" % (SUF, len(filas)), flush=True)
