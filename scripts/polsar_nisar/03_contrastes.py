# -*- coding: utf-8 -*-
r"""Contrastes preregistrados del plan (RADAR/PLAN_polsar_nisar_cgsm.md, sección 4) sobre los valores NISAR dual-pol extraídos
en los puntos por 02 (polsar_puntos_<fecha>_P<path>.csv). Puntos fuera de la reserva de validación (los de la muestra ya lo están).
 P1 (primario): AUC de alfa (y de H) para bosque muerto con troncos (fracción < 20 e indicador = sí) frente a herbácea sin troncos
     (fracción < 20 e indicador = no); IC bootstrap 2.000; p de permutación por bloques (2.000) para AUC > 0,5.
 P2: Spearman de DpRVI con el punto medio de caja de fracción de copa (0, 10, 35, 60, 75, 90), IC bootstrap; RMSE OOF por bloques
     de una regresión lineal DpRVI -> fracción.
 P3: mapa bosque / no bosque por umbral NO supervisado (Otsu sobre DpRVI en los puntos) frente a manglar / no manglar v1.1
     (manglar = intacto + degradado; no manglar = humedal + otro); macro-F1 por bloque; comparación con el mismo contraste binario
     de la unión óptica (OOF de la cadena v1.1).
 P4: sensibilidad: píxel frente a media 3 x 3, y por órbita cuando haya dos fechas.
 Holm sobre P1, P2 y P3.
USO: polsar_env/Scripts/python 03_contrastes.py 20251204 [path]
SALIDA: contrastes_<fecha>_P<path>.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from skimage.filters import threshold_otsu
from sklearn.metrics import f1_score, roc_auc_score

FECHA = sys.argv[1]; PATH = int(sys.argv[2]) if len(sys.argv) > 2 else 11
AQUI = Path(__file__).resolve().parent; MU = Path("C:/LINA/UNAL 2626-1/AVANCE TESIS/MUESTRA_2025")
d = pd.read_csv(AQUI / ("polsar_puntos_%s_P%03d.csv" % (FECHA, PATH))); pl = pd.read_csv(MU / "pliegues_cv_ampliada3.csv"); d = d.merge(pl, on="id")
rng = np.random.default_rng(20261023); MED = {"0": 0, "1-20": 10, "20-50": 35, "50-70": 60, "70-80": 75, "80-100": 90}
d["frac_mid"] = d.fraccion_copa_20261022.map(MED); res = []


def ic_boot(y, s, B=2000):
    n = len(y); bs = [roc_auc_score(y[i], s[i]) for i in (rng.integers(0, n, n) for _ in range(B)) if len(np.unique(y[i])) == 2]; return np.percentile(bs, [2.5, 97.5])


def p_perm_bloques(y, s, bl, B=2000):
    """p de AUC > 0,5 barajando la etiqueta dentro de cada bloque."""
    obs = roc_auc_score(y, s); nulo = []
    for _ in range(B):
        yb = y.copy()
        for b in np.unique(bl):
            m = bl == b; yb[m] = rng.permutation(yb[m])
        if len(np.unique(yb)) == 2: nulo.append(roc_auc_score(yb, s))
    return float((np.array(nulo) >= obs).mean())


for suf, nom in (("", "píxel"), ("_3x3", "media 3x3")):
    # P1
    m = (d.fraccion_copa_20261022.isin(["0", "1-20"])) & d.troncos_muertos_20261022.isin(["si", "no"]) & np.isfinite(d["alfa" + suf])
    sub = d[m]; y = (sub.troncos_muertos_20261022 == "si").astype(int).to_numpy(); bl = sub.bloque12.to_numpy()
    for var in ("alfa", "H", "dprvi", "C11", "C22"):
        s = sub[var + suf].to_numpy(); a = roc_auc_score(y, s); lo, hi = ic_boot(y, s); p = p_perm_bloques(y, s, bl) if var in ("alfa", "H") else np.nan
        if a < 0.5: a2, lo2, hi2 = 1 - a, 1 - hi, 1 - lo
        else: a2, lo2, hi2 = a, lo, hi
        res.append(dict(prueba="P1", variante=nom, variable=var, n_muerto=int(y.sum()), n_herbaceo=int((y == 0).sum()), estadistico="AUC muerto frente a herbáceo (orientado)", valor=round(a2, 3), lo=round(lo2, 3), hi=round(hi2, 3), p=p, direccion="muerto > herbáceo" if a >= 0.5 else "muerto < herbáceo"))
    # P2
    m2 = d.frac_mid.notna() & np.isfinite(d["dprvi" + suf]); s2 = d[m2]; rho, p2 = spearmanr(s2["dprvi" + suf], s2.frac_mid)
    n = len(s2); bs = [spearmanr(s2["dprvi" + suf].values[i], s2.frac_mid.values[i])[0] for i in (rng.integers(0, n, n) for _ in range(2000))]
    err = []
    for k in np.unique(s2.pliegue):
        te = (s2.pliegue == k).to_numpy(); tr = ~te; A = np.c_[np.ones(tr.sum()), s2["dprvi" + suf].values[tr]]; beta = np.linalg.lstsq(A, s2.frac_mid.values[tr], rcond=None)[0]
        pred = beta[0] + beta[1] * s2["dprvi" + suf].values[te]; err += list(pred - s2.frac_mid.values[te])
    err = np.array(err); mid = s2.frac_mid.between(20, 70).to_numpy()
    res.append(dict(prueba="P2", variante=nom, variable="dprvi", n_muerto=n, estadistico="Spearman DpRVI frente a fracción de copa", valor=round(rho, 3), lo=round(np.percentile(bs, 2.5), 3), hi=round(np.percentile(bs, 97.5), 3), p=p2, direccion="RMSE OOF %.1f puntos (%.1f dentro de 20-70, n %d)" % (np.sqrt(np.mean(err ** 2)), np.sqrt(np.mean(err[mid] ** 2)) if mid.any() else np.nan, int(mid.sum()))))
    # P3
    m3 = d.clase_final_v11.isin(["manglar_intacto", "manglar_degradado", "humedal_herbaceo", "otro"]) & np.isfinite(d["dprvi" + suf]); s3 = d[m3]
    y3 = s3.clase_final_v11.isin(["manglar_intacto", "manglar_degradado"]).astype(int).to_numpy(); t = threshold_otsu(s3["dprvi" + suf].to_numpy()); pred = (s3["dprvi" + suf].to_numpy() > t).astype(int)
    f = f1_score(y3, pred, average="macro"); fb = [f1_score(y3[s3.bloque12.values == b], pred[s3.bloque12.values == b], average="macro", zero_division=0) for b in np.unique(s3.bloque12) if (s3.bloque12.values == b).sum() >= 15]
    res.append(dict(prueba="P3", variante=nom, variable="dprvi > Otsu (%.3f)" % t, n_muerto=int(y3.sum()), n_herbaceo=int((y3 == 0).sum()), estadistico="macro-F1 manglar / no manglar", valor=round(f, 3), lo=round(np.percentile(fb, 25), 3) if fb else np.nan, hi=round(np.percentile(fb, 75), 3) if fb else np.nan, p=np.nan, direccion="cuartiles por bloque (n >= 15)"))
# referencia óptica para P3: mismo contraste binario con la OOF de la cadena v1.1 (820)
o = pd.read_csv("C:/LINA/UNAL 2626-1/PERCEPCION REMOTA AVANZADA/informe2_ampliada/pixel_2025_oof.csv")
mo = o.clase_final.isin(["manglar_intacto", "manglar_degradado", "humedal_herbaceo", "otro"]) & o.oof_s2_mas_alphaearth.isin(["manglar_intacto", "manglar_degradado", "humedal_herbaceo", "otro"])
yo = o[mo].clase_final.isin(["manglar_intacto", "manglar_degradado"]).astype(int); po = o[mo].oof_s2_mas_alphaearth.isin(["manglar_intacto", "manglar_degradado"]).astype(int)
res.append(dict(prueba="P3-ref", variante="óptica unión v1.1 (OOF cadena)", variable="RF 94 variables", n_muerto=int(yo.sum()), n_herbaceo=int((yo == 0).sum()), estadistico="macro-F1 manglar / no manglar", valor=round(f1_score(yo, po, average="macro"), 3), lo=np.nan, hi=np.nan, p=np.nan, direccion="referencia"))
R = pd.DataFrame(res)
# Holm sobre P1 (alfa, píxel), P2 (píxel) y P3 (sin p: se reporta tal cual)
ps = R[(R.variante == "píxel") & (((R.prueba == "P1") & (R.variable == "alfa")) | (R.prueba == "P2"))].p.values; orden = np.argsort(ps); holm = np.minimum(1, np.maximum.accumulate(ps[orden] * (len(ps) - np.arange(len(ps)))))
print("Holm (P1 alfa, P2):", dict(zip(np.array(["P1 alfa", "P2"])[orden], np.round(holm, 4))))
R.to_csv(AQUI / ("contrastes_%s_P%03d.csv" % (FECHA, PATH)), index=False); pd.set_option("display.width", 250); print(R.to_string(index=False))
