# -*- coding: utf-8 -*-
"""La misma prueba de marea con Sentinel-1 (banda C) sobre Bahía de Málaga.

Toma todas las escenas Sentinel-1 GRD IW (VV, VH, sigma cero en dB, corregidas por
terreno en Earth Engine) que cubren la caja entre oct-2025 y sep-2026, las agrupa por
órbita relativa (cada órbita tiene su hora y su geometria, como las trazas de NISAR),
muestrea los mismos 1.600 puntos (manglar de consenso, bosque, humedal, agua; semilla
42) y asigna a cada escena la marea predicha a SU hora de adquisicion. Luego aplica
la misma regla que marea_vs_radar.py: manglar menos bosque contra marea, diferencia
alta-baja y Spearman, por órbita.

Ademas restringe a las escenas a +-3 dias de una pasada NISAR para la comparacion
directa "mismas fechas".

Salidas: s1_marea_malaga.csv (por escena y clase), s1_marea_resumen.csv, fig_s1_marea.png
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
ee.Initialize(project="basic-buttress-338101")
caja = ee.Geometry.Rectangle(CAJA)


def s1_db(im):
    """Sentinel-1 en dB; con GAMMA0, gamma cero elipsoidal: sigma0 - 10 log10(cos(angulo))."""
    v = im.select(["VV", "VH"])
    return v.subtract(im.select("angle").multiply(np.pi / 180).cos().log10().multiply(10)) if GAMMA0 else v

# --- puntos, identicos a perfil_pacifico_24.py
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
mascaras = {"manglar": wc.eq(95).And(gmw), "bosque": wc.eq(10), "humedal_herbaceo": wc.eq(90), "agua": wc.eq(80)}
feats = []
for nombre, m in mascaras.items():
    fs = m.rename("m").selfMask().stratifiedSample(numPoints=400, classBand="m", region=caja, scale=10, seed=42, geometries=True, tileScale=4).getInfo()["features"]
    feats += [ee.Feature(ee.Geometry.Point(f["geometry"]["coordinates"]), {"clase": nombre}) for f in fs]
fc = ee.FeatureCollection(feats)
print("puntos:", len(feats), flush=True)

# --- marea
mareas = pd.read_csv(os.path.join(AQUI, "mareas_buenaventura.csv"))
mareas["t"] = pd.to_datetime(mareas["fecha_hora_utc"])
xp = (mareas.t - pd.Timestamp("1970-01-01")).dt.total_seconds().to_numpy()


def marea_en(t):
    x = (pd.Timestamp(t) - pd.Timestamp("1970-01-01")).total_seconds()
    return float(np.interp(x, xp, mareas.altura_m.to_numpy())) if xp[0] <= x <= xp[-1] else np.nan


# --- escenas S1
col = (ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(caja).filterDate("2025-10-01", "2026-09-11")
       .filter(ee.Filter.eq("instrumentMode", "IW")).filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
       .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VH")))
meta = col.reduceColumns(ee.Reducer.toList(4), ["system:index", "system:time_start", "orbitProperties_pass", "relativeOrbitNumber_start"]).get("list").getInfo()
print("escenas S1 IW VV+VH sobre la caja:", len(meta), flush=True)
# una pasada = todos los cuadros de la misma órbita con menos de 5 minutos entre si;
# se mosaican, porque los cuadros parten la caja (80 % + 20 %)
meta = sorted(meta, key=lambda x: x[1])
pasadas = []
for idx, t0, direccion, orb in meta:
    if pasadas and pasadas[-1]["orb"] == int(orb) and abs(t0 - pasadas[-1]["t0"]) < 5 * 60 * 1000:
        pasadas[-1]["ids"].append(idx)
    else:
        pasadas.append(dict(ids=[idx], t0=t0, direccion=direccion, orb=int(orb)))
print("pasadas (cuadros mosaicados):", len(pasadas), flush=True)
filas = []
for ps in pasadas:
    idx, t0, direccion, orb = ps["ids"][0], ps["t0"], ps["direccion"], ps["orb"]
    img = ee.ImageCollection([s1_db(ee.Image("COPERNICUS/S1_GRD/" + i)) for i in ps["ids"]]).mosaic()
    cob = img.select("VV").mask().reduceRegion(ee.Reducer.mean(), caja, 200, maxPixels=1e9).getInfo().get("VV") or 0
    if cob < 0.9:
        print("   %s cobertura %.0f %%: se salta" % (idx[17:32], 100 * cob), flush=True)
        continue
    m = img.reduceRegions(fc, ee.Reducer.first(), 10).getInfo()["features"]
    t = pd.DataFrame([dict(clase=f["properties"]["clase"], VV=f["properties"].get("VV"), VH=f["properties"].get("VH")) for f in m]).dropna()
    t_utc = pd.Timestamp(t0, unit="ms")
    for c, g in t.groupby("clase"):
        filas.append(dict(escena=idx, fecha_utc=t_utc, hora_local=(t_utc - pd.Timedelta(hours=5)).strftime("%H:%M"), direccion=direccion[0],
                          orbita=int(orb), marea_m=marea_en(t_utc), clase=c, n=len(g), VV=g.VV.median(), VH=g.VH.median(), VVmVH=(g.VV - g.VH).median()))
    print("   %s %s orb %3d %s local | marea %+.2f m | %d puntos" % (t_utc.strftime("%Y-%m-%d %H:%M"), direccion[0], int(orb), (t_utc - pd.Timedelta(hours=5)).strftime("%H:%M"), marea_en(t_utc), len(t)), flush=True)
df = pd.DataFrame(filas)
df.to_csv(os.path.join(AQUI, "s1_marea_malaga%s.csv" % SUF), index=False)

# --- mismas fechas que NISAR (+-3 dias)
nisar = pd.read_csv(os.path.join(AQUI, "perfil_pacifico_24%s.csv" % SUF), parse_dates=["fecha_utc"]).drop_duplicates("escena")
cerca = df.drop_duplicates("escena").copy()
cerca["dias_a_nisar"] = cerca.fecha_utc.apply(lambda t: (nisar.fecha_utc - t).abs().min().total_seconds() / 86400)
print("\nescenas S1 usadas: %d | a menos de 3 dias de una pasada NISAR: %d" % (len(cerca), (cerca.dias_a_nisar <= 3).sum()), flush=True)

# --- prueba por órbita
res = []
for orb, g in df.groupby("orbita"):
    if g.escena.nunique() < 8:
        continue
    w = g.pivot(index="escena", columns="clase", values=["VV", "VH", "VVmVH"])
    marea = g.drop_duplicates("escena").set_index("escena").marea_m.reindex(w.index)
    alta = marea > marea.median()
    for var in ("VV", "VH", "VVmVH"):
        for clase in ("manglar", "bosque"):
            y = w[(var, clase)]
            rho, p = spearmanr(marea, y)
            res.append(dict(orbita=orb, direccion=g.direccion.iloc[0], hora_local=g.hora_local.iloc[0], n=len(y), variable=var, clase=clase,
                            dif_alta_menos_baja=y[alta].median() - y[~alta].median(), rho=rho, p=p))
        y = w[(var, "manglar")] - w[(var, "bosque")]
        rho, p = spearmanr(marea, y)
        res.append(dict(orbita=orb, direccion=g.direccion.iloc[0], hora_local=g.hora_local.iloc[0], n=len(y), variable=var, clase="manglar_menos_bosque",
                        dif_alta_menos_baja=y[alta].median() - y[~alta].median(), rho=rho, p=p))
res = pd.DataFrame(res)
res.to_csv(os.path.join(AQUI, "s1_marea_resumen%s.csv" % SUF), index=False)
print("\n== Sentinel-1: diferencia marea alta menos baja (dB) y Spearman, por orbita ==")
for orb, g in res.groupby("orbita"):
    print("\norbita %d (%s, %s local), n = %d escenas" % (orb, g.direccion.iloc[0], g.hora_local.iloc[0], g.n.iloc[0]))
    print(g.pivot(index="clase", columns="variable", values="dif_alta_menos_baja").round(2).to_string())
    print("rho:"); print(g.pivot(index="clase", columns="variable", values="rho").round(2).to_string())
    print("p:"); print(g.pivot(index="clase", columns="variable", values="p").round(3).to_string())

# --- figura
orbs = sorted(res.orbita.unique())
fig, axes = plt.subplots(len(orbs), 3, figsize=(14, 3.8 * len(orbs)), squeeze=False)
for r, orb in enumerate(orbs):
    g = df[df.orbita == orb]
    for c, var in enumerate(("VV", "VH", "VVmVH")):
        ax = axes[r, c]
        for clase, colr in (("manglar", "#1b7837"), ("bosque", "#4d4d4d")):
            s = g[g.clase == clase]
            ax.scatter(s.marea_m, s[var], color=colr, s=26, label="Mangrove" if clase == "manglar" else "Forest (control)")
        ax.set_title("Sentinel-1 orbit %d (%s, %s local), %s" % (orb, "ascending" if g.direccion.iloc[0] == "A" else "descending", g.hora_local.iloc[0], var.replace("VVmVH", "VV − VH")), fontsize=9)
        ax.set_xlabel("Tide height at pass (m above mean level)"); ax.set_ylabel("dB"); ax.grid(alpha=0.3)
axes[0, 0].legend(fontsize=8)
fig.suptitle("Sentinel-1 C-band backscatter of Bahía de Málaga mangrove vs predicted tide height, by relative orbit (Oct 2025 – Sep 2026)", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_s1_marea%s.png" % SUF), dpi=160)
print("\nfigura: fig_s1_marea.png")
