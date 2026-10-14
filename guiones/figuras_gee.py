# -*- coding: utf-8 -*-
"""Figuras del ejercicio de SAR basics de GEE, corrido sobre el AOI de la tesis.

Replica los tres pasos del tutorial (cobertura, orbitas e incidencia,
retrodispersion) usando COPERNICUS/S1_GRD sobre AOI_tesis_CGSM_v1 en vez del
area de ejemplo. Escribe PNG en figuras/.
"""
import json
import os
import warnings

import ee
import numpy as np

warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AOI_JSON = "C:/LINA/UNAL 2626-1/AVANCE TESIS/AOI/AOI_tesis_CGSM_v1.geojson"
SAL = "C:/LINA/UNAL 2626-1/RADAR/figuras"
ANIO = "2021"
os.makedirs(SAL, exist_ok=True)

ee.Initialize(project="basic-buttress-338101")
aoi = ee.Geometry(json.load(open(AOI_JSON, encoding="utf-8"))["features"][0]["geometry"])
col = (ee.ImageCollection("COPERNICUS/S1_GRD")
       .filterBounds(aoi)
       .filterDate(f"{ANIO}-01-01", f"{ANIO+''}-12-31")
       .filter(ee.Filter.eq("instrumentMode", "IW")))


def malla(imagen, escala=300):
    """Baja una imagen de GEE como GeoTIFF y la devuelve como arreglo numpy.

    sampleRectangle falla con bandas int y tiene tope de pixeles; la descarga
    directa es la via fiable para un recorte del tamano del AOI.
    """
    import io
    import urllib.request
    import zipfile

    import rasterio

    url = imagen.toFloat().getDownloadURL({
        "region": aoi, "scale": escala, "format": "GEO_TIFF"})
    with urllib.request.urlopen(url, timeout=180) as r:
        datos = r.read()
    if datos[:2] == b"PK":                      # a veces devuelve zip
        with zipfile.ZipFile(io.BytesIO(datos)) as z:
            datos = z.read([n for n in z.namelist() if n.endswith(".tif")][0])
    with rasterio.open(io.BytesIO(datos)) as s:
        a = s.read(1).astype(float)
        nod = s.nodata
    a[a == (nod if nod is not None else 0)] = np.nan
    return a


def fig_cobertura():
    """Paso 1 adaptado: cobertura TEMPORAL, no espacial.

    El mapa de densidad del tutorial es informativo a escala continental. Sobre un
    AOI de 2.042 km2, mas pequeno que una sola franja IW (250 km), el conteo por
    pixel es practicamente constante y el mapa no dice nada. La variable que si
    varia a esta escala es el reparto temporal, que ademas alimenta el analisis de
    epocas del cubo.
    """
    from collections import Counter
    props = col.reduceColumns(
        ee.Reducer.toList(2),
        ["system:time_start", "orbitProperties_pass"]).getInfo()["list"]
    import datetime
    meses = {"ASCENDING": Counter(), "DESCENDING": Counter()}
    for t, p in props:
        m = datetime.datetime.utcfromtimestamp(t / 1000).month
        meses[p][m] += 1
    x = np.arange(1, 13)
    fig, ax = plt.subplots(figsize=(9, 3.8), dpi=110)
    asc = [meses["ASCENDING"][m] for m in x]
    des = [meses["DESCENDING"][m] for m in x]
    ax.bar(x - 0.2, asc, width=0.4, label="Ascendente (%d)" % sum(asc), color="#1F4E5F")
    ax.bar(x + 0.2, des, width=0.4, label="Descendente (%d)" % sum(des), color="#c0842f")
    ax.set_xticks(x)
    ax.set_xticklabels(["E","F","M","A","M","J","J","A","S","O","N","D"])
    ax.set_ylabel("escenas")
    ax.set_title("Cobertura temporal Sentinel-1 IW sobre el AOI de la CGSM, %s" % ANIO,
                 fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, "gee_cobertura.png"),
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("escrita: gee_cobertura.png | asc %d desc %d" % (sum(asc), sum(des)))
    return sum(asc), sum(des)


def fig_orbitas():
    """Paso 2: reparto por orbita relativa y plataforma."""
    props = col.reduceColumns(
        ee.Reducer.toList(3),
        ["relativeOrbitNumber_start", "orbitProperties_pass", "platform_number"]
    ).getInfo()["list"]
    from collections import Counter
    c = Counter((int(p[0]), p[1][:3]) for p in props)
    etiquetas = ["orb %d\n%s" % k for k in sorted(c)]
    valores = [c[k] for k in sorted(c)]
    fig, ax = plt.subplots(figsize=(7, 3.6), dpi=110)
    ax.bar(etiquetas, valores, color="#1F4E5F")
    ax.set_ylabel("escenas en %s" % ANIO)
    ax.set_title("Orbitas relativas que cubren el AOI", fontsize=10)
    for i, v in enumerate(valores):
        ax.text(i, v + 1, str(v), ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, "gee_orbitas.png"),
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("escrita: gee_orbitas.png |", dict(c))
    return dict(c)


def fig_incidencia():
    """Paso 2: angulo de incidencia sobre el AOI."""
    a = malla(ee.Image(col.first()).select("angle"), escala=200)
    v = a[np.isfinite(a)]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), dpi=110)
    im = axes[0].imshow(a, cmap="viridis")
    axes[0].set_title("Angulo de incidencia, escena unica", fontsize=10)
    axes[0].axis("off")
    plt.colorbar(im, ax=axes[0], shrink=0.8, label="grados")
    axes[1].hist(v, bins=60, color="#1F4E5F")
    axes[1].axvline(35, color="#c0392b", ls="--", lw=1.6,
                    label="35 grados: umbral de P025")
    axes[1].set_xlabel("Angulo de incidencia (grados)")
    axes[1].set_ylabel("Pixeles")
    axes[1].legend(fontsize=8)
    axes[1].set_title("Distribucion sobre el AOI", fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, "gee_incidencia.png"),
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("escrita: gee_incidencia.png | min %.1f mediana %.1f max %.1f | %% <35: %.1f"
          % (v.min(), np.median(v), v.max(), 100 * (v < 35).mean()))
    return float(v.min()), float(np.median(v)), float(v.max())


def fig_retrodispersion():
    """Paso 3: VV y VH por clase de cobertura, usando las etiquetas debiles."""
    etiquetas = ee.FeatureCollection([
        ee.Feature(ee.Geometry.Point(f["geometry"]["coordinates"]),
                   {"clase_nombre": f["properties"]["clase_nombre"]})
        for f in json.load(open(
            "C:/LINA/UNAL 2626-1/AVANCE TESIS/AOI/etiquetas_debiles_worldcover_v1.geojson",
            encoding="utf-8"))["features"]])
    # mediana de un solo mes (marzo 2021, estacion seca) en vez de las 197 escenas:
    # el proyecto esta en modo restringido de cuota y la mediana anual la excede
    med = (col.filterDate("2021-03-01", "2021-04-01").select(["VV", "VH"]).median())
    m = med.sampleRegions(collection=etiquetas, scale=10).getInfo()["features"]
    datos = {}
    for f in m:
        p = f["properties"]
        if p.get("VV") is None:
            continue
        datos.setdefault(p["clase_nombre"], {"VV": [], "VH": []})
        datos[p["clase_nombre"]]["VV"].append(p["VV"])
        datos[p["clase_nombre"]]["VH"].append(p["VH"])
    orden = [c for c in ["agua", "manglar", "humedal_herbaceo", "otro"] if c in datos]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), dpi=110)
    for ax, pol in zip(axes, ["VV", "VH"]):
        ax.boxplot([datos[c][pol] for c in orden], labels=orden, showfliers=False)
        ax.set_ylabel("%s (dB)" % pol)
        ax.set_title("Retrodispersion %s por clase, mediana %s" % (pol, ANIO), fontsize=10)
        ax.tick_params(axis="x", labelrotation=20, labelsize=8)
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(os.path.join(SAL, "gee_retrodispersion.png"),
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    for c in orden:
        print("  %-18s VV %.1f dB | VH %.1f dB (n=%d)" %
              (c, np.median(datos[c]["VV"]), np.median(datos[c]["VH"]),
               len(datos[c]["VV"])))
    print("escrita: gee_retrodispersion.png")
    return {c: (float(np.median(datos[c]["VV"])), float(np.median(datos[c]["VH"])),
                len(datos[c]["VV"])) for c in orden}


if __name__ == "__main__":
    print("escenas IW sobre el AOI en %s: %d" % (ANIO, col.size().getInfo()))
    fig_cobertura()
    fig_orbitas()
    fig_incidencia()
    fig_retrodispersion()
