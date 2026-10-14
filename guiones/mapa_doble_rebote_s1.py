# -*- coding: utf-8 -*-
r"""Mapa comparativo en banda C: el mismo "alto menos bajo" del nivel del rio que
mapa_doble_rebote.py hace con NISAR, ahora con Sentinel-1 GRD (orbita descendente 142) sobre
la misma malla de 50 m, para que la Figura del informe compare las dos bandas pixel a pixel.

COMO. En Earth Engine, pasadas de la orbita 142 en las mismas dos ventanas de fechas que los
grupos de NISAR (nivel alto: 20-oct-2025 a 15-ene-2026; nivel bajo: 20-jun a 30-sep-2026);
mediana de VV y VH (dB, como las sirve Earth Engine) por grupo, diferencia alto menos bajo,
promediada a 50 m (reduceResolution, media) y descargada sobre la malla UTM 18N del GeoTIFF de
NISAR. Resumen por clase y sector con la misma mascara. Figura de dos paneles: dHH de NISAR
y dVV de Sentinel-1 sobre manglar y bosque.

USO: python mapa_doble_rebote_s1.py   (requiere mapa_doble_rebote_50m.tif)
Salidas: mapa_s1_alto_bajo_50m.tif, mapa_doble_rebote_s1_resumen.csv, fig_mapa_c_vs_l.png
"""
import importlib.util
import io
import os

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

AQUI = os.path.dirname(os.path.abspath(__file__))
ALTO = ("2025-10-20", "2026-01-16")
BAJO = ("2026-06-20", "2026-10-01")
ORBITA = 142
SECTORES = [("norte (Salamanca, N > 1205 km)", 1205e3, 1e9), ("centro y occidente (1190 a 1205 km)", 1190e3, 1205e3),
            ("sur (caños del Magdalena, N < 1190 km)", -1e9, 1190e3)]
CLASES = {1: "manglar", 2: "bosque", 3: "humedal_herbaceo", 4: "agua"}

ee.Initialize(project="basic-buttress-338101")
CAJA = ee.Image("projects/basic-buttress-338101/assets/cgsm_datacube_v1/s2/202512").geometry()
S1 = (ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(CAJA)
      .filter(ee.Filter.eq("instrumentMode", "IW")).filter(ee.Filter.eq("orbitProperties_pass", "DESCENDING"))
      .filter(ee.Filter.eq("relativeOrbitNumber_start", ORBITA)).select(["VV", "VH"]))


def grupo(ini, fin, x0, y0, nx, ny):
    col = S1.filterDate(ini, fin)
    n = col.size().getInfo()
    med = col.median()
    # reduceResolution agota la memoria de Earth Engine con la mediana de 13 pasadas a 10 m; se usa
    # una media movil de 5 x 5 pixeles (50 m) en la malla nativa y se muestrea en la malla de 50 m
    img = ee.Image.cat(med.select("VV"), med.select("VH"), col.select("VV").count().rename("n").toFloat())
    img = img.setDefaultProjection("EPSG:32618", [10, 0, x0, 0, -10, y0]).focalMean(2, "square", "pixels")
    sal = []
    for banda in ("VV", "VH", "n"):
        url = img.select(banda).getDownloadURL({"crs": "EPSG:32618", "crs_transform": [50, 0, x0, 0, -50, y0],
                                                "dimensions": [nx, ny], "format": "GEO_TIFF"})
        r = requests.get(url, timeout=900)
        if r.status_code != 200:
            raise RuntimeError(r.content[:300])
        with rasterio.open(io.BytesIO(r.content)) as src:
            sal.append(src.read(1))
    return sal[0], sal[1], sal[2], n


def main():
    with rasterio.open(os.path.join(AQUI, "mapa_doble_rebote_50m.tif")) as src:
        d_hh, cl = src.read(1), src.read(4).astype(int)
        x0, y0 = src.transform.c, src.transform.f
        ny, nx = d_hh.shape
    vv_a, vh_a, n_a, na = grupo(ALTO[0], ALTO[1], x0, y0, nx, ny)
    vv_b, vh_b, n_b, nb = grupo(BAJO[0], BAJO[1], x0, y0, nx, ny)
    print("Sentinel-1 orbita %d: %d pasadas de nivel alto, %d de nivel bajo" % (ORBITA, na, nb))
    d_vv, d_vh = vv_a - vv_b, vh_a - vh_b
    d_q = (vv_a - vh_a) - (vv_b - vh_b)
    with rasterio.open(os.path.join(AQUI, "mapa_s1_alto_bajo_50m.tif"), "w", driver="GTiff", height=ny, width=nx, count=3,
                       dtype="float32", crs="EPSG:32618", transform=rasterio.transform.from_origin(x0, y0, 50, 50), compress="deflate") as dst:
        for i, a in enumerate([d_vv, d_vh, d_q], 1):
            dst.write(a.astype("float32"), i)
        dst.descriptions = ("dVV alto-bajo dB", "dVH alto-bajo dB", "d(VV-VH) alto-bajo dB")

    norte = y0 - (np.arange(ny) + 0.5) * 50
    N = np.repeat(norte[:, None], nx, axis=1)
    grupos = [(nombre, (cl == k)) for k, nombre in CLASES.items()]
    grupos += [("manglar " + s, (cl == 1) & (N >= a) & (N < b)) for s, a, b in SECTORES]
    filas = []
    for nombre, m in grupos:
        m = m & np.isfinite(d_vv) & np.isfinite(d_hh)
        for var, a in (("VV", d_vv), ("VH", d_vh), ("VV-VH", d_q)):
            v = a[m]
            filas.append(dict(clase=nombre, variable=var, n_pix_50m=int(m.sum()), mediana=round(float(np.median(v)), 2),
                              q25=round(float(np.percentile(v, 25)), 2), q75=round(float(np.percentile(v, 75)), 2),
                              frac_positiva=round(float((v > 0).mean()), 3)))
    res = pd.DataFrame(filas)
    res.to_csv(os.path.join(AQUI, "mapa_doble_rebote_s1_resumen.csv"), index=False)
    print(res.to_string(index=False))
    m = (cl == 1) & np.isfinite(d_vv) & np.isfinite(d_hh)
    from scipy.stats import spearmanr
    print("manglar: Spearman(dVV C, dHH L) por pixel rho %.2f" % spearmanr(d_vv[m], d_hh[m])[0])

    ext = [x0 / 1000, (x0 + nx * 50) / 1000, (y0 - ny * 50) / 1000, y0 / 1000]
    fig, axs = plt.subplots(1, 2, figsize=(11, 5.6), constrained_layout=True)
    for ax, (tit, a) in zip(axs, (("L-band, NISAR D083: ΔHH, high − low river level (dB)", d_hh),
                                   ("C-band, Sentinel-1 orbit 142: ΔVV, same date groups (dB)", d_vv))):
        ax.imshow(np.where(np.isin(cl, [1, 2]), np.nan, 0.0), extent=ext, cmap="Greys", vmin=-1, vmax=1, alpha=0.22, interpolation="nearest")
        ax.imshow(np.where(cl == 2, a, np.nan), extent=ext, cmap="RdBu_r", vmin=-2, vmax=2, alpha=0.35, interpolation="nearest")
        im = ax.imshow(np.where(cl == 1, a, np.nan), extent=ext, cmap="RdBu_r", vmin=-2, vmax=2, interpolation="nearest")
        for _, yy, _ in SECTORES[:2]:
            ax.axhline(yy / 1000, color="#444444", lw=0.6, ls=":")
        ax.set_title(tit, fontsize=10.5)
        ax.set_xlabel("UTM 18N easting (km)"); ax.set_ylabel("northing (km)"); ax.tick_params(labelsize=8)
    cb = fig.colorbar(im, ax=axs, shrink=0.8, pad=0.01); cb.set_label("dB, median of high-level minus median of low-level passes")
    fig.suptitle("Co-polar change between high and low Magdalena River level, 50 m: mangrove in full colour, dry forest control faded", fontsize=10.5)
    fig.savefig(os.path.join(AQUI, "fig_mapa_c_vs_l.png"), dpi=160)
    print("figura: fig_mapa_c_vs_l.png")


if __name__ == "__main__":
    main()
