# -*- coding: utf-8 -*-
"""Análisis inicial de la respuesta hidrológica de las coberturas de la CGSM.

PROPÓSITO
Evaluar la relación entre la retrodispersión SAR y la precipitación acumulada en los 30 días
anteriores a cada adquisición, obtenida de ERA5-Land. Se conserva la partición estacional entre
época seca y húmeda como descripción complementaria.

MÉTODO
Para cada sensor y trayectoria se calcula la mediana de retrodispersión por cobertura. La señal
del manglar se analiza de forma individual y relativa al bosque no inundable mediante la
diferencia manglar - bosque. Se usan cuatro coberturas de referencia, manglar, bosque no
inundable, humedal herbáceo y agua, con 400 puntos por clase.

SENSORES
- NISAR: HH y HV (recortes locales NISAR_AOI_*.h5).
- Sentinel-1: VV y VH (Earth Engine).
- ALOS-2: HH y HV (Earth Engine).

SALIDAS
- cgsm_temporada_<sensor>.csv
- cgsm_temporada_resumen.csv
- fig_cgsm_temporada.png

USO
    python cgsm_temporada.py
"""
import glob
import os
GAMMA0 = os.environ.get("RADAR_MAGNITUD", "sigma0").lower() == "gamma0"   # gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
SUF = "_gamma0" if GAMMA0 else ""
import sys
from datetime import datetime

import ee
import h5py
import numpy as np
import pandas as pd
from pyproj import Transformer
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
NISAR_DIR = r"D:\TESIS_DATACUBE\NISAR"
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
SENSORES = sys.argv[1:] or ["nisar", "s1", "alos2"]
T0, T1 = "2025-10-01", "2026-09-12"

ee.Initialize(project="basic-buttress-338101")
# Dos regiones, declaradas (antes las cuatro clases se muestreaban sobre la caja del cubo,
# 4.304 km2, sin decirlo: el 39 % de los puntos de agua caia en mar abierto y el 40 % de
# los de humedal fuera del area de estudio).
#   AOI     : el poligono de la tesis, 2.042 km2. Manglar, humedal y agua salen de aqui.
#   CONTROL : la caja del cubo, 4.304 km2. El bosque seco de los piedemontes, que es el
#             control que no se inunda, esta fuera del AOI a proposito.
AOI = ee.FeatureCollection("projects/basic-buttress-338101/assets/AOI_tesis_CGSM_v1").geometry()
CONTROL = ee.Image("projects/basic-buttress-338101/assets/cgsm_datacube_v1/s2/202512").geometry()
aoi = AOI                      # lluvia ERA5-Land y control de cobertura de cada pasada
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
mascaras = {"manglar": wc.eq(95).And(gmw), "bosque": wc.eq(10), "humedal_herbaceo": wc.eq(90), "agua": wc.eq(80)}
REGION = {"manglar": AOI, "humedal_herbaceo": AOI, "agua": AOI, "bosque": CONTROL}
pts = []
for nombre, m in mascaras.items():
    fs = m.rename("m").selfMask().stratifiedSample(numPoints=400, classBand="m", region=REGION[nombre], scale=10, seed=42, geometries=True, tileScale=4).getInfo()["features"]
    pts += [dict(lon=f["geometry"]["coordinates"][0], lat=f["geometry"]["coordinates"][1], clase=nombre) for f in fs]
df_pts = pd.DataFrame(pts)
fc = ee.FeatureCollection([ee.Feature(ee.Geometry.Point([r.lon, r.lat]), {"clase": r.clase}) for r in df_pts.itertuples()])
print("puntos:", df_pts.clase.value_counts().to_dict(), flush=True)

# lluvia diaria ERA5-Land sobre el AOI (mm), para acumular 30 dias antes de cada pasada
era = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR").filterDate("2025-08-01", T1).select("total_precipitation_sum")
ll = era.map(lambda im: ee.Feature(None, {"t": im.get("system:time_start"),
                                          "p": im.reduceRegion(ee.Reducer.mean(), aoi, 10000).get("total_precipitation_sum")}))
ll = pd.DataFrame(ll.reduceColumns(ee.Reducer.toList(2), ["t", "p"]).get("list").getInfo(), columns=["t", "p"])
ll["fecha"] = pd.to_datetime(ll.t, unit="ms").dt.floor("D"); ll["mm"] = ll.p * 1000
ll = ll.sort_values("fecha").set_index("fecha").mm
print("ERA5-Land: %d dias, %s a %s, lluvia total %.0f mm" % (len(ll), ll.index.min().date(), ll.index.max().date(), ll.sum()), flush=True)


def p30(t):
    fin = pd.Timestamp(t).floor("D")
    s = ll[(ll.index > fin - pd.Timedelta(days=30)) & (ll.index <= fin)]
    return float(s.sum()) if len(s) >= 25 else np.nan


def epoca(t):
    return "seca" if pd.Timestamp(t).month in (12, 1, 2, 3, 4) else "humeda"


def db(a):
    out = np.full(a.shape, np.nan, dtype="float32")
    ok = np.isfinite(a) & (a > 0)
    out[ok] = 10.0 * np.log10(a[ok])
    return out


filas = []
# ------------------------------------------------------------------ NISAR local
if "nisar" in SENSORES:
    rutas = sorted(glob.glob(os.path.join(NISAR_DIR, "NISAR_AOI_*.h5")))
    if not rutas:
        print("NISAR: sin recortes en disco (D: desmontado?) - se salta", flush=True)
    for r in rutas:
        with h5py.File(r, "r") as h:
            gr = h[GRUPO]
            xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
            fac = 1.0 if GAMMA0 else gr["rtcGammaToSigmaFactor"][:]
            hh, hv = db(gr["HHHH"][:] * fac), db(gr["HVHV"][:] * fac)
            t0 = h["science/LSAR/identification/zeroDopplerStartTime"][()]; t0 = t0.decode() if isinstance(t0, bytes) else str(t0)
            d0 = h["science/LSAR/identification/orbitPassDirection"][()]; d0 = (d0.decode() if isinstance(d0, bytes) else str(d0))[0].upper()
            epsg = int(h.attrs["epsg"]) if "epsg" in h.attrs else 32618
        t_utc = datetime.fromisoformat(t0[:19])
        tr = Transformer.from_crs("EPSG:4326", "EPSG:%d" % epsg, always_xy=True)
        ux, uy = tr.transform(df_pts.lon.to_numpy(), df_pts.lat.to_numpy())
        i = np.clip(np.searchsorted(xc, ux) - 1, 0, len(xc) - 1); j = np.clip(len(yc) - np.searchsorted(yc[::-1], uy) - 1, 0, len(yc) - 1)
        vhh, vhv = hh[j, i], hv[j, i]; val = np.isfinite(vhh)
        for c in mascaras:
            m = (df_pts.clase == c).to_numpy() & val
            filas.append(dict(sensor="NISAR", escena=os.path.basename(r), fecha_utc=t_utc, traza=d0, hora_local=(t_utc - pd.Timedelta(hours=5)).strftime("%H:%M"),
                              p30=p30(t_utc), epoca=epoca(t_utc), clase=c, n=int(m.sum()), CO=float(np.nanmedian(vhh[m])), X=float(np.nanmedian(vhv[m])), COmX=float(np.nanmedian((vhh - vhv)[m]))))
        print("NISAR %s %s | P30 %.0f mm | %s" % (t_utc.strftime("%Y-%m-%d %H:%M"), d0, p30(t_utc), epoca(t_utc)), flush=True)


def muestrear_gee(sensor, col, bandas, a_db, escala, clave_orbita, dir_prop, prefijo):
    meta = col.reduceColumns(ee.Reducer.toList(4), ["system:index", "system:time_start", dir_prop, clave_orbita]).get("list").getInfo()
    meta = sorted(meta, key=lambda x: x[1]); pasadas = []
    for idx, t0, direccion, orb in meta:
        if pasadas and pasadas[-1]["orb"] == orb and abs(t0 - pasadas[-1]["t0"]) < 5 * 60 * 1000:
            pasadas[-1]["ids"].append(idx)
        else:
            pasadas.append(dict(ids=[idx], t0=t0, direccion=str(direccion)[0].upper(), orb=orb))
    print("%s: %d escenas, %d pasadas" % (sensor, len(meta), len(pasadas)), flush=True)
    for ps in pasadas:
        img = ee.ImageCollection([a_db(ee.Image(prefijo + i)) for i in ps["ids"]]).mosaic()
        # cobertura sobre el AOI, no sobre la caja: una pasada que cubre el area de
        # estudio entera no debe descartarse por no cubrir el mar ni los piedemontes
        cob = img.select(bandas[0]).mask().reduceRegion(ee.Reducer.mean(), aoi, 300, maxPixels=1e9).getInfo().get(bandas[0]) or 0
        t_utc = pd.Timestamp(ps["t0"], unit="ms")
        if cob < 0.9:
            print("   %s %s: cobertura %.0f %%, se salta" % (sensor, t_utc.strftime("%Y-%m-%d"), 100 * cob), flush=True); continue
        m = img.reduceRegions(fc, ee.Reducer.first(), escala).getInfo()["features"]
        t = pd.DataFrame([dict(clase=f["properties"]["clase"], co=f["properties"].get(bandas[0]), x=f["properties"].get(bandas[1])) for f in m]).dropna()
        for c, g in t.groupby("clase"):
            filas.append(dict(sensor=sensor, escena=ps["ids"][0], fecha_utc=t_utc, traza="%s%s" % (ps["direccion"], ps["orb"]), hora_local=(t_utc - pd.Timedelta(hours=5)).strftime("%H:%M"),
                              p30=p30(t_utc), epoca=epoca(t_utc), clase=c, n=len(g), CO=g.co.median(), X=g.x.median(), COmX=(g.co - g.x).median()))
        print("   %s %s %s%s | P30 %.0f mm | %s | %d puntos" % (sensor, t_utc.strftime("%Y-%m-%d %H:%M"), ps["direccion"], ps["orb"], p30(t_utc), epoca(t_utc), len(t)), flush=True)


if "s1" in SENSORES:
    col = (ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(aoi).filterDate(T0, T1).filter(ee.Filter.eq("instrumentMode", "IW"))
           .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV")).filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VH")))
    muestrear_gee("S1", col, ["VV", "VH"], lambda im: (im.select(["VV", "VH"]).subtract(im.select("angle").multiply(np.pi / 180).cos().log10().multiply(10)) if GAMMA0 else im.select(["VV", "VH"])), 10, "relativeOrbitNumber_start", "orbitProperties_pass", "COPERNICUS/S1_GRD/")
if "alos2" in SENSORES:
    col = ee.ImageCollection("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR").filterBounds(aoi).filterDate(T0, T1).filter(ee.Filter.listContains("Polarizations", "HV"))
    muestrear_gee("ALOS2", col, ["HH", "HV"], lambda im: im.select(["HH", "HV"]).toFloat().pow(2).log10().multiply(10).add(-83).subtract(im.select("LIN").multiply(0.01 * np.pi / 180).cos().log10().multiply(10) if GAMMA0 else 0).updateMask(im.select("HH").gt(0)), 25,
                  "RSP_Path_Number", "PassDirection", "JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR/")

df = pd.DataFrame(filas)
for s, g in df.groupby("sensor"):
    g.to_csv(os.path.join(AQUI, "cgsm_temporada_%s%s.csv" % (s.lower(), SUF)), index=False)

# ------------------------------------------------------------------ prueba
res = []
for (sensor, traza), g in df.groupby(["sensor", "traza"]):
    g = g[g.p30.notna()]
    if g.escena.nunique() < 6:
        print("%s %s: solo %d pasadas, no se evalua" % (sensor, traza, g.escena.nunique())); continue
    w = g.pivot(index="escena", columns="clase", values=["CO", "X", "COmX"])
    meta = g.drop_duplicates("escena").set_index("escena").reindex(w.index)
    lluvia = meta.p30; humeda = meta.epoca == "humeda"
    for var in ("CO", "X", "COmX"):
        for clase in ("manglar", "bosque", "manglar_menos_bosque"):
            y = (w[(var, "manglar")] - w[(var, "bosque")]) if clase == "manglar_menos_bosque" else w[(var, clase)]
            rho, p = spearmanr(lluvia, y)
            res.append(dict(sensor=sensor, traza=traza, hora_local=meta.hora_local.iloc[0], n=len(y), n_humeda=int(humeda.sum()), variable=var, clase=clase,
                            humeda_menos_seca=(y[humeda].median() - y[~humeda].median()) if humeda.sum() and (~humeda).sum() else np.nan, rho_lluvia=rho, p=p))
res = pd.DataFrame(res)
res.to_csv(os.path.join(AQUI, "cgsm_temporada_resumen%s.csv" % SUF), index=False)
print("\n== CGSM: manglar menos bosque, humeda menos seca (dB) y Spearman con la lluvia de 30 dias ==")
print("(CO = copolar: HH en banda L, VV en banda C; X = cruzada)")
for (sensor, traza), g in res.groupby(["sensor", "traza"]):
    print("\n%s traza %s (%s local), n = %d pasadas, %d en epoca humeda" % (sensor, traza, g.hora_local.iloc[0], g.n.iloc[0], g.n_humeda.iloc[0]))
    print(g.pivot(index="clase", columns="variable", values=["humeda_menos_seca", "rho_lluvia", "p"]).round(2).to_string())

# ------------------------------------------------------------------ figura
grupos = sorted(df.groupby(["sensor", "traza"]).groups.keys())
fig, axes = plt.subplots(len(grupos), 2, figsize=(11, 3.4 * len(grupos)), squeeze=False)
for r_, (sensor, traza) in enumerate(grupos):
    g = df[(df.sensor == sensor) & (df.traza == traza)]
    for c, var in enumerate(("CO", "COmX")):
        ax = axes[r_, c]
        for clase, colr in (("manglar", "#1b7837"), ("bosque", "#4d4d4d")):
            s = g[g.clase == clase]
            ax.scatter(s.p30, s[var], color=colr, s=26, marker="o" if clase == "manglar" else "s", label="Mangrove" if clase == "manglar" else "Forest (control)")
        ax.set_title("%s track %s (%s local), %s" % (sensor, traza, g.hora_local.iloc[0], {"CO": "co-pol (HH or VV)", "COmX": "co-pol − cross-pol"}[var]), fontsize=9)
        ax.set_xlabel("Rainfall in the 30 days before the pass (mm, ERA5-Land)"); ax.set_ylabel("dB"); ax.grid(alpha=0.3)
axes[0, 0].legend(fontsize=8)
fig.suptitle("CGSM: mangrove and forest backscatter against antecedent rainfall, by sensor and track", fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.985])     # deja sitio al título general
fig.savefig(os.path.join(AQUI, "fig_cgsm_temporada%s.png" % SUF), dpi=160)
print("\nfigura: fig_cgsm_temporada.png")
