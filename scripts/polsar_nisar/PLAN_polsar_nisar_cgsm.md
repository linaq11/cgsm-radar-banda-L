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

## 7. Costo (corregido el 2026-10-22 con el catálogo real, `RADAR/nisar_gslc_cgsm_catalogo_20261022.csv`)

- Cada producto GSLC pesa 24 a 26 GB (frame completo). No se descargan enteros: se recorta el AOI de forma remota con `earthaccess` + `fsspec` + `h5py`, como ya se hizo con los GCOV (`18_nisar_recorte_remoto.py`), y se escribe un HDF5 recortado con la misma estructura de grupos para que `import_nisar_gslc` lo lea sin cambios. Disco: D: con 442 GB libres.
- Fechas disponibles: path 11 (descendente, frame 83) desde 2025-10-29 cada 12 días hasta 2026-01-09 y de 2026-06-26 a 2026-10-12; path 119 (ascendente, frame 7) solo desde 2026-06-22. Para los contrastes P1 a P3: path 11 de 2025-12-04 (época húmeda tardía) y 2025-12-16. Para P4 (sensibilidad por órbita): path 119 de 2026-07-04 frente a path 11 de 2026-07-08, misma semana. Versiones: las de 2025 traen CRID X0500 (sin P) y las de 2026 P05023; se usa la más reciente de cada fecha, como en el cuaderno.
- Entorno: `C:\LINA\TOOLS\polsar_env` (Python 3.12 con uv): polsartools 0.13, GDAL 3.13.3 (rueda de geospatial-wheels), rasterio, asf_search 14.1, h5py. Orden de importación obligatorio: `h5py` antes que `osgeo` (si no, h5py falla al cargar su DLL).
- Cómputo: una tarde. Redacción: medio día. Antes de empezar: archivo `_netrc` de Earthdata de Lina y autorización de la aplicación ASF.

## 8. Lista de chequeo

Se aplica `AVANCE TESIS/LISTA_DE_CHEQUEO_antes_de_entregar.md` antes de reportar cualquier número.
