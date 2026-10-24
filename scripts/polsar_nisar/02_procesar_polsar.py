# -*- coding: utf-8 -*-
r"""Procesamiento PolSAR dual-pol de un recorte GSLC de la CGSM, con polsartools, siguiendo el cuaderno de Guaviare:
  1. import_nisar_gslc(mat="C2", azlks=2, rglks=2): C2 (C11, C22, C12) con 2 x 2 looks (5 m -> 10 m).
  2. filter_refined_lee(win=7): C2 filtrado.
  3. rgb_dp: compuesto RGB dual-pol.  4. h_alpha_dp: entropía H y ángulo alfa.  5. dprvi: índice DpRVI.
  6. Remuestreo de H, alfa, DpRVI, C11 y C22 (dB) a la malla del cubo (10 m, EPSG:9377) y extracción en los 880 puntos de la
     muestra (etiquetas v1.1, v1.3, fracción de copa e indicador de troncos) -> CSV para los contrastes de 03.
Entorno: C:\LINA\TOOLS\polsar_env (importar h5py antes que osgeo).
USO: polsar_env/Scripts/python 02_procesar_polsar.py 20251204 [path]
SALIDAS: <carpeta del h5>/<fecha>_P<path>/{C2, C2_rlee7, H_alpha, DpRVI, rgb} y RADAR/polsar_nisar/polsar_puntos_<fecha>_P<path>.csv
"""
import importlib.util
import os
import sys
import time
from pathlib import Path

_pd = os.path.join(importlib.util.find_spec("osgeo").submodule_search_locations[0], "data", "proj")   # PROJ del entorno, no el de PostGIS
if os.path.exists(os.path.join(_pd, "proj.db")): os.environ["PROJ_DATA"] = _pd; os.environ["PROJ_LIB"] = _pd
import h5py                      # antes que osgeo
from osgeo import gdal
import numpy as np
import pandas as pd
import polsartools as pst
import rasterio
from rasterio.warp import Resampling, reproject

FECHA = sys.argv[1]; PATH = int(sys.argv[2]) if len(sys.argv) > 2 else 11
BASE = Path("D:/TESIS_DATACUBE/NISAR_GSLC") if Path("D:/").exists() else Path("C:/LINA/NISAR_GSLC")
H5 = BASE / ("NISAR_GSLC_%s_P%03d_cgsm.h5" % (FECHA, PATH)); OUT = BASE / ("%s_P%03d" % (FECHA, PATH)); OUT.mkdir(exist_ok=True)
AQUI = Path(__file__).resolve().parent; MUESTRA = Path("C:/LINA/UNAL 2626-1/AVANCE TESIS/MUESTRA_2025")
REF = Path("C:/LINA/UNAL 2626-1/PERCEPCION REMOTA AVANZADA/informe2/datos/s2_2025_seca_rgb.tif")      # malla del cubo, 10 m EPSG:9377


def paso(nombre, fn):
    t = time.time(); r = fn(); print("%s: %.0f s" % (nombre, time.time() - t), flush=True); return r


def main():
    assert H5.exists(), H5
    c2 = OUT / "C2"
    if not any(c2.glob("C11*")):
        paso("1 C2 (2x2 looks)", lambda: pst.import_nisar_gslc(str(H5), mat="C2", azlks=2, rglks=2, fmt="tif", out_dir=str(OUT)))
    c2dir = next(p for p in sorted(OUT.rglob("C11.tif")) if "rlee" not in str(p) and "_" not in p.parent.name.replace("C2HX", "")).parent; print("C2 en", c2dir, flush=True)
    lee_c = sorted(p for p in OUT.rglob("C11.tif") if "rlee" in str(p) and p.parent.name.startswith("C2"))
    if not lee_c:
        paso("2 Lee refinado 7x7", lambda: pst.filter_refined_lee(str(c2dir), win=7, fmt="tif", sub_dir=True))
        lee_c = sorted(p for p in OUT.rglob("C11.tif") if "rlee" in str(p) and p.parent.name.startswith("C2"))
    lee = lee_c[0].parent; print("C2 filtrado en", lee, flush=True)
    paso("3 RGB dual-pol", lambda: pst.rgb_dp(str(lee), type=1, save_tif=True))
    paso("4 H/alfa dual-pol", lambda: pst.h_alpha_dp(str(lee), win=1, fmt="tif"))
    paso("5 DpRVI", lambda: pst.dprvi(str(lee), win=1, fmt="tif"))
    capas = {}
    for nombre, patron in (("H", "Hdp.tif"), ("alfa", "alphadp.tif"), ("dprvi", "dprvi.tif"), ("C11", "C11.tif"), ("C22", "C22.tif")):
        cand = sorted(lee.rglob(patron)) or sorted(OUT.rglob(patron)); assert cand, "no encuentro %s (%s)" % (nombre, patron); capas[nombre] = cand[0]
    print("capas:", {k: v.name for k, v in capas.items()}, flush=True)
    # 6 remuestreo a la malla del cubo y extracción en los puntos
    with rasterio.open(REF) as r: perfil = dict(crs=r.crs, transform=r.transform, width=r.width, height=r.height)
    e = pd.read_csv(MUESTRA / "etiquetas_2025_ampliada3.csv")
    from pyproj import Transformer
    x, y = Transformer.from_crs(4326, 9377, always_xy=True).transform(e.lon.values, e.lat.values); fil, col = rasterio.transform.rowcol(perfil["transform"], x, y)
    fil = np.clip(fil, 0, perfil["height"] - 1); col = np.clip(col, 0, perfil["width"] - 1); vals = {}
    for nombre, f in capas.items():
        with rasterio.open(f) as src:
            a = src.read(1).astype("float32"); nod = src.nodata
            if nod is not None: a[a == nod] = np.nan
            dst = np.full((perfil["height"], perfil["width"]), np.nan, "float32")
            reproject(a, dst, src_transform=src.transform, src_crs=src.crs, dst_transform=perfil["transform"], dst_crs=perfil["crs"], resampling=Resampling.bilinear, src_nodata=np.nan, dst_nodata=np.nan)
        if nombre in ("C11", "C22"): dst = 10 * np.log10(np.where(dst > 0, dst, np.nan))
        vals[nombre] = dst[fil, col]
        v3 = np.full(len(e), np.nan, "float32")
        for i, (r_, c_) in enumerate(zip(fil, col)):
            w = dst[max(r_ - 1, 0):r_ + 2, max(c_ - 1, 0):c_ + 2]; v3[i] = np.nanmean(w) if np.isfinite(w).any() else np.nan
        vals[nombre + "_3x3"] = v3
        with rasterio.open(OUT / ("%s_malla10m.tif" % nombre), "w", driver="GTiff", dtype="float32", count=1, nodata=np.nan, compress="deflate", **perfil) as dsto: dsto.write(dst, 1)
    sal = e[["id", "lon", "lat", "clase_final", "clase_final_v11"] + [c for c in e.columns if c in ("fraccion_copa_20261022", "troncos_muertos_20261022", "clase_regla_copa_20261022", "borde_final")]].copy()
    for k, v in vals.items(): sal[k] = v
    sal["fecha"] = FECHA; sal["path"] = PATH; f = AQUI / ("polsar_puntos_%s_P%03d.csv" % (FECHA, PATH)); sal.to_csv(f, index=False)
    print("escrito %s: %d puntos, con valor en %d" % (f.name, len(sal), int(np.isfinite(sal.alfa).sum())), flush=True)


if __name__ == "__main__":
    main()
