# -*- coding: utf-8 -*-
r"""Baja de NISAR GCOV solo la ventana del AOI, leyendo el HDF5 remoto por rangos.

POR QUE. Un GCOV completo pesa ~5,7 GB y a la velocidad medida (0,5 MB/s) son tres
horas por escena. El AOI ocupa ~3,5 % del cuadro, y HDF5 permite leer solo los
bloques que caen dentro de una ventana. Cada recorte queda en D:\TESIS_DATACUBE\NISAR
con la misma estructura de grupos que el producto original, de modo que
16_inventario_nisar.py y 12_nisar_parches.py lo leen sin cambios.

ORDEN. Primero las tres escenas de diciembre de 2025, que caen dentro del cubo y
son las que necesita la ablacion; despues las demas.

AUTENTICACION. Como en 17_descargar_nisar.py: earthaccess lee ~/.netrc o pregunta
en la terminal; este guion no maneja contrasenas. Ejecutar desde la terminal de Lina.

USO
    python 18_nisar_recorte_remoto.py        # todas las que falten
    python 18_nisar_recorte_remoto.py 2      # como maximo dos escenas en esta corrida
"""
import json
import os
import sys
import time

import h5py
import numpy as np

DESTINO = r"D:\TESIS_DATACUBE\NISAR"
ZARR = r"D:\TESIS_DATACUBE\cgsm_cube.zarr"
MARGEN_M = 2000          # aire alrededor del AOI, en metros
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
GRANULOS = [
    # diciembre de 2025 primero: caen dentro del cubo
    "NISAR_L2_PR_GCOV_007_011_D_083_4005_DHDH_A_20251204T232730_20251204T232807_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_008_011_D_083_4005_DHDH_A_20251216T232731_20251216T232808_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_009_011_D_083_4005_DHDH_A_20251228T232731_20251228T232808_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_010_011_D_083_4005_DHDH_A_20260109T232732_20260109T232809_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_006_011_D_083_4005_DHDH_A_20251122T232729_20251122T232806_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_004_011_D_083_4005_DHDH_A_20251029T232728_20251029T232806_X05009_N_F_J_001",
]
BASE = "https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_BETA_V1/{g}/{g}.h5"

if not os.path.isdir(DESTINO):
    sys.exit("ABORTA: D: desmontado")
try:
    import earthaccess
except ImportError:
    sys.exit("falta earthaccess: pip install earthaccess --break-system-packages")

# extension del AOI en UTM 18N, que es la malla de los GCOV sobre la CGSM
from pyproj import Transformer

at = json.load(open(os.path.join(ZARR, "zarr.json"), encoding="utf-8"))["attributes"]
tr = at["transform"]
alto, ancho = 6022, 7150
t = Transformer.from_crs("EPSG:9377", "EPSG:32618", always_xy=True)
xs, ys = [], []
for cx in (tr[2], tr[2] + ancho * 10):
    for cy in (tr[5], tr[5] - alto * 10):
        u, v = t.transform(cx, cy)
        xs.append(u)
        ys.append(v)
X0, X1 = min(xs) - MARGEN_M, max(xs) + MARGEN_M
Y0, Y1 = min(ys) - MARGEN_M, max(ys) + MARGEN_M

auth = earthaccess.login()
if not auth.authenticated:
    sys.exit("sin sesion Earthdata")


def sistema_de_archivos():
    """HTTPS con la sesion de Earthdata y tiempos de espera largos.

    El fsspec que entrega earthaccess usa los tiempos por defecto de aiohttp y
    aborta en cuanto una peticion de rango tarda mas de la cuenta (FSTimeoutError).
    Aqui se construye el mismo sistema de archivos con el token de Earthdata y
    tiempos de espera de varios minutos por bloque.
    """
    import aiohttp
    import fsspec
    token = None
    try:
        token = auth.token.get("access_token")
    except Exception:
        pass
    espera = aiohttp.ClientTimeout(total=None, sock_connect=120, sock_read=600)
    if token:
        return fsspec.filesystem("https", headers={"Authorization": "Bearer " + token},
                                 client_kwargs={"timeout": espera})
    fs = earthaccess.get_fsspec_https_session()
    fs.client_kwargs = dict(getattr(fs, "client_kwargs", {}) or {}, timeout=espera)
    return fs


fs = sistema_de_archivos()
FRANJA = 256            # filas por peticion: peticiones cortas, reintentos baratos
INTENTOS = 4


def leer_por_franjas(ds, j0, j1, i0, i1):
    """Lee ds[j0:j1, i0:i1] en franjas de filas, reintentando cada franja."""
    salida = np.empty((j1 - j0, i1 - i0), dtype=ds.dtype)
    for a in range(j0, j1, FRANJA):
        b = min(a + FRANJA, j1)
        for intento in range(1, INTENTOS + 1):
            try:
                salida[a - j0:b - j0] = ds[a:b, i0:i1]
                break
            except Exception as e:      # FSTimeoutError, ClientError, OSError
                if intento == INTENTOS:
                    raise
                print("\n   reintento %d en filas %d-%d (%s)" % (intento, a, b, type(e).__name__),
                      flush=True)
                time.sleep(10 * intento)
    return salida

# tope de escenas por corrida, para poder desconectar el disco entre una y otra
TOPE = int(sys.argv[1]) if len(sys.argv) > 1 else len(GRANULOS)
hechas = 0

CAPAS = ["HHHH", "HVHV", "rtcGammaToSigmaFactor"]
META = ["science/LSAR/identification/orbitPassDirection",
        "science/LSAR/identification/productType",
        "science/LSAR/identification/zeroDopplerStartTime",
        GRUPO + "/listOfPolarizations", GRUPO + "/projection"]

for g in GRANULOS:
    fecha = g[43:51]
    salida = os.path.join(DESTINO, "NISAR_AOI_%s_%s.h5" % (fecha, g[27:32]))
    if os.path.exists(salida):
        print("ya esta:", fecha)
        continue
    if hechas >= TOPE:
        print("tope de %d escenas alcanzado; quedan pendientes desde %s" % (TOPE, fecha))
        break
    t0 = time.time()
    print("recortando", fecha, "...", end=" ", flush=True)
    try:
        fr = fs.open(BASE.format(g=g), "rb", block_size=8 * 2 ** 20, cache_type="readahead")
        h = h5py.File(fr, "r")
    except Exception as e:
        print("no se pudo abrir (%s); se salta, retomar despues" % type(e).__name__)
        continue
    with fr, h:
        gr = h[GRUPO]
        xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
        i0, i1 = np.searchsorted(xc, [X0, X1])
        j1, j0 = len(yc) - np.searchsorted(yc[::-1], [Y0, Y1])
        i0, i1, j0, j1 = max(i0, 0), min(i1, len(xc)), max(j0, 0), min(j1, len(yc))
        if i1 <= i0 or j1 <= j0:
            print("sin traslape con el AOI"); continue
        try:
            bloques = {capa: leer_por_franjas(gr[capa], j0, j1, i0, i1)
                       for capa in CAPAS if capa in gr}
        except Exception as e:
            print("fallo tras %d reintentos (%s); se salta, retomar despues"
                  % (INTENTOS, type(e).__name__))
            continue
        with h5py.File(salida + ".parcial", "w") as ho:
            go = ho.create_group(GRUPO)
            go.create_dataset("xCoordinates", data=xc[i0:i1])
            go.create_dataset("yCoordinates", data=yc[j0:j1])
            for capa, datos in bloques.items():
                go.create_dataset(capa, data=datos, compression="gzip", compression_opts=4)
            for ruta in META:
                if ruta in h:
                    ho.create_dataset(ruta, data=h[ruta][()])
                    for k, v in h[ruta].attrs.items():
                        ho[ruta].attrs[k] = v
            # angulo de incidencia: va en una malla gruesa de metadatos, pesa poco
            # y hace falta para estratificar el doble rebote (umbral de 35 grados)
            for ruta in ("science/LSAR/GCOV/metadata/radarGrid/incidenceAngle",
                         "science/LSAR/GCOV/metadata/radarGrid/xCoordinates",
                         "science/LSAR/GCOV/metadata/radarGrid/yCoordinates"):
                if ruta in h:
                    ho.create_dataset(ruta, data=h[ruta][()])
            ho.attrs["origen"] = g
            ho.attrs["ventana_utm18n"] = json.dumps([float(X0), float(X1), float(Y0), float(Y1)])
    os.replace(salida + ".parcial", salida)
    hechas += 1
    print("%.0f MB en %.1f min" % (os.path.getsize(salida) / 1e6, (time.time() - t0) / 60))
print("listo; corre 16_inventario_nisar.py")
