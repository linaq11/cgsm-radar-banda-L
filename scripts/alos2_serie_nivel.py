# -*- coding: utf-8 -*-
"""Prueba hidrológica con la serie larga de ALOS-2 (2014 a 2026) en la CGSM: resta copolar manglar − bosque
frente al nivel del río Magdalena en Remolino, por trayectoria y en conjunto.

ENTRADAS
    alos2_serie_cgsm.csv (de alos2_serie_cgsm.py); nivel_ideam_instantaneo.csv y nivel_ideam_*_2014_2024.csv
    (IDEAM 2904700095; donde no hay instantáneo se usa la media del máximo y el mínimo diarios).
REGLA
    La misma del informe 1: si la banda L responde al agua bajo el dosel, la resta HH manglar − bosque sube con el
    nivel dentro de una misma trayectoria; estadístico primario = Spearman y pendiente en dB/m con IC bootstrap.
SALIDAS
    alos2_serie_nivel_resumen.csv, alos2_serie_nivel_pasadas.csv, fig_alos2_serie_nivel.png
USO
    python alos2_serie_nivel.py
"""
import os
GAMMA0 = os.environ.get("RADAR_MAGNITUD", "sigma0").lower() == "gamma0"
SUF = "_gamma0" if GAMMA0 else ""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, theilslopes

AQUI = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261016); B = 5000
f = lambda p: os.path.join(AQUI, p)


def horario_2025():
    """Nivel instantáneo horario de Remolino (m), 2025 en adelante, el mismo del informe 1."""
    d = pd.read_csv(f("nivel_ideam_instantaneo.csv"), dtype={"codigoestacion": str}, low_memory=False); d = d[d.codigoestacion == "2904700095"]
    d["t"] = pd.to_datetime(d.fechaobservacion, errors="coerce"); d["nivel"] = pd.to_numeric(d.valorobservado, errors="coerce")
    return d.dropna(subset=["t", "nivel"]).set_index("t").nivel.resample("1h").mean().interpolate(limit=48)


def diario(cod):
    """Nivel medio diario histórico del IDEAM (cm → m), repositorio datos.ideam.gov.co, archivo <cod>-NV_MEDIA_D.csv."""
    d = pd.read_csv(f("nivel_ideam_hist_%s_NV_MEDIA_D.csv" % cod)); d["t"] = pd.to_datetime(d.fechaObservacion)
    return (pd.to_numeric(d.valorObservado, errors="coerce") / 100).set_axis(d.t).dropna().resample("1D").mean()


# Serie compuesta de Remolino: horario 2025-2026; medio diario de Remolino 2018-2024 donde existe; y en los huecos
# (2014 a abril de 2018, 2021-2022, parte de 2020 y 2023) el nivel estimado desde San Pedrito (29047070, Suan,
# 63 km aguas arriba, serie completa 2014-2026) por regresión lineal ajustada en los días comunes.
hor = horario_2025()
rem = diario("2904700095"); sp = diario("0029047070")
m = pd.concat([rem.rename("rem"), sp.rename("sp")], axis=1).dropna()
b1, b0 = np.polyfit(m.sp, m.rem, 1); r2 = np.corrcoef(m.sp, m.rem)[0, 1] ** 2
print("Remolino ~ %.3f + %.3f · San Pedrito, R² %.3f, n %d días, residuo p5-p95 %.2f a %.2f m" % (b0, b1, r2, len(m), *np.percentile(m.rem - (b0 + b1 * m.sp), [5, 95])))
est = (b0 + b1 * sp).rename("est")
dia = rem.combine_first(est)                                   # Remolino medido manda; San Pedrito rellena
fuente_dia = pd.Series(np.where(rem.reindex(dia.index).notna(), "Remolino diario", "San Pedrito regresión"), index=dia.index)
serie = hor.combine_first(dia.resample("1h").interpolate(limit=48)).interpolate(limit=48)
print("nivel compuesto: %s a %s; horario %d h, diario Remolino %d d, estimado %d d" % (serie.index.min().date(), serie.index.max().date(), hor.notna().sum(), rem.notna().sum(), (fuente_dia == "San Pedrito regresión").sum()))


def fuente_en(t_utc):
    t = pd.Timestamp(t_utc) - pd.Timedelta(hours=5)
    if t >= hor.index.min(): return "Remolino horario"
    d0 = t.floor("D")
    return fuente_dia.get(d0, "sin dato")


seg = (serie.index - pd.Timestamp("1970-01-01")).total_seconds().values


def nivel_en(t_utc):
    t = pd.Timestamp(t_utc) - pd.Timedelta(hours=5)
    if t < serie.index.min() or t > serie.index.max(): return np.nan
    v = float(np.interp((t - pd.Timestamp("1970-01-01")).total_seconds(), seg, serie.values))
    return v if np.isfinite(v) else np.nan


d = pd.read_csv(f("alos2_serie_cgsm%s.csv" % SUF), parse_dates=["fecha_utc"])
p = d.pivot_table(index=["escena", "fecha_utc", "traza", "hora_local"], columns="clase", values=["CO", "X", "COmX"]).reset_index()
p.columns = ["_".join(c).strip("_") if c[1] else c[0] for c in p.columns]
p["nivel"] = p.fecha_utc.apply(nivel_en); p["fuente_nivel"] = p.fecha_utc.apply(fuente_en)
p["resta_HH"] = p.CO_manglar - p.CO_bosque; p["resta_HV"] = p.X_manglar - p.X_bosque; p["resta_HHmHV"] = p.COmX_manglar - p.COmX_bosque
p["anio"] = p.fecha_utc.dt.year
# Lluvia diaria ERA5-Land sobre el AOI (mm), acumulada 30 días antes de cada pasada, como covariable estacional
cache = f("era5_p_diaria_aoi.csv")
if not os.path.exists(cache):
    import ee
    ee.Initialize(project="basic-buttress-338101")
    AOI = ee.FeatureCollection("projects/basic-buttress-338101/assets/AOI_tesis_CGSM_v1").geometry()
    era = ee.ImageCollection("ECMWF/ERA5_LAND/DAILY_AGGR").filterDate("2014-06-01", "2026-12-31").select("total_precipitation_sum")
    ll = era.map(lambda im: ee.Feature(None, {"t": im.get("system:time_start"), "p": im.reduceRegion(ee.Reducer.mean(), AOI, 11132, maxPixels=1e9).get("total_precipitation_sum")}))
    ll = pd.DataFrame([x["properties"] for x in ll.getInfo()["features"]])
    ll["fecha"] = pd.to_datetime(ll.t, unit="ms").dt.floor("D"); ll["mm"] = ll.p * 1000
    ll[["fecha", "mm"]].to_csv(cache, index=False)
lluvia = pd.read_csv(cache, parse_dates=["fecha"]).set_index("fecha").mm.sort_index()


def p30(t_utc):
    t = (pd.Timestamp(t_utc) - pd.Timedelta(hours=5)).floor("D")
    v = lluvia[(lluvia.index >= t - pd.Timedelta(days=30)) & (lluvia.index < t)]
    return float(v.sum()) if len(v) >= 25 else np.nan


p["p30_mm"] = p.fecha_utc.apply(p30)
p.to_csv(f("alos2_serie_nivel_pasadas%s.csv" % SUF), index=False)
print("pasadas: %d, con nivel: %d" % (len(p), p.nivel.notna().sum())); print(p.fuente_nivel.value_counts().to_string())
print(pd.crosstab(p.anio, p.traza).to_string())
q = p.dropna(subset=["nivel"])


def pendiente(x, y):
    b = np.polyfit(x, y, 1)[0]; bs = []
    for _ in range(B):
        i = rng.integers(0, len(x), len(x))
        if np.ptp(x[i]) > 0: bs.append(np.polyfit(x[i], y[i], 1)[0])
    lo, hi = np.percentile(bs, [2.5, 97.5]); ts = theilslopes(y, x, 0.95)
    return b, lo, hi, ts[0], ts[2], ts[3]


res = []
grupos = [(tr, g) for tr, g in q.groupby("traza") if len(g) >= 6] + [("todas (con efecto de traza)", q)]
for tr, g in grupos:
    for var in ("resta_HH", "resta_HV", "resta_HHmHV", "CO_manglar", "CO_bosque"):
        x = g.nivel.to_numpy(float); y = g[var].to_numpy(float)
        if tr.startswith("todas"):
            # efecto fijo de traza: se resta la mediana de cada traza antes de la regresión conjunta
            y = (g[var] - g.groupby("traza")[var].transform("median")).to_numpy(float)
        rho, pv = spearmanr(x, y); b, lo, hi, tsb, tslo, tshi = pendiente(x, y)
        r30 = g.p30_mm.to_numpy(float); ok = np.isfinite(r30)
        if ok.sum() >= 6:
            rk = lambda v: pd.Series(v).rank().to_numpy(float)
            ry, rx, rz = rk(y[ok]), rk(x[ok]), rk(r30[ok])
            ey = ry - np.polyval(np.polyfit(rz, ry, 1), rz); ex = rx - np.polyval(np.polyfit(rz, rx, 1), rz)
            rho_par = float(np.corrcoef(ex, ey)[0, 1]); rho_p30 = spearmanr(r30[ok], y[ok])[0]; rho_niv_p30 = spearmanr(r30[ok], x[ok])[0]
        else:
            rho_par = rho_p30 = rho_niv_p30 = np.nan
        gs = g.assign(y=y).sort_values("nivel"); k = max(len(gs) // 3, 2)
        res.append(dict(traza=tr, variable=var, n=len(g), nivel_min=round(x.min(), 2), nivel_max=round(x.max(), 2), anios="%d-%d" % (g.anio.min(), g.anio.max()),
                        alto_menos_bajo_db=round(gs.tail(k).y.median() - gs.head(k).y.median(), 2), rho=round(rho, 2), p=round(pv, 4),
                        rho_parcial_p30=round(rho_par, 2), rho_con_p30=round(rho_p30, 2), rho_nivel_p30=round(rho_niv_p30, 2), pendiente_db_m=round(b, 3), ic95_inf=round(lo, 3), ic95_sup=round(hi, 3), theil_sen=round(tsb, 3), ts_inf=round(tslo, 3), ts_sup=round(tshi, 3)))
r = pd.DataFrame(res); r.to_csv(f("alos2_serie_nivel_resumen%s.csv" % SUF), index=False)
print("\n== ALOS-2 2014-2026, CGSM: resta manglar − bosque frente al nivel en Remolino ==")
print(r.to_string(index=False))

# figura: resta HH frente al nivel por traza, y serie temporal de la resta con el nivel
trazas = [tr for tr, g in q.groupby("traza") if len(g) >= 6]
fig, axs = plt.subplots(2, max(len(trazas), 1), figsize=(5.2 * max(len(trazas), 1), 8), squeeze=False)
for j, tr in enumerate(trazas):
    g = q[q.traza == tr]; ax = axs[0, j]
    ax.scatter(g.nivel, g.resta_HH, c=g.anio, cmap="viridis", s=28);
    for _, rr in g.iterrows(): pass
    b = np.polyfit(g.nivel, g.resta_HH, 1); xx = np.linspace(g.nivel.min(), g.nivel.max(), 10); ax.plot(xx, np.polyval(b, xx), "k--", lw=1)
    rr = r[(r.traza == tr) & (r.variable == "resta_HH")].iloc[0]
    ax.set_title("ALOS-2 track %s, n = %d, %s\nrho %.2f, slope %.2f dB/m [%.2f, %.2f]" % (tr, len(g), rr.anios, rr.rho, rr.pendiente_db_m, rr.ic95_inf, rr.ic95_sup), fontsize=9)
    ax.set_xlabel("Magdalena level at Remolino at pass time (m)", fontsize=8); ax.set_ylabel("HH mangrove − forest (dB)", fontsize=8); ax.grid(alpha=0.3)
    ax2 = axs[1, j]; ax2.plot(g.fecha_utc, g.resta_HH, "o-", color="#1a7f3c", ms=4, lw=0.8, label="HH mangrove − forest")
    ax2.set_ylabel("dB", fontsize=8); ax2.grid(alpha=0.3); ax2.tick_params(labelsize=7)
    ax3 = ax2.twinx(); s = serie[(serie.index >= g.fecha_utc.min() - pd.Timedelta(days=30)) & (serie.index <= g.fecha_utc.max() + pd.Timedelta(days=30))]
    ax3.plot(s.index, s.values, color="#888888", lw=0.6, alpha=0.8); ax3.set_ylabel("river level (m)", fontsize=8, color="#888888"); ax3.tick_params(labelsize=7)
    ax2.set_title("time series, track %s" % tr, fontsize=9)
fig.suptitle("ALOS-2 PALSAR-2 ScanSAR over the CGSM, 2014 to 2026: mangrove minus dry-forest HH against Magdalena River level", fontsize=10.5)
fig.tight_layout(rect=[0, 0, 1, 0.97]); fig.savefig(f("fig_alos2_serie_nivel%s.png" % SUF), dpi=160)
print("figura: fig_alos2_serie_nivel%s.png" % SUF)
