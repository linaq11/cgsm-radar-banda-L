# Plan preregistrado: polarimetría dual-pol NISAR (H/α y DpRVI) en la Ciénaga Grande de Santa Marta

Fecha: 2026-10-22. Para el Informe 2 del curso Radar y LiDAR (entrega en más de un mes) y, por extensión, el capítulo 3 de la tesis. Escrito antes de bajar un solo producto. Reproduce el cuaderno `GSLC_Basic_PolSARtools_Colombia_Guaviare.html` (NISAR dual-pol GSLC, `polsartools`) en otra región de Colombia: la CGSM.

## 1. Pregunta

¿La descomposición dual-pol H/α y el índice DpRVI de NISAR en banda L separan los estados del manglar que la óptica y Sentinel-1 en banda C no separan a 10 m, en particular el bosque muerto con troncos en pie frente a la herbácea sin troncos?

## 2. Datos (verificados el 2026-10-22 con `asf_search`)

- NISAR L2 GSLC dual-pol (HH, HV; sufijo DHDH) sobre el AOI de la tesis: 24 productos entre 2025-10-29 y 2026-10-20, dos órbitas (path 11: 15 productos; path 119: 9). Mismas fechas y conteos en GCOV.
- Puntos de referencia: los 436 con fracción de copa e indicador de troncos muertos (`MUESTRA_2025/revision/fraccion_copa_resultado_20261022.csv`), etiquetas v1.1 y v1.3 de los 820, y la reserva de validación como límite de uso (ningún punto de la reserva).
- Sentinel-2 2025: compuestos seco y húmedo del cubo, para la comparación óptica del cuaderno.
- Escenas que se usan para los contrastes: las de 2025-10 a 2025-12 (más cercanas al año de las etiquetas), una por órbita; las demás solo para la serie.

## 3. Procesamiento (el del cuaderno, sin cambios de método)

1. Descarga de los productos GSLC de una fecha por órbita (Earthdata Login de Lina).
2. Matriz de covarianza C2 (HH, HV) por producto; filtro Lee refinado de 7 x 7.
3. Compuesto RGB dual-pol; descomposición H/α dual-pol (entropía H, ángulo α); DpRVI.
4. Subconjunto de alta resolución sobre el núcleo del manglar (bloque 450099, el de 132 puntos) y otro sobre Pajarales.
5. Remuestreo de H, α y DpRVI a la malla del cubo (10 m, EPSG:9377) para extraer valores en los puntos.

## 4. Contrastes preregistrados

Todos con los puntos fuera de la reserva, una sola fecha por órbita, valores extraídos en el píxel de 10 m y en la media de 3 x 3.

| # | Contraste | Grupos (regla declarada) | Estadístico | Qué refutaría la lectura |
|---|---|---|---|---|
| P1 (primario) | α separa bosque muerto con troncos de herbácea sin troncos | muerto = fracción < 20 e indicador troncos = sí; herbáceo = fracción < 20 e indicador = no (regla de `capitulo2_linea_de_corte.md`) | AUC de α (y de H) con IC bootstrap de 2.000 | AUC con IC que incluya 0,5, o menor que el de S1 en banda C (0,43 a 0,59) |
| P2 | DpRVI crece con la fracción de copa | seis cajas, punto medio | Spearman de DpRVI con el punto medio de caja, IC bootstrap; además RMSE de una regresión lineal por bloques | ρ con IC que incluya 0 |
| P3 | el mapa bosque / no bosque del cuaderno (umbral de DpRVI o de H/α) concuerda con manglar / no manglar de v1.1 | nivel 1: manglar = intacto + degradado; no manglar = humedal + otro | macro-F1 y exactitud por bloque; comparación con el 0,64 de la unión óptica | macro-F1 por debajo de 0,64 |
| P4 (sensibilidad) | P1 repetido con las dos órbitas por separado y con 3 x 3 | | mismas métricas | discrepancia de signo entre órbitas |

Corrección por multiplicidad: Holm sobre P1 a P3. P4 no cuenta.

### 4b. P4 concretado (preregistrado el 2026-10-24, antes de procesar)

Fechas: 2026-07-04 (trayectoria ascendente 119) y 2026-07-08 (descendente 11), cuatro días entre sí y misma estación (río alto), para que la diferencia sea de geometría y no de fenología. Se repiten P1, P2 y P3 en cada fecha con la misma regla y los mismos puntos. Expectativa declarada: misma dirección que en diciembre (bosque muerto con alfa, H y DpRVI menores que la herbácea; HH mayor) en las dos órbitas. Refutaría: AUC de alfa a lados opuestos de 0,5 entre órbitas, o IC del AUC de una órbita que incluya 0,5. Comparación secundaria, exploratoria: 8-jul frente a 4-dic y 16-dic (misma órbita 11) como efecto de estación. Se reporta en el informe tal como salga.

Resultado (2026-10-26, tras procesar las dos fechas): no refutado. AUC de alfa 0,66 [0,59; 0,73] en A119 y 0,62 [0,54; 0,69] en D11, misma dirección en los cinco descriptores, ningún IC de alfa, H o DpRVI incluye 0,5; P2 rho 0,55 en ambas, P3 macro-F1 0,58 y 0,56. Estación (exploratorio): AUC de alfa, H y DpRVI 0,04 a 0,05 menores en julio que en diciembre, IC solapados; umbral de Otsu del DpRVI 0,32 en diciembre y 0,40 a 0,41 en julio. Reportado en la sección 3.10 y en la Tabla 14 del informe.

### 4c. Tareas del Informe 2 pedidas en clase (diapositiva 50, 22-oct-2026), preregistradas el 2026-10-26 antes de calcular

**P5. Random Forest con las variables polarimétricas** (HH, HV, HH − HV en dB, H, alfa, DpRVI; píxel, y media 3 x 3 como sensibilidad), sobre los 880 puntos v1.3, con los mismos pliegues de 12 km y zona de exclusión de 2,6 km de la cadena de la tesis, 500 árboles, semilla 20261007, macro-F1 de seis clases fuera de pliegue.
- Brazos: radar solo (6 variables), unión óptica S2 + AlphaEarth (94), unión + radar (100). Fecha principal 16-dic-2025; 4-dic como sensibilidad; las dos fechas apiladas (12 variables) como tercera variante.
- Expectativa declarada: radar solo entre 0,30 y 0,45 de macro-F1 (muy por debajo del 0,56 de la unión óptica); unión + radar frente a unión, ganancia de 0,01 o menos, como ocurrió con Sentinel-1 (+0,005). Refutaría la lectura "el radar no añade información a 10 m": ganancia mayor de 0,02 con p de permutación por bloques menor de 0,05, o una mejora de F1 del par degradado / humedal mayor de 0,05.
- Falta de datos: los NaN de las variables ópticas se rellenan con la mediana de la columna (no por clase, para no filtrar la etiqueta).
- Resultado (2026-10-26): dentro de lo preregistrado. Radar solo 0,34 a 0,36; unión + radar frente a unión entre −0,004 y +0,010 con p > 0,48 (McNemar p >= 0,50); degradado / humedal no mejoran más de 0,015. Reportado en la sección 3.10 y en la Tabla 15 del informe; P6 a P8 quedan en el trabajo futuro del informe como pendientes preregistrados.
**P6. Detección de cambio entre dos fechas** con el log-cociente de HV (16-dic frente a 4-dic de 2025, y julio frente a diciembre cuando esté procesado): se preregistrará aparte cuando se defina qué cambio real se espera detectar (candidato: el avance de Hydrilla en la planicie, verificado por Salzwedel et al. 2026).
**P7. Comparación GSLC frente a GCOV** en los 880 puntos (sigma cero de GCOV ya extraído para el informe 1 de radar frente a C11/C22 del GSLC): correlación y sesgo por clase; se preregistra cuando se elija la fecha común.
**P8. Coherencia a 12 días** (par 4-dic / 16-dic): requiere los SLC sin recorte de fase; se evaluará si el recorte conserva la fase compleja. Pendiente.

### 4d. P9: PlanetScope del 16 de diciembre frente a NISAR del mismo día (preregistrado el 2026-10-28, antes de calcular)

Pregunta. ¿El DpRVI (y H, alfa) de NISAR del 16-dic-2025 sigue mejor la cobertura de copa observada el mismo día a 3 m en PlanetScope que la fracción de copa interpretada en la muestra, que es de otra fecha? Cierra el cabo de P2: la rho de 0,55 podía estar limitada por el radar o por la referencia desfasada.

Datos. `planet_puntos_20251216.csv` (880 puntos, escena, clear de udm2, medias 3 x 3 a 3 m, NDVI 3 x 3), escenas SR a 3 m del pedido 5c903e33, `polsar_puntos_20251216_P011.csv`. Solo puntos con clear = 1 (705).

Referencias ópticas del mismo día: (a) NDVI de Planet en 3 x 3 (9 m); (b) proxy de copa: fracción de píxeles de 3 m con NDVI > 0,5 en la ventana 3 x 3, con 0,4 y 0,6 como sensibilidad.

Estadísticos. Spearman con IC bootstrap (2.000, semilla 20261028) de DpRVI (primaria), H y alfa frente a (a), (b) y a la fracción de copa interpretada (punto medio de caja, como en P2); diferencia pareada rho(Planet) − rho(interpretada) sobre los mismos puntos con IC bootstrap. Píxel como principal, 3 x 3 como sensibilidad. Medianas por clase v1.3 de NDVI, proxy de copa y DpRVI.

Regla de lectura. Si la diferencia pareada rho(Planet) − rho(interpretada) para DpRVI es mayor de 0,05 con IC que excluye 0, la referencia desfasada era el límite de P2 y el radar sigue la copa del mismo día mejor de lo que P2 mostró. Si la diferencia es menor de 0,05 o su IC incluye 0, el límite está en el radar: el DpRVI ordena la copa pero no la estima, con cualquier referencia. Se reporta tal como salga en la sección 3.10 y la tarea de Planet deja de ser futuro. Script `07_planet_nisar.py`.

Resultado (2026-10-28): límite en el radar. Sobre los 341 puntos interpretados y despejados, DpRVI frente a NDVI Planet del mismo día rho 0,604, frente a fracción interpretada 0,558; diferencia pareada 0,046 [−0,020; 0,114], IC incluye 0. H y alfa igual. Proxy de copa a 3 m con NDVI > 0,5 saturado (mediana 1,0 en vegetación), rho 0,318: descartado. Sobre los 705 puntos de todas las clases la relación se invierte (rho −0,191) por el agua (NDVI bajo, DpRVI alto). Reportado en 3.10; Planet sale del trabajo futuro.

## 5. Lo que ya se sabe y acota la expectativa

- Sentinel-1 banda C mensual a 10 m no separa humedal de degradado (AUC 0,43 a 0,59, 2026-10-22).
- En banda L (ALOS-2, informe de radar) el manglar se separa del bosque y la deriva 2017-2025 es de recuperación del manglar.
- La polarimetría dual-pol no tiene la fase cruzada completa (no hay HV·VV*): H/α dual-pol distingue menos mecanismos que la quad-pol. Se declara.
- Las fechas NISAR (oct 2025 en adelante) no coinciden con la imagen de Google con que se etiquetó la fracción (fecha desconocida); se declara como limitación.

## 6. Entregables para el Informe 2 de radar

- Sección "Reproducción del flujo PolSAR dual-pol de NISAR en la CGSM": figuras del cuaderno (RGB, H/α, DpRVI, plano H/α) sobre el núcleo del manglar y Pajarales.
- Tabla con P1 a P4 y sus intervalos.
- Comparación con Sentinel-2 como en el cuaderno (sección 9), usando las clases v1.1 en vez de un mapa bosque/no bosque.
- Scripts en `RADAR/polsar_nisar/` y copia en el repositorio `cgsm-radar-banda-L`.

## 6b. Desviación declarada de herramienta (2026-10-22)

`polsartools` no se instala en el Python 3.14 del equipo (no hay rueda precompilada y la compilación desde fuente falla; tampoco hay enlaces GDAL `osgeo`). Las operaciones del cuaderno se reimplementan en NumPy y rasterio con las mismas ecuaciones: C2 = [[<|HH|²>, <HH·HV*>], [<HV·HH*>, <|HV|²>]]; filtro Lee refinado 7 x 7 (o boxcar 7 x 7 como sensibilidad); autovalores λ1 ≥ λ2 de C2, p_i = λ_i / (λ1 + λ2), H = −Σ p_i log2 p_i, α = Σ p_i α_i con α_i = arccos(|e_i1|) de los autovectores; DpRVI = 1 − m·β con m = √(1 − 4·det(C2)/tr(C2)²) y β = λ1/(λ1 + λ2) (Mandal et al., 2020). Se verifica contra una tesela del cuaderno de Guaviare si se consigue su producto; si no, contra los rangos de valores que el cuaderno reporta.

**Retirada el 2026-10-23.** polsartools 0.13 se instaló en un entorno aparte de Python 3.12 (`C:\LINA\TOOLS\polsar_env`, uv) con GDAL 3.13.3; el procesamiento se hizo con la biblioteca del cuaderno, sin reimplementación. Diferencias que sí quedan: recorte remoto a la AOI en lugar de descarga completa, y 2 x 2 looks (10 m) en lugar de los del cuaderno.

## 7. Costo (corregido el 2026-10-22 con el catálogo real, `RADAR/nisar_gslc_cgsm_catalogo_20261022.csv`)

- Cada producto GSLC pesa 24 a 26 GB (frame completo). No se descargan enteros: se recorta el AOI de forma remota con `earthaccess` + `fsspec` + `h5py`, como ya se hizo con los GCOV (`18_nisar_recorte_remoto.py`), y se escribe un HDF5 recortado con la misma estructura de grupos para que `import_nisar_gslc` lo lea sin cambios. Disco: D: con 442 GB libres.
- Fechas disponibles: path 11 (descendente, frame 83) desde 2025-10-29 cada 12 días hasta 2026-01-09 y de 2026-06-26 a 2026-10-12; path 119 (ascendente, frame 7) solo desde 2026-06-22. Para los contrastes P1 a P3: path 11 de 2025-12-04 (época húmeda tardía) y 2025-12-16. Para P4 (sensibilidad por órbita): path 119 de 2026-07-04 frente a path 11 de 2026-07-08, misma semana. Versiones: las de 2025 traen CRID X0500 (sin P) y las de 2026 P05023; se usa la más reciente de cada fecha, como en el cuaderno.
- Entorno: `C:\LINA\TOOLS\polsar_env` (Python 3.12 con uv): polsartools 0.13, GDAL 3.13.3 (rueda de geospatial-wheels), rasterio, asf_search 14.1, h5py. Orden de importación obligatorio: `h5py` antes que `osgeo` (si no, h5py falla al cargar su DLL).
- Cómputo: una tarde. Redacción: medio día. Antes de empezar: archivo `_netrc` de Earthdata de Lina y autorización de la aplicación ASF.

## 8. Lista de chequeo

Se aplica `AVANCE TESIS/LISTA_DE_CHEQUEO_antes_de_entregar.md` antes de reportar cualquier número.
