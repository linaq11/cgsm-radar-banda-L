# -*- coding: utf-8 -*-
r"""Inserta en Avance_proyecto_radar.md la reproducción del cuaderno PolSAR dual-pol de NISAR en la CGSM: método 2.9, resultados
3.10 (Tablas 13 y 14, Figuras 19 a 23), una frase en trabajo futuro, la fila de la Tabla A1 y las referencias nuevas. Copia las
figuras a RADAR/. Idempotente: si ya existe "### 2.9 Polarimetría" no hace nada.
USO: python -X utf8 05_insertar_en_informe.py
"""
import shutil
from pathlib import Path

AQUI = Path(__file__).resolve().parent; RADAR = AQUI.parent; MD = RADAR / "Avance_proyecto_radar.md"
s = MD.read_text(encoding="utf-8")
if "### 2.9 Polarimetría" in s: raise SystemExit("ya insertado")
for f in sorted((AQUI / "figuras").glob("fig_polsar_*.png")): shutil.copy(f, RADAR / f.name)

METODO = """### 2.9 Polarimetría dual-pol de NISAR: entropía, ángulo alfa y DpRVI

Como complemento a la retrodispersión por canal, se reprodujo en la CGSM el flujo polarimétrico dual-pol del cuaderno de NISAR para Guaviare (ASF OpenSARlab, s. f.), con el producto GSLC de nivel 2 (HH y HV en geometría geocodificada, 5 m) en lugar del GCOV. Se usaron dos adquisiciones de la trayectoria descendente 11 (4 y 16 de diciembre de 2025), recortadas de forma remota a la AOI con earthaccess y h5py (12.204 por 14.505 píxeles, 1,8 GB por fecha). El procesamiento siguió el cuaderno sin cambios de método, con la biblioteca polsartools 0.13 (Bhogapurapu, s. f.) en un entorno de Python 3.12: matriz de covarianza C2 con 2 por 2 looks (10 m), filtro de Lee refinado de 7 por 7 (Lee et al., 1999), compuesto RGB dual-pol, descomposición H/alfa de los autovalores de C2 (Cloude y Pottier, 1997) e índice de vegetación dual-pol DpRVI (Mandal et al., 2020). Las capas se remuestrearon por interpolación bilineal a la malla de 10 m del cubo óptico de la tesis (EPSG:9377) y se extrajeron en los 880 puntos de la muestra de referencia ampliada, en el píxel y en la media de 3 por 3.

Los contrastes se preregistraron antes de procesar (`PLAN_polsar_nisar_cgsm.md`, sección 4). La prueba primaria P1 compara el bosque muerto en pie, definido por fracción de copa menor del 20 % con troncos visibles en la interpretación de 2026, con la herbácea sin troncos, mediante el AUC orientado de alfa, con H y DpRVI como secundarias; la hipótesis preregistrada fue alfa mayor en el bosque muerto por el doble rebote de los troncos. P2 mide la correlación de Spearman entre DpRVI y el punto medio de la caja de fracción de copa en los 436 puntos interpretados, con el RMSE fuera de muestra de una regresión lineal por bloques. P3 deriva un mapa manglar / no manglar con un umbral no supervisado de Otsu sobre DpRVI y lo compara con las clases v1.1, con la macro-F1 por bloque de 12 km y con la misma dicotomía del mapa óptico de la cadena de la tesis. Los intervalos son bootstrap de 2.000 repeticiones, la p de P1 es de permutación por bloques y los tres contrastes se corrigen con Holm. La segunda fecha se procesó como réplica, con la estabilidad punto a punto entre fechas como control adicional.

"""

RESULTADO = """### 3.10 Polarimetría dual-pol: entropía, ángulo alfa y DpRVI en la CGSM

El compuesto RGB dual-pol separa de inmediato el agua, el manglar y la planicie herbácea (Figura 19). El manglar intacto del occidente de la ciénaga aparece con HH y HV altos y la herbácea de Pajarales con HH alto y HV bajo; la imagen PlanetScope del mismo día, con los cúmulos propios de diciembre, y el compuesto Sentinel-2 de la estación seca confirman la disposición de las coberturas. En la ventana de detalle, la entropía y el ángulo alfa son altos en el manglar intacto y bajos en la planicie herbácea y en el manglar muerto, y el DpRVI reproduce el mismo contraste (Figura 20).

![Figura 19. Compuesto RGB dual-pol de NISAR (R = HH, G = HV, B = HH − HV, en dB) del 16 de diciembre de 2025 sobre la AOI y sobre una ventana de 16 km en Pajarales y el manglar occidental, con PlanetScope del mismo día y Sentinel-2 de la estación seca de 2025 como referencia óptica.](fig_polsar_1_rgb.png)

![Figura 20. Entropía H, ángulo alfa y DpRVI de NISAR del 16 de diciembre de 2025 (Lee refinado 7 por 7, 10 m) en la ventana de detalle, con el infrarrojo color de Sentinel-2 y los puntos de la muestra de referencia.](fig_polsar_2_h_alfa_dprvi.png)

En el plano H/alfa, los píxeles de la AOI y los 880 puntos ocupan una sola banda curva, con alfa entre 5 y 40 grados, propia de un sistema dual-pol de L sin la fase cruzada completa (Figura 21). Las clases se ordenan a lo largo de esa banda: humedal herbáceo y manglar degradado en el extremo de baja entropía y alfa bajo, manglar intacto y vegetación flotante en el centro y agua en el extremo alto (Tabla 14). El orden es idéntico en las dos fechas, y los valores punto a punto se correlacionan entre el 4 y el 16 de diciembre con rho de Spearman de 0,97 en HH y HV, 0,85 en H y DpRVI y 0,80 en alfa.

![Figura 21. Plano H/alfa dual-pol de las dos fechas: densidad de píxeles de la AOI en gris, puntos de la muestra con la media de 3 por 3 y medianas por clase v1.3 en círculos grandes.](fig_polsar_3_plano.png)

Tabla 14. Medianas por clase v1.3 de los descriptores polarimétricos (media de 3 por 3) en los 880 puntos, NISAR del 16 de diciembre de 2025.

| Clase | n | HH (dB) | HV (dB) | H | Alfa (°) | DpRVI |
|---|---|---|---|---|---|---|
| Agua | 241 | −18,5 | −24,8 | 0,68 | 19,6 | 0,48 |
| Humedal herbáceo | 120 | −6,6 | −16,2 | 0,44 | 11,8 | 0,26 |
| Manglar degradado | 134 | −7,4 | −16,9 | 0,47 | 12,0 | 0,28 |
| Manglar intacto | 182 | −8,5 | −15,9 | 0,61 | 16,6 | 0,41 |
| Otro | 69 | −10,1 | −18,5 | 0,58 | 15,4 | 0,38 |
| Vegetación flotante | 134 | −15,5 | −23,2 | 0,60 | 16,7 | 0,40 |

Los contrastes preregistrados dieron el mismo resultado en las dos fechas (Tabla 13). En P1, el bosque muerto en pie no tiene alfa mayor que la herbácea sino menor: el AUC orientado en la dirección preregistrada fue 0,33 y 0,34, con p de permutación de 0,999, de modo que la hipótesis del doble rebote de los troncos queda refutada. En la dirección contraria, exploratoria, alfa separa bosque muerto de herbácea con AUC de 0,67 [0,60 a 0,73] y 0,66 [0,59 a 0,73], H con 0,69 y DpRVI con 0,69 en las dos fechas, y HH con 0,67 y 0,66, con el bosque muerto más brillante en HH. Las firmas por clase muestran el mismo patrón (Figura 22): el manglar degradado, que la interpretación de 2026 identifica como bosque muerto en pie, se parece al humedal herbáceo en los cinco descriptores y se aleja del manglar intacto en H, alfa y DpRVI. En banda L dual-pol, el bosque muerto se comporta por tanto como una superficie, con dispersión dominada por un solo mecanismo y poca despolarización, y no como un volumen ni como un reflector diedro.

Tabla 13. Contrastes preregistrados de la polarimetría dual-pol de NISAR en las dos fechas, en el píxel de 10 m; entre corchetes, intervalos bootstrap del 95 %. P1 se reporta en la dirección observada (bosque muerto menor que herbácea en alfa, H y DpRVI; mayor en HH), contraria a la preregistrada.

| Prueba | Variable | 4 de diciembre | 16 de diciembre |
|---|---|---|---|
| P1, AUC bosque muerto (n = 194) frente a herbácea sin troncos (n = 82) | Alfa | 0,67 [0,60 a 0,73] | 0,66 [0,59 a 0,73] |
| | H | 0,69 [0,62 a 0,75] | 0,69 [0,62 a 0,75] |
| | DpRVI | 0,69 [0,63 a 0,75] | 0,69 [0,63 a 0,75] |
| | HH | 0,67 [0,61 a 0,74] | 0,66 [0,60 a 0,73] |
| | HV | 0,59 [0,51 a 0,66] | 0,55 [0,47 a 0,62] |
| P2, Spearman DpRVI frente a fracción de copa (n = 436) | DpRVI | 0,55 [0,48 a 0,62] | 0,56 [0,49 a 0,62] |
| P2, RMSE fuera de muestra de la fracción de copa (puntos porcentuales) | DpRVI | 31,4 | 31,5 |
| P3, macro-F1 manglar / no manglar, umbral de Otsu sobre DpRVI | DpRVI | 0,57 [0,49 a 0,60] | 0,55 [0,48 a 0,57] |
| P3, referencia óptica (unión v1.1, fuera de muestra) | RF, 94 variables | 0,65 | 0,65 |

![Figura 22. Firmas polarimétricas por clase v1.3 en los 880 puntos (media de 3 por 3; cajas de cuartiles sin valores extremos), 4 de diciembre en claro y 16 de diciembre en oscuro.](fig_polsar_4_firmas.png)

En P2, el DpRVI sigue la fracción de copa leñosa con rho de 0,55 y 0,56, significativa tras Holm, pero el error de una regresión lineal fuera de muestra es de 31 puntos porcentuales, del tamaño de las cajas de interpretación, por lo que el índice ordena la densidad de copa sin estimarla. En P3, el umbral de Otsu (DpRVI de 0,31) separa manglar de no manglar con macro-F1 de 0,57 y 0,55 por bloque, por debajo del 0,65 del mapa óptico; sobre toda la AOI, el mapa radar coincide con el óptico en el 64 % de los píxeles de manglar, humedal y otro, con 18 % de manglar solo óptico y 18 % solo radar (Figura 23). El desacuerdo se concentra en el manglar degradado, del que el radar clasifica como bosque solo el 32 %, y en la herbácea, con 51 %; el agua, con 98 % de píxeles sobre el umbral por la despolarización de la señal cercana al piso de ruido en HV, exige una máscara previa que el DpRVI por sí solo no aporta. La sensibilidad a la media de 3 por 3 movió los AUC de P1 entre 0,00 y 0,02 y P2 a 0,57 en las dos fechas.

![Figura 23. Manglar por umbral de Otsu sobre el DpRVI de NISAR (16 de diciembre de 2025) frente al mapa óptico píxel de 2025 de la cadena de la tesis, sobre la AOI, y fracción de píxeles clasificados como bosque por el radar en cada clase del mapa óptico.](fig_polsar_5_acuerdo.png)

"""

FUTURO = " La polarimetría dual-pol (sección 3.10) deja dos tareas: la sensibilidad a la órbita, con el par del 4 y el 8 de julio de 2026 de las trayectorias ascendente 119 y descendente 11, y el contraste punto a punto con PlanetScope del 16 de diciembre, que coincide con la segunda adquisición."

FILA_A1 = "| 10. Polarimetría dual-pol | `polsar_nisar/01_recorte_gslc`, `02_procesar_polsar`, `03_contrastes`, `04_figuras_cuaderno` | Tablas 13 y 14; Figuras 19 a 23; `polsar_puntos_<fecha>_P011.csv`, `contrastes_<fecha>_P011.csv`; capas H, alfa, DpRVI, HH y HV a 10 m |\n"

REFS = {
    "ASF OpenSARlab": "ASF OpenSARlab (s. f.). *NISAR Cookbook: GSLC basic polarimetric techniques with PolSARtools*. Alaska Satellite Facility. https://asfopensarlab.github.io/NISAR_Cookbook/gslc-basic-polsartools/",
    "Bhogapurapu": "Bhogapurapu, N. (s. f.). *polsartools* (versión 0.13) [Software]. https://github.com/Narayana-Rao/polsartools",
    "Cloude": "Cloude, S. R. y Pottier, E. (1997). An entropy based classification scheme for land applications of polarimetric SAR. *IEEE Transactions on Geoscience and Remote Sensing, 35*(1), 68–78. https://doi.org/10.1109/36.551935",
    "Lee, J.-S.": "Lee, J.-S., Grunes, M. R. y de Grandi, G. (1999). Polarimetric SAR speckle filtering and its implication for classification. *IEEE Transactions on Geoscience and Remote Sensing, 37*(5), 2363–2373. https://doi.org/10.1109/36.789635",
    "Mandal": "Mandal, D., Kumar, V., Ratha, D., Dey, S., Bhattacharya, A., Lopez-Sanchez, J. M., McNairn, H. y Rao, Y. S. (2020). Dual polarimetric radar vegetation index for crop growth monitoring using Sentinel-1 SAR data. *Remote Sensing of Environment, 247*, 111954. https://doi.org/10.1016/j.rse.2020.111954",
}

s = s.replace("## 3. Resultados\n", METODO + "## 3. Resultados\n", 1)
s = s.replace("## 4. Discusión\n", RESULTADO + "## 4. Discusión\n", 1)
i = s.index("## 5. Conclusiones y trabajo futuro"); j = s.index("\n\n## Disponibilidad", i); k = s.rfind("\n\n", i, j)   # último párrafo de 5
s = s[:k] + s[k:j].rstrip() + FUTURO + s[j:]
s = s.replace("| Informe y figuras metodológicas |", FILA_A1 + "| Informe y figuras metodológicas |", 1)
s = s.replace("Los scripts de las nueve etapas,", "Los scripts de las nueve etapas y de la polarimetría dual-pol,", 1)
# referencias en orden alfabético
r0 = s.index("## Referencias\n") + len("## Referencias\n"); r1 = s.index("## Anexo A"); bloque = s[r0:r1].strip("\n").split("\n\n")
for clave, ref in REFS.items():
    if any(b.startswith(clave) for b in bloque): continue
    bloque.append(ref)
bloque.sort(key=lambda b: b.lower().replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u"))
s = s[:r0] + "\n" + "\n\n".join(bloque) + "\n\n" + s[r1:]
MD.write_text(s, encoding="utf-8"); print("insertado: 2.9, 3.10, futuro, Tabla A1, %d referencias" % len(REFS))
