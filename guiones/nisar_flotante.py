# -*- coding: utf-8 -*-
r"""Banda L frente a banda C sobre la vegetacion flotante de 2025 (evento de Hydrilla).

PARA QUE. En la ventana del informe (oct-2025 a sep-2026) el 14 % de los puntos de agua
de WorldCover 2021 dentro del AOI se cubrio de vegetacion flotante. En Sentinel-1 esos
puntos estan 7,4 dB por encima del agua abierta (−13,3 frente a −20,6 dB en VV,
diciembre de 2025). La pregunta es si la banda L los separa igual, mejor o peor, que es
un aporte propio para la clave de interpretacion (objetivo especifico 4).

COMO. Los mismos 400 puntos de agua (WorldCover 80, AOI, semilla 42) se parten en dos
grupos con la firma optica de diciembre de 2025 (NDVI > 0,25 y NDWI < 0, la regla del
evento). Se leen los recortes GCOV de NISAR en D: y se reporta, por escena, la mediana
de HH, HV y HH−HV en cada grupo. Como referencia se incluye el manglar, que es volumen,
y el humedal herbaceo, que es la clase con la que la flotante se puede confundir.

Salida: nisar_flotante.csv y fig_nisar_flotante.png
"""
import glob
import os
from datetime import datetime

import ee
import geopandas as gpd
import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pyproj import Transformer

AQUI = os.path.dirname(os.path.abspath(__file__))
NISAR_DIR = r"D:\TESIS_DATACUBE\NISAR"
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
RAIZ = "projects/basic-buttress-338101/assets/cgsm_datacube_v1"

ee.Initialize(project="basic-buttress-338101")
aoi = ee.FeatureCollection("projects/basic-buttress-338101/assets/AOI_tesis_CGSM_v1").geometry()
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = (ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3")
       .filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0))
s2 = ee.Image(RAIZ + "/s2/202512")
s1 = ee.Image(RAIZ + "/s1/202512").select(["VV", "VH"])
veg = s2.normalizedDifference(["B8", "B4"]).gt(0.25).And(
      s2.normalizedDifference(["B3", "B8"]).lt(0)).rename("veg")

MASC = {"agua": wc.eq(80), "humedal_herbaceo": wc.eq(90), "manglar": wc.eq(95).And(gmw)}
filas = []
for nombre, m in MASC.items():
    fs = (m.rename("m").selfMask()
          .stratifiedSample(numPoints=400, classBand="m", region=aoi, scale=10, seed=42,
                            geometries=True, tileScale=4))
    got = veg.addBands(s1).reduceRegions(fs, ee.Reducer.first(), 10).getInfo()["features"]
    for f in got:
        p = f["properties"]
        filas.append(dict(clase=nombre, lon=f["geometry"]["coordinates"][0],
                          lat=f["geometry"]["coordinates"][1], veg=p.get("veg"),
                          VV=p.get("VV"), VH=p.get("VH")))
pts = pd.DataFrame(filas)
pts["grupo"] = np.where((pts.clase == "agua") & (pts.veg == 1), "flotante",
                        np.where(pts.clase == "agua", "agua_abierta", pts.clase))
print(pts.grupo.value_counts().to_dict(), flush=True)


def db(a):
    out = np.full(a.shape, np.nan, dtype="float32")
    ok = np.isfinite(a) & (a > 0)
    out[ok] = 10.0 * np.log10(a[ok])
    return out


res = []
for r in sorted(glob.glob(os.path.join(NISAR_DIR, "NISAR_AOI_*.h5"))):
    with h5py.File(r, "r") as h:
        gr = h[GRUPO]
        xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
        fac = gr["rtcGammaToSigmaFactor"][:]
        hh, hv = db(gr["HHHH"][:] * fac), db(gr["HVHV"][:] * fac)
        t0 = h["science/LSAR/identification/zeroDopplerStartTime"][()]
        t0 = t0.decode() if isinstance(t0, bytes) else str(t0)
        d0 = h["science/LSAR/identification/orbitPassDirection"][()]
        d0 = (d0.decode() if isinstance(d0, bytes) else str(d0))[0].upper()
        epsg = int(h.attrs["epsg"]) if "epsg" in h.attrs else 32618
    t = datetime.fromisoformat(t0[:19])
    tr = Transformer.from_crs("EPSG:4326", "EPSG:%d" % epsg, always_xy=True)
    ux, uy = tr.transform(pts.lon.to_numpy(), pts.lat.to_numpy())
    i = np.clip(np.searchsorted(xc, ux) - 1, 0, len(xc) - 1)
    j = np.clip(len(yc) - np.searchsorted(yc[::-1], uy) - 1, 0, len(yc) - 1)
    vhh, vhv = hh[j, i], hv[j, i]
    for g, idx in pts.groupby("grupo").groups.items():
        k = np.array(sorted(idx)); ok = np.isfinite(vhh[k])
        if ok.sum() < 10:
            continue
        res.append(dict(escena=os.path.basename(r), fecha=t.date(), traza=d0, grupo=g,
                        n=int(ok.sum()), HH=float(np.nanmedian(vhh[k][ok])),
                        HV=float(np.nanmedian(vhv[k][ok])),
                        HHmHV=float(np.nanmedian((vhh[k] - vhv[k])[ok]))))
    print("  leida", os.path.basename(r), t.date(), d0, flush=True)

d = pd.DataFrame(res)
d.to_csv(os.path.join(AQUI, "nisar_flotante.csv"), index=False)

# ------------------------------------------------------------------ resumen
print("\n== Sentinel-1, diciembre de 2025 (mediana, dB) ==")
print(pts.groupby("grupo")[["VV", "VH"]].median().round(2).to_string())
print("\n== NISAR, mediana entre escenas por grupo (dB) ==")
tab = d.groupby("grupo")[["HH", "HV", "HHmHV"]].median().round(2)
print(tab.to_string())
sep = lambda t, c: round(float(t.loc["flotante", c] - t.loc["agua_abierta", c]), 2)
s1sep = pts.groupby("grupo")[["VV", "VH"]].median()
print("\nSeparacion flotante menos agua abierta:")
print("  banda C: VV %+.2f dB | VH %+.2f dB" % (s1sep.loc["flotante", "VV"] - s1sep.loc["agua_abierta", "VV"],
                                                s1sep.loc["flotante", "VH"] - s1sep.loc["agua_abierta", "VH"]))
print("  banda L: HH %+.2f dB | HV %+.2f dB | HH-HV %+.2f dB" % (sep(tab, "HH"), sep(tab, "HV"), sep(tab, "HHmHV")))
print("\npor escena (flotante menos agua abierta, HH):")
w = d.pivot(index=["escena", "fecha"], columns="grupo", values="HH")
if {"flotante", "agua_abierta"} <= set(w.columns):
    print((w["flotante"] - w["agua_abierta"]).round(2).to_string())

# ------------------------------------------------------------------ figura
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
orden = ["agua_abierta", "flotante", "humedal_herbaceo", "manglar"]
etq = {"agua_abierta": "Open water", "flotante": "Floating vegetation\n(2025 event)",
       "humedal_herbaceo": "Herbaceous\nwetland", "manglar": "Mangrove"}
col = {"agua_abierta": "#1f6f78", "flotante": "#d9571e", "humedal_herbaceo": "#c9b458", "manglar": "#1b7a3e"}
for ax, (fuente, cols, tit) in zip(axes, [
        ("C-band (Sentinel-1, Dec 2025)", ("VV", "VH"), "Sentinel-1"),
        ("L-band (NISAR, median of scenes)", ("HH", "HV"), "NISAR")]):
    for k, g in enumerate(orden):
        if tit == "Sentinel-1":
            v = [pts[pts.grupo == g][c].median() for c in cols]
        else:
            if g not in set(d.grupo):
                continue
            v = [d[d.grupo == g][c].median() for c in cols]
        ax.bar([k - 0.2, k + 0.2], v, 0.38, color=[col[g], col[g]], alpha=1.0 if True else 0.6,
               edgecolor="#14212a", linewidth=[0, 1.2])
        for x, y in zip([k - 0.2, k + 0.2], v):
            ax.annotate("%.1f" % y, (x, y), ha="center", va="top" if y < 0 else "bottom",
                        xytext=(0, -12 if y < 0 else 4), textcoords="offset points", fontsize=7.5)
    ax.set_xticks(range(len(orden))); ax.set_xticklabels([etq[g] for g in orden], fontsize=8)
    ax.set_ylabel("dB"); ax.set_title(fuente + "\nleft bar: co-pol · right bar: cross-pol", fontsize=9)
    ax.grid(axis="y", alpha=0.3)
fig.suptitle("Floating vegetation of the 2025 event against open water, mangrove and herbaceous wetland", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_nisar_flotante.png"))
print("\nfigura: fig_nisar_flotante.png")
