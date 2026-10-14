# -*- coding: utf-8 -*-
"""Ensambla el informe HTML autocontenido incrustando las figuras en base64.

Lee plantilla_informe.html (con marcadores {{IMG:archivo}}) y escribe
informe_radar.html con las imagenes embebidas como data URI.
"""
import base64
import io
import os
import re

BASE = "C:/LINA/UNAL 2626-1/RADAR"
FIG = os.path.join(BASE, "figuras")
PLANTILLA = os.path.join(BASE, "plantilla_informe.html")
SALIDA = os.path.join(BASE, "informe_radar.html")

MIME = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png"}


def incrustar(m):
    nombre = m.group(1).strip()
    ruta = os.path.join(FIG, nombre)
    if not os.path.exists(ruta):
        raise SystemExit("FALTA la figura: " + ruta)
    ext = os.path.splitext(nombre)[1].lower()
    with open(ruta, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return "data:%s;base64,%s" % (MIME[ext], b64)


def main():
    html = io.open(PLANTILLA, encoding="utf-8").read()
    n = len(re.findall(r"\{\{IMG:([^}]+)\}\}", html))
    html = re.sub(r"\{\{IMG:([^}]+)\}\}", incrustar, html)
    io.open(SALIDA, "w", encoding="utf-8").write(html)
    print("escrito:", SALIDA)
    print("figuras incrustadas:", n)
    print("tamano: %.2f MB" % (os.path.getsize(SALIDA) / 1e6))


if __name__ == "__main__":
    main()
