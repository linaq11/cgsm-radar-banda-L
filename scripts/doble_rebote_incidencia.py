# -*- coding: utf-8 -*-
"""Análisis de robustez de la respuesta hidrológica de NISAR frente al ángulo de incidencia en
Bahía de Málaga.

PROPÓSITO
Comprobar si la respuesta del manglar relativa al bosque se mantiene al estratificar las
observaciones por ángulo de incidencia.

MÉTODO
Dentro de cada trayectoria, los puntos de manglar se dividen en tres terciles de incidencia y los
mismos límites angulares se aplican al bosque de referencia. Para cada tercil se calcula la
correlación de Spearman entre la altura de marea y la mediana de HH, HV y HH-HV, y además la
diferencia manglar - bosque de cada fecha. El análisis evalúa la estabilidad de la respuesta
frente a la geometría local. Por el rango angular reducido dentro de cada trayectoria, no se usa
para establecer una relación general entre la magnitud del efecto y el ángulo de incidencia.

ENTRADAS
- 24 recortes NISAR de Bahía de Málaga
- mareas_buenaventura.csv

SALIDAS
- doble_rebote_incidencia.csv
- fig_doble_rebote_incidencia.png

USO
    python doble_rebote_incidencia.py
"""
import glob
import os
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
DIR = r"D:\TESIS_DATACUBE\NISAR_PACIFICO"
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
CAJA = [-77.40, 3.80, -77.10, 4.10]
rutas = sorted(glob.glob(os.path.join(DIR, "NISAR_MALAGA_*.h5")))

ee.Initialize(project="basic-buttress-338101")
caja = ee.Geometry.Rectangle(CAJA)
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
pts = []
for nombre, m, n in (("manglar", wc.eq(95).And(gmw), 1200), ("bosque", wc.eq(10), 1200)):
    fs = m.rename("m").selfMask().stratifiedSample(numPoints=n, classBand="m", region=caja, scale=10, seed=7, geometries=True, tileScale=4).getInfo()["features"]
    pts += [dict(lon=f["geometry"]["coordinates"][0], lat=f["geometry"]["coordinates"][1], clase=nombre) for f in fs]
df = pd.DataFrame(pts)
print("puntos:", df.clase.value_counts().to_dict(), flush=True)

mareas = pd.read_csv(os.path.join(AQUI, "mareas_buenaventura.csv"))
mareas["t"] = pd.to_datetime(mareas["fecha_hora_utc"])
xp = (mareas.t - pd.Timestamp("1970-01-01")).dt.total_seconds().to_numpy()


def db(a):
    out = np.full(a.shape, np.nan, dtype="float32")
    ok = np.isfinite(a) & (a > 0)
    out[ok] = 10.0 * np.log10(a[ok])
    return out


# valores por punto y escena
reg = []
for r in rutas:
    nombre = os.path.basename(r)
    with h5py.File(r, "r") as h:
        epsg = int(h.attrs["epsg"]); gr = h[GRUPO]
        xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
        fac = gr["rtcGammaToSigmaFactor"][:]
        hh, hv = db(gr["HHHH"][:] * fac), db(gr["HVHV"][:] * fac)
        t0 = h["science/LSAR/identification/zeroDopplerStartTime"][()]
        t0 = t0.decode() if isinstance(t0, bytes) else str(t0)
        inc = h["science/LSAR/GCOV/metadata/radarGrid/incidenceAngle"][:]
        ix, iy = h["science/LSAR/GCOV/metadata/radarGrid/xCoordinates"][:], h["science/LSAR/GCOV/metadata/radarGrid/yCoordinates"][:]
    t_utc = datetime.fromisoformat(t0[:19])
    marea = float(np.interp((pd.Timestamp(t_utc) - pd.Timestamp("1970-01-01")).total_seconds(), xp, mareas.altura_m.to_numpy()))
    tr = Transformer.from_crs("EPSG:4326", "EPSG:%d" % epsg, always_xy=True)
    ux, uy = tr.transform(df.lon.to_numpy(), df.lat.to_numpy())
    i = np.clip(np.searchsorted(xc, ux) - 1, 0, len(xc) - 1)
    j = np.clip(len(yc) - np.searchsorted(yc[::-1], uy) - 1, 0, len(yc) - 1)
    ang = inc[inc.shape[0] // 2] if inc.ndim == 3 else inc
    ii = np.clip(np.searchsorted(ix, ux) - 1, 0, len(ix) - 1)
    jj = np.clip(len(iy) - np.searchsorted(iy[::-1], uy) - 1, 0, len(iy) - 1)
    reg.append(pd.DataFrame(dict(escena=nombre[13:21], traza=nombre.split("_")[3][:4], marea=marea, clase=df.clase, punto=np.arange(len(df)),
                                 inc=ang[jj, ii], HH=hh[j, i], HV=hv[j, i])))
    print(nombre[13:26], "marea %+.2f" % marea, flush=True)
val = pd.concat(reg, ignore_index=True).dropna()
val["HHmHV"] = val.HH - val.HV

# tercios de incidencia por traza (definidos sobre los puntos de manglar; el bosque usa los mismos cortes)
filas = []
for traza, g in val.groupby("traza"):
    cortes = g[g.clase == "manglar"].groupby("punto").inc.median().quantile([1 / 3, 2 / 3]).to_numpy()
    g = g.copy()
    g["tercio"] = np.digitize(g.inc, cortes)
    for k in range(3):
        sub = g[g.tercio == k]
        med = sub.groupby(["escena", "clase"])[["HH", "HV", "HHmHV"]].median().unstack("clase")
        marea = sub.drop_duplicates("escena").set_index("escena").marea.reindex(med.index)
        rango = "%.0f–%.0f°" % (sub[sub.clase == "manglar"].inc.min(), sub[sub.clase == "manglar"].inc.max())
        n_pts = sub[sub.clase == "manglar"].punto.nunique()
        for var in ("HH", "HV", "HHmHV"):
            y = med[(var, "manglar")] - med[(var, "bosque")]
            alta = marea > marea.median()
            rho, p = spearmanr(marea, y)
            filas.append(dict(traza=traza, tercio=k, incidencia=rango, n_puntos_manglar=n_pts, n_pasadas=len(y), variable=var,
                              dif_alta_menos_baja=y[alta].median() - y[~alta].median(), rho=rho, p=p))
res = pd.DataFrame(filas)
res.to_csv(os.path.join(AQUI, "doble_rebote_incidencia.csv"), index=False)
print("\n== manglar menos bosque contra marea, por traza y tercio de incidencia ==")
print(res.pivot_table(index=["traza", "tercio", "incidencia", "n_puntos_manglar"], columns="variable", values=["dif_alta_menos_baja", "rho", "p"]).round(2).to_string())

fig, axes = plt.subplots(2, 3, figsize=(14, 7.5))
for r_, traza in enumerate(sorted(val.traza.unique())):
    g = res[res.traza == traza]
    for c, var in enumerate(("HH", "HV", "HHmHV")):
        ax = axes[r_, c]
        gg = g[g.variable == var]
        ax.bar(gg.incidencia, gg.dif_alta_menos_baja, color=["#1b7837" if p < 0.05 else "#a6dba0" for p in gg.p])
        for x, (d_, rho, p) in enumerate(zip(gg.dif_alta_menos_baja, gg.rho, gg.p)):
            ax.text(x, d_ + (0.03 if d_ >= 0 else -0.08), "ρ %.2f\np %.2f" % (rho, p), ha="center", fontsize=8)
        ax.axhline(0, color="k", lw=0.8)
        ax.set_title("%s, %s" % ("Ascending 004" if traza.startswith("A") else "Descending 087", var.replace("HHmHV", "HH − HV")), fontsize=9.5)
        ax.set_xlabel("Incidence angle tercile"); ax.set_ylabel("Mangrove − forest, high − low tide (dB)")
fig.suptitle("Double-bounce test by incidence angle: tide response of mangrove relative to forest (dark = p < 0.05)", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_doble_rebote_incidencia.png"), dpi=160)
print("\nfigura: fig_doble_rebote_incidencia.png")
