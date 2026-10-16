# Documentación de los scripts

Cabecera y comentarios de cada script, extraídos del código con `generar_documentacion.py`, en el orden del flujo de trabajo del informe. Cada cabecera dice qué hace el script, qué lee, qué escribe y cómo se corre.

## Convenciones de redacción

- script, no guion, para los archivos de Python.
- bosque no inundable de referencia, no bosque de control, al describir el método.
- forzante hidrológico, para coincidir con el informe.
- diferencia HH − HV o VV − VH, nunca cociente.
- contraste óptico para Dynamic World, no corroboración ni validación de la inundación bajo dosel.
- señal compatible con doble rebote o respuesta copolar asociada al estado hidrológico; una imagen de intensidad no identifica por sí sola el mecanismo.
- la diferencia manglar − bosque controla variaciones temporales compartidas; no se afirma que elimine la estacionalidad.
- el nivel de Remolino es un indicador regional del estado hidrológico, no una medida del nivel dentro del manglar.

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

AUTENTICACION. Earthdata exige usuario y contraseña. Este script NO los pide ni los
guarda: usa la libreria earthaccess, que lee las credenciales de ~/.netrc (o de
las variables EARTHDATA_USERNAME / EARTHDATA_PASSWORD) o abre el flujo de login
interactivo en la terminal del usuario. Ejecutar desde su terminal, no desde el agente.

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
son las que necesita la ablacion; despues las demás.

AUTENTICACION. Como en 17_descargar_nisar.py: earthaccess lee ~/.netrc o pregunta
en la terminal; este script no maneja contraseñas. Ejecutar desde la terminal del usuario.

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

AUTENTICACION. earthaccess pregunta en la terminal; este script no maneja
contraseñas. Ejecutar desde la terminal del usuario.

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

AUTENTICACION: earthaccess pregunta en la terminal. Ejecutar desde la terminal del usuario.

USO
    python 24_nisar_recorte_cgsm.py        # todas las que falten
    python 24_nisar_recorte_cgsm.py 3      # como maximo tres en esta corrida

### `nivel_ideam_descarga.py`

Descarga las series de nivel hidrológico del IDEAM usadas para caracterizar la condición
hidrológica de la CGSM.

PROPÓSITO
Obtener el nivel del río Magdalena en la estación automática Remolino y evaluar otras estaciones
disponibles como posibles referencias hidrológicas. El nivel de Remolino se usa como indicador
regional del estado hidrológico de la CGSM y complementa el análisis exploratorio basado en la
precipitación antecedente de ERA5-Land.

FUENTE
Datos Abiertos Colombia, IDEAM, a través de la API Socrata.

SALIDAS
- nivel_ideam_<dataset>.csv
- nivel_ideam_resumen.txt

USO
    python nivel_ideam_descarga.py

Comentarios en el código:

- línea 60: Nivel del mar en el Caribe (por si hay mareógrafo cerca de la CGSM)

## 2. Preprocesamiento y calibración

### `publicacion_gee/20_nisar_incidencia.py`

Anade el angulo de incidencia a los recortes NISAR que no lo traen.

Los dos primeros recortes (2025-12-04 y 2025-12-16) se hicieron antes de que
18_nisar_recorte_remoto.py copiara la malla de metadatos radarGrid. El angulo hace
falta para estratificar el doble rebote (umbral de 35 grados). Se lee solo esa
malla gruesa del producto remoto, que pesa poco, y se escribe dentro del recorte.

Como los demás scripts de descarga, usa la sesión Earthdata del usuario; correr desde
su terminal.

USO
    python 20_nisar_incidencia.py

### `alos2_marea_malaga.py`

Corroboración independiente de la respuesta a la marea con ALOS-2 PALSAR-2 ScanSAR en banda L
sobre Bahía de Málaga.

PROPÓSITO
Evaluar si la respuesta observada con NISAR se reproduce con otro sensor de banda L. El análisis
usa HH y HV y mantiene separadas las trayectorias para no mezclar geometrías de adquisición.
La comparación con Sentinel-1 evalúa si existe una respuesta equivalente en banda C, aunque no
separa del todo el efecto de la longitud de onda del de la polarización, porque Sentinel-1
observa VV y VH y ALOS-2 HH y HV.

DATOS
ALOS-2 PALSAR-2 ScanSAR Level 2.2 en Google Earth Engine, 25 m, enero de 2025 a septiembre de
2026. Los DN se convierten a sigma cero con sigma0_dB = 10 * log10(DN**2) - 83. Los cuadros de
una misma pasada se mosaican y las observaciones se agrupan por trayectoria. Se usan los mismos
1.600 puntos de referencia y la misma serie de marea del análisis con NISAR.

SALIDAS
- alos2_marea_malaga.csv
- alos2_marea_resumen.csv
- fig_alos2_marea.png

USO
    python alos2_marea_malaga.py

Comentarios en el código:

- línea 27: gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
- línea 68: gamma cero con el angulo local de incidencia LIN (centesimas de grado)
- línea 74: algunas escenas son solo HH

### `s1_marea_malaga.py`

La misma prueba de marea con Sentinel-1 (banda C) sobre Bahía de Málaga.

Toma todas las escenas Sentinel-1 GRD IW (VV, VH, sigma cero en dB, corregidas por
terreno en Earth Engine) que cubren la caja entre oct-2025 y sep-2026, las agrupa por
órbita relativa (cada órbita tiene su hora y su geometria, como las trazas de NISAR),
muestrea los mismos 1.600 puntos (manglar de consenso, bosque, humedal, agua; semilla
42) y asigna a cada escena la marea predicha a SU hora de adquisicion. Luego aplica
la misma regla que marea_vs_radar.py: manglar menos bosque contra marea, diferencia
alta-baja y Spearman, por órbita.

Ademas restringe a las escenas a +-3 dias de una pasada NISAR para la comparacion
directa "mismas fechas".

Salidas: s1_marea_malaga.csv (por escena y clase), s1_marea_resumen.csv, fig_s1_marea.png

Comentarios en el código:

- línea 18: gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
- línea 40: --- puntos, identicos a perfil_pacifico_24.py
- línea 51: --- marea
- línea 62: --- escenas S1
- línea 68: una pasada = todos los cuadros de la misma órbita con menos de 5 minutos entre si;
- línea 69: se mosaican, porque los cuadros parten la caja (80 % + 20 %)
- línea 96: --- mismas fechas que NISAR (+-3 dias)
- línea 102: --- prueba por órbita
- línea 129: --- figura

## 3. Coberturas de referencia y muestreo

### `perfil_pacifico.py`

Primer perfil de retrodispersión NISAR sobre Bahía de Málaga: mediana de HH, HV y
HH-HV (dB, sigma cero) por cobertura de WorldCover 2021 y por escena, con el ángulo
de incidencia. Valida ademas los recortes (proyeccion, tamano, cobertura).

Coberturas: manglar (95), agua (80), bosque (10), humedal herbaceo (90).
Puntos: 400 por clase, muestreados en Earth Engine dentro de la caja del recorte.

Comentarios en el código:

- línea 28: --- puntos por clase desde WorldCover, dentro de la caja del AOI
- línea 38: --- segunda mascara de manglar, independiente: Global Mangrove Watch v3, extension 2020
- línea 47: puntos donde los dos productos coinciden en manglar, y donde solo uno lo dice
- línea 102: --- Dynamic World: probabilidad de vegetación inundada y de agua en los mismos puntos,
- línea 103: con las imagenes de +-10 dias alrededor de cada escena NISAR (el Pacifico es nuboso)
- línea 121: label 2 = flooded_vegetation

### `perfil_pacifico_24.py`

Paso 1 del trabajo de radar: perfil de retrodispersión NISAR sobre Bahía de Málaga
con las 24 escenas (12 ascendentes A004, 05:00 local; 12 descendentes D087, 18:00
local), por cobertura y por traza, con columna de marea lista para llenar.

COBERTURAS (400 puntos cada una, semilla 42): manglar = consenso WorldCover 2021 (95)
y Global Mangrove Watch 2020; bosque (WC 10) como control que no se inunda; humedal
herbaceo (WC 90); agua (WC 80).

MAREA. Si existe mareas_buenaventura.csv (columnas: fecha_hora_utc en formato
YYYY-MM-DD HH:MM, altura_m), se asigna a cada pasada la altura interpolada a la hora
exacta de adquisicion. Si no existe, la columna queda vacia y el script lo dice.

SALIDAS (en RADAR/):
  perfil_pacifico_24.csv     mediana e IQR de HH, HV, HH-HV por escena y clase, con traza,
                             hora local, incidencia y marea
  fig_perfil_pacifico_24.png serie temporal por traza (ingles)
  resumen en consola: diferencia entre trazas por clase y variacion dentro de cada traza

USO
    python perfil_pacifico_24.py

Comentarios en el código:

- línea 25: gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
- línea 50: ----------------------------------------------------------------- puntos por clase
- línea 65: ----------------------------------------------------------------- marea (opcional)
- línea 81: segundos desde la epoca sin depender de la resolucion interna del datetime (pandas 3 usa microsegundos)
- línea 94: ----------------------------------------------------------------- lectura de escenas
- línea 139: ----------------------------------------------------------------- resumen
- línea 156: ----------------------------------------------------------------- figura
- línea 166: la linea se corta donde hay más de 40 dias sin escenas (hueco feb-jun), para no
- línea 167: dibujar una tendencia que no se observo

### `doble_rebote_incidencia.py`

Análisis de robustez de la respuesta hidrológica de NISAR frente al ángulo de incidencia en
Bahía de Málaga.

PROPÓSITO
Comprobar si la respuesta del manglar relativa al bosque se mantiene al estratificar las
observaciones por ángulo de incidencia.

MÉTODO
Dentro de cada trayectoria, los puntos de manglar se dividen en tres terciles de incidencia y los
mismos límites angulares se aplican al bosque de referencia. Para cada tercil se calcula la
correlación de Spearman entre la altura de marea y la mediana de HH, HV y HH-HV, y además la
diferencia manglar - bosque de cada fecha. El análisis evalúa la estabilidad de la respuesta
frente a la geometría local. Por el rango angular reducido dentro de cada trayectoria, no se usa
para establecer una relación general entre la magnitud del efecto y el ángulo de incidencia.

ENTRADAS
- 24 recortes NISAR de Bahía de Málaga
- mareas_buenaventura.csv

SALIDAS
- doble_rebote_incidencia.csv
- fig_doble_rebote_incidencia.png

USO
    python doble_rebote_incidencia.py

Comentarios en el código:

- línea 71: valores por punto y escena
- línea 99: tercios de incidencia por traza (definidos sobre los puntos de manglar; el bosque usa los mismos cortes)

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

Figuras de mapa para el informe de radar, Bahía de Málaga (ingles).

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
retrodispersión) usando COPERNICUS/S1_GRD sobre AOI_tesis_CGSM_v1 en vez del
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
Málaga) en la serie cada 10 minutos que lee perfil_pacifico_24.py, y la compara con
la predicción armonica propia.

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
- línea 71: serie de trabajo: oficial donde existe, predicción propia fuera de su cobertura
- línea 87: comparacion con la predicción propia en las 24 pasadas NISAR

### `marea_vs_radar.py`

Relación entre la altura de marea y la retrodispersión NISAR del manglar en Bahía de Málaga,
analizada por trayectoria y con el bosque no inundable como referencia.

REGLA DE LECTURA
La regla se definió antes del análisis. Si la banda L responde al agua bajo el dosel, dentro de
una misma trayectoria se espera un aumento de HH y de HH-HV en el manglar con la altura de marea,
sin una respuesta equivalente en el bosque no inundable ni en HV. Para cada trayectoria se
comparan las adquisiciones por encima y por debajo de la mediana de marea y se calcula la
correlación de Spearman entre la marea y la retrodispersión. La diferencia manglar - bosque se
calcula fecha a fecha para controlar las variaciones temporales compartidas por las dos coberturas.

ENTRADA
perfil_pacifico_24.csv y la serie de marea asignada a cada pasada.

SALIDAS
- marea_vs_radar.csv
- fig_marea_vs_radar.png

USO
    python marea_vs_radar.py

Comentarios en el código:

- línea 24: gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
- línea 53: manglar menos bosque, fecha a fecha: descuenta lo estacional

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

- línea 16: gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
- línea 32: 1. Serie de nivel: se prefiere el instantáneo; si no hay, el máximo diario.
- línea 51: Las fechas del IDEAM son hora local (UTC−5); las pasadas de radar vienen en UTC.
- línea 54: segundos, sin depender de la resolución interna
- línea 65: 2. Pasadas de radar por sensor y traza.
- línea 68: las copias _CAJA son la región anterior, no se mezclan
- línea 80: las pasadas de una traza varían un minuto
- línea 107: 3. Figura.

## 5 y 6. Estadística por pasada y prueba hidrológica

### `cgsm_temporada.py`

Análisis inicial de la respuesta hidrológica de las coberturas de la CGSM.

PROPÓSITO
Evaluar la relación entre la retrodispersión SAR y la precipitación acumulada en los 30 días
anteriores a cada adquisición, obtenida de ERA5-Land. Se conserva la partición estacional entre
época seca y húmeda como descripción complementaria.

MÉTODO
Para cada sensor y trayectoria se calcula la mediana de retrodispersión por cobertura. La señal
del manglar se analiza de forma individual y relativa al bosque no inundable mediante la
diferencia manglar - bosque. Se usan cuatro coberturas de referencia, manglar, bosque no
inundable, humedal herbáceo y agua, con 400 puntos por clase.

SENSORES
- NISAR: HH y HV (recortes locales NISAR_AOI_*.h5).
- Sentinel-1: VV y VH (Earth Engine).
- ALOS-2: HH y HV (Earth Engine).

SALIDAS
- cgsm_temporada_<sensor>.csv
- cgsm_temporada_resumen.csv
- fig_cgsm_temporada.png

USO
    python cgsm_temporada.py

Comentarios en el código:

- línea 30: gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
- línea 52: Dos regiones, declaradas (antes las cuatro clases se muestreaban sobre la caja del cubo,
- línea 53: 4.304 km2, sin decirlo: el 39 % de los puntos de agua caia en mar abierto y el 40 % de
- línea 54: los de humedal fuera del area de estudio).
- línea 55: AOI     : el poligono de la tesis, 2.042 km2. Manglar, humedal y agua salen de aqui.
- línea 56: CONTROL : la caja del cubo, 4.304 km2. El bosque seco de los piedemontes, que es el
- línea 57: control que no se inunda, esta fuera del AOI a proposito.
- línea 60: lluvia ERA5-Land y control de cobertura de cada pasada
- línea 73: lluvia diaria ERA5-Land sobre el AOI (mm), para acumular 30 dias antes de cada pasada
- línea 101: ------------------------------------------------------------------ NISAR local
- línea 138: cobertura sobre el AOI, no sobre la caja: una pasada que cubre el area de
- línea 139: estudio entera no debe descartarse por no cubrir el mar ni los piedemontes
- línea 165: ------------------------------------------------------------------ prueba
- línea 188: ------------------------------------------------------------------ figura
- línea 202: deja sitio al título general

### `figura_cgsm_optico.py`

Genera la comparación óptica y radar de las dos adquisiciones NISAR de la Figura 9 del informe
(CGSM).

La figura combina Sentinel-2 en color natural (B4, B3, B2) e infrarrojo color (B8, B4, B3) con
las composiciones NISAR de las mismas fechas, 4 de diciembre de 2025 y 9 de enero de 2026.
Sentinel-2 usa COPERNICUS/S2_SR_HARMONIZED y la mediana de las adquisiciones dentro de 10 días
de cada fecha NISAR, enmascaradas con Cloud Score+ (cs >= 0,60). Además de la figura, el script
calcula el NDVI mediano del manglar de consenso y la proporción de agua abierta dentro del área
de estudio.

SALIDAS
- fig_cgsm_optico_radar.png
- cgsm_optico_resumen.csv

USO
    python figura_cgsm_optico.py

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

Evalúa la sensibilidad de las correlaciones hidrológicas a la dependencia temporal entre
adquisiciones.

Spearman supone observaciones independientes. Cuando el forzante y la señal SAR presentan
autocorrelación temporal, el número de observaciones independientes puede ser menor que el
número nominal de pasadas. Para cada serie se estima el tamaño efectivo de muestra de Pyper y
Peterman (1998) de dos formas: con la autocorrelación de rezago 1 (n_ef, p_ef) y con todos los
rezagos hasta n/5 (n_ef_rezagos, p_ef_rezagos), que es la versión que reporta el informe. Los
valores p se recalculan con el tamaño efectivo. La variable SAR es la señal copolar del manglar
relativa al bosque. El script trabaja solo con las tablas ya generadas y no descarga ni reprocesa
imágenes.

ENTRADAS
perfil_pacifico_24.csv, s1_marea_malaga.csv, alos2_marea_malaga.csv, cgsm_temporada_*.csv y la
serie de nivel del río.

SALIDA
autocorrelacion_temporal.csv, base de la tabla de dependencia temporal del informe.

USO
    python autocorrelacion_temporal.py

Comentarios en el código:

- línea 31: archivo, columna de traza, forzante, copolarizacion, etiqueta

### `pendientes_auditoria.py`

Cuatro análisis pendientes de la auditoría del informe 1 (revisión externa del 2026-10-14).

PROPÓSITO
    A. Estadístico primario por sitio (resta copolar manglar − bosque frente al forzante), corrección de
       Holm sobre la familia de pruebas de banda L y pendientes en dB por metro con intervalo bootstrap.
    B. Borde frente a interior del manglar: cambio copolar entre periodos de nivel alto y bajo según la
       distancia del píxel de 50 m al borde del manglar (CGSM, NISAR D083) y a la marea (Málaga, A004 y D087).
    C. Separabilidad de Jeffries-Matusita con dos variables por banda (copolar y cruzada), sin la diferencia
       copolar − cruzada, que es combinación lineal de las otras dos y deja la covarianza singular.
    D. Clave de lectura con banda C sola frente a C + L: la decisión dosel cerrado / abierto con VV − VH en
       vez de HH − HV, con el umbral elegido por resustitución igual que el 7,3 dB de la clave.
ENTRADAS
    perfil_pacifico_24.csv, alos2_marea_malaga.csv, s1_marea_malaga.csv, cgsm_temporada_nisar.csv,
    cgsm_temporada_s1.csv, nivel_ideam_instantaneo.csv, autocorrelacion_temporal.csv,
    mapa_doble_rebote_50m.tif, mapa_malaga_A004_50m.tif, mapa_malaga_D087_50m.tif, clave_muestra2025_puntos.csv.
SALIDAS
    pendientes_auditoria_pendientes.csv, pendientes_auditoria_borde.csv, pendientes_auditoria_jm2.csv,
    pendientes_auditoria_clave_c.csv, fig_borde_interior.png y resumen en pantalla.
USO
    python pendientes_auditoria.py

Comentarios en el código:

- línea 40: réplicas bootstrap
- línea 46: ============================================================ A. estadístico primario, Holm y pendientes
- línea 113: p corregido por dependencia temporal (Tabla 7), tomado de autocorrelacion_temporal.csv
- línea 131: Familia primaria: las pruebas de banda L (4 de Málaga + CGSM D083); Holm sobre el p corregido por dependencia temporal
- línea 145: ============================================================ B. borde frente a interior
- línea 155: distancia de cada píxel de manglar al píxel no manglar más cercano
- línea 156: distancia al agua abierta
- línea 164: manglar a esa distancia del agua
- línea 171: correlación continua distancia al borde frente a cambio, manglar del grupo
- línea 188: figura: mediana e IQR por banda de distancia al borde, tres paneles
- línea 204: ============================================================ C. JM con dos variables
- línea 234: ============================================================ D. clave con C sola frente a C + L
- línea 257: umbral de VV − VH por resustitución: el que maximiza el acierto balanceado intacto frente a las tres clases de dosel abierto
- línea 262: 1: cerrado si VV−VH < u (como la L); −1: cerrado si VV−VH >= u
- línea 267: la misma búsqueda para HH − HV, para comparar con el 7,3 fijado en el informe

### `figura_incidencia.py`

Rehace fig_doble_rebote_incidencia.png desde doble_rebote_incidencia.csv, con los
tercios en posiciones fijas (T1 a T3) y los rotulos sin superposicion.

## 8. Clave de interpretación

### `figura_clave.py`

Genera el espacio de firmas usado para la clave de interpretación de la CGSM.

El eje x representa la retrodispersión copolar (VV en banda C o HH en banda L) y el eje y la
diferencia copolar - cruzada (VV-VH o HH-HV), en dB. Cada cobertura se representa por la mediana
multifecha de las dos variables.

FUENTES
- cgsm_temporada_s1.csv
- cgsm_temporada_nisar.csv
- nisar_flotante.csv

SALIDA
fig_clave_firmas.png

USO
    python figura_clave.py

Comentarios en el código:

- línea 40: en banda C la flotante se mide en el compuesto de dic-2025 (ver nisar_flotante.py)
- línea 43: donde dos clases casi coinciden, cada etiqueta lleva su desplazamiento y su alineacion

### `nisar_flotante.py`

Banda L frente a banda C sobre la vegetación flotante de 2025 (evento de Hydrilla).

PARA QUE. En la ventana del informe (oct-2025 a sep-2026) el 14 % de los puntos de agua
de WorldCover 2021 dentro del AOI se cubrio de vegetación flotante. En Sentinel-1 esos
puntos estan 7,4 dB por encima del agua abierta (−13,3 frente a −20,6 dB en VV,
diciembre de 2025). La pregunta es si la banda L los separa igual, mejor o peor, que es
un aporte propio para la clave de interpretación (objetivo especifico 4).

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

Evalúa la clave de interpretación SAR con la muestra de referencia de 2025.

PROPÓSITO
Contrastar las firmas y los umbrales derivados inicialmente de las coberturas de referencia con
una muestra propia de 720 puntos distribuidos en seis clases.

ANÁLISIS
1. Firmas multifecha por clase en bandas C y L: copolar, cruzada y diferencia copolar - cruzada.
2. Separabilidad de Jeffries-Matusita entre pares de clases con banda C, banda L y las dos.
3. Aplicación punto a punto de las cuatro decisiones estáticas de la clave y comparación con la
   clase de referencia: agua abierta (VV < -17 dB y VH < -25 dB); superficie oscura con
   vegetación o borde (VV < -12 dB), compatible con vegetación flotante si VV-VH >= 6,5 dB y sin
   decisión en caso contrario; dosel cerrado (VV >= -12 dB y HH-HV < 7,3 dB); dosel abierto o
   herbáceo (VV >= -12 dB y HH-HV >= 7,3 dB). La respuesta hidrológica que distingue manglar de
   bosque no inundable es de series temporales y no se evalúa a escala de punto.

IMPORTANTE
Los umbrales se definen y se evalúan con la misma muestra de 720 puntos, de modo que las métricas
corresponden a resustitución y no a validación independiente.

DATOS
Sentinel-1 GRD, órbita descendente 142, y NISAR L2 GCOV, trayectoria descendente D083, en el
periodo del informe. Valor del píxel de 10 m en cada punto (media 3 x 3 en NISAR) y mediana
entre pasadas.

USO
    python clave_vs_muestra2025.py [s1] [nisar] [clave]
Sin argumentos ejecuta el flujo completo. Salidas: clave_muestra2025_puntos.csv,
clave_muestra2025_firmas.csv, clave_muestra2025_jm.csv y clave_muestra2025_regla.csv.

Comentarios en el código:

- línea 34: gamma cero: NISAR sin factor, S1 y ALOS-2 corregidos por incidencia
- línea 47: mismo periodo que el informe
- línea 48: descendente, la de la Tabla 10
- línea 49: descendente 083
- línea 160: Umbrales absolutos de la clave (dB). En gamma cero se desplazan por la mediana de gamma - sigma medida en los
- línea 161: mismos 720 puntos (banda C: VV y VH), de modo que los umbrales equivalgan a los literales del informe en sigma cero.
- línea 195: 1) firmas por clase
- línea 204: 2) separabilidad por pares
- línea 218: 3) regla de lectura

## 9. Mapa y corroboración óptica

### `mapa_doble_rebote.py`

Cartografía del cambio de retrodispersión asociado al contraste hidrológico en la CGSM con
NISAR D083.

PROPÓSITO
Representar espacialmente la diferencia de retrodispersión entre los grupos de nivel alto y bajo
del río Magdalena y evaluar dónde se concentra la respuesta copolar observada en el análisis por
clases.

MÉTODO
Las 14 adquisiciones NISAR D083 se convierten de gamma cero RTC a sigma cero y se agregan a una
malla de 50 m por bloques de 5 x 5 píxeles en potencia. Se calculan las medianas de los grupos de
nivel alto y bajo y su diferencia para HH, HV y HH-HV. Los resultados se resumen por cobertura y,
para el manglar, por sector geográfico.

LIMITACIÓN
Los grupos de nivel alto y bajo coinciden con periodos y versiones distintas del producto NISAR
(Beta y Provisional). El mapa describe la estructura espacial de la señal observada, pero no
permite atribuirla de forma independiente al cambio de nivel del río.

SALIDAS
- fig_mapa_doble_rebote.png
- mapa_doble_rebote_50m.tif
- mapa_doble_rebote_resumen.csv

USO
    python mapa_doble_rebote.py [--desde-tif]

Comentarios en el código:

- línea 33: PostGIS deja un proj.db viejo en PROJ_DATA; rasterio necesita el suyo, y hay que fijarlo antes de importarlo
- línea 47: 5 x 5 pixeles de 10 m -> 50 m
- línea 105: esquina exterior del primer pixel de 10 m
- línea 130: Resumen por clase y, para el manglar, por sector de norte a sur
- línea 145: Figura: manglar a todo color, bosque no inundable de referencia atenuado, el resto en gris claro; sin contornos

### `mapa_doble_rebote_s1.py`

Mapa comparativo en banda C: el mismo "alto menos bajo" del nivel del rio que
mapa_doble_rebote.py hace con NISAR, ahora con Sentinel-1 GRD (órbita descendente 142) sobre
la misma malla de 50 m, para que la Figura del informe compare las dos bandas píxel a píxel.

COMO. En Earth Engine, pasadas de la órbita 142 en las mismas dos ventanas de fechas que los
grupos de NISAR (nivel alto: 20-oct-2025 a 15-ene-2026; nivel bajo: 20-jun a 30-sep-2026);
mediana de VV y VH (dB, como las sirve Earth Engine) por grupo, diferencia alto menos bajo,
promediada a 50 m (reduceResolution, media) y descargada sobre la malla UTM 18N del GeoTIFF de
NISAR. Resumen por clase y sector con la misma mascara. Figura de dos paneles: dHH de NISAR
y dVV de Sentinel-1 sobre manglar y bosque.

USO: python mapa_doble_rebote_s1.py   (requiere mapa_doble_rebote_50m.tif)
Salidas: mapa_s1_alto_bajo_50m.tif, mapa_doble_rebote_s1_resumen.csv, fig_mapa_c_vs_l.png

Comentarios en el código:

- línea 51: reduceResolution agota la memoria de Earth Engine con la mediana de 13 pasadas a 10 m; se usa
- línea 52: una media movil de 5 x 5 píxeles (50 m) en la malla nativa y se muestrea en la malla de 50 m

### `mapa_doble_rebote_malaga.py`

Cartografía del cambio de retrodispersión entre marea alta y baja en Bahía de Málaga con NISAR.

Para cada trayectoria se seleccionan las seis adquisiciones de mayor marea y las seis de menor
marea, se calculan las medianas de los dos grupos y la diferencia alta - baja para HH, HV y
HH-HV. Las trayectorias A004 y D087 se procesan por separado para no mezclar geometrías de
adquisición. Los resultados se agregan a 50 m y se resumen para manglar, bosque no inundable,
humedal herbáceo y agua.

SALIDAS
- fig_mapa_doble_rebote_malaga.png
- mapa_malaga_<traza>_50m.tif
- mapa_doble_rebote_malaga_resumen.csv

USO
    python mapa_doble_rebote_malaga.py

### `corroboracion_dw.py`

Contraste óptico de la respuesta hidrológica con Dynamic World (Brown et al., 2022).

PROPÓSITO
Comparar la señal SAR con la probabilidad de flooded_vegetation de Dynamic World en las zonas
donde la inundación puede manifestarse desde el óptico.

ANÁLISIS
1. Temporal: para cada fecha válida se calcula la probabilidad media de flooded_vegetation sobre
   manglar, humedal herbáceo y bosque no inundable, y se compara con Spearman con el nivel del
   río en Remolino.
2. Espacial: se calcula la diferencia entre los periodos de nivel alto y bajo sobre la misma
   malla de 50 m de NISAR y se compara con delta HH sobre el manglar.

LIMITACIÓN
Dynamic World observa la superficie y el dosel desde el óptico. Su clase flooded_vegetation es
sensible sobre todo al agua visible entre vegetación baja o abierta y no es una observación
directa del agua bajo un dosel cerrado. Por ello, el análisis se usa como contraste óptico y no
como validación independiente de la señal de banda L.

SALIDAS
- dw_serie.csv
- dw_resumen.txt
- fig_corroboracion_dw.png
- dw_alto_bajo_50m.tif

USO
    python corroboracion_dw.py [--solo-figura]

Comentarios en el código:

- línea 34: PostGIS deja un proj.db viejo en PROJ_DATA; rasterio necesita el suyo, y hay que fijarlo antes de importarlo
- línea 91: una fila por fecha (varias teselas S2 el mismo dia): media ponderada por cobertura
- línea 124: relee dw_serie.csv y dw_alto_bajo_50m.tif
- línea 125: 1. temporal
- línea 143: 2. espacial
- línea 173: figura: serie temporal y mapa de dDW sobre manglar + dispersion

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
  agropecuario, 23 playas y dunas, 24 infraestructura urbana, 25 otras areas sin vegetación,
  33 rio, lago y oceano, 35 palma aceitera.

USO: python mapbiomas_cruce.py      Salidas: mapbiomas_cruce_resumen.txt, mapbiomas_aoi_serie.csv

Comentarios en el código:

- línea 45: 1. malla de 50 m del mapa NISAR
- línea 70: 2. los 720 puntos
- línea 84: 3. serie anual en el AOI

## Informe y figuras de método

### `md_a_word.py`

Convierte un markdown del curso de radar a .docx: carta, margenes 2,5 cm, Calibri 10,
cuerpo justificado, encabezados en negrita sin numerar, tablas con encabezado sombreado.
El bloque de cabecera (lineas antes del primer '## ') va centrado, la ultima en negrita.

USO
    python md_a_word.py Avance_proyecto_radar.md

Comentarios en el código:

- línea 153: sin párrafo vacío al final: evita una última página en blanco tras la última tabla

### `propuesta_a_word.py`

Convierte Propuesta_trabajo_radar.md en .docx: carta, margenes 2,5 cm, Calibri 11,
justificado, titulos en negrita sin numerar.

### `construir_informe.py`

Ensambla el informe HTML autocontenido incrustando las figuras en base64.

Lee plantilla_informe.html (con marcadores {{IMG:archivo}}) y escribe
informe_radar.html con las imagenes embebidas como data URI.

### `figura_flujo.py`

Genera el diagrama del flujo de trabajo del estudio en nueve etapas.

La versión resumida representa una línea por etapa con el producto que escribe y la versión
detallada documenta todas las operaciones de cada etapa. La figura sigue la organización de los
flujos de procesamiento de De Luca et al. (2021) y Yordanov y Brovelli (2021). Los conteos,
tablas y figuras corresponden a la versión final del informe.

USO
    python figura_flujo.py             -> fig_flujo_trabajo.png
    python figura_flujo.py --detalle   -> fig_flujo_trabajo_detalle.png

Comentarios en el código:

- línea 35: geometria en pulgadas (1 unidad de eje = 1 pulgada)
- línea 37: productos intermedios
- línea 38: etapas (sin barras de software en el resumen)
- línea 39: barras de software
- línea 41: caracteres por linea de vineta
- línea 43: lineas de vineta, para medir desbordes
- línea 44: alto de linea
- línea 45: separacion entre etapas
- línea 105: ------------------------------------------------------------------ cabecera
- línea 112: ------------------------------------------------------------------ etapas
- línea 191: ------------------------------------------------------------------ software

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

Genera la figura de la muestra de referencia de 2025 sobre el área de estudio de la CGSM.

La figura muestra los 720 puntos distribuidos por clase final, la reserva de validación excluida
del muestreo y los bloques de 12 km del diseño de validación espacial.

FUENTES
- etiquetas_2025.csv
- pliegues_cv.csv
- reserva_validacion.geojson
- área de estudio de la CGSM

SALIDA
fig_muestra_2025.png

USO
    python figura_muestra_2025.py

Comentarios en el código:

- línea 57: bloques de 12 km del esquema de validacion cruzada (codigo = floor(x/12km)*10000 + floor(y/12km))

### `figura_consistencia.py`

Figura de la prueba de consistencia de la interprete (muestra 2025): matriz de la clase de
referencia (clase_final, criterio v1) frente a la segunda pasada a ciegas, con acuerdo, Wilson y
kappa en el titulo. Solo agregados; nunca ids. Para los limites de la clave del informe de radar.

Requiere la exportacion consistencia/consistencia_2025_n*.csv de la app. Si no existe, avisa y sale.
USO: python figura_consistencia.py   -> fig_consistencia_2025.png

## Otros

### `comparar_gamma0.py`

Compara los resultados del informe en sigma cero con el recálculo en gamma cero.

PROPÓSITO
    Documentar cuánto cambian las pruebas hidrológicas, las firmas, la separabilidad y la clave al pasar
    de sigma cero a gamma cero (NISAR sin el factor gamma->sigma; Sentinel-1 y ALOS-2 corregidos por el
    coseno del ángulo de incidencia).
DATOS
    Los CSV del informe y sus pares *_gamma0.csv, generados con RADAR_MAGNITUD=gamma0.
MÉTODO
    Une cada tabla por sus claves y escribe las columnas lado a lado.
SALIDAS
    GAMMA0_comparacion.md
USO
    python comparar_gamma0.py
LIMITACIÓN
    Los umbrales absolutos de la clave en gamma cero son los de sigma cero desplazados por la mediana de γ⁰ − σ⁰ en los 720 puntos.

### `figura_diseno.py`

Genera la Figura 1 alternativa del informe: síntesis del diseño analítico en seis filas.

La figura usa exclusivamente productos del análisis, incluidos un recorte HH de NISAR y la malla
de clases a 50 m, y no incluye representaciones simuladas.

USO
    python figura_diseno.py

SALIDA
fig_diseno_estudio.png

Comentarios en el código:

- línea 54: ---------- 1. datos de entrada (y 72-99)
- línea 80: ---------- 2. preprocesamiento (y 57-70)
- línea 94: ---------- 3. muestreo (y 40-53.5)
- línea 112: ---------- 4. forzante (y 31-38)
- línea 118: ---------- 5. pruebas (y 17-29)
- línea 129: ---------- 6. productos (y 3-15)

### `figura_diseno_h.py`

Figura 1 en seis columnas, armada solo con archivos reales de `figuras para flujo`:
recortes de los tres radares, cuatro recortes Sentinel-2 SWIR por cobertura, las dos series del
forzante y los tres mapas de producto. Las cajas de texto se dibujan aquí. Nada generado.

USO: python figura_diseno_h.py  -> fig_diseno_estudio_h.png

Comentarios en el código:

- línea 55: 1. datos de entrada
- línea 68: 2. preprocesamiento
- línea 77: 3. muestreo
- línea 86: 4. forzante
- línea 90: 5. pruebas
- línea 99: 6. productos

### `figura_mapa_c_vs_l.py`

Redibuja la Figura 15 (ΔHH de NISAR frente a ΔVV de Sentinel-1) con contornos de cobertura y leyenda.

PROPÓSITO
    Hacer distinguible el manglar (contorno) del bosque de control (atenuado) en el mapa de las dos bandas.
DATOS
    mapa_doble_rebote_50m.tif (banda 1 ΔHH, banda 4 clase) y mapa_s1_alto_bajo_50m.tif (banda 1 ΔVV),
    ya calculados por mapa_doble_rebote.py y mapa_doble_rebote_s1.py. No recalcula nada.
MÉTODO
    Mismo color y escala que antes (RdBu_r, ±2 dB). Manglar a todo color con contorno verde oscuro;
    bosque de control atenuado sin contorno (demasiado fragmentado); leyenda y rótulos de sectores.
SALIDAS
    fig_mapa_c_vs_l.png (reemplaza la versión anterior sin contornos)
USO
    python figura_mapa_c_vs_l.py
LIMITACIÓN
    Los contornos se trazan sobre la malla de 50 m, así que el borde es escalonado a esa resolución.
