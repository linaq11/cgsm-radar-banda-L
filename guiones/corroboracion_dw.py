# -*- coding: utf-8 -*-
"""Contraste óptico de la respuesta hidrológica con Dynamic World (Brown et al., 2022).

PROPÓSITO
Comparar la señal SAR con la probabilidad de flooded_vegetation de Dynamic World en las zonas
donde la inundación puede manifestarse desde el óptico.

ANÁLISIS
1. Temporal: para cada fecha válida se calcula la probabilidad media de flooded_vegetation sobre
   manglar, humedal herbáceo y bosque no inundable, y se compara con Spearman con el nivel del
   río en Remolino.
2. Espacial: se calcula la diferencia entre los periodos de nivel alto y bajo sobre la misma
   malla de 50 m de NISAR y se compara con delta HH sobre el manglar.

LIMITACIÓN
Dynamic World observa la superficie y el dosel desde el óptico. Su clase flooded_vegetation es
sensible sobre todo al agua visible entre vegetación baja o abierta y no es una observación
directa del agua bajo un dosel cerrado. Por ello, el análisis se usa como contraste óptico y no
como validación independiente de la señal de banda L.

SALIDAS
- dw_serie.csv
- dw_resumen.txt
- fig_corroboracion_dw.png
- dw_alto_bajo_50m.tif

USO
    python corroboracion_dw.py [--solo-figura]
"""
import io
import os

import importlib.util
# PostGIS deja un proj.db viejo en PROJ_DATA; rasterio necesita el suyo, y hay que fijarlo antes de importarlo
os.environ["PROJ_DATA"] = os.path.join(importlib.util.find_spec("rasterio").submodule_search_locations[0], "proj_data")
os.environ["PROJ_LIB"] = os.environ["PROJ_DATA"]

import ee
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import requests
from scipy.stats import spearmanr

AQUI = os.path.dirname(os.path.abspath(__file__))
COB_MIN = 0.5
INICIO, FIN = "2025-10-01", "2026-10-01"
ALTO = ("2025-10-20", "2026-01-16")
BAJO = ("2026-06-20", "2026-10-01")

ee.Initialize(project="basic-buttress-338101")
AOI = ee.FeatureCollection("projects/basic-buttress-338101/assets/AOI_tesis_CGSM_v1").geometry()
CAJA = ee.Image("projects/basic-buttress-338101/assets/cgsm_datacube_v1/s2/202512").geometry()
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(
    ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
MASC = {"manglar": wc.eq(95).And(gmw).clip(AOI), "humedal_herbaceo": wc.eq(90).clip(AOI), "bosque": wc.eq(10).clip(CAJA)}
DW = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filterBounds(AOI).filterDate(INICIO, FIN).select("flooded_vegetation")


def serie_temporal():
    """Una reduccion agrupada por clase por imagen (media y conteo de pixeles validos), en tandas."""
    cl = ee.Image(0).where(MASC["bosque"], 2).where(MASC["humedal_herbaceo"], 3).where(MASC["manglar"], 1).rename("clase")
    tot = cl.reduceRegion(ee.Reducer.frequencyHistogram(), CAJA, 50, bestEffort=True, maxPixels=1e9).get("clase").getInfo()
    tot = {int(float(k)): v for k, v in tot.items()}
    red = ee.Reducer.mean().combine(ee.Reducer.count(), sharedInputs=True).group(groupField=1, groupName="clase")

    def por_imagen(img):
        g = img.addBands(cl).reduceRegion(red, CAJA, 50, bestEffort=True, maxPixels=1e9).get("groups")
        return ee.Feature(None, {"fecha": img.date().format("YYYY-MM-dd"), "grupos": g})
    ids = DW.aggregate_array("system:index").getInfo()
    filas = []
    for k in range(0, len(ids), 30):
        fc = ee.ImageCollection([DW.filter(ee.Filter.eq("system:index", i)).first() for i in ids[k:k + 30]]).map(por_imagen)
        for x in fc.getInfo()["features"]:
            p = x["properties"]; fila = {"fecha": p["fecha"]}
            for g in p["grupos"] or []:
                nombre = {1: "manglar", 2: "bosque", 3: "humedal_herbaceo"}.get(int(g["clase"]))
                if nombre:
                    fila[nombre + "_prob"] = g.get("mean", np.nan); fila[nombre + "_cob"] = g.get("count", 0) / tot[int(g["clase"])]
            filas.append(fila)
        print("  DW %d / %d" % (min(k + 30, len(ids)), len(ids)), flush=True)
    d = pd.DataFrame(filas)
    for nombre in MASC:
        for suf in ("_prob", "_cob"):
            if nombre + suf not in d:
                d[nombre + suf] = np.nan
    # una fila por fecha (varias teselas S2 el mismo dia): media ponderada por cobertura
    g = d.groupby("fecha")
    out = pd.DataFrame({"fecha": sorted(d.fecha.unique())})
    for nombre in MASC:
        cob = g[nombre + "_cob"].sum().clip(upper=1.0)
        prob = g.apply(lambda s: np.average(s[nombre + "_prob"].fillna(0), weights=s[nombre + "_cob"].fillna(0) + 1e-9))
        out[nombre + "_cob"] = cob.reindex(out.fecha).values
        out[nombre + "_prob"] = prob.reindex(out.fecha).values
    return out


def nivel_rio(fechas):
    n = pd.read_csv(os.path.join(AQUI, "nivel_ideam_instantaneo.csv"), dtype={"codigoestacion": str})
    n = n[n.codigoestacion == "2904700095"].copy()
    n["t"] = pd.to_datetime(n.fechaobservacion); n["nivel"] = pd.to_numeric(n.valorobservado, errors="coerce")
    n = n[(n.nivel > 0)].dropna(subset=["nivel"])
    diario = n.groupby(n.t.dt.date).nivel.mean()
    return [diario.get(pd.Timestamp(f).date(), np.nan) for f in fechas]


def grupo_50m(ini, fin, x0, y0, nx, ny):
    col = DW.filterDate(ini, fin)
    med = col.median().rename("prob")
    n = col.count().rename("n")
    img = ee.Image.cat(med.toFloat(), n.toFloat())
    url = img.getDownloadURL({"crs": "EPSG:32618", "crs_transform": [50, 0, x0, 0, -50, y0],
                              "dimensions": [nx, ny], "format": "GEO_TIFF"})
    with rasterio.open(io.BytesIO(requests.get(url, timeout=900).content)) as src:
        return src.read(1), src.read(2)


def main():
    import sys
    solo_figura = "--solo-figura" in sys.argv          # relee dw_serie.csv y dw_alto_bajo_50m.tif
    # 1. temporal
    if solo_figura:
        s = pd.read_csv(os.path.join(AQUI, "dw_serie.csv"))
    else:
        s = serie_temporal()
        s["nivel"] = nivel_rio(s.fecha)
        s.to_csv(os.path.join(AQUI, "dw_serie.csv"), index=False)
    ok = s[(s.manglar_cob >= COB_MIN) & s.nivel.notna()]
    lineas = ["Dynamic World, vegetacion inundada, AOI CGSM, %s a %s: %d fechas, %d con cobertura >= %.0f %% sobre el manglar y nivel del rio"
              % (INICIO, FIN, len(s), len(ok), 100 * COB_MIN)]
    for nombre in MASC:
        r, p = spearmanr(ok.nivel, ok[nombre + "_prob"])
        lineas.append("  %-17s prob media %.3f (min %.3f, max %.3f) | Spearman con nivel del rio rho %.2f, p %.3f"
                      % (nombre, ok[nombre + "_prob"].mean(), ok[nombre + "_prob"].min(), ok[nombre + "_prob"].max(), r, p))
    alto = ok[(ok.fecha >= ALTO[0]) & (ok.fecha < ALTO[1])]; bajo = ok[(ok.fecha >= BAJO[0]) & (ok.fecha < BAJO[1])]
    lineas.append("  manglar: prob media en fechas de nivel alto %.3f (n %d) frente a nivel bajo %.3f (n %d)"
                  % (alto.manglar_prob.mean(), len(alto), bajo.manglar_prob.mean(), len(bajo)))

    # 2. espacial
    with rasterio.open(os.path.join(AQUI, "mapa_doble_rebote_50m.tif")) as src:
        d_hh, cl = src.read(1), src.read(4)
        x0, y0 = src.transform.c, src.transform.f
        ny, nx = d_hh.shape
    tif = os.path.join(AQUI, "dw_alto_bajo_50m.tif")
    if solo_figura and os.path.exists(tif) and rasterio.open(tif).count == 5:
        with rasterio.open(tif) as src:
            pa, pb, d_dw, na, nb = src.read(1), src.read(2), src.read(3), src.read(4), src.read(5)
    else:
        pa, na = grupo_50m(ALTO[0], ALTO[1], x0, y0, nx, ny)
        pb, nb = grupo_50m(BAJO[0], BAJO[1], x0, y0, nx, ny)
        d_dw = pa - pb
        with rasterio.open(os.path.join(AQUI, "dw_alto_bajo_50m.tif"), "w", driver="GTiff", height=ny, width=nx, count=5,
                           dtype="float32", crs="EPSG:32618", transform=rasterio.transform.from_origin(x0, y0, 50, 50),
                           compress="deflate") as dst:
            for i, a in enumerate([pa, pb, d_dw, na, nb], 1):
                dst.write(a.astype("float32"), i)
    valido = (na >= 2) & (nb >= 2) & np.isfinite(d_hh)
    for k, nombre in ((1, "manglar"), (2, "bosque"), (3, "humedal_herbaceo")):
        m = valido & (cl == k)
        r, p = spearmanr(d_dw[m], d_hh[m])
        lineas.append("  espacial %-17s n pix 50 m %6d | dDW mediana %+.3f | Spearman(dDW, dHH) rho %.2f, p %.3g | dHH mediana donde dDW > 0,1: %+.2f dB, donde dDW < -0,1: %+.2f dB"
                      % (nombre, m.sum(), np.median(d_dw[m]), r, p,
                         np.median(d_hh[m & (d_dw > 0.1)]) if (m & (d_dw > 0.1)).sum() > 20 else np.nan,
                         np.median(d_hh[m & (d_dw < -0.1)]) if (m & (d_dw < -0.1)).sum() > 20 else np.nan))
    txt = "\n".join(lineas)
    open(os.path.join(AQUI, "dw_resumen.txt"), "w", encoding="utf-8").write(txt + "\n")
    print(txt)

    # figura: serie temporal y mapa de dDW sobre manglar + dispersion
    fig, axs = plt.subplots(1, 3, figsize=(15, 4.8), constrained_layout=True)
    ax = axs[0]
    ax.scatter(pd.to_datetime(ok.fecha), ok.manglar_prob, s=18, color="#1b7837", label="Mangrove")
    ax.scatter(pd.to_datetime(ok.fecha), ok.humedal_herbaceo_prob, s=18, color="#c9b458", label="Herbaceous wetland")
    ax.set_ylabel("Dynamic World flooded-vegetation probability"); ax.legend(fontsize=8, loc="upper right")
    ax.tick_params(axis="x", labelsize=7, rotation=45)
    ax2 = ax.twinx(); ax2.plot(pd.to_datetime(ok.fecha), ok.nivel, color="#2F4E86", lw=1); ax2.set_ylabel("River level at Remolino (m)", color="#2F4E86")
    ax.set_title("Cloud-free dates with ≥ %.0f %% mangrove coverage (n = %d)" % (100 * COB_MIN, len(ok)), fontsize=10)
    ax = axs[1]
    ext = [x0 / 1000, (x0 + nx * 50) / 1000, (y0 - ny * 50) / 1000, y0 / 1000]
    im = ax.imshow(np.where(valido & np.isin(cl, [1, 2]), d_dw, np.nan), extent=ext, cmap="BrBG", vmin=-0.3, vmax=0.3, interpolation="nearest")
    ax.set_title("ΔDW flooded vegetation, high − low river level (mangrove and forest)", fontsize=10); ax.tick_params(labelsize=7)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax = axs[2]
    m = valido & (cl == 1)
    hb = ax.hexbin(d_dw[m], d_hh[m], gridsize=40, cmap="Greens", mincnt=1, bins="log", extent=(-0.5, 0.6, -6, 6))
    fig.colorbar(hb, ax=ax, shrink=0.8, label="pixels (log)")
    ax.set_xlabel("ΔDW flooded vegetation (probability)"); ax.set_ylabel("NISAR ΔHH, high − low (dB)")
    r, p = spearmanr(d_dw[m], d_hh[m]); ax.set_title("Mangrove pixels, 50 m: Spearman ρ = %.2f" % r, fontsize=10)
    fig.savefig(os.path.join(AQUI, "fig_corroboracion_dw.png"), dpi=160)
    print("figura: fig_corroboracion_dw.png")


if __name__ == "__main__":
    main()
