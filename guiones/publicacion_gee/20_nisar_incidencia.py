# -*- coding: utf-8 -*-
r"""Anade el angulo de incidencia a los recortes NISAR que no lo traen.

Los dos primeros recortes (2025-12-04 y 2025-12-16) se hicieron antes de que
18_nisar_recorte_remoto.py copiara la malla de metadatos radarGrid. El angulo hace
falta para estratificar el doble rebote (umbral de 35 grados). Se lee solo esa
malla gruesa del producto remoto, que pesa poco, y se escribe dentro del recorte.

Como los demás scripts de descarga, usa la sesión Earthdata del usuario; correr desde
su terminal.

USO
    python 20_nisar_incidencia.py
"""
import glob
import os
import sys

import h5py

DESTINO = r"D:\TESIS_DATACUBE\NISAR"
BASE = "https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_BETA_V1/{g}/{g}.h5"
RUTAS = ("science/LSAR/GCOV/metadata/radarGrid/incidenceAngle",
         "science/LSAR/GCOV/metadata/radarGrid/xCoordinates",
         "science/LSAR/GCOV/metadata/radarGrid/yCoordinates")

if not os.path.isdir(DESTINO):
    sys.exit("ABORTA: D: desmontado")
try:
    import earthaccess
except ImportError:
    sys.exit("falta earthaccess")

pendientes = []
for r in sorted(glob.glob(os.path.join(DESTINO, "NISAR_AOI_*.h5"))):
    with h5py.File(r, "r") as h:
        if RUTAS[0] not in h:
            pendientes.append((r, h.attrs["origen"]))
if not pendientes:
    sys.exit("todos los recortes ya tienen angulo de incidencia")
print("recortes sin incidencia:", [os.path.basename(r)[10:18] for r, _ in pendientes])

auth = earthaccess.login()
if not auth.authenticated:
    sys.exit("sin sesion Earthdata")
fs = earthaccess.get_fsspec_https_session()

for r, g in pendientes:
    print("leyendo incidencia de", g[43:51], "...", end=" ", flush=True)
    with fs.open(BASE.format(g=g), "rb", block_size=4 * 2 ** 20) as fr, h5py.File(fr, "r") as h:
        datos = {ruta: h[ruta][()] for ruta in RUTAS if ruta in h}
    with h5py.File(r, "a") as ho:
        for ruta, v in datos.items():
            ho.create_dataset(ruta, data=v)
    print("ok (%s)" % ("x".join(str(s) for s in datos[RUTAS[0]].shape) if RUTAS[0] in datos else "sin dato"))
print("listo")
