# -*- coding: utf-8 -*-
r"""Recorte remoto de un producto NISAR L2 GSLC dual-pol (HH, HV, complex64, 5 m, UTM 18N) al AOI de la tesis, sin bajar los
24 GB del frame. Lee por franjas con earthaccess + fsspec + h5py (como 18_nisar_recorte_remoto.py para los GCOV) y escribe un
HDF5 con la misma estructura de grupos que polsartools.import_nisar_gslc espera (lee por GDAL):
  /science/LSAR/GSLC/grids/frequencyA/{HH, HV, mask, xCoordinates, yCoordinates, xCoordinateSpacing, yCoordinateSpacing,
   projection (con sus atributos), listOfPolarizations, centerFrequency}
  /science/LSAR/identification (copiado entero: atributos y escalares)
Ventana: AOI_tesis_CGSM_v1 en EPSG:32618 con 500 m de margen (14.505 x 12.204 px a 5 m; 2,8 GB por fecha en los dos canales).
Reanudable: cada canal (HH, HV, mask) se escribe en el .parcial al terminar; si el .parcial existe, los canales completos se
saltan. Cada franja tiene un tiempo máximo (TIMEOUT s); si se agota, se reabre la conexión y se reintenta.
Entorno: C:\LINA\TOOLS\polsar_env (importar h5py antes que osgeo). Credenciales: ~/.netrc.
USO: polsar_env/Scripts/python 01_recorte_gslc.py 20251204 [path]      (path 11 por defecto)
SALIDA: <NISAR_BASE o D:/TESIS_DATACUBE/NISAR_GSLC o C:/LINA/NISAR_GSLC>/NISAR_GSLC_<fecha>_P<path>_cgsm.h5
"""
import os
import sys
import threading
import time
from pathlib import Path

import h5py
import numpy as np

FECHA = sys.argv[1]; PATH = int(sys.argv[2]) if len(sys.argv) > 2 else 11
SALIDA = Path(os.environ["NISAR_BASE"]) if os.environ.get("NISAR_BASE") else (Path("D:/TESIS_DATACUBE/NISAR_GSLC") if Path("D:/").exists() else Path("C:/LINA/NISAR_GSLC"))   # D: es disco externo; si no está conectado, C: (55 GB libres)
SALIDA.mkdir(parents=True, exist_ok=True); print("salida:", SALIDA, flush=True)
AOI = "C:/LINA/UNAL 2626-1/AVANCE TESIS/AOI/AOI_tesis_CGSM_v1.geojson"; MARGEN = 500.0; FRANJA = 512; TIMEOUT = 240
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


class Remoto:
    """Conexión al producto remoto que se puede reabrir cuando una lectura se cuelga."""
    def __init__(self, fs, url): self.fs, self.url, self.f, self.h = fs, url, None, None; self.abrir()
    def abrir(self):
        self.cerrar(); self.f = self.fs.open(self.url, "rb", block_size=8 * 1024 * 1024); self.h = h5py.File(self.f, "r"); self.g = self.h[G]
    def cerrar(self):
        for o in (self.h, self.f):
            try:
                if o is not None: o.close()
            except Exception: pass
    def leer(self, k, a, b, j0, j1):
        """Lee ds[a:b, j0:j1] con tiempo máximo; si se agota, reabre y lanza TimeoutError."""
        res = {}
        def tarea():
            try: res["v"] = self.g[k][a:b, j0:j1]
            except Exception as e: res["e"] = e
        t = threading.Thread(target=tarea, daemon=True); t.start(); t.join(TIMEOUT)
        if t.is_alive():
            try: self.f.close()          # cierra la conexión bloqueada para que la lectura colgada falle
            except Exception: pass
            self.abrir(); raise TimeoutError("franja %d-%d de %s sin respuesta en %d s" % (a, b, k, TIMEOUT))
        if "e" in res: raise res["e"]
        return res["v"]


ULTIMO = {"t": time.time()}


def vigilante():
    """Si ninguna franja termina en SIN_PROGRESO s, el proceso sale con código 3 y el bucle externo lo relanza (es reanudable)."""
    while True:
        time.sleep(30)
        if time.time() - ULTIMO["t"] > SIN_PROGRESO:
            print("VIGILANTE: %d s sin progreso, salgo con código 3 para relanzar" % SIN_PROGRESO, flush=True); os._exit(3)


SIN_PROGRESO = 600


def leer_por_franjas(rem, k, i0, i1, j0, j1):
    out = np.empty((i1 - i0, j1 - j0), dtype=rem.g[k].dtype); t0 = time.time()
    for a in range(i0, i1, FRANJA):
        b = min(a + FRANJA, i1); ULTIMO["t"] = time.time()
        for intento in range(6):
            try:
                out[a - i0:b - i0] = rem.leer(k, a, b, j0, j1); break
            except Exception as e:
                print("   reintento %d en %s filas %d-%d: %s" % (intento + 1, k, a, b, str(e)[:80]), flush=True); time.sleep(10 * (intento + 1))
                if intento >= 1: rem.abrir()
        else:
            raise RuntimeError("fallo persistente leyendo %s" % k)
        if ((a - i0) // FRANJA) % 4 == 0: print("   %s: %d de %d filas (%.0f s)" % (k, b - i0, i1 - i0, time.time() - t0), flush=True)
    return out


def main():
    import earthaccess
    earthaccess.login(strategy="netrc"); nombre, url = producto(); print("producto:", nombre, flush=True)
    fs = earthaccess.get_fsspec_https_session(); destino = SALIDA / ("NISAR_GSLC_%s_P%03d_cgsm.h5" % (FECHA, PATH)); parcial = Path(str(destino) + ".parcial")
    threading.Thread(target=vigilante, daemon=True).start()
    rem = Remoto(fs, url); g = rem.g; x = g["xCoordinates"][:]; y = g["yCoordinates"][:]; i0, i1, j0, j1 = ventana(x, y)
    print("ventana: filas %d-%d, columnas %d-%d (%d x %d px)" % (i0, i1, j0, j1, i1 - i0, j1 - j0), flush=True)
    with h5py.File(str(parcial), "a") as ho:
        go = ho.require_group(G)
        for k in ("HH", "HV", "mask"):
            if k not in g: continue
            if k in go and go[k].shape == (i1 - i0, j1 - j0): print("   %s ya estaba en el parcial, se salta" % k, flush=True); continue
            if k in go: del go[k]
            arr = leer_por_franjas(rem, k, i0, i1, j0, j1); d = go.create_dataset(k, data=arr, chunks=(512, 512), compression="gzip", compression_opts=1)
            for ak, av in g[k].attrs.items(): d.attrs[ak] = av
            ho.flush(); del arr
        g = rem.g; h = rem.h
        for k in ("xCoordinates", "yCoordinates"):
            if k in go: del go[k]
        go.create_dataset("xCoordinates", data=x[j0:j1]); go.create_dataset("yCoordinates", data=y[i0:i1])
        for k in ("xCoordinateSpacing", "yCoordinateSpacing", "projection", "listOfPolarizations", "centerFrequency", "numberOfSubSwaths", "azimuthBandwidth", "rangeBandwidth", "slantRangeSpacing"):
            if k in g:
                if k in go: del go[k]
                d = go.create_dataset(k, data=g[k][()])
                for ak, av in g[k].attrs.items(): d.attrs[ak] = av
        for ak, av in g.attrs.items(): go.attrs[ak] = av
        rg = "science/LSAR/GSLC/metadata/radarGrid"                      # polsartools lee la proyección aquí (get_geo_meta)
        if rg in ho and "projection" in ho[rg]: del ho[rg]["projection"]
        if rg + "/projection" in h: h.copy(rg + "/projection", ho.require_group(rg), name="projection")
        else:
            dp = ho.require_group(rg).create_dataset("projection", data=np.int32(g["projection"][()]))
            for ak, av in g["projection"].attrs.items(): dp.attrs[ak] = av
        if "science/LSAR/identification" in ho: del ho["science/LSAR/identification"]
        if "science/LSAR/identification" in h:
            h.copy("science/LSAR/identification", ho.require_group("science/LSAR"), name="identification")
        for ak, av in h.attrs.items(): ho.attrs[ak] = av
        ho.attrs["recorte"] = "AOI_tesis_CGSM_v1 + 500 m; filas %d-%d, columnas %d-%d del producto %s" % (i0, i1, j0, j1, nombre)
    rem.cerrar(); parcial.replace(destino); print("escrito:", destino, "%.2f GB" % (destino.stat().st_size / 1e9), flush=True)


if __name__ == "__main__":
    main()
