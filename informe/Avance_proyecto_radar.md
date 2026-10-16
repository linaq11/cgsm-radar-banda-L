Universidad Nacional de Colombia
Maestría en Geomática
Radar and LiDAR Remote Sensing, 2026-2
Lina María Quintero Fonseca
Respuesta de la banda L a la inundación bajo dosel de manglar: comparación con banda C en la Ciénaga Grande de Santa Marta y Bahía de Málaga

## Resumen

La inundación bajo el dosel del manglar es una condición del humedal que los radares de banda C registran mal, porque la onda apenas atraviesa un dosel denso. La banda L, con 23 cm de longitud de onda, penetra más en el dosel y puede registrar el doble rebote entre los troncos y la lámina de agua. Con el fin de establecer qué aporta esta banda, se compararon NISAR y ALOS-2 con Sentinel-1 en Bahía de Málaga, donde la inundación responde a la marea, y en la Ciénaga Grande de Santa Marta (CGSM), ligada al nivel del río Magdalena. La regla de lectura se fijó antes del análisis: si la banda L responde al agua bajo el dosel, la retrodispersión copolar del manglar debe aumentar con el forzante hidrológico sin una respuesta equivalente en el bosque de control. En Bahía de Málaga ese patrón se observó en las dos trayectorias de NISAR y en ALOS-2, con un aumento de 0,57 dB del manglar relativo al bosque en HH, mientras que Sentinel-1 y la polarización cruzada no respondieron. El resultado resiste la corrección por dependencia temporal. En la CGSM, la diferencia manglar menos bosque subió 0,83 dB entre río bajo y alto, pero los dos grupos pertenecen a versiones distintas del producto de NISAR y dentro de cada versión no hay relación con el nivel, de modo que el efecto no es identificable con las adquisiciones actuales. Una muestra propia de 720 puntos mostró mayor separabilidad entre manglar intacto y degradado en banda L que en C (0,78 frente a 0,26, todavía por debajo del umbral de 1), aunque ninguna banda separó el manglar degradado del humedal herbáceo. Finalmente, la cartografía a 50 m concentró el aumento de HH en el manglar del sur, en la desembocadura del río Fundación. Quedan pendientes el nivel del agua medido dentro del humedal y pasadas de NISAR de nivel alto y bajo dentro de una misma versión del producto.

Palabras clave: radar de apertura sintética, banda L, NISAR, manglar, inundación bajo dosel, doble rebote, Ciénaga Grande de Santa Marta, Bahía de Málaga.

## 1. Introducción

El producto de monitoreo global de inundaciones del Servicio de Gestión de Emergencias de Copernicus procesa Sentinel-1 en banda C, pero retira de la detección las superficies donde la interacción de las microondas con el terreno es compleja, entre ellas la vegetación densa (Expert Flood Monitoring Alliance, 2022, sección 4.4). En consecuencia, la inundación bajo el dosel del manglar cae por diseño fuera de lo que ese producto reporta. La banda L, con 23 cm de longitud de onda, penetra más en el dosel y puede registrar la interacción entre los troncos y la lámina de agua.

El doble rebote como mecanismo de retrodispersión en bosque inundado se conoce desde las primeras observaciones orbitales en banda L. Richards et al. (1987) atribuyeron el aumento de la retrodispersión copolar al doble rebote entre los troncos y la lámina de agua, y Hess et al. (1990) reunieron la evidencia de que ese realce se atenúa en longitudes de onda más cortas. Sobre manglar, Lucas et al. (2014) mostraron con ALOS PALSAR que la banda L aporta a la cartografía de su extensión y de sus cambios, línea de la que sale Global Mangrove Watch (Bunting et al., 2022). Sin embargo, esos trabajos no abordaron el seguimiento de la inundación bajo el dosel con un muestreo regular de pocos días.

NISAR, con doce días de repetición y un plan de adquisición sistemático (NASA ASF DAAC, 2026a, 2026b), ofrece ese muestreo. Su elección como sensor principal de banda L responde a esa frecuencia y a la continuidad temporal disponible sobre la CGSM. ALOS-2 aporta una referencia independiente en la misma banda y permite corroborar la respuesta observada en Bahía de Málaga, pero su cobertura sobre la ciénaga durante el periodo analizado se limita a diez pasadas, siete de ellas completas, insuficientes para evaluar la respuesta por trayectoria. NISAR, en cambio, permite relacionar la retrodispersión con los cambios del forzante hidrológico dentro de una misma geometría de adquisición. Por lo tanto, ALOS-2 se usa como corroboración independiente y no como sustituto de la serie temporal principal.

En la Ciénaga Grande de Santa Marta la hidrología es el problema central. La obstrucción de los caños que la conectan con el río Magdalena produjo la hipersalinización y la mortalidad masiva de manglar de los años ochenta y noventa, y la rehabilitación consistió en reabrir esa conexión (Botero y Salzwedel, 1999). Simard et al. (2008) cartografiaron en tres dimensiones el manglar de la ciénaga con SRTM, ICESat y datos de campo, y Jaramillo et al. (2018) evaluaron la conectividad hidrológica del humedal con observaciones interferométricas de radar. Ninguno de esos trabajos midió la respuesta temporal de la retrodispersión en banda L a la inundación bajo el dosel.

Con el fin de cubrir ese vacío, este avance compara NISAR y ALOS-2 en banda L con Sentinel-1 en banda C, con Bahía de Málaga como sitio mareal de contraste y la CGSM como sistema ligado al nivel del río Magdalena. La pregunta es qué información adicional aporta la banda L frente a Sentinel-1 para identificar condiciones de inundación bajo dosel de manglar en la CGSM. Para responderla se caracteriza la respuesta de retrodispersión de las coberturas representativas en las dos bandas, se compara esa respuesta en zonas de manglar con distintas condiciones de inundación y, finalmente, se interpretan las diferencias a partir de los mecanismos de dispersión de superficie, de volumen y de doble rebote.

## 2. Datos y métodos

### 2.1 Diseño y sitios de estudio

La CGSM se tomó como sitio principal y Bahía de Málaga (Buenaventura), en el Pacífico colombiano, como sitio de contraste. En la ciénaga la condición hidrológica se caracterizó con el nivel del río Magdalena y, en un primer paso, con la precipitación antecedente, y en Bahía de Málaga con la marea. Esa diferencia permite establecer si la respuesta de la banda L se mantiene bajo dos forzantes distintos.

Se analizaron cuatro coberturas: agua abierta, humedal herbáceo, manglar y un bosque de control que no se inunda. Se usaron NISAR y ALOS-2 en banda L y Sentinel-1 en banda C sobre periodos comparables, con 45 escenas de NISAR en total, 21 sobre la ciénaga y 24 sobre Bahía de Málaga (Tabla 1). La comparación se hizo dentro de cada trayectoria u órbita, por polarización, cobertura y condición hidrológica, con el ángulo de incidencia declarado. Posteriormente, la interpretación por cobertura se contrastó con una muestra de referencia propia de 2025, la distribución espacial de la señal se llevó a mapas a 50 m y Dynamic World sirvió de contraste óptico.

### 2.2 Datos SAR

Tabla 1. Inventario de adquisiciones SAR utilizadas en la CGSM y Bahía de Málaga, por sensor y trayectoria.

| Sitio | NISAR GCOV (HH, HV, 10 m) | ALOS-2 ScanSAR (HH, HV, 25 m) | Sentinel-1 GRD (VV, VH, 10 m), oct-2025 a sep-2026 |
|---|---|---|---|
| CGSM | 21 escenas, 14 descendentes (traza 083) y 7 ascendentes (traza 007), oct-2025 a sep-2026, sin cobertura entre feb y may de 2026 | serie 2025–2026 en Earth Engine, 10 pasadas, 7 completas | 119 pasadas con cobertura completa (58 en la órbita 77 y 61 en la 142) |
| Bahía de Málaga | 24 escenas que cubren completo el manglar: 12 ascendentes (traza 004, 05:46 local) y 12 descendentes (traza 087, 18:29 local), oct-2025 a sep-2026 | 72 escenas con HH y HV, ene-2025 a sep-2026, mosaicadas en 57 pasadas, 39 con cobertura completa | 89 pasadas con cobertura completa (26 en la órbita 48 y 63 en la 142) |

En todos los casos solo entran las pasadas que cubren la caja completa del sitio. En Bahía de Málaga las dos trazas de NISAR difieren en hora y en geometría, de modo que muestrean estados de marea distintos, y las comparaciones temporales se hacen dentro de cada traza. La misma separación por trayectoria u órbita se mantiene en los demás sensores. Sobre la ciénaga, las 21 escenas de NISAR son 14 de la traza descendente 083 (18:27 hora local) y siete de la ascendente 007 (05:31). Las seis de octubre de 2025 a enero de 2026 pertenecen a la colección Beta del producto y las quince de junio a septiembre de 2026 a la colección Provisional.

### 2.3 Procesamiento SAR y flujo de análisis

El procesamiento se hizo en Python y Google Earth Engine (Gorelick et al., 2017). Las escenas NISAR GCOV (NASA ASF DAAC, 2026a, 2026b) se localizaron en el catálogo CMR y se recortaron de forma remota con earthaccess y h5py. Sentinel-1 (Torres et al., 2012), ALOS-2 PALSAR-2 ScanSAR (JAXA EORC, s. f.), las coberturas globales, Sentinel-2 y ERA5-Land (Muñoz-Sabater et al., 2021) se procesaron desde la interfaz de Python de Earth Engine.

El preprocesamiento se definió por sensor. NISAR pasa de gamma cero con corrección de terreno a sigma cero con el factor que trae el producto y conserva su malla de ángulo de incidencia. ALOS-2 se calibra con la constante de JAXA (σ⁰ = 10·log10(DN²) − 83 dB) y se mosaica por pasada y trayectoria. Sentinel-1 GRD se usa con la eliminación de ruido térmico, la calibración radiométrica y la corrección de terreno que Earth Engine aplica al ingerirla, sin aplanamiento de terreno ni filtro de speckle (Google, s. f.).

La extracción se hace después del paso a decibelios, con un promedio espacial de 3 × 3 píxeles en NISAR y el píxel nativo en ALOS-2 y Sentinel-1. Cada pasada conserva traza, dirección, hora local e incidencia, y las trazas se analizan por separado porque la geometría sola desplaza el nivel hasta 1,4 dB en HH (Tabla 2). La Figura 1 resume el diseño analítico. El flujo completo en nueve etapas y la cadena por sensor, con la convención de los flujos de trabajo SAR de De Luca et al. (2021) y Yordanov y Brovelli (2021), están en el Anexo A.

![Figura 1. Flujo metodológico del estudio, desde los datos de entrada y el preprocesamiento SAR hasta las pruebas hidrológicas y los productos cartográficos.](fig_flujo_metodologico.png)

### 2.4 Coberturas de referencia y muestreo

Ante la ausencia de puntos interpretados y de estaciones de campo en Bahía de Málaga, las coberturas de referencia se definieron con WorldCover 2021 (Zanaga et al., 2022) y Global Mangrove Watch 2020 (Bunting et al., 2022). Agua, bosque y humedal herbáceo provienen de WorldCover, y el manglar se restringió a las áreas coincidentes entre los dos productos.

En Bahía de Málaga, Global Mangrove Watch cartografía 6.006 ha de manglar y WorldCover 7.576 ha, y los dos coinciden en 5.326 ha. Las zonas que solo identifica Global Mangrove Watch presentan una retrodispersión entre 0,9 y 2 dB menor y firmas próximas a las del humedal herbáceo, de modo que no se usaron como referencia de manglar. En la CGSM el consenso comprende 33.173 ha, y el bosque de control corresponde a bosque seco de las franjas oriental y meridional, fuera del plano inundable (Figura 2).

![Figura 2. Coberturas de referencia en la CGSM: (a) clases de WorldCover 2021; (b) coincidencia del manglar cartografiado por WorldCover 2021 y Global Mangrove Watch 2020.](fig_cgsm_referencia.png)

En los dos sitios se seleccionaron 400 puntos por clase con muestreo estratificado en Earth Engine (semilla 42), generados una sola vez y compartidos por los tres sensores. El bosque de control de la CGSM se muestreó sobre la caja ampliada del cubo (4.304 km²), puesto que el bosque seco de los piedemontes queda fuera del área de estudio de 2.042 km².

### 2.5 Forzantes hidrológicos

En Bahía de Málaga, la altura de marea de cada adquisición se obtuvo del pronóstico de la DIMAR para 2026 (Dirección General Marítima, s. f.), interpolado entre pleamares y bajamares y referido al nivel medio anual. Para las diez pasadas de octubre a diciembre de 2025 se usó una predicción armónica ajustada al mareógrafo histórico de Buenaventura (Caldwell et al., 2015). En 2026 las dos fuentes presentaron una correlación de Spearman de 0,95, un sesgo medio de 0,03 m y un error cuadrático medio de 0,24 m.

En la CGSM se usó primero la precipitación acumulada en los 30 días anteriores a cada adquisición, de ERA5-Land (Muñoz-Sabater et al., 2021), con las doce pasadas descendentes anteriores al 11 de septiembre de 2026, fecha hasta la que llega esa serie. Posteriormente se incorporó el nivel horario del río Magdalena en la estación automática Remolino del IDEAM (IDEAM, s. f.), interpolado a la hora de cada pasada, con el que entran las catorce pasadas descendentes y las siete ascendentes.

La respuesta SAR se evaluó con la diferencia manglar menos bosque, el contraste entre los estados alto y bajo del forzante y la correlación de Spearman. El nivel del río y la precipitación antecedente están asociados (ρ 0,70, p 0,01), de modo que las dos pruebas se interpretan como indicadores relacionados y no como evidencias independientes.

### 2.6 Regla de lectura y robustez

La regla se definió antes del análisis: si la banda L responde al agua bajo el dosel, dentro de una misma trayectoria se espera un aumento de la retrodispersión copolar del manglar y de HH − HV con el forzante hidrológico, sin una respuesta equivalente en el canal cruzado ni en el bosque no inundable.

Cada pasada se redujo a la mediana por clase y a la diferencia manglar menos bosque, que controla las variaciones temporales compartidas por las dos coberturas. En Bahía de Málaga se compararon las mitades superior e inferior de la distribución de marea, y en la CGSM los tercios superior e inferior del nivel del río. La robustez se evaluó frente al ángulo de incidencia, en tercios del rango angular, frente a la dependencia temporal y frente a la versión del producto de NISAR. El tamaño efectivo de muestra se estimó según Pyper y Peterman (1998), con los rezagos hasta n/5, y los valores p se recalcularon con él.

Como estadístico primario de cada sitio se declaró la resta copolar manglar menos bosque frente al forzante, por trayectoria, y la familia de pruebas primarias quedó formada por las cinco series de banda L: NISAR A004 y D087 y ALOS-2 139 y 140 en Bahía de Málaga, y NISAR D083 en la CGSM. Sobre los valores p corregidos por dependencia temporal se aplicó la corrección de Holm (1979). Además de la diferencia entre mitades o tercios, se estimó la pendiente de la resta frente al forzante en dB por metro de marea o de nivel, por mínimos cuadrados, con intervalo de confianza del 95 % por bootstrap de pasadas (5.000 réplicas) y con el estimador de Theil-Sen (Sen, 1968) como comprobación robusta. Las pruebas en banda C y la de la traza A007 se declaran exploratorias. Con el fin de separar el borde del interior del manglar, el cambio copolar entre periodos se resumió además por distancia del píxel de 50 m al borde del manglar y al agua abierta, calculada con la transformada de distancia sobre la máscara de referencia (`pendientes_auditoria.py`).

### 2.7 Clave de interpretación y evaluación con la muestra de referencia

La clave integra las firmas multifecha del canal copolar, del cruzado y de su diferencia en las dos bandas. Se evaluó con una muestra propia de 720 puntos, distribuida en seis clases: agua abierta, manglar intacto, vegetación flotante, manglar degradado, humedal herbáceo y otro.

La separabilidad entre pares de clases se cuantificó con la distancia de Jeffries-Matusita, derivada de la distancia de Bhattacharyya bajo supuesto gaussiano (Richards, 2013), con dos variables por banda, la copolar y la cruzada, y cuatro con las dos bandas juntas; la diferencia copolar menos cruzada no entra porque es combinación lineal de las otras dos y deja la covarianza singular. Los umbrales se definieron y se evaluaron sobre la misma muestra, de modo que el acierto corresponde a resustitución y no a una validación independiente.

Los puntos se sortearon fuera de una reserva de validación definida de antemano, con separación mínima de 200 m, y se etiquetaron a ciegas sobre imágenes de alta resolución de 2025, con revisión de los primeros 400 bajo un criterio escrito y marca de borde cuando la ventana de 3 × 3 píxeles mezcla clases (Figura 3).

![Figura 3. Muestra de referencia de 2025 en la CGSM: 720 puntos distribuidos en seis clases, reserva de validación y bloques de 12 km del diseño de validación espacial.](fig_muestra_2025.png)

### 2.8 Cartografía de la señal y contraste óptico

La señal se cartografió con diferencias píxel a píxel a 50 m en UTM 18N. En la CGSM se compararon las seis adquisiciones de NISAR D083 de nivel alto con las ocho de nivel bajo, grupos que coinciden con las colecciones Beta y Provisional, y Sentinel-1 usó las mismas ventanas de fechas con 13 y 18 pasadas de la órbita 142.

En Bahía de Málaga, cada trayectoria comparó las seis adquisiciones de mayor marea con las seis de menor marea. Como contraste óptico se usó la probabilidad de `flooded_vegetation` de Dynamic World V1 (Brown et al., 2022) en las fechas con al menos la mitad del manglar libre de nubes, con la mediana por píxel en las mismas ventanas de NISAR y al menos dos observaciones válidas por grupo. Dynamic World se interpreta como indicador de vegetación inundada visible desde el óptico y no como observación del agua bajo el dosel.

## 3. Resultados

### 3.1 Perfil de retrodispersión en Bahía de Málaga

Las cinco primeras adquisiciones de la traza A004 mostraron una señal estable dentro de cada cobertura. La variación de HH fue inferior a 1 dB en manglar, bosque y humedal herbáceo, y mayor en el agua abierta. El manglar identificado únicamente por Global Mangrove Watch fue cerca de 1,2 dB más oscuro en HH y 1,5 dB en HV que el manglar de consenso, y se aproximó al humedal herbáceo. Los valores de esas cinco adquisiciones se presentan en la Tabla B1.

Al considerar las 24 adquisiciones, el manglar mantuvo una variabilidad temporal baja dentro de cada trayectoria, con desviaciones estándar de 0,3 dB en HH para A004 y 0,4 dB para D087 (Tabla 2). Los niveles absolutos difieren entre trayectorias, con incidencia mediana de 42° en A004 y 35° en D087, y por eso se analizan por separado. En D087 el manglar quedó 0,6 dB por encima del bosque en HH y 1,1 dB en HH − HV, y en A004 fueron iguales en HH y 0,7 dB mayor en HH − HV.

Tabla 2. Mediana y desviación estándar de σ⁰ por cobertura y trayectoria en las 24 adquisiciones NISAR de Bahía de Málaga, en dB.

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

Entre las adquisiciones de noviembre a enero y las de junio a septiembre, HV aumentó entre 1 y 1,8 dB en todas las coberturas, incluida el agua. Como esa variación coincide con la transición entre las colecciones Beta y Provisional, no se atribuye solo a cambios estacionales. La Figura 4 muestra los compuestos de las dos trayectorias y la diferencia espacial de HH.

![Figura 4. Compuestos NISAR GCOV de Bahía de Málaga para las trayectorias A004 y D087 (R = HH, G = HV, B = HH − HV) y diferencia de HH entre las dos geometrías de adquisición.](fig_malaga_radar.png)

### 3.2 Marea y retrodispersión del manglar en banda L: NISAR

La señal HH del manglar relativa al bosque aumentó con la altura de marea tanto en A004 (ρ 0,83, p 0,001) como en D087 (ρ 0,74, p 0,006), con una diferencia de +0,57 dB entre marea alta y baja en las dos trayectorias (Tabla 3, Figura 5). HH − HV mostró el mismo sentido de respuesta, mientras que HV no presentó asociación con la marea.

Tabla 3. Relación entre la altura de marea y la retrodispersión de NISAR por trayectoria.

| Traza | Variable | Manglar: alta − baja (dB), ρ, p | Bosque: alta − baja (dB), ρ, p | Manglar − bosque: alta − baja (dB), ρ, p |
|---|---|---|---|---|
| A004 | HH | +0,28, 0,76, 0,004 | −0,11, −0,09, 0,78 | +0,57, 0,83, 0,001 |
| A004 | HV | −0,36, −0,11, 0,73 | −0,31, −0,13, 0,70 | +0,03, 0,11, 0,73 |
| A004 | HH−HV | +0,76, 0,53, 0,08 | +0,31, 0,20, 0,53 | +0,45, 0,83, 0,001 |
| D087 | HH | −0,02, 0,25, 0,44 | −0,49, −0,36, 0,25 | +0,57, 0,74, 0,006 |
| D087 | HV | −1,26, −0,41, 0,18 | −1,30, −0,50, 0,10 | +0,07, −0,06, 0,85 |
| D087 | HH−HV | +0,88, 0,76, 0,005 | +0,44, 0,13, 0,68 | +0,61, 0,60, 0,04 |

El bosque no presentó una respuesta equivalente. El patrón se concentró en el canal copolar y es compatible con un aumento de la contribución de doble rebote en el manglar inundado (Richards et al., 1987; Hess et al., 1990). Aunque el efecto fue pequeño, cercano a 0,6 dB, su repetición en dos trayectorias independientes permite distinguirlo de una diferencia de geometría.

![Figura 5. Retrodispersión del manglar y del bosque frente a la altura de marea asignada a cada adquisición de NISAR, por trayectoria.](fig_marea_vs_radar.png)

La estratificación por incidencia mantuvo el sentido de la respuesta: el HH relativo al bosque aumentó entre marea baja y alta en los seis terciles (+0,27 a +0,77 dB, ρ de 0,48 a 0,97) y con p menor que 0,05 en cinco de ellos, mientras que HV no respondió en ninguno (Figura 6). El rango angular disponible, de 42° a 43° en A004 y de 34° a 37° en D087, permite comprobar que la señal no cambia de signo con la geometría local, pero no estimar su dependencia con el ángulo.

![Figura 6. Respuesta del manglar relativa al bosque por tercil de ángulo de incidencia en las trayectorias A004 y D087 de NISAR.](fig_doble_rebote_incidencia.png)

### 3.3 Comparación con Sentinel-1 en banda C

La misma prueba se aplicó a las 89 adquisiciones de Sentinel-1 con cobertura completa, 26 de la órbita ascendente 48 y 63 de la descendente 142. La señal del manglar relativa al bosque no mostró relación con la marea en VV, VH ni VV − VH en ninguna órbita (Tabla 4, Figura 7).

Tabla 4. Relación entre la altura de marea y la retrodispersión del manglar relativa al bosque en Sentinel-1.

| Órbita (hora local, n) | VV | VH | VV−VH |
|---|---|---|---|
| 48 ascendente (18:21, 26) | −0,07 dB, ρ −0,18, p 0,37 | −0,11 dB, ρ −0,30, p 0,14 | +0,16 dB, ρ 0,23, p 0,26 |
| 142 descendente (05:50, 63) | −0,07 dB, ρ −0,13, p 0,32 | 0,00 dB, ρ −0,08, p 0,55 | −0,15 dB, ρ −0,15, p 0,24 |

Aunque el manglar aislado presentó una correlación negativa en VV de la órbita 142 (ρ −0,39, p 0,002), esa asociación desapareció al descontar el bosque y tuvo signo contrario al observado en HH de banda L. La comparación no separa del todo longitud de onda y polarización, puesto que Sentinel-1 observa VV y NISAR HH.

![Figura 7. Retrodispersión de Sentinel-1 del manglar y del bosque frente a la altura de marea, por órbita relativa.](fig_s1_marea.png)

### 3.4 Corroboración con ALOS-2 en banda L

Se analizaron 72 escenas de ALOS-2 PALSAR-2 ScanSAR entre enero de 2025 y septiembre de 2026, agrupadas en 57 pasadas, de las cuales 39 cubrieron el área completa. El análisis se concentró en las trayectorias descendentes 139 (21 pasadas) y 140 (15 pasadas), ambas de mediodía.

ALOS-2 reprodujo el patrón de NISAR (Tabla 5, Figura 8). La señal HH del manglar relativa al bosque aumentó con la marea en las dos trayectorias, con ρ 0,65 (p 0,002) y ρ 0,72 (p 0,002). HH − HV presentó igualmente asociaciones positivas, mientras que HV no mostró la misma respuesta. En el path 139 el HV bajó con la marea en manglar y bosque (ρ −0,66 y −0,62), una variación compartida ligada a la estación en pasadas de mediodía que la resta elimina.

Tabla 5. Relación entre la altura de marea y la retrodispersión del manglar relativa al bosque en ALOS-2 PALSAR-2.

| Path (hora local, n) | HH | HV | HH−HV |
|---|---|---|---|
| 139 descendente (11:53, 21) | +0,25 dB, ρ 0,65, p 0,002 | +0,06 dB, ρ 0,05, p 0,81 | +0,13 dB, ρ 0,47, p 0,03 |
| 140 descendente (12:00, 15) | +0,49 dB, ρ 0,72, p 0,002 | −0,16 dB, ρ −0,45, p 0,10 | +0,91 dB, ρ 0,79, p < 0,001 |

En conjunto, NISAR (ρ 0,83 y 0,74) y ALOS-2 (ρ 0,65 y 0,72) mostraron una asociación positiva en el canal copolar de banda L, ausente en Sentinel-1 (ρ −0,18 y −0,13).

![Figura 8. Retrodispersión de ALOS-2 PALSAR-2 del manglar y del bosque frente a la altura de marea, por trayectoria.](fig_alos2_marea.png)

### 3.5 La Ciénaga Grande: lluvia como forzante

Una comparación entre dos adquisiciones Beta de NISAR mostró que HH aumentó una mediana de +0,43 dB sobre el manglar entre una fecha con el Magdalena a 1,69 m y otra a 2,67 m, con el 50 % central entre −0,42 y +1,28 dB (Figura 9). La señal negativa sobre la laguna corresponde a la rugosidad del agua abierta por el viento y no a inundación.

![Figura 9. NISAR GCOV sobre la CGSM, traza D083: (a) 4 de diciembre de 2025, nivel del Magdalena de 2,67 m; (b) 9 de enero de 2026, 1,69 m; (c) diferencia de HH entre las dos fechas.](fig_cgsm_radar.png)

Los compuestos de Sentinel-2 de esas fechas (Drusch et al., 2012), enmascarados con Cloud Score+ (Pasquarella et al., 2023), no mostraron un cambio equivalente en superficie: el NDVI mediano del manglar fue de 0,855 y 0,867 y el agua abierta ocupó el 39,7 % y el 39,2 % del área válida (Figura 10). El óptico distingue las coberturas principales, pero no registra el agua bajo un dosel cerrado.

![Figura 10. Comparación de Sentinel-2 y NISAR sobre la CGSM para las dos fechas de la Figura 9. Sentinel-2 se presenta en color natural e infrarrojo color y NISAR como compuesto de HH, HV y HH − HV.](fig_cgsm_optico_radar.png)

La precipitación antecedente produjo respuestas distintas en las dos bandas (Tablas B2 y B3, Figura 11). En Sentinel-1, el bosque seco respondió a la lluvia con mayor intensidad que el manglar (ρ 0,52 y 0,58 frente a 0,32 y 0,21 en VV), de modo que la diferencia manglar menos bosque fue negativa. En NISAR D083, el HH del bosque no respondió (ρ 0,02), el manglar mostró ρ 0,50 y la diferencia manglar menos bosque alcanzó ρ 0,58 (p 0,05), sin asociación equivalente en la cruzada. La partición por calendario entre época húmeda y seca dio el signo contrario porque en este periodo las pasadas de época seca tuvieron más lluvia antecedente que las de época húmeda.

Sin embargo, esa asociación deja de distinguirse del azar al corregir la dependencia temporal (sección 3.7), y la lluvia es solo un sustituto indirecto del nivel del agua. Por ello se interpreta como una dirección y no como prueba del efecto hidrológico.

![Figura 11. Retrodispersión del manglar y del bosque frente a la precipitación acumulada durante los 30 días anteriores a cada adquisición, por sensor y trayectoria.](fig_cgsm_temporada.png)

### 3.6 La Ciénaga Grande: nivel del río Magdalena

El nivel del Magdalena en Remolino produjo una asociación más marcada con NISAR D083 (Tabla 6, Figura 12). Entre los tercios de nivel bajo y alto, HH aumentó +0,47 dB en el manglar y disminuyó −0,53 dB en el bosque, y la diferencia manglar menos bosque aumentó +0,83 dB, con ρ 0,83 (p < 0,001). La cruzada relativa al bosque no mostró una relación equivalente.

Tabla 6. Relación entre el nivel del río Magdalena en Remolino y la retrodispersión, por sensor y trayectoria. En Sentinel-1 entran 55 y 58 pasadas, porque tres por órbita caen en un hueco de 18 días de la serie del IDEAM en agosto de 2026.

| Sensor y pasada | n | Clase | Copolar (HH o VV) | Cruzada (HV o VH) | Cociente (HH−HV) |
|---|---|---|---|---|---|
| NISAR D083 (18:27) | 14 | Manglar | +0,47 dB · ρ 0,58, p 0,03 | −0,97 dB · ρ −0,74, p 0,003 | +1,27 dB · ρ 0,77, p 0,001 |
| NISAR D083 (18:27) | 14 | Bosque | −0,53 dB · ρ −0,39, p 0,16 | −1,29 dB · ρ −0,70, p 0,006 | +0,71 dB · ρ 0,71, p 0,005 |
| NISAR D083 (18:27) | 14 | Manglar − bosque | +0,83 dB · ρ 0,83, p < 0,001 | +0,35 dB · ρ 0,32, p 0,27 | +0,62 dB · ρ 0,49, p 0,08 |
| NISAR A007 (05:31) | 7 | Manglar − bosque | −0,14 dB · ρ −0,04, p 0,94 | −0,06 dB · ρ −0,39, p 0,38 | −0,30 dB · ρ −0,54, p 0,22 |
| Sentinel-1 A77 (18:06) | 55 | Manglar − bosque | −0,21 dB · ρ −0,47, p < 0,001 | +0,05 dB · ρ −0,01, p 0,95 | −0,08 dB · ρ −0,12, p 0,37 |
| Sentinel-1 D142 (05:48) | 58 | Manglar − bosque | −0,21 dB · ρ −0,33, p 0,01 | −0,14 dB · ρ −0,37, p 0,005 | −0,15 dB · ρ −0,18, p 0,18 |

La traza A007 no mostró asociación, pero sus siete adquisiciones corresponden a niveles bajos o intermedios, entre 0,82 y 1,58 m. Sentinel-1 presentó el comportamiento contrario, con el copolar relativo al bosque en descenso con el nivel, porque el VV del bosque sube con el nivel (ρ 0,39 y 0,32) y el del manglar no.

Sin embargo, las seis adquisiciones de nivel alto, entre 1,69 y 2,67 m, pertenecen a la colección Beta y las ocho de nivel bajo, entre 0,91 y 1,42 m, a la Provisional, porque en 2026 el río bajó mucho más que en 2025 para los mismos meses. Dentro de cada versión no hay asociación entre el nivel y el HH relativo al bosque: ρ −0,14 (p 0,79) en las seis Beta y ρ 0,55 (p 0,16) en las ocho Provisionales. Una regresión conjunta atribuye 0,12 dB por metro al nivel y −0,52 dB al cambio de versión. Por lo tanto, el ρ de 0,83 lo produce el escalón entre los dos bloques, y con la serie actual no es posible identificar el efecto hidrológico por separado. El HV, además, baja en las dos clases con el nivel (ρ −0,74 y −0,70), lo que puede ser estacional o de versión.

![Figura 12. Retrodispersión del manglar y del bosque frente al nivel horario del río Magdalena en Remolino, por sensor y trayectoria.](fig_cgsm_nivel_rio.png)

### 3.7 Dependencia temporal de las correlaciones

Tabla 7. Correlación entre la señal copolar manglar menos bosque y el forzante hidrológico, antes y después de corregir la dependencia temporal. La pendiente es la de la resta frente al forzante, en dB por metro de marea o de nivel, con intervalo bootstrap del 95 %; el p de Holm corrige el p corregido sobre la familia de cinco pruebas primarias de banda L.

| Serie | Traza | n | ρ | p | r1 del forzante | r1 del radar | n efectivo | p corregido | Pendiente (dB/m) [IC 95 %] | p de Holm |
|---|---|---|---|---|---|---|---|---|---|---|
| NISAR, Málaga, marea | A004 | 12 | 0,83 | 0,001 | 0,15 | −0,21 | 8,7 | 0,007 | 0,23 [0,15 a 0,38] | 0,033 |
| NISAR, Málaga, marea | D087 | 12 | 0,74 | 0,006 | −0,03 | −0,24 | 11,2 | 0,008 | 0,35 [0,20 a 0,52] | 0,033 |
| ALOS-2, Málaga, marea | 139 | 21 | 0,65 | 0,002 | 0,60 | 0,29 | 11,1 | 0,031 | 0,12 [0,05 a 0,18] | 0,063 |
| ALOS-2, Málaga, marea | 140 | 15 | 0,72 | 0,002 | 0,53 | 0,48 | 9,8 | 0,019 | 0,24 [0,09 a 0,57] | 0,057 |
| Sentinel-1, Málaga, marea | 48 | 26 | −0,18 | 0,37 | 0,23 | −0,25 | 26 | 0,37 | −0,07 [−0,19 a 0,05] | exploratoria |
| Sentinel-1, Málaga, marea | 142 | 63 | −0,13 | 0,32 | −0,65 | 0,03 | 63 | 0,32 | −0,05 [−0,11 a 0,01] | exploratoria |
| NISAR, CGSM, lluvia de 30 días | D083 | 12 | 0,58 | 0,048 | 0,45 | 0,69 | 5,7 | 0,25 | — | exploratoria |
| Sentinel-1, CGSM, lluvia de 30 días | A77 | 58 | −0,35 | 0,008 | 0,89 | 0,14 | 21,1 | 0,12 | — | exploratoria |
| Sentinel-1, CGSM, lluvia de 30 días | D142 | 61 | −0,52 | < 0,001 | 0,89 | 0,32 | 24,7 | 0,009 | — | exploratoria |
| NISAR, CGSM, nivel del río | D083 | 14 | 0,83 | < 0,001 | 0,86 | 0,64 | 4,7 | 0,10 | 0,49 [0,34 a 0,71] | 0,104 |

La corrección mantuvo las asociaciones de NISAR con la marea en A004 (p corregido 0,007) y D087 (0,008), porque un muestreo cada doce días cae en fases distintas del ciclo mareal, y las de ALOS-2 en las trayectorias 139 (0,031) y 140 (0,019), cuyo muestreo cada 28 días se acerca al ciclo de mareas vivas y muertas y reduce el tamaño efectivo a unas diez pasadas. Sentinel-1 permaneció sin asociación. La versión del producto tampoco explica el resultado de Málaga: dentro de cada bloque Beta o Provisional la resta sigue subiendo con la marea, con ρ de 0,89 y 0,90 en A004 y de 0,66 y 0,77 en D087.

En la CGSM, la relación de NISAR con la precipitación pasó de p 0,048 a p 0,25, porque la lluvia acumulada de treinta días es una serie muy suave. Para el nivel del río, los dos bloques de fechas redujeron el tamaño efectivo de 14 a 4,7 observaciones y elevaron el valor p a 0,10. En consecuencia, la evidencia robusta procede de Bahía de Málaga, y en la CGSM la señal es coherente en dirección pero no identificable frente a la estructura temporal y la versión del producto.

Con la corrección de Holm sobre las cinco pruebas primarias de banda L, las dos trayectorias de NISAR en Bahía de Málaga se mantuvieron (p 0,033), ALOS-2 quedó en el límite (0,063 y 0,057) y la CGSM no pasó (0,104); si la familia se restringe a las cuatro pruebas de Málaga, las cuatro pasan (0,026 a 0,038). Las pendientes expresan el efecto en unidades comparables entre sitios: 0,23 dB/m en A004 y 0,35 dB/m en D087 con NISAR, y 0,12 y 0,24 dB/m con ALOS-2, con intervalos que excluyen el cero, frente a −0,07 y −0,05 dB/m en Sentinel-1, con intervalos que lo incluyen. Sobre el rango de marea observado, de 2,3 a 3,4 m, el cambio esperado de la resta es de 0,4 a 0,8 dB. En la CGSM la pendiente de NISAR D083 fue de 0,49 dB/m [0,34 a 0,71], pero contiene el escalón de versión, y la de Sentinel-1 fue negativa, −0,23 y −0,25 dB/m.

### 3.8 Clave de interpretación por cobertura y mecanismo

Las firmas iniciales obtenidas con las coberturas de los productos globales se presentan en la Tabla B4 y en la Figura 13. En banda C, el manglar y el humedal herbáceo presentan firmas casi coincidentes, y en banda L sus medianas se separan en HH y HH − HV, mientras que la vegetación flotante permanece más próxima al agua abierta en banda L.

![Figura 13. Espacio de firmas de las coberturas de la CGSM en bandas C y L, definido por la retrodispersión copolar y la diferencia copolar menos cruzada.](fig_clave_firmas.png)

#### Evaluación con la muestra de referencia de 2025

La muestra propia modificó parte de esa interpretación (Tabla 8). La mayor mejora de la banda L se observó entre manglar intacto y degradado, cuya separabilidad aumentó de 0,26 en banda C a 0,78 en banda L, todavía por debajo del umbral de 1 (Tabla 9). En cambio, humedal herbáceo y manglar degradado permanecieron prácticamente inseparables, con 0,11 en C, 0,16 en L y 0,24 con las dos bandas, lo mismo que ocurre con el NDVI de Sentinel-2 (0,44). La vegetación flotante tampoco presentó una firma radar separable del agua (0,19 en L y 0,47 en C).

Tabla 8. Firmas multifecha de las clases de la muestra de referencia de 2025 en bandas C y L, en dB.

| Clase | n | VV | VH | VV − VH | HH | HV | HH − HV | HH − HV, cuartiles |
|---|---|---|---|---|---|---|---|---|
| Agua | 212 | −21,5 | −29,6 | 7,5 | −19,9 | −25,4 | 5,9 | 5,0 a 6,5 |
| Vegetación flotante | 129 | −15,2 | −22,7 | 6,7 | −17,0 | −23,7 | 6,8 | 5,6 a 7,8 |
| Manglar intacto | 151 | −9,5 | −14,8 | 5,5 | −10,0 | −16,7 | 6,6 | 6,0 a 7,4 |
| Manglar degradado | 111 | −10,7 | −15,9 | 5,3 | −8,3 | −16,8 | 8,9 | 7,5 a 10,7 |
| Humedal herbáceo | 73 | −10,4 | −15,9 | 5,4 | −9,6 | −17,3 | 7,9 | 7,3 a 8,6 |
| Otro | 44 | −10,1 | −15,4 | 6,0 | −10,7 | −18,3 | 7,5 | 6,6 a 8,6 |

La diferencia HH − HV ordenó las coberturas según la apertura del dosel: 6,6 dB en manglar intacto, 7,5 dB en la clase otro, 7,9 dB en humedal herbáceo y 8,9 dB en manglar degradado. Esta variable caracteriza estructura, pero no identifica por sí sola una clase.

Tabla 9. Separabilidad de Jeffries-Matusita entre las clases de la muestra de referencia de 2025, con la copolar y la cruzada de cada banda (dos variables por banda y cuatro con las dos bandas).

| Par | Banda C | Banda L | C + L |
|---|---|---|---|
| Agua, vegetación flotante | 0,47 | 0,19 | 0,60 |
| Agua, humedal herbáceo | 1,38 | 1,21 | 1,55 |
| Agua, manglar degradado | 1,60 | 1,53 | 1,78 |
| Agua, manglar intacto | 1,81 | 1,86 | 1,95 |
| Agua, otro | 1,43 | 1,19 | 1,60 |
| Vegetación flotante, humedal herbáceo | 0,53 | 0,62 | 0,81 |
| Vegetación flotante, manglar degradado | 0,82 | 0,91 | 1,19 |
| Vegetación flotante, manglar intacto | 1,20 | 1,47 | 1,65 |
| Vegetación flotante, otro | 0,50 | 0,67 | 0,85 |
| Humedal herbáceo, manglar degradado | 0,11 | 0,16 | 0,24 |
| Humedal herbáceo, manglar intacto | 0,43 | 0,61 | 0,82 |
| Humedal herbáceo, otro | 0,07 | 0,11 | 0,23 |
| Manglar degradado, manglar intacto | 0,26 | 0,78 | 0,87 |
| Manglar degradado, otro | 0,23 | 0,43 | 0,58 |
| Manglar intacto, otro | 0,51 | 0,43 | 0,73 |

#### Regla de lectura

La clave se redujo a cuatro decisiones sobre las medianas multifecha:

1. Agua abierta: VV por debajo de −17 dB y VH por debajo de −25 dB en σ⁰ (−16,2 y −24,2 dB en γ⁰).
2. Superficie oscura con vegetación o borde: VV por debajo de −12 dB en σ⁰ (−11,2 dB en γ⁰) sin cumplir la condición anterior, compatible con vegetación flotante cuando VV − VH es de 6,5 dB o más.
3. Dosel cerrado: VV de −12 dB o más en σ⁰ (−11,2 dB en γ⁰) y HH − HV por debajo de 7,3 dB.
4. Dosel abierto o herbáceo: VV de −12 dB o más en σ⁰ (−11,2 dB en γ⁰) y HH − HV de 7,3 dB o más, grupo donde quedan juntos el manglar degradado, el humedal herbáceo y parte de la clase otro.

La respuesta hidrológica complementa la firma estática para distinguir el manglar del bosque no inundable, puesto que la diferencia de nivel entre las dos clases (1,5 dB en VV y 1,7 dB en HH) es del orden de la que produce la geometría entre trayectorias. El criterio es el cambio del canal copolar con el forzante, observado en Bahía de Málaga y, con la confusión de versión declarada, en la CGSM.

La regla decidió 606 de los 720 puntos y acertó en 415, el 68 % de los casos decididos y el 58 % de la muestra (Tabla 10). Sin los 208 puntos de borde, decidió 444 de 512 y acertó en el 71 %. Estas cifras corresponden a resustitución.

Con el fin de medir lo que aporta la banda L a la clave, la decisión entre dosel cerrado y abierto se repitió con la banda C sola, con VV − VH en lugar de HH − HV y el umbral elegido por el mismo procedimiento de resustitución, el acierto balanceado entre manglar intacto y las tres clases de dosel abierto. El mejor umbral en C, VV − VH por debajo de 7,0 dB, alcanzó un acierto balanceado de 0,54, apenas por encima del azar, frente a 0,75 con HH − HV, cuyo umbral óptimo, 7,4 dB, coincide con el 7,3 dB fijado. Con la clave en C sola se decidieron los mismos 606 puntos, pero se acertó en 340, el 56 % de los decididos y el 47 % de la muestra, en vez de 415: 78 de los 111 puntos de manglar degradado y 44 de los 73 de humedal herbáceo pasaron a dosel cerrado. Por lo tanto, la separación entre dosel cerrado y abierto depende de la banda L.

Tabla 10. Clasificación de los 720 puntos de referencia con la clave de interpretación SAR (filas, clase de referencia; columnas, decisiones 1 a 4 de la regla). Umbrales en σ⁰; con los umbrales equivalentes en γ⁰ (desplazados +0,83 dB, la mediana de γ⁰ − σ⁰ en banda C) la tabla es idéntica salvo dos celdas: manglar degradado 63 y otro 19 en la decisión 4, con los mismos 606 puntos decididos y 415 aciertos.

| Clase de referencia | 1 Agua abierta | 2 Vegetación flotante | 3 Manglar intacto | 4 Dosel abierto o herbáceo | Sin decisión |
|---|---|---|---|---|---|
| Agua | **159** | 7 | 5 | 5 | 36 |
| Vegetación flotante | 42 | **27** | 14 | 25 | 21 |
| Manglar intacto | 0 | 0 | **107** | 32 | 12 |
| Manglar degradado | 2 | 4 | 19 | **62** | 24 |
| Humedal herbáceo | 3 | 2 | 11 | **40** | 17 |
| Otro | 2 | 3 | 15 | **20** | 4 |

### 3.9 Distribución espacial de la señal y contraste óptico

En la CGSM, la diferencia entre las seis adquisiciones de nivel alto y las ocho de nivel bajo mostró una estructura espacial marcada (Tabla 11, Figura 14). El manglar completo presentó una mediana de +0,07 dB en HH, pero el sector sur subió +0,53 dB con el 77 % de los píxeles positivos. En Isla de Salamanca, al norte, donde entra el caño Clarín, la mediana fue de −0,18 dB, y el bosque seco de control disminuyó −0,36 dB.

Tabla 11. Cambio de retrodispersión entre los periodos de nivel alto y bajo del río, por cobertura y sector del manglar, en dB.

| Clase o sector | Píxeles | ΔHH (L) | ΔHH > 0 | ΔHV (L) | Δ(HH − HV) | ΔVV (C) | ΔVV > 0 | ΔVH (C) |
|---|---|---|---|---|---|---|---|---|
| Manglar, todo | 145.398 | +0,07 (−0,47 a +0,63) | 53 % | −1,13 | +1,21 | +0,09 (−0,15 a +0,33) | 61 % | +0,01 |
| Manglar norte, Isla de Salamanca (N > 1205 km) | 69.063 | −0,18 (−0,64 a +0,30) | 40 % | −1,08 | +0,93 | +0,05 (−0,17 a +0,30) | 56 % | −0,02 |
| Manglar centro y occidente (1190 a 1205 km) | 33.412 | +0,02 (−0,52 a +0,57) | 51 % | −1,23 | +1,25 | +0,02 (−0,22 a +0,24) | 53 % | +0,01 |
| Manglar sur, desembocadura del río Fundación (N < 1190 km) | 42.923 | **+0,53 (+0,05 a +0,99)** | **77 %** | −1,15 | +1,66 | +0,21 (−0,01 a +0,39) | 74 % | +0,06 |
| Bosque seco (control) | 316.807 | −0,36 (−0,89 a +0,21) | 33 % | −1,18 | +0,84 | **+0,36 (+0,13 a +0,63)** | **86 %** | +0,21 |
| Humedal herbáceo | 207.215 | +0,46 (−0,54 a +1,82) | 62 % | −0,96 | +1,41 | +0,26 (−0,22 a +0,80) | 65 % | +0,31 |
| Agua abierta | 663.486 | −0,39 (−0,89 a +0,02) | 26 % | −1,21 | +0,73 | −0,47 (−1,08 a 0,00) | 25 % | +0,62 |

El cambio no se concentró en el borde del manglar (Tabla 12, Figura B1). En el sector sur, la mediana de ΔHH creció con la distancia al borde, de +0,31 dB en los primeros 50 m a +0,74 dB a más de 300 m, y la fracción de píxeles positivos pasó de 64 % a 91 %, con una correlación de Spearman de 0,21 entre distancia y cambio. En Isla de Salamanca el cambio fue negativo a todas las distancias, entre −0,13 y −0,26 dB. Los píxeles de manglar a menos de 50 m del agua abierta cambiaron como el agua, −0,39 dB, lo que indica mezcla de superficies en la celda de 50 m. En Bahía de Málaga el cambio de HH del manglar con la marea fue igual de borde a interior, entre +0,27 y +0,40 dB en A004 y entre +0,02 y +0,13 dB en D087 en todas las bandas de distancia. Por lo tanto, la señal copolar asociada al forzante procede del interior del rodal y no de sus bordes, lo que es compatible con el doble rebote bajo el dosel y no con un efecto de borde ni con la mezcla con agua abierta, que actuó en sentido contrario.

Tabla 12. Cambio de HH del manglar entre los periodos de nivel alto y bajo del río (CGSM, NISAR D083) y entre marea alta y baja (Bahía de Málaga) según la distancia del píxel de 50 m al borde del manglar: mediana en dB y fracción de píxeles con cambio positivo.

| Sitio y sector | 0 a 50 m | 50 a 100 m | 100 a 200 m | 200 a 300 m | Más de 300 m |
|---|---|---|---|---|---|
| Manglar de la CGSM, todo | −0,07 (47 %) | +0,03 (52 %) | +0,08 (54 %) | +0,12 (57 %) | +0,34 (67 %) |
| Manglar sur, río Fundación | +0,31 (64 %) | +0,46 (74 %) | +0,54 (79 %) | +0,58 (83 %) | +0,74 (91 %) |
| Manglar centro y occidente | −0,11 (45 %) | +0,01 (51 %) | +0,10 (55 %) | +0,22 (62 %) | +0,04 (53 %) |
| Manglar norte, Isla de Salamanca | −0,26 (38 %) | −0,16 (40 %) | −0,13 (42 %) | −0,16 (40 %) | −0,20 (37 %) |
| Bahía de Málaga, A004, marea | +0,28 (71 %) | +0,39 (77 %) | +0,40 (79 %) | +0,39 (79 %) | +0,27 (71 %) |
| Bahía de Málaga, D087, marea | +0,02 (51 %) | +0,07 (55 %) | +0,06 (55 %) | +0,07 (55 %) | +0,13 (61 %) |

![Figura 14. Cambio de HH, HV y HH − HV de NISAR D083 entre los periodos de nivel alto y bajo del río, sobre una malla de 50 m.](fig_mapa_doble_rebote.png)

El máximo aumento se localizó en la desembocadura del río Fundación, que baja de la Sierra Nevada, y no en las entradas de los caños del Magdalena: cruzado con los cauces de OpenStreetMap, el foco queda a 1,3 km del Fundación, mientras que el caño Renegado termina al occidente, a 11 km del manglar, en una franja de cambio menor. Por lo tanto, el nivel de Remolino funciona en ese sector como indicador regional de la condición hidrológica y no como forzante directo. El humedal herbáceo también subió (+0,46 dB), lo que indica que el canal copolar responde igualmente al agua o suelo expuesto fuera del dosel. Los sectores se trazaron por latitud antes de verificar la hidrografía, de modo que la lectura por sector es una hipótesis para la serie siguiente.

HV disminuyó cerca de 1 dB en todas las coberturas, incluida el agua abierta, de modo que esa señal no se atribuye a inundación bajo dosel y puede reflejar la versión del producto o la estación. La comparación espacial con Sentinel-1 mostró un patrón distinto (Figura 15): en banda C el bosque seco subió más que el manglar (+0,36 frente a +0,09 dB), mientras que en L el manglar subió y el bosque bajó, y la correlación por píxel entre ΔHH y ΔVV sobre el manglar fue débil (ρ 0,21).

![Figura 15. Cambio copolar entre los mismos periodos en NISAR (HH) y Sentinel-1 (VV), sobre una malla común de 50 m.](fig_mapa_c_vs_l.png)

#### Contraste con Dynamic World

Dynamic World mostró relación con el nivel del río en el humedal herbáceo (ρ 0,41, p 0,002, sin corregir por dependencia temporal), pero no en el manglar (ρ 0,04) ni en el bosque (ρ −0,02). La correlación espacial entre el cambio de `flooded_vegetation` y el ΔHH sobre el manglar fue débil y negativa (ρ −0,15): donde el óptico ve más agua expuesta el HH baja, y donde no ve cambio el HH sube (Figura 16). El patrón es compatible con una diferencia entre agua expuesta y agua bajo el dosel, pero no constituye una validación independiente del doble rebote.

![Figura 16. Contraste entre el nivel del río, la probabilidad de vegetación inundada de Dynamic World y el cambio de HH de NISAR.](fig_corroboracion_dw.png)

#### Distribución espacial en Bahía de Málaga

La misma comparación se repitió con las seis adquisiciones de mayor y de menor marea de cada trayectoria (Tabla B5, Figura 17). En A004, el HH subió +0,34 dB en el manglar y bajó −0,10 dB en el bosque, y en D087 los cambios fueron +0,05 y −0,39 dB. La caída del bosque en D087 coincide con la versión del producto, con cuatro pasadas Beta en el grupo de marea alta y cuatro Provisionales en el de marea baja, de modo que la resta cancela ese desplazamiento. La diferencia manglar menos bosque fue de +0,44 dB en las dos trayectorias, próxima a los +0,57 dB del muestreo por puntos. La señal positiva se distribuyó a lo largo de las franjas de manglar de la bahía, y HV bajó en todas las coberturas, por lo que no se usó como firma independiente.

![Figura 17. Cambio de HH y HV entre las seis pasadas de mayor y menor marea de cada trayectoria de NISAR en Bahía de Málaga, sobre una malla de 50 m.](fig_mapa_doble_rebote_malaga.png)

## 4. Discusión

La evidencia más sólida del estudio procede de Bahía de Málaga. El HH del manglar relativo al bosque aumentó con la marea en las dos trayectorias de NISAR y el mismo patrón se reprodujo con ALOS-2, mientras que Sentinel-1 no mostró una respuesta equivalente. Las asociaciones de los dos sensores de banda L permanecieron después de corregir la dependencia temporal y, en NISAR, dentro de cada versión del producto. En la CGSM se observó la misma dirección frente al nivel del río, pero los estados alto y bajo coinciden con las colecciones Beta y Provisional y los dos efectos no pueden separarse con la serie disponible.

El cambio copolar relativo al bosque fue pequeño, de 0,4 a 0,8 dB, frente a los realces de varios decibelios descritos para otros bosques inundados en banda L (Hess et al., 1990). Esa diferencia puede estar relacionada con la atenuación de un dosel de manglar denso, con la presencia parcial de agua dentro del píxel y con la variabilidad hidrológica entre adquisiciones. Además, la polarización dual impide separar los mecanismos con observables polarimétricos completos, y la comparación entre bandas tampoco separa del todo longitud de onda y polarización, puesto que NISAR y ALOS-2 observan HH y Sentinel-1 VV. Los resultados son compatibles con una contribución de doble rebote, pero no constituyen una identificación polarimétrica directa. Sin embargo, la reproducción del patrón en dos sensores de banda L y su ausencia en HV y en Sentinel-1 reduce la probabilidad de que la respuesta sea exclusiva de una geometría o de un sensor.

La banda L también aportó información estructural. La separabilidad entre manglar intacto y degradado aumentó de 0,26 en banda C a 0,78 en banda L, y HH − HV respondió sobre todo a la apertura del dosel, de modo que caracteriza estructura pero no sirve como etiqueta única de cobertura. Con la banda C sola, la decisión entre dosel cerrado y abierto quedó en el nivel del azar, con un acierto balanceado de 0,54 frente a 0,75 con HH − HV, de modo que esa parte de la clave depende de la banda L. La frontera entre manglar degradado y humedal herbáceo permaneció sin resolver con las dos bandas.

Finalmente, la distribución espacial mostró que la respuesta no es homogénea. El mayor aumento de HH se concentró en el manglar del sur de la CGSM, en la desembocadura del río Fundación, lo que indica que el nivel del Magdalena en Remolino actúa como indicador regional y no como forzante directo de cada sector, mientras que Sentinel-1 presentó un patrón más difuso y una respuesta mayor en el bosque seco. Dentro del manglar, el cambio creció con la distancia al borde del rodal en el sector sur y fue igual de borde a interior en Bahía de Málaga, de modo que la señal no se explica por un efecto de borde ni por la mezcla con agua abierta en el píxel, que actuó en sentido contrario. Dynamic World respondió al nivel del río donde el agua era visible desde el óptico, pero no bajo el manglar, de modo que aporta evidencia sobre el forzante y no una validación directa de la señal bajo el dosel.

### 4.1 Limitaciones

El estudio presenta cuatro limitaciones. En primer lugar, los datos son de polarización dual, HH y HV en banda L y VV y VH en banda C, de modo que la comparación combina longitud de onda y polarización y los mecanismos se infieren de la intensidad y de su respuesta hidrológica.

En segundo lugar, la serie NISAR de la CGSM es todavía corta y sus estados hidrológicos coinciden con dos versiones del producto. La dependencia temporal reduce además el tamaño efectivo de muestra, por lo que la relación con el nivel del río no puede considerarse concluyente. La ausencia de mediciones de nivel dentro del humedal impide relacionar directamente la señal SAR con la lámina de agua local, de modo que el nivel del Magdalena en Remolino se usa como indicador regional. Esas mediciones se solicitaron a INVEMAR, que informó que no están disponibles mientras el convenio de monitoreo hidrosedimentológico con CORPAMAG siga en ejecución.

En tercer lugar, la clave se definió y evaluó con los mismos 720 puntos, por lo que el 68 % de acierto corresponde a resustitución y deberá comprobarse con una muestra independiente. Además, las etiquetas representan 2025 mientras que las observaciones SAR abarcan 2025–2026, de modo que parte del desacuerdo puede corresponder a cambios reales de cobertura.

Finalmente, la referencia presenta incertidumbre intraintérprete. En una segunda interpretación a ciegas de 60 puntos, el acuerdo fue del 78 % [66–87 %], con κ = 0,72 (Figura 18); la mayor inestabilidad se concentró en el humedal herbáceo, una de las clases que los sensores tampoco separan adecuadamente.

![Figura 18. Consistencia de una misma intérprete sobre la muestra de referencia de 2025, con una segunda interpretación a ciegas de 60 puntos. Acuerdo 0,78 [0,66 a 0,87], kappa 0,72.](fig_consistencia_2025.png)

## 5. Conclusiones y trabajo futuro

En Bahía de Málaga, la banda L mostró una respuesta reproducible del copolar del manglar a la marea que no apareció en banda C. El patrón se observó en las dos trayectorias de NISAR, se reprodujo con ALOS-2, resistió la corrección por dependencia temporal y se mantuvo dentro de cada versión del producto. La respuesta se concentró en HH y no en HV, y fue compatible con un aumento de la contribución de doble rebote bajo mayor inundación. Con la corrección de Holm sobre las cinco pruebas primarias de banda L, las dos trayectorias de NISAR en Málaga se mantuvieron y ALOS-2 quedó en el límite; las pendientes fueron de 0,12 a 0,35 dB por metro de marea, con intervalos que excluyen el cero, y el cambio no se concentró en el borde del rodal.

En la CGSM se observó la misma dirección frente al nivel del río, con un aumento de +0,83 dB del HH del manglar relativo al bosque. Sin embargo, los estados alto y bajo coinciden con versiones distintas de NISAR, dentro de cada versión no existe relación con el nivel y la asociación no resiste la corrección por dependencia temporal. Por tanto, el efecto hidrológico aún no puede identificarse independientemente. La banda L también mejoró la separación entre manglar intacto y degradado, aunque no resolvió la frontera entre manglar degradado y humedal herbáceo. La clave decidió 606 de 720 puntos con un 68 % de acierto por resustitución, que deberá evaluarse con una muestra independiente.

El trabajo futuro se concentra en ampliar la serie NISAR D083 hasta disponer de estados altos y bajos del río dentro de una misma versión del producto y en repetir la cartografía con adquisiciones radiométricamente comparables. Además, se evaluará la respuesta bajo dosel con pares interferométricos de NISAR, analizando la coherencia y la fase en relación con el nivel hidrológico. Una respuesta interferométrica consistente permitiría comprobar el mecanismo propuesto con información independiente de la intensidad de retrodispersión. Finalmente, la clave deberá evaluarse con una muestra independiente y temporalmente consistente con las adquisiciones SAR. La polarimetría completa a mayor longitud de onda queda como una extensión posterior.

## Disponibilidad de datos y código

Los scripts de las nueve etapas, los resultados tabulados y las figuras del informe están en el repositorio público https://github.com/linaq11/cgsm-radar-banda-L, bajo licencia MIT. Las escenas NISAR, las series del IDEAM y del mareógrafo y los productos de Earth Engine se obtienen de sus fuentes con los scripts de la etapa 1; la muestra de referencia de 2025 es un producto propio en elaboración y no se distribuye con el informe.

## Referencias

Botero, L. y Salzwedel, H. (1999). Rehabilitation of the Ciénaga Grande de Santa Marta, a mangrove-estuarine system in the Caribbean coast of Colombia. *Ocean & Coastal Management, 42*(2–4), 243–256. https://doi.org/10.1016/S0964-5691(98)00056-8

Brown, C. F., Brumby, S. P., Guzder-Williams, B., Birch, T., Hyde, S. B., Mazzariello, J., Czerwinski, W., Pasquarella, V. J., Haertel, R., Ilyushchenko, S., Schwehr, K., Weisse, M., Stolle, F., Hanson, C., Guinan, O., Moore, R. y Tait, A. M. (2022). Dynamic World, near real-time global 10 m land use land cover mapping. *Scientific Data, 9*, Artículo 251. https://doi.org/10.1038/s41597-022-01307-4

Bunting, P., Rosenqvist, A., Hilarides, L., Lucas, R. M., Thomas, N., Tadono, T., Worthington, T. A., Spalding, M., Murray, N. J. y Rebelo, L.-M. (2022). Global mangrove extent change 1996–2020: Global Mangrove Watch version 3.0. *Remote Sensing, 14*(15), Artículo 3657. https://doi.org/10.3390/rs14153657

Caldwell, P. C., Merrifield, M. A. y Thompson, P. R. (2015). *Sea level measured by tide gauges from global oceans: The Joint Archive for Sea Level holdings* (NCEI Accession 0019568, versión 5.5) [Conjunto de datos]. NOAA National Centers for Environmental Information. https://doi.org/10.7289/V5V40S7W

De Luca, G., Silva, J. M. N. y Modica, G. (2021). A workflow based on Sentinel-1 SAR data and open-source algorithms for unsupervised burned area detection in Mediterranean ecosystems. *GIScience & Remote Sensing, 58*(4), 516–541. https://doi.org/10.1080/15481603.2021.1907896

Dirección General Marítima. (s. f.). [Pronóstico de pleamares y bajamares para Málaga, año 2026, Centro de Investigaciones Oceanográficas e Hidrográficas del Pacífico] [Conjunto de datos]. DIMAR.

Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., Hoersch, B., Isola, C., Laberinti, P., Martimort, P., Meygret, A., Spoto, F., Sy, O., Marchese, F. y Bargellini, P. (2012). Sentinel-2: ESA's optical high-resolution mission for GMES operational services. *Remote Sensing of Environment, 120*, 25–36. https://doi.org/10.1016/j.rse.2011.11.026

Expert Flood Monitoring Alliance. (2022). *Provision of an automated, global, satellite-based flood monitoring product for the Copernicus Emergency Management Service: Product Definition Document (PDD)* (Documento GFM D6, versión 1.4). Copernicus Emergency Management Service. https://elib.dlr.de/195173/1/gfm_pdd_v1_4_20220420_edit.pdf

Google. (s. f.). *Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected, log scaling* [Conjunto de datos]. Earth Engine Data Catalog. https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D. y Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment, 202*, 18–27. https://doi.org/10.1016/j.rse.2017.06.031

Hess, L. L., Melack, J. M. y Simonett, D. S. (1990). Radar detection of flooding beneath the forest canopy: A review. *International Journal of Remote Sensing, 11*(7), 1313–1325. https://doi.org/10.1080/01431169008955095

Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics, 6*(2), 65–70.

Instituto de Hidrología, Meteorología y Estudios Ambientales [IDEAM]. (s. f.). [Nivel instantáneo del río Magdalena en la estación automática Remolino, código 2904700095] [Conjunto de datos]. Datos Abiertos Colombia. https://www.datos.gov.co/d/bdmn-sqnh

Jaramillo, F., Brown, I., Castellazzi, P., Espinosa, L., Guittard, A., Hong, S.-H., Rivera-Monroy, V. H. y Wdowinski, S. (2018). Assessment of hydrologic connectivity in an ungauged wetland with InSAR observations. *Environmental Research Letters, 13*(2), 024003. https://doi.org/10.1088/1748-9326/aa9d23

JAXA EORC. (s. f.). *ALOS-2 PALSAR-2 ScanSAR products, Level 2.2* [Conjunto de datos]. Japan Aerospace Exploration Agency, Earth Observation Research Center. https://www.eorc.jaxa.jp/ALOS/en/dataset/palsar2_l22_e.htm

Lucas, R., Rebelo, L.-M., Fatoyinbo, L., Rosenqvist, A., Itoh, T., Shimada, M., Simard, M., Souza-Filho, P. W., Thomas, N., Trettin, C., Accad, A., Carreiras, J. y Hilarides, L. (2014). Contribution of L-band SAR to systematic global mangrove monitoring. *Marine and Freshwater Research, 65*(7), 589–603. https://doi.org/10.1071/MF13177

Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., Boussetta, S., Choulga, M., Harrigan, S., Hersbach, H., Martens, B., Miralles, D. G., Piles, M., Rodríguez-Fernández, N. J., Zsoter, E., Buontempo, C. y Thépaut, J.-N. (2021). ERA5-Land: A state-of-the-art global reanalysis dataset for land applications. *Earth System Science Data, 13*(9), 4349–4383. https://doi.org/10.5194/essd-13-4349-2021

NASA ASF DAAC. (2026a). *NISAR Beta Geocoded Polarimetric Covariance product (Version 1)* [Conjunto de datos]. NASA Alaska Satellite Facility Distributed Active Archive Center. https://doi.org/10.5067/NIL2GCOV-B1

NASA ASF DAAC. (2026b). *NISAR Provisional Geocoded Polarimetric Covariance product (Version 1)* [Conjunto de datos]. NASA Alaska Satellite Facility Distributed Active Archive Center. https://nisar-docs.asf.alaska.edu/gcov/

Pasquarella, V. J., Brown, C. F., Czerwinski, W. y Rucklidge, W. J. (2023). Comprehensive quality assessment of optical satellite imagery using weakly supervised video learning. En *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops* (pp. 2125–2135). https://doi.org/10.1109/CVPRW59228.2023.00206

Pyper, B. J. y Peterman, R. M. (1998). Comparison of methods to account for autocorrelation in correlation analyses of fish data. *Canadian Journal of Fisheries and Aquatic Sciences, 55*(9), 2127–2140. https://doi.org/10.1139/f98-104

Richards, J. A. (2013). *Remote sensing digital image analysis: An introduction* (5.ª ed.). Springer. https://doi.org/10.1007/978-3-642-30062-2

Richards, J. A., Woodgate, P. W. y Skidmore, A. K. (1987). An explanation of enhanced radar backscattering from flooded forests. *International Journal of Remote Sensing, 8*(7), 1093–1100. https://doi.org/10.1080/01431168708954756

Sen, P. K. (1968). Estimates of the regression coefficient based on Kendall's tau. *Journal of the American Statistical Association, 63*(324), 1379–1389. https://doi.org/10.1080/01621459.1968.10480934

Simard, M., Rivera-Monroy, V. H., Mancera-Pineda, J. E., Castañeda-Moya, E. y Twilley, R. R. (2008). A systematic method for 3D mapping of mangrove forests based on Shuttle Radar Topography Mission elevation data, ICESat/GLAS waveforms and field data: Application to Ciénaga Grande de Santa Marta, Colombia. *Remote Sensing of Environment, 112*(5), 2131–2144. https://doi.org/10.1016/j.rse.2007.10.012

Torres, R., Snoeij, P., Geudtner, D., Bibby, D., Davidson, M., Attema, E., Potin, P., Rommen, B., Floury, N., Brown, M., Navas Traver, I., Deghaye, P., Duesmann, B., Rosich, B., Miranda, N., Bruno, C., L'Abbate, M., Croci, R., Pietropaolo, A., ... Rostan, F. (2012). GMES Sentinel-1 mission. *Remote Sensing of Environment, 120*, 9–24. https://doi.org/10.1016/j.rse.2011.05.028

Yordanov, V. y Brovelli, M. A. (2021). Deforestation mapping using Sentinel-1 and object-based random forest classification on Google Earth Engine. *The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, XLIII-B3–2021*, 865–872. https://doi.org/10.5194/isprs-archives-XLIII-B3-2021-865-2021

Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., Brockmann, C., Kirches, G., Wevers, J., Cartus, O., Santoro, M., Fritz, S., Lesiv, M., Herold, M., Tsendbazar, N.-E., Xu, P., Ramoino, F. y Arino, O. (2022). *ESA WorldCover 10 m 2021 v200* [Conjunto de datos]. Zenodo. https://doi.org/10.5281/zenodo.7254221

## Anexo A. Flujo de trabajo, scripts y productos

Este anexo documenta la trazabilidad computacional del análisis. La Figura A1 presenta la cadena de procesamiento de cada sensor para las etapas de adquisición, calibración y preparación de los datos SAR, y la Figura A2 resume el flujo completo del estudio en nueve etapas, desde el acceso a los datos hasta la cartografía y el contraste óptico. La organización de la cadena SAR sigue los flujos de procesamiento revisados por De Luca et al. (2021) y Yordanov y Brovelli (2021).

Las imágenes de las Figuras 1 y A1 se exportan con `exportar_figuras_flujo.py`, `exportar_series.py` y `exportar_productos.py`, y la Figura A2 se genera con `figura_flujo.py`. La Tabla A1 relaciona cada etapa con los scripts que la ejecutan y sus principales productos.

![Figura A1. Cadena de procesamiento SAR por sensor, desde la adquisición y la calibración radiométrica hasta la extracción de la retrodispersión. Los ejemplos corresponden a NISAR D083 HH (29 de octubre de 2025), ALOS-2 ScanSAR HH (2 de diciembre de 2025) y Sentinel-1 D142 VV (9 de enero de 2026) sobre la CGSM.](fig_cadena_sar_sensores.png)

![Figura A2. Flujo de trabajo del estudio en nueve etapas, desde el acceso a los datos hasta la cartografía de la señal y el contraste óptico.](fig_flujo_trabajo_es.png)

Tabla A1. Scripts y productos de cada etapa del flujo de trabajo.

| Etapa | Scripts | Principales salidas |
|---|---|---|
| 1. Acceso a datos | `16_inventario_nisar`, `17_descargar_nisar`, `18_nisar_recorte_remoto`, `23_nisar_recorte_pacifico`, `24_nisar_recorte_cgsm`, `nivel_ideam_descarga` | Tabla 1; `nisar_cgsm_granulos.json`; 45 escenas `NISAR_AOI_*.h5`; `nivel_ideam_*.csv` |
| 2. Preprocesamiento y calibración | `18_nisar_recorte_remoto`, `20_nisar_incidencia`, `alos2_marea_malaga`, `s1_marea_malaga` | σ⁰ por sensor y pasada; malla de incidencia de NISAR; Figura 4 |
| 3. Coberturas de referencia y muestreo | `perfil_pacifico_24`, `doble_rebote_incidencia`, `figuras_cgsm`, `figuras_pacifico` | 1.600 puntos por sitio; 2.444 puntos de manglar y 2.400 de bosque para el análisis por terciles de incidencia; Figura 2 |
| 4. Forzante hidrológico | `mareas_buenaventura`, `mareas_dimar_a_serie`, `marea_vs_radar`, `cgsm_nivel_rio` | Marea, precipitación antecedente y nivel del río asignados a cada pasada |
| 5. Estadística por pasada | `perfil_pacifico_24`, `marea_vs_radar`, `cgsm_temporada` | `cgsm_temporada_*.csv`; Tabla 2 y Tabla B1 |
| 6. Prueba hidrológica | `marea_vs_radar`, `s1_marea_malaga`, `alos2_marea_malaga`, `cgsm_temporada`, `cgsm_nivel_rio`, `figura_cgsm_optico` | Tablas 3 a 6 y B2 a B3; Figuras 5 y 7 a 12 |
| 7. Robustez y límites | `doble_rebote_incidencia`, `autocorrelacion_temporal`, `pendientes_auditoria`, `auditoria_calculos.md` | Tablas 7, 9 y 12; Figuras 6 y B1; `pendientes_auditoria_*.csv`; auditoría de cálculos |
| 8. Clave de interpretación | `figura_clave`, `nisar_flotante`, `clave_vs_muestra2025` | Tablas 8 a 10 y B4; Figura 13; `clave_muestra2025_*.csv` |
| 9. Cartografía y contraste óptico | `mapa_doble_rebote`, `mapa_doble_rebote_s1`, `mapa_doble_rebote_malaga`, `corroboracion_dw` | Tabla 11 y B5; Figuras 14 a 17; `mapa_doble_rebote_50m.tif`, `mapa_s1_alto_bajo_50m.tif`, `dw_serie.csv` |
| Informe y figuras metodológicas | `md_a_word`, `exportar_figuras_flujo`, `exportar_series`, `exportar_productos`, `figura_flujo`, `figura_cadena_sar` | Informe; Figuras 1, A1 y A2 |

## Anexo B. Resultados auxiliares

Tabla B1. Mediana de σ⁰ por cobertura en las cinco primeras adquisiciones NISAR de la trayectoria A004 (8 y 20 de noviembre y 2, 14 y 26 de diciembre de 2025), en dB.

| Cobertura | HH | HV | HH−HV |
|---|---|---|---|
| Manglar (consenso WorldCover y GMW) | −6,9 / −7,2 / −7,6 / −7,8 / −7,5 | −14,3 / −14,1 / −14,0 / −14,2 / −14,1 | 7,3 / 6,7 / 6,5 / 6,4 / 6,8 |
| Manglar solo en GMW | −8,9 / −8,5 / −8,8 / −8,7 / −8,9 | −15,8 / −15,3 / −15,3 / −15,9 / −15,6 | 6,4 / 6,4 / 6,4 / 6,5 / 6,5 |
| Bosque | −7,3 / −7,6 / −7,4 / −7,8 / −7,2 | −13,4 / −13,4 / −13,4 / −13,6 / −13,5 | 6,3 / 6,0 / 6,0 / 6,0 / 6,0 |
| Humedal herbáceo | −9,7 / −9,6 / −9,4 / −9,5 / −9,9 | −17,2 / −16,8 / −16,8 / −17,4 / −16,8 | 6,8 / 6,6 / 7,0 / 6,9 / 6,9 |
| Agua | −20,5 / −18,8 / −19,3 / −19,5 / −19,2 | −25,9 / −25,8 / −26,0 / −25,8 / −25,7 | 5,2 / 6,9 / 6,8 / 6,0 / 6,7 |

Tabla B2. Correlación entre la precipitación acumulada de 30 días y la retrodispersión de Sentinel-1 en la CGSM.

| Órbita (hora local, n) | Clase | VV | VH | VV−VH |
|---|---|---|---|---|
| 77 ascendente (18:06, 58) | Manglar | ρ 0,32, p 0,01 | ρ 0,14, p 0,31 | ρ 0,25, p 0,06 |
| 77 ascendente (18:06, 58) | Bosque | ρ 0,52, p < 0,001 | ρ 0,21, p 0,12 | ρ 0,38, p 0,003 |
| 77 ascendente (18:06, 58) | Manglar − bosque | ρ −0,35, p 0,01 | ρ −0,13, p 0,35 | ρ −0,17, p 0,19 |
| 142 descendente (05:48, 61) | Manglar | ρ 0,21, p 0,11 | ρ 0,18, p 0,17 | ρ −0,04, p 0,74 |
| 142 descendente (05:48, 61) | Bosque | ρ 0,58, p < 0,001 | ρ 0,41, p 0,001 | ρ 0,50, p < 0,001 |
| 142 descendente (05:48, 61) | Manglar − bosque | ρ −0,52, p < 0,001 | ρ −0,34, p 0,01 | ρ −0,44, p < 0,001 |

Tabla B3. Relación entre la precipitación acumulada de 30 días y la retrodispersión de NISAR D083 en la CGSM.

| Clase | HH | HV | HH−HV | HH, húmeda − seca (dB) |
|---|---|---|---|---|
| Manglar | ρ 0,50, p 0,10 | ρ −0,26, p 0,42 | ρ 0,54, p 0,07 | −0,15 |
| Bosque | ρ 0,02, p 0,95 | ρ −0,34, p 0,29 | ρ 0,29, p 0,35 | +0,26 |
| Manglar − bosque | ρ 0,58, p 0,05 | ρ 0,26, p 0,42 | ρ 0,39, p 0,22 | −0,44 |

Tabla B4. Firmas multifecha de las coberturas de la CGSM en bandas C y L, en dB. La vegetación flotante se define por el polígono ZC-2025, delimitado sobre Sentinel-2.

| Cobertura | VV | VH | VV − VH | HH | HV | HH − HV |
|---|---|---|---|---|---|---|
| Agua abierta | −21,1 | −30,9 | 9,0 | −20,0 | −25,6 | 6,1 |
| Vegetación flotante | −13,3 | −20,7 | 7,5 | −16,6 | −23,3 | 6,6 |
| Humedal herbáceo | −9,9 | −15,2 | 5,3 | −9,2 | −17,5 | 7,9 |
| Manglar | −9,6 | −14,9 | 5,3 | −10,9 | −17,2 | 6,1 |
| Bosque seco (control) | −8,1 | −14,3 | 6,2 | −9,2 | −15,9 | 6,6 |

Tabla B5. Cambio de retrodispersión entre marea alta y baja en Bahía de Málaga, por trayectoria y cobertura, en dB.

| Traza | Clase | Píxeles | ΔHH | ΔHH > 0 | ΔHV | Δ(HH − HV) |
|---|---|---|---|---|---|---|
| A004 (05:46) | Manglar | 34.344 | +0,34 (−0,01 a +0,69) | 75 % | −0,36 | +0,70 |
| A004 (05:46) | Bosque (control) | 300.038 | −0,10 (−0,36 a +0,17) | 40 % | −0,34 | +0,25 |
| A004 (05:46) | Agua | 214.339 | −0,07 (−0,45 a +0,30) | 45 % | −0,51 | +0,43 |
| D087 (18:29) | Manglar | 34.344 | +0,05 (−0,35 a +0,42) | 54 % | −0,53 | +0,64 |
| D087 (18:29) | Bosque (control) | 300.038 | −0,39 (−0,79 a −0,06) | 21 % | −0,63 | +0,32 |
| D087 (18:29) | Agua | 214.339 | −0,42 (−0,90 a +0,05) | 27 % | −0,94 | +0,63 |

![Figura B1. Cambio de HH del manglar entre los periodos de nivel alto y bajo del río (CGSM, NISAR D083) y entre marea alta y baja (Bahía de Málaga, A004 y D087) según la distancia del píxel de 50 m al borde del manglar: mediana y rango intercuartílico.](fig_borde_interior.png)
