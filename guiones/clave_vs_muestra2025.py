# -*- coding: utf-8 -*-
r"""La clave de interpretacion del avance de radar, sometida a la muestra de referencia 2025.

PARA QUE. La seccion "Clave de interpretacion por cobertura y mecanismo" del informe se construyo
con 400 puntos por clase de los productos globales (WorldCover 2021 y GMW 2020). La muestra 2025
(720 puntos, clase_final: revisada bajo el criterio v1 en los ids 1-400 y primera pasada en 401-720)
es la referencia propia que la clave no tenia. Aqui se mide, sobre esos 720 puntos y sin reajustar
ningun umbral:
  1. la firma por clase en las dos bandas (mediana entre pasadas del copolar, del cruzado y de su
     diferencia), comparable con la Tabla 10 del informe;
  2. la separabilidad por pares (Jeffries-Matusita) con banda C sola, banda L sola y las dos;
  3. la regla de lectura de cinco pasos, aplicada punto a punto como arbol de decision con los
     umbrales tal como estan escritos en el informe, contra clase_final (matriz de confusion y
     exactitud por clase). El paso 4 (manglar frente a bosque seco por respuesta hidrologica) y el
     paso 5 (firma de inundacion) son de series temporales, no de un pixel: no se aplican aqui.

DATOS. Sentinel-1 GRD IW, orbita descendente 142, oct-2025 a sep-2026, pasadas con cobertura >= 90 %
del AOI, VV y VH en dB tal como los entrega Earth Engine, valor del pixel de 10 m en cada punto y
mediana entre pasadas. NISAR L2 GCOV traza descendente 083, los recortes NISAR_AOI_*.h5 del disco
(gamma0 RTC -> sigma0 con rtcGammaToSigmaFactor, dB), media 3x3 y mediana entre pasadas; las
cinco escenas de la traza ascendente 007 se excluyen como en el informe.

USO: python clave_vs_muestra2025.py [s1] [nisar] [clave]
     sin argumentos corre todo. Salidas: clave_muestra2025_puntos.csv (valores por punto),
     clave_muestra2025_firmas.csv, clave_muestra2025_jm.csv, clave_muestra2025_regla.csv
"""
import glob
import os
import sys
from datetime import datetime
from itertools import combinations

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
MUESTRA = os.path.join(AQUI, "..", "AVANCE TESIS", "MUESTRA_2025", "etiquetas_2025.csv")
NISAR_DIR = r"D:\TESIS_DATACUBE\NISAR"
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
T0, T1 = "2025-10-01", "2026-09-12"          # mismo periodo que el informe
ORBITA_S1 = 142                               # descendente, la de la Tabla 10
TRAZA_NISAR = "D"                             # descendente 083
PUNTOS = os.path.join(AQUI, "clave_muestra2025_puntos.csv")
QUE = [a for a in sys.argv[1:] if a in ("s1", "nisar", "clave")] or ["s1", "nisar", "clave"]
CLASES = ["agua", "vegetacion_flotante", "humedal_herbaceo", "manglar_degradado", "manglar_intacto", "otro"]


def db(a):
    out = np.full(a.shape, np.nan, dtype="float32")
    ok = np.isfinite(a) & (a > 0)
    out[ok] = 10.0 * np.log10(a[ok])
    return out


def cargar_puntos():
    d = pd.read_csv(MUESTRA)
    d = d[d.clase_final != "DESCARTAR"][["id", "lon", "lat", "clase_final", "borde_final", "confianza"]].copy()
    if os.path.exists(PUNTOS):
        prev = pd.read_csv(PUNTOS)
        d = d.merge(prev.drop(columns=[c for c in ("lon", "lat", "clase_final", "borde_final", "confianza") if c in prev]), on="id", how="left")
    return d


def muestrear_s1(d):
    import ee
    ee.Initialize(project="basic-buttress-338101")
    aoi = ee.FeatureCollection("projects/basic-buttress-338101/assets/AOI_tesis_CGSM_v1").geometry()
    fc = ee.FeatureCollection([ee.Feature(ee.Geometry.Point([float(r.lon), float(r.lat)]), {"id": int(r.id)}) for r in d.itertuples()])
    col = (ee.ImageCollection("COPERNICUS/S1_GRD").filterBounds(aoi).filterDate(T0, T1)
           .filter(ee.Filter.eq("instrumentMode", "IW")).filter(ee.Filter.eq("relativeOrbitNumber_start", ORBITA_S1))
           .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV")).filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VH")))
    meta = sorted(col.reduceColumns(ee.Reducer.toList(2), ["system:index", "system:time_start"]).get("list").getInfo(), key=lambda x: x[1])
    pasadas = []
    for idx, t0 in meta:
        if pasadas and abs(t0 - pasadas[-1]["t0"]) < 5 * 60 * 1000:
            pasadas[-1]["ids"].append(idx)
        else:
            pasadas.append(dict(ids=[idx], t0=t0))
    print("S1 orbita %d: %d escenas, %d pasadas" % (ORBITA_S1, len(meta), len(pasadas)), flush=True)
    vv, vh = {}, {}
    for ps in pasadas:
        img = ee.ImageCollection([ee.Image("COPERNICUS/S1_GRD/" + i).select(["VV", "VH"]) for i in ps["ids"]]).mosaic()
        cob = img.select("VV").mask().reduceRegion(ee.Reducer.mean(), aoi, 300, maxPixels=1e9).getInfo().get("VV") or 0
        if cob < 0.9:
            continue
        m = img.reduceRegions(fc, ee.Reducer.first(), 10).getInfo()["features"]
        for f in m:
            p = f["properties"]
            if p.get("VV") is not None:
                vv.setdefault(p["id"], []).append(p["VV"]); vh.setdefault(p["id"], []).append(p["VH"])
        print("   S1 %s: %d puntos" % (pd.Timestamp(ps["t0"], unit="ms").strftime("%Y-%m-%d"), len(m)), flush=True)
    d["s1_n"] = d.id.map(lambda i: len(vv.get(i, [])))
    d["VV"] = d.id.map(lambda i: np.median(vv[i]) if i in vv else np.nan)
    d["VH"] = d.id.map(lambda i: np.median(vh[i]) if i in vh else np.nan)
    d["VVmVH"] = d.id.map(lambda i: np.median(np.array(vv[i]) - np.array(vh[i])) if i in vv else np.nan)
    return d


def muestrear_nisar(d):
    import h5py
    from pyproj import Transformer
    from scipy.ndimage import uniform_filter
    rutas = sorted(glob.glob(os.path.join(NISAR_DIR, "NISAR_AOI_*.h5")))
    if not rutas:
        sys.exit("NISAR: sin recortes en %s (D: desmontado?)" % NISAR_DIR)
    hh_l, hv_l, usadas = {}, {}, []
    for r in rutas:
        with h5py.File(r, "r") as h:
            d0 = h["science/LSAR/identification/orbitPassDirection"][()]; d0 = (d0.decode() if isinstance(d0, bytes) else str(d0))[0].upper()
            if d0 != TRAZA_NISAR:
                continue
            gr = h[GRUPO]
            xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
            fac = gr["rtcGammaToSigmaFactor"][:]
            hh = db(uniform_filter(np.nan_to_num(gr["HHHH"][:] * fac), 3))
            hv = db(uniform_filter(np.nan_to_num(gr["HVHV"][:] * fac), 3))
            t0 = h["science/LSAR/identification/zeroDopplerStartTime"][()]; t0 = t0.decode() if isinstance(t0, bytes) else str(t0)
            epsg = int(h.attrs["epsg"]) if "epsg" in h.attrs else 32618
        tr = Transformer.from_crs("EPSG:4326", "EPSG:%d" % epsg, always_xy=True)
        ux, uy = tr.transform(d.lon.to_numpy(), d.lat.to_numpy())
        i = np.clip(np.searchsorted(xc, ux) - 1, 0, len(xc) - 1)
        j = np.clip(len(yc) - np.searchsorted(yc[::-1], uy) - 1, 0, len(yc) - 1)
        vhh, vhv = hh[j, i], hv[j, i]
        for k, pid in enumerate(d.id):
            if np.isfinite(vhh[k]) and np.isfinite(vhv[k]):
                hh_l.setdefault(pid, []).append(float(vhh[k])); hv_l.setdefault(pid, []).append(float(vhv[k]))
        usadas.append(os.path.basename(r))
        print("NISAR %s %s" % (t0[:10], os.path.basename(r)), flush=True)
    print("NISAR traza %s: %d escenas usadas" % (TRAZA_NISAR, len(usadas)), flush=True)
    d["nisar_n"] = d.id.map(lambda i: len(hh_l.get(i, [])))
    d["HH"] = d.id.map(lambda i: np.median(hh_l[i]) if i in hh_l else np.nan)
    d["HV"] = d.id.map(lambda i: np.median(hv_l[i]) if i in hv_l else np.nan)
    d["HHmHV"] = d.id.map(lambda i: np.median(np.array(hh_l[i]) - np.array(hv_l[i])) if i in hh_l else np.nan)
    return d


def jm(a, b):
    """Jeffries-Matusita con Bhattacharyya gaussiana; a y b de forma (n, k)."""
    ma, mb = a.mean(0), b.mean(0)
    ca, cb = np.cov(a, rowvar=False) + 1e-6 * np.eye(a.shape[1]), np.cov(b, rowvar=False) + 1e-6 * np.eye(a.shape[1])
    c = (ca + cb) / 2
    dm = ma - mb
    B = dm @ np.linalg.solve(c, dm) / 8 + 0.5 * np.log(np.linalg.det(c) / np.sqrt(np.linalg.det(ca) * np.linalg.det(cb)))
    return float(2 * (1 - np.exp(-B)))


def regla(r):
    """Pasos 1 a 3 de la regla de lectura del informe, con sus umbrales literales.
    1. copolar < -17 dB y cruzado < -25 dB: agua abierta (se evalua en banda C, VV/VH).
    2. VV entre -17 y -12 con VV-VH cerca de 7,5 dB (se toma 6,5 a 8,5): vegetacion sobre lamina.
    3. VV > -11: dosel o vegetacion densa; la banda L desempata: HH-HV cerca de 8 (>= 7,25) es
       humedal herbaceo; cerca de 6,5 (< 7,25) es manglar o bosque. Sin banda L: 'dosel'.
    Lo que no cae en ninguna franja queda 'sin regla'."""
    if np.isnan(r.VV):
        return "sin dato"
    if r.VV < -17 and r.VH < -25:
        return "agua"
    if -17 <= r.VV < -12 and 6.5 <= r.VVmVH <= 8.5:
        return "vegetacion_flotante"
    if r.VV > -11:
        if np.isnan(r.HHmHV):
            return "dosel (sin banda L)"
        return "humedal_herbaceo" if r.HHmHV >= 7.25 else "manglar_o_bosque"
    return "sin regla"


def analizar(d):
    t = d[d.clase_final.isin(CLASES)].copy()
    # 1) firmas por clase
    filas = []
    for c in CLASES:
        g = t[t.clase_final == c]
        filas.append(dict(clase=c, n=len(g), VV=g.VV.median(), VH=g.VH.median(), VVmVH=g.VVmVH.median(),
                          HH=g.HH.median(), HV=g.HV.median(), HHmHV=g.HHmHV.median(), n_nisar=int(g.HH.notna().sum())))
    firmas = pd.DataFrame(filas).round(1)
    firmas.to_csv(os.path.join(AQUI, "clave_muestra2025_firmas.csv"), index=False)
    print("\nFirmas por clase (mediana entre pasadas y entre puntos, dB):\n" + firmas.to_string(index=False))
    # 2) separabilidad por pares
    conj = {"C (VV, VH, VV-VH)": ["VV", "VH", "VVmVH"], "L (HH, HV, HH-HV)": ["HH", "HV", "HHmHV"],
            "C + L": ["VV", "VH", "VVmVH", "HH", "HV", "HHmHV"]}
    filas = []
    for c1, c2 in combinations(CLASES, 2):
        f = dict(par="%s | %s" % (c1, c2))
        for nombre, cols in conj.items():
            a = t[t.clase_final == c1][cols].dropna().to_numpy(); b = t[t.clase_final == c2][cols].dropna().to_numpy()
            f["jm " + nombre] = round(jm(a, b), 2) if len(a) > 5 and len(b) > 5 else np.nan
            f["n " + nombre] = "%d+%d" % (len(a), len(b))
        filas.append(f)
    jmt = pd.DataFrame(filas)
    jmt.to_csv(os.path.join(AQUI, "clave_muestra2025_jm.csv"), index=False)
    print("\nSeparabilidad JM por pares:\n" + jmt[["par", "jm C (VV, VH, VV-VH)", "jm L (HH, HV, HH-HV)", "jm C + L"]].to_string(index=False))
    # 3) regla de lectura
    t["regla"] = t.apply(regla, axis=1)
    cm = pd.crosstab(t.clase_final, t.regla)
    cm.to_csv(os.path.join(AQUI, "clave_muestra2025_regla.csv"))
    print("\nRegla de lectura (filas: clase_final; columnas: lo que dice la regla):\n" + cm.to_string())
    ok = {"agua": ["agua"], "vegetacion_flotante": ["vegetacion_flotante"], "humedal_herbaceo": ["humedal_herbaceo"],
          "manglar_degradado": ["manglar_o_bosque"], "manglar_intacto": ["manglar_o_bosque"], "otro": ["manglar_o_bosque", "sin regla"]}
    for c in CLASES:
        g = t[t.clase_final == c]
        print("  %-22s n %3d | acierta %3d (%.2f) | sin regla %3d | sin dato %3d" % (
            c, len(g), g.regla.isin(ok[c]).sum(), g.regla.isin(ok[c]).mean(), (g.regla == "sin regla").sum(), (g.regla == "sin dato").sum()))
    return t


def main():
    d = cargar_puntos()
    if "s1" in QUE:
        d = muestrear_s1(d)
        d.to_csv(PUNTOS, index=False)
    if "nisar" in QUE:
        d = muestrear_nisar(d)
        d.to_csv(PUNTOS, index=False)
    if "clave" in QUE:
        if "VV" not in d or "HH" not in d:
            sys.exit("faltan valores por punto: correr primero s1 y nisar")
        t = analizar(d)
        t.to_csv(PUNTOS, index=False)


if __name__ == "__main__":
    main()
