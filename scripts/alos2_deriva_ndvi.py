# -*- coding: utf-8 -*-
"""Completa la sección 4 de alos2_deriva.py: NDVI de Sentinel-2 por punto de manglar (2016 a 2026, estación seca)
y correlaciones del cambio de HH con el cambio de NDVI, con HH − HV actual y con HH inicial. Reescribe
alos2_deriva_puntos.csv, la sección 4 de alos2_deriva_resumen.md y fig_alos2_deriva.png a partir de los CSV.

USO
    python alos2_deriva_ndvi.py
"""
import os
import re

import ee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, mannwhitneyu

AQUI = os.path.dirname(os.path.abspath(__file__))
f = lambda p: os.path.join(AQUI, p)
ee.Initialize(project="basic-buttress-338101")
AOI = ee.FeatureCollection("projects/basic-buttress-338101/assets/AOI_tesis_CGSM_v1").geometry()

p = pd.read_csv(f("alos2_deriva_puntos.csv")).set_index("id")
fc = ee.FeatureCollection([ee.Feature(ee.Geometry.Point([r.lon, r.lat]), {"id": int(i)}) for i, r in p.iterrows()])
nd = {}
for a in range(2016, 2027):
    s2 = (ee.ImageCollection("COPERNICUS/S2_HARMONIZED").filterBounds(AOI).filterDate("%d-01-01" % a, "%d-05-01" % a)
          .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 60)).map(lambda im: im.updateMask(im.select("QA60").eq(0)).normalizedDifference(["B8", "B4"]).rename("NDVI")))
    n = s2.size().getInfo()
    if n == 0:
        continue
    r = s2.median().reduceRegions(fc, ee.Reducer.first(), 10).getInfo()["features"]
    nd[a] = pd.Series({x["properties"]["id"]: x["properties"].get("first") for x in r}, dtype=float)
    print("NDVI %d: %d imágenes, %d puntos con valor" % (a, n, nd[a].notna().sum()), flush=True)
nd = pd.DataFrame(nd)
p["NDVI_ini"] = nd[[c for c in (2016, 2017) if c in nd]].mean(axis=1); p["NDVI_fin"] = nd[[c for c in (2022, 2023, 2024) if c in nd]].mean(axis=1); p["dNDVI"] = p.NDVI_fin - p.NDVI_ini
for a in nd.columns:
    p["NDVI_%d" % a] = nd[a]
p.to_csv(f("alos2_deriva_puntos.csv"))

q = p.dropna(subset=["dHH", "dNDVI"]); q2 = p.dropna(subset=["dHH"])
r1 = spearmanr(q.dHH, q.dNDVI); r2 = spearmanr(q2.dHH, q2.HHmHV_actual); r3 = spearmanr(q2.dHH, q2.HH_inicial)
rec = p[p.transicion.str.startswith("herbácea inundable → manglar")]; est = p[p.transicion == "manglar → manglar"]
lineas = ["## 4. Puntos de manglar (D139): qué explica la caída de HH", "",
          "- ΔHH frente a ΔNDVI (Sentinel-2 L1C, estación seca): ρ %.2f (p %.3g, n %d). NDVI medio %.3f (2016-17) → %.3f (2022-24)." % (r1[0], r1[1], len(q), q.NDVI_ini.mean(), q.NDVI_fin.mean()),
          "- ΔHH frente a HH − HV actual (apertura del dosel 2022-24): ρ %.2f (p %.3g, n %d)." % (r2[0], r2[1], len(q2)),
          "- ΔHH frente a HH inicial (2015-17): ρ %.2f (p %.3g); los puntos que más brillaban al inicio son los que más caen." % (r3[0], r3[1]), "",
          "ΔHH y ΔNDVI por transición MapBiomas 2017 → 2023 (mediana, n):", ""]
tr = p.groupby("transicion").agg(dHH=("dHH", "median"), dNDVI=("dNDVI", "median"), NDVI_ini=("NDVI_ini", "median"), NDVI_fin=("NDVI_fin", "median"), n=("dHH", "count")).sort_values("n", ascending=False)
for t_, row in tr.iterrows():
    if row["n"] >= 8:
        lineas.append("- %s: ΔHH %+.2f dB, NDVI %.2f → %.2f (ΔNDVI %+.3f), n %d" % (t_, row.dHH, row.NDVI_ini, row.NDVI_fin, row.dNDVI, int(row.n)))
u = mannwhitneyu(rec.dHH.dropna(), est.dHH.dropna()); un = mannwhitneyu(rec.dNDVI.dropna(), est.dNDVI.dropna())
lineas += ["", "Recuperados (herbácea → manglar) frente a estables (manglar → manglar): ΔHH %+.2f frente a %+.2f dB (Mann-Whitney p %.3g); ΔNDVI %+.3f frente a %+.3f (p %.3g)." % (rec.dHH.median(), est.dHH.median(), u.pvalue, rec.dNDVI.median(), est.dNDVI.median(), un.pvalue)]
md = open(f("alos2_deriva_resumen.md"), encoding="utf-8").read()
i = md.index("## 4. Puntos de manglar")
md = md[:i] + "\n".join(lineas) + "\n"
open(f("alos2_deriva_resumen.md"), "w", encoding="utf-8").write(md)
print("\n".join(lineas))

# figura completa desde los CSV
cl = pd.read_csv(f("alos2_deriva_clases.csv"))
fig, axs = plt.subplots(2, 2, figsize=(13, 9.5))
ax = axs[0, 0]
for c, colr, lab in (("manglar", "#1a7f3c", "mangrove"), ("bosque", "#8c6d31", "dry forest (control)"), ("humedal_herbaceo", "#6baed6", "herbaceous wetland"), ("agua", "#08519c", "open water"), ("construido", "#d62728", "built-up (stable target)")):
    g = cl[(cl.traza == "D139") & (cl.clase == c)]; ax.plot(g.anio, g.HH, "o-", color=colr, label=lab)
ax.set_title("Dry-season (Jan–Apr) median HH by class, ALOS-2 D139", fontsize=10); ax.set_ylabel("HH (dB)"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
ax = axs[0, 1]
g = cl[cl.traza == "D139"].pivot(index="anio", columns="clase", values="HH")
ax.plot(g.index, g.manglar - g.bosque, "o-", color="#1a7f3c", label="mangrove − forest"); ax.plot(g.index, g.manglar - g.construido, "s--", color="#d62728", label="mangrove − built-up"); ax.plot(g.index, g.bosque - g.construido, "^:", color="#8c6d31", label="forest − built-up")
ax.set_title("Differences between classes, D139 dry season", fontsize=10); ax.set_ylabel("dB"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
ax = axs[1, 0]
col = np.where(q.transicion.str.startswith("herbácea inundable → manglar"), "#d62728", np.where(q.transicion == "manglar → manglar", "#1a7f3c", "#999999"))
ax.scatter(q.dNDVI, q.dHH, s=14, alpha=0.65, c=col)
ax.set_xlabel("ΔNDVI 2016-17 → 2022-24 (Sentinel-2, dry season)"); ax.set_ylabel("ΔHH 2015-17 → 2022-24 (dB)")
ax.set_title("Mangrove points: ΔHH vs ΔNDVI, ρ %.2f (red: herbaceous→mangrove; green: mangrove→mangrove in MapBiomas)" % r1[0], fontsize=8.5); ax.grid(alpha=0.3); ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5)
ax = axs[1, 1]
sc = ax.scatter(p.lon, p.lat, c=p.dHH, cmap="RdBu_r", vmin=-4, vmax=4, s=14); ax.set_aspect("equal"); ax.set_title("ΔHH 2015-17 → 2022-24 at mangrove points", fontsize=10)
fig.colorbar(sc, ax=ax, shrink=0.8, label="dB"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f("fig_alos2_deriva.png"), dpi=150)
print("figura: fig_alos2_deriva.png")
