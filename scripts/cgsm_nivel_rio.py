# -*- coding: utf-8 -*-
"""Prueba de doble rebote en la CGSM con el nivel del río Magdalena como forzamiento.

Reutiliza las medianas por pasada y clase de cgsm_temporada.py (cgsm_temporada_nisar.csv,
_s1.csv, _alos2.csv) y les asigna el nivel del río en el momento de cada pasada, tomado de
la estación automática Remolino (IDEAM 2904700095, datos abiertos), o de la estación que
se indique. Regla de lectura, la misma de Bahía de Málaga: manglar menos bosque, diferencia
entre el tercio de nivel alto y el de nivel bajo, y Spearman con el nivel.

USO
    python cgsm_nivel_rio.py [codigo_estacion]      (por defecto 2904700095)

Salida: cgsm_nivel_rio_resumen.csv, fig_cgsm_nivel_rio.png
"""
import os
GAMMA0 = os.environ.get("RADAR_MAGNITUD", "sigma0").lower() == "gamma0"   # gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
SUF = "_gamma0" if GAMMA0 else ""
import sys
from glob import glob

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTACION = sys.argv[1] if len(sys.argv) > 1 else "2904700095"
MIN_PASADAS = 6

# 1. Serie de nivel: se prefiere el instantáneo; si no hay, el máximo diario.
niveles = []
for nombre in ("instantaneo", "maximo", "minimo"):
    f = os.path.join(AQUI, f"nivel_ideam_{nombre}.csv")
    if os.path.exists(f):
        n = pd.read_csv(f, dtype={"codigoestacion": str})
        n = n[n.codigoestacion == ESTACION].copy()
        if len(n):
            n["t"] = pd.to_datetime(n.fechaobservacion)
            n["nivel"] = pd.to_numeric(n.valorobservado, errors="coerce")
            n = n.dropna(subset=["nivel"]).sort_values("t")
            niveles.append((nombre, n))
if not niveles:
    sys.exit(f"ABORTA: no hay nivel para la estación {ESTACION} en nivel_ideam_*.csv")
tipo, niv = niveles[0]
unidad = niv.unidadmedida.iloc[0] if "unidadmedida" in niv else "?"
estacion_nombre = niv.nombreestacion.iloc[0] if "nombreestacion" in niv else ESTACION
print(f"nivel {tipo} de {estacion_nombre} ({ESTACION}): {len(niv)} registros, "
      f"{niv.t.min()} a {niv.t.max()}, {niv.nivel.min():.2f} a {niv.nivel.max():.2f} {unidad}")
# Las fechas del IDEAM son hora local (UTC−5); las pasadas de radar vienen en UTC.
serie = niv.set_index("t").nivel.resample("1h").mean().interpolate(limit=48)
EPOCA = pd.Timestamp("1970-01-01")
serie_seg = (serie.index - EPOCA).total_seconds().values      # segundos, sin depender de la resolución interna
print(f"registros en cero: {int((niv.nivel == 0).sum())} de {len(niv)}")


def nivel_en(fecha_utc):
    t_local = pd.Timestamp(fecha_utc) - pd.Timedelta(hours=5)
    if t_local < serie.index.min() or t_local > serie.index.max():
        return np.nan
    return float(np.interp((t_local - EPOCA).total_seconds(), serie_seg, serie.values))


# 2. Pasadas de radar por sensor y traza.
filas = []
for f in glob(os.path.join(AQUI, "cgsm_temporada_*.csv")):
    if "resumen" in f or "_CAJA" in f or (("_gamma0" in f) != GAMMA0):        # las copias _CAJA son la región anterior, no se mezclan
        continue
    d = pd.read_csv(f)
    d["nivel"] = d.fecha_utc.apply(nivel_en)
    filas.append(d)
todo = pd.concat(filas, ignore_index=True).dropna(subset=["nivel"])
piv = todo.pivot_table(index=["sensor", "traza", "hora_local", "escena", "fecha_utc", "nivel"],
                       columns="clase", values=["CO", "X", "COmX"]).reset_index()
piv.columns = ["_".join(c).strip("_") if c[1] else c[0] for c in piv.columns]

res, paneles = [], []
for (sensor, traza), g in piv.groupby(["sensor", "traza"]):
    hora = g.hora_local.mode().iloc[0]                 # las pasadas de una traza varían un minuto
    if len(g) < MIN_PASADAS:
        print(f"{sensor} {traza}: solo {len(g)} pasadas con nivel, no se evalúa")
        continue
    g = g.sort_values("nivel")
    k = max(len(g) // 3, 2)
    bajo, alto = g.head(k), g.tail(k)
    for var in ("CO", "X", "COmX"):
        for clase in ("manglar", "bosque", "manglar_menos_bosque"):
            y = (g[f"{var}_manglar"] - g[f"{var}_bosque"]) if clase == "manglar_menos_bosque" else g[f"{var}_{clase}"]
            yb = (bajo[f"{var}_manglar"] - bajo[f"{var}_bosque"]) if clase == "manglar_menos_bosque" else bajo[f"{var}_{clase}"]
            ya = (alto[f"{var}_manglar"] - alto[f"{var}_bosque"]) if clase == "manglar_menos_bosque" else alto[f"{var}_{clase}"]
            rho, p = spearmanr(g.nivel, y)
            res.append({"sensor": sensor, "traza": traza, "hora_local": hora, "n": len(g),
                        "nivel_min": round(g.nivel.min(), 2), "nivel_max": round(g.nivel.max(), 2),
                        "variable": var, "clase": clase,
                        "alto_menos_bajo_db": round(ya.median() - yb.median(), 2),
                        "rho_nivel": round(rho, 2), "p": round(p, 3)})
    paneles.append((sensor, traza, hora, g))

resumen = pd.DataFrame(res)
resumen.to_csv(os.path.join(AQUI, "cgsm_nivel_rio_resumen%s.csv" % SUF), index=False)
print(f"\n== CGSM: manglar menos bosque frente al nivel del río ({estacion_nombre}), alto − bajo (dB) y Spearman ==")
for (sensor, traza, hora, n), g in resumen.groupby(["sensor", "traza", "hora_local", "n"]):
    print(f"\n{sensor} {traza} ({hora} local), n = {n}, nivel {g.nivel_min.iloc[0]} a {g.nivel_max.iloc[0]} {unidad}")
    print(g.pivot_table(index="clase", columns="variable", values=["alto_menos_bajo_db", "rho_nivel", "p"]).to_string())

# 3. Figura.
if paneles:
    fig, axes = plt.subplots(len(paneles), 2, figsize=(11, 3.4 * len(paneles)), squeeze=False)
    for i, (sensor, traza, hora, g) in enumerate(paneles):
        for j, (var, titulo) in enumerate((("CO", "co-pol (HH or VV)"), ("COmX", "co-pol − cross-pol"))):
            ax = axes[i, j]
            ax.scatter(g.nivel, g[f"{var}_manglar"], color="#1a7f3c", label="Mangrove")
            ax.scatter(g.nivel, g[f"{var}_bosque"], color="#555555", marker="s", label="Forest (control)")
            ax.set_title(f"{sensor} track {traza} ({hora} local), {titulo}", fontsize=9)
            ax.set_xlabel(f"River level at {estacion_nombre.title()} at pass time ({unidad})", fontsize=8)
            ax.set_ylabel("dB"); ax.grid(alpha=0.3)
            if i == 0 and j == 0:
                ax.legend(fontsize=8)
    fig.suptitle("CGSM: mangrove and forest backscatter against Magdalena River level, by sensor and track", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.985])
    fig.savefig(os.path.join(AQUI, "fig_cgsm_nivel_rio%s.png" % SUF), dpi=160)
    print("\nfigura: fig_cgsm_nivel_rio.png")
