# -*- coding: utf-8 -*-
"""Evalúa la clave de interpretación SAR con la muestra de referencia de 2025.

PROPÓSITO
Contrastar las firmas y los umbrales derivados inicialmente de las coberturas de referencia con
una muestra propia de 720 puntos distribuidos en seis clases.

ANÁLISIS
1. Firmas multifecha por clase en bandas C y L: copolar, cruzada y diferencia copolar - cruzada.
2. Separabilidad de Jeffries-Matusita entre pares de clases con banda C, banda L y las dos.
3. Aplicación punto a punto de las cuatro decisiones estáticas de la clave y comparación con la
   clase de referencia: agua abierta (VV < -17 dB y VH < -25 dB); superficie oscura con
   vegetación o borde (VV < -12 dB), compatible con vegetación flotante si VV-VH >= 6,5 dB y sin
   decisión en caso contrario; dosel cerrado (VV >= -12 dB y HH-HV < 7,3 dB); dosel abierto o
   herbáceo (VV >= -12 dB y HH-HV >= 7,3 dB). La respuesta hidrológica que distingue manglar de
   bosque no inundable es de series temporales y no se evalúa a escala de punto.

IMPORTANTE
Los umbrales se definen y se evalúan con la misma muestra de 720 puntos, de modo que las métricas
corresponden a resustitución y no a validación independiente.

DATOS
Sentinel-1 GRD, órbita descendente 142, y NISAR L2 GCOV, trayectoria descendente D083, en el
periodo del informe. Valor del píxel de 10 m en cada punto (media 3 x 3 en NISAR) y mediana
entre pasadas.

USO
    python clave_vs_muestra2025.py [s1] [nisar] [clave]
Sin argumentos ejecuta el flujo completo. Salidas: clave_muestra2025_puntos.csv,
clave_muestra2025_firmas.csv, clave_muestra2025_jm.csv y clave_muestra2025_regla.csv.
"""
import glob
import os
GAMMA0 = os.environ.get("RADAR_MAGNITUD", "sigma0").lower() == "gamma0"   # gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
SUF = "_gamma0" if GAMMA0 else ""
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
PUNTOS = os.path.join(AQUI, "clave_muestra2025_puntos%s.csv" % SUF)
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


def s1_db(im):
    """Sentinel-1 en dB; con GAMMA0, gamma cero elipsoidal: sigma0 - 10 log10(cos(angulo))."""
    v = im.select(["VV", "VH"])
    return v.subtract(im.select("angle").multiply(np.pi / 180).cos().log10().multiply(10)) if GAMMA0 else v


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
        img = ee.ImageCollection([s1_db(ee.Image("COPERNICUS/S1_GRD/" + i)) for i in ps["ids"]]).mosaic()
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
            fac = 1.0 if GAMMA0 else gr["rtcGammaToSigmaFactor"][:]
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
    """Las cuatro decisiones estáticas de la clave del informe, con sus umbrales literales.
    1. agua abierta: VV < -17 dB y VH < -25 dB;
    2. superficie oscura con vegetación o borde: VV < -12 dB sin cumplir la anterior; con
       VV-VH >= 6,5 dB es compatible con vegetación flotante, en caso contrario no hay decisión;
    3. dosel cerrado: VV >= -12 dB y HH-HV < 7,3 dB (compatible sobre todo con manglar intacto);
    4. dosel abierto o herbáceo: VV >= -12 dB y HH-HV >= 7,3 dB (manglar degradado, humedal
       herbáceo y parte de la clase otro, que no se separan con estas bandas)."""
    if np.isnan(r.VV):
        return "sin decision"
    if r.VV < -17 and r.VH < -25:
        return "1 agua abierta"
    if r.VV < -12:
        return "2 vegetacion flotante" if r.VVmVH >= 6.5 else "sin decision"
    if np.isnan(r.HHmHV):
        return "sin decision"
    return "3 dosel cerrado" if r.HHmHV < 7.3 else "4 dosel abierto"


def analizar(d):
    t = d[d.clase_final.isin(CLASES)].copy()
    # 1) firmas por clase
    filas = []
    for c in CLASES:
        g = t[t.clase_final == c]
        filas.append(dict(clase=c, n=len(g), VV=g.VV.median(), VH=g.VH.median(), VVmVH=g.VVmVH.median(),
                          HH=g.HH.median(), HV=g.HV.median(), HHmHV=g.HHmHV.median(), n_nisar=int(g.HH.notna().sum())))
    firmas = pd.DataFrame(filas).round(1)
    firmas.to_csv(os.path.join(AQUI, "clave_muestra2025_firmas%s.csv" % SUF), index=False)
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
    jmt.to_csv(os.path.join(AQUI, "clave_muestra2025_jm%s.csv" % SUF), index=False)
    print("\nSeparabilidad JM por pares:\n" + jmt[["par", "jm C (VV, VH, VV-VH)", "jm L (HH, HV, HH-HV)", "jm C + L"]].to_string(index=False))
    # 3) regla de lectura
    t["regla"] = t.apply(regla, axis=1)
    cm = pd.crosstab(t.clase_final, t.regla)
    cm.to_csv(os.path.join(AQUI, "clave_muestra2025_regla%s.csv" % SUF))
    print("\nRegla de lectura (filas: clase_final; columnas: lo que dice la regla):\n" + cm.to_string())
    ok = {"agua": "1 agua abierta", "vegetacion_flotante": "2 vegetacion flotante", "manglar_intacto": "3 dosel cerrado",
          "manglar_degradado": "4 dosel abierto", "humedal_herbaceo": "4 dosel abierto", "otro": "4 dosel abierto"}
    dec = t[t.regla != "sin decision"]
    aciertos = sum(int(((dec.clase_final == c) & (dec.regla == v)).sum()) for c, v in ok.items())
    print("  decide en %d de %d puntos y acierta en %d (%.1f %% de los decididos, %.1f %% del total); resustitución" % (
        len(dec), len(t), aciertos, 100 * aciertos / len(dec), 100 * aciertos / len(t)))
    for c in CLASES:
        g = t[t.clase_final == c]
        print("  %-22s n %3d | acierta %3d | sin decisión %3d" % (c, len(g), int((g.regla == ok[c]).sum()), int((g.regla == "sin decision").sum())))
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
