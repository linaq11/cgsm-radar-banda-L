# -*- coding: utf-8 -*-
r"""Recorta las escenas NISAR GCOV que faltan sobre la CGSM (las 11 Provisional de
jun-sep 2026, de las que 3 ya estan completas en disco), con el mismo metodo de
18_nisar_recorte_remoto.py y 23_nisar_recorte_pacifico.py: lectura remota por rangos
de la ventana del AOI (extension del cubo + 2 km), proyeccion leida del producto.

Lista con URL en nisar_cgsm_granulos.json (inventario CMR del 12-sep-2026): 6 Beta
(D083, ya recortadas como NISAR_AOI_<fecha>_083_4.h5) y 11 Provisional: 6 de la traza
descendente D083 (18:29 local) y 5 de la ascendente A007 (nueva sobre la CGSM). Se
saltan las fechas que ya esten en disco con cualquiera de los dos nombres.

AUTENTICACION: earthaccess pregunta en la terminal. Ejecutar desde la terminal del usuario.

USO
    python 24_nisar_recorte_cgsm.py        # todas las que falten
    python 24_nisar_recorte_cgsm.py 3      # como maximo tres en esta corrida
"""
import glob
import json
import os
import sys
import time

import h5py
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
DESTINO = r"D:\TESIS_DATACUBE\NISAR"
ZARR = r"D:\TESIS_DATACUBE\cgsm_cube.zarr"
LISTA = os.path.join(AQUI, "nisar_cgsm_granulos.json")
MARGEN_M = 2000
GRUPO = "science/LSAR/GCOV/grids/frequencyA"

if not os.path.isdir(DESTINO):
    sys.exit("ABORTA: D: desmontado")
try:
    import earthaccess
except ImportError:
    sys.exit("falta earthaccess: pip install earthaccess --break-system-packages")
from pyproj import Transformer

at = json.load(open(os.path.join(ZARR, "zarr.json"), encoding="utf-8"))["attributes"]
tr = at["transform"]
alto, ancho = 6022, 7150
esq = [(tr[2], tr[5]), (tr[2] + ancho * 10, tr[5]), (tr[2], tr[5] - alto * 10), (tr[2] + ancho * 10, tr[5] - alto * 10)]

granulos = sorted([g for g in json.load(open(LISTA, encoding="utf-8")) if g["url"]], key=lambda g: g["fecha"])
fechas_en_disco = {os.path.basename(f)[10:18] for f in glob.glob(os.path.join(DESTINO, "NISAR_AOI_*.h5"))}
pendientes = [g for g in granulos if g["fecha"].replace("-", "") not in fechas_en_disco]
print("en disco: %d fechas | pendientes: %d -> %s" % (len(fechas_en_disco), len(pendientes), [g["fecha"] + " " + g["dir"] + g["traza"] for g in pendientes]))

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
        return fsspec.filesystem("https", headers={"Authorization": "Bearer " + token}, client_kwargs={"timeout": espera})
    fs = earthaccess.get_fsspec_https_session()
    fs.client_kwargs = dict(getattr(fs, "client_kwargs", {}) or {}, timeout=espera)
    return fs


fs = sistema_de_archivos()
FRANJA, INTENTOS = 256, 4


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
    t = Transformer.from_crs("EPSG:9377", "EPSG:%d" % epsg, always_xy=True)
    xs, ys = zip(*[t.transform(x, y) for x, y in esq])
    return epsg, min(xs) - MARGEN_M, max(xs) + MARGEN_M, min(ys) - MARGEN_M, max(ys) + MARGEN_M


TOPE = int(sys.argv[1]) if len(sys.argv) > 1 else len(pendientes)
CAPAS = ["HHHH", "HVHV", "rtcGammaToSigmaFactor"]
META = ["science/LSAR/identification/orbitPassDirection", "science/LSAR/identification/productType",
        "science/LSAR/identification/zeroDopplerStartTime", GRUPO + "/listOfPolarizations", GRUPO + "/projection"]
hechas = 0
for g in pendientes:
    if hechas >= TOPE:
        print("tope de %d escenas alcanzado" % TOPE)
        break
    fecha = g["fecha"].replace("-", "")
    salida = os.path.join(DESTINO, "NISAR_AOI_%s_%s%s.h5" % (fecha, g["dir"], g["traza"]))
    t0 = time.time()
    print("recortando", fecha, g["dir"] + g["traza"], "...", end=" ", flush=True)
    try:
        fr_ = fs.open(g["url"], "rb", block_size=8 * 2 ** 20, cache_type="readahead")
        h = h5py.File(fr_, "r")
    except Exception as e:
        print("no se pudo abrir (%s); se salta" % type(e).__name__)
        continue
    with fr_, h:
        gr = h[GRUPO]
        epsg, X0, X1, Y0, Y1 = ventana(h)
        xc, yc = gr["xCoordinates"][:], gr["yCoordinates"][:]
        i0, i1 = np.searchsorted(xc, [X0, X1])
        j1, j0 = len(yc) - np.searchsorted(yc[::-1], [Y0, Y1])
        i0, i1, j0, j1 = max(i0, 0), min(i1, len(xc)), max(j0, 0), min(j1, len(yc))
        if i1 <= i0 or j1 <= j0:
            print("sin traslape"); continue
        try:
            bloques = {capa: leer_por_franjas(gr[capa], j0, j1, i0, i1) for capa in CAPAS if capa in gr}
        except Exception as e:
            print("fallo tras %d reintentos (%s); se salta" % (INTENTOS, type(e).__name__))
            continue
        with h5py.File(salida + ".parcial", "w") as ho:
            go = ho.create_group(GRUPO)
            go.create_dataset("xCoordinates", data=xc[i0:i1]); go.create_dataset("yCoordinates", data=yc[j0:j1])
            for capa, datos in bloques.items():
                go.create_dataset(capa, data=datos, compression="gzip", compression_opts=4)
            for ruta in META:
                if ruta in h:
                    ho.create_dataset(ruta, data=h[ruta][()])
                    for k, v in h[ruta].attrs.items():
                        ho[ruta].attrs[k] = v
            for ruta in ("science/LSAR/GCOV/metadata/radarGrid/incidenceAngle", "science/LSAR/GCOV/metadata/radarGrid/xCoordinates",
                         "science/LSAR/GCOV/metadata/radarGrid/yCoordinates"):
                if ruta in h:
                    ho.create_dataset(ruta, data=h[ruta][()])
            ho.attrs["origen"] = g["titulo"]; ho.attrs["coleccion"] = g["col"]; ho.attrs["epsg"] = epsg
            ho.attrs["ventana"] = json.dumps([float(X0), float(X1), float(Y0), float(Y1)])
    os.replace(salida + ".parcial", salida)
    hechas += 1
    print("%.0f MB en %.1f min" % (os.path.getsize(salida) / 1e6, (time.time() - t0) / 60))
print("listo")
