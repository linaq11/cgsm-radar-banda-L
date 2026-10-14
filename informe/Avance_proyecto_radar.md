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

En la Ciénaga Grande de Santa Marta la hidrología es el problema central. La obstrucción de los caños que la conectan con el río Magdalena produjo la hipersalinización y la mortalidad masiva de manglar de los años ochenta y noventa, y la rehabilitación consistió en reabrir esa conexión (Botero y Salzwedel, 1999). Simard et al. (2008) cartografiaron en tres dimensiones el manglar de la ciénaga con SRTM, ICESat y datos de campo. Jaramillo et al. (2018) evaluaron la conectividad hidrológica del humedal, que no tiene aforos, con observaciones interferométricas de radar. Ninguno de esos trabajos midió la respuesta temporal de la retrodispersión en banda L a la inundación bajo el dosel. En este sentido, el nivel del río en Remolino y, cuando INVEMAR las entregue, las series de nivel dentro del humedal son los forzantes contra los que se contrasta la señal.

Con el fin de cubrir ese vacío, este avance compara NISAR y ALOS-2 en banda L con Sentinel-1 en banda C, con Bahía de Málaga como sitio mareal de contraste y la CGSM como sistema ligado al nivel del río Magdalena. La pregunta es qué información adicional aporta la banda L frente a Sentinel-1 para identificar condiciones de inundación bajo dosel de manglar en la CGSM. Para responderla se caracteriza la respuesta de retrodispersión de las coberturas representativas de la ciénaga en las dos bandas, se compara esa respuesta en zonas de manglar con distintas condiciones de inundación y, finalmente, se interpretan las diferencias a partir de los mecanismos de dispersión de superficie, de volumen y de doble rebote.

## 2. Datos y métodos

### 2.1 Diseño y sitios de estudio

El estudio se diseñó con la Ciénaga Grande de Santa Marta (CGSM) como sitio principal y Bahía de Málaga (Buenaventura), en el Pacífico colombiano, como sitio de contraste. En la ciénaga la inundación del manglar sigue al nivel del río Magdalena, mientras que en Bahía de Málaga responde a la marea. Esa diferencia permite establecer si la respuesta de la banda L se mantiene bajo dos forzantes hidrológicos distintos.

Se analizaron cuatro coberturas: agua abierta, humedal herbáceo, manglar y un bosque de control que no se inunda. La extensión de manglar se tomó del consenso entre WorldCover 2021 y Global Mangrove Watch. Se usaron Sentinel-1 en banda C y NISAR y ALOS-2 en banda L sobre periodos comparables, con 45 escenas de NISAR en total, 21 sobre la ciénaga y 24 sobre Bahía de Málaga (Tabla 1).

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

![Figura 1. Flujo metodológico del estudio. Integración de datos SAR y auxiliares, preprocesamiento por sensor, muestreo por coberturas, asignación de forzantes hidrológicos, pruebas analíticas y productos cartográficos utilizados para comparar la respuesta de las bandas C y L ante condiciones de inundación bajo dosel.](fig_diseno_estudio_h.png)

### 2.4 Coberturas de referencia y muestreo

Puesto que en el Pacífico no existen puntos interpretados ni estaciones de campo, la cobertura se toma de dos productos globales independientes. Para agua, bosque y humedal herbáceo se usa WorldCover 2021 (10 m, Zanaga et al., 2022). Para el manglar se usa el consenso entre WorldCover y Global Mangrove Watch v3 (extensión de 2020, Bunting et al., 2022).

Sobre la caja de Bahía de Málaga, Global Mangrove Watch marca 6.006 ha de manglar y WorldCover 7.576 ha. Los dos productos coinciden en 5.326 ha, el 89 % del primero y el 70 % del segundo. El manglar que solo aparece en Global Mangrove Watch es entre 0,9 y 2 dB más oscuro en las dos polarizaciones (mediana de 1,2 dB en HH y 1,5 en HV) y se parece al humedal herbáceo. Por lo tanto, corresponde a bordes, manglar bajo o zonas que cambiaron entre 2020 y 2021. De esta manera, la clase de referencia del Pacífico es el manglar en el que ambos productos coinciden.

La Figura 2 muestra las coberturas de referencia dentro del área de estudio. El manglar de consenso entre WorldCover 2021 y Global Mangrove Watch 2020 suma 33.173 ha. Otras 8.157 ha aparecen solo en WorldCover y 8.395 ha solo en Global Mangrove Watch, y estas últimas se concentran en el delta del suroccidente y en el borde noroccidental. El bosque que se usa como control ocupa las franjas del oriente y del sur, fuera del plano inundable, y corresponde a bosque seco.

![Figura 2. Coberturas de referencia dentro del área de estudio de la CGSM (2.042 km²): (a) clases de WorldCover 2021; (b) coincidencia entre la clase manglar de WorldCover 2021 y Global Mangrove Watch 2020. El manglar muestreado en las pruebas es el que cartografían los dos productos.](fig_cgsm_referencia.png)

En los dos sitios se muestrearon 400 puntos por clase, sorteados una vez con el muestreo estratificado de Earth Engine (semilla 42) y compartidos por los tres sensores. En la ciénaga el sorteo usa dos regiones declaradas. La primera reúne el manglar de consenso, el humedal herbáceo y el agua dentro del área de estudio de 2.042 km². La segunda es el bosque de WorldCover sobre la caja del cubo de 4.304 km², puesto que el bosque seco de los piedemontes que sirve de control queda fuera del área de estudio en todas las pasadas de Sentinel-1 con cobertura completa del periodo y en las de ALOS-2, que son solo diez sobre la ciénaga, siete completas, insuficientes para evaluar por trayectoria.

### 2.5 Forzantes hidrológicos

La altura de marea en cada pasada se tomó del pronóstico oficial de la DIMAR para Málaga (Dirección General Marítima, s. f.). Ese pronóstico es la tabla anual de pleamares y bajamares de 2026 referida al LAT, que se interpoló entre extremos con medio coseno y se refirió al nivel medio del año.

Para las diez pasadas de octubre a diciembre de 2025, año que la DIMAR ya no publica, se usó una predicción armónica propia ajustada al mareógrafo histórico de Buenaventura (UHSLC, estación 085, registro horario 1953 a 2014; Caldwell et al., 2015). La predicción usa once constituyentes ajustados a 2010–2013, con M2 de 1,51 m y S2 de 0,41 m, y se validó en 2014 con un error medio cuadrático de 0,15 m sobre un rango de 5,24 m.

En las catorce pasadas de 2026 ambas fuentes coinciden con una correlación de Spearman de 0,95, un sesgo medio de 3 cm y una diferencia absoluta media de 20 cm (error cuadrático medio de 24 cm, máximo de 41 cm). Por lo tanto, el orden de las pasadas por marea es el mismo con una u otra fuente, aunque las alturas difieran. Las 24 pasadas caen entre −1,2 y +2,2 m respecto al nivel medio, en las dos trazas.

En la CGSM no hay marea, de modo que la variable hidrológica se reemplazó por la lluvia acumulada (Tabla 7 para Sentinel-1, Tabla 8 para NISAR) en los treinta días previos a cada pasada, promediada sobre el AOI con ERA5-Land. También se usó la partición entre época seca (diciembre a abril) y húmeda (mayo a noviembre).

La prueba con la lluvia usa las 12 pasadas descendentes anteriores al 11 de septiembre de 2026, fecha hasta la que llega ERA5-Land. Las dos de septiembre entran en la prueba con el nivel del río y en la clave. La traza ascendente, con seis pasadas con lluvia, no se evalúa con la lluvia. Con el nivel del río, en cambio, alcanza las siete pasadas y entra en la Tabla 9.

La lluvia se reemplazó después por una variable hidrológica medida, el nivel del río Magdalena en la estación automática Remolino del IDEAM (código 2904700095, a 10,83° N y 74,74° O, aguas arriba de los caños que alimentan el occidente de la ciénaga). La estación tiene registro horario desde enero de 2025, disponible en los datos abiertos del IDEAM (IDEAM, s. f., `nivel_ideam_descarga.py`, `cgsm_nivel_rio.py`).

El nivel se interpoló a la hora de cada pasada y se aplicó la misma regla de lectura del sitio mareal: manglar menos bosque, diferencia entre el tercio de nivel alto y el de nivel bajo, y correlación de Spearman con el nivel. En el periodo de las pasadas el río osciló entre 0,79 m (Sentinel-1) o 0,91 m (NISAR D083; 0,82 m en la traza A007) y 2,67 m. Además, el nivel y la lluvia de treinta días están correlacionados (ρ 0,70, p 0,01), de modo que las dos pruebas no son independientes.

### 2.6 Regla de lectura y robustez

La regla de lectura se fijó antes de mirar los números. Si la banda L ve la inundación bajo el dosel, dentro de cada traza el manglar debe mostrar mayor HH y mayor HH−HV en marea alta que en baja, y el bosque, que no se inunda, no. Para descontar el efecto estacional, se resta fecha a fecha el valor del bosque al del manglar. La Tabla 4 y la Figura 5 muestran el resultado.

Cada pasada se reduce a una mediana por clase y a la resta manglar menos bosque, que descuenta la humedad estacional común a todas las coberturas. Dentro de cada traza se calcula la diferencia de medianas entre las pasadas de forzante alto y bajo (mitades en Málaga, tercios en la ciénaga) y la correlación de Spearman con el forzante. La robustez somete ese resultado a los tercios de ángulo de incidencia, a la corrección por dependencia temporal, a una recomputación independiente y a la versión del producto de NISAR.

La correlación de Spearman trata cada pasada como una observación independiente. Si la serie de radar y la de su forzante se parecen a sí mismas de una pasada a la siguiente, las n pasadas valen por menos y el valor p sale optimista. Por lo tanto, para cada traza se midió la autocorrelación de rezago 1 de las dos series, sobre rangos y en orden de fecha. Después se calculó el tamaño efectivo de muestra de Pyper y Peterman (1998), primero con el rezago 1 y después con todos los rezagos hasta n/5, que es la versión que corresponde a una serie con ciclo estacional. El valor p se recalculó con ese tamaño efectivo (`autocorrelacion_temporal.py`).

### 2.7 Clave de interpretación y validación

La clave de interpretación, que responde al tercer propósito de la introducción, reúne la firma de cada cobertura en las dos bandas, como mediana entre pasadas del copolar, del cruzado y de su diferencia. Esa firma se calcula primero sobre las coberturas de los productos globales y después sobre los 720 puntos de la muestra de referencia de 2025 de la tesis, con la separabilidad de Jeffries-Matusita por pares de clases. La regla de lectura se reescribe con los umbrales medidos en esa muestra y se evalúa sobre ella (acierto de resustitución). La separabilidad se calcula como distancia de Jeffries-Matusita con la distancia de Bhattacharyya bajo supuesto gaussiano, en un guion propio (`clave_vs_muestra2025.py`). Los 720 puntos son la muestra de entrenamiento de la tesis: ocho estratos y sorteo fuera de la reserva de validación con distancia mínima de 200 m. Se etiquetaron a ciegas en seis clases sobre imagen de alta resolución de 2025, los 400 primeros se revisaron bajo un criterio escrito, y cada punto lleva marca de borde cuando la ventana de 3 × 3 píxeles mezcla clases. La Figura 3 muestra los 720 puntos por clase final sobre el área de estudio, la reserva de validación que el sorteo no toca y los bloques de 12 km de la validación cruzada espacial de la tesis.

![Figura 3. Muestra de referencia de 2025 sobre el área de estudio de la CGSM: 720 puntos coloreados por clase final (agua abierta 212, manglar intacto 151, vegetación flotante 129, manglar degradado 111, humedal herbáceo 73, otro 44), la reserva de validación que el sorteo no toca (sombreada) y los bloques de 12 km de la validación cruzada espacial (punteados). Los puntos se sortearon fuera de la reserva con una separación mínima de 200 m y se etiquetaron a ciegas sobre imagen de alta resolución de 2025.](fig_muestra_2025.png)

### 2.8 Cartografía de la señal y contraste óptico

Los mapas de la señal aplican la comparación alto menos bajo píxel a píxel, a 50 m, sobre la malla UTM 18N (EPSG:32618) de los recortes de NISAR, que cubren la caja del cubo más un margen de 2 km. Se diferencian de la prueba por clase en el reparto. En lugar de tercios de nivel, en la ciénaga se usan todas las pasadas de la traza 083 en dos bloques de fechas: seis de nivel alto (octubre de 2025 a enero de 2026, colección Beta) y ocho de nivel bajo (junio a septiembre de 2026, colección Provisional). Por lo tanto, el reparto coincide con la versión del producto y así se declara. Con Sentinel-1 se toman las pasadas de la órbita 142 en las mismas dos ventanas de fechas (13 y 18), lo que compara periodos y no niveles. En Bahía de Málaga el forzante es la marea en la pasada y, por traza, se comparan las seis pasadas de marea más alta con las seis de marea más baja sobre el recorte completo de cada traza, que excede la caja de 2.4. La corroboración óptica usa la banda `flooded_vegetation` de Dynamic World V1 (Brown et al., 2022) en las fechas con al menos la mitad del manglar sin nubes, con la media por clase por fecha y, para el mapa, la mediana por píxel en las mismas dos ventanas de fechas de NISAR con al menos dos fechas válidas por grupo.

## 3. Resultados

### 3.1 Perfil de retrodispersión en Bahía de Málaga

Tabla 2. Mediana de sigma cero en dB (GCOV, gamma cero con corrección de terreno, convertido a sigma cero con el factor que trae el producto) por cobertura en las cinco primeras escenas NISAR (traza ascendente 004: 8 y 20 de noviembre, 2, 14 y 26 de diciembre de 2025), 400 puntos por clase, ángulo de incidencia mediano de 42°.

| Cobertura | HH | HV | HH−HV |
|---|---|---|---|
| Manglar (consenso WorldCover y GMW) | −6,9 / −7,2 / −7,6 / −7,8 / −7,5 | −14,3 / −14,1 / −14,0 / −14,2 / −14,1 | 7,3 / 6,7 / 6,5 / 6,4 / 6,8 |
| Manglar solo en GMW | −8,9 / −8,5 / −8,8 / −8,7 / −8,9 | −15,8 / −15,3 / −15,3 / −15,9 / −15,6 | 6,4 / 6,4 / 6,4 / 6,5 / 6,5 |
| Bosque | −7,3 / −7,6 / −7,4 / −7,8 / −7,2 | −13,4 / −13,4 / −13,4 / −13,6 / −13,5 | 6,3 / 6,0 / 6,0 / 6,0 / 6,0 |
| Humedal herbáceo | −9,7 / −9,6 / −9,4 / −9,5 / −9,9 | −17,2 / −16,8 / −16,8 / −17,4 / −16,8 | 6,8 / 6,6 / 7,0 / 6,9 / 6,9 |
| Agua | −20,5 / −18,8 / −19,3 / −19,5 / −19,2 | −25,9 / −25,8 / −26,0 / −25,8 / −25,7 | 5,2 / 6,9 / 6,8 / 6,0 / 6,7 |

De la Tabla 2 se desprenden tres lecturas preliminares. En primer lugar, las cinco fechas, tomadas en siete semanas a la misma hora, varían menos de 1 dB en bosque, humedal herbáceo y manglar de consenso, y hasta 1,7 dB en el agua abierta en HH. Esta variación da la línea base de estabilidad antes de buscar el efecto de la marea.

En segundo lugar, el manglar devuelve entre 0,4 y 1 dB más de HH−HV que el bosque con HV igual o menor, lo que es compatible con una componente de doble rebote que en el bosque no existe. Sin embargo, con cinco fechas de la misma hora se trata de un indicio y no de un resultado. Finalmente, frente a la CGSM en diciembre de 2025 (manglar HH −10,8 dB y HV −17,7 dB), el manglar del Pacífico es unos 3,5 dB más brillante en ambas polarizaciones, coherente con un bosque más alto y denso. No obstante, la diferencia de traza, hora e incidencia impide atribuirla todavía a la estructura sola.

Con las dos trazas completas, la Tabla 3 resume el nivel y la variación de cada cobertura por traza, y de ella se desprenden tres observaciones. En primer lugar, dentro de cada traza el manglar varía muy poco entre fechas, con desviación de 0,3 a 0,4 dB en HH. Por lo tanto, el efecto de la marea, si existe, es de ese orden y exige la altura de marea por pasada para aislarlo.

En segundo lugar, las dos trazas no son comparables de forma directa porque su geometría difiere, con incidencia mediana de 42° en la ascendente y 35° en la descendente. A esa diferencia de geometría se debe la diferencia de nivel entre ellas. Finalmente, en la traza descendente, de incidencia más pronunciada, el manglar queda 0,6 dB por encima del bosque en HH y 1,1 dB en HH−HV. En la ascendente, en cambio, son iguales en HH y el manglar queda 0,7 dB por encima en HH−HV. Este es el comportamiento que se esperaría de una componente de doble rebote que crece al disminuir el ángulo de incidencia, y es la hipótesis que la marea permitirá poner a prueba.

Por otra parte, todas las coberturas, incluida el agua, suben entre 1 y 1,8 dB en HV (mediana 1,5) entre junio y septiembre frente a noviembre y enero. Puesto que afecta también al agua abierta, puede ser un efecto de la versión del producto, Beta hasta enero y Provisional desde junio, tanto como estacional, y en cualquier caso debe descontarse antes de leer la marea.

Tabla 3. Mediana por cobertura y traza en las 24 escenas NISAR (dB, sigma cero) y desviación estándar entre las 12 fechas de cada traza.

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

La Figura 4 muestra las composiciones de NISAR de las dos trazas sobre Bahía de Málaga, con el contorno de manglar de consenso, y la diferencia de HH entre ellas.

![Figura 4. Compuestos NISAR GCOV de Bahía de Málaga (R = HH, G = HV, B = HH − HV) para las trazas ascendente y descendente con dos días de diferencia, con el contorno del manglar de consenso, y la diferencia de HH entre trazas, que refleja la distinta geometría de incidencia.](fig_malaga_radar.png)

### 3.2 Marea y retrodispersión del manglar en banda L (NISAR)

Tabla 4. Relación entre la altura de marea en la pasada y la retrodispersión, por traza (12 pasadas cada una): diferencia de medianas entre las pasadas por encima y por debajo de la mediana de marea, y correlación de Spearman con su valor p.

| Traza | Variable | Manglar: alta − baja (dB), ρ, p | Bosque: alta − baja (dB), ρ, p | Manglar − bosque: alta − baja (dB), ρ, p |
|---|---|---|---|---|
| A004 | HH | +0,28, 0,76, 0,004 | −0,11, −0,09, 0,78 | +0,57, 0,83, 0,001 |
| A004 | HV | −0,36, −0,11, 0,73 | −0,31, −0,13, 0,70 | +0,03, 0,11, 0,73 |
| A004 | HH−HV | +0,76, 0,53, 0,08 | +0,31, 0,20, 0,53 | +0,45, 0,83, 0,001 |
| D087 | HH | −0,02, 0,25, 0,44 | −0,49, −0,36, 0,25 | +0,57, 0,74, 0,006 |
| D087 | HV | −1,26, −0,41, 0,18 | −1,30, −0,50, 0,10 | +0,07, −0,06, 0,85 |
| D087 | HH−HV | +0,88, 0,76, 0,005 | +0,44, 0,13, 0,68 | +0,61, 0,60, 0,04 |

En las dos trazas, de forma independiente, la señal del manglar relativa al bosque sube con la marea en HH (ρ de 0,83 y 0,74, p de 0,001 y 0,006) y en HH−HV (ρ de 0,83 y 0,60), y no en HV (ρ de 0,11 y −0,06). El bosque no responde a la marea en ninguna variable. Este patrón es compatible con el doble rebote entre troncos y agua, descrito para bosques inundados desde los primeros trabajos con radar de banda L (Richards et al., 1987; Hess et al., 1990): aumenta la polarización HH y no la cruzada.

El tamaño del efecto es pequeño, cerca de 0,6 dB entre marea alta y baja, del orden de la variación entre fechas dentro de una traza. Esto explica por qué no se veía sin la marea. Con doce pasadas por traza y una marea tomada de la tabla oficial en 2026 y predicha en 2025, el resultado se reporta como una dirección con alta consistencia entre trazas, no como una medida definitiva. Esa dirección se somete a continuación a la estratificación por ángulo de incidencia y a la comparación con Sentinel-1 y ALOS-2 sobre el mismo sitio.

Una auditoría independiente de los cálculos (16 de septiembre, `auditoria_calculos.md`) rederivó esta tabla desde los datos y encontró que la versión anterior se había calculado con la predicción propia en las 24 pasadas. Los valores de esta versión corresponden a la serie mixta, y los seis estadísticos que sostienen la lectura no cambian.

![Figura 5. Retrodispersión del manglar y del bosque frente a la altura de marea predicha a la hora de cada pasada de NISAR, por traza. El HH y el HH − HV del manglar relativos al bosque suben con la marea; el HV no responde en ninguna de las dos clases.](fig_marea_vs_radar.png)

La estratificación por ángulo de incidencia se hizo con unos 1.200 puntos de manglar por traza (1.232 en la ascendente y 1.212 en la descendente) y otros 1.200 de bosque divididos en tercios de incidencia dentro de cada traza. El primer hallazgo es una limitación del sitio. La caja de Bahía de Málaga ocupa una fracción tan pequeña de la franja de NISAR que la incidencia casi no varía dentro de ella, de 42° a 43° en la traza ascendente y de 34° a 37° en la descendente. Por lo tanto, la estratificación aporta poco contraste de incidencia.

Aun así, la respuesta a la marea del manglar relativa al bosque es positiva en HH en los seis tercios (entre +0,27 y +0,77 dB de marea alta a baja, ρ de 0,48 a 0,97, p menor que 0,05 en cinco de seis) y en HH−HV en los seis. En cambio, HV no responde en ninguno (ρ entre −0,34 y 0,37, todos con p mayor que 0,2).

En la traza descendente el tercio de menor incidencia responde más que el de mayor, en la dirección que predice el doble rebote. Sin embargo, con dos grados de diferencia esa comparación no se sostiene como prueba. Así, el resultado no cambia de signo con la geometría dentro de cada traza. No obstante, establecer la dependencia con la incidencia exige un sitio más ancho en rango o trazas con la misma hora de paso (Figura 6).

![Figura 6. Prueba de doble rebote por tercil de ángulo de incidencia dentro de cada traza de NISAR: cambio de la retrodispersión manglar menos bosque entre marea alta y baja, con la correlación de Spearman y su valor p. HH y HH − HV responden en todos los terciles; HV en ninguno.](fig_doble_rebote_incidencia.png)

### 3.3 La misma prueba con Sentinel-1

Con el fin de establecer si la banda C muestra la misma respuesta, se repitió la prueba con todas las pasadas de Sentinel-1 GRD que cubren la caja entre octubre de 2025 y septiembre de 2026. En total son 89 pasadas con cobertura completa, en dos órbitas relativas, la 48 ascendente a las 18:21 hora local cada doce días (26 pasadas) y la 142 descendente a las 05:50 cada cinco o seis días (63 pasadas). La prueba se hizo sobre los mismos 1.600 puntos y con la marea predicha a la hora de cada pasada.

Veintitrés de esas pasadas caen a menos de tres días de una pasada de NISAR. La Tabla 5 resume el resultado con la misma regla.

Tabla 5. Sentinel-1: relación entre la altura de marea en la pasada y la retrodispersión del manglar relativa al bosque, por órbita (diferencia de medianas alta − baja, ρ de Spearman y valor p).

| Órbita (hora local, n) | VV | VH | VV−VH |
|---|---|---|---|
| 48 ascendente (18:21, 26) | −0,07 dB, ρ −0,18, p 0,37 | −0,11 dB, ρ −0,30, p 0,14 | +0,16 dB, ρ 0,23, p 0,26 |
| 142 descendente (05:50, 63) | −0,07 dB, ρ −0,13, p 0,32 | 0,00 dB, ρ −0,08, p 0,55 | −0,15 dB, ρ −0,15, p 0,24 |

En banda C no hay relación entre la marea y la señal del manglar relativa al bosque en ninguna órbita ni polarización (Figura 7), con muestras de 26 y 63 pasadas, mayores que las de NISAR. Además, en el copolar los signos son contrarios a los de la banda L. En VV − VH la órbita 48 da +0,16 dB sin significancia. La única correlación con valor p bajo es la del manglar solo en VV de la órbita 142, negativa (ρ −0,39, p 0,002). Esta correlación desaparece al restar el bosque y, en todo caso, va en la dirección opuesta al doble rebote.

Por lo tanto, sobre el mismo sitio, los mismos puntos y la misma marea, la banda L responde a la marea en el manglar y la banda C no. La limitación declarada en la propuesta se mantiene. Puesto que Sentinel-1 no tiene HH, parte de la diferencia puede deberse a la polarización y no solo a la longitud de onda.

![Figura 7. Retrodispersión de Sentinel-1 en banda C del manglar y del bosque frente a la altura de marea predicha, por órbita relativa. A diferencia del HH de NISAR, ninguna polarización sube con la marea en el manglar.](fig_s1_marea.png)

### 3.4 La misma prueba con ALOS-2

Puesto que Sentinel-1 no tiene HH, se repitió la prueba con ALOS-2 PALSAR-2 ScanSAR, el otro sensor de banda L, que sí observa en HH y HV. Se reunieron 72 escenas con ambas polarizaciones entre enero de 2025 y septiembre de 2026, mosaicadas en 57 pasadas, de las cuales 39 cubren la caja completa. De estas, 36 están en dos trayectorias descendentes que pasan al mediodía (path 139, 21 pasadas a las 11:53, y path 140, 15 pasadas a las 12:00) y 3 en una ascendente nocturna (path 47) que no se evalúa.

La prueba se hizo sobre los mismos 1.600 puntos y con la marea a la hora de cada pasada, tomada de la predicción armónica extendida a 2025. La Tabla 6 resume el resultado con la misma regla.

Tabla 6. ALOS-2: relación entre la altura de marea en la pasada y la retrodispersión del manglar relativa al bosque, por trayectoria (diferencia de medianas alta − baja, ρ de Spearman y valor p).

| Path (hora local, n) | HH | HV | HH−HV |
|---|---|---|---|
| 139 descendente (11:53, 21) | +0,25 dB, ρ 0,65, p 0,002 | +0,06 dB, ρ 0,05, p 0,81 | +0,13 dB, ρ 0,47, p 0,03 |
| 140 descendente (12:00, 15) | +0,49 dB, ρ 0,72, p 0,002 | −0,16 dB, ρ −0,45, p 0,10 | +0,91 dB, ρ 0,79, p < 0,001 |

ALOS-2 reproduce el resultado de NISAR (Figura 8). En las dos trayectorias la señal del manglar relativa al bosque sube con la marea en HH y en HH−HV, y no en HV, y el bosque solo no responde en HH (ρ −0,04 y −0,11). En el path 139 el HV de las dos coberturas, bosque incluido, baja con la marea (ρ −0,66 y −0,62). Esto muestra que en pasadas de mediodía la altura de marea queda ligada a la estación y arrastra el efecto estacional de HV. La resta del bosque elimina ese sesgo, y por eso es el estadístico que se reporta.

Con tres sensores sobre el mismo sitio, los mismos puntos y la misma marea, el balance es el siguiente. En NISAR HH, ρ es de 0,83 y 0,74, en ALOS-2 HH es de 0,65 y 0,72 y en Sentinel-1 VV es de −0,18 y −0,13. Dos sensores de banda L con geometría y hora de paso distintas coinciden, y en ambos la respuesta está en la polarización paralela y no en la cruzada, que es la firma del doble rebote.

La comparación sigue sin separar del todo polarización de longitud de onda, pues la banda C se observa en VV y la banda L en HH. Aun así, la coherencia entre los dos sensores de banda L y la ausencia de respuesta en HV refuerzan la lectura física.

![Figura 8. Retrodispersión de ALOS-2 PALSAR-2 en banda L del manglar y del bosque frente a la altura de marea a la hora de cada pasada, por trayectoria. Como en NISAR, el HH y el HH − HV del manglar suben con la marea y el bosque no.](fig_alos2_marea.png)

### 3.5 La Ciénaga Grande: lluvia como forzante

La Figura 9 presenta dos pasadas de NISAR de la traza descendente 083, ambas de la colección Beta, y la diferencia de HH entre ellas. La primera corresponde al río Magdalena alto (4 de diciembre de 2025, 2,67 m en Remolino) y la segunda al río más bajo (9 de enero de 2026, 1,69 m). Sobre el manglar de consenso, la diferencia tiene una mediana de +0,43 dB, con el 50 % central entre −0,42 y +1,28 dB. Por lo tanto, el aumento con el río alto existe pero no es uniforme, puesto que en una cuarta parte del manglar la señal baja en lugar de subir.

La gran mancha negativa sobre la laguna no es inundación sino rugosidad del agua abierta, que depende del viento en el momento de la pasada. Las pasadas con el río más bajo, entre 0,9 y 1,4 m, pertenecen a la colección Provisional. Estas pasadas no se restaron, con el fin de no mezclar el cambio de calibración con el cambio de nivel.

![Figura 9. σ⁰ de NISAR GCOV sobre la CGSM, traza descendente 083, colección Beta (R = HH, G = HV, B = HH − HV): (a) 4 de diciembre de 2025, río Magdalena a 2,67 m; (b) 9 de enero de 2026, río a 1,69 m; (c) diferencia de HH, (a) menos (b). Contorno amarillo o negro: manglar cartografiado por WorldCover y GMW; línea blanca o negra: área de estudio. La mancha negativa sobre la laguna abierta refleja la rugosidad de la superficie por el viento, no inundación.](fig_cgsm_radar.png)

Como referencia óptica, la Figura 10 coloca junto a esas dos pasadas los compuestos de Sentinel-2 (Drusch et al., 2012) de las mismas fechas, en color natural (B4, B3, B2) y en infrarrojo color (B8, B4, B3). Cada compuesto es la mediana de las diez adquisiciones a menos de diez días de la pasada, enmascaradas con Cloud Score+ (Pasquarella et al., 2023).

En el óptico, el manglar no cambia entre las dos fechas. Su NDVI mediano es de 0,855 con el río alto y de 0,867 con el río más bajo, y el agua abierta (MNDWI mayor que cero) ocupa el 39,7 % y el 39,2 % del área válida del AOI. Por lo tanto, el descenso de un metro en el río no se traduce en un cambio visible de la lámina de agua.

El óptico separa bien el agua abierta, el humedal herbáceo, el manglar cerrado y el bosque seco, y por eso sirve de apoyo a la clave de interpretación. Sin embargo, no separa la frontera entre manglar degradado y humedal (separabilidad 0,44 con el NDVI de la muestra de 2025). Tampoco registra el agua bajo el dosel, que es donde la banda L aporta la señal de la Figura 9. En Bahía de Málaga esta comparación no es posible, puesto que entre enero de 2025 y septiembre de 2026 solo ocho imágenes tienen más del 30 % del área despejada.

![Figura 10. Vistas óptica y de banda L de la CGSM en las dos fechas de la Figura 9. Filas: 4 de diciembre de 2025 (río Magdalena a 2,67 m) y 9 de enero de 2026 (1,69 m). Columnas: Sentinel-2 en color natural (B4, B3, B2) e infrarrojo color (B8, B4, B3), mediana de las diez adquisiciones dentro de los diez días de cada pasada, enmascarada con Cloud Score+, donde los huecos blancos son píxeles sin observación libre de nubes; y compuestos de la traza 083 de NISAR (R = HH, G = HV, B = HH − HV). Contorno amarillo: manglar cartografiado por WorldCover y GMW; línea blanca: área de estudio.](fig_cgsm_optico_radar.png)

Tabla 7. Sentinel-1 en la CGSM: correlación de Spearman entre la lluvia de treinta días y la retrodispersión, por órbita.

| Órbita (hora local, n) | Clase | VV | VH | VV−VH |
|---|---|---|---|---|
| 77 ascendente (18:06, 58) | Manglar | ρ 0,32, p 0,01 | ρ 0,14, p 0,31 | ρ 0,25, p 0,06 |
| 77 ascendente (18:06, 58) | Bosque | ρ 0,52, p < 0,001 | ρ 0,21, p 0,12 | ρ 0,38, p 0,003 |
| 77 ascendente (18:06, 58) | Manglar − bosque | ρ −0,35, p 0,01 | ρ −0,13, p 0,35 | ρ −0,17, p 0,19 |
| 142 descendente (05:48, 61) | Manglar | ρ 0,21, p 0,11 | ρ 0,18, p 0,17 | ρ −0,04, p 0,74 |
| 142 descendente (05:48, 61) | Bosque | ρ 0,58, p < 0,001 | ρ 0,41, p 0,001 | ρ 0,50, p < 0,001 |
| 142 descendente (05:48, 61) | Manglar − bosque | ρ −0,52, p < 0,001 | ρ −0,34, p 0,01 | ρ −0,44, p < 0,001 |

El resultado informa más sobre el diseño que sobre el manglar. En la CGSM, el bosque de referencia no funciona como control, puesto que su VV sube con la lluvia con más fuerza que el del manglar (ρ de 0,52 y 0,58 frente a 0,32 y 0,21). La explicación más probable es que, como bosque seco de los piedemontes, se humedece y recupera follaje con las lluvias, aunque no se comprobó con una serie de NDVI. Así, la resta manglar menos bosque sale negativa, y eso no es evidencia de inundación en ningún sentido. Puesto que en banda C la lluvia mueve la humedad de toda la vegetación, con un control caducifolio la prueba no separa la inundación bajo dosel de la humedad general.

Por lo tanto, en la ciénaga el diseño debe cambiar en dos puntos. En primer lugar, la variable hidrológica debe ser el nivel del agua, a partir de las estaciones de INVEMAR o del pulso del río, y no la lluvia. En segundo lugar, el control debe ser vegetación perenne que no se inunde, que dentro del AOI casi no existe. Por esta razón, la prueba fuerte del sitio es la resta manglar menos bosque en banda L con NISAR (Tabla 8, Figura 11), que descuenta lo que el control comparte con el manglar.

Tabla 8. NISAR en la CGSM, traza descendente 083 (18:27 hora local, 12 pasadas, 8 de época húmeda): correlación de Spearman con la lluvia de treinta días y diferencia húmeda menos seca según el calendario.

| Clase | HH | HV | HH−HV | HH, húmeda − seca (dB) |
|---|---|---|---|---|
| Manglar | ρ 0,50, p 0,10 | ρ −0,26, p 0,42 | ρ 0,54, p 0,07 | −0,15 |
| Bosque | ρ 0,02, p 0,95 | ρ −0,34, p 0,29 | ρ 0,29, p 0,35 | +0,26 |
| Manglar − bosque | ρ 0,58, p 0,05 | ρ 0,26, p 0,42 | ρ 0,39, p 0,22 | −0,44 |

En banda L el resultado cambia en dos puntos. En primer lugar, el bosque seco deja de responder a la lluvia (ρ 0,02 en HH frente a 0,52 y 0,58 en el VV de Sentinel-1), de modo que en NISAR sí funciona como control. En segundo lugar, el HH del manglar sube con la lluvia (ρ 0,50) y la resta manglar menos bosque da ρ 0,58 con p 0,05, mientras que la polarización cruzada no responde (ρ 0,26, p 0,42). Se trata de la misma firma que en Bahía de Málaga: sube la copolar y no la cruzada, y el control no se mueve.

La diferencia húmeda menos seca por calendario sale con el signo contrario (−0,44 dB), puesto que el calendario no sigue a la lluvia en este periodo. Las pasadas de "época seca" de diciembre y enero tuvieron entre 90 y 193 mm de lluvia antecedente, y las de "época húmeda" de junio a septiembre de 2026 entre 51 y 151 mm. Por lo tanto, la partición por época no ordena las pasadas por humedad, y la correlación con la lluvia medida es el estadístico que corresponde leer.

El resultado proviene de doce pasadas, usa una lluvia promediada sobre el AOI como sustituto del nivel del agua y tiene un p de 0,05 en el borde, que además no resiste la corrección por dependencia temporal de la Tabla 10 (p entre 0,21 y 0,25). Por esta razón, se reporta como una dirección coherente con el sitio mareal y no como una medida. La confirmación exige el nivel del agua de INVEMAR y las pasadas que la traza 083 siga añadiendo cada doce días.

![Figura 11. CGSM: retrodispersión del manglar y del bosque frente a la lluvia acumulada de los 30 días previos, por sensor y traza. En banda C (Sentinel-1) las dos clases se aclaran con la lluvia, el bosque seco más que el manglar; en banda L (NISAR, traza D083) el bosque no responde y el copolar del manglar sube con la lluvia. ALOS-2 y la traza A007 de NISAR tienen muy pocas pasadas para evaluar.](fig_cgsm_temporada.png)

### 3.6 La Ciénaga Grande: nivel del río Magdalena

Tabla 9. Retrodispersión frente al nivel del río Magdalena en Remolino: diferencia entre el tercio de nivel alto y el de nivel bajo (dB) y correlación de Spearman, por sensor y traza. En Sentinel-1 entran 55 y 58 de las 58 y 61 pasadas: las tres restantes por órbita caen en un hueco de 18 días de la serie del IDEAM (12 a 30 de agosto de 2026).

| Sensor y pasada | n | Clase | Copolar (HH o VV) | Cruzada (HV o VH) | Cociente (HH−HV) |
|---|---|---|---|---|---|
| NISAR D083 (18:27) | 14 | Manglar | +0,47 dB · ρ 0,58, p 0,03 | −0,97 dB · ρ −0,74, p 0,003 | +1,27 dB · ρ 0,77, p 0,001 |
| NISAR D083 (18:27) | 14 | Bosque | −0,53 dB · ρ −0,39, p 0,16 | −1,29 dB · ρ −0,70, p 0,006 | +0,71 dB · ρ 0,71, p 0,005 |
| NISAR D083 (18:27) | 14 | Manglar − bosque | +0,83 dB · ρ 0,83, p < 0,001 | +0,35 dB · ρ 0,32, p 0,27 | +0,62 dB · ρ 0,49, p 0,08 |
| NISAR A007 (05:31) | 7 | Manglar − bosque | −0,14 dB · ρ −0,04, p 0,94 | −0,06 dB · ρ −0,39, p 0,38 | −0,30 dB · ρ −0,54, p 0,22 |
| Sentinel-1 A77 (18:06) | 55 | Manglar − bosque | −0,21 dB · ρ −0,47, p < 0,001 | +0,05 dB · ρ −0,01, p 0,95 | −0,08 dB · ρ −0,12, p 0,37 |
| Sentinel-1 D142 (05:48) | 58 | Manglar − bosque | −0,21 dB · ρ −0,33, p 0,01 | −0,14 dB · ρ −0,37, p 0,005 | −0,15 dB · ρ −0,18, p 0,18 |

Con el nivel del río, la señal de banda L se hace más nítida que con la lluvia. Con las catorce pasadas disponibles al 7 de octubre, el HH del manglar sube 0,47 dB entre el tercio bajo y el alto (ρ 0,58), y el del bosque no (ρ −0,39). La resta manglar menos bosque sube 0,83 dB con ρ 0,83 y p < 0,001, mientras que la cruzada del manglar relativa al bosque no responde (ρ 0,32). Las dos pasadas de septiembre, añadidas a las doce con que se hizo la primera versión, mantuvieron la dirección y subieron la resta de 0,70 a 0,83 dB.

La traza ascendente 007, con siete pasadas, todas de junio a septiembre de 2026, y el río entre 0,82 y 1,58 m, no muestra relación (ρ −0,04). Puesto que no tiene pasadas de nivel alto, no puede verla, y se reporta solo para dejar constancia de que la serie ascendente existe y crece. En banda C la resta sigue siendo negativa en las dos órbitas, porque el VV del bosque sube con el nivel (ρ 0,39 y 0,32) y el del manglar no. Se mantiene la misma firma de Bahía de Málaga, ahora con una variable medida en lugar de un sustituto (Figura 12).

Sin embargo, hay una limitación que impide leer este resultado como confirmación. Las catorce pasadas se reparten en dos bloques que coinciden con el nivel. Las ocho de nivel bajo (0,91 a 1,42 m) son todas de junio a septiembre de 2026, y las seis de nivel alto (1,69 a 2,67 m) son de octubre de 2025 a enero de 2026. Esto se debe a que en 2026 el río bajó mucho más que en 2025 para los mismos meses (media de agosto 0,96 m frente a 2,18 m).

Por lo tanto, el nivel está confundido con el periodo y con la versión del producto. Las seis pasadas altas son de la colección Beta y las ocho bajas de la Provisional. Las dos de septiembre, con el río entre 1,09 y 1,21 m, engrosaron el bloque bajo sin romper la confusión. El bosque de control protege en parte, puesto que un cambio de calibración entre versiones movería a las dos clases por igual y la resta lo cancela. El HH del bosque baja (−0,53 dB, Tabla 9), igual que el del agua abierta en el mapa (Tabla 15), mientras que el del manglar sube. No obstante, el HV baja en las dos clases con el nivel (ρ −0,74 y −0,70), lo que puede ser estacional o de versión y no se puede distinguir con catorce fechas.

La Tabla 10 cuantifica esa limitación. Puesto que el nivel y la señal cambian despacio y en bloque (autocorrelación de rezago 1 de 0,86 y 0,64), las catorce pasadas valen por cuatro o cinco observaciones independientes, y el valor p de 0,0003 pasa a estar entre 0,10 y 0,17. Dentro de cada versión, además, no hay relación con el nivel. En las seis pasadas Beta, con el río entre 1,69 y 2,67 m, la resta da ρ −0,14 (p 0,79), y en las ocho Provisionales, entre 0,91 y 1,42 m, ρ 0,55 (p 0,16). Una regresión de la resta sobre el nivel y un indicador de versión reparte 0,12 dB por metro al nivel y −0,52 dB a la versión. Por lo tanto, el ρ de 0,83 lo produce el escalón entre los dos bloques, y el efecto del nivel no es identificable con las pasadas actuales. Solo podrá evaluarse cuando la traza 083 acumule pasadas de nivel alto dentro de la colección Provisional.

![Figura 12. CGSM: retrodispersión del manglar y del bosque frente al nivel del río Magdalena en Remolino (IDEAM, horario) a la hora de la pasada, por sensor y traza. En banda L (NISAR D083) el copolar del manglar sube con el nivel del río y el bosque de control no; en banda C (Sentinel-1) sube el bosque y no el manglar. Las ocho pasadas de nivel bajo de NISAR son todas de junio a septiembre de 2026 y las seis de nivel alto de octubre de 2025 a enero de 2026.](fig_cgsm_nivel_rio.png)

### 3.7 Dependencia temporal de las correlaciones

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

El resultado central del avance resiste la corrección. En Bahía de Málaga, la marea en el instante de la pasada casi no se parece a la de la pasada anterior en NISAR (r1 de 0,15 y −0,03). Esto ocurre porque un muestreo cada doce días cae en fases distintas del ciclo mareal, de modo que el valor p apenas se mueve (0,007 y 0,008). La versión del producto tampoco explica ese resultado. Por fecha, las doce pasadas de cada traza se reparten en siete Beta y cinco Provisionales (A004) y seis y seis (D087), y dentro de cada bloque la resta sigue subiendo con la marea, con ρ de 0,89 y 0,90 en la traza ascendente y de 0,66 y 0,77 en la descendente.

En ALOS-2, cuyas adquisiciones sobre cada trayectoria se repiten cada 28 días y ese intervalo se acerca a un múltiplo del ciclo de mareas vivas y muertas, la marea muestreada sí se parece a la de la pasada anterior (r1 de 0,60 y 0,53). Por lo tanto, el tamaño efectivo baja a unas diez pasadas, y la relación se sostiene con p de 0,03 y 0,02.

En la Ciénaga Grande la corrección pesa más, puesto que la lluvia acumulada de treinta días es por construcción una serie muy suave (r1 de 0,89 en Sentinel-1, cuyas pasadas distan menos que la ventana de acumulación). Así, la relación de NISAR con la lluvia, que ya estaba en el borde con doce pasadas, deja de distinguirse del azar (p de 0,25). En Sentinel-1 la correlación negativa de la traza descendente, que la sección 3.5 atribuye al control, se sostiene (p de 0,009) y la ascendente no (p de 0,12).

La relación de NISAR con el nivel del río, que era la más nítida del sitio (ρ de 0,83, p de 0,0003 con catorce pasadas), es también la más afectada. Sus pasadas forman dos bloques de fechas, de modo que el tamaño efectivo cae a cinco y el valor p corregido es de 0,10, o de 0,17 si solo se usa el rezago 1.

Esta corrección no cambia la lectura de esas cifras, que el texto ya presenta como una dirección en el caso de la lluvia y como un efecto no identificable frente a la versión del producto en el caso del nivel del río. Sin embargo, sí fija cuánto falta. En la prueba con la lluvia, con un tamaño efectivo cercano a seis, NISAR necesita del orden del doble de pasadas para que una correlación de 0,58 sea distinguible. En la prueba con el nivel del río, con tamaño efectivo de cinco, lo que falta no son pasadas sino pasadas de nivel alto de la misma versión del producto.

Dos límites acompañan la tabla. En primer lugar, el tamaño efectivo se estima con series de doce a 63 pasadas, de modo que él mismo es incierto, sobre todo con n de 12. En segundo lugar, la corrección atiende la dependencia entre fechas y no la dependencia entre los píxeles que se promedian dentro de cada clase. Esta última no infla aquí el valor p, puesto que cada pasada entra como un solo número por clase.

### 3.8 Clave de interpretación por cobertura y mecanismo

Esta sección reúne lo medido en los dos sitios en una regla de lectura, y no en una descripción general. Cada cifra sale de las medianas por clase sobre los mismos 400 puntos por clase y las mismas pasadas de las secciones 3.5 y 3.6 (Tabla 11). A estas clases se suma la vegetación flotante, definida por su firma óptica.

Tabla 11. Firma de cada cobertura de la CGSM en las dos bandas: mediana entre pasadas del copolar, del cruzado y de su diferencia, en dB (la diferencia es la mediana de la resta por pasada, no la resta de las medianas). Banda C, Sentinel-1 traza descendente 142, 61 pasadas; banda L, NISAR traza descendente 083, 14 pasadas. La vegetación flotante no es una clase de los productos globales y se define por la firma óptica de diciembre de 2025, cuando el evento ya cubría el 55,7 % de la zona ZC-2025-v1, el polígono de vegetación flotante de 2025 delimitado sobre Sentinel-2 en el cubo de datos de la tesis.

| Cobertura | VV | VH | VV − VH | HH | HV | HH − HV |
|---|---|---|---|---|---|---|
| Agua abierta | −21,1 | −30,9 | 9,0 | −20,0 | −25,6 | 6,1 |
| Vegetación flotante | −13,3 | −20,7 | 7,5 | −16,6 | −23,3 | 6,6 |
| Humedal herbáceo | −9,9 | −15,2 | 5,3 | −9,2 | −17,5 | 7,9 |
| Manglar | −9,6 | −14,9 | 5,3 | −10,9 | −17,2 | 6,1 |
| Bosque seco (control) | −8,1 | −14,3 | 6,2 | −9,2 | −15,9 | 6,6 |

![Figura 13. Espacio de firmas de las coberturas de la CGSM en las dos bandas: retrodispersión copolar frente al cociente copolar menos cruzada, un punto por clase (mediana entre pasadas). En banda C el manglar y el humedal herbáceo caen en el mismo punto; en banda L se separan, mientras la vegetación flotante se desplaza hacia el agua abierta.](fig_clave_firmas.png)

La Figura 13 muestra el resultado principal de la clave: cada banda acerca a la separación un par distinto de clases. Por lo tanto, la elección de banda depende de qué confusión se quiera reducir y no de cuál banda sea mejor.

En banda C, el manglar y el humedal herbáceo caen en el mismo punto, con −9,6 y −9,9 dB en VV y 5,3 dB de diferencia entre polarizaciones en ambos. En banda L se apartan. El HH del humedal es 1,7 dB más brillante que el del manglar, y su diferencia HH − HV es 1,8 dB mayor, 7,9 frente a 6,1. Por lo tanto, la banda L aporta donde la banda C no distingue, que es exactamente la confusión que un informe previo del curso de Percepción Remota Avanzada, no publicado, encontró más difícil en el dominio óptico.

Con la vegetación flotante ocurre lo contrario. Frente al agua abierta, la mediana de la banda C se aparta 7,8 dB en VV y 10,2 en VH, mientras que la de la banda L se aparta solo 3,4 y 2,3 dB (Tabla 11). En la comprobación hecha con las 17 escenas de NISAR disponibles en septiembre, la diferencia fue positiva en todas, entre 2,5 y 7,8 dB.

La explicación física es la misma que sostiene el resto del trabajo, aplicada al revés. Con 5,6 cm de longitud de onda, las hojas y tallos de la vegetación flotante son dispersores del tamaño de la onda. Con 23 cm, en cambio, la capa flotante es delgada y la lámina de agua que queda debajo sigue dominando la señal. Por lo tanto, esa penetración, que es la ventaja de la banda L bajo el dosel del manglar, aquí actúa en contra.

Conviene no leer esas distancias entre medianas como separabilidad. La clase flotante es tan dispersa que, con la muestra de 2025, su separabilidad frente al agua queda en 0,47 en banda C y 0,28 en banda L (Tabla 13), por debajo de 1 en las dos. Frente al humedal herbáceo queda en 0,74 y 0,64. Por lo tanto, la banda C las aparta más, pero ninguna de las dos bandas las separa.

#### Validación con la muestra de referencia de 2025

Las firmas de la Tabla 11 salen de productos globales de 2020 y 2021, cuya clase menos confiable es el humedal herbáceo. Con el fin de comprobar la clave contra una referencia propia, se extrajo la firma de las dos bandas en los 720 puntos de la muestra de entrenamiento de la tesis (`clave_vs_muestra2025.py`). Estos puntos se etiquetaron a ciegas en seis clases sobre imagen de alta resolución de 2025. Los 400 primeros se revisaron bajo un criterio escrito, y los 320 restantes se etiquetaron con él.

Para la banda C se tomó la mediana de VV y VH de las 61 pasadas de la traza 142 de Sentinel-1 entre el 5 de octubre de 2025 y el 7 de septiembre de 2026. Para la banda L se tomó la mediana de HH y HV de las 14 escenas de la traza 083 de NISAR entre el 29 de octubre de 2025 y el 30 de septiembre de 2026. La extracción usó una ventana de 3 × 3 píxeles.

La Tabla 12 resume las firmas, y la Tabla 13 la separabilidad de Jeffries-Matusita (Richards, 2013) de cada par de clases con las tres variables de cada banda y con las seis juntas. Esta separabilidad se expresa en una escala de 0 a 2, donde por debajo de 1 no hay separación útil.

Tabla 12. Firma de cada clase de la muestra de referencia de 2025 en las dos bandas: mediana entre puntos de la mediana entre pasadas, en dB, con el rango intercuartil de la diferencia HH − HV. Banda C, Sentinel-1 traza 142, 61 pasadas; banda L, NISAR traza 083, 14 escenas.

| Clase | n | VV | VH | VV − VH | HH | HV | HH − HV | HH − HV, cuartiles |
|---|---|---|---|---|---|---|---|---|
| Agua | 212 | −21,5 | −29,6 | 7,5 | −19,9 | −25,4 | 5,9 | 5,0 a 6,5 |
| Vegetación flotante | 129 | −15,2 | −22,7 | 6,7 | −17,0 | −23,7 | 6,8 | 5,6 a 7,8 |
| Manglar intacto | 151 | −9,5 | −14,8 | 5,5 | −10,0 | −16,7 | 6,6 | 6,0 a 7,4 |
| Manglar degradado | 111 | −10,7 | −15,9 | 5,3 | −8,3 | −16,8 | 8,9 | 7,5 a 10,7 |
| Humedal herbáceo | 73 | −10,4 | −15,9 | 5,4 | −9,6 | −17,3 | 7,9 | 7,3 a 8,6 |
| Otro | 44 | −10,1 | −15,4 | 6,0 | −10,7 | −18,3 | 7,5 | 6,6 a 8,6 |

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

La muestra confirma una parte de la clave y corrige otra. En primer lugar, la banda L aporta donde la C no distingue, pero el par que más mejora no es el que la Tabla 11 sugería. Manglar intacto frente a manglar degradado pasa de 0,30 con banda C a 0,91 con banda L, todavía por debajo del umbral de 1 pero tres veces más. En cambio, humedal herbáceo frente a manglar queda en 0,22 con el degradado y en 0,76 con el intacto.

En segundo lugar, la diferencia HH − HV ordena las clases de dosel por su apertura y no por tipo de cobertura: manglar intacto 6,6, otro 7,5, humedal herbáceo 7,9 y manglar degradado 8,9 dB. Un dosel cerrado devuelve HV alto por dispersión de volumen y mantiene la diferencia baja. Cuando el dosel se abre, el HV cae y el HH sube por el suelo o la lámina expuestos, de modo que el manglar degradado queda del lado del humedal y no del manglar. Por lo tanto, el umbral de la versión preliminar de la clave, construida con las firmas de los productos globales,, que asignaba al humedal toda diferencia HH − HV cercana a 8 dB, enviaba al humedal 47 de los 111 puntos de manglar degradado.

En tercer lugar, el par humedal herbáceo frente a manglar degradado no se separa con ninguna banda ni con las dos juntas (0,38), lo mismo que ocurre con el NDVI de Sentinel-2 en la muestra (0,44). Se trata de la frontera que ni los sensores disponibles ni la referencia resuelven (sección 4.1), y se declara como límite. Finalmente, la vegetación flotante no tiene firma propia en radar. De sus 129 puntos, 42 caen en la firma del agua, y su separabilidad frente al agua está entre las más bajas de la tabla con ambas bandas (0,28 en L, 0,47 en C). Además, su rango intercuartil de VV va de −19,1 a −11,6 dB y cubre desde la lámina hasta el dosel.

#### Regla de lectura

La clave se reescribe con los umbrales medidos en la muestra de 2025. Se aplica en el orden que sigue, sobre la mediana de varias pasadas de la misma traza y no sobre una imagen suelta. Dos umbrales son puntos medios entre las medianas de las clases vecinas de la Tabla 12: −12 dB entre flotante e intacto en VV, y 7,3 dB entre intacto y humedal en HH − HV.

Los umbrales de agua (−17 y −25 dB) se conservan de esa versión preliminar, puesto que quedan entre el cuartil superior del agua (−18,2 y −25,5) y la mediana de la flotante (−15,2 y −22,7). El umbral de VV − VH (6,5 dB) está cerca de la mediana de la flotante (6,7) y por encima del cuartil superior de intacto, degradado y humedal (5,7 a 5,9) y cerca del de otro (6,7). La Tabla 14 muestra lo que la regla decide en los mismos 720 puntos con que se fijaron los umbrales, de modo que su acierto es de resustitución y no una estimación independiente.

1. VV por debajo de −17 dB con VH por debajo de −25 dB: superficie lisa, agua abierta. Acierta 159 de los 212 puntos de agua. Los 42 puntos de vegetación flotante que también caen aquí son la capa rala que el radar lee como lámina.
2. VV por debajo de −12 dB que no cumplió el paso 1: lámina con vegetación o borde de dosel. Con VV − VH de 6,5 dB o más es vegetación flotante (43 puntos, 27 de ellos de esa clase). Con VV − VH por debajo de 6,5 dB no hay decisión y se pasa al óptico. En este caso caen 92 puntos con VV entre −17 y −12, repartidos entre las seis clases y 38 de ellos marcados como borde. A ellos se suman 22 con VV por debajo de −17 pero VH de −25 o más, para un total de los 114 de la columna sin decisión de la Tabla 14.
3. VV de −12 dB o más con HH − HV por debajo de 7,3 dB: dosel cerrado, manglar intacto. Acierta 107 de 151. Los 32 intactos que superan el umbral tienen una diferencia mediana de 7,9 dB, dentro del rango del humedal y del manglar degradado, de modo que el radar los lee como dosel abierto.
4. VV de −12 dB o más con HH − HV de 7,3 dB o más: dosel abierto o herbáceo, donde caben el manglar degradado, el humedal herbáceo y las coberturas de la clase otro. La banda L no separa estas tres entre sí (Tabla 13, pares de 0,17 a 0,47), de modo que la clave entrega el grupo y deja la clase a la imagen de alta resolución o al óptico.
5. Para separar el manglar del bosque seco no basta el nivel de retrodispersión. La diferencia entre las dos clases, 1,5 dB en VV y 1,7 dB en HH (Tabla 11), es del orden de la que produce la geometría entre trazas (hasta 1,4 dB, Tabla 3). Por lo tanto, lo que los distingue es la respuesta hidrológica. Con el nivel del río Magdalena y catorce pasadas, el HH del manglar sube 0,47 dB entre el tercio de nivel bajo y el alto, con ρ 0,58, mientras que el del bosque baja 0,53 dB, con ρ −0,39 y sin significancia.
6. La firma de inundación bajo dosel es el copolar del manglar relativo al bosque: sube con el forzante en los dos sitios (+0,83 dB, ρ 0,83 con el nivel del río, y +0,57 dB, ρ 0,83 y 0,74 con la marea), mientras que el del bosque no. En Bahía de Málaga la cruzada no responde (ρ 0,11 y −0,06), lo que constituye la firma completa del doble rebote: gana el rebote entre troncos y lámina y no cambia el volumen del dosel. En la ciénaga la cruzada del manglar baja (−0,97 dB, ρ −0,74) y la diferencia HH − HV sube (+1,27 dB, ρ 0,77). Sin embargo, el bosque y el agua abierta hacen lo mismo (Tabla 9, Tabla 15), de modo que allí esas dos señales están mezcladas con la versión del producto o con la estación y no se usan como firma. En banda C el copolar relativo al bosque da el signo contrario, puesto que el VV responde a la humedad del dosel y del suelo y no al agua bajo el dosel.

Tabla 14. Lo que la regla decide en los 720 puntos de la muestra de 2025 (filas, clase de referencia; columnas, pasos 1 a 4 de la regla). La regla decide en 606 puntos y acierta en 415, el 68 % de los decididos y el 58 % de los 720, con un 16 % sin decisión y con las tres clases de dosel abierto agrupadas; sin los 208 puntos marcados como borde decide en 444 de 512 y acierta en el 71 %.

| Clase de referencia | 1 Agua abierta | 2 Vegetación flotante | 3 Manglar intacto | 4 Dosel abierto o herbáceo | Sin decisión |
|---|---|---|---|---|---|
| Agua | **159** | 7 | 5 | 5 | 36 |
| Vegetación flotante | 42 | **27** | 14 | 25 | 21 |
| Manglar intacto | 0 | 0 | **107** | 32 | 12 |
| Manglar degradado | 2 | 4 | 19 | **62** | 24 |
| Humedal herbáceo | 3 | 2 | 11 | **40** | 17 |
| Otro | 2 | 3 | 15 | **20** | 4 |

### 3.9 Mapa de la señal y corroboración óptica

La prueba del nivel del río entrega un número por clase. Con el fin de ver dónde aparece la señal, la misma comparación se llevó al píxel (`mapa_doble_rebote.py`). Respecto de la Tabla 9 hay dos diferencias, y ambas explican por qué sus cifras no coinciden.

La primera es el reparto. En lugar de los tercios de nivel, que dejan cuatro o cinco pasadas por grupo, el mapa usa todas las pasadas en los dos bloques de fechas, seis de nivel alto (1,69 a 2,67 m) y ocho de nivel bajo (0,91 a 1,42 m), con el fin de que la mediana por píxel tenga más pasadas y menos moteado. Esa diferencia de reparto, junto con la de extensión que sigue, explica que el manglar completo dé +0,07 dB aquí y +0,47 dB en la Tabla 9.

La segunda es la extensión. El mapa cubre la caja del cubo (4.304 km²) más un margen de 2 km, unos 4.900 km², no solo el AOI de 2.042 km². Por lo tanto, entran 36.350 ha de manglar de consenso frente a las 33.173 ha del AOI, y el bosque de control de los piedemontes queda dentro.

Las catorce escenas de la traza 083 se convirtieron a σ⁰ y se agregaron a 50 m por media de bloques de 5 × 5 píxeles en potencia. Posteriormente, se tomó la mediana de cada grupo. La diferencia alto menos bajo de HH, HV y HH − HV se escribió como GeoTIFF (`mapa_doble_rebote_50m.tif`), junto con la máscara de clases de WorldCover y GMW sobre la misma malla. La Figura 14 muestra las tres diferencias sobre el manglar y el bosque de control. La Tabla 15 las resume por clase y, para el manglar, por sector de norte a sur.

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

![Figura 14. NISAR D083 sobre la CGSM a 50 m: cambio de HH, HV y HH − HV entre la mediana de las seis pasadas de nivel alto del río (octubre de 2025 a enero de 2026) y la mediana de las ocho de nivel bajo (junio a septiembre de 2026). Manglar en color pleno, bosque de control atenuado, otras coberturas en gris; las líneas punteadas marcan los sectores de la Tabla 15. El aumento de HH se concentra en el manglar del sur, en la desembocadura del río Fundación, y se desvanece hacia el norte; el HV baja cerca de 1,1 dB en todas las coberturas, incluida el agua abierta.](fig_mapa_doble_rebote.png)

El mapa añade dos cosas que el número por clase no decía. En primer lugar, la señal tiene estructura espacial. El aumento de HH se concentra en el manglar del sur (mediana +0,53 dB, 77 % de los píxeles positivos) y es nulo en el centro. En Isla de Salamanca, al norte, donde entra el caño Clarín, el aumento se invierte (−0,18 dB, 40 %). Cruzado con los cauces con nombre de OpenStreetMap, el foco del sur (este 555 a 565 km, mediana +0,67 dB, 85 % de píxeles positivos) coincide con la desembocadura del río Fundación, que baja de la Sierra Nevada, y no con la entrada de los caños del Magdalena: el caño Renegado termina al occidente, a 11 km del manglar, en una franja donde el cambio es menor (+0,09 a +0,25 dB), y el Clarín entra por el norte. Por lo tanto, en ese sector el nivel del Magdalena en Remolino actúa como índice regional de la temporada y no como el forzante directo. Hay también una franja positiva en la orilla oriental, entre 575 y 580 km de este y 1195 y 1210 km de norte, que los sectores por latitud no aíslan.

Ese gradiente es compatible con agua fluvial bajo el dosel, pero no señala al Magdalena en particular. Además, los sectores se trazaron por latitud antes de verificar la hidrografía, de modo que la lectura por sector es una hipótesis para la serie siguiente y no un resultado. Por otra parte, el humedal herbáceo, que no tiene dosel, sube casi lo mismo que el sector sur del manglar (+0,46 dB), lo que recuerda que el HH también responde al suelo y a la lámina expuesta.

Además, el mapa hereda el confundido de la Tabla 9, con los grupos de nivel coincidentes con las dos versiones del producto, de modo que lo que muestra es la estructura espacial de una dirección coherente, no una confirmación.

En segundo lugar, el HV baja entre 0,96 y 1,21 dB en todas las clases, incluida el agua abierta, donde no hay dosel que inundar. Un cambio idéntico en el agua no puede ser inundación. Se trata de un desplazamiento entre las dos versiones del producto (las seis pasadas altas son Beta y las ocho bajas Provisional) o de un efecto estacional de la humedad, y esto explica por qué Δ(HH − HV) sale positivo hasta en el bosque de control.

Por lo tanto, lo que se puede leer del mapa no está en la diferencia entre polarizaciones sino en el HH del manglar relativo al bosque. En el manglar completo son +0,07 dB frente a −0,36 dB del control (resta +0,43), y en el sur son +0,53 dB frente a −0,36 (resta +0,89).

Con el fin de que la comparación entre bandas sea también espacial, el mismo mapa se construyó con Sentinel-1 en banda C (`mapa_doble_rebote_s1.py`). Se tomó la mediana de VV y VH de las pasadas de la órbita descendente 142 en las mismas dos ventanas de fechas, 13 de nivel alto y 18 de nivel bajo, promediadas a 50 m sobre la misma malla. La Figura 15 pone los dos copolares lado a lado y la Tabla 15 añade sus cifras.

En banda C el cambio es pequeño y difuso. El manglar sube 0,09 dB (61 % de píxeles positivos) y el bosque de control sube más, 0,36 dB con el 86 % de los píxeles positivos, de modo que la resta manglar menos bosque es negativa, como en la Tabla 9. La banda C registra sobre todo la humedad estacional del suelo y del dosel, que el bosque seco acusa más que el manglar.

En banda L, en cambio, la resta es positiva (+0,07 frente a −0,36) y la señal tiene estructura. El sector sur sube 0,53 dB en HH frente a 0,21 en VV, y la correlación por píxel entre los dos cambios sobre el manglar es débil (ρ 0,21). Esa correlación por píxel no se somete a prueba, por la autocorrelación espacial, pero su valor bajo indica que los dos cambios no comparten el mismo patrón. Esa es la forma espacial del resultado de la Tabla 9.

![Figura 15. El mismo cambio alto menos bajo del nivel del río en las dos bandas sobre la malla de 50 m: HH de banda L de NISAR D083 (6 pasadas altas, 8 bajas) y VV de banda C de Sentinel-1, órbita 142 (13 altas, 18 bajas en las mismas ventanas de fechas). Manglar en color pleno, bosque de control atenuado. En banda L el aumento se concentra en el manglar del sur y el bosque baja; en banda C el cambio es pequeño, el bosque sube más que el manglar y la correlación por píxel entre las dos bandas sobre el manglar es débil (ρ 0,21).](fig_mapa_c_vs_l.png)

Como corroboración óptica se usó la clase de vegetación inundada de Dynamic World (Brown et al., 2022), que da por píxel de 10 m la probabilidad de vegetación con agua visible. Se usaron las 105 fechas de Sentinel-2 entre octubre de 2025 y septiembre de 2026 con alguna cobertura del AOI (`corroboracion_dw.py`). Sobre ellas se hicieron dos pruebas, una temporal y una espacial.

En la prueba temporal, la probabilidad media sobre cada clase en las 54 fechas con al menos la mitad del manglar sin nubes se correlacionó con el nivel del río del día. En el humedal herbáceo la relación existe (ρ 0,41, p 0,002). Ese valor no está corregido por dependencia temporal, que con un río de autocorrelación 0,86 la haría menos nítida.

En el bosque, en cambio, no hay relación (ρ −0,02). Sobre el manglar tampoco (ρ 0,04, p 0,79), con una media de 0,197 en las fechas de nivel alto frente a 0,191 en las de nivel bajo. Así, el óptico ve la inundación solo donde no hay dosel y apoya que el nivel del río es un forzante del humedal.

En la prueba espacial, la diferencia alto menos bajo de la probabilidad de Dynamic World se cruzó con el ΔHH de NISAR píxel a píxel (Figura 16), en la misma malla de 50 m y con al menos dos fechas válidas por grupo. Sobre el manglar la correlación es débil y negativa (ρ −0,15). Donde el óptico ve más agua con el río alto el HH baja (−0,38 dB en los píxeles con ΔDW > 0,1), mientras que donde el óptico no ve cambio el HH sube.

Esa lectura, formulada después de ver el dato, es coherente con los mecanismos. En los claros del manglar el agua queda expuesta, el óptico la detecta y el radar la ve como superficie lisa que baja el HH. Bajo el dosel cerrado, en cambio, el óptico no ve nada y el doble rebote entre troncos y lámina sube el HH. En consecuencia, Dynamic World apoya el forzante y es compatible con la complementariedad de los sensores. Sin embargo, no corrobora la señal bajo dosel en sí, que por definición queda fuera de lo que el óptico puede ver, y una correlación de −0,15 es una compatibilidad, no una prueba.

![Figura 16. Contraste óptico con la probabilidad de vegetación inundada de Dynamic World. Izquierda: probabilidad media sobre manglar y humedal herbáceo en las 54 fechas sin nubes frente al nivel del río en Remolino; el humedal sigue al río (ρ 0,41), el manglar no (ρ 0,04). Centro: cambio de la probabilidad entre fechas de nivel alto y bajo sobre la malla de 50 m. Derecha: ese cambio frente al ΔHH de NISAR en los píxeles de manglar (ρ −0,15): donde el óptico ve más agua expuesta el HH baja, y el aumento de HH ocurre donde el óptico no ve cambio.](fig_corroboracion_dw.png)

El mismo mapa se construyó en Bahía de Málaga con la marea como forzante (`mapa_doble_rebote_malaga.py`). Por traza, se calculó la mediana de las seis pasadas de marea más alta menos la mediana de las seis de marea más baja, sobre la malla de 50 m de cada traza (Tabla 16, Figura 17). En las dos trazas, de forma independiente, el manglar queda por encima del bosque de control. En la ascendente el HH del manglar sube +0,34 dB con el 75 % de los píxeles positivos y el del bosque baja −0,10. En la descendente el manglar apenas cambia (+0,05, 54 % positivos) y es el bosque el que baja (−0,39). Esa caída coincide con la versión del producto: en esa traza cuatro de las seis pasadas de marea alta son Beta y cuatro de las seis de marea baja son Provisionales, y la versión desplaza el HH de todas las clases, de modo que la resta cancela ese desplazamiento y no describe una caída real del bosque. Así, la resta manglar menos bosque es de +0,44 dB en ambas, del orden de los +0,57 dB de la Tabla 4.

El HV baja en todas las clases, agua incluida, como en la ciénaga, de modo que tampoco aquí se usa como firma. La señal positiva de HH se reparte por las franjas de manglar de toda la bahía y no se concentra en un sector. Esto es coherente con un forzante, la marea, que entra por todos los bordes a la vez. Por último, en la traza descendente la esquina noroccidental muestra un bloque negativo en HH y HV que coincide con el borde de la franja, y se trata como artefacto de cobertura hasta comprobarlo.

Tabla 16. Bahía de Málaga: diferencia marea alta menos marea baja por píxel de 50 m (mediana y cuartiles, dB) y fracción de píxeles positivos, por traza y clase. Seis pasadas por grupo en cada traza; el humedal herbáceo tiene solo 224 píxeles y se omite.

| Traza | Clase | Píxeles | ΔHH | ΔHH > 0 | ΔHV | Δ(HH − HV) |
|---|---|---|---|---|---|---|
| A004 (05:46) | Manglar | 34.344 | +0,34 (−0,01 a +0,69) | 75 % | −0,36 | +0,70 |
| A004 (05:46) | Bosque (control) | 300.038 | −0,10 (−0,36 a +0,17) | 40 % | −0,34 | +0,25 |
| A004 (05:46) | Agua | 214.339 | −0,07 (−0,45 a +0,30) | 45 % | −0,51 | +0,43 |
| D087 (18:29) | Manglar | 34.344 | +0,05 (−0,35 a +0,42) | 54 % | −0,53 | +0,64 |
| D087 (18:29) | Bosque (control) | 300.038 | −0,39 (−0,79 a −0,06) | 21 % | −0,63 | +0,32 |
| D087 (18:29) | Agua | 214.339 | −0,42 (−0,90 a +0,05) | 27 % | −0,94 | +0,63 |

![Figura 17. Bahía de Málaga a 50 m: cambio de HH (izquierda) y HV (derecha) entre la mediana de las seis pasadas de marea más alta y las seis de marea más baja de cada traza de NISAR, A004 (arriba) y D087 (abajo). Manglar en color pleno, bosque de control atenuado. El HH sube en las franjas del manglar en las dos trazas y el bosque no; el HV baja en todas las coberturas. El bloque negativo de la esquina noroccidental de D087 coincide con el borde de la franja y se trata como artefacto de cobertura.](fig_mapa_doble_rebote_malaga.png)


## 4. Discusión

La pregunta era qué aporta la banda L frente a la C para identificar inundación bajo el dosel del manglar, y la respuesta tiene dos partes. En primer lugar, con el forzante hidrológico, el copolar del manglar relativo al bosque sube cuando sube el agua en los dos sitios con NISAR y, en Málaga, también con ALOS-2. En banda C no sube: en Málaga no responde y en la ciénaga la resta baja, puesto que el VV responde a la humedad del dosel y del suelo y no al agua bajo el dosel. En Bahía de Málaga esa dirección resiste la corrección por dependencia temporal. En la Ciénaga Grande no la resiste, debido a los bloques de fechas y de versión del producto. El tamaño del efecto, entre 0,4 y 0,8 dB en la resta manglar menos bosque, queda muy por debajo de los realces de varios decibelios que Hess et al. (1990) reunieron para bosques inundados en banda L. Esa diferencia es coherente con tres condiciones de este caso: un dosel de manglar denso que atenúa el doble rebote, una inundación que no cubre todo el píxel de 10 m y, en la ciénaga, pasadas que promedian estados de agua distintos. También lo es con la polarización dual, que impide aislar el doble rebote por la fase entre HH y VV, lo que exige datos polarimétricos completos. Los mapas de Málaga (Tabla 16) muestran que la resta por traza, +0,44 dB, está en el mismo orden que la de los puntos, y que en la traza descendente la produce el bosque que baja y no el manglar que sube.

En segundo lugar, con las coberturas, la banda L aparta pares que la C deja juntos, sin llegar a separarlos, sobre todo manglar intacto frente a degradado, y lo que mide la diferencia HH − HV es la apertura del dosel. Sin embargo, la frontera entre manglar degradado y humedal herbáceo no la resuelve ningún sensor.

El mapa a 50 m muestra que la señal de banda L tiene estructura espacial, concentrada en la desembocadura del río Fundación, al sur, y no en la entrada de los caños del Magdalena. La de banda C, en cambio, es pequeña y difusa, sube más en el bosque de control que en el manglar, y también crece hacia el sur (+0,21 dB con el 74 % de los píxeles positivos frente a +0,05 al norte), con el mismo orden espacial que la banda L y menos de la mitad de su amplitud. Finalmente, Dynamic World ve el río en el humedal sin dosel y no en el manglar, lo que apoya el forzante y la complementariedad, no la señal bajo dosel en sí.

### 4.1 Límites

Los productos disponibles son de polarización dual, HH y HV en banda L y VV y VH en banda C. Por lo tanto, no se puede aplicar una descomposición polarimétrica, y los mecanismos se infieren de los niveles y de su respuesta hidrológica. Además, Sentinel-1 no tiene HH sobre la zona, de modo que la comparación entre bandas mezcla longitud de onda y polarización. Las cifras de banda L en la ciénaga descansan en 14 pasadas de una sola traza, con los tercios de nivel repartidos entre versiones distintas del producto.

La validación tiene dos límites propios. En primer lugar, los umbrales se fijaron y se evaluaron sobre los mismos 720 puntos, así que el 68 % de la Tabla 14 es un acierto de resustitución. La estimación independiente corresponde a la muestra de validación de la tesis, que todavía no existe. En segundo lugar, las pasadas de radar van de octubre de 2025 a septiembre de 2026 y las etiquetas describen la imagen de 2025. Por lo tanto, una parte del desacuerdo puede ser cambio real y no error de la clave, sobre todo en la vegetación flotante, que es un evento en curso.

Por último, la referencia tiene su propia incertidumbre. En una segunda pasada a ciegas de 60 puntos, siete días después de la primera y sin criterio escrito, la intérprete coincidió consigo misma en el 75 % [63 a 84 %] de los puntos (kappa 0,69). Bajo el criterio escrito, en una segunda pasada a ciegas de otros 60 puntos sorteados entre los 720 y hecha el 14 de octubre, siete días después de la última sesión de etiquetado, la intérprete coincidió con la clase de referencia en el 78 % [66 a 87 %] de los puntos, con kappa 0,72 (Figura 18). Manglar intacto y degradado se repitieron en todos sus puntos (14 de 14 y 6 de 6), el agua en 15 de 17 y la vegetación flotante en 7 de 11. El humedal herbáceo, en cambio, solo se repitió en 2 de 7: tres pasaron a manglar intacto y dos a agua, con una n demasiado pequeña para una cifra por clase. Por lo tanto, la referencia tiene una inconsistencia cercana al 22 % que acota lo que la clave puede alcanzar, aunque no se midió qué fracción del desacuerdo de la Tabla 14 cae en puntos inconsistentes, y la clase donde esa incertidumbre se concentra es la misma que ningún sensor separa.

![Figura 18. Consistencia de la intérprete sobre la referencia de 2025: confusión entre la etiqueta de referencia (clase_final, criterio escrito) y una segunda pasada a ciegas de la misma intérprete sobre 60 puntos sorteados entre los 720 (semilla fijada en septiembre), siete días después de la última sesión de etiquetado. Acuerdo 0,78 [0,66 a 0,87], kappa 0,72. Manglar intacto y degradado se repiten en todos sus puntos; el humedal herbáceo se repite en 2 de 7.](fig_consistencia_2025.png)

## 5. Conclusiones y trabajo futuro

La banda L muestra en Bahía de Málaga, con dos sensores y dos trazas, una respuesta del copolar del manglar a la marea que la banda C no muestra, compatible con el doble rebote entre troncos y lámina de agua, y esa respuesta se mantiene dentro de cada versión del producto de NISAR. En la Ciénaga Grande, en cambio, el cambio entre pasadas de río alto y bajo coincide con el cambio de versión y dentro de cada versión no hay relación con el nivel, de modo que allí el efecto no es identificable todavía. La clave de interpretación queda contrastada con una referencia propia, con un acierto de resustitución del 68 %, y declara con cifras qué aparta cada banda y qué no separa ninguna.

En primer lugar, se debe repetir la prueba de NISAR contra el nivel del río a medida que la traza 083 añada pasadas de la colección Provisional, hasta que los dos tercios de nivel contengan fechas de la misma versión del producto. Asimismo, se deben obtener de INVEMAR, ya solicitadas, las lecturas diarias de nivel de los caños y de la ciénaga del monitoreo hidrosedimentológico, que miden el agua dentro del humedal y no en el río.

En segundo lugar, se debe repetir el mapa de la Figura 14 con grupos de nivel tomados de una sola versión del producto, con el fin de separar el desplazamiento del HV de la señal del HH. La corroboración de Dynamic World en Bahía de Málaga queda limitada a las 8 imágenes con más del 30 % del área despejada, todas entre febrero y julio de 2026, que es lo que ese sitio permite.

En tercer lugar, se debe estimar el acierto de la clave con una muestra independiente de los 720 puntos que fijaron sus umbrales, que será la muestra de validación de la tesis. Además, se debe repetir la validación de la clave con etiquetas del mismo año que el radar, sea con la muestra de validación de 2026 o restringiendo la extracción a las pasadas de 2025.

Finalmente, queda una vía que ninguno de los tres sensores permite. Con polarización dual no hay fase entre HH y VV, y el doble rebote se infiere del nivel de HH frente al bosque de control. Una escena polarimétrica completa de banda P de BIOMASS sobre la ciénaga permitiría verlo de forma directa en la componente HH − VV de la base de Pauli y en la fase copolar, como se hizo en la práctica del curso sobre Camboya. Su disponibilidad sobre el sitio no se ha verificado.

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
