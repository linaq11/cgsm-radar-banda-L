# -*- coding: utf-8 -*-
r"""Comprueba si las correlaciones con la marea y con la lluvia estan infladas por dependencia temporal.

Spearman trata cada pasada como una observacion independiente. Si la serie de radar y la del
forzante (marea, lluvia de 30 dias) se parecen a si mismas de una pasada a la siguiente, las n
pasadas valen por menos. Para cada traza se mide la autocorrelacion de rezago 1 de las dos
series (sobre rangos, en orden de fecha) y se calcula el tamano efectivo de Pyper y Peterman
(1998): n_ef = n (1 - r1x r1y) / (1 + r1x r1y), acotado a n. El p se recalcula con n_ef.

La variable de radar es manglar menos bosque en copolarizacion, que es la que usa el informe.
No reentrena ni descarga nada: lee las tablas por fecha que ya estan en la carpeta.

USO: python autocorrelacion_temporal.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

AQUI = Path(__file__).resolve().parent
SERIES = [  # archivo, columna de traza, forzante, copolarizacion, etiqueta
    ("perfil_pacifico_24.csv", "traza", "marea_m", "HH", "NISAR Malaga, marea"),
    ("s1_marea_malaga.csv", "orbita", "marea_m", "VV", "Sentinel-1 Malaga, marea"),
    ("alos2_marea_malaga.csv", "path", "marea_m", "HH", "ALOS-2 Malaga, marea"),
    ("cgsm_temporada_nisar.csv", "traza", "p30", "CO", "NISAR CGSM, lluvia 30 d"),
    ("cgsm_temporada_s1.csv", "traza", "p30", "CO", "Sentinel-1 CGSM, lluvia 30 d"),
    ("cgsm_temporada_alos2.csv", "traza", "p30", "CO", "ALOS-2 CGSM, lluvia 30 d"),
]


def rk(v, k=1):
    r = stats.rankdata(v)
    return float(np.corrcoef(r[:-k], r[k:])[0, 1]) if len(v) > k + 3 else 0.0


def r1(v):
    return rk(v, 1)


def n_ef_rezagos(x, y):
    """Pyper y Peterman con todos los rezagos hasta n/5, para series con ciclo estacional."""
    n = len(x)
    s = sum((n - k) / n * rk(x, k) * rk(y, k) for k in range(1, max(2, n // 5) + 1))
    return min(n, n / max(1 + 2 * s, 1e-6)) if 1 + 2 * s > 0 else n


def fila_rio():
    """NISAR D083 en la CGSM contra el nivel del rio Magdalena en Remolino (IDEAM), con la misma
    interpolacion horaria de cgsm_nivel_rio.py. Las fechas del IDEAM son hora local (UTC-5)."""
    n = pd.read_csv(AQUI / "nivel_ideam_instantaneo.csv", dtype={"codigoestacion": str})
    n = n[n.codigoestacion == "2904700095"].copy()
    n["t"] = pd.to_datetime(n.fechaobservacion)
    n["nivel"] = pd.to_numeric(n.valorobservado, errors="coerce")
    serie = n.dropna(subset=["nivel"]).sort_values("t").set_index("t").nivel.resample("1h").mean().interpolate(limit=48)
    ep = pd.Timestamp("1970-01-01")
    seg = (serie.index - ep).total_seconds().values
    d = pd.read_csv(AQUI / "cgsm_temporada_nisar.csv")
    d = d[d.traza.astype(str) == "D"]
    d["nivel"] = [float(np.interp((pd.Timestamp(f).tz_localize(None) - pd.Timedelta(hours=5) - ep).total_seconds(),
                                  seg, serie.values)) for f in d.fecha_utc]
    t = d.pivot_table(index=["fecha_utc", "nivel"], columns="clase", values="CO").reset_index().sort_values("fecha_utc")
    man = [c for c in t.columns if "mangl" in str(c)][0]
    bos = [c for c in t.columns if "bosq" in str(c)][0]
    x, y = t.nivel.values, (t[man] - t[bos]).values
    rho, p = stats.spearmanr(x, y)
    ax, ay, n_ = r1(x), r1(y), len(x)
    nef = min(n_, n_ * (1 - ax * ay) / (1 + ax * ay))
    nef2 = n_ef_rezagos(x, y)
    pv = lambda k: 2 * stats.t.sf(abs(rho * np.sqrt(max(k - 2, 0.01) / max(1 - rho ** 2, 1e-9))), max(k - 2, 0.01))
    return dict(serie="NISAR CGSM, nivel del rio", traza="D", n=n_, paso_dias=12.0, rho=rho, p=p, r1_forzante=ax,
                r1_radar=ay, n_ef=nef, p_ef=pv(nef), n_ef_rezagos=nef2, p_ef_rezagos=pv(nef2))


def main():
    filas = [fila_rio()]
    for archivo, ctraza, forz, co, etq in SERIES:
        d = pd.read_csv(AQUI / archivo)
        man = [c for c in d.clase.unique() if "mangl" in str(c).lower()]
        bos = [c for c in d.clase.unique() if "bosq" in str(c).lower()]
        if not man or not bos:
            print("%s: clases %s, no se pudo armar manglar - bosque" % (archivo, d.clase.unique().tolist()))
            continue
        for tz, g in d.groupby(ctraza):
            t = g.pivot_table(index="escena", columns="clase", values=co, aggfunc="first")
            x = g.groupby("escena")[forz].first()
            f = pd.to_datetime(g.groupby("escena").fecha_utc.first(), utc=True)
            s = pd.DataFrame({"f": f, "x": x, "y": t[man[0]] - t[bos[0]]}).dropna().sort_values("f")
            n = len(s)
            if n < 8:
                continue
            rho, p = stats.spearmanr(s.x, s.y)
            ax, ay = r1(s.x.values), r1(s.y.values)
            nef = min(n, n * (1 - ax * ay) / (1 + ax * ay))
            tt = rho * np.sqrt(max(nef - 2, 0.01) / max(1 - rho ** 2, 1e-9))
            pef = 2 * stats.t.sf(abs(tt), max(nef - 2, 0.01))
            paso = s.f.diff().dt.days.median()
            nef2 = n_ef_rezagos(s.x.values, s.y.values)
            t2 = rho * np.sqrt(max(nef2 - 2, 0.01) / max(1 - rho ** 2, 1e-9))
            filas.append(dict(serie=etq, traza=tz, n=n, paso_dias=paso, rho=rho, p=p, r1_forzante=ax, r1_radar=ay,
                              n_ef=nef, p_ef=pef, n_ef_rezagos=nef2,
                              p_ef_rezagos=2 * stats.t.sf(abs(t2), max(nef2 - 2, 0.01))))
    r = pd.DataFrame(filas)
    pd.set_option("display.width", 220)
    print(r.round({"rho": 2, "p": 4, "r1_forzante": 2, "r1_radar": 2, "n_ef": 1, "p_ef": 4, "n_ef_rezagos": 1,
                   "p_ef_rezagos": 4}).to_string(index=False))
    r.to_csv(AQUI / "autocorrelacion_temporal.csv", index=False)
    sig = r[r.p < 0.05]
    print("\ncorrelaciones con p < 0,05: %d | siguen con p_ef < 0,05: %d" % (len(sig), int((sig.p_ef < 0.05).sum())))


if __name__ == "__main__":
    main()
