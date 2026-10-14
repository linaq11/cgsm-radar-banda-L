# -*- coding: utf-8 -*-
"""Paso 1 del trabajo de radar: perfil de retrodispersión NISAR sobre Bahía de Málaga
con las 24 escenas (12 ascendentes A004, 05:00 local; 12 descendentes D087, 18:00
local), por cobertura y por traza, con columna de marea lista para llenar.

COBERTURAS (400 puntos cada una, semilla 42): manglar = consenso WorldCover 2021 (95)
y Global Mangrove Watch 2020; bosque (WC 10) como control que no se inunda; humedal
herbaceo (WC 90); agua (WC 80).

MAREA. Si existe mareas_buenaventura.csv (columnas: fecha_hora_utc en formato
YYYY-MM-DD HH:MM, altura_m), se asigna a cada pasada la altura interpolada a la hora
exacta de adquisicion. Si no existe, la columna queda vacia y el script lo dice.

SALIDAS (en RADAR/):
  perfil_pacifico_24.csv     mediana e IQR de HH, HV, HH-HV por escena y clase, con traza,
                             hora local, incidencia y marea
  fig_perfil_pacifico_24.png serie temporal por traza (ingles)
  resumen en consola: diferencia entre trazas por clase y variacion dentro de cada traza

USO
    python perfil_pacifico_24.py
"""
import glob
import os
import sys
from datetime import datetime, timedelta

import ee
import h5py
import numpy as np
import pandas as pd
from pyproj import Transformer
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR = r"D:\TESIS_DATACUBE\NISAR_PACIFICO"
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
CAJA = [-77.40, 3.80, -77.10, 4.10]
MAREAS = os.path.join(AQUI, "mareas_buenaventura.csv")
N_PUNTOS = 400
if not os.path.isdir(DIR):
    sys.exit("ABORTA: D: desmontado")
rutas = sorted(glob.glob(os.path.join(DIR, "NISAR_MALAGA_*.h5")))
print("recortes en disco:", len(rutas), flush=True)

# ----------------------------------------------------------------- puntos por clase
ee.Initialize(project="basic-buttress-338101")
caja = ee.Geometry.Rectangle(CAJA)
wc = ee.Image("ESA/WorldCover/v200/2021").select("Map")
gmw = ee.ImageCollection("projects/sat-io/open-datasets/GMW/extent/GMW_V3") \
    .filter(ee.Filter.stringContains("system:index", "2020")).first().select(0).unmask(0).gt(0)
mascaras = {"manglar": wc.eq(95).And(gmw), "bosque": wc.eq(10), "humedal_herbaceo": wc.eq(90), "agua": wc.eq(80)}
df = []
for nombre, m in mascaras.items():
    fs = m.rename("m").selfMask().stratifiedSample(numPoints=N_PUNTOS, classBand="m", region=caja, scale=10, seed=42,
                                                   geometries=True, tileScale=4).getInfo()["features"]
    df += [dict(lon=f["geometry"]["coordinates"][0], lat=f["geometry"]["coordinates"][1], clase=nombre) for f in fs]
df = pd.DataFrame(df)
print("puntos:", df.clase.value_counts().to_dict(), flush=True)

# ----------------------------------------------------------------- marea (opcional)
mareas = None
if os.path.exists(MAREAS):
    mareas = pd.read_csv(MAREAS)
    mareas["t"] = pd.to_datetime(mareas["fecha_hora_utc"])
    mareas = mareas.sort_values("t")
    print("tabla de mareas:", len(mareas), "registros,", mareas.t.min(), "a", mareas.t.max(), flush=True)
else:
    print("sin mareas_buenaventura.csv: la columna marea_m queda vacia", flush=True)


def marea_en(t):
    if mareas is None:
        return np.nan
    if t < mareas.t.iloc[0] or t > mareas.t.iloc[-1]:
        return np.nan
    # segundos desde la epoca sin depender de la resolucion interna del datetime (pandas 3 usa microsegundos)
    xp = (mareas.t - pd.Timestamp("1970-01-01")).dt.total_seconds().to_numpy()
    x = (pd.Timestamp(t) - pd.Timestamp("1970-01-01")).total_seconds()
    return float(np.interp(x, xp, mareas.altura_m.to_numpy()))


def db(a):
    out = np.full(a.shape, np.nan, dtype="float32")
    ok = np.isfinite(a) & (a > 0)
    out[ok] = 10.0 * np.log10(a[ok])
    return out


# ----------------------------------------------------------------- lectura de escenas
filas = []
for r in rutas:
    nombre = os.path.basename(r)
    with h5py.File(r, "r") as h:
        epsg = int(h.attrs["epsg"])
        gr = h[GRUPO]
        xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
        fac = gr["rtcGammaToSigmaFactor"][:]
        hh, hv = db(gr["HHHH"][:] * fac), db(gr["HVHV"][:] * fac)
        t0 = h["science/LSAR/identification/zeroDopplerStartTime"][()]
        t0 = t0.decode() if isinstance(t0, bytes) else str(t0)
        ri = "science/LSAR/GCOV/metadata/radarGrid/incidenceAngle"
        inc = h[ri][:] if ri in h else None
        if inc is not None:
            ix, iy = h["science/LSAR/GCOV/metadata/radarGrid/xCoordinates"][:], h["science/LSAR/GCOV/metadata/radarGrid/yCoordinates"][:]
    t_utc = datetime.fromisoformat(t0[:19])
    t_loc = t_utc - timedelta(hours=5)
    traza = nombre.split("_")[3][:4]
    tr = Transformer.from_crs("EPSG:4326", "EPSG:%d" % epsg, always_xy=True)
    ux, uy = tr.transform(df.lon.to_numpy(), df.lat.to_numpy())
    i = np.clip(np.searchsorted(xc, ux) - 1, 0, len(xc) - 1)
    j = np.clip(len(yc) - np.searchsorted(yc[::-1], uy) - 1, 0, len(yc) - 1)
    vhh, vhv = hh[j, i], hv[j, i]
    if inc is not None:
        ang = inc[inc.shape[0] // 2] if inc.ndim == 3 else inc
        ii = np.clip(np.searchsorted(ix, ux) - 1, 0, len(ix) - 1)
        jj = np.clip(len(iy) - np.searchsorted(iy[::-1], uy) - 1, 0, len(iy) - 1)
        vinc = ang[jj, ii]
    else:
        vinc = np.full(len(df), np.nan)
    val = np.isfinite(vhh)
    for c in mascaras:
        m = (df.clase == c).to_numpy() & val
        d = vhh[m] - vhv[m]
        filas.append(dict(escena=nombre[13:21], traza=traza, direccion=traza[0], fecha_utc=t_utc, hora_local=t_loc.strftime("%H:%M"),
                          marea_m=marea_en(t_utc), clase=c, n=int(m.sum()), inc=float(np.nanmedian(vinc[m])),
                          HH=float(np.nanmedian(vhh[m])), HH_p25=float(np.nanpercentile(vhh[m], 25)), HH_p75=float(np.nanpercentile(vhh[m], 75)),
                          HV=float(np.nanmedian(vhv[m])), HV_p25=float(np.nanpercentile(vhv[m], 25)), HV_p75=float(np.nanpercentile(vhv[m], 75)),
                          HHmHV=float(np.nanmedian(d)), HHmHV_p25=float(np.nanpercentile(d, 25)), HHmHV_p75=float(np.nanpercentile(d, 75))))
    print("%s | %s | %s local | %d/%d puntos" % (nombre[13:26], t_utc.strftime("%Y-%m-%d %H:%M UTC"), t_loc.strftime("%H:%M"), val.sum(), len(df)), flush=True)

out = pd.DataFrame(filas).sort_values(["clase", "fecha_utc"])
out.to_csv(os.path.join(AQUI, "perfil_pacifico_24.csv"), index=False)

# ----------------------------------------------------------------- resumen
print("\n== mediana por clase y traza (dB), y variacion dentro de cada traza (sd entre fechas) ==")
res = out.groupby(["clase", "traza"]).agg(n_fechas=("escena", "nunique"), HH=("HH", "median"), HH_sd=("HH", "std"),
                                          HV=("HV", "median"), HV_sd=("HV", "std"), HHmHV=("HHmHV", "median"), HHmHV_sd=("HHmHV", "std"),
                                          inc=("inc", "median")).round(2)
print(res.to_string())
print("\n== diferencia ascendente (05:00) menos descendente (18:00), mediana por clase ==")
piv = out.groupby(["clase", "direccion"])[["HH", "HV", "HHmHV"]].median().unstack("direccion")
if ("HH", "A") in piv.columns and ("HH", "D") in piv.columns:
    dif = pd.DataFrame({v: piv[(v, "A")] - piv[(v, "D")] for v in ("HH", "HV", "HHmHV")}).round(2)
    print(dif.to_string())
    print("\nlectura: la diferencia entre trazas mezcla hora del dia, marea y geometria; solo con la marea por pasada se separa.")
else:
    print("solo hay una traza en disco; la comparacion entre horas queda pendiente.")
if out.marea_m.notna().any():
    print("\nmarea asignada a %d de %d escenas" % (out.drop_duplicates("escena").marea_m.notna().sum(), out.escena.nunique()))

# ----------------------------------------------------------------- figura
fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True)
col = {"manglar": "#1b7837", "bosque": "#4d4d4d", "humedal_herbaceo": "#b8860b", "agua": "#2166ac"}
nom = {"manglar": "Mangrove (WorldCover ∩ GMW)", "bosque": "Forest (control)", "humedal_herbaceo": "Herbaceous wetland", "agua": "Water"}
for ax, var, tit in zip(axes, ["HH", "HV", "HHmHV"], ["HH (dB)", "HV (dB)", "HH − HV (dB)"]):
    for c in mascaras:
        for dr, mk, ls in (("A", "o", "-"), ("D", "s", "--")):
            s = out[(out.clase == c) & (out.direccion == dr)].sort_values("fecha_utc")
            if not len(s):
                continue
            # la linea se corta donde hay más de 40 dias sin escenas (hueco feb-jun), para no
            # dibujar una tendencia que no se observo
            s = s.copy()
            s["tramo"] = (s.fecha_utc.diff() > pd.Timedelta(days=40)).cumsum()
            for k, (_, g) in enumerate(s.groupby("tramo")):
                ax.errorbar(g.fecha_utc, g[var], yerr=[g[var] - g[var + "_p25"], g[var + "_p75"] - g[var]], fmt=mk + ls, ms=4, lw=1.3,
                            capsize=2, color=col[c], alpha=0.9 if dr == "A" else 0.6,
                            label="%s, %s" % (nom[c], "ascending 05:00" if dr == "A" else "descending 18:00") if (var == "HH" and k == 0) else None)
    ax.set_ylabel(tit); ax.grid(alpha=0.3)
axes[0].legend(fontsize=7.5, ncol=2, loc="lower left")
axes[0].set_title("NISAR GCOV σ⁰ over Bahía de Málaga mangroves by track (median and IQR of 400 points per class)", fontsize=10.5)
axes[-1].set_xlabel("Acquisition date")
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_perfil_pacifico_24.png"), dpi=170)
print("\nfigura: fig_perfil_pacifico_24.png | tabla: perfil_pacifico_24.csv")
