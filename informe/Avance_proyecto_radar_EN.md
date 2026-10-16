Universidad Nacional de Colombia
Master's Programme in Geomatics
Radar and LiDAR Remote Sensing, 2026-2
Lina María Quintero Fonseca
L-band response to flooding beneath the mangrove canopy: comparison with C-band in the Ciénaga Grande de Santa Marta and Bahía de Málaga

## Abstract

Flooding beneath the mangrove canopy is a wetland condition that C-band radars record poorly, because the wave barely penetrates a dense canopy. L-band, with a wavelength of 23 cm, penetrates further into the canopy and can record the double bounce between the trunks and the water surface. To establish what this band contributes, NISAR and ALOS-2 were compared with Sentinel-1 in Bahía de Málaga, where flooding responds to the tide, and in the Ciénaga Grande de Santa Marta (CGSM), where it is linked to the level of the Magdalena River. The reading rule was fixed before the analysis: if L-band responds to water beneath the canopy, the co-polarised backscatter of the mangrove should increase with the hydrological forcing without an equivalent response in the control forest. In Bahía de Málaga this pattern was observed on both NISAR tracks and in ALOS-2, with an increase of 0.57 dB of the mangrove relative to the forest in HH, whereas Sentinel-1 and the cross-polarised channel did not respond. The result holds after correction for temporal dependence. In the CGSM, the mangrove-minus-forest difference rose by 0.83 dB between low and high river level, but the two groups belong to different NISAR product versions and within each version there is no relationship with the level, so the effect cannot be identified with the current acquisitions. An own 720-point sample showed greater separability between intact and degraded mangrove in L-band than in C-band (0.78 versus 0.26, still below the threshold of 1), although neither band separated degraded mangrove from herbaceous wetland. Finally, mapping at 50 m concentrated the HH increase in the southern mangrove, at the mouth of the Fundación River. Water level measured inside the wetland and NISAR passes at high and low level within a single product version remain pending.

Keywords: synthetic aperture radar, L-band, NISAR, mangrove, flooding beneath the canopy, double bounce, Ciénaga Grande de Santa Marta, Bahía de Málaga.

## 1. Introduction

The global flood monitoring product of the Copernicus Emergency Management Service processes Sentinel-1 in C-band, but excludes from detection the surfaces where the interaction of microwaves with the terrain is complex, among them dense vegetation (Expert Flood Monitoring Alliance, 2022, section 4.4). Consequently, flooding beneath the mangrove canopy falls, by design, outside what that product reports. L-band, with a wavelength of 23 cm, penetrates further into the canopy and can record the interaction between the trunks and the water surface.

Double bounce as a backscatter mechanism in flooded forest has been known since the first orbital L-band observations. Richards et al. (1987) attributed the increase in co-polarised backscatter to double bounce between the trunks and the water surface, and Hess et al. (1990) gathered the evidence that this enhancement weakens at shorter wavelengths. Over mangrove, Lucas et al. (2014) showed with ALOS PALSAR that L-band contributes to mapping its extent and its changes, the line of work from which Global Mangrove Watch emerged (Bunting et al., 2022). However, those studies did not address the monitoring of flooding beneath the canopy with regular sampling every few days.

NISAR, with a twelve-day repeat cycle and a systematic acquisition plan (NASA ASF DAAC, 2026a, 2026b), offers that sampling. Its choice as the main L-band sensor responds to that frequency and to the temporal continuity available over the CGSM. ALOS-2 provides an independent reference in the same band and makes it possible to corroborate the response observed in Bahía de Málaga, but its coverage over the lagoon during the analysed period is limited to ten passes, seven of them complete, which is insufficient to evaluate the response per track. NISAR, by contrast, makes it possible to relate backscatter to changes in the hydrological forcing within a single acquisition geometry. Therefore, ALOS-2 is used as independent corroboration and not as a substitute for the main time series.

In the Ciénaga Grande de Santa Marta, hydrology is the central problem. The obstruction of the channels that connect it to the Magdalena River produced the hypersalinisation and mass mangrove mortality of the 1980s and 1990s, and rehabilitation consisted of reopening that connection (Botero and Salzwedel, 1999). Simard et al. (2008) mapped the mangrove of the lagoon in three dimensions with SRTM, ICESat and field data, and Jaramillo et al. (2018) assessed the hydrological connectivity of the wetland with interferometric radar observations. None of those studies measured the temporal response of L-band backscatter to flooding beneath the canopy.

To fill that gap, this report compares NISAR and ALOS-2 in L-band with Sentinel-1 in C-band, with Bahía de Málaga as a tidal contrast site and the CGSM as a system linked to the level of the Magdalena River. The question is what additional information L-band provides, relative to Sentinel-1, for identifying flooding conditions beneath the mangrove canopy in the CGSM. To answer it, the backscatter response of representative land covers is characterised in both bands, that response is compared across mangrove zones with different flooding conditions and, finally, the differences are interpreted in terms of surface, volume and double-bounce scattering mechanisms.

## 2. Data and methods

### 2.1 Design and study sites

The CGSM was taken as the main site and Bahía de Málaga (Buenaventura), on the Colombian Pacific coast, as the contrast site. In the lagoon the hydrological condition was characterised with the level of the Magdalena River and, as a first step, with antecedent precipitation, and in Bahía de Málaga with the tide. This difference makes it possible to establish whether the L-band response holds under two different forcings.

Four land covers were analysed: open water, herbaceous wetland, mangrove and a control forest that does not flood. NISAR and ALOS-2 in L-band and Sentinel-1 in C-band were used over comparable periods, with 45 NISAR scenes in total, 21 over the lagoon and 24 over Bahía de Málaga (Table 1). The comparison was made within each track or orbit, by polarisation, land cover and hydrological condition, with the incidence angle stated. Subsequently, the interpretation by land cover was checked against an own 2025 reference sample, the spatial distribution of the signal was mapped at 50 m and Dynamic World served as an optical contrast.

### 2.2 SAR data

Table 1. Inventory of SAR acquisitions used in the CGSM and Bahía de Málaga, by sensor and track.

| Site | NISAR GCOV (HH, HV, 10 m) | ALOS-2 ScanSAR (HH, HV, 25 m) | Sentinel-1 GRD (VV, VH, 10 m), Oct-2025 to Sep-2026 |
|---|---|---|---|
| CGSM | 21 scenes, 14 descending (track 083) and 7 ascending (track 007), Oct-2025 to Sep-2026, no coverage between Feb and May 2026 | 2025–2026 series in Earth Engine, 10 passes, 7 complete | 119 passes with full coverage (58 on orbit 77 and 61 on orbit 142) |
| Bahía de Málaga | 24 scenes fully covering the mangrove: 12 ascending (track 004, 05:46 local) and 12 descending (track 087, 18:29 local), Oct-2025 to Sep-2026 | 72 scenes with HH and HV, Jan-2025 to Sep-2026, mosaicked into 57 passes, 39 with full coverage | 89 passes with full coverage (26 on orbit 48 and 63 on orbit 142) |

In all cases, only the passes covering the full site box were included. In Bahía de Málaga the two NISAR tracks differ in time and geometry, so they sample different tidal states, and temporal comparisons were made within each track. The same separation by track or orbit was kept for the other sensors. Over the lagoon, the 21 NISAR scenes are 14 from descending track 083 (18:27 local time) and seven from ascending track 007 (05:31). The six from October 2025 to January 2026 belong to the Beta collection of the product and the fifteen from June to September 2026 to the Provisional collection.

### 2.3 SAR processing and analysis workflow

Processing was carried out in Python and Google Earth Engine (Gorelick et al., 2017). The NISAR GCOV scenes (NASA ASF DAAC, 2026a, 2026b) were located in the CMR catalogue and subset remotely with earthaccess and h5py. Sentinel-1 (Torres et al., 2012), ALOS-2 PALSAR-2 ScanSAR (JAXA EORC, n.d.), the global land cover products, Sentinel-2 and ERA5-Land (Muñoz-Sabater et al., 2021) were processed through the Earth Engine Python interface.

Preprocessing was defined per sensor. NISAR was converted from terrain-corrected gamma nought to sigma nought with the factor supplied in the product and kept its incidence angle grid. ALOS-2 was calibrated with the JAXA constant (σ⁰ = 10·log10(DN²) − 83 dB) and mosaicked by pass and track. Sentinel-1 GRD was used with the thermal noise removal, radiometric calibration and terrain correction that Earth Engine applies on ingestion, without terrain flattening or speckle filtering (Google, n.d.).

Extraction was performed after conversion to decibels, with a spatial average of 3 × 3 pixels for NISAR and the native pixel for ALOS-2 and Sentinel-1. Each pass kept its track, direction, local time and incidence, and the tracks were analysed separately because geometry alone shifts the level by up to 1.4 dB in HH (Table 2). Figure 1 summarises the analytical design. The full nine-stage workflow and the per-sensor chain, following the convention of the SAR workflows of De Luca et al. (2021) and Yordanov and Brovelli (2021), are given in Appendix A.

![Figure 1. Methodological workflow of the study, from the input data and SAR preprocessing to the hydrological tests and the cartographic products.](fig_flujo_metodologico.png)

### 2.4 Reference covers and sampling

In the absence of interpreted points and field stations in Bahía de Málaga, the reference covers were defined with WorldCover 2021 (Zanaga et al., 2022) and Global Mangrove Watch 2020 (Bunting et al., 2022). Water, forest and herbaceous wetland come from WorldCover, and mangrove was restricted to the areas where the two products coincide.

In Bahía de Málaga, Global Mangrove Watch maps 6,006 ha of mangrove and WorldCover 7,576 ha, and the two coincide over 5,326 ha. The areas identified only by Global Mangrove Watch show backscatter between 0.9 and 2 dB lower and signatures close to those of herbaceous wetland, so they were not used as mangrove reference. In the CGSM the consensus covers 33,173 ha, and the control forest corresponds to dry forest on the eastern and southern margins, outside the floodplain (Figure 2).

![Figure 2. Reference covers in the CGSM: (a) WorldCover 2021 classes; (b) agreement between the mangrove mapped by WorldCover 2021 and Global Mangrove Watch 2020.](fig_cgsm_referencia.png)

At both sites, 400 points per class were selected by stratified sampling in Earth Engine (seed 42), generated once and shared by the three sensors. The control forest of the CGSM was sampled over the extended box of the data cube (4,304 km²), since the dry forest of the foothills lies outside the 2,042 km² study area.

### 2.5 Hydrological forcings

In Bahía de Málaga, the tidal height at each acquisition was obtained from the DIMAR forecast for 2026 (Dirección General Marítima, n.d.), interpolated between high and low waters and referenced to the annual mean level. For the ten passes from October to December 2025, a harmonic prediction fitted to the historical Buenaventura tide gauge was used (Caldwell et al., 2015). In 2026 the two sources showed a Spearman correlation of 0.95, a mean bias of 0.03 m and a root mean square error of 0.24 m.

In the CGSM, the precipitation accumulated over the 30 days before each acquisition, from ERA5-Land (Muñoz-Sabater et al., 2021), was used first, with the twelve descending passes prior to 11 September 2026, the date up to which that series extends. The hourly level of the Magdalena River at the IDEAM automatic Remolino gauging station (IDEAM, n.d.), interpolated to the time of each pass, was subsequently incorporated, which brings in all fourteen descending passes and the seven ascending ones.

The SAR response was evaluated with the mangrove-minus-forest difference, the contrast between the high and low states of the forcing and the Spearman correlation. River level and antecedent precipitation are associated (ρ 0.70, p 0.01), so the two tests are interpreted as related indicators and not as independent evidence.

### 2.6 Reading rule and robustness

The rule was defined before the analysis: if L-band responds to water beneath the canopy, within a single track an increase in the co-polarised backscatter of the mangrove and in HH − HV with the hydrological forcing is expected, without an equivalent response in the cross-polarised channel or in the non-flooded forest.

Each pass was reduced to the median per class and to the mangrove-minus-forest difference, which controls for the temporal variations shared by the two covers. In Bahía de Málaga the upper and lower halves of the tidal distribution were compared, and in the CGSM the upper and lower terciles of river level. Robustness was assessed against the incidence angle, in terciles of the angular range, against temporal dependence and against the NISAR product version. The effective sample size was estimated following Pyper and Peterman (1998), with lags up to n/5, and the p values were recalculated with it.

The co-polarised mangrove-minus-forest difference against the forcing, by track, was declared the primary statistic of each site, and the family of primary tests comprises the five L-band series: NISAR A004 and D087 and ALOS-2 139 and 140 in Bahía de Málaga, and NISAR D083 in the CGSM. The Holm (1979) correction was applied to the p values corrected for temporal dependence. In addition to the difference between halves or terciles, the slope of the difference against the forcing was estimated in dB per metre of tide or river level by least squares, with a 95% confidence interval from a bootstrap of passes (5,000 replicates) and with the Theil-Sen estimator (Sen, 1968) as a robust check. The C-band tests and track A007 are declared exploratory. To separate the mangrove edge from its interior, the co-polarised change between periods was also summarised by the distance of each 50 m pixel to the mangrove edge and to open water, computed with the distance transform on the reference mask (`pendientes_auditoria.py`).

### 2.7 Interpretation key and assessment with the reference sample

The key integrates the multi-date signatures of the co-polarised channel, the cross-polarised channel and their difference in both bands. It was assessed with an own 720-point sample distributed across six classes: open water, intact mangrove, floating vegetation, degraded mangrove, herbaceous wetland and other.

Separability between pairs of classes was quantified with the Jeffries-Matusita distance, derived from the Bhattacharyya distance under a Gaussian assumption (Richards, 2013), with two variables per band, the co-polarised and the cross-polarised channel, and four with both bands; the co-polarised minus cross-polarised difference is excluded because it is a linear combination of the other two and leaves the covariance singular. The thresholds were defined and evaluated on the same sample, so the agreement with the reference corresponds to resubstitution and not to an independent validation.

The points were drawn outside a validation reserve defined in advance, with a minimum separation of 200 m, and labelled blind on high-resolution 2025 imagery, with the first 400 reviewed under a written criterion and an edge flag when the 3 × 3 pixel window mixes classes (Figure 3).

![Figure 3. 2025 reference sample in the CGSM: 720 points distributed across six classes, validation reserve and 12 km blocks of the spatial validation design.](fig_muestra_2025.png)

### 2.8 Signal mapping and optical contrast

The signal was mapped with pixel-by-pixel differences at 50 m in UTM 18N. In the CGSM, the six high-level NISAR D083 acquisitions were compared with the eight low-level ones, groups that coincide with the Beta and Provisional collections, and Sentinel-1 used the same date windows with 13 and 18 passes from orbit 142.

In Bahía de Málaga, each track compared the six acquisitions with the highest tide with the six with the lowest tide. As an optical contrast, the `flooded_vegetation` probability of Dynamic World V1 (Brown et al., 2022) was used on the dates with at least half of the mangrove free of cloud, with the per-pixel median over the same NISAR windows and at least two valid observations per group. Dynamic World is interpreted as an indicator of flooded vegetation visible in optical imagery and not as an observation of water beneath the canopy.

## 3. Results

### 3.1 Backscatter profile in Bahía de Málaga

The first five acquisitions of track A004 showed a stable signal within each land cover. The variation in HH was below 1 dB in mangrove, forest and herbaceous wetland, and larger in open water. The mangrove identified only by Global Mangrove Watch was about 1.2 dB darker in HH and 1.5 dB darker in HV than the consensus mangrove, and approached the herbaceous wetland. The values of those five acquisitions are presented in Table B1.

Across the 24 acquisitions, the mangrove kept a low temporal variability within each track, with standard deviations of 0.3 dB in HH for A004 and 0.4 dB for D087 (Table 2). Absolute levels differ between tracks, with a median incidence of 42° in A004 and 35° in D087, and they are therefore analysed separately. In D087 the mangrove was 0.6 dB above the forest in HH and 1.1 dB above it in HH − HV, while in A004 both were equal in HH and the mangrove was 0.7 dB higher in HH − HV.

Table 2. Median and standard deviation of σ⁰ by land cover and track for the 24 NISAR acquisitions over Bahía de Málaga, in dB.

| Land cover | Track (local time, incidence) | HH (sd) | HV (sd) | HH−HV (sd) |
|---|---|---|---|---|
| Mangrove (consensus) | A004 (05:46, 42°) | −7.4 (0.3) | −14.2 (0.7) | 6.6 (0.7) |
| Mangrove (consensus) | D087 (18:29, 35°) | −8.2 (0.4) | −13.9 (0.7) | 5.6 (0.5) |
| Forest | A004 | −7.4 (0.2) | −13.4 (0.5) | 5.9 (0.4) |
| Forest | D087 | −8.8 (0.4) | −13.2 (0.7) | 4.5 (0.5) |
| Herbaceous wetland | A004 | −9.4 (0.3) | −16.8 (0.9) | 6.7 (0.5) |
| Herbaceous wetland | D087 | −8.7 (0.5) | −14.3 (1.0) | 5.7 (0.5) |
| Water | A004 | −19.1 (0.7) | −25.7 (0.9) | 5.9 (0.6) |
| Water | D087 | −18.5 (1.0) | −25.5 (1.1) | 7.0 (1.2) |

Between the November to January acquisitions and the June to September acquisitions, HV increased by 1 to 1.8 dB in all land covers, including water. Because this variation coincides with the transition between the Beta and Provisional collections, it is not attributed solely to seasonal changes. Figure 4 shows the composites of the two tracks and the spatial difference in HH.

![Figure 4. NISAR GCOV composites of Bahía de Málaga for tracks A004 and D087 (R = HH, G = HV, B = HH − HV) and HH difference between the two acquisition geometries.](fig_malaga_radar.png)

### 3.2 Tide and L-band mangrove backscatter: NISAR

The mangrove HH signal relative to the forest increased with tidal height in both A004 (ρ 0.83, p 0.001) and D087 (ρ 0.74, p 0.006), with a difference of +0.57 dB between high and low tide in both tracks (Table 3, Figure 5). HH − HV showed a response in the same direction, whereas HV showed no association with the tide.

Table 3. Relationship between tidal height and NISAR backscatter by track.

| Track | Variable | Mangrove: high − low (dB), ρ, p | Forest: high − low (dB), ρ, p | Mangrove − forest: high − low (dB), ρ, p |
|---|---|---|---|---|
| A004 | HH | +0.28, 0.76, 0.004 | −0.11, −0.09, 0.78 | +0.57, 0.83, 0.001 |
| A004 | HV | −0.36, −0.11, 0.73 | −0.31, −0.13, 0.70 | +0.03, 0.11, 0.73 |
| A004 | HH−HV | +0.76, 0.53, 0.08 | +0.31, 0.20, 0.53 | +0.45, 0.83, 0.001 |
| D087 | HH | −0.02, 0.25, 0.44 | −0.49, −0.36, 0.25 | +0.57, 0.74, 0.006 |
| D087 | HV | −1.26, −0.41, 0.18 | −1.30, −0.50, 0.10 | +0.07, −0.06, 0.85 |
| D087 | HH−HV | +0.88, 0.76, 0.005 | +0.44, 0.13, 0.68 | +0.61, 0.60, 0.04 |

The forest showed no equivalent response. The pattern was concentrated in the co-polarised channel and is consistent with an increased double-bounce contribution in the flooded mangrove (Richards et al., 1987; Hess et al., 1990). Although the effect was small, close to 0.6 dB, its repetition in two independent tracks allows it to be distinguished from a geometry difference.

![Figure 5. Mangrove and forest backscatter against the tidal height assigned to each NISAR acquisition, by track.](fig_marea_vs_radar.png)

Stratification by incidence angle preserved the direction of the response: HH relative to the forest increased between low and high tide in all six terciles (+0.27 to +0.77 dB, ρ from 0.48 to 0.97), with p below 0.05 in five of them, whereas HV did not respond in any (Figure 6). The available angular range, from 42° to 43° in A004 and from 34° to 37° in D087, makes it possible to verify that the signal does not change sign with the local geometry, but not to estimate its dependence on angle.

![Figure 6. Mangrove response relative to the forest by incidence angle tercile in NISAR tracks A004 and D087.](fig_doble_rebote_incidencia.png)

### 3.3 Comparison with C-band Sentinel-1

The same test was applied to the 89 Sentinel-1 acquisitions with full coverage, 26 from ascending orbit 48 and 63 from descending orbit 142. The mangrove signal relative to the forest showed no relationship with the tide in VV, VH or VV − VH in either orbit (Table 4, Figure 7).

Table 4. Relationship between tidal height and mangrove backscatter relative to the forest in Sentinel-1.

| Orbit (local time, n) | VV | VH | VV−VH |
|---|---|---|---|
| 48 ascending (18:21, 26) | −0.07 dB, ρ −0.18, p 0.37 | −0.11 dB, ρ −0.30, p 0.14 | +0.16 dB, ρ 0.23, p 0.26 |
| 142 descending (05:50, 63) | −0.07 dB, ρ −0.13, p 0.32 | 0.00 dB, ρ −0.08, p 0.55 | −0.15 dB, ρ −0.15, p 0.24 |

Although the mangrove alone showed a negative correlation in VV for orbit 142 (ρ −0.39, p 0.002), this association disappeared once the forest was subtracted and had the opposite sign to that observed in L-band HH. The comparison does not fully separate wavelength from polarisation, since Sentinel-1 observes VV and NISAR observes HH.

![Figure 7. Sentinel-1 mangrove and forest backscatter against tidal height, by relative orbit.](fig_s1_marea.png)

### 3.4 Corroboration with L-band ALOS-2

A total of 72 ALOS-2 PALSAR-2 ScanSAR scenes between January 2025 and September 2026 were analysed, grouped into 57 passes, of which 39 covered the full area. The analysis focused on descending tracks 139 (21 passes) and 140 (15 passes), both acquired around midday.

ALOS-2 reproduced the NISAR pattern (Table 5, Figure 8). The mangrove HH signal relative to the forest increased with the tide in both tracks, with ρ 0.65 (p 0.002) and ρ 0.72 (p 0.002). HH − HV likewise showed positive associations, whereas HV did not show the same response. In path 139, HV decreased with the tide in both mangrove and forest (ρ −0.66 and −0.62), a shared seasonal variation in midday passes that the difference removes.

Table 5. Relationship between tidal height and mangrove backscatter relative to the forest in ALOS-2 PALSAR-2.

| Path (local time, n) | HH | HV | HH−HV |
|---|---|---|---|
| 139 descending (11:53, 21) | +0.25 dB, ρ 0.65, p 0.002 | +0.06 dB, ρ 0.05, p 0.81 | +0.13 dB, ρ 0.47, p 0.03 |
| 140 descending (12:00, 15) | +0.49 dB, ρ 0.72, p 0.002 | −0.16 dB, ρ −0.45, p 0.10 | +0.91 dB, ρ 0.79, p < 0.001 |

Taken together, NISAR (ρ 0.83 and 0.74) and ALOS-2 (ρ 0.65 and 0.72) showed a positive association in the L-band co-polarised channel, which was absent in Sentinel-1 (ρ −0.18 and −0.13).

![Figure 8. ALOS-2 PALSAR-2 mangrove and forest backscatter against tidal height, by track.](fig_alos2_marea.png)

### 3.5 Ciénaga Grande: rainfall as forcing

A comparison between two NISAR Beta acquisitions showed that HH increased by a median of +0.43 dB over the mangrove between a date with the Magdalena at 1.69 m and another at 2.67 m, with the central 50% ranging from −0.42 to +1.28 dB (Figure 9). The negative signal over the lagoon corresponds to wind-driven roughness of the open water and not to flooding.

![Figure 9. NISAR GCOV over the CGSM, track D083: (a) 4 December 2025, Magdalena level of 2.67 m; (b) 9 January 2026, 1.69 m; (c) HH difference between the two dates.](fig_cgsm_radar.png)

The Sentinel-2 composites for those dates (Drusch et al., 2012), masked with Cloud Score+ (Pasquarella et al., 2023), showed no equivalent change at the surface: the median mangrove NDVI was 0.855 and 0.867, and open water occupied 39.7% and 39.2% of the valid area (Figure 10). Optical imagery distinguishes the main land covers but does not record water beneath a closed canopy.

![Figure 10. Comparison of Sentinel-2 and NISAR over the CGSM for the two dates of Figure 9. Sentinel-2 is shown in natural colour and colour infrared, and NISAR as a composite of HH, HV and HH − HV.](fig_cgsm_optico_radar.png)

Antecedent precipitation produced different responses in the two bands (Tables B2 and B3, Figure 11). In Sentinel-1, the dry forest responded to rainfall more strongly than the mangrove (ρ 0.52 and 0.58 against 0.32 and 0.21 in VV), so the mangrove-minus-forest difference was negative. In NISAR D083, forest HH did not respond (ρ 0.02), the mangrove showed ρ 0.50 and the mangrove-minus-forest difference reached ρ 0.58 (p 0.05), with no equivalent association in the cross-polarised channel. Partitioning by calendar into wet and dry seasons gave the opposite sign because, in this period, the dry-season passes had more antecedent rainfall than the wet-season passes.

However, this association can no longer be distinguished from chance once temporal dependence is corrected (section 3.7), and rainfall is only an indirect proxy for water level. It is therefore interpreted as a direction and not as evidence of the hydrological effect.

![Figure 11. Mangrove and forest backscatter against precipitation accumulated over the 30 days before each acquisition, by sensor and track.](fig_cgsm_temporada.png)

### 3.6 Ciénaga Grande: Magdalena River level

The Magdalena level at Remolino produced a stronger association with NISAR D083 (Table 6, Figure 12). Between the lower and upper level terciles, HH increased by +0.47 dB in the mangrove and decreased by −0.53 dB in the forest, and the mangrove-minus-forest difference increased by +0.83 dB, with ρ 0.83 (p < 0.001). The cross-polarised channel relative to the forest showed no equivalent relationship.

Table 6. Relationship between the Magdalena River level at Remolino and backscatter, by sensor and track. Sentinel-1 includes 55 and 58 passes, because three per orbit fall in an 18-day gap in the IDEAM series in August 2026.

| Sensor and pass | n | Class | Co-polarised (HH or VV) | Cross-polarised (HV or VH) | Ratio (HH−HV) |
|---|---|---|---|---|---|
| NISAR D083 (18:27) | 14 | Mangrove | +0.47 dB · ρ 0.58, p 0.03 | −0.97 dB · ρ −0.74, p 0.003 | +1.27 dB · ρ 0.77, p 0.001 |
| NISAR D083 (18:27) | 14 | Forest | −0.53 dB · ρ −0.39, p 0.16 | −1.29 dB · ρ −0.70, p 0.006 | +0.71 dB · ρ 0.71, p 0.005 |
| NISAR D083 (18:27) | 14 | Mangrove − forest | +0.83 dB · ρ 0.83, p < 0.001 | +0.35 dB · ρ 0.32, p 0.27 | +0.62 dB · ρ 0.49, p 0.08 |
| NISAR A007 (05:31) | 7 | Mangrove − forest | −0.14 dB · ρ −0.04, p 0.94 | −0.06 dB · ρ −0.39, p 0.38 | −0.30 dB · ρ −0.54, p 0.22 |
| Sentinel-1 A77 (18:06) | 55 | Mangrove − forest | −0.21 dB · ρ −0.47, p < 0.001 | +0.05 dB · ρ −0.01, p 0.95 | −0.08 dB · ρ −0.12, p 0.37 |
| Sentinel-1 D142 (05:48) | 58 | Mangrove − forest | −0.21 dB · ρ −0.33, p 0.01 | −0.14 dB · ρ −0.37, p 0.005 | −0.15 dB · ρ −0.18, p 0.18 |

Track A007 showed no association, but its seven acquisitions correspond to low or intermediate levels, between 0.82 and 1.58 m. Sentinel-1 showed the opposite behaviour, with the co-polarised channel relative to the forest decreasing with level, because forest VV rises with level (ρ 0.39 and 0.32) while mangrove VV does not.

However, the six high-level acquisitions, between 1.69 and 2.67 m, belong to the Beta collection and the eight low-level acquisitions, between 0.91 and 1.42 m, to the Provisional collection, because in 2026 the river fell much further than in 2025 for the same months. Within each version there is no association between level and HH relative to the forest: ρ −0.14 (p 0.79) in the six Beta acquisitions and ρ 0.55 (p 0.16) in the eight Provisional acquisitions. A joint regression attributes 0.12 dB per metre to level and −0.52 dB to the version change. The ρ of 0.83 is therefore produced by the step between the two blocks, and with the current series the hydrological effect cannot be identified separately. HV, moreover, decreases with level in both classes (ρ −0.74 and −0.70), which may be seasonal or due to the version.

![Figure 12. Mangrove and forest backscatter against the hourly Magdalena River level at Remolino, by sensor and track.](fig_cgsm_nivel_rio.png)

### 3.7 Temporal dependence of the correlations

Table 7. Correlation between the co-polarised mangrove-minus-forest signal and the hydrological forcing, before and after correcting for temporal dependence. The slope is that of the difference against the forcing, in dB per metre of tide or river level, with a 95% bootstrap interval; the Holm p adjusts the corrected p over the family of five primary L-band tests.

| Series | Track | n | ρ | p | r1 of forcing | r1 of radar | Effective n | Corrected p | Slope (dB/m) [95% CI] | Holm p |
|---|---|---|---|---|---|---|---|---|---|---|
| NISAR, Málaga, tide | A004 | 12 | 0.83 | 0.001 | 0.15 | −0.21 | 8.7 | 0.007 | 0.23 [0.15 to 0.38] | 0.033 |
| NISAR, Málaga, tide | D087 | 12 | 0.74 | 0.006 | −0.03 | −0.24 | 11.2 | 0.008 | 0.35 [0.20 to 0.52] | 0.033 |
| ALOS-2, Málaga, tide | 139 | 21 | 0.65 | 0.002 | 0.60 | 0.29 | 11.1 | 0.031 | 0.12 [0.05 to 0.18] | 0.063 |
| ALOS-2, Málaga, tide | 140 | 15 | 0.72 | 0.002 | 0.53 | 0.48 | 9.8 | 0.019 | 0.24 [0.09 to 0.57] | 0.057 |
| Sentinel-1, Málaga, tide | 48 | 26 | −0.18 | 0.37 | 0.23 | −0.25 | 26 | 0.37 | −0.07 [−0.19 to 0.05] | exploratory |
| Sentinel-1, Málaga, tide | 142 | 63 | −0.13 | 0.32 | −0.65 | 0.03 | 63 | 0.32 | −0.05 [−0.11 to 0.01] | exploratory |
| NISAR, CGSM, 30-day rainfall | D083 | 12 | 0.58 | 0.048 | 0.45 | 0.69 | 5.7 | 0.25 | — | exploratory |
| Sentinel-1, CGSM, 30-day rainfall | A77 | 58 | −0.35 | 0.008 | 0.89 | 0.14 | 21.1 | 0.12 | — | exploratory |
| Sentinel-1, CGSM, 30-day rainfall | D142 | 61 | −0.52 | < 0.001 | 0.89 | 0.32 | 24.7 | 0.009 | — | exploratory |
| NISAR, CGSM, river level | D083 | 14 | 0.83 | < 0.001 | 0.86 | 0.64 | 4.7 | 0.10 | 0.49 [0.34 to 0.71] | 0.104 |

The correction preserved the NISAR associations with the tide in A004 (corrected p 0.007) and D087 (0.008), because sampling every twelve days falls at different phases of the tidal cycle, and the ALOS-2 associations in tracks 139 (0.031) and 140 (0.019), whose 28-day sampling approaches the spring-neap cycle and reduces the effective sample size to about ten passes. Sentinel-1 remained without association. The product version does not explain the Málaga result either: within each Beta or Provisional block the difference keeps rising with the tide, with ρ of 0.89 and 0.90 in A004 and of 0.66 and 0.77 in D087.

In the CGSM, the NISAR relationship with precipitation went from p 0.048 to p 0.25, because thirty-day accumulated rainfall is a very smooth series. For river level, the two blocks of dates reduced the effective sample size from 14 to 4.7 observations and raised the p-value to 0.10. Consequently, the robust evidence comes from Bahía de Málaga, and in the CGSM the signal is consistent in direction but not identifiable against the temporal structure and the product version.

With the Holm correction over the five primary L-band tests, the two NISAR tracks in Bahía de Málaga held (p 0.033), ALOS-2 was borderline (0.063 and 0.057) and the CGSM did not pass (0.104); if the family is restricted to the four Málaga tests, all four pass (0.026 to 0.038). The slopes express the effect in units comparable between sites: 0.23 dB/m in A004 and 0.35 dB/m in D087 with NISAR, and 0.12 and 0.24 dB/m with ALOS-2, with intervals that exclude zero, against −0.07 and −0.05 dB/m in Sentinel-1, with intervals that include it. Over the observed tidal range, 2.3 to 3.4 m, the expected change of the difference is 0.4 to 0.8 dB. In the CGSM the NISAR D083 slope was 0.49 dB/m [0.34 to 0.71], but it contains the version step, and the Sentinel-1 slope was negative, −0.23 and −0.25 dB/m.

### 3.8 Interpretation key by land cover and mechanism

The initial signatures obtained with the land covers of the global products are presented in Table B4 and Figure 13. In C-band, mangrove and herbaceous wetland show almost coincident signatures, and in L-band their medians separate in HH and HH − HV, whereas floating vegetation remains closer to open water in L-band.

![Figure 13. Signature space of the CGSM land covers in C- and L-band, defined by co-polarised backscatter and the co-polarised minus cross-polarised difference.](fig_clave_firmas.png)

#### Evaluation with the 2025 reference sample

This study's own sample changed part of that interpretation (Table 8). The largest L-band improvement was observed between intact and degraded mangrove, whose separability increased from 0.26 in C-band to 0.78 in L-band, still below the threshold of 1 (Table 9). In contrast, herbaceous wetland and degraded mangrove remained practically inseparable, with 0.11 in C, 0.16 in L and 0.24 with both bands, as also occurs with the Sentinel-2 NDVI (0.44). Floating vegetation did not show a radar signature separable from water either (0.19 in L and 0.47 in C).

Table 8. Multi-date signatures of the 2025 reference sample classes in C- and L-band, in dB.

| Class | n | VV | VH | VV − VH | HH | HV | HH − HV | HH − HV, quartiles |
|---|---|---|---|---|---|---|---|---|
| Water | 212 | −21.5 | −29.6 | 7.5 | −19.9 | −25.4 | 5.9 | 5.0 to 6.5 |
| Floating vegetation | 129 | −15.2 | −22.7 | 6.7 | −17.0 | −23.7 | 6.8 | 5.6 to 7.8 |
| Intact mangrove | 151 | −9.5 | −14.8 | 5.5 | −10.0 | −16.7 | 6.6 | 6.0 to 7.4 |
| Degraded mangrove | 111 | −10.7 | −15.9 | 5.3 | −8.3 | −16.8 | 8.9 | 7.5 to 10.7 |
| Herbaceous wetland | 73 | −10.4 | −15.9 | 5.4 | −9.6 | −17.3 | 7.9 | 7.3 to 8.6 |
| Other | 44 | −10.1 | −15.4 | 6.0 | −10.7 | −18.3 | 7.5 | 6.6 to 8.6 |

The HH − HV difference ordered the land covers according to canopy openness: 6.6 dB in intact mangrove, 7.5 dB in the other class, 7.9 dB in herbaceous wetland and 8.9 dB in degraded mangrove. This variable characterises structure, but it does not by itself identify a class.

Table 9. Jeffries-Matusita separability between the 2025 reference sample classes, with the co-polarised and cross-polarised channel of each band (two variables per band and four with both bands).

| Pair | C-band | L-band | C + L |
|---|---|---|---|
| Water, floating vegetation | 0.47 | 0.19 | 0.60 |
| Water, herbaceous wetland | 1.38 | 1.21 | 1.55 |
| Water, degraded mangrove | 1.60 | 1.53 | 1.78 |
| Water, intact mangrove | 1.81 | 1.86 | 1.95 |
| Water, other | 1.43 | 1.19 | 1.60 |
| Floating vegetation, herbaceous wetland | 0.53 | 0.62 | 0.81 |
| Floating vegetation, degraded mangrove | 0.82 | 0.91 | 1.19 |
| Floating vegetation, intact mangrove | 1.20 | 1.47 | 1.65 |
| Floating vegetation, other | 0.50 | 0.67 | 0.85 |
| Herbaceous wetland, degraded mangrove | 0.11 | 0.16 | 0.24 |
| Herbaceous wetland, intact mangrove | 0.43 | 0.61 | 0.82 |
| Herbaceous wetland, other | 0.07 | 0.11 | 0.23 |
| Degraded mangrove, intact mangrove | 0.26 | 0.78 | 0.87 |
| Degraded mangrove, other | 0.23 | 0.43 | 0.58 |
| Intact mangrove, other | 0.51 | 0.43 | 0.73 |

#### Reading rule

The key was reduced to four decisions on the multi-date medians:

1. Open water: VV below −17 dB and VH below −25 dB in σ⁰ (−16.2 and −24.2 dB in γ⁰).
2. Dark surface with vegetation or edge: VV below −12 dB in σ⁰ (−11.2 dB in γ⁰) without meeting the previous condition, compatible with floating vegetation when VV − VH is 6.5 dB or more.
3. Closed canopy: VV of −12 dB or more in σ⁰ (−11.2 dB in γ⁰) and HH − HV below 7.3 dB.
4. Open or herbaceous canopy: VV of −12 dB or more in σ⁰ (−11.2 dB in γ⁰) and HH − HV of 7.3 dB or more, a group in which degraded mangrove, herbaceous wetland and part of the other class remain together.

The hydrological response complements the static signature to distinguish mangrove from non-flooded forest, since the level difference between the two classes (1.5 dB in VV and 1.7 dB in HH) is of the order of that produced by the geometry between tracks. The criterion is the change in the co-polarised channel with the hydrological forcing, observed in Bahía de Málaga and, subject to the stated confounding with product version, in the CGSM.

The rule decided 606 of the 720 points and agreed with the reference in 415, 68% of the decided cases and 58% of the sample (Table 10). Without the 208 edge points, it decided 444 of 512 and agreed with the reference in 71%. These figures correspond to resubstitution.

To measure what L-band contributes to the key, the decision between closed and open canopy was repeated with C-band alone, with VV − VH in place of HH − HV and the threshold chosen by the same resubstitution procedure, the balanced accuracy between intact mangrove and the three open-canopy classes. The best C-band threshold, VV − VH below 7.0 dB, reached a balanced accuracy of 0.54, barely above chance, against 0.75 with HH − HV, whose optimal threshold, 7.4 dB, matches the fixed 7.3 dB. With the C-band-only key the same 606 points were decided, but 340 agreed with the reference, 56% of the decided points and 47% of the sample, instead of 415: 78 of the 111 degraded mangrove points and 44 of the 73 herbaceous wetland points moved to closed canopy. The separation between closed and open canopy therefore depends on L-band.

Table 10. Classification of the 720 reference points with the SAR interpretation key (rows, reference class; columns, decisions 1 to 4 of the rule). Thresholds in σ⁰; with the equivalent γ⁰ thresholds (shifted by +0.83 dB, the median of γ⁰ − σ⁰ in C-band) the table is identical except for two cells, degraded mangrove 63 and other 19 under decision 4, with the same 606 decided points and 415 agreements.

| Reference class | 1 Open water | 2 Floating vegetation | 3 Intact mangrove | 4 Open or herbaceous canopy | No decision |
|---|---|---|---|---|---|
| Water | **159** | 7 | 5 | 5 | 36 |
| Floating vegetation | 42 | **27** | 14 | 25 | 21 |
| Intact mangrove | 0 | 0 | **107** | 32 | 12 |
| Degraded mangrove | 2 | 4 | 19 | **62** | 24 |
| Herbaceous wetland | 3 | 2 | 11 | **40** | 17 |
| Other | 2 | 3 | 15 | **20** | 4 |

### 3.9 Spatial distribution of the signal and optical contrast

In the CGSM, the difference between the six high-level acquisitions and the eight low-level acquisitions showed a marked spatial structure (Table 11, Figure 14). The mangrove as a whole had a median of +0.07 dB in HH, but the southern sector rose by +0.53 dB, with 77% of pixels positive. In Isla de Salamanca, to the north, where the Caño Clarín channel enters, the median was −0.18 dB, and the control dry forest decreased by −0.36 dB.

Table 11. Backscatter change between the high and low river-level periods, by land cover and mangrove sector, in dB.

| Class or sector | Pixels | ΔHH (L) | ΔHH > 0 | ΔHV (L) | Δ(HH − HV) | ΔVV (C) | ΔVV > 0 | ΔVH (C) |
|---|---|---|---|---|---|---|---|---|
| Mangrove, all | 145,398 | +0.07 (−0.47 to +0.63) | 53% | −1.13 | +1.21 | +0.09 (−0.15 to +0.33) | 61% | +0.01 |
| Northern mangrove, Isla de Salamanca (N > 1205 km) | 69,063 | −0.18 (−0.64 to +0.30) | 40% | −1.08 | +0.93 | +0.05 (−0.17 to +0.30) | 56% | −0.02 |
| Central and western mangrove (1190 to 1205 km) | 33,412 | +0.02 (−0.52 to +0.57) | 51% | −1.23 | +1.25 | +0.02 (−0.22 to +0.24) | 53% | +0.01 |
| Southern mangrove, mouth of the Fundación River (N < 1190 km) | 42,923 | **+0.53 (+0.05 to +0.99)** | **77%** | −1.15 | +1.66 | +0.21 (−0.01 to +0.39) | 74% | +0.06 |
| Dry forest (control) | 316,807 | −0.36 (−0.89 to +0.21) | 33% | −1.18 | +0.84 | **+0.36 (+0.13 to +0.63)** | **86%** | +0.21 |
| Herbaceous wetland | 207,215 | +0.46 (−0.54 to +1.82) | 62% | −0.96 | +1.41 | +0.26 (−0.22 to +0.80) | 65% | +0.31 |
| Open water | 663,486 | −0.39 (−0.89 to +0.02) | 26% | −1.21 | +0.73 | −0.47 (−1.08 to 0.00) | 25% | +0.62 |

The change was not concentrated at the mangrove edge (Table 12, Figure B1). In the southern sector, the median ΔHH grew with distance to the edge, from +0.31 dB in the first 50 m to +0.74 dB beyond 300 m, and the fraction of positive pixels rose from 64% to 91%, with a Spearman correlation of 0.21 between distance and change. In Isla de Salamanca the change was negative at every distance, between −0.13 and −0.26 dB. Mangrove pixels within 50 m of open water changed like water, −0.39 dB, which indicates mixed surfaces within the 50 m cell. In Bahía de Málaga the change in mangrove HH with the tide was the same from edge to interior, between +0.27 and +0.40 dB in A004 and between +0.02 and +0.13 dB in D087 across all distance bands. The co-polarised signal associated with the forcing therefore comes from the interior of the stand and not from its edges, which is consistent with double bounce beneath the canopy and not with an edge effect or with mixing with open water, which acted in the opposite direction.

Table 12. Change in mangrove HH between the high and low river-level periods (CGSM, NISAR D083) and between high and low tide (Bahía de Málaga) by distance of the 50 m pixel to the mangrove edge: median in dB and fraction of pixels with positive change.

| Site and sector | 0 to 50 m | 50 to 100 m | 100 to 200 m | 200 to 300 m | More than 300 m |
|---|---|---|---|---|---|
| CGSM mangrove, all | −0.07 (47 %) | +0.03 (52 %) | +0.08 (54 %) | +0.12 (57 %) | +0.34 (67 %) |
| Southern mangrove, Fundación River | +0.31 (64 %) | +0.46 (74 %) | +0.54 (79 %) | +0.58 (83 %) | +0.74 (91 %) |
| Central and western mangrove | −0.11 (45 %) | +0.01 (51 %) | +0.10 (55 %) | +0.22 (62 %) | +0.04 (53 %) |
| Northern mangrove, Isla de Salamanca | −0.26 (38 %) | −0.16 (40 %) | −0.13 (42 %) | −0.16 (40 %) | −0.20 (37 %) |
| Bahía de Málaga, A004, tide | +0.28 (71 %) | +0.39 (77 %) | +0.40 (79 %) | +0.39 (79 %) | +0.27 (71 %) |
| Bahía de Málaga, D087, tide | +0.02 (51 %) | +0.07 (55 %) | +0.06 (55 %) | +0.07 (55 %) | +0.13 (61 %) |

![Figure 14. Change in HH, HV and HH − HV from NISAR D083 between the high and low river-level periods, on a 50 m grid.](fig_mapa_doble_rebote.png)

The maximum increase was located at the mouth of the Fundación River, which descends from the Sierra Nevada, and not at the inlets of the Magdalena channels: when crossed with the OpenStreetMap watercourses, the hotspot lies 1.3 km from the Fundación, whereas the Caño Renegado channel ends to the west, 11 km from the mangrove, in a strip of smaller change. Therefore, the Remolino level acts in that sector as a regional indicator of the hydrological condition and not as a direct hydrological forcing. The herbaceous wetland also rose (+0.46 dB), which indicates that the co-polarised channel also responds to water or exposed soil outside the canopy. The sectors were delineated by latitude before the hydrography was checked, so the sector-level reading is a hypothesis for the next series.

HV decreased by about 1 dB in all land covers, including open water, so this signal is not attributed to flooding beneath the canopy and may reflect the product version or the season. The spatial comparison with Sentinel-1 showed a different pattern (Figure 15): in C-band the dry forest rose more than the mangrove (+0.36 versus +0.09 dB), whereas in L-band the mangrove rose and the forest fell, and the per-pixel correlation between ΔHH and ΔVV over the mangrove was weak (ρ 0.21).

![Figure 15. Co-polarised change between the same periods in NISAR (HH) and Sentinel-1 (VV), on a common 50 m grid.](fig_mapa_c_vs_l.png)

#### Contrast with Dynamic World

Dynamic World showed a relationship with river level in the herbaceous wetland (ρ 0.41, p 0.002, uncorrected for temporal dependence), but not in the mangrove (ρ 0.04) or in the forest (ρ −0.02). The spatial correlation between the change in `flooded_vegetation` and ΔHH over the mangrove was weak and negative (ρ −0.15): where the optical sensor sees more exposed water, HH decreases, and where it sees no change, HH increases (Figure 16). The pattern is compatible with a difference between exposed water and water beneath the canopy, but it does not constitute an independent validation of double bounce.

![Figure 16. Contrast between river level, the Dynamic World flooded vegetation probability and the NISAR HH change.](fig_corroboracion_dw.png)

#### Spatial distribution in Bahía de Málaga

The same comparison was repeated with the six highest-tide and the six lowest-tide acquisitions of each track (Table B5, Figure 17). In A004, HH rose by +0.34 dB in the mangrove and fell by −0.10 dB in the forest, and in D087 the changes were +0.05 and −0.39 dB. The forest decrease in D087 coincides with the product version, with four Beta passes in the high-tide group and four Provisional passes in the low-tide group, so the subtraction cancels that shift. The mangrove-minus-forest difference was +0.44 dB in both tracks, close to the +0.57 dB of the point sampling. The positive signal was distributed along the mangrove fringes of the bay, and HV fell in all land covers, so it was not used as an independent signature.

![Figure 17. Change in HH and HV between the six highest-tide and lowest-tide passes of each NISAR track in Bahía de Málaga, on a 50 m grid.](fig_mapa_doble_rebote_malaga.png)

## 4. Discussion

The strongest evidence in this study comes from Bahía de Málaga. Mangrove HH relative to forest increased with tide in both NISAR tracks and the same pattern was reproduced with ALOS-2, whereas Sentinel-1 did not show an equivalent response. The associations of the two L-band sensors persisted after correction for temporal dependence and, in NISAR, within each product version. In the CGSM the same direction was observed against river level, but the high and low states coincide with the Beta and Provisional collections, and the two effects cannot be separated with the available series.

The co-polarised change relative to forest was small, 0.4 to 0.8 dB, compared with the enhancements of several decibels described for other flooded forests in L-band (Hess et al., 1990). That difference may be related to attenuation by a dense mangrove canopy, to the partial presence of water within the pixel and to hydrological variability between acquisitions. In addition, dual polarisation prevents the mechanisms from being separated with full polarimetric observables, and the comparison between bands does not fully separate wavelength and polarisation either, since NISAR and ALOS-2 observe HH and Sentinel-1 observes VV. The results are compatible with a double-bounce contribution, but they do not constitute a direct polarimetric identification. However, the reproduction of the pattern in two L-band sensors and its absence in HV and in Sentinel-1 reduce the likelihood that the response is specific to one geometry or one sensor.

L-band also provided structural information. The separability between intact and degraded mangrove increased from 0.26 in C-band to 0.78 in L-band, and HH − HV responded mainly to canopy openness, so it characterises structure but does not serve as a single land-cover label. The boundary between degraded mangrove and herbaceous wetland remained unresolved with both bands. With C-band alone, the decision between closed and open canopy was at chance level, with a balanced accuracy of 0.54 against 0.75 with HH − HV, so that part of the key depends on L-band.

Finally, the spatial distribution showed that the response is not homogeneous. The largest HH increase was concentrated in the mangrove of the southern CGSM, at the mouth of the Fundación River, which indicates that the Magdalena level at Remolino acts as a regional indicator and not as a direct hydrological forcing of each sector, whereas Sentinel-1 showed a more diffuse pattern and a larger response in the dry forest. Within the mangrove, the change grew with distance to the edge of the stand in the southern sector and was the same from edge to interior in Bahía de Málaga, so the signal is not explained by an edge effect or by mixing with open water within the pixel, which acted in the opposite direction. Dynamic World responded to river level where water was visible to the optical sensor, but not beneath the mangrove, so it provides evidence on the forcing rather than a direct validation of the signal beneath the canopy.

### 4.1 Limitations

The study has four limitations. First, the data are dual-polarised, HH and HV in L-band and VV and VH in C-band, so the comparison combines wavelength and polarisation, and the mechanisms are inferred from intensity and its hydrological response.

Second, the NISAR series for the CGSM is still short and its hydrological states coincide with two product versions. Temporal dependence further reduces the effective sample size, so the relationship with river level cannot be considered conclusive. The absence of level measurements within the wetland prevents the SAR signal from being related directly to the local water surface, so the Magdalena level at Remolino is used as a regional indicator. These measurements were requested from INVEMAR, which reported that they are not available while the hydrosedimentological monitoring agreement with CORPAMAG remains in progress.

Third, the key was defined and evaluated with the same 720 points, so the 68% agreement with the reference corresponds to resubstitution and must be verified with an independent sample. In addition, the labels represent 2025 whereas the SAR observations span 2025–2026, so part of the disagreement may correspond to real land-cover changes.

Finally, the reference has intra-interpreter uncertainty. In a second blind interpretation of 60 points, agreement was 78% [66–87%], with κ = 0.72 (Figure 18). The greatest instability was concentrated in the herbaceous wetland, one of the classes that the sensors also fail to separate adequately.

![Figure 18. Consistency of the same interpreter on the 2025 reference sample, with a second blind interpretation of 60 points. Agreement 0.78 [0.66 to 0.87], kappa 0.72.](fig_consistencia_2025.png)

## 5. Conclusions and future work

In Bahía de Málaga, L-band showed a reproducible response of the mangrove co-polarised channel to the tide that did not appear in C-band. The pattern was observed in both NISAR tracks, was reproduced with ALOS-2, withstood correction for temporal dependence and held within each product version. The response was concentrated in HH and not in HV, and it was compatible with an increase in the double-bounce contribution under greater flooding. With the Holm correction over the five primary L-band tests, the two NISAR tracks in Málaga held and ALOS-2 was borderline; the slopes were 0.12 to 0.35 dB per metre of tide, with intervals that exclude zero, and the change was not concentrated at the edge of the stand.

In the CGSM the same direction was observed against river level, with an increase of +0.83 dB in mangrove HH relative to forest. However, the high and low states coincide with different NISAR versions, within each version there is no relationship with level, and the association does not withstand correction for temporal dependence. Therefore, the hydrological effect cannot yet be identified independently. L-band also improved the separation between intact and degraded mangrove, although it did not resolve the boundary between degraded mangrove and herbaceous wetland. The key decided 606 of 720 points with 68% agreement with the reference by resubstitution, which must be evaluated with an independent sample.

Future work focuses on extending the NISAR D083 series until high and low river states are available within a single product version, and on repeating the mapping with radiometrically comparable acquisitions. In addition, the response beneath the canopy will be evaluated with NISAR interferometric pairs, analysing coherence and phase in relation to the hydrological level. A consistent interferometric response would make it possible to test the proposed mechanism with information independent of backscatter intensity. Finally, the key must be evaluated with an independent sample that is temporally consistent with the SAR acquisitions. Full polarimetry at a longer wavelength remains a later extension.

## Data and code availability

The scripts for the nine stages, the tabulated results and the report figures are available in the public repository https://github.com/linaq11/cgsm-radar-banda-L, under the MIT licence. The NISAR scenes, the IDEAM and tide gauge series and the Earth Engine products are obtained from their sources with the stage 1 scripts. The 2025 reference sample is an in-house product still under development and is not distributed with the report.

## References

Botero, L. y Salzwedel, H. (1999). Rehabilitation of the Ciénaga Grande de Santa Marta, a mangrove-estuarine system in the Caribbean coast of Colombia. *Ocean & Coastal Management, 42*(2–4), 243–256. https://doi.org/10.1016/S0964-5691(98)00056-8

Brown, C. F., Brumby, S. P., Guzder-Williams, B., Birch, T., Hyde, S. B., Mazzariello, J., Czerwinski, W., Pasquarella, V. J., Haertel, R., Ilyushchenko, S., Schwehr, K., Weisse, M., Stolle, F., Hanson, C., Guinan, O., Moore, R. y Tait, A. M. (2022). Dynamic World, near real-time global 10 m land use land cover mapping. *Scientific Data, 9*, Artículo 251. https://doi.org/10.1038/s41597-022-01307-4

Bunting, P., Rosenqvist, A., Hilarides, L., Lucas, R. M., Thomas, N., Tadono, T., Worthington, T. A., Spalding, M., Murray, N. J. y Rebelo, L.-M. (2022). Global mangrove extent change 1996–2020: Global Mangrove Watch version 3.0. *Remote Sensing, 14*(15), Artículo 3657. https://doi.org/10.3390/rs14153657

Caldwell, P. C., Merrifield, M. A. y Thompson, P. R. (2015). *Sea level measured by tide gauges from global oceans: The Joint Archive for Sea Level holdings* (NCEI Accession 0019568, versión 5.5) [Data set]. NOAA National Centers for Environmental Information. https://doi.org/10.7289/V5V40S7W

De Luca, G., Silva, J. M. N. y Modica, G. (2021). A workflow based on Sentinel-1 SAR data and open-source algorithms for unsupervised burned area detection in Mediterranean ecosystems. *GIScience & Remote Sensing, 58*(4), 516–541. https://doi.org/10.1080/15481603.2021.1907896

Dirección General Marítima. (n.d.). [Pronóstico de pleamares y bajamares para Málaga, año 2026, Centro de Investigaciones Oceanográficas e Hidrográficas del Pacífico] [Data set]. DIMAR.

Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., Hoersch, B., Isola, C., Laberinti, P., Martimort, P., Meygret, A., Spoto, F., Sy, O., Marchese, F. y Bargellini, P. (2012). Sentinel-2: ESA's optical high-resolution mission for GMES operational services. *Remote Sensing of Environment, 120*, 25–36. https://doi.org/10.1016/j.rse.2011.11.026

Expert Flood Monitoring Alliance. (2022). *Provision of an automated, global, satellite-based flood monitoring product for the Copernicus Emergency Management Service: Product Definition Document (PDD)* (Documento GFM D6, versión 1.4). Copernicus Emergency Management Service. https://elib.dlr.de/195173/1/gfm_pdd_v1_4_20220420_edit.pdf

Google. (n.d.). *Sentinel-1 SAR GRD: C-band Synthetic Aperture Radar Ground Range Detected, log scaling* [Data set]. Earth Engine Data Catalog. https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD

Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D. y Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment, 202*, 18–27. https://doi.org/10.1016/j.rse.2017.06.031

Hess, L. L., Melack, J. M. y Simonett, D. S. (1990). Radar detection of flooding beneath the forest canopy: A review. *International Journal of Remote Sensing, 11*(7), 1313–1325. https://doi.org/10.1080/01431169008955095

Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics, 6*(2), 65–70.

Instituto de Hidrología, Meteorología y Estudios Ambientales [IDEAM]. (n.d.). [Nivel instantáneo del río Magdalena en la estación automática Remolino, código 2904700095] [Data set]. Datos Abiertos Colombia. https://www.datos.gov.co/d/bdmn-sqnh

Jaramillo, F., Brown, I., Castellazzi, P., Espinosa, L., Guittard, A., Hong, S.-H., Rivera-Monroy, V. H. y Wdowinski, S. (2018). Assessment of hydrologic connectivity in an ungauged wetland with InSAR observations. *Environmental Research Letters, 13*(2), 024003. https://doi.org/10.1088/1748-9326/aa9d23

JAXA EORC. (n.d.). *ALOS-2 PALSAR-2 ScanSAR products, Level 2.2* [Data set]. Japan Aerospace Exploration Agency, Earth Observation Research Center. https://www.eorc.jaxa.jp/ALOS/en/dataset/palsar2_l22_e.htm

Lucas, R., Rebelo, L.-M., Fatoyinbo, L., Rosenqvist, A., Itoh, T., Shimada, M., Simard, M., Souza-Filho, P. W., Thomas, N., Trettin, C., Accad, A., Carreiras, J. y Hilarides, L. (2014). Contribution of L-band SAR to systematic global mangrove monitoring. *Marine and Freshwater Research, 65*(7), 589–603. https://doi.org/10.1071/MF13177

Muñoz-Sabater, J., Dutra, E., Agustí-Panareda, A., Albergel, C., Arduini, G., Balsamo, G., Boussetta, S., Choulga, M., Harrigan, S., Hersbach, H., Martens, B., Miralles, D. G., Piles, M., Rodríguez-Fernández, N. J., Zsoter, E., Buontempo, C. y Thépaut, J.-N. (2021). ERA5-Land: A state-of-the-art global reanalysis dataset for land applications. *Earth System Science Data, 13*(9), 4349–4383. https://doi.org/10.5194/essd-13-4349-2021

NASA ASF DAAC. (2026a). *NISAR Beta Geocoded Polarimetric Covariance product (Version 1)* [Data set]. NASA Alaska Satellite Facility Distributed Active Archive Center. https://doi.org/10.5067/NIL2GCOV-B1

NASA ASF DAAC. (2026b). *NISAR Provisional Geocoded Polarimetric Covariance product (Version 1)* [Data set]. NASA Alaska Satellite Facility Distributed Active Archive Center. https://nisar-docs.asf.alaska.edu/gcov/

Pasquarella, V. J., Brown, C. F., Czerwinski, W. y Rucklidge, W. J. (2023). Comprehensive quality assessment of optical satellite imagery using weakly supervised video learning. En *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops* (pp. 2125–2135). https://doi.org/10.1109/CVPRW59228.2023.00206

Pyper, B. J. y Peterman, R. M. (1998). Comparison of methods to account for autocorrelation in correlation analyses of fish data. *Canadian Journal of Fisheries and Aquatic Sciences, 55*(9), 2127–2140. https://doi.org/10.1139/f98-104

Richards, J. A. (2013). *Remote sensing digital image analysis: An introduction* (5.ª ed.). Springer. https://doi.org/10.1007/978-3-642-30062-2

Richards, J. A., Woodgate, P. W. y Skidmore, A. K. (1987). An explanation of enhanced radar backscattering from flooded forests. *International Journal of Remote Sensing, 8*(7), 1093–1100. https://doi.org/10.1080/01431168708954756

Sen, P. K. (1968). Estimates of the regression coefficient based on Kendall's tau. *Journal of the American Statistical Association, 63*(324), 1379–1389. https://doi.org/10.1080/01621459.1968.10480934

Simard, M., Rivera-Monroy, V. H., Mancera-Pineda, J. E., Castañeda-Moya, E. y Twilley, R. R. (2008). A systematic method for 3D mapping of mangrove forests based on Shuttle Radar Topography Mission elevation data, ICESat/GLAS waveforms and field data: Application to Ciénaga Grande de Santa Marta, Colombia. *Remote Sensing of Environment, 112*(5), 2131–2144. https://doi.org/10.1016/j.rse.2007.10.012

Torres, R., Snoeij, P., Geudtner, D., Bibby, D., Davidson, M., Attema, E., Potin, P., Rommen, B., Floury, N., Brown, M., Navas Traver, I., Deghaye, P., Duesmann, B., Rosich, B., Miranda, N., Bruno, C., L'Abbate, M., Croci, R., Pietropaolo, A., ... Rostan, F. (2012). GMES Sentinel-1 mission. *Remote Sensing of Environment, 120*, 9–24. https://doi.org/10.1016/j.rse.2011.05.028

Yordanov, V. y Brovelli, M. A. (2021). Deforestation mapping using Sentinel-1 and object-based random forest classification on Google Earth Engine. *The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences, XLIII-B3–2021*, 865–872. https://doi.org/10.5194/isprs-archives-XLIII-B3-2021-865-2021

Zanaga, D., Van De Kerchove, R., Daems, D., De Keersmaecker, W., Brockmann, C., Kirches, G., Wevers, J., Cartus, O., Santoro, M., Fritz, S., Lesiv, M., Herold, M., Tsendbazar, N.-E., Xu, P., Ramoino, F. y Arino, O. (2022). *ESA WorldCover 10 m 2021 v200* [Data set]. Zenodo. https://doi.org/10.5281/zenodo.7254221

## Appendix A. Workflow, scripts and outputs

This appendix documents the computational traceability of the analysis. Figure A1 presents the processing chain of each sensor for the acquisition, calibration and preparation stages of the SAR data, and Figure A2 summarises the complete workflow of the study in nine stages, from data access to mapping and the optical contrast. The organisation of the SAR chain follows the processing workflows reviewed by De Luca et al. (2021) and Yordanov and Brovelli (2021).

The images in Figures 1 and A1 are exported with `exportar_figuras_flujo.py`, `exportar_series.py` and `exportar_productos.py`, and Figure A2 is generated with `figura_flujo_en.py`. Table A1 relates each stage to the scripts that run it and its main outputs.

![Figure A1. SAR processing chain by sensor, from acquisition and radiometric calibration to backscatter extraction. The examples correspond to NISAR D083 HH (29 October 2025), ALOS-2 ScanSAR HH (2 December 2025) and Sentinel-1 D142 VV (9 January 2026) over the CGSM.](fig_cadena_sar_sensores.png)

![Figure A2. Nine-stage workflow of the study, from data access to signal mapping and the optical contrast.](fig_flujo_trabajo_en.png)

Table A1. Scripts and outputs of each stage of the workflow.

| Stage | Scripts | Main outputs |
|---|---|---|
| 1. Data access | `16_inventario_nisar`, `17_descargar_nisar`, `18_nisar_recorte_remoto`, `23_nisar_recorte_pacifico`, `24_nisar_recorte_cgsm`, `nivel_ideam_descarga` | Table 1; `nisar_cgsm_granulos.json`; 45 `NISAR_AOI_*.h5` scenes; `nivel_ideam_*.csv` |
| 2. Preprocessing and calibration | `18_nisar_recorte_remoto`, `20_nisar_incidencia`, `alos2_marea_malaga`, `s1_marea_malaga` | σ⁰ per sensor and pass; NISAR incidence angle grid; Figure 4 |
| 3. Reference land covers and sampling | `perfil_pacifico_24`, `doble_rebote_incidencia`, `figuras_cgsm`, `figuras_pacifico` | 1,600 points per site; 2,444 mangrove points and 2,400 forest points for the analysis by incidence angle terciles; Figure 2 |
| 4. Hydrological forcing | `mareas_buenaventura`, `mareas_dimar_a_serie`, `marea_vs_radar`, `cgsm_nivel_rio` | Tide, antecedent precipitation and river level assigned to each pass |
| 5. Per-pass statistics | `perfil_pacifico_24`, `marea_vs_radar`, `cgsm_temporada` | `cgsm_temporada_*.csv`; Table 2 and Table B1 |
| 6. Hydrological test | `marea_vs_radar`, `s1_marea_malaga`, `alos2_marea_malaga`, `cgsm_temporada`, `cgsm_nivel_rio`, `figura_cgsm_optico` | Tables 3 to 6 and B2 to B3; Figures 5 and 7 to 12 |
| 7. Robustness and limits | `doble_rebote_incidencia`, `autocorrelacion_temporal`, `pendientes_auditoria`, `auditoria_calculos.md` | Tables 7, 9 and 12; Figures 6 and B1; `pendientes_auditoria_*.csv`; calculation audit |
| 8. Interpretation key | `figura_clave`, `nisar_flotante`, `clave_vs_muestra2025` | Tables 8 to 10 and B4; Figure 13; `clave_muestra2025_*.csv` |
| 9. Mapping and optical contrast | `mapa_doble_rebote`, `mapa_doble_rebote_s1`, `mapa_doble_rebote_malaga`, `corroboracion_dw` | Tables 11 and B5; Figures 14 to 17; `mapa_doble_rebote_50m.tif`, `mapa_s1_alto_bajo_50m.tif`, `dw_serie.csv` |
| Report and methodological figures | `md_a_word`, `exportar_figuras_flujo`, `exportar_series`, `exportar_productos`, `figura_flujo`, `figura_cadena_sar` | Report; Figures 1, A1 and A2 |

## Appendix B. Auxiliary results

Table B1. Median σ⁰ by land cover in the first five NISAR acquisitions of track A004 (8 and 20 November and 2, 14 and 26 December 2025), in dB.

| Land cover | HH | HV | HH−HV |
|---|---|---|---|
| Mangrove (WorldCover and GMW consensus) | −6.9 / −7.2 / −7.6 / −7.8 / −7.5 | −14.3 / −14.1 / −14.0 / −14.2 / −14.1 | 7.3 / 6.7 / 6.5 / 6.4 / 6.8 |
| Mangrove in GMW only | −8.9 / −8.5 / −8.8 / −8.7 / −8.9 | −15.8 / −15.3 / −15.3 / −15.9 / −15.6 | 6.4 / 6.4 / 6.4 / 6.5 / 6.5 |
| Forest | −7.3 / −7.6 / −7.4 / −7.8 / −7.2 | −13.4 / −13.4 / −13.4 / −13.6 / −13.5 | 6.3 / 6.0 / 6.0 / 6.0 / 6.0 |
| Herbaceous wetland | −9.7 / −9.6 / −9.4 / −9.5 / −9.9 | −17.2 / −16.8 / −16.8 / −17.4 / −16.8 | 6.8 / 6.6 / 7.0 / 6.9 / 6.9 |
| Water | −20.5 / −18.8 / −19.3 / −19.5 / −19.2 | −25.9 / −25.8 / −26.0 / −25.8 / −25.7 | 5.2 / 6.9 / 6.8 / 6.0 / 6.7 |

Table B2. Correlation between 30-day accumulated precipitation and Sentinel-1 backscatter in the CGSM.

| Orbit (local time, n) | Class | VV | VH | VV−VH |
|---|---|---|---|---|
| 77 ascending (18:06, 58) | Mangrove | ρ 0.32, p 0.01 | ρ 0.14, p 0.31 | ρ 0.25, p 0.06 |
| 77 ascending (18:06, 58) | Forest | ρ 0.52, p < 0.001 | ρ 0.21, p 0.12 | ρ 0.38, p 0.003 |
| 77 ascending (18:06, 58) | Mangrove − forest | ρ −0.35, p 0.01 | ρ −0.13, p 0.35 | ρ −0.17, p 0.19 |
| 142 descending (05:48, 61) | Mangrove | ρ 0.21, p 0.11 | ρ 0.18, p 0.17 | ρ −0.04, p 0.74 |
| 142 descending (05:48, 61) | Forest | ρ 0.58, p < 0.001 | ρ 0.41, p 0.001 | ρ 0.50, p < 0.001 |
| 142 descending (05:48, 61) | Mangrove − forest | ρ −0.52, p < 0.001 | ρ −0.34, p 0.01 | ρ −0.44, p < 0.001 |

Table B3. Relationship between 30-day accumulated precipitation and NISAR D083 backscatter in the CGSM.

| Class | HH | HV | HH−HV | HH, wet − dry (dB) |
|---|---|---|---|---|
| Mangrove | ρ 0.50, p 0.10 | ρ −0.26, p 0.42 | ρ 0.54, p 0.07 | −0.15 |
| Forest | ρ 0.02, p 0.95 | ρ −0.34, p 0.29 | ρ 0.29, p 0.35 | +0.26 |
| Mangrove − forest | ρ 0.58, p 0.05 | ρ 0.26, p 0.42 | ρ 0.39, p 0.22 | −0.44 |

Table B4. Multi-date signatures of the CGSM land covers in C-band and L-band, in dB. Floating vegetation is defined by polygon ZC-2025, delineated on Sentinel-2.

| Land cover | VV | VH | VV − VH | HH | HV | HH − HV |
|---|---|---|---|---|---|---|
| Open water | −21.1 | −30.9 | 9.0 | −20.0 | −25.6 | 6.1 |
| Floating vegetation | −13.3 | −20.7 | 7.5 | −16.6 | −23.3 | 6.6 |
| Herbaceous wetland | −9.9 | −15.2 | 5.3 | −9.2 | −17.5 | 7.9 |
| Mangrove | −9.6 | −14.9 | 5.3 | −10.9 | −17.2 | 6.1 |
| Dry forest (control) | −8.1 | −14.3 | 6.2 | −9.2 | −15.9 | 6.6 |

Table B5. Backscatter change between high and low tide in Bahía de Málaga, by track and land cover, in dB.

| Track | Class | Pixels | ΔHH | ΔHH > 0 | ΔHV | Δ(HH − HV) |
|---|---|---|---|---|---|---|
| A004 (05:46) | Mangrove | 34,344 | +0.34 (−0.01 to +0.69) | 75% | −0.36 | +0.70 |
| A004 (05:46) | Forest (control) | 300,038 | −0.10 (−0.36 to +0.17) | 40% | −0.34 | +0.25 |
| A004 (05:46) | Water | 214,339 | −0.07 (−0.45 to +0.30) | 45% | −0.51 | +0.43 |
| D087 (18:29) | Mangrove | 34,344 | +0.05 (−0.35 to +0.42) | 54% | −0.53 | +0.64 |
| D087 (18:29) | Forest (control) | 300,038 | −0.39 (−0.79 to −0.06) | 21% | −0.63 | +0.32 |
| D087 (18:29) | Water | 214,339 | −0.42 (−0.90 to +0.05) | 27% | −0.94 | +0.63 |

![Figure B1. Change in mangrove HH between the high and low river-level periods (CGSM, NISAR D083) and between high and low tide (Bahía de Málaga, A004 and D087) by distance of the 50 m pixel to the mangrove edge: median and interquartile range.](fig_borde_interior.png)
