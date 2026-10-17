# -*- coding: utf-8 -*-
"""Descarga el nivel histórico del río Magdalena en Remolino (IDEAM 2904700095), 2014 a 2024, para la serie ALOS-2.

Complementa nivel_ideam_descarga.py, que solo baja desde 2025. Misma fuente (Datos Abiertos Colombia, API Socrata)
y mismos tres conjuntos: instantáneo, máximo diario y mínimo diario. Se descarga por año para no superar el límite
de la API y se guarda en nivel_ideam_<nombre>_2014_2024.csv.

USO
    python nivel_ideam_historico.py
"""
import os
import time

import pandas as pd
import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTACION = "2904700095"
DATASETS = {"bdmn-sqnh": "instantaneo", "vfth-yucv": "maximo", "pt9a-aamx": "minimo"}

for rid, nombre in DATASETS.items():
    partes = []
    for anio in range(2014, 2025):
        url = "https://www.datos.gov.co/resource/%s.json" % rid
        params = {"$where": "codigoestacion='%s' AND fechaobservacion >= '%d-01-01T00:00:00' AND fechaobservacion < '%d-01-01T00:00:00'" % (ESTACION, anio, anio + 1),
                  "$limit": 500000, "$order": "fechaobservacion"}
        t0 = time.time()
        for intento in range(3):
            try:
                r = requests.get(url, params=params, timeout=600); r.raise_for_status(); d = pd.DataFrame(r.json()); break
            except Exception as e:
                print("%s %d intento %d: %r" % (nombre, anio, intento + 1, e), flush=True); d = None; time.sleep(10)
        if d is None:
            continue
        print("%s %d: %d filas en %.0f s" % (nombre, anio, len(d), time.time() - t0), flush=True)
        if len(d):
            partes.append(d)
    if partes:
        todo = pd.concat(partes, ignore_index=True)
        todo.to_csv(os.path.join(AQUI, "nivel_ideam_%s_2014_2024.csv" % nombre), index=False)
        print("  -> nivel_ideam_%s_2014_2024.csv %s, %s a %s" % (nombre, todo.shape, todo.fechaobservacion.min(), todo.fechaobservacion.max()), flush=True)
print("FIN", flush=True)
