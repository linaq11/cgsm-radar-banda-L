# -*- coding: utf-8 -*-
"""Reúne en un solo Markdown todo lo redactado en los scripts: la cabecera (docstring) y los
comentarios de cada uno, en el orden del flujo de trabajo. Escribe DOCUMENTACION_scripts.md.

USO: python generar_documentacion.py
"""
import ast
import io
import os
import tokenize

AQUI = os.path.dirname(os.path.abspath(__file__))
ORDEN = [
    ("1. Acceso a datos", ["publicacion_gee/16_inventario_nisar.py", "publicacion_gee/17_descargar_nisar.py", "publicacion_gee/18_nisar_recorte_remoto.py",
                           "publicacion_gee/23_nisar_recorte_pacifico.py", "publicacion_gee/24_nisar_recorte_cgsm.py", "nivel_ideam_descarga.py"]),
    ("2. Preprocesamiento y calibración", ["publicacion_gee/20_nisar_incidencia.py", "alos2_marea_malaga.py", "s1_marea_malaga.py"]),
    ("3. Coberturas de referencia y muestreo", ["perfil_pacifico.py", "perfil_pacifico_24.py", "doble_rebote_incidencia.py", "figuras_cgsm.py", "figuras_pacifico.py", "figuras_gee.py", "figura_sitios.py"]),
    ("4. Forzante hidrológico", ["mareas_buenaventura.py", "mareas_dimar_a_serie.py", "marea_vs_radar.py", "cgsm_nivel_rio.py"]),
    ("5 y 6. Estadística por pasada y prueba hidrológica", ["cgsm_temporada.py", "figura_cgsm_optico.py", "figuras_informe.py"]),
    ("7. Robustez y límites", ["autocorrelacion_temporal.py", "figura_incidencia.py"]),
    ("8. Clave de interpretación", ["figura_clave.py", "nisar_flotante.py", "clave_vs_muestra2025.py"]),
    ("9. Mapa y corroboración óptica", ["mapa_doble_rebote.py", "mapa_doble_rebote_s1.py", "mapa_doble_rebote_malaga.py", "corroboracion_dw.py", "mapbiomas_cruce.py"]),
    ("Informe y figuras de método", ["md_a_word.py", "propuesta_a_word.py", "construir_informe.py", "figura_flujo.py", "figura_cadena_sar.py", "figura_muestra_2025.py", "figura_consistencia.py"]),
]


def cabecera_y_comentarios(ruta):
    src = open(ruta, encoding="utf-8").read()
    doc = ast.get_docstring(ast.parse(src)) or "(sin cabecera)"
    coms = []
    for tok in tokenize.generate_tokens(io.StringIO(src).readline):
        if tok.type == tokenize.COMMENT and not tok.string.startswith("# -*-"):
            coms.append((tok.start[0], tok.string.lstrip("# ").rstrip()))
    return doc, coms


salida = ["# Documentación de los scripts", "", "Cabecera y comentarios de cada script, extraídos del código con `generar_documentacion.py`, en el orden del flujo de trabajo del informe. Cada cabecera dice qué hace el script, qué lee, qué escribe y cómo se corre.", "", "## Convenciones de redacción", "", "- script, no guion, para los archivos de Python.", "- bosque no inundable de referencia, no bosque de control, al describir el método.", "- forzante hidrológico, para coincidir con el informe.", "- diferencia HH − HV o VV − VH, nunca cociente.", "- contraste óptico para Dynamic World, no corroboración ni validación de la inundación bajo dosel.", "- señal compatible con doble rebote o respuesta copolar asociada al estado hidrológico; una imagen de intensidad no identifica por sí sola el mecanismo.", "- la diferencia manglar − bosque controla variaciones temporales compartidas; no se afirma que elimine la estacionalidad.", "- el nivel de Remolino es un indicador regional del estado hidrológico, no una medida del nivel dentro del manglar.", ""]
vistos = set()
for etapa, lista in ORDEN:
    salida += ["## " + etapa, ""]
    for f in lista:
        ruta = os.path.join(AQUI, "scripts", f)
        if not os.path.exists(ruta):
            continue
        vistos.add(f)
        doc, coms = cabecera_y_comentarios(ruta)
        salida += ["### `%s`" % f, "", doc.strip(), ""]
        if coms:
            salida += ["Comentarios en el código:", ""] + ["- línea %d: %s" % (n, c) for n, c in coms] + [""]
faltan = [f for f in sorted(os.listdir(os.path.join(AQUI, "scripts"))) if f.endswith(".py") and f not in vistos]
if faltan:
    salida += ["## Otros", ""]
    for f in faltan:
        doc, coms = cabecera_y_comentarios(os.path.join(AQUI, "scripts", f))
        salida += ["### `%s`" % f, "", doc.strip(), ""] + (["Comentarios en el código:", ""] + ["- línea %d: %s" % (n, c) for n, c in coms] + [""] if coms else [])
open(os.path.join(AQUI, "DOCUMENTACION_scripts.md"), "w", encoding="utf-8", newline="\n").write("\n".join(salida))
print("DOCUMENTACION_scripts.md:", len(vistos) + len(faltan), "scripts,", sum(len(x.split()) for x in salida), "palabras")
