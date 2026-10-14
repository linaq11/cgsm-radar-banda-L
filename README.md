# Aporte de la banda L para la inundación bajo dosel de manglar en la Ciénaga Grande de Santa Marta

Código, resultados y figuras del informe de avance del curso *Radar and LiDAR Remote Sensing* (Maestría en Geomática, Universidad Nacional de Colombia, 2026-2). Autora: Lina María Quintero Fonseca.

Pregunta: qué información adicional aporta la banda L (NISAR, ALOS-2) frente a Sentinel-1 en banda C para identificar inundación bajo el dosel del manglar, en dos sitios con regímenes distintos: Bahía de Málaga (marea) y la Ciénaga Grande de Santa Marta, CGSM (río Magdalena).

El informe completo está en `informe/Avance_proyecto_radar.md`; la nota de auditoría de cálculos, en `informe/auditoria_calculos.md`.

## Qué hay

| Carpeta | Contenido |
|---|---|
| `guiones/` | Los 34 guiones de Python del informe, en la carpeta `RADAR` del proyecto original. Cada uno trae en su cabecera qué hace, qué lee, qué escribe y cómo se corre. |
| `guiones/publicacion_gee/` | Los seis guiones numerados de acceso a NISAR (inventario en el CMR, descarga y recorte remoto, malla de incidencia), que pertenecen a la publicación del cubo de datos de la tesis. |
| `resultados/` | Tablas CSV y resúmenes de texto que producen los guiones y que alimentan las tablas del informe. |
| `figuras/` | Las figuras del informe (PNG). |
| `informe/` | El informe en Markdown y la auditoría. |

No se incluyen los datos de entrada grandes: las escenas NISAR recortadas (`NISAR_AOI_*.h5`, 45 escenas, unos 470 MB cada una), los GeoTIFF de 50 m de los mapas ni las series completas del IDEAM y del mareógrafo UHSLC. Todos se regeneran o descargan con los guiones de la etapa 1.

## Flujo de trabajo

Las nueve etapas del informe (Figura 1 y Anexo A) y los guiones que las ejecutan:

| Etapa | Guiones | Salidas |
|---|---|---|
| 1. Acceso a datos | `16_inventario_nisar`, `17_descargar_nisar`, `18_nisar_recorte_remoto`, `23_nisar_recorte_pacifico`, `24_nisar_recorte_cgsm`, `nivel_ideam_descarga` | inventario `nisar_cgsm_granulos.json`, escenas `NISAR_AOI_*.h5`, `nivel_ideam_*.csv` |
| 2. Preprocesamiento y calibración | `18_nisar_recorte_remoto`, `20_nisar_incidencia`, `alos2_marea_malaga`, `s1_marea_malaga` | σ⁰ por sensor y pasada; malla de incidencia de NISAR |
| 3. Coberturas de referencia y muestreo | `perfil_pacifico_24`, `doble_rebote_incidencia`, `figuras_cgsm`, `figuras_pacifico` | 1.600 puntos por sitio; puntos de los tercios de incidencia |
| 4. Forzante hidrológico | `mareas_buenaventura`, `mareas_dimar_a_serie`, `marea_vs_radar`, `cgsm_nivel_rio` | marea, lluvia o nivel del río a la hora de cada pasada |
| 5. Estadística por pasada | `perfil_pacifico_24`, `marea_vs_radar`, `cgsm_temporada` | `cgsm_temporada_*.csv` |
| 6. Prueba hidrológica | `marea_vs_radar`, `s1_marea_malaga`, `alos2_marea_malaga`, `cgsm_temporada`, `cgsm_nivel_rio`, `figura_cgsm_optico` | tablas 4 a 9 del informe |
| 7. Robustez y límites | `doble_rebote_incidencia`, `autocorrelacion_temporal`, `auditoria_calculos.md` | tabla 10 del informe |
| 8. Clave de interpretación | `figura_clave`, `nisar_flotante`, `clave_vs_muestra2025` | `clave_muestra2025_*.csv`, tablas 11 a 14 |
| 9. Mapa y corroboración óptica | `mapa_doble_rebote`, `mapa_doble_rebote_s1`, `mapa_doble_rebote_malaga`, `corroboracion_dw` | `mapa_*_50m.tif`, `dw_serie.csv`, tablas 15 y 16 |
| Informe y figuras de método | `md_a_word`, `figura_flujo`, `figura_cadena_sar`, `figura_muestra_2025`, `figura_consistencia` | `Avance_proyecto_radar.docx`, figuras 1, 2, 4 y 19 |

`mapbiomas_cruce.py` es un cruce exploratorio con MapBiomas Colombia (colección 2) que no forma parte del informe.

## Datos externos y cómo se obtienen

- **NISAR L2 GCOV** (Beta y Provisional): archivo de la NASA (ASF DAAC) vía el catálogo CMR y `earthaccess`; hace falta una cuenta Earthdata. Los guiones de `publicacion_gee/` recortan de forma remota la ventana de cada sitio.
- **Sentinel-1 GRD, ALOS-2 PALSAR-2 ScanSAR L2.2, WorldCover 2021, Global Mangrove Watch 2020, ERA5-Land, Sentinel-2, Dynamic World, MapBiomas Colombia**: Google Earth Engine, con un proyecto propio. Los guiones usan `ee.Initialize(project=...)`; cambiar el identificador del proyecto.
- **Nivel del río Magdalena en Remolino**: datos abiertos del IDEAM en datos.gov.co (`nivel_ideam_descarga.py`).
- **Marea en Bahía de Málaga**: tabla de pleamares y bajamares 2026 de la DIMAR y predicción armónica propia a partir del mareógrafo UHSLC 085 de Buenaventura (`mareas_buenaventura.py`, `mareas_dimar_a_serie.py`).
- **Muestra de referencia de 2025** (720 puntos): pertenece a la tesis y no se publica aquí; `clave_vs_muestra2025.py` y `figura_muestra_2025.py` la leen de la carpeta de la tesis.

## Cómo correrlo

Python 3.12 o superior. Instalar dependencias:

```
pip install -r requirements.txt
```

Cada guion se corre desde la carpeta `guiones/` y documenta en su cabecera los argumentos y las salidas. El orden es el de la tabla de arriba; las etapas 5 a 9 leen los CSV que dejan las anteriores, de modo que se pueden reproducir desde `resultados/` sin descargar las escenas. Dos avisos: en Windows con PostGIS instalado, `rasterio` necesita su propio `PROJ_DATA` (los guiones de mapas lo fijan al arrancar); y las escenas NISAR se esperan en `D:\TESIS_DATACUBE\NISAR` y `NISAR_PACIFICO` (cambiar la ruta en la cabecera de cada guion).

## Cómo citar

Quintero Fonseca, L. M. (2026). *Aporte de la banda L para la identificación de inundación bajo dosel de manglar en la Ciénaga Grande de Santa Marta* [Informe de avance, curso Radar and LiDAR Remote Sensing]. Universidad Nacional de Colombia. https://github.com/linaq11/cgsm-radar-banda-L

## Licencia

Código bajo licencia MIT (ver `LICENSE`). Los productos de datos de terceros conservan sus licencias: NISAR (NASA, dominio público), Copernicus Sentinel (ESA, libre con atribución), ALOS-2 ScanSAR (JAXA, libre para uso no comercial), WorldCover (CC BY 4.0), Global Mangrove Watch (CC BY 4.0), Dynamic World (CC BY 4.0), MapBiomas Colombia (CC BY-SA 4.0), IDEAM y DIMAR (datos abiertos).
