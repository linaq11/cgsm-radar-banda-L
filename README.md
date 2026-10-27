# Respuesta de la banda L a la inundación bajo dosel de manglar: comparación con banda C en la Ciénaga Grande de Santa Marta y Bahía de Málaga

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23709974.svg)](https://doi.org/10.5281/zenodo.23709974)

Código, resultados y figuras de un estudio de radar desarrollado en la Maestría en Geomática de la Universidad Nacional de Colombia (2026).

**Autora:** Lina María Quintero Fonseca

El estudio evalúa qué información adicional aporta la banda L (NISAR y ALOS-2) frente a Sentinel-1 en banda C para identificar condiciones de inundación bajo el dosel del manglar. El análisis se desarrolla en dos sistemas con forzantes hidrológicos distintos: Bahía de Málaga, dominada por la marea, y la Ciénaga Grande de Santa Marta (CGSM), analizada en relación con el nivel del río Magdalena.

El informe completo de este trabajo forma parte de la tesis de maestría en curso de la autora y se publicará con ella; este repositorio contiene el código, los resultados tabulados y las figuras que lo sustentan. La auditoría de cálculos está en `informe/auditoria_calculos.md`.

## Contenido del repositorio

| Carpeta | Contenido |
|---|---|
| `scripts/` | 36 scripts de Python usados en el informe. Cada uno documenta en su cabecera su propósito, los archivos de entrada, los productos que genera y la forma de ejecutarlo. |
| `scripts/publicacion_gee/` | Seis scripts numerados para el acceso y el procesamiento inicial de NISAR: consulta del catálogo CMR, descarga, recorte remoto y extracción de la malla de incidencia. |
| `resultados/` | Tablas CSV y archivos de texto generados por los scripts, con los que se construyen las tablas y los análisis del informe. |
| `figuras/` | Figuras del informe en PNG. La subcarpeta `figuras para flujo/` contiene los recortes reales de los tres radares, los recortes Sentinel-2 por cobertura, las series del forzante y los mapas de producto que componen la Figura 1, con sus scripts de exportación y un archivo `FUENTES.txt` con la procedencia de cada imagen. |
| `informe/` | Auditoría de cálculos. |

Los archivos de entrada de gran tamaño no se incluyen. Entre ellos están las 45 escenas NISAR recortadas (`NISAR_AOI_*.h5`, cerca de 450 MB cada una), los GeoTIFF de 50 m de la cartografía y las series completas del IDEAM y del mareógrafo UHSLC. Todos se descargan o se regeneran con los scripts de la etapa 1.

## Flujo de trabajo

El análisis se organiza en nueve etapas. La correspondencia entre etapas, scripts y productos es la siguiente:

| Etapa | Scripts principales | Salidas principales |
|---|---|---|
| 1. Acceso a datos | `16_inventario_nisar`, `17_descargar_nisar`, `18_nisar_recorte_remoto`, `23_nisar_recorte_pacifico`, `24_nisar_recorte_cgsm`, `nivel_ideam_descarga` | `nisar_cgsm_granulos.json`, escenas `NISAR_AOI_*.h5`, `nivel_ideam_*.csv` |
| 2. Preprocesamiento y calibración | `18_nisar_recorte_remoto`, `20_nisar_incidencia`, `alos2_marea_malaga`, `s1_marea_malaga` | σ⁰ por sensor y pasada; malla de ángulo de incidencia de NISAR |
| 3. Coberturas de referencia y muestreo | `perfil_pacifico_24`, `doble_rebote_incidencia`, `figuras_cgsm`, `figuras_pacifico` | 1.600 puntos por sitio; 4.844 puntos para el análisis por terciles de incidencia |
| 4. Forzante hidrológico | `mareas_buenaventura`, `mareas_dimar_a_serie`, `marea_vs_radar`, `cgsm_nivel_rio` | Marea, precipitación antecedente y nivel del río asignados a la hora de cada pasada |
| 5. Estadística por pasada | `perfil_pacifico_24`, `marea_vs_radar`, `cgsm_temporada` | `cgsm_temporada_*.csv`; Tabla 2 y Tabla B1 |
| 6. Prueba hidrológica | `marea_vs_radar`, `s1_marea_malaga`, `alos2_marea_malaga`, `cgsm_temporada`, `cgsm_nivel_rio`, `figura_cgsm_optico` | Tablas 3 a 6, B2 y B3; Figuras 5 y 7 a 12 |
| 7. Robustez y límites | `doble_rebote_incidencia`, `autocorrelacion_temporal`, `auditoria_calculos.md` | Tabla 7; Figura 6; auditoría de cálculos |
| 8. Clave de interpretación | `figura_clave`, `nisar_flotante`, `clave_vs_muestra2025` | `clave_muestra2025_*.csv`; Tablas 8 a 10 y B4; Figura 13 |
| 9. Cartografía y contraste óptico | `mapa_doble_rebote`, `mapa_doble_rebote_s1`, `mapa_doble_rebote_malaga`, `corroboracion_dw` | `mapa_*_50m.tif`, `dw_serie.csv`; Tabla 11 y B5; Figuras 14 a 17 |
| Informe y figuras metodológicas | `md_a_word`, `figura_flujo`, `figura_cadena_sar`, `figura_diseno_h`, `figura_muestra_2025`, `figura_consistencia` y los `exportar_*.py` de `figuras/figuras para flujo/` | Documento del informe y figuras metodológicas y de evaluación |

El script `mapbiomas_cruce.py` corresponde a un análisis exploratorio con MapBiomas Colombia, colección 2, y no forma parte de los resultados del informe.

## Datos externos

### NISAR L2 GCOV

Se usan productos NISAR L2 GCOV de las colecciones Beta y Provisional, obtenidos del archivo de NASA ASF DAAC a través del catálogo CMR y `earthaccess`. Se requiere una cuenta de NASA Earthdata. Los scripts de `scripts/publicacion_gee/` localizan los gránulos y recortan de forma remota la ventana de cada sitio.

### Google Earth Engine

Desde Earth Engine se acceden Sentinel-1 GRD, ALOS-2 PALSAR-2 ScanSAR L2.2, ESA WorldCover 2021, Global Mangrove Watch 2020, ERA5-Land, Sentinel-2, Dynamic World y, solo para el análisis exploratorio, MapBiomas Colombia.

Los scripts inicializan Earth Engine con un identificador de proyecto:

```python
ee.Initialize(project="...")
```

Ese identificador debe sustituirse por el proyecto de Earth Engine de quien ejecute los scripts.

### Nivel del río Magdalena

El nivel del río se toma de la estación automática Remolino del IDEAM a través del portal de Datos Abiertos de Colombia. El script `nivel_ideam_descarga.py` descarga y prepara la serie.

### Marea en Bahía de Málaga

La serie de marea combina dos fuentes: para 2026, las tablas oficiales de pleamares y bajamares de la DIMAR, y para octubre a diciembre de 2025, una predicción armónica ajustada al mareógrafo UHSLC 085 de Buenaventura. Los scripts son `mareas_buenaventura.py` y `mareas_dimar_a_serie.py`.

### Muestra de referencia de 2025

La muestra de referencia contiene 720 puntos distribuidos en seis clases y forma parte de un trabajo de tesis en curso, por lo que no se distribuye en este repositorio. Los scripts `clave_vs_muestra2025.py` y `figura_muestra_2025.py` esperan encontrarla en la estructura local de ese proyecto.

## Ejecución

Se recomienda Python 3.12 o superior. Las dependencias se instalan con:

```bash
pip install -r requirements.txt
```

Los scripts se ejecutan desde la carpeta `scripts/`. Cada archivo documenta en su cabecera los datos de entrada, los argumentos y los productos. El orden general corresponde a las nueve etapas. Las etapas 5 a 9 trabajan sobre los CSV y productos intermedios de las etapas previas, de modo que gran parte del análisis se reproduce desde la carpeta `resultados/` sin volver a descargar las escenas SAR.

### Consideraciones locales

En Windows, una instalación paralela de PostGIS puede dejar en `PROJ_DATA` una base de datos de PROJ incompatible con la de `rasterio`. Los scripts de cartografía fijan de forma explícita la ruta de PROJ del entorno de Python antes de importar `rasterio`.

Los archivos NISAR están configurados en rutas locales como las siguientes, que deben cambiarse al ejecutar el flujo en otro equipo:

```text
D:\TESIS_DATACUBE\NISAR\
D:\TESIS_DATACUBE\NISAR_PACIFICO\
```

## Reproducibilidad

El repositorio contiene los scripts, los resultados tabulados y las figuras necesarios para reconstruir los análisis del informe. Los archivos de gran tamaño y los datos de repositorios externos no se duplican, sino que se recuperan de sus fuentes. La muestra de referencia de 2025 es la única entrada del análisis que no se distribuye.

## Cómo citar

Quintero Fonseca, L. M. (2026). *Respuesta de la banda L a la inundación bajo dosel de manglar: comparación con banda C en la Ciénaga Grande de Santa Marta y Bahía de Málaga* [Informe de avance, curso Radar and LiDAR Remote Sensing]. Universidad Nacional de Colombia. https://github.com/linaq11/cgsm-radar-banda-L

## Licencia

El código se distribuye bajo licencia MIT (véase `LICENSE`). Los datos y productos de terceros conservan las condiciones de uso de sus fuentes:

- NISAR: NASA.
- Copernicus Sentinel: ESA.
- ALOS-2 PALSAR-2 ScanSAR: JAXA.
- ESA WorldCover: CC BY 4.0.
- Global Mangrove Watch: CC BY 4.0.
- Dynamic World: CC BY 4.0.
- MapBiomas Colombia: CC BY-SA 4.0.
- IDEAM y DIMAR: según las condiciones de sus portales de datos.
