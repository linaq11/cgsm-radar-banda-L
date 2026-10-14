# -*- coding: utf-8 -*-
r"""Descarga las escenas NISAR GCOV Beta sobre el AOI que faltan en D:\TESIS_DATACUBE\NISAR.

Las seis escenas salieron de una consulta a CMR (NASA) el 2026-09-09 sobre la
envolvente del AOI. Cubren octubre de 2025 a enero de 2026, todas descendentes,
traza D_083, cuadro 011, HH+HV; las tres de diciembre de 2025 caen dentro del cubo.

AUTENTICACION. Earthdata exige usuario y contraseña. Este script NO los pide ni los
guarda: usa la libreria earthaccess, que lee las credenciales de ~/.netrc (o de
las variables EARTHDATA_USERNAME / EARTHDATA_PASSWORD) o abre el flujo de login
interactivo en la terminal del usuario. Ejecutar desde su terminal, no desde el agente.

USO
    pip install earthaccess --break-system-packages   (si no esta)
    python 17_descargar_nisar.py
"""
import os
import sys

DESTINO = r"D:\TESIS_DATACUBE\NISAR"
GRANULOS = [
    "NISAR_L2_PR_GCOV_004_011_D_083_4005_DHDH_A_20251029T232728_20251029T232806_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_006_011_D_083_4005_DHDH_A_20251122T232729_20251122T232806_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_007_011_D_083_4005_DHDH_A_20251204T232730_20251204T232807_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_008_011_D_083_4005_DHDH_A_20251216T232731_20251216T232808_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_009_011_D_083_4005_DHDH_A_20251228T232731_20251228T232808_X05009_N_F_J_001",
    "NISAR_L2_PR_GCOV_010_011_D_083_4005_DHDH_A_20260109T232732_20260109T232809_X05009_N_F_J_001",
]
BASE = "https://nisar.asf.earthdatacloud.nasa.gov/NISAR/NISAR_L2_GCOV_BETA_V1/{g}/{g}.h5"

if not os.path.isdir(DESTINO):
    sys.exit("ABORTA: D: desmontado")

try:
    import earthaccess
except ImportError:
    sys.exit("falta earthaccess: pip install earthaccess --break-system-packages")

auth = earthaccess.login()          # netrc, variables de entorno o login interactivo
if not auth.authenticated:
    sys.exit("sin sesion Earthdata")

sesion = earthaccess.get_requests_https_session()
for g in GRANULOS:
    ruta = os.path.join(DESTINO, g + ".h5")
    if os.path.exists(ruta) and os.path.getsize(ruta) > 1e8:
        print("ya esta:", g[:40])
        continue
    url = BASE.format(g=g)
    print("descargando", g[43:51], "...", end=" ", flush=True)
    with sesion.get(url, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(ruta + ".parcial", "wb") as f:
            for trozo in r.iter_content(chunk_size=1 << 20):
                f.write(trozo)
    os.replace(ruta + ".parcial", ruta)
    print("%.0f MB" % (os.path.getsize(ruta) / 1e6))
print("listo; ahora corre 16_inventario_nisar.py para verificar cobertura")
