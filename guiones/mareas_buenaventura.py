# -*- coding: utf-8 -*-
"""Prediccion de marea en Buenaventura para 2025-2026 por analisis armonico del
mareografo historico (UHSLC estacion 085, horario, 1953-2014, calidad revisada).

POR QUE. Las tablas oficiales de la DIMAR/CIOH son la fuente de referencia, pero no se
pudieron descargar desde esta maquina. La marea astronomica es determinista: con los
constituyentes armonicos ajustados a un registro largo se predice la altura a
cualquier hora futura, que es lo que hacen las tablas. No incluye el residuo
meteorologico (marejada, presion), pequeno frente a un rango de 3 a 4 m.

METODO. Minimos cuadrados sobre seno y coseno de 11 constituyentes (M2, S2, N2, K2,
K1, O1, P1, Q1, M4, MS4, MN4) con sus frecuencias astronomicas, ajustados a 2010-2014.
Sin correccion nodal (ciclo de 18,6 anos): error de amplitud de pocos por ciento,
irrelevante para ordenar pasadas por marea alta o baja. La calidad se mide
reconstruyendo 2014 y comparando con lo observado.

SALIDA. mareas_buenaventura.csv (fecha_hora_utc, altura_m respecto al nivel medio)
cada 10 minutos de oct-2025 a sep-2026, en el formato que lee perfil_pacifico_24.py.
"""
import os

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
# frecuencias en ciclos por hora (constantes astronomicas estandar)
FREQ = {"M2": 0.0805114007, "S2": 0.0833333333, "N2": 0.0789992488, "K2": 0.0835614924,
        "K1": 0.0417807462, "O1": 0.0387306544, "P1": 0.0415525871, "Q1": 0.0372185026,
        "M4": 0.1610228013, "MS4": 0.1638447340, "MN4": 0.1595106495}
T0 = pd.Timestamp("2000-01-01", tz="UTC")


def diseno(t):
    h = (t - T0) / pd.Timedelta(hours=1)
    h = np.asarray(h, dtype="float64")
    cols = [np.ones_like(h)]
    for f in FREQ.values():
        w = 2 * np.pi * f * h
        cols += [np.cos(w), np.sin(w)]
    return np.column_stack(cols)


raw = pd.read_csv(os.path.join(AQUI, "uhslc_h085_buenaventura.csv"), header=None, names=["a", "m", "d", "h", "mm"])
raw = raw[raw.mm != -32767]
raw["t"] = pd.to_datetime(dict(year=raw.a, month=raw.m, day=raw.d, hour=raw.h), utc=True)
raw["z"] = raw.mm / 1000.0
print("registro:", raw.t.min().date(), "a", raw.t.max().date(), "|", len(raw), "horas validas", flush=True)
aj = raw[(raw.t >= "2010-01-01") & (raw.t < "2014-01-01")]
val = raw[raw.t >= "2014-01-01"]
print("ajuste 2010-2013: %d horas | validacion 2014: %d horas" % (len(aj), len(val)), flush=True)

X = diseno(aj.t)
beta, *_ = np.linalg.lstsq(X, aj.z.to_numpy(), rcond=None)
nombres = list(FREQ)
amp = {n: float(np.hypot(beta[1 + 2 * i], beta[2 + 2 * i])) for i, n in enumerate(nombres)}
print("nivel medio %.3f m | amplitudes (m):" % beta[0], {k: round(v, 3) for k, v in sorted(amp.items(), key=lambda x: -x[1])}, flush=True)

rec = diseno(val.t) @ beta
res = val.z.to_numpy() - rec
print("validacion 2014: rango observado %.2f m | rmse %.3f m | varianza explicada %.1f %%"
      % (np.ptp(val.z), np.sqrt(np.mean(res ** 2)), 100 * (1 - np.var(res) / np.var(val.z))), flush=True)

tp = pd.date_range("2025-01-01", "2026-09-30 23:50", freq="10min", tz="UTC")   # desde ene-2025 para cubrir ALOS-2
hp = diseno(tp) @ beta - beta[0]
out = pd.DataFrame({"fecha_hora_utc": tp.strftime("%Y-%m-%d %H:%M"), "altura_m": np.round(hp, 3)})
out.to_csv(os.path.join(AQUI, "mareas_prediccion_propia.csv"), index=False)
if not os.path.exists(os.path.join(AQUI, "mareas_dimar_serie.csv")):
    out.to_csv(os.path.join(AQUI, "mareas_buenaventura.csv"), index=False)   # sin tabla oficial, la propia es la serie de trabajo
else:
    print("hay serie oficial: corre mareas_dimar_a_serie.py para rehacer la serie de trabajo hibrida")
print("prediccion: %d registros | rango %.2f a %.2f m respecto al nivel medio" % (len(out), hp.min(), hp.max()), flush=True)
print("escrito mareas_buenaventura.csv")
