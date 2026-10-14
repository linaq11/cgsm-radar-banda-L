# -*- coding: utf-8 -*-
r"""Recorta NISAR GCOV sobre el manglar de Bahia de Malaga (Buenaventura), sitio de
contraste del trabajo de radar, leyendo el HDF5 remoto por rangos como en
18_nisar_recorte_remoto.py.

ESCENAS. De las 55 dual-pol que tocan el nucleo del manglar, solo dos trazas lo
cubren completo: la ascendente 004 (frame 4005, 12 fechas, 10:00 UTC = 05:00
local, archivos de 1,6 GB) y la descendente 087 (frame 4005, 12 fechas, 23:00 UTC
= 18:00 local, 6,6 GB). Las dos horas del dia dan estados de marea distintos, que es
el contraste que se busca. Van primero las ascendentes, por ser mas rapidas. La
lista con sus URL esta en nisar_pacifico_granulos.json (inventario CMR del
11-sep-2026); las Beta y las Provisional traen URL distintas y se usan tal cual.

AOI. Caja lon/lat -77.40, 3.80, -77.10, 4.10 mas 2 km de margen, transformada a la
proyeccion que declara cada producto (se lee del archivo, no se supone).

AUTENTICACION. earthaccess pregunta en la terminal; este script no maneja
contraseñas. Ejecutar desde la terminal del usuario.

USO
    python 23_nisar_recorte_pacifico.py        # todas las que falten
    python 23_nisar_recorte_pacifico.py 3      # como maximo tres escenas en esta corrida
"""
import json
import os
import sys
import time

import h5py
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
DESTINO = r"D:\TESIS_DATACUBE\NISAR_PACIFICO"
LISTA = os.path.join(AQUI, "nisar_pacifico_granulos.json")
AOI = (-77.40, 3.80, -77.10, 4.10)      # lon0, lat0, lon1, lat1
MARGEN_M = 2000
GRUPO = "science/LSAR/GCOV/grids/frequencyA"
TRAZAS = [("A", "004", "4005"), ("D", "087", "4005")]   # en este orden

if not os.path.isdir(r"D:\TESIS_DATACUBE"):
    sys.exit("ABORTA: D: desmontado")
os.makedirs(DESTINO, exist_ok=True)
try:
    import earthaccess
except ImportError:
    sys.exit("falta earthaccess: pip install earthaccess --break-system-packages")
from pyproj import Transformer

granulos = [g for g in json.load(open(LISTA, encoding="utf-8")) if g["url"]]
orden = []
for d, tr_, fr in TRAZAS:
    orden += sorted([g for g in granulos if (g["dir"], g["traza"], g["frame"]) == (d, tr_, fr)], key=lambda g: g["fecha"])
print("escenas en lista:", len(orden))

auth = earthaccess.login()
if not auth.authenticated:
    sys.exit("sin sesion Earthdata")


def sistema_de_archivos():
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
FRANJA = 256
INTENTOS = 4


def leer_por_franjas(ds, j0, j1, i0, i1):
    salida = np.empty((j1 - j0, i1 - i0), dtype=ds.dtype)
    for a in range(j0, j1, FRANJA):
        b = min(a + FRANJA, j1)
        for intento in range(1, INTENTOS + 1):
            try:
                salida[a - j0:b - j0] = ds[a:b, i0:i1]
                break
            except Exception as e:
                if intento == INTENTOS:
                    raise
                print("\n   reintento %d en filas %d-%d (%s)" % (intento, a, b, type(e).__name__), flush=True)
                time.sleep(10 * intento)
    return salida


def ventana(h):
    """Caja del AOI en la proyeccion del producto, leida del propio archivo."""
    epsg = None
    pr = h.get(GRUPO + "/projection")
    if pr is not None:
        for k in ("epsg_code", "spatial_ref", "epsg"):
            if k in pr.attrs:
                try:
                    epsg = int(pr.attrs[k]); break
                except (TypeError, ValueError):
                    pass
        if epsg is None:
            try:
                epsg = int(pr[()])
            except Exception:
                pass
    if epsg is None:
        epsg = 32618
    t = Transformer.from_crs("EPSG:4326", "EPSG:%d" % epsg, always_xy=True)
    xs, ys = [], []
    for lon in (AOI[0], AOI[2]):
        for lat in (AOI[1], AOI[3]):
            u, v = t.transform(lon, lat)
            xs.append(u); ys.append(v)
    return epsg, min(xs) - MARGEN_M, max(xs) + MARGEN_M, min(ys) - MARGEN_M, max(ys) + MARGEN_M


TOPE = int(sys.argv[1]) if len(sys.argv) > 1 else len(orden)
hechas = 0
CAPAS = ["HHHH", "HVHV", "rtcGammaToSigmaFactor"]
META = ["science/LSAR/identification/orbitPassDirection",
        "science/LSAR/identification/productType",
        "science/LSAR/identification/zeroDopplerStartTime",
        GRUPO + "/listOfPolarizations", GRUPO + "/projection"]

for g in orden:
    fecha = g["fecha"].replace("-", "")
    salida = os.path.join(DESTINO, "NISAR_MALAGA_%s_%s%s.h5" % (fecha, g["dir"], g["traza"]))
    if os.path.exists(salida):
        print("ya esta:", fecha, g["dir"] + g["traza"])
        continue
    if hechas >= TOPE:
        print("tope de %d escenas alcanzado; quedan pendientes desde %s" % (TOPE, fecha))
        break
    t0 = time.time()
    print("recortando", fecha, g["dir"] + g["traza"], "...", end=" ", flush=True)
    try:
        fr_ = fs.open(g["url"], "rb", block_size=8 * 2 ** 20, cache_type="readahead")
        h = h5py.File(fr_, "r")
    except Exception as e:
        print("no se pudo abrir (%s); se salta, retomar despues" % type(e).__name__)
        continue
    with fr_, h:
        gr = h[GRUPO]
        epsg, X0, X1, Y0, Y1 = ventana(h)
        xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
        i0, i1 = np.searchsorted(xc, [X0, X1])
        j1, j0 = len(yc) - np.searchsorted(yc[::-1], [Y0, Y1])
        i0, i1, j0, j1 = max(i0, 0), min(i1, len(xc)), max(j0, 0), min(j1, len(yc))
        if i1 <= i0 or j1 <= j0:
            print("sin traslape con el AOI (EPSG %d)" % epsg); continue
        try:
            bloques = {capa: leer_por_franjas(gr[capa], j0, j1, i0, i1) for capa in CAPAS if capa in gr}
        except Exception as e:
            print("fallo tras %d reintentos (%s); se salta, retomar despues" % (INTENTOS, type(e).__name__))
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
            for ruta in ("science/LSAR/GCOV/metadata/radarGrid/incidenceAngle",
                         "science/LSAR/GCOV/metadata/radarGrid/xCoordinates",
                         "science/LSAR/GCOV/metadata/radarGrid/yCoordinates"):
                if ruta in h:
                    ho.create_dataset(ruta, data=h[ruta][()])
            ho.attrs["origen"] = g["titulo"]
            ho.attrs["coleccion"] = g["col"]
            ho.attrs["epsg"] = epsg
            ho.attrs["ventana"] = json.dumps([float(X0), float(X1), float(Y0), float(Y1)])
    os.replace(salida + ".parcial", salida)
    hechas += 1
    print("%.0f MB en %.1f min" % (os.path.getsize(salida) / 1e6, (time.time() - t0) / 60))
print("listo")
