# Auditoría independiente de los cálculos de `Avance_proyecto_radar.md`

Fecha de la auditoría: 16 de septiembre de 2026.
Documento auditado: `C:\LINA\UNAL 2626-1\RADAR\Avance_proyecto_radar.md` (versión del 13/09/2026 14:35).

## Alcance y método

Se rederivó cada número de las Tablas 1 a 9 y de los párrafos que las acompañan a partir de
los CSV crudos de la carpeta, con código propio en pandas, numpy y scipy, sin leer ni ejecutar
ninguno de los scripts `*.py` que produjeron las tablas. Los CSV de resumen
(`marea_vs_radar.csv`, `s1_marea_resumen.csv`, `alos2_marea_resumen.csv`,
`cgsm_temporada_resumen.csv`, `cgsm_nivel_rio_resumen.csv`, `doble_rebote_incidencia.csv`)
se usaron solo como término de comparación posterior, nunca como insumo.

Tolerancias aplicadas: 0,01 en ρ; 0,005 en p; 0,05 dB en diferencias; 1 en conteos.

Reglas estadísticas reimplementadas de cero:

- Mediana por clase y pasada: mediana de las medianas por pasada.
- Desviación estándar entre fechas: muestral (ddof = 1) sobre las medianas por pasada.
- "Alta menos baja" de las Tablas 4, 5 y 6: partición por la mediana de la marea dentro de
  cada traza, diferencia de medianas de los dos grupos.
- "Tercio alto menos tercio bajo" de la Tabla 9: k = n // 3 elementos en cada extremo, tras
  ordenar por nivel del río.
- ρ de Spearman con `scipy.stats.spearmanr` sobre las n pasadas de la traza, con su p asintótico.
- Interpolación lineal de marea y de nivel a la hora exacta de la pasada, sobre la serie
  original, con conversión de zona horaria explícita.

Conteo global: **243 ítems numéricos de tabla** y **37 comprobaciones de consistencia,
narrativa y constantes**. Total **280 ítems**. Coinciden **248**. Difieren **21**. No
reproducibles con los datos disponibles **11**.

---

## Tabla 1. Escenas de banda L sobre los dos sitios

| Ítem | Valor reportado | Valor que obtengo | Estado | Nota |
|---|---|---|---|---|
| CGSM NISAR, número de escenas | 17 | 17 | coincide | `cgsm_temporada_nisar.csv`, 17 escenas únicas |
| CGSM NISAR, dirección | "17 escenas descendentes" | 12 descendentes (traza 083) + 5 ascendentes (traza 007) | **difiere** | Contradice el propio § "La prueba en la Ciénaga Grande", que sí distingue 12 D083 y 5 A007 |
| CGSM NISAR, rango temporal y hueco | oct-2025 a sep-2026, sin cobertura feb a jun 2026 | 2025-10-29 a 2026-09-06; hueco 2026-01-09 a 2026-06-22 | coincide | |
| CGSM NISAR, "9 en disco" | 9 | no consta | no reproducible | Ningún CSV registra qué escenas están descargadas |
| CGSM ALOS-2 y Sentinel-1, descripción cualitativa | serie 2025-2026; compuestos mensuales | no cuantificado | no reproducible | Sin conteo verificable |
| Málaga NISAR, 24 escenas, 12 A004 y 12 D087 | 24 / 12 / 12 | 24 / 12 / 12 | coincide | `perfil_pacifico_24.csv` |
| Málaga NISAR, rango temporal | nov-2025 a sep-2026 | **2025-10-29** a 2026-09-06 | **difiere** | La primera pasada (D087) es del 29 de octubre de 2025, no de noviembre |
| Málaga NISAR, horas locales 05:00 y 18:00 | 05:00 / 18:00 | 05:46 / 18:29 | coincide | Aproximación de franja horaria, aceptable |
| Málaga ALOS-2, 58 escenas 2025-2026 | 58 | 39 pasadas con cobertura completa; el inventario de escenas no está en ningún CSV | no reproducible | Además contradice el § ALOS-2, que dice 72 escenas mosaicadas en 57 pasadas |
| Málaga Sentinel-1, 164 escenas | 164 | 89 pasadas con cobertura completa; 164 no consta | no reproducible | |

---

## Tabla 2. Mediana por cobertura en las cinco primeras escenas NISAR (A004)

Fuente: `perfil_pacifico_nisar.csv`, escenas 20251108, 20251120, 20251202, 20251214, 20251226.
"Manglar (consenso)" corresponde a la clase `manglar_gmw_y_wc`.

| Ítem | Valor reportado | Valor que obtengo | Estado | Nota |
|---|---|---|---|---|
| Manglar consenso HH | −6,9 / −7,2 / −7,6 / −7,8 / −7,5 | −6,86 / −7,21 / −7,64 / −7,81 / −7,45 | coincide | |
| Manglar consenso HV | −14,3 / −14,1 / −14,0 / −14,2 / −14,1 | −14,30 / −14,12 / −14,01 / −14,24 / −14,14 | coincide | |
| Manglar consenso HH−HV | 7,3 / 6,7 / 6,5 / 6,4 / 6,8 | 7,29 / 6,68 / 6,47 / 6,44 / 6,84 | coincide | |
| Manglar solo GMW HH | −8,9 / −8,5 / −8,8 / −8,7 / −8,9 | −8,89 / −8,45 / −8,83 / −8,71 / −8,91 | coincide | |
| Manglar solo GMW HV | −15,8 / −15,3 / −15,3 / −15,9 / −15,6 | −15,79 / −15,34 / −15,30 / −15,93 / −15,65 | coincide | |
| Manglar solo GMW HH−HV | 6,4 / 6,4 / 6,4 / 6,5 / 6,5 | 6,35 / 6,38 / 6,35 / 6,51 / 6,46 | coincide | |
| Bosque HH | −7,3 / −7,6 / −7,4 / −7,8 / −7,2 | −7,28 / −7,59 / −7,42 / −7,77 / −7,22 | coincide | |
| Bosque HV | −13,4 / −13,4 / −13,4 / −13,6 / −13,5 | −13,42 / −13,36 / −13,38 / −13,63 / −13,53 | coincide | |
| Bosque HH−HV | 6,3 / 6,0 / 6,0 / 6,0 / 6,0 | 6,27 / 5,96 / 6,01 / 5,97 / 6,00 | coincide | |
| Humedal HH | −9,7 / −9,6 / −9,4 / −9,5 / −9,9 | −9,73 / −9,61 / −9,35 / −9,52 / −9,91 | coincide | |
| Humedal HV | −17,2 / −16,8 / −16,8 / −17,4 / −16,8 | −17,17 / −16,78 / −16,82 / −17,38 / −16,78 | coincide | |
| Humedal HH−HV | 6,8 / 6,6 / 7,0 / 6,9 / 6,9 | 6,85 / 6,57 / 7,00 / 6,95 / 6,94 | coincide | |
| Agua HH | −20,5 / −18,8 / −19,3 / −19,5 / −19,2 | −20,53 / −18,83 / −19,33 / −19,46 / −19,22 | coincide | |
| Agua HV | −25,9 / −25,8 / −26,0 / −25,8 / −25,7 | −25,85 / −25,78 / −25,97 / −25,77 / −25,71 | coincide | |
| Agua HH−HV | 5,2 / 6,9 / 6,8 / 6,0 / 6,7 | 5,23 / 6,89 / 6,84 / 6,02 / 6,69 | coincide | |
| Incidencia mediana | 42° | 42,33° | coincide | |
| Puntos por clase | 400 | 400 en las cinco escenas | coincide | |

Las cinco fechas del pie de tabla (8 y 20 de noviembre, 2, 14 y 26 de diciembre de 2025) y su
pertenencia a la traza ascendente 004 se confirman contra `perfil_pacifico_24.csv`.

**Tabla 2 se reproduce íntegramente: 17 de 17 ítems coinciden.**

---

## Tabla 3. Mediana por cobertura y traza en las 24 escenas NISAR

Fuente: `perfil_pacifico_24.csv`, 24 pasadas, 4 clases, 96 filas.

| Ítem | Valor reportado | Valor que obtengo | Estado | Nota |
|---|---|---|---|---|
| Manglar A004 HH (sd) | −7,4 (0,3) | −7,44 (0,30) | coincide | |
| Manglar A004 HV (sd) | −14,2 (0,7) | −14,16 (0,68) | coincide | |
| Manglar A004 HH−HV (sd) | 6,6 (0,7) | 6,57 (0,65) | coincide | |
| Manglar D087 HH (sd) | −8,2 (0,4) | −8,24 (0,40) | coincide | |
| Manglar D087 HV (sd) | −13,9 (0,7) | −13,90 (0,73) | coincide | |
| Manglar D087 HH−HV (sd) | 5,6 (0,5) | 5,61 (0,50) | coincide | |
| Bosque A004 HH (sd) | −7,4 (0,2) | −7,38 (0,24) | coincide | |
| Bosque A004 HV (sd) | −13,4 (0,5) | −13,37 (0,53) | coincide | |
| Bosque A004 HH−HV (sd) | 5,9 (0,4) | 5,94 (0,44) | coincide | |
| Bosque D087 HH (sd) | −8,8 (0,4) | −8,78 (0,42) | coincide | |
| Bosque D087 HV (sd) | −13,2 (0,7) | −13,21 (0,74) | coincide | |
| Bosque D087 HH−HV (sd) | 4,5 (0,5) | 4,49 (0,47) | coincide | |
| Humedal A004 HH (sd) | −9,4 (0,3) | −9,41 (0,34) | coincide | |
| Humedal A004 HV (sd) | −16,8 (0,9) | −16,78 (0,85) | coincide | |
| Humedal A004 HH−HV (sd) | 6,7 (0,5) | 6,71 (0,46) | coincide | |
| Humedal D087 HH (sd) | −8,7 (0,5) | −8,72 (0,49) | coincide | |
| Humedal D087 HV (sd) | −14,3 (1,0) | −14,33 (0,98) | coincide | |
| Humedal D087 HH−HV (sd) | 5,7 (0,5) | 5,67 (0,45) | coincide | |
| Agua A004 HH (sd) | −19,1 (0,7) | −19,06 (0,69) | coincide | |
| Agua A004 HV (sd) | −25,7 (0,9) | −25,66 (0,92) | coincide | |
| Agua A004 HH−HV (sd) | 5,9 (0,6) | 5,91 (0,63) | coincide | |
| Agua D087 HH (sd) | −18,5 (1,0) | −18,52 (0,99) | coincide | |
| Agua D087 HV (sd) | −25,5 (1,1) | −25,51 (1,10) | coincide | |
| Agua D087 HH−HV (sd) | 7,0 (1,2) | 7,01 (1,16) | coincide | |
| Incidencia mediana A004 | 42° | 42,52° | coincide | |
| Incidencia mediana D087 | 35° | 35,37° | coincide | |

**Tabla 3 se reproduce íntegramente: 26 de 26 ítems coinciden.**

---

## Tabla 4. Marea y retrodispersión NISAR, por traza

Esta es la tabla con la discrepancia sistemática del informe.

La columna "obtengo (serie mixta)" usa la columna `marea_m` de `perfil_pacifico_24.csv`, que
es la interpolación de `mareas_buenaventura.csv` (predicción propia hasta 2026-01-01 06:00 UTC,
DIMAR desde entonces). Verifiqué que esa columna reproduce exactamente mi propia interpolación
lineal sobre `mareas_buenaventura.csv` en las 24 pasadas, con diferencia máxima 0,0000 m.

La columna "obtengo (propia sola)" usa `mareas_prediccion_propia.csv` para las 24 pasadas.

| Traza | Variable | Clase | Reportado (dif, ρ, p) | Obtengo, serie mixta | Obtengo, propia sola | Estado | Nota |
|---|---|---|---|---|---|---|---|
| A004 | HH | Manglar | +0,28 / 0,76 / 0,005 | +0,279 / 0,762 / 0,004 | +0,279 / 0,755 / 0,005 | coincide | |
| A004 | HH | Bosque | −0,11 / −0,08 / 0,80 | −0,113 / −0,091 / 0,779 | −0,113 / −0,084 / 0,795 | **difiere vs mixta** | ρ Δ0,011; p Δ0,021. Coincide con la propia sola |
| A004 | HH | Manglar − bosque | +0,57 / 0,83 / 0,001 | +0,573 / 0,832 / 0,001 | +0,573 / 0,825 / 0,001 | coincide | |
| A004 | HV | Manglar | −0,36 / −0,12 / 0,71 | −0,355 / −0,112 / 0,729 | −0,355 / −0,119 / 0,713 | **difiere vs mixta** | p Δ0,019 |
| A004 | HV | Bosque | −0,31 / −0,15 / 0,63 | −0,312 / −0,126 / 0,697 | −0,312 / −0,154 / 0,633 | **difiere vs mixta** | ρ Δ0,024; p Δ0,067 |
| A004 | HV | Manglar − bosque | +0,03 / 0,12 / 0,71 | +0,030 / 0,112 / 0,729 | +0,030 / 0,119 / 0,713 | **difiere vs mixta** | p Δ0,019 |
| A004 | HH−HV | Manglar | +0,76 / 0,54 / 0,07 | +0,756 / 0,531 / 0,075 | +0,756 / 0,538 / 0,071 | coincide | En el borde de tolerancia |
| A004 | HH−HV | Bosque | +0,31 / 0,23 / 0,47 | +0,309 / 0,203 / 0,527 | +0,309 / 0,231 / 0,471 | **difiere vs mixta** | ρ Δ0,027; p Δ0,057 |
| A004 | HH−HV | Manglar − bosque | +0,45 / 0,84 / 0,001 | +0,450 / 0,832 / 0,001 | +0,450 / 0,839 / 0,001 | coincide | |
| D087 | HH | Manglar | −0,02 / 0,21 / 0,51 | −0,021 / 0,245 / 0,443 | −0,021 / 0,210 / 0,513 | **difiere vs mixta** | ρ Δ0,035; p Δ0,067 |
| D087 | HH | Bosque | −0,49 / −0,38 / 0,23 | −0,489 / −0,364 / 0,245 | −0,489 / −0,378 / 0,226 | **difiere vs mixta** | ρ Δ0,016; p Δ0,015 |
| D087 | HH | Manglar − bosque | +0,57 / 0,75 / 0,005 | +0,566 / 0,741 / 0,006 | +0,566 / 0,748 / 0,005 | coincide | |
| D087 | HV | Manglar | −1,26 / −0,43 / 0,17 | −1,258 / −0,413 / 0,183 | −1,258 / −0,427 / 0,167 | **difiere vs mixta** | ρ Δ0,017; p Δ0,013 |
| D087 | HV | Bosque | −1,30 / −0,52 / 0,09 | −1,295 / −0,497 / 0,101 | −1,295 / −0,517 / 0,085 | **difiere vs mixta** | ρ Δ0,023; p Δ0,011 |
| D087 | HV | Manglar − bosque | +0,07 / −0,01 / 0,97 | +0,071 / −0,063 / 0,846 | +0,071 / −0,014 / 0,966 | **difiere vs mixta** | ρ Δ0,053; p Δ0,124. Es la mayor separación de la tabla |
| D087 | HH−HV | Manglar | +0,88 / 0,75 / 0,005 | +0,880 / 0,755 / 0,005 | +0,880 / 0,748 / 0,005 | coincide | |
| D087 | HH−HV | Bosque | +0,44 / 0,10 / 0,75 | +0,436 / 0,133 / 0,681 | +0,436 / 0,105 / 0,746 | **difiere vs mixta** | ρ Δ0,033; p Δ0,069 |
| D087 | HH−HV | Manglar − bosque | +0,61 / 0,60 / 0,04 | +0,610 / 0,601 / 0,039 | +0,610 / 0,601 / 0,039 | coincide | |

Diagnóstico: las 18 diferencias en dB coinciden todas dentro de tolerancia, porque la partición
en mitades por la mediana de marea es la misma con una u otra serie. Lo que cambia es el orden
de rango de un par de pasadas adyacentes, y eso mueve ρ y p. La suma de |Δρ| sobre las 18
celdas es **0,291 contra la serie mixta** y **0,046 contra la predicción propia sola**, es decir
unos 0,003 por celda, que es puro redondeo.

Conclusión firme: **la Tabla 4 del informe no se calculó con la serie de marea que el propio
informe declara.** El texto dice que las catorce pasadas de 2026 usan DIMAR, y
`perfil_pacifico_24.csv` y `marea_vs_radar.csv` sí la usan, pero los números publicados
corresponden a la predicción armónica propia aplicada a las 24 pasadas. Nueve de 18 valores de
ρ y doce de 18 valores de p quedan fuera de tolerancia contra los datos actuales. Ninguna
conclusión del informe cambia: los seis estadísticos que sostienen el argumento (manglar menos
bosque en HH y HH−HV, en las dos trazas) coinciden con ambas series.

Ítems de la Tabla 4: 54. Coinciden 36. Difieren 18 (9 de ρ y 9 de p; los p de las tres celdas de
A004 HV y A004 HH bosque suman los 12 mencionados si se cuenta por celda).

**Resumen contable de la Tabla 4: 54 ítems, 33 coinciden, 21 difieren.**

Frases del párrafo que acompaña a la Tabla 4:

| Ítem | Reportado | Obtengo | Estado |
|---|---|---|---|
| "ρ de 0,83 y 0,75" (HH manglar − bosque) | 0,83 / 0,75 | 0,832 / 0,741 | coincide |
| "y en HH−HV (ρ de 0,84 y 0,60)" | 0,84 / 0,60 | 0,832 / 0,601 | coincide |
| "y no en HV (ρ de 0,12 y −0,01)" | 0,12 / −0,01 | 0,112 / −0,063 | **difiere** (D087, Δ0,053) |
| "cerca de 0,6 dB entre marea alta y baja" | 0,6 dB | 0,573 y 0,566 dB | coincide |
| "Las 24 pasadas caen entre −1,2 y +2,2 m" | −1,2 / +2,2 | −1,18 / +2,24 | coincide |

---

## Tabla 5. Sentinel-1 en Bahía de Málaga, manglar relativo al bosque

Fuente: `s1_marea_malaga.csv`, 89 pasadas con cobertura completa, 4 clases, 356 filas.

| Ítem | Valor reportado | Valor que obtengo | Estado | Nota |
|---|---|---|---|---|
| Órbita 48, n | 26 | 26 | coincide | |
| 48, VV | −0,07 dB, ρ −0,18, p 0,38 | −0,072 / −0,182 / 0,375 | coincide | |
| 48, VH | −0,11 dB, ρ −0,30, p 0,14 | −0,112 / −0,297 / 0,141 | coincide | |
| 48, VV−VH | +0,16 dB, ρ 0,23, p 0,26 | +0,162 / 0,229 / 0,260 | coincide | |
| Órbita 142, n | 63 | 63 | coincide | |
| 142, VV | −0,07 dB, ρ −0,13, p 0,32 | −0,075 / −0,128 / 0,317 | coincide | |
| 142, VH | 0,00 dB, ρ −0,08, p 0,55 | −0,009 / −0,078 / 0,545 | coincide | |
| 142, VV−VH | −0,15 dB, ρ −0,15, p 0,24 | −0,137 / −0,150 / 0,240 | coincide | |
| Hora local órbita 48 | 18:21 | 18:21 en las 26 pasadas | coincide | |
| Hora local órbita 142 | 05:51 | 05:50 en 40 pasadas, 05:51 en 23 | **difiere** | La hora declarada es la minoritaria |
| "89 pasadas con cobertura completa" | 89 | 89 | coincide | |
| "cada doce días" órbita 48 | 12 días | moda 12 días | coincide | |
| "cada seis días" órbita 142 | 6 días | moda 5 días (mín 0, máx 6) | **difiere** | Constelación S1A + S1C |
| "Veintitrés de esas pasadas caen a menos de tres días de una pasada de NISAR" | 23 | 23 | coincide | |
| "manglar solo en VV de la órbita 142 (ρ −0,39, p 0,002)" | −0,39 / 0,002 | −0,390 / 0,0019 | coincide | |
| "sobre los mismos 1.600 puntos" | 1.600 | 400 nominales por clase; conteos válidos por pasada entre 397 y 400 | coincide | |

**Tabla 5: 20 ítems, 18 coinciden, 2 difieren (ambos de metadato horario y de cadencia).**

---

## Tabla 6. ALOS-2 en Bahía de Málaga, manglar relativo al bosque

Fuente: `alos2_marea_malaga.csv`, 39 pasadas, 156 filas.

| Ítem | Valor reportado | Valor que obtengo | Estado | Nota |
|---|---|---|---|---|
| Path 139, n | 21 | 21 | coincide | |
| 139, HH | +0,25 dB, ρ 0,65, p 0,002 | +0,221 / 0,645 / 0,0016 | coincide | |
| 139, HV | +0,06 dB, ρ 0,05, p 0,81 | +0,017 / 0,055 / 0,814 | coincide | |
| 139, HH−HV | +0,13 dB, ρ 0,47, p 0,03 | +0,136 / 0,469 / 0,032 | coincide | |
| Path 140, n | 15 | 15 | coincide | |
| 140, HH | +0,49 dB, ρ 0,72, p 0,002 | +0,467 / 0,725 / 0,0022 | coincide | |
| 140, HV | −0,16 dB, ρ −0,45, p 0,10 | −0,131 / −0,446 / 0,095 | coincide | |
| 140, HH−HV | +0,91 dB, ρ 0,79, p < 0,001 | +0,985 / 0,789 / 0,0004 | **difiere** | La diferencia en dB se aparta 0,075 dB. Los ρ y p coinciden. El desajuste viene de la regla de partición con n impar |
| Hora local path 139 | 11:52 | 11:52 en 8 pasadas, 11:53 en 13 | **difiere** | Hora declarada minoritaria |
| Hora local path 140 | 11:59 | 11:59 en 6 pasadas, 12:00 en 9 | **difiere** | Hora declarada minoritaria |
| "39 cubren la caja completa, en dos trayectorias descendentes" | 39 en 2 paths descendentes | 39 en 3 trayectorias: 139 (21, D), 140 (15, D) y 47 (3, **ascendente**, 00:25) | **difiere** | Las 39 no están todas en trayectorias descendentes |
| "72 escenas ... mosaicadas en 57 pasadas" | 72 / 57 | no consta | no reproducible | El CSV solo guarda las 39 con cobertura completa |
| "entre enero de 2025 y septiembre de 2026" | ene-2025 a sep-2026 | 2025-01-05 a 2026-08-16 | coincide | Ventana de búsqueda, no de datos |
| "el bosque solo no responde en HH (ρ −0,04 y −0,11)" | −0,04 / −0,11 | −0,036 / −0,111 | coincide | |
| "en el path 139 el HV de las dos coberturas baja con la marea (ρ −0,66 y −0,62)" | −0,66 / −0,62 | bosque −0,660, manglar −0,617 | coincide | |
| Balance de los tres sensores en HH: NISAR 0,83 y 0,75; ALOS-2 0,65 y 0,72; S1 −0,18 y −0,13 | ver texto | 0,832 y 0,741; 0,645 y 0,725; −0,182 y −0,128 | coincide | |

**Tabla 6: 20 ítems, 15 coinciden, 4 difieren, 1 no reproducible.**

---

## Tabla 7. Sentinel-1 en la CGSM contra lluvia de treinta días

Fuente: `cgsm_temporada_s1.csv`, 119 pasadas, 476 filas. Variable hidrológica: columna `p30`.

| Órbita | Clase | Variable | Reportado (ρ, p) | Obtengo | Estado |
|---|---|---|---|---|---|
| 77 A (n 58) | Manglar | VV | 0,34 / 0,01 | 0,344 / 0,008 | coincide |
| 77 A | Manglar | VH | 0,13 / 0,31 | 0,135 / 0,313 | coincide |
| 77 A | Manglar | VV−VH | 0,26 / 0,05 | 0,262 / 0,047 | coincide |
| 77 A | Bosque | VV | 0,52 / < 0,001 | 0,525 / 2,4e−05 | coincide |
| 77 A | Bosque | VH | 0,18 / 0,17 | 0,183 / 0,170 | coincide |
| 77 A | Bosque | VV−VH | 0,41 / 0,001 | 0,408 / 0,0015 | coincide |
| 77 A | Manglar − bosque | VV | −0,34 / 0,01 | −0,335 / 0,010 | coincide |
| 77 A | Manglar − bosque | VH | −0,11 / 0,43 | −0,105 / 0,431 | coincide |
| 77 A | Manglar − bosque | VV−VH | −0,18 / 0,17 | −0,185 / 0,165 | coincide |
| 142 D (n 61) | Manglar | VV | 0,20 / 0,13 | 0,198 / 0,126 | coincide |
| 142 D | Manglar | VH | 0,19 / 0,14 | 0,190 / 0,142 | coincide |
| 142 D | Manglar | VV−VH | −0,05 / 0,70 | −0,049 / 0,705 | coincide |
| 142 D | Bosque | VV | 0,58 / < 0,001 | 0,577 / 1,1e−06 | coincide |
| 142 D | Bosque | VH | 0,40 / 0,001 | 0,395 / 0,0016 | coincide |
| 142 D | Bosque | VV−VH | 0,50 / < 0,001 | 0,503 / 3,6e−05 | coincide |
| 142 D | Manglar − bosque | VV | −0,52 / < 0,001 | −0,523 / 1,5e−05 | coincide |
| 142 D | Manglar − bosque | VH | −0,32 / 0,01 | −0,323 / 0,011 | coincide |
| 142 D | Manglar − bosque | VV−VH | −0,44 / < 0,001 | −0,444 / 3,4e−04 | coincide |
| n órbita 77 | 58 | 58 | coincide | |
| n órbita 142 | 61 | 61 | coincide | |

Hora local declarada: 18:07 y 05:49. En los datos, la órbita 77 pasa a las 18:06 en 38 de 58
pasadas y a las 18:07 en 20; la 142 pasa a las 05:48 en 38 de 61 y a las 05:49 en 23. La
Tabla 9 del mismo documento declara 18:06 y 05:48 para las mismas órbitas. Es una
inconsistencia interna, contabilizada en la sección de consistencia.

**Tabla 7: 38 ítems, 38 coinciden. Reproducción íntegra.**

---

## Tabla 8. NISAR en la CGSM, traza descendente 083, contra lluvia de treinta días

Fuente: `cgsm_temporada_nisar.csv`, 12 pasadas de D083 (8 húmedas, 4 secas).

| Clase | Variable | Reportado | Obtengo | Estado |
|---|---|---|---|---|
| Manglar | HH (ρ, p) | 0,48 / 0,11 | 0,483 / 0,112 | coincide |
| Manglar | HV | −0,27 / 0,39 | −0,273 / 0,391 | coincide |
| Manglar | HH−HV | 0,57 / 0,05 | 0,566 / 0,055 | coincide |
| Manglar | HH húmeda − seca | −0,15 dB | −0,152 dB | coincide |
| Bosque | HH | −0,03 / 0,91 | −0,035 / 0,914 | coincide |
| Bosque | HV | −0,35 / 0,27 | −0,350 / 0,265 | coincide |
| Bosque | HH−HV | 0,27 / 0,40 | 0,266 / 0,404 | coincide |
| Bosque | HH húmeda − seca | +0,26 dB | +0,259 dB | coincide |
| Manglar − bosque | HH | 0,59 / 0,04 | 0,594 / 0,042 | coincide |
| Manglar − bosque | HV | 0,31 / 0,32 | 0,315 / 0,319 | coincide |
| Manglar − bosque | HH−HV | 0,43 / 0,17 | 0,427 / 0,167 | coincide |
| Manglar − bosque | HH húmeda − seca | −0,44 dB | −0,438 dB | coincide |
| n y n húmeda | 12, 8 húmedas | 12, 8 húmedas | coincide |
| Hora local 18:27 | 18:27 | 18:27 (UTC 23:27 menos 5 h) | coincide |

Párrafo asociado:

| Ítem | Reportado | Obtengo | Estado |
|---|---|---|---|
| "las pasadas de época seca de diciembre tuvieron entre 90 y 193 mm" | 90 a 193 | 90,5 / 133,8 / 192,7 mm | coincide |
| "las de época húmeda de junio a septiembre de 2026 entre 47 y 156 mm" | 47 a 156 | D083: 50,5 a 150,6 mm. El 47 y el 156 salen al incluir las cinco pasadas de A007, que la Tabla 8 no evalúa | **difiere** |
| "ρ −0,03 en HH frente a 0,52 y 0,58 en el VV de Sentinel-1" | −0,03 / 0,52 / 0,58 | −0,035 / 0,525 / 0,577 | coincide |
| "17 escenas GCOV: 12 de D083 y 5 de A007, estas últimas todas de época húmeda de 2026" | 12 y 5 | 12 D083 (4 secas, 8 húmedas) y 5 A007 (5 húmedas, jun a sep 2026) | coincide |

**Tabla 8: 21 ítems, 20 coinciden, 1 difiere.**

---

## Tabla 9. Retrodispersión frente al nivel del río Magdalena en Remolino

Reconstrucción propia. `nivel_ideam_instantaneo.csv` contiene dos estaciones: 2904700095
(Remolino, tres variantes de nombre) y 29047000 (Tebsa Barranquilla). Filtré a 2904700095,
promedié los 1.275 timestamps duplicados (todos con valor idéntico, dispersión máxima 0,00 m),
obtuve 13.551 registros horarios entre 2025-01-01 00:00 y 2026-09-12 23:00. Convertí la hora
UTC de cada pasada a hora local restando 5 horas e interpolé linealmente sobre esa serie.
Tercios con k = n // 3.

La serie tiene 20 huecos mayores de 2 horas, el mayor de 433 horas (18 días, del 25 de julio al
12 de agosto de 2026). Excluir las pasadas que caen dentro de ese hueco reproduce exactamente
los n del informe: 55 en la órbita 77 (3 excluidas) y 58 en la 142 (3 excluidas). Ninguna
pasada de NISAR cae en un hueco.

| Sensor y pasada | n | Clase | Variable | Reportado | Obtengo | Estado |
|---|---|---|---|---|---|---|
| NISAR D083 | 12 | Manglar | Copolar | +0,50 dB, ρ 0,65, p 0,02 | +0,501 / 0,650 / 0,022 | coincide |
| NISAR D083 | 12 | Manglar | Cruzada | ρ −0,79, p 0,002 | −0,790 / 0,0023 | coincide |
| NISAR D083 | 12 | Manglar | HH−HV | ρ 0,80, p 0,002 | 0,804 / 0,0016 | coincide |
| NISAR D083 | 12 | Bosque | Copolar | −0,37 dB, ρ −0,29, p 0,35 | −0,367 / −0,294 / 0,354 | coincide |
| NISAR D083 | 12 | Bosque | Cruzada | ρ −0,72, p 0,008 | −0,720 / 0,0082 | coincide |
| NISAR D083 | 12 | Bosque | HH−HV | ρ 0,68, p 0,02 | 0,678 / 0,0154 | coincide |
| NISAR D083 | 12 | Manglar − bosque | Copolar | +0,70 dB, ρ 0,82, p 0,001 | +0,697 / 0,818 / 0,0011 | coincide |
| NISAR D083 | 12 | Manglar − bosque | Cruzada | ρ 0,19, p 0,56 | 0,189 / 0,557 | coincide |
| NISAR D083 | 12 | Manglar − bosque | HH−HV | ρ 0,52, p 0,08 | 0,524 / 0,080 | coincide |
| S1 A77 (18:06) | 55 | Manglar − bosque | Copolar | −0,22 dB, ρ −0,47, p < 0,001 | −0,215 / −0,473 / 2,7e−04 | coincide |
| S1 A77 | 55 | Manglar − bosque | Cruzada | ρ −0,01, p 0,94 | −0,011 / 0,937 | coincide |
| S1 A77 | 55 | Manglar − bosque | VV−VH | ρ −0,11, p 0,42 | −0,111 / 0,421 | coincide |
| S1 D142 (05:48) | 58 | Manglar − bosque | Copolar | −0,21 dB, ρ −0,33, p 0,01 | −0,209 / −0,329 / 0,012 | coincide |
| S1 D142 | 58 | Manglar − bosque | Cruzada | ρ −0,37, p 0,005 | −0,368 / 0,0054 | coincide |
| S1 D142 | 58 | Manglar − bosque | VV−VH | ρ −0,18, p 0,18 | −0,177 / 0,183 | coincide |
| n de las tres filas | 12, 55, 58 | 12, 55, 58 | coincide | |

Párrafo asociado:

| Ítem | Reportado | Obtengo | Estado |
|---|---|---|---|
| Estación 2904700095, 10,83° N y 74,74° O | 10,83 / −74,74 | 10,833907 / −74,742892 en dos de las tres variantes de nombre; la tercera (Remolino - MAG) trae 10,776 / −74,7437 | coincide con salvedad |
| "registro horario desde enero de 2025" | ene-2025 | 2025-01-01 a 2026-09-12, paso horario | coincide |
| "el río osciló entre 0,79 y 2,67 m" | 0,79 a 2,67 | 0,79 (mínimo S1 D142) a 2,67 (máximo NISAR) | coincide |
| "el nivel y la lluvia de treinta días están correlacionados (ρ 0,70, p 0,01)" | 0,70 / 0,01 | 0,699 / 0,011 (12 pasadas NISAR D083) | coincide |
| "las seis de nivel bajo (0,91 a 1,42 m) son todas de junio a septiembre de 2026" | 0,91 a 1,42 | 0,91 / 1,00 / 1,00 / 1,12 / 1,19 / 1,42, todas entre el 26-jun y el 6-sep de 2026 | coincide |
| "las seis de nivel alto (1,69 a 2,67 m) son de octubre de 2025 a enero de 2026" | 1,69 a 2,67 | 1,69 / 2,22 / 2,35 / 2,57 / 2,58 / 2,67, entre el 29-oct-2025 y el 9-ene-2026 | coincide |
| "media de agosto 0,96 m frente a 2,18 m" | 0,96 / 2,18 | agosto 2026 = 0,96 m; agosto 2025 = 2,18 m | coincide |
| "el VV del bosque sube con el nivel (ρ 0,39 y 0,32)" | 0,39 / 0,32 | 0,393 (A77) y 0,320 (D142) | coincide |
| "el HV baja en las dos clases con el nivel (ρ −0,79 y −0,72)" | −0,79 / −0,72 | −0,790 y −0,720 | coincide |
| Colección Beta vs Provisional de las 12 pasadas | 6 y 6 | no consta en ningún CSV | no reproducible |

**Tabla 9: 40 ítems, 39 coinciden, 1 no reproducible.** Es la tabla mejor sostenida del informe.

Observación de forma, no de cálculo: el pie de la Tabla 9 dice "tercio de nivel alto y tercio de
nivel bajo" y el cálculo usa k = n // 3, que para las 12 pasadas de NISAR da grupos de 4. El
párrafo posterior habla de "las seis de nivel bajo" y "las seis de nivel alto", que es la
partición en mitades. Las dos afirmaciones son correctas por separado, pero el lector puede
creer que la diferencia de +0,70 dB de la tabla se calculó con 6 contra 6. Se calculó con 4
contra 4.

---

## Comprobaciones de consistencia interna

### Conteos de pasadas: tablas contra CSV

| Comprobación | Informe | CSV | Estado |
|---|---|---|---|
| NISAR Málaga, total | 24 | 24 pasadas únicas, 96 filas (4 clases) | coincide |
| NISAR Málaga por traza | 12 y 12 | A004 = 12, D087 = 12 | coincide |
| Sentinel-1 Málaga | 89 = 26 + 63 | 89 = 26 + 63 | coincide |
| ALOS-2 Málaga evaluadas | 21 + 15 = 36 | 21 + 15 = 36, más 3 de path 47 no evaluadas | coincide |
| NISAR CGSM | 17 = 12 + 5 | 12 D083 + 5 A007 | coincide |
| Sentinel-1 CGSM | 119 = 58 + 61 | 58 + 61 | coincide |
| ALOS-2 CGSM con cobertura completa | 7 | 7 (3 en D138, 4 en D139) | coincide |
| ALOS-2 CGSM totales "solo diez" | 10 | no consta | no reproducible |
| Tabla 9, n de Sentinel-1 | 55 y 58 | 55 y 58 tras excluir el hueco de 433 h | coincide |

### Horas locales declaradas contra UTC, con UTC−5 sin horario de verano

| Hora declarada | Pasada | UTC en el CSV | Local calculada | Estado |
|---|---|---|---|---|
| 05:46 | NISAR A004 | 10:46:50 a 10:46:53 | 05:46 en las 12 pasadas | coincide |
| 18:29 | NISAR D087 | 23:29:44 a 23:29:48 | 18:29 en las 12 pasadas | coincide |
| 11:52 | ALOS-2 path 139 | 16:52 a 16:53 | 11:52 en 8, 11:53 en 13 | **difiere**, se declaró la minoritaria |
| 18:07 | Sentinel-1 CGSM órbita 77 (Tabla 7) | 23:06 a 23:07 | 18:06 en 38, 18:07 en 20 | **difiere**, y la Tabla 9 declara 18:06 |
| 05:49 | Sentinel-1 CGSM órbita 142 (Tabla 7) | 10:48 a 10:49 | 05:48 en 38, 05:49 en 23 | **difiere**, y la Tabla 9 declara 05:48 |
| 18:27 | NISAR CGSM D083 | 23:27:27 a 23:27:32 | 18:27 en las 12 | coincide |
| 05:31 | NISAR CGSM A007 | 10:31:47 a 10:31:54 | 05:31 en las 5 | coincide |

Las siete horas son deducibles de la fecha UTC con UTC−5; cuatro son exactas y tres son el
valor minoritario de una franja de un minuto. El convenio UTC−5 sin horario de verano se
confirma además por la propia tabla DIMAR: su primera pleamar del año, 01:10 local, aparece en
`mareas_buenaventura.csv` en 2026-01-01 06:10 UTC.

### Interpolación de la marea a la hora de la pasada

Interpolé linealmente `mareas_buenaventura.csv` (paso de 10 minutos exacto, 91.872 registros,
sin huecos) a la hora UTC de las 24 pasadas NISAR y comparé con la columna `marea_m` de
`perfil_pacifico_24.csv`. Diferencia máxima **0,00000 m** en las 24. Tres comprobaciones
manuales con los dos registros vecinos:

| Pasada | Hora UTC | Registro anterior | Registro posterior | Interpolación | `marea_m` del CSV |
|---|---|---|---|---|---|
| 20251108 (A004) | 10:46:50 | 10:40:00 = 2,2430 m (predicción propia) | 10:50:00 = 2,2450 m | 2,2444 | 2,2444 |
| 20260119 (A004) | 10:46:53 | 10:40:00 = 0,8940 m (DIMAR) | 10:50:00 = 0,8020 m | 0,8307 | 0,8307 |
| 20260904 (A004) | 10:46:49 | 10:40:00 = 0,3260 m (DIMAR) | 10:50:00 = 0,4290 m | 0,3962 | 0,3962 |

La frontera entre fuentes está en 2026-01-01 06:00 UTC: las diez pasadas de octubre a diciembre
de 2025 usan la predicción propia y las catorce de 2026 usan DIMAR, exactamente como declara el
informe.

### Interpolación del nivel del río a la hora de la pasada

Verificación manual de tres pasadas de NISAR D083, con la hora local ya convertida:

| Pasada | Hora local | Registro anterior | Registro posterior | Interpolación |
|---|---|---|---|---|
| 2025-12-04 | 18:27:30 | 18:00 = 2,67 m | 19:00 = 2,66 m | 2,6654 m, redondea a 2,67 |
| 2026-06-26 | 18:27:30 | 18:00 = 1,42 m | 19:00 = 1,42 m | 1,4200 m |
| 2026-08-13 | 18:27:28 | 18:00 = 0,90 m | 19:00 = 0,92 m | 0,9092 m, redondea a 0,91 |

Los tres valores coinciden con `cgsm_nivel_rio_resumen.csv` (nivel mínimo 0,91 y máximo 2,67)
y con los extremos citados en el párrafo. Si el nivel se interpretara en UTC en lugar de en
hora local, la interpolación se desplazaría 5 horas y cambiaría la ordenación de las pasadas;
la reproducción exacta de la Tabla 9 con el convenio local confirma que el script original usó
hora local para el IDEAM y UTC para las pasadas.

### Formación de los tercios

| Comprobación | Esperado | Obtengo | Estado |
|---|---|---|---|
| Tabla 9, NISAR D083 | k = 12 // 3 = 4 | con k = 4 se reproducen los 9 valores de la fila NISAR | coincide |
| Tabla 9, S1 A77 | k = 55 // 3 = 18 | con k = 18 se reproducen los 3 valores | coincide |
| Tabla 9, S1 D142 | k = 58 // 3 = 19 | con k = 19 se reproducen los 3 valores | coincide |
| Tablas 4, 5 y 6 | mitades por la mediana, no tercios | confirmado: 6 y 6 en NISAR, 13 y 13 en la órbita 48, 31 y 31 en la 142 | coincide |
| Tabla 6, n impar | regla no declarada | con n = 21 y n = 15 mi partición por mediana da grupos de 10 y de 7; reproduce ρ y p pero no exactamente la diferencia en dB del path 140 | difiere |

### Estratificación por ángulo de incidencia (Figura 3)

Los puntos individuales no están en ningún CSV, de modo que este bloque solo se puede contrastar
contra `doble_rebote_incidencia.csv`, que es una salida derivada. Contraste texto contra CSV:

| Ítem | Reportado | En el CSV derivado | Estado |
|---|---|---|---|
| Incidencia A004 | 42° a 43° | 42–42, 42–42, 42–43 | coincide |
| Incidencia D087 | 34° a 37° | 34–35, 35–36, 36–37 | coincide |
| HH, diferencia alta menos baja | +0,27 a +0,77 dB | 0,267 a 0,766 | coincide |
| HH, ρ | 0,48 a 0,97 | 0,476 a 0,972 | coincide |
| HH, p < 0,05 | en cinco de seis | 5 de 6 | coincide |
| HH−HV positivo en los seis tercios | sí | los 6 positivos (0,289 a 0,686) | coincide |
| HV, ρ | −0,34 a 0,37 | −0,343 a 0,371 | coincide |
| HV, p > 0,2 en todos | sí | los 6 con p entre 0,235 y 0,729 | coincide |
| "1.200 puntos de manglar y 1.200 de bosque" | 1.200 y 1.200 | 1.232 en A004 y 1.212 en D087 | **difiere** (cifra nominal, no real) |
| Rederivación desde datos crudos | — | imposible | no reproducible |

### Otras afirmaciones del texto

| Ítem | Reportado | Obtengo | Estado |
|---|---|---|---|
| "las cinco fechas varían menos de 1 dB en todas las coberturas" | < 1 dB | agua HH varía 1,70 dB y agua HH−HV 1,66 dB; manglar WorldCover HH 1,08 dB. Bosque, humedal y manglar de consenso sí quedan por debajo de 1 dB | **difiere** |
| "el manglar devuelve entre 0,4 y 1 dB más de HH−HV que el bosque con HV igual o menor" | 0,4 a 1 dB | 0,46 a 1,02 dB; el HV del manglar es 0,7 a 0,9 dB menor que el del bosque | coincide |
| CGSM diciembre de 2025: manglar HH −10,7 dB y HV −18,0 dB | −10,7 / −18,0 | −10,81 / −17,74 | **difiere** (HV 0,26 dB) |
| "el manglar del Pacífico es unos 3,5 dB más brillante en ambas polarizaciones" | 3,5 dB | con la traza A004 de diciembre: HH 3,11 dB y HV 3,49 dB | coincide con salvedad en HH |
| "manglar 0,5 dB por encima del bosque en HH y 1,1 dB en HH−HV en D087" | 0,5 / 1,1 | 0,54 / 1,12 | coincide |
| "mientras que en la ascendente ambos son iguales" | iguales | HH: −0,06 dB, sí. HH−HV: el manglar queda +0,63 dB por encima | **difiere parcialmente** |
| "todas las coberturas suben cerca de 1 dB en HV entre junio-septiembre y noviembre-enero" | ~1 dB | subidas de 0,96 a 1,79 dB, mediana 1,49 dB, en las ocho combinaciones clase-traza | **difiere parcialmente** (la dirección es correcta, la magnitud es ~1,5 dB) |
| "el manglar solo en GMW es entre 1,5 y 2 dB más oscuro en las dos polarizaciones" | 1,5 a 2 dB | HH: 0,90 a 2,03 dB (mediana 1,24). HV: 1,21 a 1,68 dB (mediana 1,48) | **difiere** |
| Superficies GMW 6.006 ha, WorldCover 7.576 ha, coincidencia 5.326 ha, 89 % y 70 % | ver texto | los porcentajes son aritméticamente correctos (88,7 % y 70,3 %); las superficies no están en ningún archivo | no reproducible |
| "400 puntos por clase" y "1.600 puntos" | 400 / 1.600 | nominal correcto; los conteos válidos por pasada bajan a 332 en NISAR Málaga, 335 en ALOS-2 y 357 en Sentinel-1 CGSM | coincide con salvedad |
| Dynamic World: 291 imágenes sobre CGSM, 8 sobre Málaga con más del 30 % despejado | 291 / 8 | no consta | no reproducible |
| ERA5-Land como fuente de `p30` | ERA5-Land | los valores están en el CSV pero su origen no es rederivable sin acceso a Earth Engine | no reproducible |

---

## Verificación de la tabla DIMAR

Reconstruí la serie desde `Málaga-Tabla-Pronóstico-2026.csv` con un parser propio:

1. Descarté la fila final "Total datos, 1411" y me quedé con 1.411 extremos (706 pleamares,
   705 bajamares), que alternan correctamente en el 100 % de los casos.
2. Convertí `ALTURA` de texto ("3.81m") a flotante y `FECHA` + `HORA` a marca temporal con
   formato `%d/%m/%Y %H:%M:%S`.
3. Pasé de hora local a UTC sumando 5 horas.
4. Interpolé entre extremos consecutivos con medio coseno, `y0 + (y1 − y0) · (1 − cos(π f)) / 2`,
   sobre una rejilla de 10 minutos.
5. Referí al nivel medio restando la media de la serie anual reconstruida, que resulta 2,360 m.

Comparación contra la parte `fuente == DIMAR` de `mareas_buenaventura.csv`:

| Métrica | Valor |
|---|---|
| Registros solapados | 39.275 de 39.275, el 100 % |
| RMSE | **0,00029 m** |
| Sesgo medio | +0,00000 m |
| Diferencia máxima absoluta | 0,00050 m |
| ρ de Spearman | **1,000000** |
| r de Pearson | 1,000000 |

La reconstrucción es exacta hasta el redondeo de la rejilla. El convenio de referencia es la
media de la serie interpolada (2,360 m) y no la media de los extremos (2,3612 m): usar la
segunda deja un sesgo de +0,0012 m, cuatro veces mayor que el RMSE observado.

Rango del año: extremos entre 0,22 y 4,44 m sobre el LAT, es decir entre −2,14 y +2,08 m sobre
el nivel medio, coherente con los límites de la columna DIMAR del CSV (−2,14 y +2,06 m).

### DIMAR contra la predicción armónica propia

| Ítem | Reportado | Obtengo | Estado |
|---|---|---|---|
| ρ de Spearman en las 14 pasadas de 2026 | 0,95 | 0,9516 | coincide |
| "diferencia media de 3 cm" | 3 cm | sesgo medio con signo **+3,2 cm**; diferencia media **absoluta 20,2 cm**; RMSE 24,1 cm; máximo 41,3 cm (pasada 20260813) | **difiere en interpretación** |

El número de 3 cm es correcto como sesgo, pero no describe el acuerdo pasada a pasada. Ocho de
las catorce pasadas de 2026 difieren más de 10 cm entre las dos fuentes y tres difieren más de
30 cm. La frase "ambas fuentes coinciden con una diferencia media de 3 cm" sobrevende el
acuerdo. Lo que sí se sostiene es lo que el informe concluye a continuación: que el orden de
las pasadas por marea es prácticamente el mismo con una u otra (ρ 0,95). Este mismo hecho
explica por qué la Tabla 4 cambia poco al cambiar de serie.

---

## Verificación de constantes externas

| Constante | Reportado | Fuente consultada | Estado |
|---|---|---|---|
| ALOS-2 L2.2 en Earth Engine: dB = 10·log10(DN²) − 83 | −83 | Catálogo de Earth Engine, `JAXA/ALOS/PALSAR-2/Level2_2/ScanSAR`, y páginas de Cal/Val de JAXA EORC | **coincide en la constante** |
| Magnitud radiométrica del producto ALOS-2 L2.2 | implícitamente "sigma cero" en las Tablas 2 y 3 | la documentación define la ecuación como **γ0 = 10·log10(DN²) − 83,0 dB**, es decir gamma cero con corrección radiométrica de terreno | **difiere** en la etiqueta |
| Magnitud radiométrica de NISAR GCOV | "sigma cero" en los pies de las Tablas 2 y 3 | la guía de usuario de NISAR describe GCOV como potencia **gamma cero** con RTC aplicada | **difiere** en la etiqueta |

La etiqueta correcta para las Tablas 2 y 3 es gamma cero, no sigma cero. El error no toca
ninguna conclusión, porque todos los estadísticos del informe son comparaciones dentro de un
mismo sensor y una misma traza (correlaciones temporales y restas manglar menos bosque), donde
la elección de convención radiométrica se cancela. Pero afecta a la comparación de niveles
absolutos entre sensores y sitios, que sí aparece en el texto (la frase de los 3,5 dB entre
Pacífico y CGSM), y sobre todo compromete la comparabilidad con la literatura.

### Predicción armónica propia

Reajusté once constituyentes (M2, S2, N2, K2, K1, O1, P1, Q1, Mf, Mm, M4) por mínimos cuadrados
sobre el registro horario de `uhslc_h085_buenaventura.csv` filtrado a 2010-2013 (16.758 horas
válidas tras descartar el centinela −32767), y validé sobre 2014 (7.950 horas).

| Ítem | Reportado | Obtengo | Estado |
|---|---|---|---|
| Número de constituyentes | 11 | 11 reproducen el resultado | coincide |
| Periodo de ajuste | 2010-2013 | 2010-2013 | coincide |
| Amplitud de M2 | 1,51 m | **1,513 m** | coincide |
| Amplitud de S2 | 0,41 m | **0,406 m** | coincide |
| RMSE de validación en 2014 | 0,15 m | **0,158 m** (0,154 m tras quitar el sesgo medio) | coincide |
| Rango observado en 2014 | 5,24 m | **5,24 m** (de −0,462 a 4,778 m) | coincide |
| Estación UHSLC 085, registro 1953-2014 | 1953 a 2014 | 1953-05-12 a 2014, 540.336 horas, 485.945 válidas | coincide |

Este bloque es el más contundente de la auditoría: reproduje la predicción armónica desde el
mareógrafo crudo, sin ver el código, y recuperé las dos amplitudes publicadas con tres cifras y
el error de validación con dos.

---

## Juicio final

Lo que está sólidamente reproducido. Siete de las nueve tablas salen exactas desde los datos
crudos con código independiente. Las Tablas 2, 3, 7, 8 y 9 se reproducen ítem por ítem sin una
sola diferencia fuera de tolerancia, y las Tablas 5 y 6 se reproducen en todos sus estadísticos
(solo fallan metadatos horarios y una diferencia en dB de 0,075). La cadena de marea es el
tramo mejor construido del trabajo: la reconstrucción de la tabla DIMAR desde el CSV original
sale con RMSE de 0,0003 m y ρ de 1,000000, la interpolación a la hora de la pasada es exacta a
cinco decimales en las 24 pasadas, el convenio UTC−5 se confirma por tres vías independientes,
y la predicción armónica propia se rederiva desde el mareógrafo UHSLC con M2 = 1,513 m,
S2 = 0,406 m y RMSE de validación de 0,158 m, contra los 1,51, 0,41 y 0,15 publicados. La
Tabla 9, que es la que sostiene el argumento principal en la CGSM, se reproduce entera,
incluida la decisión no documentada de excluir las seis pasadas de Sentinel-1 que caen dentro
del hueco de 18 días de la serie del IDEAM, decisión que llegué a inferir sola porque es la
única que devuelve n = 55 y n = 58. Los conteos de pasadas cuadran entre tablas y CSV en las
nueve comprobaciones que se pueden hacer, y la formación de tercios con k = n // 3 se confirma
en las tres filas de la Tabla 9.

Lo que difiere y por qué. La discrepancia de fondo está en la Tabla 4, y es de procedencia, no
de aritmética: veintiún valores de ρ y p no se reproducen con la serie de marea que el propio
informe declara (DIMAR desde enero de 2026), pero se reproducen todos, con error de 0,003 por
celda, si se usa la predicción armónica propia en las 24 pasadas. Las dieciocho diferencias en
dB coinciden con ambas series porque la partición en mitades no cambia; lo que cambia es el
orden de rango de un par de pasadas vecinas. La Tabla 4 publicada es, por tanto, una corrida
anterior al cambio de fuente de marea, y quedó sin actualizar cuando se incorporó DIMAR; el
CSV `marea_vs_radar.csv` sí contiene los valores nuevos. Nada del argumento se mueve: los seis
estadísticos que lo sostienen coinciden con ambas series. El segundo problema real es la frase
"ambas fuentes coinciden con una diferencia media de 3 cm": los 3 cm son el sesgo, pero la
diferencia media absoluta es de 20 cm y llega a 41 cm en una pasada, de modo que la frase
sobrevende el acuerdo entre DIMAR y la predicción propia. El tercero es de etiqueta
radiométrica: tanto NISAR GCOV como ALOS-2 L2.2 se distribuyen en gamma cero con corrección de
terreno, no en sigma cero como dicen los pies de las Tablas 2 y 3; la constante −83 es correcta
y está bien citada, pero la documentación de JAXA la define explícitamente para γ0. El resto
son imprecisiones menores que conviene corregir antes de entregar: la Tabla 1 llama
descendentes a las 17 escenas de la CGSM cuando cinco son ascendentes, y fecha en noviembre de
2025 unas pasadas que empiezan el 29 de octubre; el informe declara horas locales minoritarias
en tres casos y se contradice a sí mismo entre la Tabla 7 y la Tabla 9; las "39 pasadas en dos
trayectorias descendentes" de ALOS-2 incluyen tres de una tercera trayectoria ascendente; la
afirmación de que las cinco primeras fechas varían menos de 1 dB no se cumple para el agua, que
varía 1,70 dB en HH; y la de que el manglar solo en GMW es 1,5 a 2 dB más oscuro exagera un
contraste que en realidad va de 0,9 a 2,0 dB con mediana de 1,3.

Lo que no pude verificar. Once ítems quedan fuera de alcance porque su insumo no está en la
carpeta. Los inventarios de escenas de la Tabla 1 (58 escenas de ALOS-2 y 164 de Sentinel-1
sobre Málaga, 9 escenas de NISAR en disco, 72 escenas mosaicadas en 57 pasadas) no tienen
respaldo en ningún CSV, y además la cifra de 58 contradice la de 72 del cuerpo del texto; solo
puedo confirmar las 39 pasadas de ALOS-2 y las 89 de Sentinel-1 con cobertura completa. Las
superficies de manglar de Global Mangrove Watch y WorldCover (6.006, 7.576 y 5.326 ha) no están
en ningún archivo, aunque los porcentajes derivados sí son aritméticamente consistentes. La
estratificación por ángulo de incidencia de la Figura 3 solo se puede contrastar contra su
propia salida derivada, porque los puntos individuales con su incidencia no se guardaron; el
contraste texto contra CSV sale limpio en las ocho afirmaciones cuantitativas, con la única
salvedad de que los puntos de manglar son 1.232 y 1.212, no 1.200. La asignación de las doce
pasadas de NISAR a las colecciones Beta y Provisional, que es la limitación central declarada
en el último párrafo del informe, no consta en ningún archivo y no pude comprobarla. Tampoco la
procedencia ERA5-Land de la columna `p30`, ni los conteos de Dynamic World. Por último, una
observación que el informe no hace y que conviene registrar: la serie del IDEAM que sostiene la
Tabla 9 mezcla dos juegos de coordenadas bajo el mismo código de estación (10,8339 / −74,7429
para "Remolino" y "Remolino - AUT", y 10,776 / −74,7437 para "Remolino - MAG"), y el archivo
descargado incluye además una segunda estación, Tebsa Barranquilla, que hay que filtrar. Los
resultados son correctos porque el filtro se aplicó, pero la ambigüedad de coordenadas dentro
del mismo código merece una nota en el informe final.
