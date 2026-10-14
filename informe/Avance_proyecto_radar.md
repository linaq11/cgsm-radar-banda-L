Universidad Nacional de Colombia
Maestría en Geomática
Radar and LiDAR Remote Sensing, 2026-2
Avance del proyecto
Lina María Quintero Fonseca
Aporte de la banda L para la identificación de inundación bajo dosel de manglar en la Ciénaga Grande de Santa Marta

## Resumen

La inundación bajo el dosel del manglar es una condición del humedal que los radares de banda C registran mal, porque la onda apenas atraviesa un dosel denso. La banda L, con 23 cm de longitud de onda, penetra el dosel y puede registrar el doble rebote entre los troncos y la lámina de agua. Con el fin de establecer qué aporta la banda L, se compararon NISAR y ALOS-2 con Sentinel-1 en Bahía de Málaga, donde el agua sigue a la marea, y en la Ciénaga Grande de Santa Marta, donde sigue al nivel del río Magdalena. La regla de lectura se fijó antes de mirar los datos: si la banda L ve el agua bajo el dosel, la retrodispersión copolar del manglar debe subir con el forzante hidrológico y la del bosque de control no. En Bahía de Málaga ocurre así en las dos trazas de NISAR y en ALOS-2, con un aumento de 0,57 dB del manglar frente al bosque en HH, mientras que Sentinel-1 y la polarización cruzada no responden. Ese resultado resiste la corrección por dependencia temporal. En la Ciénaga Grande la resta sube 0,83 dB entre río bajo y alto, pero las pasadas de cada nivel pertenecen a versiones distintas del producto y dentro de cada versión no hay relación con el nivel, de modo que el efecto no es identificable con las pasadas actuales. Posteriormente, la clave de interpretación se contrastó con una muestra de referencia de 720 puntos: la banda L distingue mejor que la C el manglar intacto del degradado (separabilidad 0,91 frente a 0,30, todavía por debajo del umbral de 1) y ninguna banda separa el manglar degradado del humedal herbáceo. Finalmente, un mapa a 50 m concentra la señal en el manglar del sur, en la desembocadura del río Fundación, y no en la entrada de los caños del Magdalena. Quedan pendientes el nivel del agua medido dentro del humedal y pasadas de NISAR de una sola versión.

Palabras clave: radar de apertura sintética, banda L, NISAR, manglar, inundación bajo dosel, doble rebote, Ciénaga Grande de Santa Marta, Bahía de Málaga.

## 1. Introducción

El producto de monitoreo global de inundaciones del Servicio de Gestión de Emergencias de Copernicus procesa toda la Sentinel-1 en banda C, pero retira de la detección las superficies donde la interacción de las microondas con el terreno es compleja. Entre ellas está la vegetación densa, combinada con las áreas urbanas en una máscara de "sin sensibilidad" (Expert Flood Monitoring Alliance, 2022, sección 4.4). En consecuencia, la inundación bajo el dosel del manglar cae por diseño fuera de lo que la banda C reporta a escala global. La banda L, con 23 cm de longitud de onda, penetra más en el dosel y puede registrar la interacción entre los troncos y la lámina de agua.

El doble rebote como mecanismo de retrodispersión en bosque inundado se conoce desde las primeras observaciones orbitales en banda L, Seasat y SIR-B. Richards et al. (1987) atribuyeron el aumento de la retrodispersión copolar al doble rebote entre los troncos y la lámina de agua. Posteriormente, Hess et al. (1990) reunieron la evidencia de que ese realce aparece en banda L y se atenúa en longitudes de onda más cortas, donde el dosel lo oculta.

Sobre manglar, Lucas et al. (2014) mostraron con ALOS PALSAR que la banda L aporta a la cartografía sistemática de su extensión y de sus cambios. De esa línea sale el producto Global Mangrove Watch que aquí sirve de referencia (Bunting et al., 2022). Sin embargo, esos trabajos no abordaron el seguimiento de la inundación bajo el dosel con un muestreo regular de pocos días. NISAR, con doce días de repetición y un plan de adquisición sistemático (NASA ASF DAAC, 2026a, 2026b), ofrece ese muestreo sobre los dos sitios.

La elección de NISAR como sensor principal de banda L responde a esa frecuencia de adquisición y a la continuidad temporal disponible sobre la CGSM. ALOS-2 aporta una referencia independiente en la misma banda y permite corroborar la respuesta observada en Bahía de Málaga, pero su cobertura sobre la ciénaga durante el periodo analizado se limita a diez pasadas, siete de ellas completas, insuficientes para evaluar la respuesta por trayectoria. NISAR, en cambio, proporciona una serie cada doce días que permite relacionar la retrodispersión con los cambios del forzante hidrológico dentro de una misma geometría de adquisición. Por lo tanto, ALOS-2 se usa como corroboración independiente y no como sustituto de la serie temporal principal.

En la Ciénaga Grande de Santa Marta la hidrología es el problema central. La obstrucción de los caños que la conectan con el río Magdalena produjo la hipersalinización y la mortalidad masiva de manglar de los años ochenta y noventa, y la rehabilitación consistió en reabrir esa conexión (Botero y Salzwedel, 1999). Simard et al. (2008) cartografiaron en tres dimensiones el manglar de la ciénaga con SRTM, ICESat y datos de campo. Jaramillo et al. (2018) evaluaron la conectividad hidrológica del humedal, que no tiene aforos, con observaciones interferométricas de radar. Ninguno de esos trabajos midió la respuesta temporal de la retrodispersión en banda L a la inundación bajo el dosel. En este sentido, el nivel del río en Remolino y, cuando INVEMAR las entregue, las series de nivel dentro del humedal son los forzantes contra los que se contrasta la señal.

Con el fin de cubrir ese vacío, este avance compara NISAR y ALOS-2 en banda L con Sentinel-1 en banda C, con Bahía de Málaga como sitio mareal de contraste y la CGSM como sistema ligado al nivel del río Magdalena. La pregunta es qué información adicional aporta la banda L frente a Sentinel-1 para identificar condiciones de inundación bajo dosel de manglar en la CGSM. Para responderla se caracteriza la respuesta de retrodispersión de las coberturas representativas de la ciénaga en las dos bandas, se compara esa respuesta en zonas de manglar con distintas condiciones de inundación y, finalmente, se interpretan las diferencias a partir de los mecanismos de dispersión de superficie, de volumen y de doble rebote.

## 2. Datos y métodos

### 2.1 Diseño y sitios de estudio

El estudio se diseñó con la Ciénaga Grande de Santa Marta (CGSM) como sitio principal y Bahía de Málaga (Buenaventura), en el Pacífico colombiano, como sitio de contraste. En la ciénaga la inundación del manglar sigue al nivel del río Magdalena, mientras que en Bahía de Málaga responde a la marea. Esa diferencia permite establecer si la respuesta de la banda L se mantiene bajo dos forzantes hidrológicos distintos.

Se analizaron cuatro coberturas: agua abierta, humedal herbáceo, manglar y un bosque de control que no se inunda. La extensión de manglar se tomó del consenso entre WorldCover 2021 y Global Mangrove Watch. Se usaron Sentinel-1 en banda C y NISAR y ALOS-2 en banda L sobre periodos comparables, con 45 escenas de NISAR en total, 21 sobre la ciénaga y 24 sobre Bahía de Málaga (Tabla 1). NISAR es la serie principal de banda L para el análisis temporal, ALOS-2 la corroboración independiente en la misma banda y Sentinel-1 la referencia en banda C.

La comparación se hizo por polarización, cobertura y condición hidrológica, dentro de cada traza y con el ángulo de incidencia declarado. En Bahía de Málaga la retrodispersión se contrastó con la altura de marea en la pasada. En la ciénaga se usaron la lluvia acumulada de treinta días y el nivel del río Magdalena. La interpretación se centró en el canal copolar, el cruzado y su diferencia, según la respuesta esperada de los mecanismos de dispersión de superficie, de volumen y de doble rebote. Posteriormente, la interpretación por cobertura se contrastó con una muestra de referencia propia de 2025, la distribución espacial de la señal se llevó a mapas de cambio a 50 m y Dynamic World sirvió de contraste óptico.

### 2.2 Datos SAR

Tabla 1. Escenas SAR sobre los dos sitios, verificadas en el archivo de la NASA y en Earth Engine el 11 de septiembre de 2026 y actualizadas el 7 de octubre.

| Sitio | NISAR GCOV (HH, HV, 10 m) | ALOS-2 ScanSAR (HH, HV, 25 m) | Sentinel-1 GRD (VV, VH, 10 m), oct-2025 a sep-2026 |
|---|---|---|---|
| CGSM | 21 escenas, 14 descendentes (traza 083) y 7 ascendentes (traza 007), oct-2025 a sep-2026, sin cobertura entre feb y may de 2026; las 21 en disco (inventario actualizado el 7 de octubre con las cuatro de septiembre) | serie 2025–2026 en Earth Engine, 10 pasadas, 7 completas | 119 pasadas con cobertura completa (58 en la órbita 77 y 61 en la 142) |
| Bahía de Málaga | 24 escenas que cubren completo el manglar: 12 ascendentes (traza 004, 05:46 local) y 12 descendentes (traza 087, 18:29 local), oct-2025 a sep-2026; las 24 en disco | 72 escenas con HH y HV, ene-2025 a sep-2026, mosaicadas en 57 pasadas, 39 con cobertura completa | 89 pasadas con cobertura completa (26 en la órbita 48 y 63 en la 142) |

En todos los casos solo entran las pasadas que cubren la caja completa del sitio. En Bahía de Málaga las dos trazas de NISAR difieren en hora y en geometría, de modo que muestrean estados de marea distintos. Por esta razón, las comparaciones temporales se hacen dentro de cada traza y no entre ellas, y la misma separación por trayectoria u órbita se mantiene en los demás sensores.

Sobre la ciénaga, las 21 escenas de NISAR se reparten en 14 de la traza descendente 083 (18:27 hora local), con cuatro pasadas de época seca entre diciembre de 2025 y enero de 2026 y diez de época húmeda entre octubre y noviembre de 2025 y entre junio y septiembre de 2026, y siete de la traza ascendente 007 (05:31), todas de la época húmeda de 2026. Las seis de octubre de 2025 a enero de 2026 pertenecen a la colección Beta del producto y las quince de junio a septiembre de 2026 a la colección Provisional.

### 2.3 Procesamiento SAR y flujo de análisis

El procesamiento se hizo en Python y Google Earth Engine (Gorelick et al., 2017). Las escenas NISAR GCOV (NASA ASF DAAC, 2026a, 2026b), que no están en Earth Engine, se localizaron en el catálogo CMR y se recortaron de forma remota con earthaccess y h5py. Sentinel-1 (Torres et al., 2012), ALOS-2 PALSAR-2 ScanSAR (JAXA EORC, s. f.), las coberturas globales, Sentinel-2 y ERA5-Land (Muñoz-Sabater et al., 2021) se procesaron desde la interfaz de Python de Earth Engine. La marea, el nivel del río, la estadística y las figuras se trabajaron en Python.

El preprocesamiento se definió por sensor. NISAR pasa de gamma cero con corrección de terreno a sigma cero con el factor que trae el producto y conserva su malla de ángulo de incidencia. ALOS-2 se calibra con la constante de JAXA (σ⁰ = 10·log10(DN²) − 83 dB) y se mosaica por pasada y trayectoria. Sentinel-1 GRD se usa con la eliminación de ruido térmico, la calibración radiométrica y la corrección de terreno con SRTM de 30 m que Earth Engine aplica al ingerirla, sin aplanamiento de terreno ni filtro de speckle (Google, s. f.).

La extracción se hace después del paso a decibelios, con un promedio espacial de 3 × 3 píxeles en NISAR y el píxel nativo en ALOS-2 y Sentinel-1. Cada pasada conserva traza, dirección, hora local e incidencia. Las trazas se analizan por separado, puesto que la geometría sola desplaza el nivel hasta 1,4 dB en HH en NISAR (Tabla 3).

La Figura 1 resume el diseño analítico en seis etapas, de los datos de entrada a los productos. El flujo de trabajo completo tiene nueve etapas: acceso a datos, preprocesamiento, coberturas de referencia y muestreo, forzante hidrológico, estadística por pasada, prueba hidrológica, robustez, clave de interpretación y mapa de la señal con contraste óptico (Figura A2). Las etapas posteriores al procesamiento se describen en las secciones 2.4 a 2.8. La cadena por sensor, con la convención de los flujos de trabajo SAR de De Luca et al. (2021) y Yordanov y Brovelli (2021), y los guiones de cada etapa están en el Anexo A.

![Figura 1. Flujo metodológico del estudio, desde los datos de entrada y el preprocesamiento SAR hasta las pruebas hidrológicas y los productos cartográficos.](fig_flujo_metodologico.png)

### 2.4 Coberturas de referencia y muestreo

Ante la ausencia de puntos interpretados y de estaciones de campo en Bahía de Málaga, las coberturas de referencia se definieron a partir de dos productos globales independientes. Para agua, bosque y humedal herbáceo se utilizó WorldCover 2021 a 10 m (Zanaga et al., 2022), mientras que el manglar se definió mediante el consenso entre WorldCover 2021 y Global Mangrove Watch v3, cuya extensión corresponde a 2020 (Bunting et al., 2022).

En Bahía de Málaga, Global Mangrove Watch cartografía 6.006 ha de manglar y WorldCover 7.576 ha. Los dos productos coinciden en 5.326 ha, el 89 % del primero y el 70 % del segundo. Las áreas que solo identifica Global Mangrove Watch presentan una retrodispersión entre 0,9 y 2 dB menor en las dos polarizaciones, con diferencias medianas de 1,2 dB en HH y 1,5 dB en HV, y firmas próximas a las del humedal herbáceo. Este comportamiento es compatible con bordes, manglar de menor estructura o cambios ocurridos entre las fechas de referencia de los dos productos. Por esta razón, el manglar usado como clase de referencia en el Pacífico se restringió a las áreas coincidentes entre los dos mapas.

En la CGSM, el consenso entre WorldCover 2021 y Global Mangrove Watch 2020 comprende 33.173 ha de manglar. Otras 8.157 ha aparecen únicamente en WorldCover y 8.395 ha únicamente en Global Mangrove Watch, estas últimas concentradas en el delta del suroccidente y en el borde noroccidental. El bosque utilizado como referencia no inundable corresponde a bosque seco de las franjas oriental y meridional, fuera del plano inundable (Figura 2).

![Figura 2. Coberturas de referencia en la CGSM: (a) clases de WorldCover 2021; (b) coincidencia del manglar cartografiado por WorldCover 2021 y Global Mangrove Watch 2020.](fig_cgsm_referencia.png)

En los dos sitios se seleccionaron 400 puntos por clase mediante muestreo estratificado en Earth Engine, con semilla 42. Los puntos se generaron una sola vez y se emplearon en los tres sensores. En la CGSM, el manglar de consenso, el humedal herbáceo y el agua se muestrearon dentro del área de estudio de 2.042 km². El bosque no inundable se muestreó sobre la caja ampliada del cubo de 4.304 km², puesto que el bosque seco de los piedemontes que sirve de control queda fuera del área de estudio en todas las pasadas de Sentinel-1 con cobertura completa del periodo y en las de ALOS-2, que son solo diez sobre la ciénaga, siete completas, insuficientes para evaluar por trayectoria.

### 2.5 Forzantes hidrológicos

En Bahía de Málaga, la altura de marea de cada adquisición se obtuvo del pronóstico oficial de la DIMAR para 2026 (Dirección General Marítima, s. f.), interpolado entre pleamares y bajamares y expresado respecto al nivel medio anual. Para las diez pasadas de octubre a diciembre de 2025 se utilizó una predicción armónica ajustada al mareógrafo histórico de Buenaventura (UHSLC, estación 085; Caldwell et al., 2015). En las catorce pasadas de 2026 las dos fuentes presentaron una correlación de Spearman de 0,95, un sesgo medio de 0,03 m y un error cuadrático medio de 0,24 m, de modo que conservan el mismo orden de las pasadas por altura de marea. Las 24 adquisiciones abarcaron condiciones entre −1,2 y +2,2 m respecto al nivel medio.

En la CGSM, la condición hidrológica se caracterizó inicialmente con la precipitación acumulada en los 30 días anteriores a cada adquisición, obtenida de ERA5-Land y promediada sobre el área de estudio (Muñoz-Sabater et al., 2021), y con la partición entre época seca, de diciembre a abril, y húmeda, de mayo a noviembre. Esa prueba usa las doce pasadas descendentes anteriores al 11 de septiembre de 2026, fecha hasta la que llega ERA5-Land. Posteriormente, se incorporó el nivel horario del río Magdalena en la estación automática Remolino del IDEAM (código 2904700095; IDEAM, s. f.), interpolado a la hora de cada pasada, con el que entran las catorce pasadas descendentes y las siete ascendentes.

La respuesta SAR se evaluó con la diferencia manglar menos bosque, el contraste entre los estados alto y bajo del forzante y la correlación de Spearman. El nivel del río varió entre 0,79 y 2,67 m para Sentinel-1, entre 0,91 y 2,67 m para NISAR D083 y entre 0,82 y 1,58 m para NISAR A007. El nivel y la precipitación acumulada de 30 días están asociados (ρ 0,70, p 0,01), de modo que las dos pruebas se interpretan como indicadores relacionados y no como evidencias independientes.

### 2.6 Regla de lectura y robustez

La regla de lectura se definió antes del análisis. Si la banda L responde al agua bajo el dosel, dentro de una misma trayectoria se espera un aumento de la retrodispersión copolar del manglar y de HH − HV con el forzante hidrológico, sin una respuesta equivalente en el canal cruzado ni en el bosque no inundable de referencia.

Cada pasada se redujo a la mediana de retrodispersión por clase y a la diferencia manglar menos bosque, que controla las variaciones temporales compartidas por las dos coberturas. En Bahía de Málaga se compararon las mitades superior e inferior de la distribución de marea, y en la CGSM los tercios superior e inferior del nivel del río. Para cada variable se calcularon la diferencia entre los estados alto y bajo y la correlación de Spearman con el forzante.

La robustez se evaluó frente al ángulo de incidencia, en tercios del rango angular, frente a la dependencia temporal y frente a la versión del producto de NISAR. Para corregir la autocorrelación entre pasadas se estimó el tamaño efectivo de muestra según Pyper y Peterman (1998), con los rezagos hasta n/5, y se recalcularon los valores p. En la CGSM se examinó además la coincidencia entre los estados hidrológicos y las colecciones Beta y Provisional de NISAR.

### 2.7 Clave de interpretación y evaluación con la muestra de referencia

La clave de interpretación integra las firmas multifecha del canal copolar, del canal cruzado y de su diferencia en las dos bandas. Estas firmas se calcularon primero sobre las coberturas de referencia y después sobre una muestra propia de 720 puntos de 2025, distribuida en seis clases: agua abierta, manglar intacto, vegetación flotante, manglar degradado, humedal herbáceo y otro.

La separabilidad entre pares de clases se cuantificó con la distancia de Jeffries-Matusita, calculada a partir de la distancia de Bhattacharyya bajo supuesto gaussiano. Los umbrales de la clave se definieron con esta misma muestra y se evaluaron sobre ella, de modo que el acierto corresponde a resustitución y no a una validación independiente.

Los puntos se sortearon fuera de la reserva de validación de la tesis, con una separación mínima de 200 m, y se etiquetaron a ciegas sobre imágenes de alta resolución de 2025, con revisión de los primeros 400 bajo un criterio escrito y marca de borde cuando la ventana de 3 × 3 píxeles mezcla clases. La Figura 3 muestra su distribución por clase, la reserva de validación excluida del muestreo y los bloques de 12 km del diseño de validación espacial de la tesis.

![Figura 3. Muestra de referencia de 2025 en la CGSM: 720 puntos por clase, reserva de validación y bloques de 12 km del diseño de validación espacial.](fig_muestra_2025.png)

### 2.8 Cartografía de la señal y contraste óptico

La distribución espacial de la señal se evaluó con diferencias píxel a píxel a 50 m sobre la malla UTM 18N (EPSG:32618) de los recortes de NISAR.

En la CGSM, NISAR D083 compara las seis pasadas de nivel alto, de octubre de 2025 a enero de 2026, con las ocho de nivel bajo, de junio a septiembre de 2026. Los dos grupos coinciden con las colecciones Beta y Provisional, de modo que el contraste espacial está confundido con la versión del producto. Sentinel-1 usa las mismas ventanas de fechas, con 13 y 18 pasadas de la órbita 142.

En Bahía de Málaga, cada trayectoria compara las seis pasadas de marea más alta con las seis de marea más baja. Como contraste óptico se empleó la probabilidad de `flooded_vegetation` de Dynamic World V1 (Brown et al., 2022) en las fechas con al menos la mitad del manglar libre de nubes. Para los mapas se calculó la mediana por píxel en las mismas ventanas de fechas de NISAR, con al menos dos observaciones válidas por grupo. Dynamic World se interpreta como indicador de vegetación inundada visible desde el óptico, no como observación directa del agua bajo el dosel.

## 3. Resultados

### 3.1 Perfil de retrodispersión en Bahía de Málaga

Las cinco primeras adquisiciones de la traza A004 mostraron una señal estable dentro de cada cobertura. La variación de HH fue inferior a 1 dB en el manglar de consenso, el bosque y el humedal herbáceo, mientras que el agua abierta presentó un intervalo mayor, de hasta 1,7 dB (Tabla 2). En esas fechas el manglar de consenso presentó valores de HH entre −6,9 y −7,8 dB y de HV entre −14,0 y −14,3 dB.

El manglar identificado únicamente por Global Mangrove Watch fue sistemáticamente más oscuro que el manglar de consenso, con una diferencia mediana cercana a 1,2 dB en HH y 1,5 dB en HV. Su respuesta se aproximó a la del humedal herbáceo, lo que respalda la decisión de restringir la clase de manglar a las áreas coincidentes entre WorldCover y Global Mangrove Watch.

Tabla 2. Mediana de σ⁰ (dB) por cobertura en las cinco primeras escenas NISAR de la traza ascendente A004 (8 y 20 de noviembre y 2, 14 y 26 de diciembre de 2025), 400 puntos por clase, ángulo de incidencia mediano de 42°.

| Cobertura | HH | HV | HH−HV |
|---|---|---|---|
| Manglar (consenso WorldCover y GMW) | −6,9 / −7,2 / −7,6 / −7,8 / −7,5 | −14,3 / −14,1 / −14,0 / −14,2 / −14,1 | 7,3 / 6,7 / 6,5 / 6,4 / 6,8 |
| Manglar solo en GMW | −8,9 / −8,5 / −8,8 / −8,7 / −8,9 | −15,8 / −15,3 / −15,3 / −15,9 / −15,6 | 6,4 / 6,4 / 6,4 / 6,5 / 6,5 |
| Bosque | −7,3 / −7,6 / −7,4 / −7,8 / −7,2 | −13,4 / −13,4 / −13,4 / −13,6 / −13,5 | 6,3 / 6,0 / 6,0 / 6,0 / 6,0 |
| Humedal herbáceo | −9,7 / −9,6 / −9,4 / −9,5 / −9,9 | −17,2 / −16,8 / −16,8 / −17,4 / −16,8 | 6,8 / 6,6 / 7,0 / 6,9 / 6,9 |
| Agua | −20,5 / −18,8 / −19,3 / −19,5 / −19,2 | −25,9 / −25,8 / −26,0 / −25,8 / −25,7 | 5,2 / 6,9 / 6,8 / 6,0 / 6,7 |

Al considerar las 24 adquisiciones, el manglar mantuvo una variabilidad temporal baja dentro de cada trayectoria, con desviaciones estándar de 0,3 dB en HH para A004 y 0,4 dB para D087 (Tabla 3). Sin embargo, los niveles absolutos difirieron entre trayectorias. A004 tiene un ángulo de incidencia mediano de 42° y D087 de 35°, por lo que las comparaciones hidrológicas se realizaron siempre dentro de cada trayectoria.

En D087, el manglar presentó una mediana de HH 0,6 dB superior a la del bosque y una diferencia HH − HV 1,1 dB mayor. En A004, las medianas de HH de manglar y bosque fueron prácticamente iguales, mientras que HH − HV fue 0,7 dB mayor en el manglar. Estas diferencias establecen la línea de base para evaluar después su variación con la altura de marea.

Tabla 3. Mediana de σ⁰ por cobertura y trayectoria en las 24 escenas NISAR y desviación estándar entre las 12 adquisiciones de cada trayectoria.

| Cobertura | Traza (hora local, incidencia) | HH (sd) | HV (sd) | HH−HV (sd) |
|---|---|---|---|---|
| Manglar (consenso) | A004 (05:46, 42°) | −7,4 (0,3) | −14,2 (0,7) | 6,6 (0,7) |
| Manglar (consenso) | D087 (18:29, 35°) | −8,2 (0,4) | −13,9 (0,7) | 5,6 (0,5) |
| Bosque | A004 | −7,4 (0,2) | −13,4 (0,5) | 5,9 (0,4) |
| Bosque | D087 | −8,8 (0,4) | −13,2 (0,7) | 4,5 (0,5) |
| Humedal herbáceo | A004 | −9,4 (0,3) | −16,8 (0,9) | 6,7 (0,5) |
| Humedal herbáceo | D087 | −8,7 (0,5) | −14,3 (1,0) | 5,7 (0,5) |
| Agua | A004 | −19,1 (0,7) | −25,7 (0,9) | 5,9 (0,6) |
| Agua | D087 | −18,5 (1,0) | −25,5 (1,1) | 7,0 (1,2) |

Entre las adquisiciones de noviembre a enero y las de junio a septiembre, HV aumentó entre 1 y 1,8 dB en todas las coberturas, incluida el agua abierta. Como este cambio coincide con la transición entre las colecciones Beta y Provisional de NISAR, la variación temporal de HV no puede atribuirse únicamente a cambios estacionales y se considera de forma explícita en el análisis de robustez.

La Figura 4 muestra los compuestos de las dos trayectorias y la diferencia espacial de HH. Las diferencias entre A004 y D087 afectan tanto al manglar como a las demás coberturas, lo que confirma la necesidad de analizar cada geometría de adquisición por separado.

![Figura 4. Compuestos NISAR GCOV de Bahía de Málaga para las trayectorias A004 y D087 (R = HH, G = HV, B = HH − HV) y diferencia de HH entre las dos geometrías de adquisición.](fig_malaga_radar.png)

### 3.2 Marea y retrodispersión del manglar en banda L: NISAR

La relación entre la marea y la retrodispersión fue consistente en las dos trayectorias de NISAR (Tabla 4). En HH, la señal del manglar relativa al bosque aumentó con la altura de marea tanto en A004 (ρ 0,83, p 0,001) como en D087 (ρ 0,74, p 0,006). La diferencia entre los grupos de marea alta y baja fue de +0,57 dB en las dos trayectorias. HH − HV mostró el mismo sentido de respuesta, mientras que HV no presentó asociación con la marea.

Tabla 4. Relación entre la altura de marea en la pasada y la retrodispersión de NISAR, por trayectoria (12 pasadas cada una): diferencia de medianas entre las pasadas por encima y por debajo de la mediana de marea, correlación de Spearman y su valor p.

| Traza | Variable | Manglar: alta − baja (dB), ρ, p | Bosque: alta − baja (dB), ρ, p | Manglar − bosque: alta − baja (dB), ρ, p |
|---|---|---|---|---|
| A004 | HH | +0,28, 0,76, 0,004 | −0,11, −0,09, 0,78 | +0,57, 0,83, 0,001 |
| A004 | HV | −0,36, −0,11, 0,73 | −0,31, −0,13, 0,70 | +0,03, 0,11, 0,73 |
| A004 | HH−HV | +0,76, 0,53, 0,08 | +0,31, 0,20, 0,53 | +0,45, 0,83, 0,001 |
| D087 | HH | −0,02, 0,25, 0,44 | −0,49, −0,36, 0,25 | +0,57, 0,74, 0,006 |
| D087 | HV | −1,26, −0,41, 0,18 | −1,30, −0,50, 0,10 | +0,07, −0,06, 0,85 |
| D087 | HH−HV | +0,88, 0,76, 0,005 | +0,44, 0,13, 0,68 | +0,61, 0,60, 0,04 |

El bosque no mostró asociación con la marea en ninguna de las variables. La respuesta se concentró, por lo tanto, en el canal copolar y en HH − HV, y no en HV. Este patrón es compatible con un aumento de la contribución de doble rebote en el manglar inundado (Richards et al., 1987; Hess et al., 1990).

El efecto fue pequeño, cercano a 0,6 dB en HH, y del mismo orden que la variabilidad entre adquisiciones dentro de una trayectoria. Sin embargo, su repetición independiente en A004 y D087 permite distinguirlo de una diferencia de geometría de observación (Figura 5).

![Figura 5. Retrodispersión del manglar y del bosque frente a la altura de marea asignada a cada adquisición de NISAR, por trayectoria.](fig_marea_vs_radar.png)

La estratificación por ángulo de incidencia confirmó el sentido de la respuesta, aunque el rango angular disponible fue reducido, de 42° a 43° en A004 y de 34° a 37° en D087. La diferencia manglar menos bosque aumentó entre marea baja y alta en HH en los seis terciles de incidencia (+0,27 a +0,77 dB, ρ de 0,48 a 0,97), con p menor que 0,05 en cinco de ellos, y también fue positiva en HH − HV. HV no mostró asociación en ningún tercil (Figura 6).

Debido al escaso rango de incidencia dentro de cada trayectoria, este análisis permite comprobar que la respuesta no cambia de signo con la geometría local, pero no establecer una relación entre la magnitud del efecto y el ángulo de incidencia.

![Figura 6. Respuesta del manglar relativa al bosque por tercil de ángulo de incidencia en las trayectorias A004 y D087 de NISAR.](fig_doble_rebote_incidencia.png)

### 3.3 Comparación con Sentinel-1 en banda C

La misma prueba se aplicó a las 89 adquisiciones de Sentinel-1 con cobertura completa de Bahía de Málaga entre octubre de 2025 y septiembre de 2026, 26 de la órbita ascendente 48 y 63 de la órbita descendente 142, con los mismos puntos de muestreo y la altura de marea de cada adquisición. A diferencia de NISAR, la señal del manglar relativa al bosque no mostró relación con la marea en VV, VH ni VV − VH en ninguna de las dos órbitas (Tabla 5, Figura 7).

Tabla 5. Sentinel-1: relación entre la altura de marea en la pasada y la retrodispersión del manglar relativa al bosque, por órbita (diferencia de medianas alta − baja, ρ de Spearman y valor p).

| Órbita (hora local, n) | VV | VH | VV−VH |
|---|---|---|---|
| 48 ascendente (18:21, 26) | −0,07 dB, ρ −0,18, p 0,37 | −0,11 dB, ρ −0,30, p 0,14 | +0,16 dB, ρ 0,23, p 0,26 |
| 142 descendente (05:50, 63) | −0,07 dB, ρ −0,13, p 0,32 | 0,00 dB, ρ −0,08, p 0,55 | −0,15 dB, ρ −0,15, p 0,24 |

Aunque el manglar analizado de forma aislada presentó en VV de la órbita 142 una correlación negativa con la marea (ρ −0,39, p 0,002), esa asociación desapareció al descontar el bosque y además tuvo signo contrario al observado en HH de banda L.

Así, sobre el mismo sitio y con la misma referencia hidrológica, NISAR mostró una respuesta positiva del manglar relativo al bosque en el canal copolar, mientras que Sentinel-1 no presentó una respuesta equivalente. Esta comparación no separa del todo el efecto de la longitud de onda del de la polarización, puesto que Sentinel-1 observa VV y NISAR HH.

![Figura 7. Retrodispersión de Sentinel-1 del manglar y del bosque frente a la altura de marea, por órbita relativa.](fig_s1_marea.png)

### 3.4 Corroboración con ALOS-2 en banda L

Para comprobar si la respuesta observada con NISAR se reproducía con otro sensor de banda L, se analizaron 72 escenas de ALOS-2 PALSAR-2 ScanSAR adquiridas entre enero de 2025 y septiembre de 2026, agrupadas en 57 pasadas. Treinta y nueve cubrieron por completo el área de estudio, y el análisis se concentró en las trayectorias descendentes 139 (21 pasadas) y 140 (15 pasadas), ambas adquiridas alrededor del mediodía.

ALOS-2 reprodujo el patrón observado con NISAR (Tabla 6, Figura 8). La señal HH del manglar relativa al bosque aumentó con la marea en las dos trayectorias, con ρ 0,65 (p 0,002) en el path 139 y ρ 0,72 (p 0,002) en el path 140. HH − HV presentó igualmente asociaciones positivas, mientras que HV no mostró el mismo comportamiento.

Tabla 6. ALOS-2: relación entre la altura de marea en la pasada y la retrodispersión del manglar relativa al bosque, por trayectoria (diferencia de medianas alta − baja, ρ de Spearman y valor p).

| Path (hora local, n) | HH | HV | HH−HV |
|---|---|---|---|
| 139 descendente (11:53, 21) | +0,25 dB, ρ 0,65, p 0,002 | +0,06 dB, ρ 0,05, p 0,81 | +0,13 dB, ρ 0,47, p 0,03 |
| 140 descendente (12:00, 15) | +0,49 dB, ρ 0,72, p 0,002 | −0,16 dB, ρ −0,45, p 0,10 | +0,91 dB, ρ 0,79, p < 0,001 |

En el path 139, HV disminuyó con la marea tanto en el manglar como en el bosque (ρ −0,66 y −0,62), lo que indica una variación compartida por las dos coberturas, ligada a la estación en pasadas de mediodía. Esa señal se redujo al usar la diferencia manglar menos bosque.

La comparación entre sensores muestra un patrón consistente en el canal copolar de banda L: NISAR presentó ρ 0,83 y 0,74 y ALOS-2 ρ 0,65 y 0,72, mientras que Sentinel-1 presentó ρ −0,18 y −0,13 en VV. En los dos sensores de banda L, la asociación positiva se concentró en HH y HH − HV y estuvo ausente en HV.

![Figura 8. Retrodispersión de ALOS-2 PALSAR-2 del manglar y del bosque frente a la altura de marea, por trayectoria.](fig_alos2_marea.png)

### 3.5 La Ciénaga Grande: lluvia como forzante

La comparación inicial dentro de la colección Beta de NISAR mostró una respuesta espacial heterogénea. Entre el 4 de diciembre de 2025, con el río Magdalena a 2,67 m en Remolino, y el 9 de enero de 2026, con 1,69 m, el HH aumentó una mediana de +0,43 dB sobre el manglar de consenso, aunque el 50 % central de las diferencias abarcó de −0,42 a +1,28 dB (Figura 9). La señal negativa sobre la laguna corresponde a cambios en la rugosidad del agua abierta por el viento y no a inundación. Las pasadas de río más bajo, de la colección Provisional, no se restaron, con el fin de no mezclar el cambio de calibración con el cambio de nivel.

![Figura 9. NISAR GCOV sobre la CGSM, traza D083: (a) 4 de diciembre de 2025, nivel del Magdalena de 2,67 m; (b) 9 de enero de 2026, 1,69 m; (c) diferencia de HH entre las dos fechas.](fig_cgsm_radar.png)

Los compuestos de Sentinel-2 (Drusch et al., 2012) de esas fechas, mediana de las diez adquisiciones a menos de diez días de cada pasada enmascaradas con Cloud Score+ (Pasquarella et al., 2023), no mostraron un cambio equivalente en superficie (Figura 10). El NDVI mediano del manglar fue de 0,855 y 0,867, y el agua abierta ocupó el 39,7 % y el 39,2 % del área válida. El óptico distingue las coberturas principales, pero no registra el agua situada bajo un dosel cerrado.

![Figura 10. Comparación de Sentinel-2 y NISAR sobre la CGSM para las dos fechas de la Figura 9. Sentinel-2 se presenta en color natural e infrarrojo color y NISAR como compuesto de HH, HV y HH − HV.](fig_cgsm_optico_radar.png)

La precipitación acumulada de 30 días produjo respuestas distintas en las dos bandas. En Sentinel-1, el bosque seco respondió a la lluvia con mayor intensidad que el manglar, sobre todo en VV (ρ 0,52 y 0,58 frente a 0,32 y 0,21), de modo que la diferencia manglar menos bosque resultó negativa (Tabla 7). En banda C, por lo tanto, el bosque no constituye un control estable frente a la humedad estacional.

Tabla 7. Sentinel-1 en la CGSM: correlación de Spearman entre la lluvia de treinta días y la retrodispersión, por órbita.

| Órbita (hora local, n) | Clase | VV | VH | VV−VH |
|---|---|---|---|---|
| 77 ascendente (18:06, 58) | Manglar | ρ 0,32, p 0,01 | ρ 0,14, p 0,31 | ρ 0,25, p 0,06 |
| 77 ascendente (18:06, 58) | Bosque | ρ 0,52, p < 0,001 | ρ 0,21, p 0,12 | ρ 0,38, p 0,003 |
| 77 ascendente (18:06, 58) | Manglar − bosque | ρ −0,35, p 0,01 | ρ −0,13, p 0,35 | ρ −0,17, p 0,19 |
| 142 descendente (05:48, 61) | Manglar | ρ 0,21, p 0,11 | ρ 0,18, p 0,17 | ρ −0,04, p 0,74 |
| 142 descendente (05:48, 61) | Bosque | ρ 0,58, p < 0,001 | ρ 0,41, p 0,001 | ρ 0,50, p < 0,001 |
| 142 descendente (05:48, 61) | Manglar − bosque | ρ −0,52, p < 0,001 | ρ −0,34, p 0,01 | ρ −0,44, p < 0,001 |

En NISAR D083, en cambio, el HH del bosque no presentó relación con la lluvia (ρ 0,02), mientras que el manglar mostró ρ 0,50 y la diferencia manglar menos bosque alcanzó ρ 0,58 (p 0,05). La polarización cruzada no mostró una asociación equivalente (Tabla 8, Figura 11). La partición por calendario entre época húmeda y seca produjo el signo contrario (−0,44 dB) porque, en el periodo estudiado, las pasadas de época seca de diciembre y enero tuvieron entre 90 y 193 mm de lluvia antecedente y las de época húmeda de junio a septiembre de 2026 entre 51 y 151 mm.

Tabla 8. NISAR en la CGSM, traza descendente 083 (18:27 hora local, 12 pasadas, 8 de época húmeda): correlación de Spearman con la lluvia de treinta días y diferencia húmeda menos seca según el calendario.

| Clase | HH | HV | HH−HV | HH, húmeda − seca (dB) |
|---|---|---|---|---|
| Manglar | ρ 0,50, p 0,10 | ρ −0,26, p 0,42 | ρ 0,54, p 0,07 | −0,15 |
| Bosque | ρ 0,02, p 0,95 | ρ −0,34, p 0,29 | ρ 0,29, p 0,35 | +0,26 |
| Manglar − bosque | ρ 0,58, p 0,05 | ρ 0,26, p 0,42 | ρ 0,39, p 0,22 | −0,44 |

La relación con la precipitación se interpreta únicamente como una dirección: usa doce pasadas, la lluvia es un sustituto indirecto del nivel del agua y la asociación deja de distinguirse del azar al corregir la dependencia temporal (sección 3.7).

![Figura 11. Retrodispersión del manglar y del bosque frente a la precipitación acumulada durante los 30 días anteriores a cada adquisición, por sensor y trayectoria.](fig_cgsm_temporada.png)

### 3.6 La Ciénaga Grande: nivel del río Magdalena

El nivel del Magdalena en Remolino produjo una asociación más marcada con NISAR D083 que la precipitación (Tabla 9, Figura 12). Entre los tercios de nivel bajo y alto, el HH del manglar aumentó +0,47 dB, mientras que el del bosque disminuyó −0,53 dB. Como resultado, la diferencia manglar menos bosque aumentó +0,83 dB, con ρ 0,83 (p < 0,001). La polarización cruzada relativa al bosque no mostró una relación equivalente.

Tabla 9. Retrodispersión frente al nivel del río Magdalena en Remolino: diferencia entre el tercio de nivel alto y el de nivel bajo (dB) y correlación de Spearman, por sensor y traza. En Sentinel-1 entran 55 y 58 de las 58 y 61 pasadas: las tres restantes por órbita caen en un hueco de 18 días de la serie del IDEAM (12 a 30 de agosto de 2026).

| Sensor y pasada | n | Clase | Copolar (HH o VV) | Cruzada (HV o VH) | Cociente (HH−HV) |
|---|---|---|---|---|---|
| NISAR D083 (18:27) | 14 | Manglar | +0,47 dB · ρ 0,58, p 0,03 | −0,97 dB · ρ −0,74, p 0,003 | +1,27 dB · ρ 0,77, p 0,001 |
| NISAR D083 (18:27) | 14 | Bosque | −0,53 dB · ρ −0,39, p 0,16 | −1,29 dB · ρ −0,70, p 0,006 | +0,71 dB · ρ 0,71, p 0,005 |
| NISAR D083 (18:27) | 14 | Manglar − bosque | +0,83 dB · ρ 0,83, p < 0,001 | +0,35 dB · ρ 0,32, p 0,27 | +0,62 dB · ρ 0,49, p 0,08 |
| NISAR A007 (05:31) | 7 | Manglar − bosque | −0,14 dB · ρ −0,04, p 0,94 | −0,06 dB · ρ −0,39, p 0,38 | −0,30 dB · ρ −0,54, p 0,22 |
| Sentinel-1 A77 (18:06) | 55 | Manglar − bosque | −0,21 dB · ρ −0,47, p < 0,001 | +0,05 dB · ρ −0,01, p 0,95 | −0,08 dB · ρ −0,12, p 0,37 |
| Sentinel-1 D142 (05:48) | 58 | Manglar − bosque | −0,21 dB · ρ −0,33, p 0,01 | −0,14 dB · ρ −0,37, p 0,005 | −0,15 dB · ρ −0,18, p 0,18 |

La traza A007 no presentó asociación, pero sus siete adquisiciones corresponden únicamente a niveles bajos o intermedios del río, entre 0,82 y 1,58 m. Sentinel-1 mostró una respuesta diferente: la señal copolar manglar menos bosque disminuyó con el nivel en las dos órbitas, porque el VV del bosque sube con el nivel (ρ 0,39 y 0,32) y el del manglar no.

Sin embargo, en D083 el nivel del río está confundido con el periodo de adquisición y con la versión del producto. Las seis pasadas de nivel alto, entre 1,69 y 2,67 m, pertenecen a la colección Beta y las ocho de nivel bajo, entre 0,91 y 1,42 m, a la Provisional, porque en 2026 el río bajó mucho más que en 2025 para los mismos meses (media de agosto 0,96 m frente a 2,18 m). Dentro de cada versión no se observa asociación entre el nivel y el HH relativo al bosque: ρ −0,14 (p 0,79) en las seis Beta y ρ 0,55 (p 0,16) en las ocho Provisionales. Una regresión conjunta atribuye 0,12 dB por metro al nivel y −0,52 dB al cambio de versión. Por lo tanto, el ρ de 0,83 lo produce el escalón entre los dos bloques, y con las adquisiciones actuales no es posible separar los dos efectos. El HV, además, baja en las dos clases con el nivel (ρ −0,74 y −0,70), lo que puede ser estacional o de versión y no se distingue con catorce fechas.

![Figura 12. Retrodispersión del manglar y del bosque frente al nivel horario del río Magdalena en Remolino, por sensor y trayectoria.](fig_cgsm_nivel_rio.png)

### 3.7 Dependencia temporal de las correlaciones

La corrección por dependencia temporal produjo resultados distintos en los dos sitios (Tabla 10). En Bahía de Málaga, las asociaciones de NISAR con la marea se mantuvieron después de ajustar el tamaño efectivo de muestra, con p de 0,007 para A004 y de 0,008 para D087, porque un muestreo cada doce días cae en fases distintas del ciclo mareal y la marea de una pasada casi no se parece a la de la anterior (r1 de 0,15 y −0,03). ALOS-2, cuyas pasadas cada 28 días se acercan a un múltiplo del ciclo de mareas vivas y muertas, mostró mayor autocorrelación, pero las relaciones se conservaron con p corregidos de 0,031 y 0,019. Sentinel-1 permaneció sin asociación.

Tabla 10. Correlación de la resta manglar menos bosque en copolarización con su forzante, y valor p corregido por dependencia temporal con todos los rezagos hasta n/5; el texto da entre paréntesis, cuando difiere, el valor corregido solo con el rezago 1.

| Serie | Traza | n | ρ | p | r1 del forzante | r1 del radar | n efectivo | p corregido |
|---|---|---|---|---|---|---|---|---|
| NISAR, Málaga, marea | A004 | 12 | 0,83 | 0,001 | 0,15 | −0,21 | 8,7 | 0,007 |
| NISAR, Málaga, marea | D087 | 12 | 0,74 | 0,006 | −0,03 | −0,24 | 11,2 | 0,008 |
| ALOS-2, Málaga, marea | 139 | 21 | 0,65 | 0,002 | 0,60 | 0,29 | 11,1 | 0,031 |
| ALOS-2, Málaga, marea | 140 | 15 | 0,72 | 0,002 | 0,53 | 0,48 | 9,8 | 0,019 |
| Sentinel-1, Málaga, marea | 48 | 26 | −0,18 | 0,37 | 0,23 | −0,25 | 26 | 0,37 |
| Sentinel-1, Málaga, marea | 142 | 63 | −0,13 | 0,32 | −0,65 | 0,03 | 63 | 0,32 |
| NISAR, CGSM, lluvia de 30 días | D083 | 12 | 0,58 | 0,048 | 0,45 | 0,69 | 5,7 | 0,25 |
| Sentinel-1, CGSM, lluvia de 30 días | A77 | 58 | −0,35 | 0,008 | 0,89 | 0,14 | 21,1 | 0,12 |
| Sentinel-1, CGSM, lluvia de 30 días | D142 | 61 | −0,52 | < 0,001 | 0,89 | 0,32 | 24,7 | 0,009 |
| NISAR, CGSM, nivel del río | D083 | 14 | 0,83 | < 0,001 | 0,86 | 0,64 | 4,7 | 0,10 |

La versión del producto tampoco explica el resultado de Málaga. Por fecha, las doce pasadas de cada traza se reparten en siete Beta y cinco Provisionales (A004) y seis y seis (D087), y dentro de cada bloque la resta sigue subiendo con la marea, con ρ de 0,89 y 0,90 en la traza ascendente y de 0,66 y 0,77 en la descendente.

En la CGSM, la dependencia temporal redujo de forma considerable la evidencia estadística. La asociación de NISAR con la precipitación pasó de p 0,048 a p 0,25, porque la lluvia acumulada de treinta días es por construcción una serie muy suave. Para el nivel del río, la autocorrelación y la concentración de las adquisiciones en dos bloques de fechas redujeron el tamaño efectivo de 14 a 4,7 observaciones y elevaron el valor p a 0,10. El tamaño efectivo se estima con series de doce a 63 pasadas, de modo que él mismo es incierto, y la corrección atiende la dependencia entre fechas y no la dependencia entre píxeles, que no infla el valor p porque cada pasada entra como un solo número por clase.

En consecuencia, la evidencia más robusta procede de Bahía de Málaga, donde la respuesta copolar en banda L se reproduce en NISAR y ALOS-2, resiste la corrección por dependencia temporal y se mantiene dentro de cada versión del producto. En la CGSM, la dirección observada con NISAR es consistente con ese patrón, pero la asociación con la lluvia no resiste la corrección temporal y la relación con el nivel del río no es identificable frente al periodo y la versión del producto. Su evaluación requiere pasadas de nivel alto dentro de la colección Provisional.

### 3.8 Clave de interpretación por cobertura y mecanismo

Las firmas multifecha de las coberturas principales muestran que las bandas C y L resuelven confusiones diferentes (Tabla 11, Figura 13). En banda C, el manglar y el humedal herbáceo presentan valores prácticamente coincidentes, mientras que en banda L sus medianas se separan en HH y en HH − HV. La vegetación flotante, en cambio, permanece más próxima al agua abierta en banda L que en banda C.

Tabla 11. Firma de cada cobertura de la CGSM en las dos bandas: mediana entre pasadas del copolar, del cruzado y de su diferencia, en dB (la diferencia es la mediana de la resta por pasada, no la resta de las medianas). Banda C, Sentinel-1 traza descendente 142, 61 pasadas; banda L, NISAR traza descendente 083, 14 pasadas. La vegetación flotante no es una clase de los productos globales y se define por la firma óptica de diciembre de 2025, cuando el evento ya cubría el 55,7 % de la zona ZC-2025-v1, el polígono de vegetación flotante de 2025 delimitado sobre Sentinel-2 en el cubo de datos de la tesis.

| Cobertura | VV | VH | VV − VH | HH | HV | HH − HV |
|---|---|---|---|---|---|---|
| Agua abierta | −21,1 | −30,9 | 9,0 | −20,0 | −25,6 | 6,1 |
| Vegetación flotante | −13,3 | −20,7 | 7,5 | −16,6 | −23,3 | 6,6 |
| Humedal herbáceo | −9,9 | −15,2 | 5,3 | −9,2 | −17,5 | 7,9 |
| Manglar | −9,6 | −14,9 | 5,3 | −10,9 | −17,2 | 6,1 |
| Bosque seco (control) | −8,1 | −14,3 | 6,2 | −9,2 | −15,9 | 6,6 |

![Figura 13. Espacio de firmas de las coberturas de la CGSM en bandas C y L, definido por la retrodispersión copolar y la diferencia copolar menos cruzada.](fig_clave_firmas.png)

#### Evaluación con la muestra de referencia de 2025

La clave se evaluó después con los 720 puntos de referencia etiquetados sobre imágenes de alta resolución de 2025. Para cada punto se extrajo la mediana multifecha de Sentinel-1 y de NISAR (Tabla 12), y la separabilidad entre pares de clases se calculó con la distancia de Jeffries-Matusita (Tabla 13).

La muestra modificó parte de la interpretación obtenida con los productos globales. La mayor mejora de la banda L se observó entre manglar intacto y manglar degradado, cuya separabilidad aumentó de 0,30 en banda C a 0,91 en banda L, todavía por debajo del umbral de 1. Sin embargo, humedal herbáceo y manglar degradado permanecieron prácticamente inseparables, con 0,17 en C, 0,22 en L y 0,38 al combinar las dos bandas, lo mismo que ocurre con el NDVI de Sentinel-2 en la muestra (0,44). La vegetación flotante tampoco presentó una firma radar separable del agua abierta (0,28 en L y 0,47 en C): de sus 129 puntos, 42 caen en la firma del agua.

Tabla 12. Firma de cada clase de la muestra de referencia de 2025 en las dos bandas: mediana entre puntos de la mediana entre pasadas, en dB, con el rango intercuartil de la diferencia HH − HV. Banda C, Sentinel-1 traza 142, 61 pasadas; banda L, NISAR traza 083, 14 escenas.

| Clase | n | VV | VH | VV − VH | HH | HV | HH − HV | HH − HV, cuartiles |
|---|---|---|---|---|---|---|---|---|
| Agua | 212 | −21,5 | −29,6 | 7,5 | −19,9 | −25,4 | 5,9 | 5,0 a 6,5 |
| Vegetación flotante | 129 | −15,2 | −22,7 | 6,7 | −17,0 | −23,7 | 6,8 | 5,6 a 7,8 |
| Manglar intacto | 151 | −9,5 | −14,8 | 5,5 | −10,0 | −16,7 | 6,6 | 6,0 a 7,4 |
| Manglar degradado | 111 | −10,7 | −15,9 | 5,3 | −8,3 | −16,8 | 8,9 | 7,5 a 10,7 |
| Humedal herbáceo | 73 | −10,4 | −15,9 | 5,4 | −9,6 | −17,3 | 7,9 | 7,3 a 8,6 |
| Otro | 44 | −10,1 | −15,4 | 6,0 | −10,7 | −18,3 | 7,5 | 6,6 a 8,6 |

La diferencia HH − HV ordenó las coberturas según la apertura del dosel: 6,6 dB en manglar intacto, 7,5 dB en la clase otro, 7,9 dB en humedal herbáceo y 8,9 dB en manglar degradado. Por lo tanto, esta variable no identifica por sí sola una cobertura específica, sino que distingue doseles cerrados de superficies con vegetación más abierta.

Tabla 13. Separabilidad de Jeffries-Matusita por pares de clases de la muestra de 2025, con las variables de banda C (VV, VH, VV − VH), de banda L (HH, HV, HH − HV) y de las dos bandas.

| Par | Banda C | Banda L | C + L |
|---|---|---|---|
| Agua, vegetación flotante | 0,47 | 0,28 | 0,69 |
| Agua, humedal herbáceo | 1,50 | 1,24 | 1,66 |
| Agua, manglar degradado | 1,65 | 1,56 | 1,82 |
| Agua, manglar intacto | 1,85 | 1,87 | 1,96 |
| Agua, otro | 1,51 | 1,27 | 1,69 |
| Vegetación flotante, humedal herbáceo | 0,74 | 0,64 | 1,02 |
| Vegetación flotante, manglar degradado | 0,94 | 0,97 | 1,33 |
| Vegetación flotante, manglar intacto | 1,34 | 1,59 | 1,78 |
| Vegetación flotante, otro | 0,64 | 0,77 | 1,09 |
| Humedal herbáceo, manglar degradado | 0,17 | 0,22 | 0,38 |
| Humedal herbáceo, manglar intacto | 0,45 | 0,76 | 0,96 |
| Humedal herbáceo, otro | 0,12 | 0,17 | 0,43 |
| Manglar degradado, manglar intacto | 0,30 | 0,91 | 1,04 |
| Manglar degradado, otro | 0,27 | 0,47 | 0,69 |
| Manglar intacto, otro | 0,56 | 0,54 | 0,89 |

#### Regla de lectura

Con base en la muestra de 2025, la clave se redujo a cuatro decisiones aplicadas sobre las medianas multifecha:

1. Agua abierta: VV por debajo de −17 dB y VH por debajo de −25 dB.
2. Superficie oscura con vegetación o borde: VV por debajo de −12 dB sin cumplir la condición anterior. Con VV − VH de 6,5 dB o más es compatible con vegetación flotante, y los casos restantes requieren apoyo óptico.
3. Dosel cerrado: VV de −12 dB o más y HH − HV por debajo de 7,3 dB, compatible sobre todo con manglar intacto.
4. Dosel abierto o herbáceo: VV de −12 dB o más y HH − HV de 7,3 dB o más. En este grupo quedan el manglar degradado, el humedal herbáceo y parte de la clase otro, que no se separan de forma fiable solo con estas bandas.

La respuesta hidrológica se usa además para distinguir el manglar del bosque no inundable, puesto que la diferencia de nivel entre las dos clases, 1,5 dB en VV y 1,7 dB en HH (Tabla 11), es del orden de la que produce la geometría entre trazas (hasta 1,4 dB, Tabla 3). El criterio no es el nivel absoluto de retrodispersión sino el cambio del canal copolar con el forzante. En Bahía de Málaga, el HH del manglar relativo al bosque aumentó con la marea en las dos trayectorias y la cruzada no respondió. En la CGSM se observó la misma dirección con el nivel del río, aunque allí permanece confundida con la versión del producto.

La regla tomó una decisión en 606 de los 720 puntos y acertó en 415, el 68 % de los puntos decididos y el 58 % de la muestra completa (Tabla 14). Como los umbrales se definieron y evaluaron sobre los mismos datos, estas cifras corresponden a resustitución y no a una validación independiente.

Tabla 14. Lo que la regla decide en los 720 puntos de la muestra de 2025 (filas, clase de referencia; columnas, pasos 1 a 4 de la regla). La regla decide en 606 puntos y acierta en 415, el 68 % de los decididos y el 58 % de los 720, con un 16 % sin decisión y con las tres clases de dosel abierto agrupadas; sin los 208 puntos marcados como borde decide en 444 de 512 y acierta en el 71 %.

| Clase de referencia | 1 Agua abierta | 2 Vegetación flotante | 3 Manglar intacto | 4 Dosel abierto o herbáceo | Sin decisión |
|---|---|---|---|---|---|
| Agua | **159** | 7 | 5 | 5 | 36 |
| Vegetación flotante | 42 | **27** | 14 | 25 | 21 |
| Manglar intacto | 0 | 0 | **107** | 32 | 12 |
| Manglar degradado | 2 | 4 | 19 | **62** | 24 |
| Humedal herbáceo | 3 | 2 | 11 | **40** | 17 |
| Otro | 2 | 3 | 15 | **20** | 4 |

### 3.9 Distribución espacial de la señal y contraste óptico

La señal hidrológica se cartografió a 50 m con la diferencia entre las medianas de las adquisiciones de nivel alto y bajo del río, seis y ocho pasadas de NISAR D083. Este reparto aumenta el número de adquisiciones por grupo respecto a la prueba por clases, pero mantiene la confusión entre nivel hidrológico y versión del producto.

El cambio de HH mostró una marcada estructura espacial (Tabla 15, Figura 14). Para el manglar completo la mediana fue de solo +0,07 dB, pero en el sector sur aumentó a +0,53 dB con el 77 % de los píxeles positivos. En el norte, sobre Isla de Salamanca, donde entra el caño Clarín, la mediana fue de −0,18 dB. El bosque seco de control disminuyó −0,36 dB.

Tabla 15. Diferencia alto menos bajo del nivel del río por píxel de 50 m (mediana y, para el copolar, cuartiles; dB) y fracción de píxeles con diferencia positiva, por clase y por sector del manglar. Banda L: seis pasadas de nivel alto y ocho de nivel bajo de NISAR D083; banda C: 13 y 18 pasadas de Sentinel-1 órbita 142 en las mismas dos ventanas de fechas.

| Clase o sector | Píxeles | ΔHH (L) | ΔHH > 0 | ΔHV (L) | Δ(HH − HV) | ΔVV (C) | ΔVV > 0 | ΔVH (C) |
|---|---|---|---|---|---|---|---|---|
| Manglar, todo | 145.398 | +0,07 (−0,47 a +0,63) | 53 % | −1,13 | +1,21 | +0,09 (−0,15 a +0,33) | 61 % | +0,01 |
| Manglar norte, Isla de Salamanca (N > 1205 km) | 69.063 | −0,18 (−0,64 a +0,30) | 40 % | −1,08 | +0,93 | +0,05 (−0,17 a +0,30) | 56 % | −0,02 |
| Manglar centro y occidente (1190 a 1205 km) | 33.412 | +0,02 (−0,52 a +0,57) | 51 % | −1,23 | +1,25 | +0,02 (−0,22 a +0,24) | 53 % | +0,01 |
| Manglar sur, desembocadura del río Fundación (N < 1190 km) | 42.923 | **+0,53 (+0,05 a +0,99)** | **77 %** | −1,15 | +1,66 | +0,21 (−0,01 a +0,39) | 74 % | +0,06 |
| Bosque seco (control) | 316.807 | −0,36 (−0,89 a +0,21) | 33 % | −1,18 | +0,84 | **+0,36 (+0,13 a +0,63)** | **86 %** | +0,21 |
| Humedal herbáceo | 207.215 | +0,46 (−0,54 a +1,82) | 62 % | −0,96 | +1,41 | +0,26 (−0,22 a +0,80) | 65 % | +0,31 |
| Agua abierta | 663.486 | −0,39 (−0,89 a +0,02) | 26 % | −1,21 | +0,73 | −0,47 (−1,08 a 0,00) | 25 % | +0,62 |

![Figura 14. Cambio de HH, HV y HH − HV de NISAR D083 entre los periodos de nivel alto y bajo del río, sobre una malla de 50 m.](fig_mapa_doble_rebote.png)

El máximo aumento se localizó en la desembocadura del río Fundación, que baja de la Sierra Nevada, y no en las entradas de los caños del Magdalena. Cruzado con los cauces con nombre de OpenStreetMap, el foco (este 555 a 565 km, mediana +0,67 dB, 85 % de píxeles positivos) queda a 1,3 km del cauce del Fundación, mientras que el caño Renegado termina al occidente, a 11 km del manglar, en una franja donde el cambio es menor (+0,09 a +0,25 dB). Por lo tanto, el nivel registrado en Remolino funciona en este sector como indicador regional del estado hidrológico y no como causa espacial de la señal. Además, el humedal herbáceo presentó un aumento de HH similar al del manglar del sur (+0,46 dB), lo que indica que el canal copolar también responde a agua o suelo expuesto fuera del dosel. Los sectores se trazaron por latitud antes de verificar la hidrografía, de modo que la lectura por sector es una hipótesis para la serie siguiente y no un resultado.

HV disminuyó cerca de 1 dB en todas las coberturas, incluida el agua abierta. Ese comportamiento común es incompatible con una explicación exclusiva por inundación bajo dosel y señala un efecto de versión del producto o de estacionalidad. Por esta razón, la interpretación espacial se concentra en el HH del manglar relativo al bosque y no en HH − HV.

La comparación espacial con Sentinel-1 mostró un patrón distinto (Figura 15). En banda C, el manglar aumentó +0,09 dB y el bosque +0,36 dB, de modo que la diferencia manglar menos bosque fue negativa, como en la Tabla 9. En banda L, el manglar aumentó mientras el bosque disminuyó, y la correspondencia por píxel entre ΔHH y ΔVV sobre el manglar fue débil (ρ 0,21), un valor que no se somete a prueba por la autocorrelación espacial pero que indica que los dos cambios no comparten el mismo patrón.

![Figura 15. Cambio copolar entre los mismos periodos en NISAR (HH) y Sentinel-1 (VV), sobre una malla común de 50 m.](fig_mapa_c_vs_l.png)

#### Contraste con Dynamic World

Dynamic World mostró una respuesta al nivel del río únicamente donde la inundación es visible desde el óptico (Figura 16). En el humedal herbáceo, la probabilidad media de `flooded_vegetation` en las 54 fechas sin nubes aumentó con el nivel (ρ 0,41, p 0,002, sin corregir por dependencia temporal), mientras que no hubo relación en el bosque (ρ −0,02) ni en el manglar (ρ 0,04, p 0,79).

La comparación espacial con NISAR produjo una correlación débil y negativa sobre el manglar (ρ −0,15). Donde Dynamic World registró más agua visible, el HH tendió a disminuir, y donde el óptico no mostró cambios, el HH tendió a aumentar. Este patrón es compatible con una diferencia entre agua expuesta y agua bajo el dosel, pero no constituye una validación independiente del doble rebote.

![Figura 16. Contraste entre el nivel del río, la probabilidad de vegetación inundada de Dynamic World y el cambio de HH de NISAR.](fig_corroboracion_dw.png)

#### Distribución espacial en Bahía de Málaga

En Bahía de Málaga se repitió el análisis con las seis pasadas de mayor y de menor marea de cada trayectoria (Tabla 16, Figura 17). En A004, el HH del manglar aumentó +0,34 dB con el 75 % de los píxeles positivos y el bosque disminuyó −0,10 dB. En D087, el manglar cambió +0,05 dB y el bosque −0,39 dB. Esa caída del bosque coincide con la versión del producto: en esa traza cuatro de las seis pasadas de marea alta son Beta y cuatro de las seis de marea baja son Provisionales, y la versión desplaza el HH de todas las clases, de modo que la resta cancela ese desplazamiento y no describe una caída real del bosque. En las dos trayectorias, la diferencia manglar menos bosque fue de +0,44 dB, próxima a los +0,57 dB de la comparación por puntos.

Tabla 16. Bahía de Málaga: diferencia marea alta menos marea baja por píxel de 50 m (mediana y cuartiles, dB) y fracción de píxeles positivos, por traza y clase. Seis pasadas por grupo en cada traza; el humedal herbáceo tiene solo 224 píxeles y se omite.

| Traza | Clase | Píxeles | ΔHH | ΔHH > 0 | ΔHV | Δ(HH − HV) |
|---|---|---|---|---|---|---|
| A004 (05:46) | Manglar | 34.344 | +0,34 (−0,01 a +0,69) | 75 % | −0,36 | +0,70 |
| A004 (05:46) | Bosque (control) | 300.038 | −0,10 (−0,36 a +0,17) | 40 % | −0,34 | +0,25 |
| A004 (05:46) | Agua | 214.339 | −0,07 (−0,45 a +0,30) | 45 % | −0,51 | +0,43 |
| D087 (18:29) | Manglar | 34.344 | +0,05 (−0,35 a +0,42) | 54 % | −0,53 | +0,64 |
| D087 (18:29) | Bosque (control) | 300.038 | −0,39 (−0,79 a −0,06) | 21 % | −0,63 | +0,32 |
| D087 (18:29) | Agua | 214.339 | −0,42 (−0,90 a +0,05) | 27 % | −0,94 | +0,63 |

La señal positiva de HH se distribuyó a lo largo de las franjas de manglar de la bahía, sin concentrarse en un único sector. HV disminuyó en todas las coberturas y, por lo tanto, tampoco se usó como firma independiente.

![Figura 17. Cambio de HH y HV entre las seis pasadas de mayor y menor marea de cada trayectoria de NISAR en Bahía de Málaga, sobre una malla de 50 m.](fig_mapa_doble_rebote_malaga.png)

## 4. Discusión

La banda L aporta información sobre la inundación bajo dosel que no aparece de la misma forma en banda C. En Bahía de Málaga, el HH del manglar relativo al bosque aumentó con la marea en las dos trayectorias de NISAR y el mismo patrón se reprodujo con ALOS-2, mientras que Sentinel-1 no mostró una respuesta equivalente. Además, las asociaciones de los dos sensores de banda L permanecieron después de corregir la dependencia temporal y, en NISAR, dentro de cada versión del producto. En la CGSM, NISAR mostró la misma dirección frente al nivel del río, pero las adquisiciones de nivel alto y bajo coinciden con las colecciones Beta y Provisional, de modo que los dos efectos no pueden separarse con la serie actual.

El aumento del copolar relativo al bosque fue pequeño, del orden de 0,4 a 0,8 dB, frente a los realces de varios decibelios descritos para otros bosques inundados en banda L (Hess et al., 1990). Esta menor amplitud puede estar relacionada con la atenuación de un dosel de manglar denso, con la presencia parcial de agua dentro del píxel y con la variabilidad del nivel entre adquisiciones. La disponibilidad únicamente de polarización dual impide, además, aislar el mecanismo con observables polarimétricos completos. Por ello, los resultados son compatibles con una contribución de doble rebote, pero no constituyen una separación polarimétrica directa del mecanismo.

La comparación entre bandas tampoco puede atribuirse exclusivamente a la longitud de onda, puesto que NISAR y ALOS-2 observan HH mientras que Sentinel-1 usa VV. Sin embargo, la coincidencia entre dos sensores de banda L con geometrías y horarios diferentes, junto con la ausencia de una respuesta equivalente en HV y en Sentinel-1, refuerza la interpretación de una interacción específica entre la señal copolar de banda L y el estado de inundación del manglar. En banda C, el VV del bosque seco responde a la humedad del dosel y del suelo más que el del manglar, y por eso la resta sale negativa en la ciénaga.

La banda L también modificó la separación entre coberturas. Su mayor mejora se observó entre manglar intacto y degradado, cuya separabilidad aumentó de 0,30 en banda C a 0,91 en banda L. No obstante, esa mejora sigue por debajo de una separación completa. La diferencia HH − HV respondió sobre todo a la apertura del dosel, menor en manglar intacto y mayor en manglar degradado y humedal herbáceo. En consecuencia, esta variable sirve para caracterizar estructura, pero no funciona como etiqueta única de cobertura. La principal ambigüedad permanece entre manglar degradado y humedal herbáceo, que ninguna de las dos bandas separó de forma fiable.

La cartografía a 50 m mostró además que la respuesta de banda L no es espacialmente uniforme. En la CGSM, el mayor incremento de HH se concentró en el manglar del sur, en la desembocadura del río Fundación, mientras que hacia el norte disminuyó o cambió de signo. Esta distribución indica que el nivel del Magdalena en Remolino debe interpretarse como un indicador regional del estado hidrológico y no como el forzante directo de cada sector del humedal. Sentinel-1 presentó un cambio espacial más débil y una respuesta mayor en el bosque seco que en el manglar.

Dynamic World aportó un contraste complementario. La probabilidad de vegetación inundada aumentó con el nivel del río en el humedal herbáceo, pero no en el manglar. Esto confirma que el forzante hidrológico produce cambios detectables donde el agua queda expuesta, pero no valida directamente la señal bajo dosel. La complementariedad entre los dos tipos de observación es precisamente esa diferencia: el óptico responde al agua visible, mientras que la banda L conserva información en los sectores cubiertos por vegetación leñosa.

### 4.1 Limitaciones

El estudio presenta cuatro limitaciones principales. En primer lugar, los datos disponibles son de polarización dual, HH y HV en banda L y VV y VH en banda C. Por lo tanto, los mecanismos de dispersión se infieren de la intensidad y de su respuesta hidrológica, sin una descomposición polarimétrica completa, y la comparación entre bandas combina diferencias de longitud de onda y de polarización.

En segundo lugar, la evidencia de la CGSM depende todavía de una serie NISAR corta. Las 14 adquisiciones de D083 se dividen en dos bloques de fechas que coinciden con las colecciones Beta y Provisional y con estados distintos del río. La corrección por dependencia temporal reduce el tamaño efectivo de muestra y la relación con el nivel deja de ser concluyente. Por ello, la CGSM aporta una dirección coherente con Málaga, pero no una confirmación independiente.

En tercer lugar, la clave de interpretación se definió y se evaluó con los mismos 720 puntos. El 68 % de acierto corresponde, por lo tanto, a resustitución y no al desempeño sobre una muestra independiente, que será la muestra de validación de la tesis. Además, las observaciones de radar abarcan 2025 y 2026, mientras que las etiquetas representan las condiciones de las imágenes de 2025, de modo que parte del desacuerdo puede corresponder a cambios reales de cobertura, sobre todo en la vegetación flotante, que es un evento en curso.

Finalmente, la propia referencia presenta incertidumbre, medida como consistencia de una sola intérprete y no como exactitud. En una segunda interpretación a ciegas de 60 puntos bajo el criterio escrito, siete días después de la última sesión de etiquetado, el acuerdo con la referencia fue del 78 % [66 a 87 %], con kappa 0,72 (Figura 18). El manglar intacto y el degradado fueron consistentes en todos los puntos reevaluados, mientras que el humedal herbáceo presentó la mayor inestabilidad, con 2 de 7. Esa incertidumbre se concentra precisamente en una de las fronteras que las bandas C y L tampoco resuelven.

![Figura 18. Consistencia de una misma intérprete sobre la muestra de referencia de 2025, con una segunda interpretación a ciegas de 60 puntos. Acuerdo 0,78 [0,66 a 0,87], kappa 0,72.](fig_consistencia_2025.png)

## 5. Conclusiones y trabajo futuro

En Bahía de Málaga, la banda L mostró una respuesta reproducible del copolar del manglar a la marea que no apareció en banda C. El patrón se observó de manera independiente en las dos trayectorias de NISAR, se reprodujo con ALOS-2, permaneció después de corregir la dependencia temporal y se mantuvo dentro de cada versión del producto. La respuesta se concentró en HH y no en HV, y fue compatible con un incremento de la contribución de doble rebote bajo mayor inundación.

En la CGSM, NISAR mostró una dirección similar frente al nivel del río, con un aumento de +0,83 dB del HH del manglar relativo al bosque entre los estados bajo y alto. Sin embargo, las adquisiciones de los dos estados corresponden a versiones distintas del producto, dentro de cada versión no hay relación con el nivel y la asociación no resiste la corrección por dependencia temporal. Con la serie actual, por lo tanto, el efecto del nivel del río no puede separarse del cambio de periodo y de versión.

La banda L también aportó información estructural. La separabilidad entre manglar intacto y degradado aumentó de 0,30 en banda C a 0,91 en banda L, mientras que HH − HV ordenó las coberturas según la apertura del dosel. Ninguna de las bandas resolvió la frontera entre manglar degradado y humedal herbáceo. La clave resultante decidió 606 de los 720 puntos de referencia y alcanzó un 68 % de acierto entre los casos decididos, valor que corresponde a resustitución y deberá evaluarse con una muestra independiente.

El trabajo futuro se concentra en tres frentes. En primer lugar, ampliar la serie NISAR D083 hasta disponer de estados altos y bajos del río dentro de una misma versión del producto y contrastarlos con los niveles medidos dentro de la ciénaga y sus caños, ya solicitados a INVEMAR. En segundo lugar, repetir la cartografía espacial con adquisiciones radiométricamente comparables, con el fin de separar el desplazamiento del HV de la señal del HH. En tercer lugar, evaluar la clave sobre una muestra independiente y del mismo año que las adquisiciones SAR.

Finalmente, queda una vía que ninguno de los tres sensores permite. Con polarización dual no hay fase entre HH y VV, y el doble rebote se infiere del nivel de HH frente al bosque de control. Una escena polarimétrica completa de banda P de BIOMASS sobre la ciénaga permitiría verlo de forma directa en la componente HH − VV de la base de Pauli y en la fase copolar. Su disponibilidad sobre el sitio no se ha verificado.

## Disponibilidad de datos y código

Los guiones de las nueve etapas, los resultados tabulados y las figuras del informe están en el repositorio público https://github.com/linaq11/cgsm-radar-banda-L, bajo licencia MIT. Las escenas NISAR, las series del IDEAM y del mareógrafo y los productos de Earth Engine se obtienen de sus fuentes con los guiones de la etapa 1; la muestra de referencia de 2025 pertenece a la tesis y no se distribuye con el informe.

## Referencias

Botero, L. y Salzwedel, H. (1999). Rehabilitation of the Ciénaga Grande de Santa Marta, a mangrove-estuarine system in the Caribbean coast of Colombia. *Ocean & Coastal Management, 42*(2-4), 243-256. https://doi.org/10.1016/S0964-5691(98)00056-8

Brown, C. F., Brumby, S. P., Guzder-Williams, B., Birch, T., Hyde, S. B., Mazzariello, J., Czerwinski, W., Pasquarella, V. J., Haertel, R., Ilyushchenko, S., Schwehr, K., Weisse, M., Stolle, F., Hanson, C., Guinan, O., Moore, R. y Tait, A. M. (2022). Dynamic World, near real-time global 10 m land use land cover mapping. *Scientific Data, 9*, Artículo 251. https://doi.org/10.1038/s41597-022-01307-4

Bunting, P., Rosenqvist, A., Hilarides, L., Lucas, R. M., Thomas, N., Tadono, T., Worthington, T. A., Spalding, M., Murray, N. J. y Rebelo, L.-M. (2022). Global mangrove extent change 1996-2020: Global Mangrove Watch version 3.0. *Remote Sensing, 14*(15), Artículo 3657. https://doi.org/10.3390/rs14153657

Caldwell, P. C., Merrifield, M. A. y Thompson, P. R. (2015). *Sea level measured by tide gauges from global oceans: The Joint Archive for Sea Level holdings* (NCEI Accession 0019568, versión 5.5) [Conjunto de datos]. NOAA National Centers for Environmental Information. https://doi.org/10.7289/V5V40S7W

De Luca, G., Silva, J. M. N. y Modica, G. (2021). A workflow based on Sentinel-1 SAR data and open-source algorithms for unsupervised burned area detection in Mediterranean ecosystems. *GIScience & Remote Sensing, 58*(4), 516-541. https://doi.org/10.1080/15481603.2021.1907896

Dirección General Marítima. (s. f.). [Pronóstico de pleamares y bajamares para Málaga, año 2026, Centro de Investigaciones Oceanográficas e Hidrográficas del Pacífico] [Conjunto de datos]. DIMAR.

Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., Hoersch, B., Isola, C., Laberinti, P., Martimort, P., Meygret, A., Spoto, F., Sy, O., Marchese, F. y Bargellini, P. (2012). Sentinel-2: ESA's optical high-resolution mission for GMES operational services. *Remote Sensing of Environment, 120*, 25-36. https://doi.org/10.1016/j.rse.2011.11.026

Expert Flood Monitoring Alliance. (2022). *Provision of an automated, global, satellite-based flood monitoring product for the Copernicus Emergency Management Service: Product Definition Document (PDD)* (Documento GFM D6, versión 1.4). Copernicus Emergency Management Service. https://elib.dlr.de/195173/1/gfm_pdd_v1_4_20220420_edit.pdf

Google. (s. f.). *Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected, log scaling* [Conjunto de datos]. Earth Engine Data Catalog. https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D. y Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment, 202*, 18-27. https://doi.org/10.1016/j.rse.2017.06.031

Hess, L. L., Melack, J. M. y Simonett, D. S. (1990). Radar detection of flooding beneath the forest canopy: A review. *International Journal of Remote Sensing, 11*(7), 1313-1325. https://doi.org/10.1080/01431169008955095

Instituto de Hidrología, Meteorología y Estudios Ambientales [IDEAM]. (s. f.). [Nivel instantáneo del río Magdalena en la estación automática Remolino, código 2904700095] [Conjunto de datos]. Datos Abiertos Colombia. https://www.datos.gov.co/d/bdmn-sqnh

Jaramillo, F., Brown, I., Castellazzi, P., Espinosa, L., Guittard, A., Hong, S.-H., Rivera-Monroy, V. H. y Wdowinski, S. (2018). Assessment of hydrologic connectivity in an ungauged wetland with InSAR observations. *Environmental Research Letters, 13*(2), 024003. https://doi.org/10.1088/1748-9326/aa9d23

JAXA EORC. (s. f.). *ALOS-2 PALSAR-2 ScanSAR products, Level 2.2* [Conjunto de datos]. Japan Aerospace Exploration Agency, Earth Observation Research Center. https://www.eorc.jaxa.jp/ALOS/en/dataset/palsar2_l22_e.htm

Lucas, R., Rebelo, L.-M., Fatoyinbo, L., Rosenqvist, A., Itoh, T., Shimada, M., Simard, M., Souza-Filho, P. W., Thomas, N., Trettin, C., Accad, A., Carreiras, J. y Hilarides, L. (2014). Contribution of L-band SAR to systematic global mangrove monitoring. *Marine and Freshwater Research, 65*(7), 589-603. https://doi.org/10.1071/MF13177

Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., Boussetta, S., Choulga, M., Harrigan, S., Hersbach, H., Martens, B., Miralles, D. G., Piles, M., Rodríguez-Fernández, N. J., Zsoter, E., Buontempo, C. y Thépaut, J.-N. (2021). ERA5-Land: A state-of-the-art global reanalysis dataset for land applications. *Earth System Science Data, 13*(9), 4349-4383. https://doi.org/10.5194/essd-13-4349-2021

NASA ASF DAAC. (2026a). *NISAR Beta Geocoded Polarimetric Covariance product (Version 1)* [Conjunto de datos]. NASA Alaska Satellite Facility Distributed Active Archive Center. https://doi.org/10.5067/NIL2GCOV-B1

NASA ASF DAAC. (2026b). *NISAR Provisional Geocoded Polarimetric Covariance product (Version 1)* [Conjunto de datos]. NASA Alaska Satellite Facility Distributed Active Archive Center. https://nisar-docs.asf.alaska.edu/gcov/

Pasquarella, V. J., Brown, C. F., Czerwinski, W. y Rucklidge, W. J. (2023). Comprehensive quality assessment of optical satellite imagery using weakly supervised video learning. En *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops* (pp. 2125-2135). https://doi.org/10.1109/CVPRW59228.2023.00206

Pyper, B. J. y Peterman, R. M. (1998). Comparison of methods to account for autocorrelation in correlation analyses of fish data. *Canadian Journal of Fisheries and Aquatic Sciences, 55*(9), 2127-2140. https://doi.org/10.1139/f98-104

Richards, J. A. (2013). *Remote sensing digital image analysis: An introduction* (5.ª ed.). Springer. https://doi.org/10.1007/978-3-642-30062-2

Richards, J. A., Woodgate, P. W. y Skidmore, A. K. (1987). An explanation of enhanced radar backscattering from flooded forests. *International Journal of Remote Sensing, 8*(7), 1093-1100. https://doi.org/10.1080/01431168708954756

Simard, M., Rivera-Monroy, V. H., Mancera-Pineda, J. E., Castañeda-Moya, E. y Twilley, R. R. (2008). A systematic method for 3D mapping of mangrove forests based on Shuttle Radar Topography Mission elevation data, ICESat/GLAS waveforms and field data: Application to Ciénaga Grande de Santa Marta, Colombia. *Remote Sensing of Environment, 112*(5), 2131-2144. https://doi.org/10.1016/j.rse.2007.10.012

Torres, R., Snoeij, P., Geudtner, D., Bibby, D., Davidson, M., Attema, E., Potin, P., Rommen, B., Floury, N., Brown, M., Navas Traver, I., Deghaye, P., Duesmann, B., Rosich, B., Miranda, N., Bruno, C., L'Abbate, M., Croci, R., Pietropaolo, A., ... Rostan, F. (2012). GMES Sentinel-1 mission. *Remote Sensing of Environment, 120*, 9-24. https://doi.org/10.1016/j.rse.2011.05.028

Yordanov, V. y Brovelli, M. A. (2021). Deforestation mapping using Sentinel-1 and object-based random forest classification on Google Earth Engine. *The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, XLIII-B3-2021*, 865-872. https://doi.org/10.5194/isprs-archives-XLIII-B3-2021-865-2021

Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., Brockmann, C., Kirches, G., Wevers, J., Cartus, O., Santoro, M., Fritz, S., Lesiv, M., Herold, M., Tsendbazar, N.-E., Xu, P., Ramoino, F. y Arino, O. (2022). *ESA WorldCover 10 m 2021 v200* [Conjunto de datos]. Zenodo. https://doi.org/10.5281/zenodo.7254221

## Anexo A. Guiones por etapa

La Figura A2 es el flujo de trabajo en nueve etapas, cada una resumida en una línea con el producto que escribe a su izquierda. La Figura A1 abre sus tres primeras etapas por sensor, con la convención de los flujos de trabajo SAR revisados en el curso (De Luca et al., 2021; Yordanov y Brovelli, 2021): adquisición, calibración radiométrica y promediado, con los productos intermedios y sus conteos a la izquierda y el software a la derecha. Las Figuras 1 y A2 se generan con `figura_diseno.py` y `figura_flujo.py`; los recortes de la Figura A1 se exportan con `exportar_figuras_flujo.py` (carpeta `figuras para flujo`).

![Figura A2. Flujo de trabajo del proyecto de radar en nueve etapas, del acceso a datos al mapa espacial y el contraste óptico. Cada etapa se resume en una línea; la columna izquierda lleva el producto que escribe cada etapa, con los conteos de escenas, pasadas y puntos que reporta el texto. La flecha discontinua marca la etapa con pendientes. Las etapas 1 a 3 se abren por sensor en la Figura A1; los guiones de cada etapa se listan en la Tabla A1.](fig_flujo_trabajo.png)

![Figura A1. Cadena de procesamiento SAR por sensor en cinco pasos: adquisición y selección, calibración radiométrica, preparación para el análisis, salida para extracción, y extracción y organización comunes a los tres sensores. Los recortes son pasadas reales sobre la caja de la CGSM: NISAR GCOV HH (traza D083, 29 de octubre de 2025), ALOS-2 ScanSAR HH (2 de diciembre de 2025) y Sentinel-1 GRD VV (órbita 142, 9 de enero de 2026).](fig_cadena_sar_sensores.png)

Tabla A1. Etapas del flujo de trabajo (Figura A2), guiones que las ejecutan y salidas. Los guiones están en la carpeta `RADAR` del repositorio; los numerados, en `AVANCE TESIS/PUBLICACION_GEE`. La versión detallada del diagrama, con todas las operaciones de cada etapa, se genera con `figura_flujo.py --detalle`.

| Etapa | Guiones | Salidas |
|---|---|---|
| 1. Acceso a datos | `16_inventario_nisar`, `17_descargar_nisar`, `18_nisar_recorte_remoto`, `23_nisar_recorte_pacifico`, `24_nisar_recorte_cgsm`, `nivel_ideam_descarga` | Tabla 1; `nisar_cgsm_granulos.json`, escenas `NISAR_AOI_*.h5` (45), `nivel_ideam_*.csv` |
| 2. Preprocesamiento y calibración | `18_nisar_recorte_remoto`, `20_nisar_incidencia`, `alos2_marea_malaga`, `s1_marea_malaga` | σ⁰ por sensor y pasada; malla de incidencia de NISAR; Figura 4 |
| 3. Coberturas de referencia y muestreo | `perfil_pacifico_24`, `doble_rebote_incidencia`, `figuras_cgsm`, `figuras_pacifico` | 1.600 puntos por sitio; 2.444 de manglar y 2.400 de bosque para los tercios de incidencia; Figura 2 |
| 4. Forzante hidrológico | `mareas_buenaventura`, `mareas_dimar_a_serie`, `marea_vs_radar`, `cgsm_nivel_rio` | marea, lluvia o nivel del río a la hora de cada pasada |
| 5. Estadística por pasada | `perfil_pacifico_24`, `marea_vs_radar`, `cgsm_temporada` | `cgsm_temporada_*.csv`; Tablas 2 y 3 |
| 6. Prueba hidrológica | `marea_vs_radar`, `s1_marea_malaga`, `alos2_marea_malaga`, `cgsm_temporada`, `cgsm_nivel_rio`, `figura_cgsm_optico` | Tablas 4 a 9; Figuras 5, 7, 8, 9 a 12 |
| 7. Robustez y límites | `doble_rebote_incidencia`, `autocorrelacion_temporal`, `auditoria_calculos.md` | Tabla 10, Figura 6; nota de auditoría del 16-sep-2026 |
| 8. Clave de interpretación | `figura_clave`, `nisar_flotante`, `clave_vs_muestra2025` | Tablas 11 a 14, Figura 13; `clave_muestra2025_*.csv` |
| 9. Mapa y corroboración óptica | `mapa_doble_rebote`, `mapa_doble_rebote_s1`, `mapa_doble_rebote_malaga`, `corroboracion_dw` | Tablas 15 y 16, Figuras 14 a 17; `mapa_doble_rebote_50m.tif`, `mapa_s1_alto_bajo_50m.tif`, `dw_serie.csv` |
| Informe y figuras de método | `md_a_word`, `figura_diseno`, `figura_flujo`, `figura_cadena_sar` | `Avance_proyecto_radar.docx`, Figuras 1, A1 y A2 |
