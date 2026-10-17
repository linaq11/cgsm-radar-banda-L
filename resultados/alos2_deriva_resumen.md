# Deriva de ALOS-2 en la CGSM: ¿producto o manglar?

## 1. Metadatos del producto por año de adquisición

Año de procesamiento (SourceProcParam_ProcessingDate) por año de adquisición:

proc  2024  2025  2026
anio                  
2014     0     4     0
2015     0    14     0
2016     0    16     0
2017     0    13     0
2018     0    24     0
2019     0    24     0
2020     0    13     0
2021     4     7     0
2022     9     0     0
2023     9     0     0
2024    10     2     0
2025     0     9     6
2026     0     0     6

Versiones: Product_Version ['1']; software ['000.000 ']; fechas de descarga 2024-10-24 a 2026-09-08.

## 2. Mediana anual de HH (dB) por clase, estación seca enero a abril, traza D139

clase   agua  bosque  construido  humedal_herbaceo  manglar
anio                                                       
2015  -17.75   -9.29       -3.92             -9.97   -10.87
2016  -17.71   -9.57       -4.42            -10.89   -10.27
2017  -17.57   -9.34       -4.36            -10.92    -8.93
2018  -18.30   -8.54       -3.48            -10.12    -9.39
2019  -17.02   -8.90       -3.70            -10.24    -9.90
2020  -17.99   -8.82       -3.54            -10.05   -10.27
2021  -16.70   -8.40       -3.68             -9.46   -10.17
2022  -17.85   -8.37       -3.35             -8.95   -10.17
2023  -17.21   -8.77       -3.25             -8.75    -9.84
2024  -18.23   -9.22       -3.25             -9.13   -10.87
2025  -17.86   -9.49       -3.37             -9.12   -11.01
2026  -18.41   -8.58       -3.03             -7.80   -10.22

## 3. Cambio por punto entre 2015-2017 y 2022-2024, traza D139 (mediana y rango intercuartílico, dB)

- manglar: ΔHH -0.22 [-1.91 a +1.11], ΔHV +1.05, n 400
- bosque: ΔHH +0.59 [-0.44 a +1.76], ΔHV +1.41, n 400
- humedal_herbaceo: ΔHH +1.71 [+0.19 a +3.12], ΔHV +2.41, n 400
- agua: ΔHH -0.07 [-1.09 a +1.13], ΔHV +1.92, n 400
- construido: ΔHH +0.75 [-0.15 a +2.02], ΔHV +1.90, n 200

## 4. Puntos de manglar (D139): qué explica la caída de HH

- ΔHH frente a ΔNDVI (Sentinel-2 L1C, estación seca): ρ -0.57 (p 7.84e-36, n 400). NDVI medio 0.360 (2016-17) → 0.566 (2022-24).
- ΔHH frente a HH − HV actual (apertura del dosel 2022-24): ρ 0.11 (p 0.0328, n 400).
- ΔHH frente a HH inicial (2015-17): ρ -0.61 (p 2.42e-41); los puntos que más brillaban al inicio son los que más caen.

ΔHH y ΔNDVI por transición MapBiomas 2017 → 2023 (mediana, n):

- manglar → manglar: ΔHH +0.31 dB, NDVI 0.48 → 0.60 (ΔNDVI +0.128), n 219
- herbácea inundable → manglar: ΔHH -1.92 dB, NDVI 0.25 → 0.58 (ΔNDVI +0.296), n 71
- herbácea inundable → herbácea inundable: ΔHH +0.05 dB, NDVI 0.32 → 0.51 (ΔNDVI +0.194), n 31
- agua → manglar: ΔHH -2.88 dB, NDVI 0.09 → 0.60 (ΔNDVI +0.456), n 17
- bosque inundable → bosque inundable: ΔHH -1.12 dB, NDVI 0.12 → 0.42 (ΔNDVI +0.265), n 15
- agua → agua: ΔHH -0.17 dB, NDVI 0.08 → 0.20 (ΔNDVI +0.195), n 11
- agua → herbácea inundable: ΔHH +0.12 dB, NDVI 0.09 → 0.53 (ΔNDVI +0.405), n 8
- agua → bosque inundable: ΔHH -1.15 dB, NDVI 0.09 → 0.49 (ΔNDVI +0.360), n 8

Recuperados (herbácea → manglar) frente a estables (manglar → manglar): ΔHH -1.92 frente a +0.31 dB (Mann-Whitney p 1.8e-10); ΔNDVI +0.296 frente a +0.128 (p 1.21e-18).
