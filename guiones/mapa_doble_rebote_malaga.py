# -*- coding: utf-8 -*-
"""Cartografía del cambio de retrodispersión entre marea alta y baja en Bahía de Málaga con NISAR.

Para cada trayectoria se seleccionan las seis adquisiciones de mayor marea y las seis de menor
marea, se calculan las medianas de los dos grupos y la diferencia alta - baja para HH, HV y
HH-HV. Las trayectorias A004 y D087 se procesan por separado para no mezclar geometrías de
adquisición. Los resultados se agregan a 50 m y se resumen para manglar, bosque no inundable,
humedal herbáceo y agua.

SALIDAS
- fig_mapa_doble_rebote_malaga.png
- mapa_malaga_<traza>_50m.tif
- mapa_doble_rebote_malaga_resumen.csv

USO
    python mapa_doble_rebote_malaga.py
"""
import glob
import importlib.util
import io
import os
import sys

os.environ["PROJ_DATA"] = os.path.join(importlib.util.find_spec("rasterio").submodule_search_locations[0], "proj_data")
os.environ["PROJ_LIB"] = os.environ["PROJ_DATA"]

import h5py
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
import requests
from rasterio.transform import from_origin

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR = r"D:\TESIS_DATACUBE\NISAR_PACIFICO"
G = "science/LSAR/GCOV/grids/frequencyA"
B = 5
CLASES = {1: "manglar", 2: "bosque", 3: "humedal_herbaceo", 4: "agua"}
if not os.path.isdir(DIR):
    sys.exit("ABORTA: D: desmontado")


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
        epsg = int(h.attrs["epsg"]) if "epsg" in h.attrs else 32618
    return 10 * np.log10(hh), 10 * np.log10(hv), xc, yc, epsg


def mascara_gee(epsg, x0, y0, nx, ny):
    import ee
    ee.Initialize(project="basic-buttress-338101")
    wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
    gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3").filter(
        ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
    cl = ee.Image(0).where(wc.eq(80), 4).where(wc.eq(90), 3).where(wc.eq(10), 2).where(wc.eq(95).And(gmw), 1).toUint8()
    url = cl.getDownloadURL({"crs": "EPSG:%d" % epsg, "crs_transform": [B * 10, 0, x0, 0, -B * 10, y0],
                             "dimensions": [nx, ny], "format": "GEO_TIFF"})
    with rasterio.open(io.BytesIO(requests.get(url, timeout=600).content)) as src:
        return src.read(1)


def main():
    p = pd.read_csv(os.path.join(AQUI, "perfil_pacifico_24.csv")).drop_duplicates("escena")[["escena", "traza", "marea_m"]]
    p["escena"] = p.escena.astype(str)
    rutas = {os.path.basename(r)[13:21]: r for r in glob.glob(os.path.join(DIR, "NISAR_MALAGA_*.h5"))}
    print("recortes en disco:", len(rutas), "| con marea:", p.escena.isin(rutas).sum())
    res, mapas = [], {}
    for traza, s in p.groupby("traza"):
        s = s[s.escena.isin(rutas)].sort_values("marea_m")
        k = len(s) // 2
        baja, alta = s.escena.iloc[:k].tolist(), s.escena.iloc[-k:].tolist()
        print("%s: %d pasadas | alta (%.2f a %.2f m) %s | baja (%.2f a %.2f m) %s" % (
            traza, len(s), s.marea_m.iloc[-k], s.marea_m.iloc[-1], alta, s.marea_m.iloc[0], s.marea_m.iloc[k - 1], baja), flush=True)
        grupos = {"alta": [], "baja": []}
        for esc in alta + baja:
            hh, hv, xc, yc, epsg = leer(rutas[esc])
            grupos["alta" if esc in alta else "baja"].append((hh, hv))
        med = lambda L, i: np.nanmedian(np.stack([t[i] for t in L]), axis=0)
        hh_a, hv_a, hh_b, hv_b = med(grupos["alta"], 0), med(grupos["alta"], 1), med(grupos["baja"], 0), med(grupos["baja"], 1)
        d_hh, d_hv, d_q = hh_a - hh_b, hv_a - hv_b, (hh_a - hv_a) - (hh_b - hv_b)
        ny, nx = d_hh.shape
        x0, y0 = float(xc[0]) - 5, float(yc[0]) + 5
        cl = mascara_gee(epsg, x0, y0, nx, ny)
        with rasterio.open(os.path.join(AQUI, "mapa_malaga_%s_50m.tif" % traza), "w", driver="GTiff", height=ny, width=nx, count=4,
                           dtype="float32", crs="EPSG:%d" % epsg, transform=from_origin(x0, y0, B * 10, B * 10), compress="deflate") as dst:
            for i, a in enumerate([d_hh, d_hv, d_q, cl.astype("float32")], 1):
                dst.write(a.astype("float32"), i)
        for kcl, nombre in CLASES.items():
            m = (cl == kcl) & np.isfinite(d_hh)
            for var, a in (("HH", d_hh), ("HV", d_hv), ("HH-HV", d_q)):
                v = a[m]
                if len(v) == 0:
                    continue
                res.append(dict(traza=traza, clase=nombre, variable=var, n_pix_50m=int(m.sum()), mediana=round(float(np.median(v)), 2),
                                q25=round(float(np.percentile(v, 25)), 2), q75=round(float(np.percentile(v, 75)), 2),
                                frac_positiva=round(float((v > 0).mean()), 3)))
        mapas[traza] = (d_hh, d_hv, cl, [x0 / 1000, (x0 + nx * B * 10) / 1000, (y0 - ny * B * 10) / 1000, y0 / 1000], epsg)
    r = pd.DataFrame(res)
    r.to_csv(os.path.join(AQUI, "mapa_doble_rebote_malaga_resumen.csv"), index=False)
    print(r.to_string(index=False))

    fig, axs = plt.subplots(2, 2, figsize=(12, 10.5), constrained_layout=True)
    for row, (traza, (d_hh, d_hv, cl, ext, epsg)) in enumerate(sorted(mapas.items())):
        for col, (tit, a) in enumerate((("ΔHH, high − low tide (dB)", d_hh), ("ΔHV (dB)", d_hv))):
            ax = axs[row, col]
            ax.imshow(np.where(np.isin(cl, [1, 2]), np.nan, 0.0), extent=ext, cmap="Greys", vmin=-1, vmax=1, alpha=0.22, interpolation="nearest")
            ax.imshow(np.where(cl == 2, a, np.nan), extent=ext, cmap="RdBu_r", vmin=-2, vmax=2, alpha=0.35, interpolation="nearest")
            im = ax.imshow(np.where(cl == 1, a, np.nan), extent=ext, cmap="RdBu_r", vmin=-2, vmax=2, interpolation="nearest")
            ax.set_title("NISAR %s: %s" % (traza, tit), fontsize=10.5)
            ax.set_xlabel("UTM easting (km)"); ax.set_ylabel("northing (km)"); ax.tick_params(labelsize=8)
    cb = fig.colorbar(im, ax=axs, shrink=0.7, pad=0.01); cb.set_label("dB, median of the 6 highest-tide minus median of the 6 lowest-tide passes")
    fig.suptitle("Bahía de Málaga, 50 m: backscatter change between high and low tide at pass time, per track; mangrove in full colour, forest control faded", fontsize=10.5)
    fig.savefig(os.path.join(AQUI, "fig_mapa_doble_rebote_malaga.png"), dpi=160)
    print("figura: fig_mapa_doble_rebote_malaga.png")


if __name__ == "__main__":
    main()
