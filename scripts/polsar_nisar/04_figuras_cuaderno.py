# -*- coding: utf-8 -*-
r"""Figuras del cuaderno PolSAR dual-pol NISAR reproducido en la CGSM (secciones 6, 7, 7c, 9.3, 9.5 y 9.6 del cuaderno de Guaviare),
a partir de los rásteres de 10 m ya remuestreados a la malla del cubo (malla10m/<fecha>_P011/*.tif) y de los valores en los 880 puntos.
 1 fig_polsar_1_rgb.png        RGB dual-pol (R = HH dB, G = HV dB, B = HH − HV dB) de toda la AOI y de la ventana de detalle, con
                               PlanetScope del mismo día (16-dic) y Sentinel-2 seca 2025 al lado.
 2 fig_polsar_2_h_alfa_dprvi.png  H, alfa y DpRVI en la ventana de detalle (16-dic) y Sentinel-2 seca.
 3 fig_polsar_3_plano.png      plano H/alfa dual-pol: densidad de píxeles de la AOI y medianas por clase v1.3 (dos fechas).
 4 fig_polsar_4_firmas.png     firmas por clase: H, alfa, DpRVI, HH y HV, dos fechas.
 5 fig_polsar_5_acuerdo.png    acuerdo del mapa manglar / no manglar por Otsu sobre DpRVI con el mapa óptico píxel 2025.
Ventana de detalle: 16 km alrededor de Pajarales y el manglar occidental (centro 4827000 E, 2754000 N, EPSG:9377).
SALIDAS: figuras/*.png, figuras_cuaderno_numeros.csv
USO: python -X utf8 04_figuras_cuaderno.py
"""
import importlib.util
import os
from pathlib import Path

os.environ["PROJ_DATA"] = os.path.join(importlib.util.find_spec("rasterio").submodule_search_locations[0], "proj_data"); os.environ["PROJ_LIB"] = os.environ["PROJ_DATA"]
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import from_bounds
from skimage.filters import threshold_otsu

AQUI = Path(__file__).resolve().parent; FIG = AQUI / "figuras"; FIG.mkdir(exist_ok=True)
CUBO = Path("C:/LINA/UNAL 2626-1/PERCEPCION REMOTA AVANZADA/informe2/datos"); PLANET = Path("C:/LINA/UNAL 2626-1/AVANCE TESIS/PLANET")
FECHAS = ["20251204", "20251216"]; CX, CY, L = 4827000, 2754000, 8000; DET = (CX - L, CY - L, CX + L, CY + L)
CLASES = ["agua", "humedal_herbaceo", "manglar_degradado", "manglar_intacto", "otro", "vegetacion_flotante"]
NOMBRE = {"agua": "Agua", "humedal_herbaceo": "Humedal herbáceo", "manglar_degradado": "Manglar degradado", "manglar_intacto": "Manglar intacto", "otro": "Otro", "vegetacion_flotante": "Vegetación flotante"}
COLOR = {"agua": "#3b6fb6", "humedal_herbaceo": "#c9a227", "manglar_degradado": "#b5533c", "manglar_intacto": "#2f7d3a", "otro": "#8c8c8c", "vegetacion_flotante": "#7bc96f"}
CODIGO = {1: "agua", 2: "humedal_herbaceo", 3: "manglar_degradado", 4: "manglar_intacto", 5: "otro", 6: "vegetacion_flotante"}   # mapa_pixel_2025.tif (se verifica abajo)


def capa(fecha, nombre, ventana=None):
    with rasterio.open(AQUI / "malla10m" / ("%s_P011" % fecha) / ("%s_malla10m.tif" % nombre)) as r:
        w = from_bounds(*ventana, r.transform) if ventana else None; a = r.read(1, window=w).astype("float32"); return a, (r.window_bounds(w) if w else r.bounds)


def estirar(a, lo, hi): return np.clip((a - lo) / (hi - lo), 0, 1)


def rgb_dp(fecha, ventana=None):
    hh, ext = capa(fecha, "C11", ventana); hv, _ = capa(fecha, "C22", ventana)
    return np.dstack([estirar(hh, -22, -4), estirar(hv, -30, -12), estirar(hh - hv, 2, 14)]), ext


def rgb_optico(f, bandas, ventana=None, p=(2, 98), mascara=None):
    with rasterio.open(f) as r:
        w = from_bounds(*ventana, r.transform) if ventana else None; a = r.read(bandas, window=w).astype("float32"); ext = r.window_bounds(w) if w else r.bounds
    if mascara is not None:
        with rasterio.open(mascara) as r: ok = r.read(1, window=w) > 0.99
    else: ok = np.ones(a.shape[1:], bool)
    out = np.zeros(a.shape, "float32")
    for i in range(3):
        v = a[i][(a[i] > 0) & ok]; lo, hi = np.percentile(v, p); out[i] = estirar(a[i], lo, hi)
    return out.transpose(1, 2, 0), ext


def ext_mpl(b): return (b[0] / 1000, b[2] / 1000, b[1] / 1000, b[3] / 1000)


def main():
    pts = {f: pd.read_csv(AQUI / ("polsar_puntos_%s_P011.csv" % f)) for f in FECHAS}; numeros = []
    # 1 RGB dual-pol
    fig, ax = plt.subplots(2, 2, figsize=(12, 11)); im, b = rgb_dp("20251216"); ax[0, 0].imshow(im, extent=ext_mpl(b)); ax[0, 0].set_title("(a) NISAR 16-dic-2025, RGB dual-pol, AOI completa")
    ax[0, 0].add_patch(plt.Rectangle((DET[0] / 1000, DET[1] / 1000), 2 * L / 1000, 2 * L / 1000, fill=False, color="yellow", lw=1.5))
    im, b = rgb_dp("20251216", DET); ax[0, 1].imshow(im, extent=ext_mpl(b)); ax[0, 1].set_title("(b) NISAR 16-dic-2025, ventana de detalle")
    im, b = rgb_optico(PLANET / "planet_20251216_10m_EPSG9377.tif", [6, 4, 2], DET, mascara=PLANET / "planet_20251216_clear_10m.tif"); ax[1, 0].imshow(im, extent=ext_mpl(b)); ax[1, 0].set_title("(c) PlanetScope 16-dic-2025, color natural (10 m)")
    im, b = rgb_optico(CUBO / "s2_2025_seca.tif", [1, 2, 3], DET); ax[1, 1].imshow(im, extent=ext_mpl(b)); ax[1, 1].set_title("(d) Sentinel-2 estación seca 2025, color natural")
    for a in ax.ravel(): a.set_xlabel("E (km, EPSG:9377)"); a.set_ylabel("N (km)")
    fig.suptitle("Compuesto RGB dual-pol (R = HH, G = HV, B = HH − HV, en dB) y referencia óptica", fontsize=12); fig.tight_layout(); fig.savefig(FIG / "fig_polsar_1_rgb.png", dpi=130); plt.close(fig)
    # 2 H, alfa, DpRVI
    fig, ax = plt.subplots(2, 2, figsize=(12, 11))
    for a, (nombre, titulo, vmin, vmax, cmap) in zip(ax.ravel()[:3], [("H", "(a) Entropía H", 0, 1, "viridis"), ("alfa", "(b) Ángulo alfa (°)", 0, 45, "magma"), ("dprvi", "(c) DpRVI", 0, 0.8, "YlGn")]):
        v, b = capa("20251216", nombre, DET); m = a.imshow(v, extent=ext_mpl(b), vmin=vmin, vmax=vmax, cmap=cmap); a.set_title(titulo); fig.colorbar(m, ax=a, shrink=0.8)
    im, b = rgb_optico(CUBO / "s2_2025_seca.tif", [4, 1, 2], DET); ax[1, 1].imshow(im, extent=ext_mpl(b)); ax[1, 1].set_title("(d) Sentinel-2 seca 2025, infrarrojo color")
    p = pts["20251216"]
    from pyproj import Transformer
    x, y = Transformer.from_crs(4326, 9377, always_xy=True).transform(p.lon.values, p.lat.values); den = (x > DET[0]) & (x < DET[2]) & (y > DET[1]) & (y < DET[3])
    for c in CLASES: s = den & (p.clase_final == c).values; ax[1, 1].scatter(x[s] / 1000, y[s] / 1000, s=14, c=COLOR[c], edgecolor="k", lw=0.3, label=NOMBRE[c])
    ax[1, 1].legend(fontsize=7, loc="lower left")
    for a in ax.ravel(): a.set_xlabel("E (km)"); a.set_ylabel("N (km)")
    fig.suptitle("Descomposición H/alfa dual-pol y DpRVI, NISAR 16-dic-2025 (Lee refinado 7 x 7, 10 m), ventana de detalle", fontsize=12); fig.tight_layout(); fig.savefig(FIG / "fig_polsar_2_h_alfa_dprvi.png", dpi=130); plt.close(fig)
    # 3 plano H/alfa
    fig, ax = plt.subplots(1, 2, figsize=(13, 5.5), sharey=True)
    for a, f in zip(ax, FECHAS):
        H, _ = capa(f, "H"); A, _ = capa(f, "alfa"); ok = np.isfinite(H) & np.isfinite(A); h = H[ok][::7]; al = A[ok][::7]
        a.hist2d(h, al, bins=120, range=[[0, 1], [0, 45]], cmap="Greys", cmin=1); p = pts[f]
        for c in CLASES:
            s = p[p.clase_final == c]; a.scatter(s.H_3x3, s.alfa_3x3, s=9, c=COLOR[c], alpha=0.55, edgecolor="none"); a.scatter(s.H_3x3.median(), s.alfa_3x3.median(), s=140, c=COLOR[c], edgecolor="k", lw=1.2, marker="o", label=NOMBRE[c], zorder=5)
        a.set_xlabel("Entropía H"); a.set_title("NISAR %s-%s-%s" % (f[6:], f[4:6], f[:4])); a.set_xlim(0, 1); a.set_ylim(0, 45)
    ax[0].set_ylabel("Ángulo alfa (°)"); ax[1].legend(fontsize=8, loc="upper left", title="Clases v1.3 (puntos: media 3 x 3; círculo grande: mediana)", title_fontsize=8)
    fig.suptitle("Plano H/alfa dual-pol: densidad de píxeles de la AOI (gris) y los 880 puntos de la muestra", fontsize=12); fig.tight_layout(); fig.savefig(FIG / "fig_polsar_3_plano.png", dpi=130); plt.close(fig)
    # 4 firmas por clase
    VARS = [("H_3x3", "Entropía H"), ("alfa_3x3", "Alfa (°)"), ("dprvi_3x3", "DpRVI"), ("C11_3x3", "HH (dB)"), ("C22_3x3", "HV (dB)")]
    fig, ax = plt.subplots(1, 5, figsize=(17, 4.6))
    for a, (v, t) in zip(ax, VARS):
        pos = np.arange(len(CLASES)); w = 0.36
        for k, f in enumerate(FECHAS):
            p = pts[f]; datos = [p.loc[p.clase_final == c, v].dropna().values for c in CLASES]
            bp = a.boxplot(datos, positions=pos + (k - 0.5) * w * 1.05, widths=w, showfliers=False, patch_artist=True, medianprops=dict(color="k"))
            for parche, c in zip(bp["boxes"], CLASES): parche.set_facecolor(COLOR[c]); parche.set_alpha(0.95 if k else 0.45)
            for c, d_ in zip(CLASES, datos): numeros.append(dict(figura=4, fecha=f, variable=v, clase=c, n=len(d_), mediana=round(float(np.median(d_)), 3), q1=round(float(np.percentile(d_, 25)), 3), q3=round(float(np.percentile(d_, 75)), 3)))
        a.set_xticks(pos); a.set_xticklabels(["Agua", "Hum.", "Degr.", "Int.", "Otro", "Flot."], fontsize=8); a.set_title(t)
    fig.suptitle("Firmas PolSAR por clase v1.3 (media 3 x 3 en los 880 puntos; cajas = cuartiles, sin valores extremos; claro 4-dic, oscuro 16-dic)" + chr(10) + "Hum. = humedal herbáceo, Degr. = manglar degradado, Int. = manglar intacto, Flot. = vegetación flotante", fontsize=11); fig.tight_layout(); fig.savefig(FIG / "fig_polsar_4_firmas.png", dpi=130); plt.close(fig)
    # 5 acuerdo con el mapa óptico
    with rasterio.open(CUBO / "mapa_pixel_2025.tif") as r: mapa = r.read(1); bm = r.bounds
    p = pts["20251216"].dropna(subset=["dprvi"]); p = p[p.clase_final.isin(["manglar_intacto", "manglar_degradado", "humedal_herbaceo", "otro"])]; umbral = threshold_otsu(p.dprvi.values)
    D, _ = capa("20251216", "dprvi"); radar_bosque = D > umbral; valido = np.isfinite(D) & (mapa > 0)
    # verificación del código de clases del mapa con los puntos
    from pyproj import Transformer
    pp = pts["20251216"]; x, y = Transformer.from_crs(4326, 9377, always_xy=True).transform(pp.lon.values, pp.lat.values)
    with rasterio.open(CUBO / "mapa_pixel_2025.tif") as r: fil, col = rasterio.transform.rowcol(r.transform, x, y)
    cod = mapa[np.clip(fil, 0, mapa.shape[0] - 1), np.clip(col, 0, mapa.shape[1] - 1)]; acuerdo = np.mean([CODIGO.get(int(c), "?") == k for c, k in zip(cod, pp.clase_final)]); print("acuerdo mapa óptico vs etiqueta v1.3 en los puntos (verifica CODIGO): %.2f" % acuerdo, flush=True)
    opt_manglar = np.isin(mapa, [3, 4]); opt_no = np.isin(mapa, [2, 5])
    cat = np.zeros(mapa.shape, "uint8"); cat[valido & opt_manglar & radar_bosque] = 1; cat[valido & opt_manglar & ~radar_bosque] = 2; cat[valido & opt_no & radar_bosque] = 3; cat[valido & opt_no & ~radar_bosque] = 4
    n = {k: int((cat == k).sum()) for k in (1, 2, 3, 4)}; tot = sum(n.values()); print("acuerdo píxel (manglar/no manglar, sin agua ni flotante): %.3f; umbral Otsu %.3f" % ((n[1] + n[4]) / tot, umbral), flush=True)
    for k, nombre in ((1, "ambos manglar"), (2, "solo óptico"), (3, "solo radar"), (4, "ambos no manglar")): numeros.append(dict(figura=5, fecha="20251216", variable="acuerdo", clase=nombre, n=n[k], mediana=round(n[k] / tot, 3)))
    frac = {CODIGO[c]: float(radar_bosque[valido & (mapa == c)].mean()) for c in range(1, 7)}
    for c, v in frac.items(): numeros.append(dict(figura=5, fecha="20251216", variable="fraccion_radar_bosque", clase=c, n=int((valido & (mapa == CLASES.index(c) + 1)).sum()), mediana=round(v, 3)))
    from matplotlib.colors import ListedColormap
    fig, ax = plt.subplots(1, 2, figsize=(14, 6.5), gridspec_kw=dict(width_ratios=[1.35, 1]))
    cm = ListedColormap(["white", "#2f7d3a", "#c9a227", "#b5533c", "#e8e8e8"]); ax[0].imshow(cat, extent=ext_mpl(bm), cmap=cm, vmin=0, vmax=4, interpolation="nearest")
    from matplotlib.patches import Patch
    ax[0].legend(handles=[Patch(color="#2f7d3a", label="Manglar en ambos (%.0f %%)" % (100 * n[1] / tot)), Patch(color="#c9a227", label="Solo óptico (%.0f %%)" % (100 * n[2] / tot)), Patch(color="#b5533c", label="Solo radar (%.0f %%)" % (100 * n[3] / tot)), Patch(color="#e8e8e8", label="No manglar en ambos (%.0f %%)" % (100 * n[4] / tot))], fontsize=8, loc="lower left")
    ax[0].set_title("(a) Manglar por DpRVI > %.3f (Otsu) frente al mapa óptico 2025" % umbral); ax[0].set_xlabel("E (km)"); ax[0].set_ylabel("N (km)")
    ax[1].barh([NOMBRE[c] for c in CLASES], [100 * frac[c] for c in CLASES], color=[COLOR[c] for c in CLASES]); ax[1].set_xlabel("Píxeles clasificados como bosque por el radar (%)"); ax[1].set_title("(b) Por clase del mapa óptico"); ax[1].set_xlim(0, 100)
    fig.tight_layout(); fig.savefig(FIG / "fig_polsar_5_acuerdo.png", dpi=130); plt.close(fig)
    pd.DataFrame(numeros).to_csv(AQUI / "figuras_cuaderno_numeros.csv", index=False); print("figuras en", FIG, flush=True)


if __name__ == "__main__":
    main()
