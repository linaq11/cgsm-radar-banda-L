# Documentación de los guiones

Cabecera y comentarios de cada guion, extraídos del código con `generar_documentacion.py`, en el orden del flujo de trabajo del informe. Cada cabecera dice qué hace el guion, qué lee, qué escribe y cómo se corre.

## 1. Acceso a datos

### `publicacion_gee/16_inventario_nisar.py`

Inventario de las escenas NISAR GCOV disponibles: fecha, orbita, polarizaciones,
incidencia y cobertura del AOI. Es el primer paso del experimento de ablacion que
decide si NISAR se queda en la tesis (criterio de disponibilidad: al menos una
adquisicion por estacion seca y una por humeda con cobertura completa del AOI).

Salida: tabla en pantalla y PUBLICACION_GEE/inventario_nisar.csv

Comentarios en el código:

- línea 16: noqa: F401
- línea 30: extension del AOI (malla del cubo) en UTM 18N
- línea 57: GCOV completo (..._20251204T232730_...) o recorte del AOI (NISAR_AOI_20251204_...)
- línea 67: recorte del AOI dentro de la malla de la escena
- línea 74: fraccion de pixeles validos dentro del AOI, muestreando cada 10 px
- línea 79: incidencia, si el producto la trae

### `publicacion_gee/17_descargar_nisar.py`

Descarga las escenas NISAR GCOV Beta sobre el AOI que faltan en D:\TESIS_DATACUBE\NISAR.

Las seis escenas salieron de una consulta a CMR (NASA) el 2026-09-09 sobre la
envolvente del AOI. Cubren octubre de 2025 a enero de 2026, todas descendentes,
traza D_083, cuadro 011, HH+HV; las tres de diciembre de 2025 caen dentro del cubo.

AUTENTICACION. Earthdata exige usuario y contrasena. Este guion NO los pide ni los
guarda: usa la libreria earthaccess, que lee las credenciales de ~/.netrc (o de
las variables EARTHDATA_USERNAME / EARTHDATA_PASSWORD) o abre el flujo de login
interactivo en la terminal de Lina. Ejecutar desde su terminal, no desde el agente.

USO
    pip install earthaccess --break-system-packages   (si no esta)
    python 17_descargar_nisar.py

Comentarios en el código:

- línea 39: netrc, variables de entorno o login interactivo

### `publicacion_gee/18_nisar_recorte_remoto.py`

Baja de NISAR GCOV solo la ventana del AOI, leyendo el HDF5 remoto por rangos.

POR QUE. Un GCOV completo pesa ~5,7 GB y a la velocidad medida (0,5 MB/s) son tres
horas por escena. El AOI ocupa ~3,5 % del cuadro, y HDF5 permite leer solo los
bloques que caen dentro de una ventana. Cada recorte queda en D:\TESIS_DATACUBE\NISAR
con la misma estructura de grupos que el producto original, de modo que
16_inventario_nisar.py y 12_nisar_parches.py lo leen sin cambios.

ORDEN. Primero las tres escenas de diciembre de 2025, que caen dentro del cubo y
son las que necesita la ablacion; despues las demas.

AUTENTICACION. Como en 17_descargar_nisar.py: earthaccess lee ~/.netrc o pregunta
en la terminal; este guion no maneja contrasenas. Ejecutar desde la terminal de Lina.

USO
    python 18_nisar_recorte_remoto.py        # todas las que falten
    python 18_nisar_recorte_remoto.py 2      # como maximo dos escenas en esta corrida

Comentarios en el código:

- línea 30: aire alrededor del AOI, en metros
- línea 33: diciembre de 2025 primero: caen dentro del cubo
- línea 50: extension del AOI en UTM 18N, que es la malla de los GCOV sobre la CGSM
- línea 96: filas por peticion: peticiones cortas, reintentos baratos
- línea 109: FSTimeoutError, ClientError, OSError
- línea 117: tope de escenas por corrida, para poder desconectar el disco entre una y otra
- línea 170: angulo de incidencia: va en una malla gruesa de metadatos, pesa poco
- línea 171: y hace falta para estratificar el doble rebote (umbral de 35 grados)

### `publicacion_gee/23_nisar_recorte_pacifico.py`

Recorta NISAR GCOV sobre el manglar de Bahia de Malaga (Buenaventura), sitio de
contraste del trabajo de radar, leyendo el HDF5 remoto por rangos como en
18_nisar_recorte_remoto.py.

ESCENAS. De las 55 dual-pol que tocan el nucleo del manglar, solo dos trazas lo
cubren completo: la ascendente 004 (frame 4005, 12 fechas, 10:00 UTC = 05:00
local, archivos de 1,6 GB) y la descendente 087 (frame 4005, 12 fechas, 23:00 UTC
= 18:00 local, 6,6 GB). Las dos horas del dia dan estados de marea distintos, que es
el contraste que se busca. Van primero las ascendentes, por ser mas rapidas. La
lista con sus URL esta en nisar_pacifico_granulos.json (inventario CMR del
11-sep-2026); las Beta y las Provisional traen URL distintas y se usan tal cual.

AOI. Caja lon/lat -77.40, 3.80, -77.10, 4.10 mas 2 km de margen, transformada a la
proyeccion que declara cada producto (se lee del archivo, no se supone).

AUTENTICACION. earthaccess pregunta en la terminal; este guion no maneja
contrasenas. Ejecutar desde la terminal de Lina.

USO
    python 23_nisar_recorte_pacifico.py        # todas las que falten
    python 23_nisar_recorte_pacifico.py 3      # como maximo tres escenas en esta corrida

Comentarios en el código:

- línea 35: lon0, lat0, lon1, lat1
- línea 38: en este orden

### `publicacion_gee/24_nisar_recorte_cgsm.py`

Recorta las escenas NISAR GCOV que faltan sobre la CGSM (las 11 Provisional de
jun-sep 2026, de las que 3 ya estan completas en disco), con el mismo metodo de
18_nisar_recorte_remoto.py y 23_nisar_recorte_pacifico.py: lectura remota por rangos
de la ventana del AOI (extension del cubo + 2 km), proyeccion leida del producto.

Lista con URL en nisar_cgsm_granulos.json (inventario CMR del 12-sep-2026): 6 Beta
(D083, ya recortadas como NISAR_AOI_<fecha>_083_4.h5) y 11 Provisional: 6 de la traza
descendente D083 (18:29 local) y 5 de la ascendente A007 (nueva sobre la CGSM). Se
saltan las fechas que ya esten en disco con cualquiera de los dos nombres.

AUTENTICACION: earthaccess pregunta en la terminal. Ejecutar desde la terminal de Lina.

USO
    python 24_nisar_recorte_cgsm.py        # todas las que falten
    python 24_nisar_recorte_cgsm.py 3      # como maximo tres en esta corrida

### `nivel_ideam_descarga.py`

Descarga el nivel del río Magdalena (y candidatos cercanos) desde los datos abiertos del
IDEAM en datos.gov.co, para usarlo como forzamiento hidrológico de la prueba de doble
rebote en la CGSM en lugar de la lluvia.

Conjuntos de datos (Socrata, sin registro):
  bdmn-sqnh  Nivel Instantáneo del Río
  vfth-yucv  Nivel Máximo del Río
  pt9a-aamx  Nivel Mínimo del Río
  ia8x-22em  Nivel del Mar
Estaciones (Catálogo Nacional de Estaciones, hp9r-jxuu):
  2904700095 Remolino AUT (Magdalena, automática con telemetría)
  0029047020 Las Flores (Magdalena, Barranquilla)
  0029047000 Tebsa Barranquilla AUT
  0029067130 Puente Ferrocarril Aracataca (río Aracataca)

Salida: nivel_ideam_<dataset>.csv por conjunto con datos, y nivel_ideam_resumen.txt.

Comentarios en el código:

- línea 58: Nivel del mar en el Caribe (por si hay mareógrafo cerca de la CGSM)

## 2. Preprocesamiento y calibración

### `publicacion_gee/20_nisar_incidencia.py`

Anade el angulo de incidencia a los recortes NISAR que no lo traen.

Los dos primeros recortes (2025-12-04 y 2025-12-16) se hicieron antes de que
18_nisar_recorte_remoto.py copiara la malla de metadatos radarGrid. El angulo hace
falta para estratificar el doble rebote (umbral de 35 grados). Se lee solo esa
malla gruesa del producto remoto, que pesa poco, y se escribe dentro del recorte.

Como los demas guiones de descarga, usa la sesion Earthdata de Lina; correr desde
su terminal.

USO
    python 20_nisar_incidencia.py

### `alos2_marea_malaga.py`

La misma prueba de marea con ALOS-2 PALSAR-2 ScanSAR (banda L, HH y HV como NISAR)
sobre Bahia de Malaga. Separa polarizacion de longitud de onda: si ALOS-2 muestra la
subida de HH con la marea que muestra NISAR y no muestra Sentinel-1, la diferencia con
Sentinel-1 es de longitud de onda.

Datos: JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR en Earth Engine (25 m, DN), 2025-01 a 2026-09,
dB = 10*log10(DN^2) - 83 (misma conversion que 22_alos2_gee.py). Los cuadros de una misma
pasada (mismo path, menos de 5 min) se mosaican. Se agrupa por path (RSP_Path_Number),
que fija hora y geometria, como las trazas de NISAR. Mismos 1.600 puntos y misma marea
(serie de trabajo mareas_buenaventura.csv, que debe cubrir desde ene-2025).

Salidas: alos2_marea_malaga.csv, alos2_marea_resumen.csv, fig_alos2_marea.png

Comentarios en el código:

- línea 58: algunas escenas son solo HH

### `s1_marea_malaga.py`

La misma prueba de marea con Sentinel-1 (banda C) sobre Bahia de Malaga.

Toma todas las escenas Sentinel-1 GRD IW (VV, VH, sigma cero en dB, corregidas por
terreno en Earth Engine) que cubren la caja entre oct-2025 y sep-2026, las agrupa por
orbita relativa (cada orbita tiene su hora y su geometria, como las trazas de NISAR),
muestrea los mismos 1.600 puntos (manglar de consenso, bosque, humedal, agua; semilla
42) y asigna a cada escena la marea predicha a SU hora de adquisicion. Luego aplica
la misma regla que marea_vs_radar.py: manglar menos bosque contra marea, diferencia
alta-baja y Spearman, por orbita.

Ademas restringe a las escenas a +-3 dias de una pasada NISAR para la comparacion
directa "mismas fechas".

Salidas: s1_marea_malaga.csv (por escena y clase), s1_marea_resumen.csv, fig_s1_marea.png

Comentarios en el código:

- línea 32: --- puntos, identicos a perfil_pacifico_24.py
- línea 43: --- marea
- línea 54: --- escenas S1
- línea 60: una pasada = todos los cuadros de la misma orbita con menos de 5 minutos entre si;
- línea 61: se mosaican, porque los cuadros parten la caja (80 % + 20 %)
- línea 88: --- mismas fechas que NISAR (+-3 dias)
- línea 94: --- prueba por orbita
- línea 121: --- figura

## 3. Coberturas de referencia y muestreo

### `perfil_pacifico.py`

Primer perfil de retrodispersion NISAR sobre Bahia de Malaga: mediana de HH, HV y
HH-HV (dB, sigma cero) por cobertura de WorldCover 2021 y por escena, con el angulo
de incidencia. Valida ademas los recortes (proyeccion, tamano, cobertura).

Coberturas: manglar (95), agua (80), bosque (10), humedal herbaceo (90).
Puntos: 400 por clase, muestreados en Earth Engine dentro de la caja del recorte.

Comentarios en el código:

- línea 28: --- puntos por clase desde WorldCover, dentro de la caja del AOI
- línea 38: --- segunda mascara de manglar, independiente: Global Mangrove Watch v3, extension 2020
- línea 47: puntos donde los dos productos coinciden en manglar, y donde solo uno lo dice
- línea 102: --- Dynamic World: probabilidad de vegetacion inundada y de agua en los mismos puntos,
- línea 103: con las imagenes de +-10 dias alrededor de cada escena NISAR (el Pacifico es nuboso)
- línea 121: label 2 = flooded_vegetation

### `perfil_pacifico_24.py`

Paso 1 del trabajo de radar: perfil de retrodispersion NISAR sobre Bahia de Malaga
con las 24 escenas (12 ascendentes A004, 05:00 local; 12 descendentes D087, 18:00
local), por cobertura y por traza, con columna de marea lista para llenar.

COBERTURAS (400 puntos cada una, semilla 42): manglar = consenso WorldCover 2021 (95)
y Global Mangrove Watch 2020; bosque (WC 10) como control que no se inunda; humedal
herbaceo (WC 90); agua (WC 80).

MAREA. Si existe mareas_buenaventura.csv (columnas: fecha_hora_utc en formato
YYYY-MM-DD HH:MM, altura_m), se asigna a cada pasada la altura interpolada a la hora
exacta de adquisicion. Si no existe, la columna queda vacia y el guion lo dice.

SALIDAS (en RADAR/):
  perfil_pacifico_24.csv     mediana e IQR de HH, HV, HH-HV por escena y clase, con traza,
                             hora local, incidencia y marea
  fig_perfil_pacifico_24.png serie temporal por traza (ingles)
  resumen en consola: diferencia entre trazas por clase y variacion dentro de cada traza

USO
    python perfil_pacifico_24.py

Comentarios en el código:

- línea 48: ----------------------------------------------------------------- puntos por clase
- línea 63: ----------------------------------------------------------------- marea (opcional)
- línea 79: segundos desde la epoca sin depender de la resolucion interna del datetime (pandas 3 usa microsegundos)
- línea 92: ----------------------------------------------------------------- lectura de escenas
- línea 137: ----------------------------------------------------------------- resumen
- línea 154: ----------------------------------------------------------------- figura
- línea 164: la linea se corta donde hay mas de 40 dias sin escenas (hueco feb-jun), para no
- línea 165: dibujar una tendencia que no se observo

### `doble_rebote_incidencia.py`

Paso 3 completo: la prueba del doble rebote estratificada por angulo de incidencia.

REGLA (escrita antes de mirar). Si el aumento de HH del manglar con la marea es doble
rebote tronco-agua, debe ser mayor donde la incidencia es menor (el haz llega mas
vertical y el rebote esquina es mas eficiente) y no depender de la incidencia en el
bosque. Dentro de cada traza se dividen los puntos de manglar en tres tercios de
incidencia y se repite, para cada tercio, la correlacion de Spearman entre la marea
de la pasada y la mediana de HH, HV y HH-HV del tercio, restando fecha a fecha la
mediana del bosque del mismo tercio.

Lee los 24 recortes NISAR y mareas_buenaventura.csv. Escribe doble_rebote_incidencia.csv
y fig_doble_rebote_incidencia.png.

Comentarios en el código:

- línea 58: valores por punto y escena
- línea 86: tercios de incidencia por traza (definidos sobre los puntos de manglar; el bosque usa los mismos cortes)

### `figuras_cgsm.py`

Figuras de mapa para el informe de radar, Ciénaga Grande de Santa Marta (inglés).

fig_cgsm_radar.png       composiciones NISAR (R = HH, G = HV, B = HH-HV) de dos pasadas de la
                         traza descendente 083 de la misma versión del producto (Beta), una con
                         el río Magdalena alto (4-dic-2025, 2,67 m en Remolino) y otra con el río
                         más bajo (9-ene-2026, 1,69 m), con el contorno del manglar de consenso y
                         del AOI, y el mapa de diferencia de HH entre ambas. Las pasadas con el
                         río más bajo (0,9 a 1,2 m) son de la colección Provisional y no se
                         restan para no mezclar el cambio de calibración.
fig_cgsm_referencia.png  coberturas WorldCover 2021 y acuerdo WorldCover / GMW dentro del AOI.

Comentarios en el código:

- línea 37: submuestreo para la figura (60 m)
- línea 65: contorno del AOI en UTM
- línea 81: máscaras desde Earth Engine en la malla de la figura
- línea 101: áreas dentro del AOI (ha)
- línea 102: 1 solo WC, 2 solo GMW, 3 ambos
- línea 108: ---------------------------------------------------------------- figura 1
- línea 132: ---------------------------------------------------------------- figura 2

### `figuras_pacifico.py`

Figuras de mapa para el informe de radar, Bahia de Malaga (ingles).

fig_malaga_radar.png     composiciones NISAR (R = HH, G = HV, B = HH-HV) de una escena
                         ascendente y una descendente cercanas en fecha, con el contorno
                         del manglar de consenso, y el mapa de diferencia HH entre ambas
fig_malaga_referencia.png coberturas WorldCover 2021 y acuerdo WorldCover / GMW

Comentarios en el código:

- línea 30: submuestreo de pixeles para la figura (30 m)
- línea 51: ---------------------------------------------------------------- recorte comun a la caja
- línea 76: ---------------------------------------------------------------- mascara de consenso desde Earth Engine, en la malla de la figura
- línea 97: ---------------------------------------------------------------- figura 1: composiciones y diferencia
- línea 105: diferencia HH (A - D), reproyectada por simple recorte comun (misma malla UTM y mismo paso)
- línea 118: ---------------------------------------------------------------- figura 2: referencia
- línea 122: 0 ninguno, 1 solo WC, 2 solo GMW, 3 ambos

### `figuras_gee.py`

Figuras del ejercicio de SAR basics de GEE, corrido sobre el AOI de la tesis.

Replica los tres pasos del tutorial (cobertura, orbitas e incidencia,
retrodispersion) usando COPERNICUS/S1_GRD sobre AOI_tesis_CGSM_v1 en vez del
area de ejemplo. Escribe PNG en figuras/.

Comentarios en el código:

- línea 49: a veces devuelve zip
- línea 155: mediana de un solo mes (marzo 2021, estacion seca) en vez de las 197 escenas:
- línea 156: el proyecto esta en modo restringido de cuota y la mediana anual la excede

### `figura_sitios.py`

Mapa de localización de los dos sitios del trabajo de radar, para la diapositiva
"Diseño comparativo": Bahía de Málaga (régimen mareal) y Ciénaga Grande de Santa Marta
(régimen hidrológico continental), con los sensores usados en cada uno.

Fondo: teselas CartoDB Positron (panel principal) y Esri World Imagery (recuadros), vía
contextily. Salida: fig_sitios_localizacion.png (inglés, como todas las figuras).

Comentarios en el código:

- línea 22: python figura_sitios.py es  -> versión en español
- línea 42: CartoDB exige clave desde 2026
- línea 47: texto sin recuadro: solo un halo blanco fino para que se lea sobre el mapa base
- línea 63: Recuadros con imagen satelital y el contorno de cada sitio.

## 4. Forzante hidrológico

### `mareas_buenaventura.py`

Prediccion de marea en Buenaventura para 2025-2026 por analisis armonico del
mareografo historico (UHSLC estacion 085, horario, 1953-2014, calidad revisada).

POR QUE. Las tablas oficiales de la DIMAR/CIOH son la fuente de referencia, pero no se
pudieron descargar desde esta maquina. La marea astronomica es determinista: con los
constituyentes armonicos ajustados a un registro largo se predice la altura a
cualquier hora futura, que es lo que hacen las tablas. No incluye el residuo
meteorologico (marejada, presion), pequeno frente a un rango de 3 a 4 m.

METODO. Minimos cuadrados sobre seno y coseno de 11 constituyentes (M2, S2, N2, K2,
K1, O1, P1, Q1, M4, MS4, MN4) con sus frecuencias astronomicas, ajustados a 2010-2014.
Sin correccion nodal (ciclo de 18,6 anos): error de amplitud de pocos por ciento,
irrelevante para ordenar pasadas por marea alta o baja. La calidad se mide
reconstruyendo 2014 y comparando con lo observado.

SALIDA. mareas_buenaventura.csv (fecha_hora_utc, altura_m respecto al nivel medio)
cada 10 minutos de oct-2025 a sep-2026, en el formato que lee perfil_pacifico_24.py.

Comentarios en el código:

- línea 26: frecuencias en ciclos por hora (constantes astronomicas estandar)
- línea 63: desde ene-2025 para cubrir ALOS-2
- línea 68: sin tabla oficial, la propia es la serie de trabajo

### `mareas_dimar_a_serie.py`

Convierte la tabla oficial de pleamares y bajamares de la DIMAR (CCCP, pronostico de
Malaga) en la serie cada 10 minutos que lee perfil_pacifico_24.py, y la compara con
la prediccion armonica propia.

ENTRADA: mareas_dimar_malaga.csv con una fila por extremo, columnas:
    fecha_hora_local, altura_lat_m
  (hora local de Colombia, UTC-5; altura referida al LAT como la publica la DIMAR).
  Ejemplo:
    2026-09-11 03:43, 4.24
    2026-09-11 09:38, 0.63
Entre extremos consecutivos se interpola con medio coseno, que es la forma de la
onda de marea entre una pleamar y una bajamar.

SALIDA: mareas_buenaventura.csv se reemplaza por la serie oficial (la propia queda
como mareas_prediccion_propia.csv) y se imprime la comparacion en las 24 pasadas.

Comentarios en el código:

- línea 28: acepta uno o varios archivos: los que se pasen por linea de comandos, o por defecto
- línea 29: mareas_dimar_malaga.csv y todos los "Málaga-Tabla-Pronóstico-AAAA.csv" descargados de la DIMAR
- línea 45: tabla de la DIMAR, con o sin comillas: "Pleamar","03:43:00","4.24m","11/09/2026"
- línea 71: serie de trabajo: oficial donde existe, prediccion propia fuera de su cobertura
- línea 87: comparacion con la prediccion propia en las 24 pasadas NISAR

### `marea_vs_radar.py`

Paso 3, version preliminar: relacion entre la altura de marea en la pasada y la
retrodispersion NISAR del manglar, por traza, con el bosque como control.

REGLA DE LECTURA (escrita antes de mirar los numeros). Si la banda L ve la inundacion
bajo el dosel, dentro de cada traza el manglar debe mostrar mayor HH (y mayor HH-HV)
en marea alta que en baja, y el bosque no. Se compara la mediana de las pasadas por
encima de la mediana de marea contra las de abajo, y la correlacion de Spearman entre
marea y HH. El efecto estacional se descuenta restando, fecha a fecha, el valor del
bosque (que no se inunda) al del manglar.

Lee perfil_pacifico_24.csv (con marea_m) y escribe marea_vs_radar.csv y una figura.

Comentarios en el código:

- línea 42: manglar menos bosque, fecha a fecha: descuenta lo estacional

### `cgsm_nivel_rio.py`

Prueba de doble rebote en la CGSM con el nivel del río Magdalena como forzamiento.

Reutiliza las medianas por pasada y clase de cgsm_temporada.py (cgsm_temporada_nisar.csv,
_s1.csv, _alos2.csv) y les asigna el nivel del río en el momento de cada pasada, tomado de
la estación automática Remolino (IDEAM 2904700095, datos abiertos), o de la estación que
se indique. Regla de lectura, la misma de Bahía de Málaga: manglar menos bosque, diferencia
entre el tercio de nivel alto y el de nivel bajo, y Spearman con el nivel.

USO
    python cgsm_nivel_rio.py [codigo_estacion]      (por defecto 2904700095)

Salida: cgsm_nivel_rio_resumen.csv, fig_cgsm_nivel_rio.png

Comentarios en el código:

- línea 30: 1. Serie de nivel: se prefiere el instantáneo; si no hay, el máximo diario.
- línea 49: Las fechas del IDEAM son hora local (UTC−5); las pasadas de radar vienen en UTC.
- línea 52: segundos, sin depender de la resolución interna
- línea 63: 2. Pasadas de radar por sensor y traza.
- línea 66: las copias _CAJA son la región anterior, no se mezclan
- línea 78: las pasadas de una traza varían un minuto
- línea 105: 3. Figura.

## 5 y 6. Estadística por pasada y prueba hidrológica

### `cgsm_temporada.py`

La prueba de inundacion bajo dosel en la CGSM, donde no hay marea: la variable
hidrologica es la lluvia acumulada en los 30 dias previos a cada pasada (ERA5-Land,
promedio sobre el AOI) y, como particion, epoca seca (dic-abr) frente a humeda
(may-nov). Misma regla que en el Pacifico: manglar menos bosque contra la variable,
diferencia entre las pasadas de mas y menos lluvia, Spearman; el bosque (WorldCover 10,
sobre todo bosque seco de los piedemontes) es el control que no se inunda.

Sensores: NISAR (recortes locales en D:\TESIS_DATACUBE\NISAR, HH y HV), Sentinel-1 GRD
(VV y VH, Earth Engine) y ALOS-2 ScanSAR (HH y HV, Earth Engine), oct-2025 a sep-2026,
todos sobre los mismos 1.600 puntos del AOI (manglar WorldCover∩GMW, bosque, humedal
herbaceo, agua; 400 por clase). Los sensores sin recortes en disco se saltan.

USO: python cgsm_temporada.py [nisar|s1|alos2 ...]   (por defecto los tres)
Salidas: cgsm_temporada_<sensor>.csv, cgsm_temporada_resumen.csv, fig_cgsm_temporada.png

Comentarios en el código:

- línea 39: Dos regiones, declaradas (antes las cuatro clases se muestreaban sobre la caja del cubo,
- línea 40: 4.304 km2, sin decirlo: el 39 % de los puntos de agua caia en mar abierto y el 40 % de
- línea 41: los de humedal fuera del area de estudio).
- línea 42: AOI     : el poligono de la tesis, 2.042 km2. Manglar, humedal y agua salen de aqui.
- línea 43: CONTROL : la caja del cubo, 4.304 km2. El bosque seco de los piedemontes, que es el
- línea 44: control que no se inunda, esta fuera del AOI a proposito.
- línea 47: lluvia ERA5-Land y control de cobertura de cada pasada
- línea 60: lluvia diaria ERA5-Land sobre el AOI (mm), para acumular 30 dias antes de cada pasada
- línea 88: ------------------------------------------------------------------ NISAR local
- línea 125: cobertura sobre el AOI, no sobre la caja: una pasada que cubre el area de
- línea 126: estudio entera no debe descartarse por no cubrir el mar ni los piedemontes
- línea 152: ------------------------------------------------------------------ prueba
- línea 175: ------------------------------------------------------------------ figura
- línea 189: deja sitio al título general

### `figura_cgsm_optico.py`

Figura de contexto óptico para el informe de radar (inglés): Sentinel-2 en color natural
(B4, B3, B2) y en infrarrojo color (B8, B4, B3) junto a las composiciones NISAR de las mismas
dos fechas de la Figura 7 (río alto, 4-dic-2025; río más bajo, 9-ene-2026), sobre la CGSM.

Sentinel-2: COPERNICUS/S2_SR_HARMONIZED, mediana de las escenas a ±10 días de cada pasada,
enmascaradas con Cloud Score+ (cs >= 0,60). Se reportan además, para el texto, el NDVI mediano
del manglar de consenso y el área de agua abierta (MNDWI > 0) dentro del AOI en cada fecha.
El radar submuestreado y los PNG ópticos se guardan en C: para no depender de D:.

Salida: fig_cgsm_optico_radar.png y cgsm_optico_resumen.csv

### `figuras_informe.py`

Genera las figuras del informe del ejercicio polarimetrico desde los productos SNAP.

Lee los BEAM-DIMAP producidos por la cadena Calibrate -> T3 -> Refined Lee ->
Freeman-Durden -> Terrain Correction y escribe PNG en figuras/.

Comentarios en el código:

- línea 21: submuestreo para que las figuras pesen poco
- línea 73: T11 es potencia lineal (positiva); el coef. de variacion mide el speckle
- línea 106: los extremos (<5 y >80 grados) son artefactos de borde del DEM, no terreno real

## 7. Robustez y límites

### `autocorrelacion_temporal.py`

Comprueba si las correlaciones con la marea y con la lluvia estan infladas por dependencia temporal.

Spearman trata cada pasada como una observacion independiente. Si la serie de radar y la del
forzante (marea, lluvia de 30 dias) se parecen a si mismas de una pasada a la siguiente, las n
pasadas valen por menos. Para cada traza se mide la autocorrelacion de rezago 1 de las dos
series (sobre rangos, en orden de fecha) y se calcula el tamano efectivo de Pyper y Peterman
(1998): n_ef = n (1 - r1x r1y) / (1 + r1x r1y), acotado a n. El p se recalcula con n_ef.

La variable de radar es manglar menos bosque en copolarizacion, que es la que usa el informe.
No reentrena ni descarga nada: lee las tablas por fecha que ya estan en la carpeta.

USO: python autocorrelacion_temporal.py

Comentarios en el código:

- línea 22: archivo, columna de traza, forzante, copolarizacion, etiqueta

### `figura_incidencia.py`

Rehace fig_doble_rebote_incidencia.png desde doble_rebote_incidencia.csv, con los
tercios en posiciones fijas (T1 a T3) y los rotulos sin superposicion.

## 8. Clave de interpretación

### `figura_clave.py`

Figura de la clave de interpretacion: espacio de firmas de la CGSM en banda C y en
banda L. Eje x, copolar (VV o HH); eje y, cociente copolar menos cruzada, que separa
superficie de volumen. Un punto por clase, con la mediana entre pasadas.

Fuentes: cgsm_temporada_s1.csv (S1 D142, 61 pasadas), cgsm_temporada_nisar.csv (NISAR
traza D083, 12 pasadas) y nisar_flotante.csv para la vegetacion flotante del evento de
2025, que no es una clase de WorldCover y se define por la firma optica de dic-2025.
Salida: fig_clave_firmas.png

Comentarios en el código:

- línea 32: en banda C la flotante se mide en el compuesto de dic-2025 (ver nisar_flotante.py)
- línea 35: donde dos clases casi coinciden, cada etiqueta lleva su desplazamiento y su alineacion

### `nisar_flotante.py`

Banda L frente a banda C sobre la vegetacion flotante de 2025 (evento de Hydrilla).

PARA QUE. En la ventana del informe (oct-2025 a sep-2026) el 14 % de los puntos de agua
de WorldCover 2021 dentro del AOI se cubrio de vegetacion flotante. En Sentinel-1 esos
puntos estan 7,4 dB por encima del agua abierta (−13,3 frente a −20,6 dB en VV,
diciembre de 2025). La pregunta es si la banda L los separa igual, mejor o peor, que es
un aporte propio para la clave de interpretacion (objetivo especifico 4).

COMO. Los mismos 400 puntos de agua (WorldCover 80, AOI, semilla 42) se parten en dos
grupos con la firma optica de diciembre de 2025 (NDVI > 0,25 y NDWI < 0, la regla del
evento). Se leen los recortes GCOV de NISAR en D: y se reporta, por escena, la mediana
de HH, HV y HH−HV en cada grupo. Como referencia se incluye el manglar, que es volumen,
y el humedal herbaceo, que es la clase con la que la flotante se puede confundir.

Salida: nisar_flotante.csv y fig_nisar_flotante.png

Comentarios en el código:

- línea 103: ------------------------------------------------------------------ resumen
- línea 120: ------------------------------------------------------------------ figura

### `clave_vs_muestra2025.py`

La clave de interpretacion del avance de radar, sometida a la muestra de referencia 2025.

PARA QUE. La seccion "Clave de interpretacion por cobertura y mecanismo" del informe se construyo
con 400 puntos por clase de los productos globales (WorldCover 2021 y GMW 2020). La muestra 2025
(720 puntos, clase_final: revisada bajo el criterio v1 en los ids 1-400 y primera pasada en 401-720)
es la referencia propia que la clave no tenia. Aqui se mide, sobre esos 720 puntos y sin reajustar
ningun umbral:
  1. la firma por clase en las dos bandas (mediana entre pasadas del copolar, del cruzado y de su
     diferencia), comparable con la Tabla 10 del informe;
  2. la separabilidad por pares (Jeffries-Matusita) con banda C sola, banda L sola y las dos;
  3. la regla de lectura de cinco pasos, aplicada punto a punto como arbol de decision con los
     umbrales tal como estan escritos en el informe, contra clase_final (matriz de confusion y
     exactitud por clase). El paso 4 (manglar frente a bosque seco por respuesta hidrologica) y el
     paso 5 (firma de inundacion) son de series temporales, no de un pixel: no se aplican aqui.

DATOS. Sentinel-1 GRD IW, orbita descendente 142, oct-2025 a sep-2026, pasadas con cobertura >= 90 %
del AOI, VV y VH en dB tal como los entrega Earth Engine, valor del pixel de 10 m en cada punto y
mediana entre pasadas. NISAR L2 GCOV traza descendente 083, los recortes NISAR_AOI_*.h5 del disco
(gamma0 RTC -> sigma0 con rtcGammaToSigmaFactor, dB), media 3x3 y mediana entre pasadas; las
cinco escenas de la traza ascendente 007 se excluyen como en el informe.

USO: python clave_vs_muestra2025.py [s1] [nisar] [clave]
     sin argumentos corre todo. Salidas: clave_muestra2025_puntos.csv (valores por punto),
     clave_muestra2025_firmas.csv, clave_muestra2025_jm.csv, clave_muestra2025_regla.csv

Comentarios en el código:

- línea 40: mismo periodo que el informe
- línea 41: descendente, la de la Tabla 10
- línea 42: descendente 083
- línea 169: 1) firmas por clase
- línea 178: 2) separabilidad por pares
- línea 192: 3) regla de lectura

## 9. Mapa y corroboración óptica

### `mapa_doble_rebote.py`

Mapa de la senal de inundacion bajo dosel en la CGSM con NISAR (traza D083): diferencia
por pixel entre las pasadas de nivel alto del rio Magdalena y las de nivel bajo.

PARA QUE. La propuesta del curso promete "mapas de retrodispersion"; la prueba del nivel del
rio (cgsm_nivel_rio.py) es un numero por clase. Aqui la misma regla, alto menos bajo, se
aplica pixel a pixel para ver DONDE aparece el doble rebote y donde no.

COMO. Las 14 escenas NISAR_AOI_*D083*.h5 comparten la malla UTM 18N de 10 m (7590 x 6469).
Cada escena: gamma0 RTC -> sigma0 con rtcGammaToSigmaFactor, agregacion a 50 m por media de
bloques 5 x 5 en potencia, dB. Grupos: nivel alto = tercio alto de cgsm_nivel_rio.py (6
pasadas, oct-2025 a ene-2026) y nivel bajo = las 8 de jun a sep 2026; mediana por grupo y
diferencia alto - bajo para HH, HV y HH - HV. La mascara de manglar (WorldCover 95 y GMW
2020), bosque (WorldCover 10), humedal herbaceo (90) y agua (80) se descarga de Earth Engine
sobre la misma malla de 50 m. Se escriben la figura, un GeoTIFF con las tres diferencias y
un resumen por clase (mediana, cuartiles y fraccion de pixeles con diferencia positiva).

LIMITE. Los dos grupos coinciden con el periodo y con la version del producto (Beta frente a
Provisional); el mapa muestra la estructura espacial de la senal, no su causa.

USO: python mapa_doble_rebote.py        Salidas: fig_mapa_doble_rebote.png,
     mapa_doble_rebote_50m.tif, mapa_doble_rebote_resumen.csv

Comentarios en el código:

- línea 28: PostGIS deja un proj.db viejo en PROJ_DATA; rasterio necesita el suyo, y hay que fijarlo antes de importarlo
- línea 42: 5 x 5 pixeles de 10 m -> 50 m
- línea 100: esquina exterior del primer pixel de 10 m
- línea 125: Resumen por clase y, para el manglar, por sector de norte a sur
- línea 140: Figura: manglar a todo color, bosque de control atenuado, el resto en gris claro; sin contornos

### `mapa_doble_rebote_s1.py`

Mapa comparativo en banda C: el mismo "alto menos bajo" del nivel del rio que
mapa_doble_rebote.py hace con NISAR, ahora con Sentinel-1 GRD (orbita descendente 142) sobre
la misma malla de 50 m, para que la Figura del informe compare las dos bandas pixel a pixel.

COMO. En Earth Engine, pasadas de la orbita 142 en las mismas dos ventanas de fechas que los
grupos de NISAR (nivel alto: 20-oct-2025 a 15-ene-2026; nivel bajo: 20-jun a 30-sep-2026);
mediana de VV y VH (dB, como las sirve Earth Engine) por grupo, diferencia alto menos bajo,
promediada a 50 m (reduceResolution, media) y descargada sobre la malla UTM 18N del GeoTIFF de
NISAR. Resumen por clase y sector con la misma mascara. Figura de dos paneles: dHH de NISAR
y dVV de Sentinel-1 sobre manglar y bosque.

USO: python mapa_doble_rebote_s1.py   (requiere mapa_doble_rebote_50m.tif)
Salidas: mapa_s1_alto_bajo_50m.tif, mapa_doble_rebote_s1_resumen.csv, fig_mapa_c_vs_l.png

Comentarios en el código:

- línea 51: reduceResolution agota la memoria de Earth Engine con la mediana de 13 pasadas a 10 m; se usa
- línea 52: una media movil de 5 x 5 pixeles (50 m) en la malla nativa y se muestrea en la malla de 50 m

### `mapa_doble_rebote_malaga.py`

Mapa de la senal de doble rebote en Bahia de Malaga con NISAR: diferencia por pixel entre las
pasadas de marea alta y las de marea baja, por traza (A004 a las 05:46, D087 a las 18:29).

Mismo metodo que mapa_doble_rebote.py en la CGSM, con la marea como forzante: cada traza tiene
12 pasadas; se usan las 6 de marea mas alta y las 6 de marea mas baja en la pasada (marea de
perfil_pacifico_24.csv, columna marea_m), mediana por grupo y diferencia alta menos baja de HH,
HV y HH - HV. Las escenas de cada traza comparten malla UTM; las dos trazas se mapean por
separado y nunca se mezclan. Agregacion a 50 m (bloques 5 x 5 en potencia), sigma0 dB.
Mascara de clases (manglar WorldCover 95 y GMW 2020, bosque 10, humedal 90, agua 80) desde
Earth Engine sobre cada malla.

USO: python mapa_doble_rebote_malaga.py   (requiere D:\TESIS_DATACUBE\NISAR_PACIFICO)
Salidas: fig_mapa_doble_rebote_malaga.png, mapa_malaga_<traza>_50m.tif, mapa_doble_rebote_malaga_resumen.csv

### `corroboracion_dw.py`

Corroboracion optica de la inundacion bajo dosel con Dynamic World (Brown et al., 2022):
la clase "vegetacion inundada" (flooded_vegetation, probabilidad por pixel a 10 m) en las
fechas sin nubes de Sentinel-2, frente al nivel del rio y frente al mapa de NISAR.

DOS PRUEBAS.
  1. Temporal: para cada imagen de Dynamic World sobre el AOI entre oct-2025 y sep-2026, la
     probabilidad media de vegetacion inundada sobre el manglar (WorldCover 95 y GMW), el
     humedal herbaceo y el bosque de control, con la fraccion de pixeles validos (sin nube).
     Se conservan las fechas con cobertura >= COB_MIN sobre el manglar y se correlaciona
     (Spearman) con el nivel del rio en Remolino ese dia (IDEAM, nivel_ideam_instantaneo.csv).
  2. Espacial: mediana de la probabilidad por pixel en las fechas del grupo de nivel alto
     (20-oct-2025 a 15-ene-2026) y del grupo de nivel bajo (20-jun a 30-sep-2026), en la misma
     malla de 50 m de mapa_doble_rebote_50m.tif; diferencia alto - bajo y correlacion de
     Spearman con el dHH de NISAR sobre los pixeles de manglar con al menos 2 observaciones
     validas por grupo.

LIMITE. Dynamic World ve el dosel desde arriba: su "vegetacion inundada" responde a agua
visible entre vegetacion baja o abierta, no al agua bajo un dosel cerrado. Una correlacion
positiva corrobora; una nula no refuta.

USO: python corroboracion_dw.py      (requiere mapa_doble_rebote_50m.tif ya escrito)
Salidas: dw_serie.csv, dw_resumen.txt, fig_corroboracion_dw.png, dw_alto_bajo_50m.tif

Comentarios en el código:

- línea 29: PostGIS deja un proj.db viejo en PROJ_DATA; rasterio necesita el suyo, y hay que fijarlo antes de importarlo
- línea 86: una fila por fecha (varias teselas S2 el mismo dia): media ponderada por cobertura
- línea 119: relee dw_serie.csv y dw_alto_bajo_50m.tif
- línea 120: 1. temporal
- línea 138: 2. espacial
- línea 168: figura: serie temporal y mapa de dDW sobre manglar + dispersion

### `mapbiomas_cruce.py`

Cruce exploratorio de MapBiomas Colombia (coleccion 2, clasificacion 2023, 30 m) con la
referencia del informe de radar y con la muestra 2025 de la tesis.

Tres preguntas:
  1. Sobre la malla de 50 m del mapa de NISAR, que dice el dHH (alto menos bajo del rio) en las
     clases de MapBiomas manglar (5), bosque inundable (6) y formacion herbacea inundable (11),
     y cuanto coinciden esas clases con las de WorldCover/GMW usadas en el informe.
  2. Como etiqueta MapBiomas 2023 los 720 puntos de la muestra 2025 (clase_final): si separa el
     humedal herbaceo del manglar degradado mejor que WorldCover.
  3. Hectareas por clase de MapBiomas dentro del AOI, 2015 a 2023, para la serie de la tesis.

Codigos de la leyenda MapBiomas Colombia col. 2 (verificar en el sitio antes de citar):
  3 bosque, 5 manglar, 6 bosque inundable, 11 formacion herbacea inundable, 21 mosaico
  agropecuario, 23 playas y dunas, 24 infraestructura urbana, 25 otras areas sin vegetacion,
  33 rio, lago y oceano, 35 palma aceitera.

USO: python mapbiomas_cruce.py      Salidas: mapbiomas_cruce_resumen.txt, mapbiomas_aoi_serie.csv

Comentarios en el código:

- línea 45: 1. malla de 50 m del mapa NISAR
- línea 70: 2. los 720 puntos
- línea 84: 3. serie anual en el AOI

## Informe y figuras de método

### `md_a_word.py`

Convierte un markdown del curso de radar a .docx: carta, margenes 2,5 cm, Calibri 11,
cuerpo justificado, encabezados en negrita sin numerar, tablas con encabezado sombreado.
El bloque de cabecera (lineas antes del primer '## ') va centrado, la ultima en negrita.

USO
    python md_a_word.py Avance_proyecto_radar.md

### `propuesta_a_word.py`

Convierte Propuesta_trabajo_radar.md en .docx: carta, margenes 2,5 cm, Calibri 11,
justificado, titulos en negrita sin numerar.

### `construir_informe.py`

Ensambla el informe HTML autocontenido incrustando las figuras en base64.

Lee plantilla_informe.html (con marcadores {{IMG:archivo}}) y escribe
informe_radar.html con las imagenes embebidas como data URI.

### `figura_flujo.py`

Diagrama del flujo de trabajo del avance de radar, en ingles, para el informe.

Sigue la convencion vista en clase (semana 5: De Luca et al. 2021, Yordanov y Brovelli
2021): flujo vertical por etapas, cada etapa con las operaciones que ejecuta, los
productos intermedios a la izquierda con sus conteos y el software a la derecha con
barras que marcan en que etapas interviene. Al pie de cada etapa, en monoespaciada
azul, los guiones de RADAR/ (los numerados, de AVANCE TESIS/PUBLICACION_GEE/) que la
ejecutan. Las cifras son las del informe.

Esta pensado para la pagina: md_a_word.py inserta las figuras a 6,3 pulgadas de ancho,
de modo que la figura se dibuja a ese ancho y con letra de 6,8 pt para que se imprima
tal cual. La altura se calcula del texto y se avisa si supera lo que cabe en una
pagina carta con margenes de 2,5 cm (unas 8,4 pulgadas con leyenda).

USO
    python figura_flujo.py             -> fig_flujo_trabajo.png (resumen: una linea por etapa, Figura 1)
    python figura_flujo.py --detalle   -> fig_flujo_trabajo_detalle.png (todas las operaciones, anexo)

Comentarios en el código:

- línea 42: geometria en pulgadas (1 unidad de eje = 1 pulgada)
- línea 44: productos intermedios
- línea 45: etapas (sin barras de software en el resumen)
- línea 46: barras de software
- línea 48: caracteres por linea de vineta
- línea 50: lineas de vineta, para medir desbordes
- línea 51: alto de linea
- línea 52: separacion entre etapas
- línea 112: ------------------------------------------------------------------ cabecera
- línea 119: ------------------------------------------------------------------ etapas
- línea 198: ------------------------------------------------------------------ software

### `figura_cadena_sar.py`

Cadena de procesamiento SAR del avance de radar, por sensor, en ingles (Figura A1 del anexo).

Convencion de la semana 5 (De Luca et al. 2021; Yordanov y Brovelli 2021): flujo vertical
por etapas, cada etapa abierta en tres columnas, una por sensor (NISAR, ALOS-2, Sentinel-1),
productos intermedios a la izquierda con sus conteos y barras de software a la derecha.
Cubre solo las etapas 1 a 3 del metodo (Figura 1): adquisicion, calibracion radiometrica,
promediado espacial y conversion a dB, geometria por pasada y extraccion en los puntos.
Las cifras son las del informe (Tabla 1 y texto).

USO
    python figura_cadena_sar.py      -> fig_cadena_sar.png

Comentarios en el código:

- línea 32: productos
- línea 33: etapas
- línea 34: barras de software
- línea 39: caracteres por linea dentro de cada columna de sensor
- línea 65: titulo de la etapa sobre las tres columnas
- línea 101: cabecera de sensores
- línea 157: cada columna de sensor termina en su propio borde

### `figura_muestra_2025.py`

Figura de la muestra de referencia de 2025 sobre el AOI de la CGSM: los 720 puntos por clase
final, la reserva de validacion (que la muestra no toca) y los bloques de 12 km de la validacion
cruzada. Para la seccion 2.7 del informe de radar (y reutilizable en la tesis).

Fuentes: AVANCE TESIS/MUESTRA_2025/etiquetas_2025.csv (clase_final, lon, lat), pliegues_cv.csv
(bloque12), reserva_validacion.geojson; AOI desde el asset de Earth Engine.
USO: python figura_muestra_2025.py   -> fig_muestra_2025.png

Comentarios en el código:

- línea 48: bloques de 12 km del esquema de validacion cruzada (codigo = floor(x/12km)*10000 + floor(y/12km))

### `figura_consistencia.py`

Figura de la prueba de consistencia de la interprete (muestra 2025): matriz de la clase de
referencia (clase_final, criterio v1) frente a la segunda pasada a ciegas, con acuerdo, Wilson y
kappa en el titulo. Solo agregados; nunca ids. Para los limites de la clave del informe de radar.

Requiere la exportacion consistencia/consistencia_2025_n*.csv de la app. Si no existe, avisa y sale.
USO: python figura_consistencia.py   -> fig_consistencia_2025.png

## Otros

### `figura_diseno.py`

Figura 1 del informe: diseño analítico del estudio en seis filas, esquemático, con dos
miniaturas reales (recorte HH de NISAR y malla de clases a 50 m). Nada ilustrativo ni inventado.

USO: python figura_diseno.py   -> fig_diseno_estudio.png
Lee: D:\TESIS_DATACUBE\NISAR\NISAR_AOI_20251029_083_4.h5 y mapa_doble_rebote_50m.tif.

Comentarios en el código:

- línea 49: ---------- 1. datos de entrada (y 72-99)
- línea 75: ---------- 2. preprocesamiento (y 57-70)
- línea 89: ---------- 3. muestreo (y 40-53.5)
- línea 107: ---------- 4. forzante (y 31-38)
- línea 113: ---------- 5. pruebas (y 17-29)
- línea 124: ---------- 6. productos (y 3-15)
