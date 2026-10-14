# -*- coding: utf-8 -*-
"""Inventario de las escenas NISAR GCOV disponibles: fecha, orbita, polarizaciones,
incidencia y cobertura del AOI. Es el primer paso del experimento de ablacion que
decide si NISAR se queda en la tesis (criterio de disponibilidad: al menos una
adquisicion por estacion seca y una por humeda con cobertura completa del AOI).

Salida: tabla en pantalla y PUBLICACION_GEE/inventario_nisar.csv
"""
import csv
import glob
import json
import os
import re
import sys

import _proj  # noqa: F401

import h5py
import numpy as np
from pyproj import Transformer

DIR = r"D:\TESIS_DATACUBE\NISAR"
ZARR = r"D:\TESIS_DATACUBE\cgsm_cube.zarr"
SAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventario_nisar.csv")
GRUPO = "science/LSAR/GCOV/grids/frequencyA"

if not os.path.isdir(DIR):
    sys.exit("ABORTA: D: desmontado")

# extension del AOI (malla del cubo) en UTM 18N
at = json.load(open(os.path.join(ZARR, "zarr.json"), encoding="utf-8"))["attributes"]
tr = at["transform"]
alto, ancho = 6022, 7150
t = Transformer.from_crs("EPSG:9377", "EPSG:32618", always_xy=True)
xs, ys = [], []
for cx in (tr[2], tr[2] + ancho * 10):
    for cy in (tr[5], tr[5] - alto * 10):
        u, v = t.transform(cx, cy)
        xs.append(u)
        ys.append(v)
X0, X1, Y0, Y1 = min(xs), max(xs), min(ys), max(ys)
AREA_AOI = (X1 - X0) * (Y1 - Y0)


def attr(h, rutas):
    """Primer atributo o dataset escalar que exista entre varias rutas candidatas."""
    for r in rutas:
        if r in h:
            v = h[r][()]
            return v.decode() if isinstance(v, bytes) else v
    return None


filas = []
for ruta in sorted(glob.glob(os.path.join(DIR, "*.h5"))):
    nombre = os.path.basename(ruta)
    # GCOV completo (..._20251204T232730_...) o recorte del AOI (NISAR_AOI_20251204_...)
    m = re.search(r"(20\d{6})T\d{6}", nombre) or re.search(r"NISAR_AOI_(20\d{6})", nombre)
    fecha = "%s-%s-%s" % (m.group(1)[:4], m.group(1)[4:6], m.group(1)[6:]) if m else "?"
    with h5py.File(ruta, "r") as h:
        gr = h[GRUPO]
        xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
        pols = [p.decode() if isinstance(p, bytes) else str(p) for p in gr["listOfPolarizations"][:]] \
            if "listOfPolarizations" in gr else [k for k in gr.keys() if re.fullmatch(r"[HV]{4}", k)]
        orbita = attr(h, ["science/LSAR/identification/orbitPassDirection"])
        modo = attr(h, ["science/LSAR/identification/productType"])
        # recorte del AOI dentro de la malla de la escena
        i0, i1 = np.searchsorted(xc, [X0, X1])
        j1, j0 = len(yc) - np.searchsorted(yc[::-1], [Y0, Y1])
        i0, i1, j0, j1 = max(i0, 0), min(i1, len(xc)), max(j0, 0), min(j1, len(yc))
        ext_x = (min(xc[-1], X1) - max(xc[0], X0)) if i1 > i0 else 0
        ext_y = (min(yc[0], Y1) - max(yc[-1], Y0)) if j1 > j0 else 0
        frac_bbox = max(0.0, ext_x * ext_y / AREA_AOI)
        # fraccion de pixeles validos dentro del AOI, muestreando cada 10 px
        val = float("nan")
        if i1 > i0 and j1 > j0:
            hh = gr["HHHH"][j0:j1:10, i0:i1:10]
            val = float(np.isfinite(hh).mean()) * frac_bbox
        # incidencia, si el producto la trae
        inc = None
        for cand in ("science/LSAR/GCOV/metadata/radarGrid/incidenceAngle",
                     "science/LSAR/GCOV/metadata/calibrationInformation/geometry/incidenceAngle"):
            if cand in h:
                a = h[cand][:]
                inc = "%.1f-%.1f" % (np.nanmin(a), np.nanmax(a))
                break
    filas.append(dict(archivo=nombre, fecha=fecha, orbita=orbita, producto=modo,
                      polarizaciones="+".join(pols), incidencia=inc,
                      cobertura_bbox=round(frac_bbox, 3), cobertura_valida=round(val, 3)))

with open(SAL, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(filas[0].keys()))
    w.writeheader()
    w.writerows(filas)

print("escenas NISAR: %d" % len(filas))
print("%-10s %-11s %-9s %-14s %-11s %8s %8s" % ("fecha", "orbita", "prod", "pols", "incid", "bbox", "valida"))
for r in filas:
    print("%-10s %-11s %-9s %-14s %-11s %8.2f %8.2f" % (
        r["fecha"], r["orbita"], r["producto"], r["polarizaciones"], r["incidencia"],
        r["cobertura_bbox"], r["cobertura_valida"]))
seca = [r for r in filas if r["fecha"][5:7] in ("12", "01", "02", "03", "04")]
hum = [r for r in filas if r["fecha"][5:7] in ("05", "06", "07", "08", "09", "10", "11")]
print("\nestacion seca (dic-abr): %d escenas | humeda (may-nov): %d escenas" % (len(seca), len(hum)))
print("escrito:", SAL)
