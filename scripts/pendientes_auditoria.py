# -*- coding: utf-8 -*-
"""Cuatro análisis pendientes de la auditoría del informe 1 (revisión externa del 2026-10-14).

PROPÓSITO
    A. Estadístico primario por sitio (resta copolar manglar − bosque frente al forzante), corrección de
       Holm sobre la familia de pruebas de banda L y pendientes en dB por metro con intervalo bootstrap.
    B. Borde frente a interior del manglar: cambio copolar entre periodos de nivel alto y bajo según la
       distancia del píxel de 50 m al borde del manglar (CGSM, NISAR D083) y a la marea (Málaga, A004 y D087).
    C. Separabilidad de Jeffries-Matusita con dos variables por banda (copolar y cruzada), sin la diferencia
       copolar − cruzada, que es combinación lineal de las otras dos y deja la covarianza singular.
    D. Clave de lectura con banda C sola frente a C + L: la decisión dosel cerrado / abierto con VV − VH en
       vez de HH − HV, con el umbral elegido por resustitución igual que el 7,3 dB de la clave.
ENTRADAS
    perfil_pacifico_24.csv, alos2_marea_malaga.csv, s1_marea_malaga.csv, cgsm_temporada_nisar.csv,
    cgsm_temporada_s1.csv, nivel_ideam_instantaneo.csv, autocorrelacion_temporal.csv,
    mapa_doble_rebote_50m.tif, mapa_malaga_A004_50m.tif, mapa_malaga_D087_50m.tif, clave_muestra2025_puntos.csv.
SALIDAS
    pendientes_auditoria_pendientes.csv, pendientes_auditoria_borde.csv, pendientes_auditoria_jm2.csv,
    pendientes_auditoria_clave_c.csv, fig_borde_interior.png y resumen en pantalla.
USO
    python pendientes_auditoria.py
"""
import importlib.util
import os
os.environ["PROJ_DATA"] = os.path.join(importlib.util.find_spec("rasterio").submodule_search_locations[0], "proj_data")
os.environ["PROJ_LIB"] = os.environ["PROJ_DATA"]
from itertools import combinations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from scipy.ndimage import distance_transform_edt
from scipy.stats import spearmanr, theilslopes

AQUI = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20261016)
B = 5000                                     # réplicas bootstrap


def f(p): return os.path.join(AQUI, p)


# ============================================================ A. estadístico primario, Holm y pendientes
def serie_nivel(estacion="2904700095"):
    n = pd.read_csv(f("nivel_ideam_instantaneo.csv"), dtype={"codigoestacion": str})
    n = n[n.codigoestacion == estacion].copy()
    n["t"] = pd.to_datetime(n.fechaobservacion); n["nivel"] = pd.to_numeric(n.valorobservado, errors="coerce")
    n = n.dropna(subset=["nivel"]).sort_values("t")
    s = n.set_index("t").nivel.resample("1h").mean().interpolate(limit=48)
    seg = (s.index - pd.Timestamp("1970-01-01")).total_seconds().values
    def en(fecha_utc):
        t = pd.Timestamp(fecha_utc) - pd.Timedelta(hours=5)
        if t < s.index.min() or t > s.index.max(): return np.nan
        return float(np.interp((t - pd.Timestamp("1970-01-01")).total_seconds(), seg, s.values))
    return en


def resta(df, grupo, forz, co):
    """Por pasada: forzante y copolar manglar − bosque, para cada valor de la columna grupo."""
    out = {}
    for g, d in df.groupby(grupo):
        p = d.pivot_table(index=["escena", forz], columns="clase", values=co).reset_index()
        if "manglar" not in p or "bosque" not in p: continue
        p = p.dropna(subset=["manglar", "bosque"])
        out[g] = (p[forz].to_numpy(float), (p.manglar - p.bosque).to_numpy(float))
    return out


def pendiente(x, y):
    """Pendiente OLS en dB por metro con IC bootstrap del 95 % y Theil–Sen con su IC."""
    n = len(x); b = np.polyfit(x, y, 1)[0]
    bs = []
    for _ in range(B):
        i = rng.integers(0, n, n)
        if np.ptp(x[i]) == 0: continue
        bs.append(np.polyfit(x[i], y[i], 1)[0])
    lo, hi = np.percentile(bs, [2.5, 97.5])
    ts = theilslopes(y, x, 0.95)
    return b, lo, hi, ts[0], ts[2], ts[3]


def holm(p):
    """Valores p ajustados por Holm (step-down), mismo orden de entrada."""
    p = np.asarray(p, float); m = len(p); o = np.argsort(p); adj = np.empty(m)
    run = 0.0
    for k, i in enumerate(o):
        run = max(run, (m - k) * p[i]); adj[i] = min(1.0, run)
    return adj


def parte_a():
    series = []
    nis = pd.read_csv(f("perfil_pacifico_24.csv"))
    for tr, (x, y) in resta(nis, "traza", "marea_m", "HH").items():
        series.append(("NISAR, Málaga, marea", "L", tr, "HH", x, y))
    alos = pd.read_csv(f("alos2_marea_malaga.csv"))
    for tr, (x, y) in resta(alos, "path", "marea_m", "HH").items():
        series.append(("ALOS-2, Málaga, marea", "L", str(tr), "HH", x, y))
    s1m = pd.read_csv(f("s1_marea_malaga.csv"))
    for tr, (x, y) in resta(s1m, "orbita", "marea_m", "VV").items():
        series.append(("Sentinel-1, Málaga, marea", "C", str(tr), "VV", x, y))
    en = serie_nivel()
    cg = pd.read_csv(f("cgsm_temporada_nisar.csv")); cg["nivel"] = cg.fecha_utc.apply(en); cg = cg.dropna(subset=["nivel"])
    for tr, (x, y) in resta(cg, "traza", "nivel", "CO").items():
        if len(x) >= 6: series.append(("NISAR, CGSM, nivel del río", "L", "D083" if tr == "D" else "A007", "HH", x, y))
    s1c = pd.read_csv(f("cgsm_temporada_s1.csv")); s1c["nivel"] = s1c.fecha_utc.apply(en); s1c = s1c.dropna(subset=["nivel"])
    for tr, (x, y) in resta(s1c, "traza", "nivel", "CO").items():
        series.append(("Sentinel-1, CGSM, nivel del río", "C", tr, "VV", x, y))

    # p corregido por dependencia temporal (Tabla 7), tomado de autocorrelacion_temporal.csv
    ac = pd.read_csv(f("autocorrelacion_temporal.csv"))
    def p_ef(nombre, tr):
        clave = {"NISAR, Málaga, marea": "NISAR Malaga, marea", "ALOS-2, Málaga, marea": "ALOS-2 Malaga, marea",
                 "Sentinel-1, Málaga, marea": "S1 Malaga, marea", "NISAR, CGSM, nivel del río": "NISAR CGSM, nivel del rio",
                 "Sentinel-1, CGSM, nivel del río": "S1 CGSM, nivel del rio"}.get(nombre)
        r = ac[(ac.serie.str.replace("á", "a") == clave) & (ac.traza.astype(str) == ("D" if tr == "D083" else tr))]
        return float(r.p_ef_rezagos.iloc[0]) if len(r) else np.nan

    filas = []
    for nombre, banda, tr, var, x, y in series:
        rho, p = spearmanr(x, y); b, lo, hi, tsb, tslo, tshi = pendiente(x, y)
        filas.append(dict(serie=nombre, banda=banda, traza=tr, variable=var + " manglar − bosque", n=len(x),
                          rango_forzante_m=round(float(np.ptp(x)), 2), rho=round(rho, 2), p=round(p, 4), p_temporal=p_ef(nombre, tr),
                          pendiente_db_m=round(b, 2), ic95_inf=round(lo, 2), ic95_sup=round(hi, 2),
                          theil_sen_db_m=round(tsb, 2), ts_ic_inf=round(tslo, 2), ts_ic_sup=round(tshi, 2),
                          cambio_en_el_rango_db=round(b * float(np.ptp(x)), 2)))
    t = pd.DataFrame(filas)
    # Familia primaria: las pruebas de banda L (4 de Málaga + CGSM D083); Holm sobre el p corregido por dependencia temporal
    prim = t.banda.eq("L") & t.traza.isin(["A004", "D087", "139", "140", "D083"])
    t["familia"] = np.where(prim, "primaria (L)", "exploratoria")
    t["p_holm_L5"] = np.nan; t.loc[prim, "p_holm_L5"] = holm(t.loc[prim, "p_temporal"].fillna(t.loc[prim, "p"]))
    m4 = prim & t.traza.ne("D083")
    t["p_holm_L4_malaga"] = np.nan; t.loc[m4, "p_holm_L4_malaga"] = holm(t.loc[m4, "p_temporal"])
    t["p_holm_todas"] = holm(t.p_temporal.fillna(t.p))
    t = t.round({"p_temporal": 4, "p_holm_L5": 4, "p_holm_L4_malaga": 4, "p_holm_todas": 4})
    t.to_csv(f("pendientes_auditoria_pendientes.csv"), index=False)
    print("\n== A. Estadístico primario, Holm y pendientes (resta copolar manglar − bosque) ==")
    print(t.drop(columns=["variable"]).to_string(index=False))
    return t


# ============================================================ B. borde frente a interior
BANDAS_DIST = [(50, 50, "0 a 50 m (borde)"), (100, 100, "50 a 100 m"), (150, 200, "100 a 200 m"), (250, 300, "200 a 300 m"), (350, 1e9, "más de 300 m")]


def borde_sitio(tif, etiqueta, sectores=None):
    with rasterio.open(f(tif)) as src:
        dhh = src.read(1); cl = src.read(4).astype(int); x0, y0 = src.transform.c, src.transform.f; res = src.res[0]
    ny, nx = dhh.shape
    N = y0 - (np.arange(ny) + 0.5) * res; N = np.repeat(N[:, None], nx, axis=1)
    man = cl == 1
    d_borde = distance_transform_edt(man) * res            # distancia de cada píxel de manglar al píxel no manglar más cercano
    d_agua = distance_transform_edt(cl != 4) * res         # distancia al agua abierta
    filas = []
    grupos = [("todo", man)] + ([(s, man & (N >= a) & (N < b)) for s, a, b in sectores] if sectores else [])
    for gn, gm in grupos:
        for dist, col in (("al borde del manglar", d_borde), ("al agua abierta", d_agua)):
            for lo_, hi_, nombre in BANDAS_DIST:
                lo = lo_ - 50 if dist == "al borde del manglar" else lo_ - 50
                m = gm & np.isfinite(dhh) & (col > lo) & (col <= hi_)
                if dist == "al agua abierta":                                   # manglar a esa distancia del agua
                    m = gm & np.isfinite(dhh) & (col > lo) & (col <= hi_) & (col > 0)
                v = dhh[m]
                if len(v) < 30: continue
                filas.append(dict(sitio=etiqueta, grupo=gn, distancia=dist, banda=nombre, n_pix_50m=int(len(v)),
                                  mediana=round(float(np.median(v)), 2), q25=round(float(np.percentile(v, 25)), 2),
                                  q75=round(float(np.percentile(v, 75)), 2), frac_positiva=round(float((v > 0).mean()), 3)))
        # correlación continua distancia al borde frente a cambio, manglar del grupo
        m = gm & np.isfinite(dhh)
        rho, p = spearmanr(d_borde[m], dhh[m])
        filas.append(dict(sitio=etiqueta, grupo=gn, distancia="al borde del manglar", banda="Spearman distancia vs ΔHH", n_pix_50m=int(m.sum()),
                          mediana=round(rho, 3), q25=np.nan, q75=np.nan, frac_positiva=float("%.2g" % p)))
    return pd.DataFrame(filas)


def parte_b():
    sect = [("norte (Salamanca, N > 1205 km)", 1205000, 1e12), ("centro y occidente (1190 a 1205 km)", 1190000, 1205000), ("sur (río Fundación, N < 1190 km)", -1e12, 1190000)]
    t = pd.concat([borde_sitio("mapa_doble_rebote_50m.tif", "CGSM, NISAR D083, nivel del río", sect),
                   borde_sitio("mapa_malaga_A004_50m.tif", "Málaga, NISAR A004, marea"),
                   borde_sitio("mapa_malaga_D087_50m.tif", "Málaga, NISAR D087, marea")], ignore_index=True)
    t.to_csv(f("pendientes_auditoria_borde.csv"), index=False)
    print("\n== B. Borde frente a interior del manglar (ΔHH alto − bajo, dB, malla de 50 m) ==")
    print(t[t.banda != "Spearman distancia vs ΔHH"].to_string(index=False))
    print(t[t.banda == "Spearman distancia vs ΔHH"][["sitio", "grupo", "n_pix_50m", "mediana", "frac_positiva"]].rename(columns={"mediana": "rho", "frac_positiva": "p"}).to_string(index=False))
    # figura: mediana e IQR por banda de distancia al borde, tres paneles
    fig, axs = plt.subplots(1, 3, figsize=(14, 4.2), constrained_layout=True)
    for ax, sitio in zip(axs, t.sitio.unique()):
        d = t[(t.sitio == sitio) & (t.distancia == "al borde del manglar") & (t.banda != "Spearman distancia vs ΔHH")]
        grupos = d.grupo.unique()
        for k, g in enumerate(grupos):
            dd = d[d.grupo == g]; xx = np.arange(len(dd)) + 0.8 * (k - (len(grupos) - 1) / 2) / max(len(grupos), 1) * 0.9
            ax.errorbar(xx, dd.mediana, yerr=[dd.mediana - dd.q25, dd.q75 - dd.mediana], fmt="o", capsize=3, label=g if g != "todo" else "all mangrove")
            ax.set_xticks(np.arange(len(dd))); ax.set_xticklabels([b.replace(" (borde)", "").replace("más de", ">").replace(" a ", "–").replace(" m", "") + " m" for b in dd.banda], fontsize=8)
        ax.axhline(0, color="k", lw=0.6); ax.set_title(sitio.replace("Málaga", "Malaga").replace("nivel del río", "river level").replace("marea", "tide"), fontsize=9)
        ax.set_xlabel("distance to mangrove edge (50 m cells)", fontsize=8); ax.set_ylabel("ΔHH high − low (dB), median and IQR", fontsize=8)
        ax.grid(alpha=0.3); ax.legend(fontsize=7)
    fig.savefig(f("fig_borde_interior.png"), dpi=160)
    return t


# ============================================================ C. JM con dos variables
def jm(a, b):
    ma, mb = a.mean(0), b.mean(0)
    ca, cb = np.cov(a, rowvar=False), np.cov(b, rowvar=False)
    c = (ca + cb) / 2; dm = ma - mb
    Bd = dm @ np.linalg.solve(c, dm) / 8 + 0.5 * np.log(np.linalg.det(c) / np.sqrt(np.linalg.det(ca) * np.linalg.det(cb)))
    return float(2 * (1 - np.exp(-Bd)))


CLASES = ["agua", "vegetacion_flotante", "humedal_herbaceo", "manglar_degradado", "manglar_intacto", "otro"]


def parte_c():
    t = pd.read_csv(f("clave_muestra2025_puntos.csv")); t = t[t.clase_final.isin(CLASES)]
    viejo = pd.read_csv(f("clave_muestra2025_jm.csv")).set_index("par")
    conj = {"C (VV, VH)": ["VV", "VH"], "L (HH, HV)": ["HH", "HV"], "C + L (VV, VH, HH, HV)": ["VV", "VH", "HH", "HV"]}
    filas = []
    for c1, c2 in combinations(CLASES, 2):
        par = "%s | %s" % (c1, c2); fl = dict(par=par)
        for nombre, cols in conj.items():
            a = t[t.clase_final == c1][cols].dropna().to_numpy(); b = t[t.clase_final == c2][cols].dropna().to_numpy()
            fl["jm " + nombre] = round(jm(a, b), 2)
        fl["jm C 3 var (informe)"] = viejo.loc[par, "jm C (VV, VH, VV-VH)"]; fl["jm L 3 var (informe)"] = viejo.loc[par, "jm L (HH, HV, HH-HV)"]; fl["jm C+L 6 var (informe)"] = viejo.loc[par, "jm C + L"]
        filas.append(fl)
    r = pd.DataFrame(filas); r.to_csv(f("pendientes_auditoria_jm2.csv"), index=False)
    print("\n== C. Jeffries-Matusita con dos variables por banda frente a las tres del informe ==")
    print(r.to_string(index=False))
    return r


# ============================================================ D. clave con C sola frente a C + L
OK = {"agua": "1 agua abierta", "vegetacion_flotante": "2 vegetacion flotante", "manglar_intacto": "3 dosel cerrado",
      "manglar_degradado": "4 dosel abierto", "humedal_herbaceo": "4 dosel abierto", "otro": "4 dosel abierto"}


def regla_c(r, umbral, var):
    if np.isnan(r.VV): return "sin decision"
    if r.VV < -17 and r.VH < -25: return "1 agua abierta"
    if r.VV < -12: return "2 vegetacion flotante" if r.VVmVH >= 6.5 else "sin decision"
    v = getattr(r, var)
    if np.isnan(v): return "sin decision"
    return "3 dosel cerrado" if v < umbral else "4 dosel abierto"


def evaluar(t, col):
    dec = t[t[col] != "sin decision"]
    ac = sum(int(((dec.clase_final == c) & (dec[col] == v)).sum()) for c, v in OK.items())
    por = {c: int(((t.clase_final == c) & (t[col] == v)).sum()) for c, v in OK.items()}
    return len(dec), ac, por


def parte_d():
    t = pd.read_csv(f("clave_muestra2025_puntos.csv")); t = t[t.clase_final.isin(CLASES)].copy()
    # umbral de VV − VH por resustitución: el que maximiza el acierto balanceado intacto frente a las tres clases de dosel abierto
    sub = t[(t.VV >= -12)].dropna(subset=["VVmVH"])
    cerrado = sub.clase_final.eq("manglar_intacto").to_numpy(); abierto = sub.clase_final.isin(["manglar_degradado", "humedal_herbaceo", "otro"]).to_numpy()
    mejor = None
    for u in np.round(np.arange(3.0, 9.0, 0.1), 1):
        for sentido in (1, -1):                                   # 1: cerrado si VV−VH < u (como la L); −1: cerrado si VV−VH >= u
            pred_cerrado = (sub.VVmVH < u) if sentido == 1 else (sub.VVmVH >= u)
            ba = 0.5 * ((pred_cerrado & cerrado).sum() / cerrado.sum() + (~pred_cerrado & abierto).sum() / abierto.sum())
            if mejor is None or ba > mejor[0]: mejor = (ba, u, sentido)
    ba, u, sentido = mejor
    # la misma búsqueda para HH − HV, para comparar con el 7,3 fijado en el informe
    subl = sub.dropna(subset=["HHmHV"]); cl_ = subl.clase_final.eq("manglar_intacto").to_numpy(); ab_ = subl.clase_final.isin(["manglar_degradado", "humedal_herbaceo", "otro"]).to_numpy()
    ba_l = max((0.5 * (((subl.HHmHV < uu) & cl_).sum() / cl_.sum() + ((subl.HHmHV >= uu) & ab_).sum() / ab_.sum()), uu) for uu in np.round(np.arange(5.0, 10.0, 0.1), 1))
    t["clave C+L"] = t.apply(lambda r: regla_c(r, 7.3, "HHmHV"), axis=1)
    t["clave C sola"] = t.apply(lambda r: regla_c(r, u, "VVmVH") if sentido == 1 else ("3 dosel cerrado" if regla_c(r, u, "VVmVH") == "4 dosel abierto" else ("4 dosel abierto" if regla_c(r, u, "VVmVH") == "3 dosel cerrado" else regla_c(r, u, "VVmVH"))), axis=1)
    filas = []
    for col in ("clave C+L", "clave C sola"):
        nd, ac, por = evaluar(t, col)
        filas.append(dict(clave=col, decide=nd, acierta=ac, pct_decididos=round(100 * ac / nd, 1), pct_total=round(100 * ac / len(t), 1), **{"acierta " + c: v for c, v in por.items()}))
    r = pd.DataFrame(filas); r.to_csv(f("pendientes_auditoria_clave_c.csv"), index=False)
    print("\n== D. Clave con banda C sola frente a C + L (720 puntos, resustitución) ==")
    print("umbral C: VV − VH %s %.1f dB = dosel cerrado (acierto balanceado %.2f); el mismo criterio con HH − HV da %.1f dB (%.2f), el informe usa 7,3" % ("<" if sentido == 1 else ">=", u, ba, ba_l[1], ba_l[0]))
    print(r.to_string(index=False))
    cm = pd.crosstab(t.clase_final, t["clave C sola"]); print(cm.to_string())
    return r


if __name__ == "__main__":
    parte_a(); parte_b(); parte_c(); parte_d()
