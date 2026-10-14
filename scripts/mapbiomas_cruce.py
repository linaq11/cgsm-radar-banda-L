# -*- coding: utf-8 -*-
r"""Cruce exploratorio de MapBiomas Colombia (coleccion 2, clasificacion 2023, 30 m) con la
referencia del informe de radar y con la muestra 2025 de la tesis.

Tres preguntas:
  1. Sobre la malla de 50 m del mapa de NISAR, que dice el dHH (alto menos bajo del rio) en las
     clases de MapBiomas manglar (5), bosque inundable (6) y formacion herbacea inundable (11),
     y cuanto coinciden esas clases con las de WorldCover/GMW usadas en el informe.
  2. Como etiqueta MapBiomas 2023 los 720 puntos de la muestra 2025 (clase_final): si separa el
     humedal herbaceo del manglar degradado mejor que WorldCover.
  3. Hectareas por clase de MapBiomas dentro del AOI, 2015 a 2023, para la serie de la tesis.

Codigos de la leyenda MapBiomas Colombia col. 2 (verificar en el sitio antes de citar):
  3 bosque, 5 manglar, 6 bosque inundable, 11 formacion herbacea inundable, 21 mosaico
  agropecuario, 23 playas y dunas, 24 infraestructura urbana, 25 otras areas sin vegetación,
  33 rio, lago y oceano, 35 palma aceitera.

USO: python mapbiomas_cruce.py      Salidas: mapbiomas_cruce_resumen.txt, mapbiomas_aoi_serie.csv
"""
import importlib.util
import io
import os

os.environ["PROJ_DATA"] = os.path.join(importlib.util.find_spec("rasterio").submodule_search_locations[0], "proj_data")
os.environ["PROJ_LIB"] = os.environ["PROJ_DATA"]

import ee
import numpy as np
import pandas as pd
import rasterio
import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
MUESTRA = os.path.join(AQUI, "..", "AVANCE TESIS", "MUESTRA_2025", "etiquetas_2025.csv")
MB = "projects/mapbiomas-public/assets/colombia/collection2/mapbiomas_colombia_collection2_integration_v1"
NOMBRE = {3: "bosque", 5: "manglar", 6: "bosque_inundable", 11: "herbacea_inundable", 21: "mosaico_agro", 23: "playa",
          24: "urbano", 25: "sin_vegetacion", 33: "agua", 35: "palma"}
CL_WC = {1: "manglar_WC_GMW", 2: "bosque_WC", 3: "humedal_WC", 4: "agua_WC", 0: "otro"}

ee.Initialize(project="basic-buttress-338101")
AOI = ee.FeatureCollection("projects/basic-buttress-338101/assets/AOI_tesis_CGSM_v1").geometry()
mb = ee.Image(MB)
lineas = []

# 1. malla de 50 m del mapa NISAR
with rasterio.open(os.path.join(AQUI, "mapa_doble_rebote_50m.tif")) as src:
    d_hh, cl = src.read(1), src.read(4).astype(int)
    x0, y0 = src.transform.c, src.transform.f; ny, nx = d_hh.shape
with rasterio.open(os.path.join(AQUI, "mapa_s1_alto_bajo_50m.tif")) as src:
    d_vv = src.read(1)
url = mb.select("classification_2023").getDownloadURL({"crs": "EPSG:32618", "crs_transform": [50, 0, x0, 0, -50, y0],
                                                         "dimensions": [nx, ny], "format": "GEO_TIFF"})
with rasterio.open(io.BytesIO(requests.get(url, timeout=600).content)) as src:
    m23 = src.read(1).astype(int)
lineas.append("1. Malla de 50 m (caja del cubo + 2 km), MapBiomas 2023 frente a dHH NISAR y dVV Sentinel-1 (alto menos bajo del rio):")
for k in (5, 6, 11, 3, 21, 33):
    m = (m23 == k) & np.isfinite(d_hh) & np.isfinite(d_vv)
    if m.sum() < 100:
        continue
    lineas.append("   MapBiomas %-19s n %7d | dHH mediana %+.2f (positivos %.0f %%) | dVV mediana %+.2f | WorldCover/GMW en esos pixeles: %s"
                  % (NOMBRE[k], m.sum(), np.median(d_hh[m]), 100 * (d_hh[m] > 0).mean(), np.median(d_vv[m]),
                     {CL_WC[c]: round(100 * (cl[m] == c).mean()) for c in (1, 2, 3, 4, 0) if (cl[m] == c).mean() > 0.03}))
mg, wg = (m23 == 5), (cl == 1)
lineas.append("   manglar: MapBiomas %d ha, WorldCover∩GMW %d ha, interseccion %d ha (Jaccard %.2f)"
              % (mg.sum() * 0.25, wg.sum() * 0.25, (mg & wg).sum() * 0.25, (mg & wg).sum() / (mg | wg).sum()))
hm, hw = (m23 == 11), (cl == 3)
lineas.append("   herbacea inundable (MB) frente a humedal herbaceo (WC 90): %d ha frente a %d ha, interseccion %d ha (Jaccard %.2f)"
              % (hm.sum() * 0.25, hw.sum() * 0.25, (hm & hw).sum() * 0.25, (hm & hw).sum() / (hm | hw).sum()))

# 2. los 720 puntos
e = pd.read_csv(MUESTRA)[["id", "lon", "lat", "clase_final"]]
fc = ee.FeatureCollection([ee.Feature(ee.Geometry.Point([float(r.lon), float(r.lat)]), {"id": int(r.id)}) for r in e.itertuples()])
s = mb.select(["classification_2023", "classification_2021"]).reduceRegions(fc, ee.Reducer.first(), 30).getInfo()["features"]
d = pd.DataFrame([f["properties"] for f in s]).merge(e, on="id")
d["mb23"] = d.classification_2023.map(lambda v: NOMBRE.get(int(v), str(v)) if pd.notna(v) else "sin dato")
ct = pd.crosstab(d.clase_final, d.mb23)
lineas.append("\n2. Los 720 puntos de la muestra 2025 (filas: clase_final) segun MapBiomas 2023:\n" + ct.to_string())
for c in ("humedal_herbaceo", "manglar_degradado", "manglar_intacto", "otro"):
    s_ = d[d.clase_final == c].mb23.value_counts(normalize=True).round(2).head(3).to_dict()
    lineas.append("   %-18s -> %s" % (c, s_))
hd = d[d.clase_final.isin(["humedal_herbaceo", "manglar_degradado"])]
lineas.append("   humedal: %s | degradado: %s" % (hd[hd.clase_final == "humedal_herbaceo"].mb23.value_counts().to_dict(), hd[hd.clase_final == "manglar_degradado"].mb23.value_counts().to_dict()))

# 3. serie anual en el AOI
filas = []
for y in range(2015, 2024):
    h = mb.select("classification_%d" % y).reduceRegion(ee.Reducer.frequencyHistogram(), AOI, 30, maxPixels=1e10).getInfo()["classification_%d" % y]
    fila = {"anio": y}
    for k, v in h.items():
        fila[NOMBRE.get(int(float(k)), "c" + k)] = round(v * 0.09)
    filas.append(fila)
serie = pd.DataFrame(filas).fillna(0).astype(int)
serie.to_csv(os.path.join(AQUI, "mapbiomas_aoi_serie.csv"), index=False)
lineas.append("\n3. Hectareas por clase de MapBiomas dentro del AOI, 2015 a 2023 (30 m):\n" + serie[["anio", "manglar", "bosque_inundable", "herbacea_inundable", "agua", "mosaico_agro"]].to_string(index=False))
txt = "\n".join(lineas)
open(os.path.join(AQUI, "mapbiomas_cruce_resumen.txt"), "w", encoding="utf-8").write(txt + "\n")
print(txt)
