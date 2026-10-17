# -*- coding: utf-8 -*-
"""¿La deriva interanual de la resta HH manglar − bosque en ALOS-2 (2014 a 2026, CGSM) es del producto JAXA o del manglar?

PRUEBAS
    1. Metadatos: versión del producto, instalación, software y fecha de procesamiento por año (si todo se procesó en
       un mismo lote con una misma versión, no hay escalón de producto declarado).
    2. Blancos de referencia: compuestos anuales de estación seca (enero a abril, traza D139 y D138) y mediana anual
       por clase (manglar, bosque seco, humedal, agua) más una clase estable, zonas construidas (WorldCover 50) en la
       caja del cubo. Un cambio de producto mueve todas las clases a la vez; un cambio del manglar solo mueve al manglar.
    3. Por punto: cambio de HH de cada punto de manglar entre 2015-2017 y 2022-2024, contra (a) el cambio de NDVI de
       Sentinel-2 en las mismas fechas (verdor del dosel), (b) la clase MapBiomas del punto en 2017 y 2023 (herbácea
       inundable → manglar = recuperación) y (c) HH − HV actual (apertura del dosel). Si la caída de HH se concentra en
       los puntos que reverdecieron o que pasaron de herbácea a manglar, la deriva es del manglar.
SALIDAS
    alos2_deriva_clases.csv, alos2_deriva_puntos.csv, alos2_deriva_resumen.md, fig_alos2_deriva.png
USO
    python alos2_deriva.py
"""
import os

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
CONTROL = ee.Image("projects/basic-buttress-338101/assets/cgsm_datacube_v1/s2/202512").geometry()
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
mascaras = {"manglar": wc.eq(95).And(gmw), "bosque": wc.eq(10), "humedal_herbaceo": wc.eq(90), "agua": wc.eq(80), "construido": wc.eq(50)}
REGION = {"manglar": AOI, "humedal_herbaceo": AOI, "agua": AOI, "bosque": CONTROL, "construido": CONTROL}
ANIOS = list(range(2015, 2027))

# ---------------------------------------------------------------- 1. metadatos por año
col = ee.ImageCollection("JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR").filterBounds(AOI).filterDate("2014-08-01", "2026-12-31").filter(ee.Filter.listContains("Polarizations", "HV"))
keys = ["system:time_start", "RSP_Path_Number", "Product_Version", "SourceProcParam_ProcessingDate", "SourceProcParam_SoftwareVersion", "DataAccess_ProcessingTime", "IonosphericDelayCorrectionApplied"]
meta = pd.DataFrame(col.reduceColumns(ee.Reducer.toList(len(keys)), keys).get("list").getInfo(), columns=keys)
meta["anio"] = pd.to_datetime(meta["system:time_start"], unit="ms").dt.year
meta["proc"] = meta.SourceProcParam_ProcessingDate.astype(str).str[:4]
resumen = ["## 1. Metadatos del producto por año de adquisición", "", "Año de procesamiento (SourceProcParam_ProcessingDate) por año de adquisición:", "", pd.crosstab(meta.anio, meta.proc).to_string(), "",
           "Versiones: Product_Version %s; software %s; fechas de descarga %s a %s." % (sorted(meta.Product_Version.astype(str).unique()), sorted(meta.SourceProcParam_SoftwareVersion.astype(str).unique()), meta.DataAccess_ProcessingTime.astype(str).min()[:10], meta.DataAccess_ProcessingTime.astype(str).max()[:10]), ""]
print("\n".join(resumen), flush=True)

# ---------------------------------------------------------------- 2. puntos (semilla 42) y compuestos anuales de estación seca
pts = []
for nombre, m in mascaras.items():
    n = 200 if nombre == "construido" else 400
    fs = m.rename("m").selfMask().stratifiedSample(numPoints=n, classBand="m", region=REGION[nombre], scale=10, seed=42, geometries=True, tileScale=4).getInfo()["features"]
    pts += [dict(lon=ft["geometry"]["coordinates"][0], lat=ft["geometry"]["coordinates"][1], clase=nombre) for ft in fs]
df = pd.DataFrame(pts); df["id"] = np.arange(len(df))
fc = ee.FeatureCollection([ee.Feature(ee.Geometry.Point([r.lon, r.lat]), {"id": int(r.id)}) for r in df.itertuples()])
print("puntos:", df.clase.value_counts().to_dict(), flush=True)


def db(im):
    return im.select(["HH", "HV"]).toFloat().pow(2).log10().multiply(10).add(-83).updateMask(im.select("HH").gt(0))


def muestrear(img, bandas, escala):
    r = img.reduceRegions(fc, ee.Reducer.first(), escala).getInfo()["features"]
    # con una sola banda, Reducer.first() llama a la propiedad "first" y no con el nombre de la banda
    return pd.DataFrame([dict(id=x["properties"]["id"], **{b: x["properties"].get(b, x["properties"].get("first")) for b in bandas}) for x in r]).set_index("id")


tablas = []
for traza in (139, 138):
    for a in ANIOS:
        c = col.filter(ee.Filter.eq("RSP_Path_Number", traza)).filter(ee.Filter.eq("PassDirection", "Descending")).filterDate("%d-01-01" % a, "%d-05-01" % a)
        n = c.size().getInfo()
        if n == 0:
            continue
        t = muestrear(c.map(db).median(), ["HH", "HV"], 25); t["traza"] = "D%d" % traza; t["anio"] = a; t["n_pasadas"] = n
        tablas.append(t.reset_index()); print("D%d %d: %d pasadas enero-abril" % (traza, a, n), flush=True)
alos = pd.concat(tablas, ignore_index=True).merge(df, on="id")
alos["HHmHV"] = alos.HH - alos.HV

# NDVI de Sentinel-2 L1C (TOA, consistente 2016-2026), estación seca, mediana con máscara QA60
ndvi_t = []
for a in range(2016, 2027):
    s2 = (ee.ImageCollection("COPERNICUS/S2_HARMONIZED").filterBounds(AOI).filterDate("%d-01-01" % a, "%d-05-01" % a)
          .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 60))
          .map(lambda im: im.updateMask(im.select("QA60").eq(0)).normalizedDifference(["B8", "B4"]).rename("NDVI")))
    if s2.size().getInfo() == 0:
        continue
    t = muestrear(s2.median(), ["NDVI"], 10); t["anio"] = a; ndvi_t.append(t.reset_index())
ndvi = pd.concat(ndvi_t, ignore_index=True)

# MapBiomas Colombia colección 2 (1985-2023, 30 m): clase por punto y año
mb = ee.Image("projects/mapbiomas-public/assets/colombia/collection2/mapbiomas_colombia_collection2_integration_v1")
mbt = muestrear(mb.select(["classification_%d" % a for a in range(2015, 2024)]), ["classification_%d" % a for a in range(2015, 2024)], 30).reset_index()

# ---------------------------------------------------------------- 3. análisis
cl = alos.groupby(["traza", "anio", "clase"]).agg(HH=("HH", "median"), HV=("HV", "median"), HHmHV=("HHmHV", "median"), n=("HH", "count"), n_pasadas=("n_pasadas", "first")).round(2).reset_index()
cl.to_csv(f("alos2_deriva_clases.csv"), index=False)
piv = cl[cl.traza == "D139"].pivot(index="anio", columns="clase", values="HH")
resumen += ["## 2. Mediana anual de HH (dB) por clase, estación seca enero a abril, traza D139", "", piv.round(2).to_string(), ""]
# cambio 2015-2017 → 2022-2024 por clase (D139)
def cambio(g, var="HH"):
    a = g[g.anio.isin([2015, 2016, 2017])].groupby("id")[var].mean(); b = g[g.anio.isin([2022, 2023, 2024])].groupby("id")[var].mean()
    return (b - a).dropna()
lineas = ["## 3. Cambio por punto entre 2015-2017 y 2022-2024, traza D139 (mediana y rango intercuartílico, dB)", ""]
for c in mascaras:
    g = alos[(alos.traza == "D139") & (alos.clase == c)]; d = cambio(g); dhv = cambio(g, "HV")
    lineas.append("- %s: ΔHH %+.2f [%+.2f a %+.2f], ΔHV %+.2f, n %d" % (c, d.median(), d.quantile(.25), d.quantile(.75), dhv.median(), len(d)))
resumen += lineas + [""]

# por punto de manglar: ΔHH, ΔNDVI, transición MapBiomas, HH−HV actual
gm = alos[(alos.traza == "D139") & (alos.clase == "manglar")]
p = pd.DataFrame({"dHH": cambio(gm), "dHV": cambio(gm, "HV")})
p["HHmHV_actual"] = gm[gm.anio.isin([2022, 2023, 2024])].groupby("id").HHmHV.mean()
p["HH_inicial"] = gm[gm.anio.isin([2015, 2016, 2017])].groupby("id").HH.mean()
nd = ndvi.pivot(index="id", columns="anio", values="NDVI")
p["NDVI_ini"] = nd[[c for c in (2016, 2017) if c in nd]].mean(axis=1); p["NDVI_fin"] = nd[[c for c in (2022, 2023, 2024) if c in nd]].mean(axis=1); p["dNDVI"] = p.NDVI_fin - p.NDVI_ini
m = mbt.set_index("id"); p["mb2017"] = m["classification_2017"]; p["mb2023"] = m["classification_2023"]
nombres = {5: "manglar", 6: "bosque inundable", 11: "herbácea inundable", 33: "agua", 3: "bosque", 21: "mosaico agropecuario", 12: "herbácea", 24: "infraestructura", 25: "otra área no vegetada", 31: "acuicultura"}
p["transicion"] = p.mb2017.map(lambda x: nombres.get(int(x), str(x)) if pd.notna(x) else "sin dato") + " → " + p.mb2023.map(lambda x: nombres.get(int(x), str(x)) if pd.notna(x) else "sin dato")
p = p.merge(df[["id", "lon", "lat"]], left_index=True, right_on="id").set_index("id")
p.to_csv(f("alos2_deriva_puntos.csv"))
q = p.dropna(subset=["dHH", "dNDVI"]); q2 = p.dropna(subset=["dHH"])
r1 = spearmanr(q.dHH, q.dNDVI); r2 = spearmanr(q2.dHH, q2.HHmHV_actual); r3 = spearmanr(q2.dHH, q2.HH_inicial)
lineas = ["## 4. Puntos de manglar (D139): qué explica la caída de HH", "",
          "- ΔHH frente a ΔNDVI (Sentinel-2, estación seca): ρ %.2f (p %.3g, n %d). NDVI medio %.3f (2016-17) → %.3f (2022-24)." % (r1[0], r1[1], len(q), q.NDVI_ini.mean(), q.NDVI_fin.mean()),
          "- ΔHH frente a HH − HV actual (apertura del dosel 2022-24): ρ %.2f (p %.3g)." % (r2[0], r2[1]),
          "- ΔHH frente a HH inicial (2015-17): ρ %.2f (p %.3g); los puntos que más brillaban al inicio son los que más caen." % (r3[0], r3[1]), "",
          "ΔHH por transición MapBiomas 2017 → 2023 (mediana, n):", ""]
tr = p.groupby("transicion").dHH.agg(["median", "count"]).sort_values("count", ascending=False)
for t_, row in tr.iterrows():
    if row["count"] >= 8: lineas.append("- %s: %+.2f dB (n %d)" % (t_, row["median"], int(row["count"])))
rec = p[p.transicion.str.startswith("herbácea inundable → manglar")].dHH; est = p[p.transicion == "manglar → manglar"].dHH
if len(rec) >= 8 and len(est) >= 8:
    u = mannwhitneyu(rec, est, alternative="two-sided")
    lineas.append(""); lineas.append("Recuperados (herbácea → manglar) frente a estables (manglar → manglar): %+.2f frente a %+.2f dB, Mann-Whitney p %.3g." % (rec.median(), est.median(), u.pvalue))
resumen += lineas + [""]
open(f("alos2_deriva_resumen.md"), "w", encoding="utf-8").write("# Deriva de ALOS-2 en la CGSM: ¿producto o manglar?\n\n" + "\n".join(resumen))
print("\n".join(lineas), flush=True)

# ---------------------------------------------------------------- figura
fig, axs = plt.subplots(2, 2, figsize=(13, 9.5))
ax = axs[0, 0]
for c, colr in (("manglar", "#1a7f3c"), ("bosque", "#8c6d31"), ("humedal_herbaceo", "#6baed6"), ("agua", "#08519c"), ("construido", "#d62728")):
    g = cl[(cl.traza == "D139") & (cl.clase == c)]; ax.plot(g.anio, g.HH, "o-", color=colr, label=c)
ax.set_title("Dry-season (Jan–Apr) median HH by class, ALOS-2 D139", fontsize=10); ax.set_ylabel("HH (dB)"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
ax = axs[0, 1]
g = cl[cl.traza == "D139"].pivot(index="anio", columns="clase", values="HH"); ax.plot(g.index, g.manglar - g.bosque, "o-", color="#1a7f3c", label="mangrove − forest")
ax.plot(g.index, g.manglar - g.construido, "s--", color="#d62728", label="mangrove − built-up"); ax.plot(g.index, g.bosque - g.construido, "^:", color="#8c6d31", label="forest − built-up")
ax.set_title("Differences between classes, D139 dry season", fontsize=10); ax.set_ylabel("dB"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
ax = axs[1, 0]
ax.scatter(q.dNDVI, q.dHH, s=12, alpha=0.6, c=np.where(q.transicion.str.startswith("herbácea inundable → manglar"), "#d62728", "#1a7f3c"))
ax.set_xlabel("ΔNDVI 2016-17 → 2022-24 (Sentinel-2, dry season)"); ax.set_ylabel("ΔHH 2015-17 → 2022-24 (dB)"); ax.set_title("Mangrove points: ΔHH vs ΔNDVI (red = herbaceous→mangrove in MapBiomas), ρ %.2f" % r1[0], fontsize=9); ax.grid(alpha=0.3); ax.axhline(0, color="k", lw=0.5); ax.axvline(0, color="k", lw=0.5)
ax = axs[1, 1]
sc = ax.scatter(p.lon, p.lat, c=p.dHH, cmap="RdBu_r", vmin=-4, vmax=4, s=14); ax.set_aspect("equal"); ax.set_title("ΔHH 2015-17 → 2022-24 at mangrove points", fontsize=10)
fig.colorbar(sc, ax=ax, shrink=0.8, label="dB"); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(f("fig_alos2_deriva.png"), dpi=150)
print("figura: fig_alos2_deriva.png")
