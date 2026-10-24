# -*- coding: utf-8 -*-
r"""Recorte remoto de un producto NISAR L2 GSLC dual-pol (HH, HV, complex64, 5 m, UTM 18N) al AOI de la tesis, sin bajar los
24 GB del frame. Lee por franjas con earthaccess + fsspec + h5py (como 18_nisar_recorte_remoto.py para los GCOV) y escribe un
HDF5 con la misma estructura de grupos que polsartools.import_nisar_gslc espera (lee por GDAL):
  /science/LSAR/GSLC/grids/frequencyA/{HH, HV, mask, xCoordinates, yCoordinates, xCoordinateSpacing, yCoordinateSpacing,
   projection (con sus atributos), listOfPolarizations, centerFrequency}
  /science/LSAR/identification (copiado entero: atributos y escalares)
Ventana: AOI_tesis_CGSM_v1 en EPSG:32618 con 500 m de margen (14.505 x 12.204 px a 5 m; 2,8 GB por fecha en los dos canales).
Entorno: C:\LINA\TOOLS\polsar_env (importar h5py antes que osgeo). Credenciales: ~/.netrc.
USO: polsar_env/Scripts/python 01_recorte_gslc.py 20251204 [path]      (path 11 por defecto)
SALIDA: D:/TESIS_DATACUBE/NISAR_GSLC/NISAR_GSLC_<fecha>_P<path>_cgsm.h5
"""
import sys
import time
from pathlib import Path

import h5py
import numpy as np

FECHA = sys.argv[1]; PATH = int(sys.argv[2]) if len(sys.argv) > 2 else 11
SALIDA = Path("D:/TESIS_DATACUBE/NISAR_GSLC") if Path("D:/").exists() else Path("C:/LINA/NISAR_GSLC")   # D: es disco externo; si no está conectado, C: (55 GB libres)
SALIDA.mkdir(parents=True, exist_ok=True); print("salida:", SALIDA, flush=True)
AOI = "C:/LINA/UNAL 2626-1/AVANCE TESIS/AOI/AOI_tesis_CGSM_v1.geojson"; MARGEN = 500.0; FRANJA = 512
G = "science/LSAR/GSLC/grids/frequencyA"


def producto():
    import asf_search as asf
    from datetime import datetime, timedelta
    d0 = datetime.strptime(FECHA, "%Y%m%d"); r = asf.search(platform="NISAR", processingLevel="GSLC", start=(d0 - timedelta(days=1)).isoformat(), end=(d0 + timedelta(days=1)).isoformat(), intersectsWith="POINT(-74.42 10.85)")
    cand = [x for x in r if "QA_STATS" not in x.properties["fileName"] and x.properties.get("pathNumber") == PATH and FECHA in x.properties["fileName"]]
    assert cand, "sin producto GSLC para %s path %d" % (FECHA, PATH)
    cand.sort(key=lambda x: x.properties["fileName"]); p = cand[-1]; return p.properties["fileName"], p.properties["url"]


def ventana(x, y):
    import geopandas as gpd
    b = gpd.read_file(AOI).to_crs(32618).total_bounds
    j0, j1 = np.searchsorted(x, b[0] - MARGEN), np.searchsorted(x, b[2] + MARGEN)
    yd = -y                                                     # y decrece: buscar en el negativo
    i0, i1 = np.searchsorted(yd, -(b[3] + MARGEN)), np.searchsorted(yd, -(b[1] - MARGEN))
    return int(i0), int(i1), int(j0), int(j1)


def leer_por_franjas(ds, i0, i1, j0, j1, nombre):
    out = np.empty((i1 - i0, j1 - j0), dtype=ds.dtype); t0 = time.time()
    for a in range(i0, i1, FRANJA):
        b = min(a + FRANJA, i1)
        for intento in range(5):
            try:
                out[a - i0:b - i0] = ds[a:b, j0:j1]; break
            except Exception as e:
                print("   reintento %d en %s filas %d-%d: %s" % (intento + 1, nombre, a, b, str(e)[:80]), flush=True); time.sleep(10 * (intento + 1))
        else:
            raise RuntimeError("fallo persistente leyendo %s" % nombre)
        if ((a - i0) // FRANJA) % 4 == 0: print("   %s: %d de %d filas (%.0f s)" % (nombre, b - i0, i1 - i0, time.time() - t0), flush=True)
    return out


def main():
    import earthaccess
    earthaccess.login(strategy="netrc"); nombre, url = producto(); print("producto:", nombre, flush=True)
    fs = earthaccess.get_fsspec_https_session(); destino = SALIDA / ("NISAR_GSLC_%s_P%03d_cgsm.h5" % (FECHA, PATH))
    with fs.open(url, "rb", block_size=8 * 1024 * 1024) as f, h5py.File(f, "r") as h, h5py.File(str(destino) + ".parcial", "w") as ho:
        g = h[G]; x = g["xCoordinates"][:]; y = g["yCoordinates"][:]; i0, i1, j0, j1 = ventana(x, y)
        print("ventana: filas %d-%d, columnas %d-%d (%d x %d px)" % (i0, i1, j0, j1, i1 - i0, j1 - j0), flush=True)
        go = ho.require_group(G)
        for k in ("HH", "HV", "mask"):
            if k in g:
                arr = leer_por_franjas(g[k], i0, i1, j0, j1, k); d = go.create_dataset(k, data=arr, chunks=(512, 512), compression="gzip", compression_opts=1)
                for ak, av in g[k].attrs.items(): d.attrs[ak] = av
        go.create_dataset("xCoordinates", data=x[j0:j1]); go.create_dataset("yCoordinates", data=y[i0:i1])
        for k in ("xCoordinateSpacing", "yCoordinateSpacing", "projection", "listOfPolarizations", "centerFrequency", "numberOfSubSwaths", "azimuthBandwidth", "rangeBandwidth", "slantRangeSpacing"):
            if k in g:
                d = go.create_dataset(k, data=g[k][()])
                for ak, av in g[k].attrs.items(): d.attrs[ak] = av
        for ak, av in g.attrs.items(): go.attrs[ak] = av
        rg = "science/LSAR/GSLC/metadata/radarGrid"                      # polsartools lee la proyección aquí (get_geo_meta)
        if rg + "/projection" in h: h.copy(rg + "/projection", ho.require_group(rg), name="projection")
        else:
            dp = ho.require_group(rg).create_dataset("projection", data=np.int32(g["projection"][()]))
            for ak, av in g["projection"].attrs.items(): dp.attrs[ak] = av
        if "science/LSAR/identification" in h:
            h.copy("science/LSAR/identification", ho.require_group("science/LSAR"), name="identification")
        for ak, av in h.attrs.items(): ho.attrs[ak] = av
        ho.attrs["recorte"] = "AOI_tesis_CGSM_v1 + 500 m; filas %d-%d, columnas %d-%d del producto %s" % (i0, i1, j0, j1, nombre)
    Path(str(destino) + ".parcial").replace(destino); print("escrito:", destino, "%.2f GB" % (destino.stat().st_size / 1e9), flush=True)


if __name__ == "__main__":
    main()
