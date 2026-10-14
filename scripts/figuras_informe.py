# -*- coding: utf-8 -*-
"""Genera las figuras del informe del ejercicio polarimetrico desde los productos SNAP.

Lee los BEAM-DIMAP producidos por la cadena Calibrate -> T3 -> Refined Lee ->
Freeman-Durden -> Terrain Correction y escribe PNG en figuras/.
"""
import os

import numpy as np
import rasterio

os.environ["PROJ_LIB"] = os.path.join(os.path.dirname(rasterio.__file__), "proj_data")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = ("C:/LINA/UNAL 2626-1/RADAR/"
        "RS2_OK153952_PK1408399_DK1372518_FQ17_20150626_052324_HH_VV_HV_VH_SLC")
SAL = "C:/LINA/UNAL 2626-1/RADAR/figuras"
os.makedirs(SAL, exist_ok=True)
PASO = 3  # submuestreo para que las figuras pesen poco


def leer(prod, banda, paso=PASO):
    with rasterio.open(os.path.join(BASE, prod, banda)) as s:
        return s.read(1)[::paso, ::paso]


def validos(a):
    """Mascara de pixeles con dato: SNAP escribe 0 exacto fuera de la huella."""
    return np.isfinite(a) & (a != 0)


def estirar(a, lo=2, hi=98):
    """Estiramiento por percentiles. Las bandas Freeman vienen en dB (negativas),
    asi que el filtro es por no-dato, no por signo."""
    m = validos(a)
    v = a[m]
    if v.size == 0:
        return np.zeros_like(a)
    p1, p2 = np.percentile(v, [lo, hi])
    out = np.clip((a - p1) / (p2 - p1 + 1e-12), 0, 1)
    out[~m] = 0.0
    return out


def rgb_freeman(prod, titulo, salida, lo=2, hi=98):
    r = estirar(leer(prod, "Freeman_dbl_r.img"), lo, hi)
    g = estirar(leer(prod, "Freeman_vol_g.img"), lo, hi)
    b = estirar(leer(prod, "Freeman_surf_b.img"), lo, hi)
    img = np.dstack([r, g, b])
    alto, ancho = img.shape[:2]
    fig, ax = plt.subplots(figsize=(7, 7 * alto / ancho), dpi=110)
    ax.imshow(img)
    ax.set_title(titulo, fontsize=10)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, salida), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("escrita:", salida)


def comparar_speckle():
    """Recorte igual antes y despues del filtro Refined Lee."""
    y0, x0, lado = 1200, 900, 400
    fig, axes = plt.subplots(1, 2, figsize=(10, 5.2), dpi=110)
    for ax, prod, tit in [
            (axes[0], "RS2_FQ17_Cal_T3.data", "T11 sin filtrar"),
            (axes[1], "RS2_FQ17_Cal_T3_Spk.data", "T11 tras Refined Lee")]:
        with rasterio.open(os.path.join(BASE, prod, "T11.img")) as s:
            a = s.read(1, window=((y0, y0 + lado), (x0, x0 + lado)))
        ax.imshow(estirar(a, 2, 98), cmap="gray")
        # T11 es potencia lineal (positiva); el coef. de variacion mide el speckle
        v = a[np.isfinite(a) & (a > 0)]
        cv = v.std() / v.mean() if v.size else float("nan")
        ax.set_title("%s\ncoef. de variacion = %.2f" % (tit, cv), fontsize=10)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, "speckle_antes_despues.png"),
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("escrita: speckle_antes_despues.png")


def canales_freeman():
    """Los tres mecanismos por separado, en escala de grises."""
    prod = "RS2_FQ17_Cal_T3_Spk_Decomp_TC.data"
    datos = [("Freeman_surf_b.img", "Superficie\n(agua lisa, suelo desnudo)"),
             ("Freeman_vol_g.img", "Volumen\n(dosel, dispersores al azar)"),
             ("Freeman_dbl_r.img", "Doble rebote\n(estructuras verticales)")]
    fig, axes = plt.subplots(1, 3, figsize=(13, 5.6), dpi=110)
    for ax, (b, t) in zip(axes, datos):
        ax.imshow(estirar(leer(prod, b), 2, 98), cmap="gray")
        ax.set_title(t, fontsize=10)
        ax.axis("off")
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, "canales_freeman.png"),
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("escrita: canales_freeman.png")


def histograma_incidencia():
    a = leer("RS2_FQ17_Cal_T3_Spk_Decomp_TC.data", "localIncidenceAngle.img")
    v = a[validos(a)]
    # los extremos (<5 y >80 grados) son artefactos de borde del DEM, no terreno real
    v = v[(v > 5) & (v < 80)]
    fig, ax = plt.subplots(figsize=(7, 3.4), dpi=110)
    ax.hist(v, bins=80, color="#1F4E5F")
    ax.axvline(35, color="#c0392b", ls="--", lw=1.6,
               label="35 grados: umbral de P025")
    ax.set_xlabel("Angulo de incidencia local (grados)")
    ax.set_ylabel("Pixeles")
    ax.set_title("Angulo de incidencia local en la escena de Wesenberg", fontsize=10)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, "incidencia_hist.png"),
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    pct = 100 * (v < 35).mean()
    print("escrita: incidencia_hist.png | mediana %.1f | %% bajo 35 grados: %.1f"
          % (np.median(v), pct))
    return float(np.median(v)), float(pct), float(v.min()), float(v.max())


if __name__ == "__main__":
    rgb_freeman("RS2_FQ17_Cal_T3_Spk_Decomp.data",
                "Freeman-Durden en geometria de rango-azimut",
                "freeman_rango.png")
    rgb_freeman("RS2_FQ17_Cal_T3_Spk_Decomp_TC.data",
                "Freeman-Durden tras correccion de terreno (WGS84)",
                "freeman_tc.png")
    comparar_speckle()
    canales_freeman()
    med, pct, mn, mx = histograma_incidencia()
    print("\nresumen incidencia: min %.1f max %.1f mediana %.1f, %.1f%% bajo 35"
          % (mn, mx, med, pct))
