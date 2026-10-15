# -*- coding: utf-8 -*-
"""Compara los resultados del informe en sigma cero con el recálculo en gamma cero.

PROPÓSITO
    Documentar cuánto cambian las pruebas hidrológicas, las firmas, la separabilidad y la clave al pasar
    de sigma cero a gamma cero (NISAR sin el factor gamma->sigma; Sentinel-1 y ALOS-2 corregidos por el
    coseno del ángulo de incidencia).
DATOS
    Los CSV del informe y sus pares *_gamma0.csv, generados con RADAR_MAGNITUD=gamma0.
MÉTODO
    Une cada tabla por sus claves y escribe las columnas lado a lado.
SALIDAS
    GAMMA0_comparacion.md
USO
    python comparar_gamma0.py
LIMITACIÓN
    Los umbrales absolutos de la clave en gamma cero son los de sigma cero desplazados por la mediana de γ⁰ − σ⁰ en los 720 puntos.
"""
import os
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
L = ["# Sigma cero frente a gamma cero", "",
     "Recálculo del 15 de octubre de 2026 con `RADAR_MAGNITUD=gamma0`. NISAR usa el γ⁰ RTC del producto sin el factor "
     "`rtcGammaToSigmaFactor`; Sentinel-1 se corrige con la banda `angle` (γ⁰ elipsoidal, σ⁰ − 10·log10 cos θ); "
     "ALOS-2 con el ángulo local `LIN`. Las diferencias copolar menos cruzada no cambian por construcción.", ""]

def tabla(df, cols):
    L.append("| " + " | ".join(cols) + " |"); L.append("|" + "---|" * len(cols))
    for _, r in df[cols].iterrows():
        L.append("| " + " | ".join(("%.2f" % v) if isinstance(v, float) else str(v) for v in r) + " |")
    L.append("")

def comparar(titulo, nombre, claves, vals, filtro=None):
    a = pd.read_csv(os.path.join(AQUI, nombre + ".csv")); b = pd.read_csv(os.path.join(AQUI, nombre + "_gamma0.csv"))
    if filtro: a, b = a[filtro(a)], b[filtro(b)]
    m = a.merge(b, on=claves, suffixes=(" σ⁰", " γ⁰"))
    L.append("## " + titulo); L.append("")
    tabla(m, claves + [c + s for c in vals for s in (" σ⁰", " γ⁰")])

f = lambda d: d.clase.astype(str).str.contains("menos")
comparar("Bahía de Málaga, NISAR: resta manglar menos bosque frente a la marea", "marea_vs_radar", ["traza", "variable"], ["dif_alta_menos_baja", "rho_spearman", "p"], f)
comparar("Bahía de Málaga, Sentinel-1", "s1_marea_resumen", ["orbita", "variable"], ["dif_alta_menos_baja", "rho", "p"], f)
comparar("Bahía de Málaga, ALOS-2", "alos2_marea_resumen", ["path", "variable"], ["dif_alta_menos_baja", "rho", "p"], f)
comparar("CGSM: resta manglar menos bosque frente al nivel del río", "cgsm_nivel_rio_resumen", ["sensor", "traza", "variable"], ["alto_menos_bajo_db", "rho_nivel", "p"], f)

fs = pd.read_csv(os.path.join(AQUI, "clave_muestra2025_firmas.csv")); fg = pd.read_csv(os.path.join(AQUI, "clave_muestra2025_firmas_gamma0.csv"))
m = fs.merge(fg, on="clase", suffixes=(" σ⁰", " γ⁰"))
L.append("## Firmas por clase, muestra de 720 puntos (medianas, dB)"); L.append("")
tabla(m, ["clase"] + [c + s for c in ("VV", "VH", "VVmVH", "HH", "HV", "HHmHV") for s in (" σ⁰", " γ⁰")])
js = pd.read_csv(os.path.join(AQUI, "clave_muestra2025_jm.csv")); jg = pd.read_csv(os.path.join(AQUI, "clave_muestra2025_jm_gamma0.csv"))
cols = [c for c in js.columns if c.startswith("jm ")]
mm = js.merge(jg, on="par", suffixes=(" σ⁰", " γ⁰"))
L.append("## Separabilidad de Jeffries-Matusita"); L.append("")
tabla(mm, ["par"] + [c + s for c in cols for s in (" σ⁰", " γ⁰")])

def acierto(ruta):
    cm = pd.read_csv(ruta, index_col=0)
    dec = cm.drop(columns=["sin decision"]).sum().sum()
    ok = {"agua": "1 agua abierta", "vegetacion_flotante": "2 vegetacion flotante", "manglar_intacto": "3 dosel cerrado",
          "manglar_degradado": "4 dosel abierto", "humedal_herbaceo": "4 dosel abierto", "otro": "4 dosel abierto"}
    bien = sum(cm.loc[c, k] for c, k in ok.items() if c in cm.index)
    return int(dec), int(bien)
ds, bs = acierto(os.path.join(AQUI, "clave_muestra2025_regla.csv")); dg, bg = acierto(os.path.join(AQUI, "clave_muestra2025_regla_gamma0.csv"))
L += ["## Clave de interpretación: umbrales literales en σ⁰ y umbrales desplazados en γ⁰", "",
      "| Magnitud | Decididos de 720 | Coinciden con la referencia | Acierto entre decididos |", "|---|---|---|---|",
      "| σ⁰ | %d | %d | %.1f %% |" % (ds, bs, 100 * bs / ds), "| γ⁰ (umbrales desplazados por la mediana de γ⁰ − σ⁰: VV y VH +0,83 dB) | %d | %d | %.1f %% |" % (dg, bg, 100 * bg / dg), "",
      "En γ⁰ los niveles de Sentinel-1 suben 0,83 dB y los de NISAR 1,30 dB (el término −10·log10 cos θ). Los umbrales absolutos de la clave "
      "actúan sobre VV y VH, así que en γ⁰ pasan de −17, −25 y −12 dB a −16,17, −24,17 y −11,17 dB; los umbrales sobre VV − VH (6,5) y HH − HV (7,3) "
      "no cambian. Con ese desplazamiento la clave en γ⁰ reproduce la de σ⁰ salvo tres puntos.", ""]
open(os.path.join(AQUI, "GAMMA0_comparacion.md"), "w", encoding="utf-8").write("\n".join(L))
print("escrito GAMMA0_comparacion.md | clave: sigma0 %d/%d, gamma0 %d/%d" % (bs, ds, bg, dg))
