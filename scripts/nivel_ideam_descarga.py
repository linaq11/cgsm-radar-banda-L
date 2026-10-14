# -*- coding: utf-8 -*-
"""Descarga las series de nivel hidrológico del IDEAM usadas para caracterizar la condición
hidrológica de la CGSM.

PROPÓSITO
Obtener el nivel del río Magdalena en la estación automática Remolino y evaluar otras estaciones
disponibles como posibles referencias hidrológicas. El nivel de Remolino se usa como indicador
regional del estado hidrológico de la CGSM y complementa el análisis exploratorio basado en la
precipitación antecedente de ERA5-Land.

FUENTE
Datos Abiertos Colombia, IDEAM, a través de la API Socrata.

SALIDAS
- nivel_ideam_<dataset>.csv
- nivel_ideam_resumen.txt

USO
    python nivel_ideam_descarga.py
"""
import io
import os
import time

import pandas as pd
import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
DESDE = "2025-01-01T00:00:00"
ESTACIONES = ["2904700095", "0029047020", "0029047000", "0029067130"]
DATASETS = {"bdmn-sqnh": "instantaneo", "vfth-yucv": "maximo", "pt9a-aamx": "minimo"}

resumen = []
for rid, nombre in DATASETS.items():
    partes = []
    for cod in ESTACIONES:
        url = f"https://www.datos.gov.co/resource/{rid}.json"
        params = {"$where": f"codigoestacion='{cod}' AND fechaobservacion >= '{DESDE}'",
                  "$limit": 500000, "$order": "fechaobservacion"}
        t0 = time.time()
        try:
            r = requests.get(url, params=params, timeout=600)
            r.raise_for_status()
            d = pd.DataFrame(r.json())
        except Exception as e:
            resumen.append(f"{rid} {nombre} {cod}: ERROR {e!r}")
            print(resumen[-1], flush=True)
            continue
        resumen.append(f"{rid} {nombre} {cod}: {len(d)} filas en {time.time() - t0:.0f} s"
                       + (f", {d.fechaobservacion.min()} a {d.fechaobservacion.max()}" if len(d) else ""))
        print(resumen[-1], flush=True)
        if len(d):
            partes.append(d)
    if partes:
        todo = pd.concat(partes, ignore_index=True)
        todo.to_csv(os.path.join(AQUI, f"nivel_ideam_{nombre}.csv"), index=False)
        print("  ->", f"nivel_ideam_{nombre}.csv", todo.shape, flush=True)
        print(todo.groupby(["codigoestacion", "nombreestacion", "descripcionsensor", "unidadmedida"]).size().to_string(), flush=True)

# Nivel del mar en el Caribe (por si hay mareógrafo cerca de la CGSM)
try:
    r = requests.get("https://www.datos.gov.co/resource/ia8x-22em.json",
                     params={"$where": f"fechaobservacion >= '{DESDE}'", "$limit": 500000}, timeout=600)
    r.raise_for_status()
    m = pd.DataFrame(r.json())
    if len(m):
        m.to_csv(os.path.join(AQUI, "nivel_ideam_mar.csv"), index=False)
        g = m.groupby(["codigoestacion", "nombreestacion", "departamento", "municipio", "latitud", "longitud"]).agg(
            n=("valorobservado", "size"), f0=("fechaobservacion", "min"), f1=("fechaobservacion", "max"))
        print("\nNivel del mar, estaciones con datos desde 2025:\n" + g.to_string(), flush=True)
        resumen.append("nivel del mar: " + str(len(m)) + " filas, " + str(len(g)) + " estaciones")
    else:
        resumen.append("nivel del mar: sin filas desde 2025")
except Exception as e:
    resumen.append(f"nivel del mar: ERROR {e!r}")
print(resumen[-1], flush=True)

io.open(os.path.join(AQUI, "nivel_ideam_resumen.txt"), "w", encoding="utf-8").write("\n".join(resumen))
print("FIN", flush=True)
