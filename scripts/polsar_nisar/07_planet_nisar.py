# -*- coding: utf-8 -*-
r"""P9 del plan (preregistrado en PLAN_polsar_nisar_cgsm.md, 4d): ¿el DpRVI (y H, alfa) de NISAR del 16-dic-2025 sigue mejor
la cobertura de copa observada el mismo día a 3 m en PlanetScope que la fracción de copa interpretada en la muestra (otra fecha)?

Entradas
  AVANCE TESIS/PLANET/planet_puntos_20251216.csv      880 puntos: escena, clear, bandas a 3 m y medias 3 x 3 (ndvi_3x3)
  AVANCE TESIS/PLANET/descargas/CGSM_20251216/files/   escenas SR 8 bandas a 3 m (UTM 18N) para el proxy de copa
  polsar_puntos_20251216_P011.csv                      H, alfa, DpRVI, C11, C22 en píxel y 3 x 3; fracción de copa interpretada
Proxy de copa a 3 m: fracción de píxeles de 3 m con NDVI > 0,5 en la ventana 3 x 3 (9 m) centrada en el punto, en la misma
escena que usó la extracción; sensibilidad con umbrales 0,4 y 0,6.
Estadísticos: Spearman con IC bootstrap (2.000, semilla 20261028) de DpRVI, H y alfa frente a (a) NDVI 3 x 3 de Planet,
(b) proxy de copa, (c) fracción de copa interpretada; y diferencia pareada rho(Planet) − rho(interpretada) sobre los mismos
puntos, con IC bootstrap. Solo puntos con clear = 1.
SALIDAS: planet_nisar_20251216.csv (por punto), planet_nisar_resultados.csv, planet_nisar_resumen.json
USO: python -X utf8 07_planet_nisar.py
"""
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from pyproj import Transformer
from scipy.stats import spearmanr

AQUI = Path(__file__).resolve().parent; PL = Path("C:/LINA/UNAL 2626-1/AVANCE TESIS/PLANET")
ESC = PL / "descargas" / "CGSM_20251216" / "files"
rng = np.random.default_rng(20261028); B = 2000
MED = {"0": 0, "1-20": 10, "20-50": 35, "50-70": 60, "70-80": 75, "80-100": 90}
UMBRALES = (0.5, 0.4, 0.6)


def rho_ic(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
    r = spearmanr(x, y)[0]
    bs = np.array([spearmanr(x[i], y[i])[0] for i in (rng.integers(0, n, n) for _ in range(B))])
    return float(r), float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5)), n


def dif_ic(v, a, b):
    """Diferencia pareada rho(v,a) − rho(v,b) sobre los mismos puntos."""
    v = np.asarray(v, float); a = np.asarray(a, float); b = np.asarray(b, float); n = len(v)
    d = spearmanr(v, a)[0] - spearmanr(v, b)[0]
    bs = np.array([spearmanr(v[i], a[i])[0] - spearmanr(v[i], b[i])[0] for i in (rng.integers(0, n, n) for _ in range(B))])
    return float(d), float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5)), n


def main():
    p = pd.read_csv(PL / "planet_puntos_20251216.csv"); q = pd.read_csv(AQUI / "polsar_puntos_20251216_P011.csv")
    d = p.merge(q[["id", "H", "H_3x3", "alfa", "alfa_3x3", "dprvi", "dprvi_3x3", "C11", "C22"]], on="id", validate="1:1")
    d["frac_mid"] = d.fraccion_copa_20261022.map(MED)
    # proxy de copa a 3 m
    tr = Transformer.from_crs("EPSG:4326", "EPSG:32618", always_xy=True); x, y = tr.transform(d.lon.to_numpy(), d.lat.to_numpy())
    for u in UMBRALES:
        d["copa_%02d" % int(u * 10)] = np.nan
    for esc, g in d.groupby("escena"):
        f = ESC / ("%s_3B_AnalyticMS_SR_8b_clip.tif" % esc)
        if not f.exists():
            print("sin escena", esc, len(g)); continue
        with rasterio.open(f) as r:
            for i in g.index:
                fil, col = r.index(x[i], y[i])
                w = r.read([6, 8], window=((max(fil - 1, 0), fil + 2), (max(col - 1, 0), col + 2))).astype("float32")
                red, nir = w[0], w[1]; ok = (red > 0) & (nir > 0)
                if ok.sum() < 5:
                    continue
                ndvi = (nir - red) / (nir + red + 1e-6)
                for u in UMBRALES:
                    d.loc[i, "copa_%02d" % int(u * 10)] = float((ndvi[ok] > u).mean())
    d.to_csv(AQUI / "planet_nisar_20251216.csv", index=False)
    c = d[(d.clear == 1) & np.isfinite(d.ndvi_3x3) & np.isfinite(d.dprvi)].copy()
    print("puntos despejados con radar:", len(c), "| con fracción interpretada:", int(c.frac_mid.notna().sum()), flush=True)

    res = []
    for var in ("dprvi", "H", "alfa", "dprvi_3x3", "H_3x3", "alfa_3x3"):
        for ref, col in (("NDVI Planet 3x3", "ndvi_3x3"), ("copa Planet NDVI>0,5", "copa_05"), ("copa Planet NDVI>0,4", "copa_04"), ("copa Planet NDVI>0,6", "copa_06"), ("fracción de copa interpretada", "frac_mid")):
            s = c[np.isfinite(c[col])]; r, lo, hi, n = rho_ic(s[var], s[col])
            res.append(dict(variable=var, referencia=ref, n=n, rho=round(r, 3), lo=round(lo, 3), hi=round(hi, 3)))
        # diferencia pareada sobre los puntos que tienen las tres cosas
        s = c[np.isfinite(c.frac_mid) & np.isfinite(c.copa_05)]
        for ref, col in (("NDVI Planet 3x3", "ndvi_3x3"), ("copa Planet NDVI>0,5", "copa_05")):
            dd, lo, hi, n = dif_ic(s[var], s[col], s.frac_mid)
            res.append(dict(variable=var, referencia="dif rho(%s) - rho(interpretada), mismos puntos" % ref, n=n, rho=round(dd, 3), lo=round(lo, 3), hi=round(hi, 3)))
    R = pd.DataFrame(res); R.to_csv(AQUI / "planet_nisar_resultados.csv", index=False)
    # medianas por clase
    med = c.groupby("clase_final")[["ndvi_3x3", "copa_05", "dprvi", "H", "alfa"]].median().round(3)
    nn = c.groupby("clase_final").size()
    resumen = {"n_despejados": int(len(c)), "n_interpretados": int(c.frac_mid.notna().sum()),
               "principal": {k: v for k, v in R[R.variable == "dprvi"].set_index("referencia")[["n", "rho", "lo", "hi"]].T.to_dict().items()},
               "medianas_por_clase": {k: dict(n=int(nn[k]), **med.loc[k].to_dict()) for k in med.index}}
    (AQUI / "planet_nisar_resumen.json").write_text(json.dumps(resumen, indent=1, ensure_ascii=False), encoding="utf-8")
    print(R[R.variable.isin(["dprvi", "H", "alfa"])].to_string(index=False)); print(med.assign(n=nn).to_string())


if __name__ == "__main__":
    os.environ.setdefault("PROJ_DATA", os.path.join(os.path.dirname(rasterio.__file__), "proj_data"))
    main()
