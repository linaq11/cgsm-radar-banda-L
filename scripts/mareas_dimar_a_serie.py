# -*- coding: utf-8 -*-
"""Convierte la tabla oficial de pleamares y bajamares de la DIMAR (CCCP, pronostico de
Málaga) en la serie cada 10 minutos que lee perfil_pacifico_24.py, y la compara con
la predicción armonica propia.

ENTRADA: mareas_dimar_malaga.csv con una fila por extremo, columnas:
    fecha_hora_local, altura_lat_m
  (hora local de Colombia, UTC-5; altura referida al LAT como la publica la DIMAR).
  Ejemplo:
    2026-09-11 03:43, 4.24
    2026-09-11 09:38, 0.63
Entre extremos consecutivos se interpola con medio coseno, que es la forma de la
onda de marea entre una pleamar y una bajamar.

SALIDA: mareas_buenaventura.csv se reemplaza por la serie oficial (la propia queda
como mareas_prediccion_propia.csv) y se imprime la comparacion en las 24 pasadas.
"""
import os
import shutil

import numpy as np
import pandas as pd

import glob
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
# acepta uno o varios archivos: los que se pasen por linea de comandos, o por defecto
# mareas_dimar_malaga.csv y todos los "Málaga-Tabla-Pronóstico-AAAA.csv" descargados de la DIMAR
ENTRADAS = sys.argv[1:] or [f for f in [os.path.join(AQUI, "mareas_dimar_malaga.csv")] if os.path.exists(f)] + \
    sorted(glob.glob(os.path.join(AQUI, "M*laga-Tabla-Pron*stico-*.csv")))
if not ENTRADAS:
    raise SystemExit("falta la tabla de la DIMAR (mareas_dimar_malaga.csv o Málaga-Tabla-Pronóstico-AAAA.csv)")
print("entradas:", [os.path.basename(e) for e in ENTRADAS])
ENT = ENTRADAS[0]
import re
filas = []
for ent in ENTRADAS:
    texto = open(ent, encoding="utf-8-sig", errors="replace").read()
    if "fecha_hora_local" in texto:
        e = pd.read_csv(ent)
        for _, r in e.iterrows():
            filas.append(dict(t=pd.to_datetime(r["fecha_hora_local"]) + pd.Timedelta(hours=5), altura_lat_m=float(r["altura_lat_m"])))
        continue
    # tabla de la DIMAR, con o sin comillas: "Pleamar","03:43:00","4.24m","11/09/2026"
    for ln in texto.splitlines():
        ln = ln.replace('"', " ").replace(",", " ")
        m = re.search(r"(Pleamar|Bajamar)\s+(\d{1,2}:\d{2})(?::\d{2})?\s+([\d.]+)\s*m?\s+(\d{1,2}/\d{1,2}/\d{4})", ln, re.I)
        if m:
            filas.append(dict(t=pd.to_datetime(m.group(4) + " " + m.group(2), format="%d/%m/%Y %H:%M") + pd.Timedelta(hours=5),
                              altura_lat_m=float(m.group(3))))
ext = pd.DataFrame(filas)
if ext.empty:
    raise SystemExit("no se reconocio ninguna fila Pleamar/Bajamar")
ext = ext.drop_duplicates("t").sort_values("t").reset_index(drop=True)
print("extremos:", len(ext), "|", ext.t.min(), "a", ext.t.max(), "| alturas LAT %.2f a %.2f m" % (ext.altura_lat_m.min(), ext.altura_lat_m.max()))

t = pd.date_range(ext.t.iloc[0], ext.t.iloc[-1], freq="10min")
h = np.full(len(t), np.nan)
for k in range(len(ext) - 1):
    t0, t1 = ext.t[k], ext.t[k + 1]
    h0, h1 = ext.altura_lat_m[k], ext.altura_lat_m[k + 1]
    sel = (t >= t0) & (t <= t1)
    frac = (t[sel] - t0) / (t1 - t0)
    h[sel] = h0 + (h1 - h0) * (1 - np.cos(np.pi * frac.to_numpy())) / 2
nivel = np.nanmean(h)
oficial = pd.DataFrame({"t": t, "altura_m": np.round(h - nivel, 3)})
oficial.to_csv(os.path.join(AQUI, "mareas_dimar_serie.csv"), index=False)
print("serie oficial: %d registros cada 10 min, %s a %s, nivel medio %.2f m LAT restado" % (len(oficial), t[0], t[-1], nivel))

# serie de trabajo: oficial donde existe, predicción propia fuera de su cobertura
destino = os.path.join(AQUI, "mareas_buenaventura.csv")
prop = os.path.join(AQUI, "mareas_prediccion_propia.csv")
if not os.path.exists(prop):
    shutil.copy(destino, prop)
p = pd.read_csv(prop); p["t"] = pd.to_datetime(p["fecha_hora_utc"])
hib = p[["t", "altura_m"]].copy()
en_oficial = (hib.t >= t[0]) & (hib.t <= t[-1])
xp_o = (t - pd.Timestamp("1970-01-01")).total_seconds().to_numpy()
x_h = (hib.t - pd.Timestamp("1970-01-01")).dt.total_seconds().to_numpy()
hib.loc[en_oficial, "altura_m"] = np.round(np.interp(x_h[en_oficial], xp_o, oficial.altura_m), 3)
hib["fuente"] = np.where(en_oficial, "DIMAR", "prediccion_propia")
pd.DataFrame({"fecha_hora_utc": hib.t.dt.strftime("%Y-%m-%d %H:%M"), "altura_m": hib.altura_m, "fuente": hib.fuente}).to_csv(destino, index=False)
print("serie de trabajo escrita en mareas_buenaventura.csv: %d registros DIMAR, %d de prediccion propia" % (en_oficial.sum(), (~en_oficial).sum()))
serie = oficial.rename(columns={"t": "fecha_hora_utc"})

# comparacion con la predicción propia en las 24 pasadas NISAR
perf = os.path.join(AQUI, "perfil_pacifico_24.csv")
prop = os.path.join(AQUI, "mareas_prediccion_propia.csv")
if os.path.exists(perf) and os.path.exists(prop):
    p = pd.read_csv(prop); p["t"] = pd.to_datetime(p["fecha_hora_utc"])
    xp_p = (p.t - pd.Timestamp("1970-01-01")).dt.total_seconds().to_numpy()
    xp_o = (t - pd.Timestamp("1970-01-01")).total_seconds().to_numpy()
    pas = pd.read_csv(perf, parse_dates=["fecha_utc"]).drop_duplicates("escena")
    pas = pas[(pas.fecha_utc >= t[0]) & (pas.fecha_utc <= t[-1])].reset_index(drop=True)
    print("\npasadas NISAR dentro de la cobertura oficial: %d de 24" % len(pas))
    x = (pas.fecha_utc - pd.Timestamp("1970-01-01")).dt.total_seconds().to_numpy()
    pas["propia"] = np.interp(x, xp_p, p.altura_m); pas["oficial"] = np.interp(x, xp_o, serie.altura_m)
    print("\npasada           propia  oficial")
    for _, r in pas.iterrows():
        print("%s %s  %+.2f   %+.2f" % (r.escena, r.traza, r.propia, r.oficial))
    from scipy.stats import spearmanr
    print("Spearman propia-oficial en las 24 pasadas: %.3f | diferencia media %.2f m | rms %.2f m"
          % (spearmanr(pas.propia, pas.oficial)[0], (pas.propia - pas.oficial).mean(), np.sqrt(((pas.propia - pas.oficial) ** 2).mean())))
    print("luego: python perfil_pacifico_24.py && python marea_vs_radar.py")
