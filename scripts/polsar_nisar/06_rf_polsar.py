# -*- coding: utf-8 -*-
r"""P5 del plan (tarea del Informe 2 pedida en clase): Random Forest con las variables polarimétricas de NISAR sobre los 880
puntos v1.3, con la validación de la cadena de la tesis (pliegues de 12 km, zona de exclusión de 2,6 km, 500 árboles,
semilla de 40_ablacion_entradas). Brazos: radar solo, unión óptica (S2 + AlphaEarth) y unión + radar. Fecha principal
16-dic-2025; 4-dic como sensibilidad; las dos fechas apiladas como tercera variante. Píxel y media 3 x 3.
Contrastes: macro-F1 de seis clases fuera de pliegue; unión + radar frente a unión con permutación pareada por bloques
(5.000) y McNemar; F1 por clase para ver el par degradado / humedal.
SALIDA: rf_polsar_resultados.csv, rf_polsar_f1_clases.csv
USO: python -X utf8 06_rf_polsar.py
"""
import importlib.util
import os

os.environ["PROJ_DATA"] = os.path.join(importlib.util.find_spec("rasterio").submodule_search_locations[0], "proj_data"); os.environ["PROJ_LIB"] = os.environ["PROJ_DATA"]
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import f1_score

AQUI = Path(__file__).resolve().parent; MUESTRA = Path("C:/LINA/UNAL 2626-1/AVANCE TESIS/MUESTRA_2025"); R3 = Path("C:/LINA/UNAL 2626-1/PERCEPCION REMOTA AVANZADA/informe2_ronda3")
CLASES = ["agua", "humedal_herbaceo", "manglar_degradado", "manglar_intacto", "otro", "vegetacion_flotante"]; BUFER = 2600


def mod(n, f):
    s = importlib.util.spec_from_file_location(n, f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


def radar(fecha, suf):
    r = pd.read_csv(AQUI / ("polsar_puntos_%s_P011.csv" % fecha)); t = "_3x3" if suf == "3x3" else ""
    out = pd.DataFrame({"id": r.id, "hh_" + fecha: r["C11" + t], "hv_" + fecha: r["C22" + t], "hhhv_" + fecha: r["C11" + t] - r["C22" + t], "H_" + fecha: r["H" + t], "alfa_" + fecha: r["alfa" + t], "dprvi_" + fecha: r["dprvi" + t]})
    return out


def main():
    v01 = mod("v01", R3 / "01_variables_2025.py"); abl = mod("abl", MUESTRA / "40_ablacion_entradas.py"); abl.N_REP = 5000
    OPT = v01.F_S2 + v01.F_AE; d0 = pd.read_csv(R3 / "variables_2025_puntos.csv")
    for c in OPT:
        if d0[c].isna().any(): d0[c] = d0[c].fillna(d0[c].median())
    rng = np.random.default_rng(20261026); filas = []; f1s = []
    base_pred = None
    for suf in ("pixel", "3x3"):
        for etiqueta, fechas in (("16dic", ["20251216"]), ("04dic", ["20251204"]), ("2fechas", ["20251204", "20251216"])):
            d = d0.copy(); RAD = []
            for f in fechas:
                rf_ = radar(f, suf); d = d.merge(rf_, on="id", how="left"); RAD += [c for c in rf_.columns if c != "id"]
            for c in RAD: d[c] = d[c].fillna(d[c].median())
            y = d.clase_final.to_numpy(); bl = d.bloque12.to_numpy()
            p_rad = abl.oof(d, RAD, BUFER)
            if base_pred is None: base_pred = abl.oof(d, OPT, BUFER)          # la unión óptica no depende del radar: una sola vez
            p_uni = base_pred; p_mix = abl.oof(d, OPT + RAD, BUFER)
            m = {k: abl.macro(y, p, CLASES) for k, p in (("radar", p_rad), ("union", p_uni), ("union_radar", p_mix))}
            dif, pperm = abl.permutacion_bloques(y, p_mix, p_uni, bl, CLASES, rng); b, c, pmc = abl.mcnemar(y, p_mix, p_uni)
            dif_r, pperm_r = abl.permutacion_bloques(y, p_rad, p_uni, bl, CLASES, rng)
            filas.append(dict(variante=suf, fechas=etiqueta, n_vars_radar=len(RAD), macro_f1_radar=round(m["radar"], 3), macro_f1_union=round(m["union"], 3), macro_f1_union_radar=round(m["union_radar"], 3),
                              dif_union_radar_vs_union=round(dif, 4), p_perm=round(pperm, 4), mcnemar_solo_union=b, mcnemar_solo_mixto=c, p_mcnemar=round(pmc, 4), dif_radar_vs_union=round(dif_r, 3), p_perm_radar=round(pperm_r, 4)))
            for k, p in (("radar", p_rad), ("union", p_uni), ("union_radar", p_mix)):
                f = f1_score(y, p, labels=CLASES, average=None, zero_division=0)
                f1s.append(dict(variante=suf, fechas=etiqueta, brazo=k, **{c_: round(x, 3) for c_, x in zip(CLASES, f)}))
            print("%s %s: radar %.3f | unión %.3f | unión+radar %.3f (dif %+.4f, p perm %.3f, McNemar %d/%d p %.3f)" % (suf, etiqueta, m["radar"], m["union"], m["union_radar"], dif, pperm, b, c, pmc), flush=True)
    pd.DataFrame(filas).to_csv(AQUI / "rf_polsar_resultados.csv", index=False); pd.DataFrame(f1s).to_csv(AQUI / "rf_polsar_f1_clases.csv", index=False); print("escrito rf_polsar_resultados.csv, rf_polsar_f1_clases.csv", flush=True)


if __name__ == "__main__":
    main()
