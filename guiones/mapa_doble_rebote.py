# -*- coding: utf-8 -*-
r"""Mapa de la senal de inundacion bajo dosel en la CGSM con NISAR (traza D083): diferencia
por pixel entre las pasadas de nivel alto del rio Magdalena y las de nivel bajo.

PARA QUE. La propuesta del curso promete "mapas de retrodispersion"; la prueba del nivel del
rio (cgsm_nivel_rio.py) es un numero por clase. Aqui la misma regla, alto menos bajo, se
aplica pixel a pixel para ver DONDE aparece el doble rebote y donde no.

COMO. Las 14 escenas NISAR_AOI_*D083*.h5 comparten la malla UTM 18N de 10 m (7590 x 6469).
Cada escena: gamma0 RTC -> sigma0 con rtcGammaToSigmaFactor, agregacion a 50 m por media de
bloques 5 x 5 en potencia, dB. Grupos: nivel alto = tercio alto de cgsm_nivel_rio.py (6
pasadas, oct-2025 a ene-2026) y nivel bajo = las 8 de jun a sep 2026; mediana por grupo y
diferencia alto - bajo para HH, HV y HH - HV. La mascara de manglar (WorldCover 95 y GMW
2020), bosque (WorldCover 10), humedal herbaceo (90) y agua (80) se descarga de Earth Engine
sobre la misma malla de 50 m. Se escriben la figura, un GeoTIFF con las tres diferencias y
un resumen por clase (mediana, cuartiles y fraccion de pixeles con diferencia positiva).

LIMITE. Los dos grupos coinciden con el periodo y con la version del producto (Beta frente a
Provisional); el mapa muestra la estructura espacial de la senal, no su causa.

USO: python mapa_doble_rebote.py        Salidas: fig_mapa_doble_rebote.png,
     mapa_doble_rebote_50m.tif, mapa_doble_rebote_resumen.csv
"""
import glob
import os

import importlib.util
# PostGIS deja un proj.db viejo en PROJ_DATA; rasterio necesita el suyo, y hay que fijarlo antes de importarlo
os.environ["PROJ_DATA"] = os.path.join(importlib.util.find_spec("rasterio").submodule_search_locations[0], "proj_data")
os.environ["PROJ_LIB"] = os.environ["PROJ_DATA"]

import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
NISAR = r"D:\TESIS_DATACUBE\NISAR"
G = "science/LSAR/GCOV/grids/frequencyA"
B = 5                                      # 5 x 5 pixeles de 10 m -> 50 m
ALTO = {"20251029", "20251122", "20251204", "20251216", "20251228", "20260109"}
BAJO = {"20260626", "20260708", "20260720", "20260813", "20260825", "20260906", "20260918", "20260930"}
CLASES = {1: "manglar", 2: "bosque", 3: "humedal_herbaceo", 4: "agua"}


def agregar(a):
    ny, nx = (a.shape[0] // B) * B, (a.shape[1] // B) * B
    return np.nanmean(a[:ny, :nx].reshape(ny // B, B, nx // B, B), axis=(1, 3))


def leer(ruta):
    with h5py.File(ruta, "r") as h:
        g = h[G]
        fac = g["rtcGammaToSigmaFactor"][:]
        hh = agregar(np.where(np.isfinite(g["HHHH"][:]), g["HHHH"][:], np.nan) * fac)
        hv = agregar(np.where(np.isfinite(g["HVHV"][:]), g["HVHV"][:], np.nan) * fac)
        xc, yc = g["xCoordinates"][:], g["yCoordinates"][:]
    return 10 * np.log10(hh), 10 * np.log10(hv), xc, yc


def mascara_gee(x0, y0, nx, ny):
    """Clases en la malla de 50 m (UTM 18N): 1 manglar, 2 bosque, 3 humedal, 4 agua, 0 otro."""
    import io
    import ee
    import requests
    import rasterio
    ee.Initialize(project="basic-buttress-338101")
    wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
    gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(
        ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
    cl = ee.Image(0).where(wc.eq(80), 4).where(wc.eq(90), 3).where(wc.eq(10), 2).where(wc.eq(95).And(gmw), 1).toUint8()
    url = cl.getDownloadURL({"crs": "EPSG:32618", "crs_transform": [B * 10, 0, x0, 0, -B * 10, y0],
                             "dimensions": [nx, ny], "format": "GEO_TIFF"})
    with rasterio.open(io.BytesIO(requests.get(url, timeout=600).content)) as src:
        return src.read(1)


SECTORES = [("norte (Salamanca, N > 1205 km)", 1205e3, 1e9), ("centro y occidente (1190 a 1205 km)", 1190e3, 1205e3),
            ("sur (caños del Magdalena, N < 1190 km)", -1e9, 1190e3)]


def calcular():
    rutas = sorted(glob.glob(os.path.join(NISAR, "NISAR_AOI_*083*.h5")))
    alto, bajo = [], []
    for r in rutas:
        fecha = os.path.basename(r)[10:18]
        if fecha not in ALTO | BAJO:
            continue
        hh, hv, xc, yc = leer(r)
        (alto if fecha in ALTO else bajo).append((hh, hv))
        print("  %s %s" % (fecha, "alto" if fecha in ALTO else "bajo"), flush=True)
    print("alto %d, bajo %d" % (len(alto), len(bajo)))
    med = lambda L, i: np.nanmedian(np.stack([t[i] for t in L]), axis=0)
    hh_a, hv_a, hh_b, hv_b = med(alto, 0), med(alto, 1), med(bajo, 0), med(bajo, 1)
    d_hh, d_hv = hh_a - hh_b, hv_a - hv_b
    d_q = (hh_a - hv_a) - (hh_b - hv_b)
    ny, nx = d_hh.shape
    x0, y0 = float(xc[0]) - 5, float(yc[0]) + 5           # esquina exterior del primer pixel de 10 m
    cl = mascara_gee(x0, y0, nx, ny)
    print("mascara:", {CLASES[k]: int((cl == k).sum()) for k in CLASES})
    import rasterio
    from rasterio.transform import from_origin
    with rasterio.open(os.path.join(AQUI, "mapa_doble_rebote_50m.tif"), "w", driver="GTiff", height=ny, width=nx,
                       count=4, dtype="float32", crs="EPSG:32618", transform=from_origin(x0, y0, B * 10, B * 10),
                       compress="deflate") as dst:
        for i, a in enumerate([d_hh, d_hv, d_q, cl.astype("float32")], 1):
            dst.write(a.astype("float32"), i)
        dst.descriptions = ("dHH alto-bajo dB", "dHV alto-bajo dB", "d(HH-HV) alto-bajo dB", "clase 1 manglar 2 bosque 3 humedal 4 agua")


def main():
    import sys
    if "--desde-tif" not in sys.argv:
        calcular()
    import rasterio
    with rasterio.open(os.path.join(AQUI, "mapa_doble_rebote_50m.tif")) as src:
        d_hh, d_hv, d_q, cl = src.read(1), src.read(2), src.read(3), src.read(4).astype(int)
        x0, y0 = src.transform.c, src.transform.f
    ny, nx = d_hh.shape
    norte = y0 - (np.arange(ny) + 0.5) * B * 10
    N = np.repeat(norte[:, None], nx, axis=1)

    # Resumen por clase y, para el manglar, por sector de norte a sur
    filas = []
    grupos = [(nombre, (cl == k)) for k, nombre in CLASES.items()]
    grupos += [("manglar " + s, (cl == 1) & (N >= a) & (N < b)) for s, a, b in SECTORES]
    for nombre, m in grupos:
        m = m & np.isfinite(d_hh)
        for var, a in (("HH", d_hh), ("HV", d_hv), ("HH-HV", d_q)):
            v = a[m]
            filas.append(dict(clase=nombre, variable=var, n_pix_50m=int(m.sum()), mediana=round(float(np.median(v)), 2),
                              q25=round(float(np.percentile(v, 25)), 2), q75=round(float(np.percentile(v, 75)), 2),
                              frac_positiva=round(float((v > 0).mean()), 3), frac_mayor_0_5=round(float((v > 0.5).mean()), 3)))
    res = pd.DataFrame(filas)
    res.to_csv(os.path.join(AQUI, "mapa_doble_rebote_resumen.csv"), index=False)
    print(res.to_string(index=False))

    # Figura: manglar a todo color, bosque de control atenuado, el resto en gris claro; sin contornos
    ext = [x0 / 1000, (x0 + nx * B * 10) / 1000, (y0 - ny * B * 10) / 1000, y0 / 1000]
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.6), constrained_layout=True)
    for ax, (tit, a) in zip(axs, (("ΔHH, high − low river level (dB)", d_hh), ("ΔHV (dB)", d_hv), ("Δ(HH − HV) (dB)", d_q))):
        ax.imshow(np.where(np.isin(cl, [1, 2]), np.nan, 0.0), extent=ext, cmap="Greys", vmin=-1, vmax=1, alpha=0.22, interpolation="nearest")
        ax.imshow(np.where(cl == 2, a, np.nan), extent=ext, cmap="RdBu_r", vmin=-2, vmax=2, alpha=0.35, interpolation="nearest")
        im = ax.imshow(np.where(cl == 1, a, np.nan), extent=ext, cmap="RdBu_r", vmin=-2, vmax=2, interpolation="nearest")
        for _, yy, _ in SECTORES[:2]:
            ax.axhline(yy / 1000, color="#444444", lw=0.6, ls=":")
        ax.set_title(tit, fontsize=11)
        ax.set_xlabel("UTM 18N easting (km)"); ax.set_ylabel("northing (km)")
        ax.tick_params(labelsize=8)
    cb = fig.colorbar(im, ax=axs, shrink=0.8, pad=0.01); cb.set_label("dB, median of 6 high-level minus median of 8 low-level passes")
    fig.suptitle("NISAR D083, CGSM, 50 m: backscatter change between high and low Magdalena River level. Mangrove in full colour, dry forest control faded; dotted lines = sectors of the summary table", fontsize=10.5)
    fig.savefig(os.path.join(AQUI, "fig_mapa_doble_rebote.png"), dpi=160)
    print("figura: fig_mapa_doble_rebote.png")


if __name__ == "__main__":
    main()
