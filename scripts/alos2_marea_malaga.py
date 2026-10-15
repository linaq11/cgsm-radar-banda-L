# -*- coding: utf-8 -*-
"""Corroboración independiente de la respuesta a la marea con ALOS-2 PALSAR-2 ScanSAR en banda L
sobre Bahía de Málaga.

PROPÓSITO
Evaluar si la respuesta observada con NISAR se reproduce con otro sensor de banda L. El análisis
usa HH y HV y mantiene separadas las trayectorias para no mezclar geometrías de adquisición.
La comparación con Sentinel-1 evalúa si existe una respuesta equivalente en banda C, aunque no
separa del todo el efecto de la longitud de onda del de la polarización, porque Sentinel-1
observa VV y VH y ALOS-2 HH y HV.

DATOS
ALOS-2 PALSAR-2 ScanSAR Level 2.2 en Google Earth Engine, 25 m, enero de 2025 a septiembre de
2026. Los DN se convierten a sigma cero con sigma0_dB = 10 * log10(DN**2) - 83. Los cuadros de
una misma pasada se mosaican y las observaciones se agrupan por trayectoria. Se usan los mismos
1.600 puntos de referencia y la misma serie de marea del análisis con NISAR.

SALIDAS
- alos2_marea_malaga.csv
- alos2_marea_resumen.csv
- fig_alos2_marea.png

USO
    python alos2_marea_malaga.py
"""
import os
GAMMA0 = os.environ.get("RADAR_MAGNITUD", "sigma0").lower() == "gamma0"   # gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
SUF = "_gamma0" if GAMMA0 else ""

import ee
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
CAJA = [-77.40, 3.80, -77.10, 4.10]
CF = -83.0
ee.Initialize(project="basic-buttress-338101")
caja = ee.Geometry.Rectangle(CAJA)

wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
mascaras = {"manglar": wc.eq(95).And(gmw), "bosque": wc.eq(10), "humedal_herbaceo": wc.eq(90), "agua": wc.eq(80)}
feats = []
for nombre, m in mascaras.items():
    fs = m.rename("m").selfMask().stratifiedSample(numPoints=400, classBand="m", region=caja, scale=10, seed=42, geometries=True, tileScale=4).getInfo()["features"]
    feats += [ee.Feature(ee.Geometry.Point(f["geometry"]["coordinates"]), {"clase": nombre}) for f in fs]
fc = ee.FeatureCollection(feats)
print("puntos:", len(feats), flush=True)

mareas = pd.read_csv(os.path.join(AQUI, "mareas_buenaventura.csv"))
mareas["t"] = pd.to_datetime(mareas["fecha_hora_utc"])
xp = (mareas.t - pd.Timestamp("1970-01-01")).dt.total_seconds().to_numpy()
print("marea de trabajo:", mareas.t.min(), "a", mareas.t.max(), flush=True)


def marea_en(t):
    x = (pd.Timestamp(t) - pd.Timestamp("1970-01-01")).total_seconds()
    return float(np.interp(x, xp, mareas.altura_m.to_numpy())) if xp[0] <= x <= xp[-1] else np.nan


def a_db(img):
    dn = img.select(["HH", "HV"]).toFloat()
    s = dn.pow(2).log10().multiply(10.0).add(CF)
    if GAMMA0:   # gamma cero con el angulo local de incidencia LIN (centesimas de grado)
        s = s.subtract(img.select("LIN").multiply(0.01 * np.pi / 180).cos().log10().multiply(10))
    return s.updateMask(dn.gt(0))


col = ee.ImageCollection("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR").filterBounds(caja).filterDate("2025-01-01", "2026-09-11")
col = col.filter(ee.Filter.listContains("Polarizations", "HV"))   # algunas escenas son solo HH
meta = col.reduceColumns(ee.Reducer.toList(4), ["system:index", "system:time_start", "PassDirection", "RSP_Path_Number"]).get("list").getInfo()
meta = sorted(meta, key=lambda x: x[1])
pasadas = []
for idx, t0, direccion, path in meta:
    if pasadas and pasadas[-1]["path"] == int(path) and abs(t0 - pasadas[-1]["t0"]) < 5 * 60 * 1000:
        pasadas[-1]["ids"].append(idx)
    else:
        pasadas.append(dict(ids=[idx], t0=t0, direccion=direccion, path=int(path)))
print("escenas:", len(meta), "| pasadas:", len(pasadas), flush=True)

filas = []
for ps in pasadas:
    img = ee.ImageCollection([a_db(ee.Image("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR/" + i)) for i in ps["ids"]]).mosaic()
    cob = img.select("HH").mask().reduceRegion(ee.Reducer.mean(), caja, 250, maxPixels=1e9).getInfo().get("HH") or 0
    t_utc = pd.Timestamp(ps["t0"], unit="ms")
    if cob < 0.9:
        print("   %s path %d cobertura %.0f %%: se salta" % (t_utc.strftime("%Y-%m-%d"), ps["path"], 100 * cob), flush=True)
        continue
    m = img.reduceRegions(fc, ee.Reducer.first(), 25).getInfo()["features"]
    t = pd.DataFrame([dict(clase=f["properties"]["clase"], HH=f["properties"].get("HH"), HV=f["properties"].get("HV")) for f in m]).dropna()
    for c, g in t.groupby("clase"):
        filas.append(dict(escena=ps["ids"][0], fecha_utc=t_utc, hora_local=(t_utc - pd.Timedelta(hours=5)).strftime("%H:%M"), direccion=ps["direccion"][0],
                          path=ps["path"], marea_m=marea_en(t_utc), clase=c, n=len(g), HH=g.HH.median(), HV=g.HV.median(), HHmHV=(g.HH - g.HV).median()))
    print("   %s %s path %3d %s local | marea %+.2f m | %d puntos" % (t_utc.strftime("%Y-%m-%d %H:%M"), ps["direccion"][0], ps["path"], (t_utc - pd.Timedelta(hours=5)).strftime("%H:%M"), marea_en(t_utc), len(t)), flush=True)
df = pd.DataFrame(filas)
df.to_csv(os.path.join(AQUI, "alos2_marea_malaga%s.csv" % SUF), index=False)

res = []
for path, g in df.groupby("path"):
    g = g[g.marea_m.notna()]
    if g.escena.nunique() < 8:
        print("path %d: solo %d pasadas con marea, no se evalua" % (path, g.escena.nunique()))
        continue
    w = g.pivot(index="escena", columns="clase", values=["HH", "HV", "HHmHV"])
    marea = g.drop_duplicates("escena").set_index("escena").marea_m.reindex(w.index)
    alta = marea > marea.median()
    for var in ("HH", "HV", "HHmHV"):
        for clase in ("manglar", "bosque"):
            y = w[(var, clase)]; rho, p = spearmanr(marea, y)
            res.append(dict(path=path, direccion=g.direccion.iloc[0], hora_local=g.hora_local.iloc[0], n=len(y), variable=var, clase=clase,
                            dif_alta_menos_baja=y[alta].median() - y[~alta].median(), rho=rho, p=p))
        y = w[(var, "manglar")] - w[(var, "bosque")]; rho, p = spearmanr(marea, y)
        res.append(dict(path=path, direccion=g.direccion.iloc[0], hora_local=g.hora_local.iloc[0], n=len(y), variable=var, clase="manglar_menos_bosque",
                        dif_alta_menos_baja=y[alta].median() - y[~alta].median(), rho=rho, p=p))
res = pd.DataFrame(res)
res.to_csv(os.path.join(AQUI, "alos2_marea_resumen%s.csv" % SUF), index=False)
print("\n== ALOS-2: diferencia marea alta menos baja (dB) y Spearman, por path ==")
for path, g in res.groupby("path"):
    print("\npath %d (%s, %s local), n = %d pasadas | marea %.2f a %.2f m" % (path, g.direccion.iloc[0], g.hora_local.iloc[0], g.n.iloc[0],
          df[df.path == path].marea_m.min(), df[df.path == path].marea_m.max()))
    print(g.pivot(index="clase", columns="variable", values="dif_alta_menos_baja").round(2).to_string())
    print("rho:"); print(g.pivot(index="clase", columns="variable", values="rho").round(2).to_string())
    print("p:"); print(g.pivot(index="clase", columns="variable", values="p").round(3).to_string())

paths = sorted(res.path.unique())
fig, axes = plt.subplots(len(paths), 3, figsize=(14, 3.8 * len(paths)), squeeze=False)
for r_, path in enumerate(paths):
    g = df[df.path == path]
    for c, var in enumerate(("HH", "HV", "HHmHV")):
        ax = axes[r_, c]
        for clase, colr in (("manglar", "#1b7837"), ("bosque", "#4d4d4d")):
            s = g[g.clase == clase]
            ax.scatter(s.marea_m, s[var], color=colr, s=26, label="Mangrove" if clase == "manglar" else "Forest (control)")
        ax.set_title("ALOS-2 path %d (%s, %s local), %s" % (path, "ascending" if g.direccion.iloc[0] == "A" else "descending", g.hora_local.iloc[0], var.replace("HHmHV", "HH − HV")), fontsize=9)
        ax.set_xlabel("Tide height at pass (m above mean level)"); ax.set_ylabel("dB"); ax.grid(alpha=0.3)
axes[0, 0].legend(fontsize=8)
fig.suptitle("ALOS-2 PALSAR-2 ScanSAR L-band backscatter of Bahía de Málaga mangrove vs tide height at pass, by path (Jan 2025 – Sep 2026)", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_alos2_marea%s.png" % SUF), dpi=160)
print("\nfigura: fig_alos2_marea.png")
