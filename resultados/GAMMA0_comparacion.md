# Sigma cero frente a gamma cero

Recálculo del 15 de octubre de 2026 con `RADAR_MAGNITUD=gamma0`. NISAR usa el γ⁰ RTC del producto sin el factor `rtcGammaToSigmaFactor`; Sentinel-1 se corrige con la banda `angle` (γ⁰ elipsoidal, σ⁰ − 10·log10 cos θ); ALOS-2 con el ángulo local `LIN`. Las diferencias copolar menos cruzada no cambian por construcción.

## Bahía de Málaga, NISAR: resta manglar menos bosque frente a la marea

| traza | variable | dif_alta_menos_baja σ⁰ | dif_alta_menos_baja γ⁰ | rho_spearman σ⁰ | rho_spearman γ⁰ | p σ⁰ | p γ⁰ |
|---|---|---|---|---|---|---|---|
| A004 | HH | 0.57 | 0.67 | 0.83 | 0.83 | 0.00 | 0.00 |
| A004 | HV | 0.03 | -0.01 | 0.11 | 0.01 | 0.73 | 0.97 |
| A004 | HHmHV | 0.45 | 0.45 | 0.83 | 0.83 | 0.00 | 0.00 |
| D087 | HH | 0.57 | 0.52 | 0.74 | 0.69 | 0.01 | 0.01 |
| D087 | HV | 0.07 | 0.04 | -0.06 | 0.10 | 0.85 | 0.75 |
| D087 | HHmHV | 0.61 | 0.61 | 0.60 | 0.60 | 0.04 | 0.04 |

## Bahía de Málaga, Sentinel-1

| orbita | variable | dif_alta_menos_baja σ⁰ | dif_alta_menos_baja γ⁰ | rho σ⁰ | rho γ⁰ | p σ⁰ | p γ⁰ |
|---|---|---|---|---|---|---|---|
| 48 | VV | -0.07 | -0.09 | -0.18 | -0.20 | 0.37 | 0.32 |
| 48 | VH | -0.11 | -0.07 | -0.30 | -0.29 | 0.14 | 0.15 |
| 48 | VVmVH | 0.16 | 0.16 | 0.23 | 0.23 | 0.26 | 0.26 |
| 142 | VV | -0.07 | -0.08 | -0.13 | -0.12 | 0.32 | 0.36 |
| 142 | VH | -0.00 | 0.01 | -0.08 | -0.08 | 0.55 | 0.53 |
| 142 | VVmVH | -0.15 | -0.15 | -0.15 | -0.15 | 0.24 | 0.24 |

## Bahía de Málaga, ALOS-2

| path | variable | dif_alta_menos_baja σ⁰ | dif_alta_menos_baja γ⁰ | rho σ⁰ | rho γ⁰ | p σ⁰ | p γ⁰ |
|---|---|---|---|---|---|---|---|
| 139 | HH | 0.25 | 0.08 | 0.65 | 0.62 | 0.00 | 0.00 |
| 139 | HV | 0.06 | 0.11 | 0.05 | 0.12 | 0.81 | 0.60 |
| 139 | HHmHV | 0.13 | 0.13 | 0.47 | 0.45 | 0.03 | 0.03 |
| 140 | HH | 0.49 | 0.46 | 0.72 | 0.77 | 0.00 | 0.00 |
| 140 | HV | -0.16 | -0.09 | -0.45 | -0.61 | 0.10 | 0.01 |
| 140 | HHmHV | 0.91 | 0.80 | 0.79 | 0.75 | 0.00 | 0.00 |

## CGSM: resta manglar menos bosque frente al nivel del río

| sensor | traza | variable | alto_menos_bajo_db σ⁰ | alto_menos_bajo_db γ⁰ | rho_nivel σ⁰ | rho_nivel γ⁰ | p σ⁰ | p γ⁰ |
|---|---|---|---|---|---|---|---|---|
| NISAR | A | CO | -0.14 | -0.16 | -0.04 | -0.39 | 0.94 | 0.38 |
| NISAR | A | X | -0.06 | -0.04 | -0.39 | -0.11 | 0.38 | 0.82 |
| NISAR | A | COmX | -0.30 | -0.30 | -0.54 | -0.54 | 0.21 | 0.21 |
| NISAR | D | CO | 0.83 | 0.84 | 0.83 | 0.80 | 0.00 | 0.00 |
| NISAR | D | X | 0.35 | 0.35 | 0.32 | 0.20 | 0.27 | 0.50 |
| NISAR | D | COmX | 0.62 | 0.62 | 0.49 | 0.49 | 0.08 | 0.08 |
| S1 | A77 | CO | -0.21 | -0.20 | -0.47 | -0.48 | 0.00 | 0.00 |
| S1 | A77 | X | 0.05 | 0.08 | -0.01 | 0.04 | 0.95 | 0.79 |
| S1 | A77 | COmX | -0.08 | -0.08 | -0.12 | -0.12 | 0.36 | 0.36 |
| S1 | D142 | CO | -0.21 | -0.17 | -0.33 | -0.30 | 0.01 | 0.02 |
| S1 | D142 | X | -0.14 | -0.16 | -0.37 | -0.35 | 0.01 | 0.01 |
| S1 | D142 | COmX | -0.15 | -0.15 | -0.18 | -0.18 | 0.18 | 0.18 |

## Firmas por clase, muestra de 720 puntos (medianas, dB)

| clase | VV σ⁰ | VV γ⁰ | VH σ⁰ | VH γ⁰ | VVmVH σ⁰ | VVmVH γ⁰ | HH σ⁰ | HH γ⁰ | HV σ⁰ | HV γ⁰ | HHmHV σ⁰ | HHmHV γ⁰ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| agua | -21.50 | -20.70 | -29.60 | -28.80 | 7.50 | 7.50 | -19.90 | -18.60 | -25.40 | -24.10 | 5.90 | 5.90 |
| vegetacion_flotante | -15.20 | -14.40 | -22.70 | -21.80 | 6.70 | 6.70 | -17.00 | -15.70 | -23.70 | -22.40 | 6.80 | 6.80 |
| humedal_herbaceo | -10.40 | -9.50 | -15.90 | -15.00 | 5.40 | 5.40 | -9.60 | -8.30 | -17.30 | -16.10 | 7.90 | 7.90 |
| manglar_degradado | -10.70 | -9.80 | -15.90 | -15.10 | 5.30 | 5.30 | -8.30 | -7.20 | -16.80 | -15.50 | 8.90 | 8.90 |
| manglar_intacto | -9.50 | -8.60 | -14.80 | -14.00 | 5.50 | 5.50 | -10.00 | -8.60 | -16.70 | -15.20 | 6.60 | 6.60 |
| otro | -10.10 | -9.20 | -15.40 | -14.70 | 6.00 | 6.00 | -10.70 | -9.40 | -18.30 | -16.80 | 7.50 | 7.50 |

## Separabilidad de Jeffries-Matusita

| par | jm C (VV, VH, VV-VH) σ⁰ | jm C (VV, VH, VV-VH) γ⁰ | jm L (HH, HV, HH-HV) σ⁰ | jm L (HH, HV, HH-HV) γ⁰ | jm C + L σ⁰ | jm C + L γ⁰ |
|---|---|---|---|---|---|---|
| agua | vegetacion_flotante | 0.47 | 0.47 | 0.28 | 0.27 | 0.69 | 0.68 |
| agua | humedal_herbaceo | 1.50 | 1.50 | 1.24 | 1.22 | 1.66 | 1.66 |
| agua | manglar_degradado | 1.65 | 1.65 | 1.56 | 1.55 | 1.82 | 1.82 |
| agua | manglar_intacto | 1.85 | 1.85 | 1.87 | 1.88 | 1.96 | 1.96 |
| agua | otro | 1.51 | 1.51 | 1.27 | 1.28 | 1.69 | 1.69 |
| vegetacion_flotante | humedal_herbaceo | 0.74 | 0.74 | 0.64 | 0.64 | 1.02 | 1.02 |
| vegetacion_flotante | manglar_degradado | 0.94 | 0.94 | 0.97 | 0.96 | 1.33 | 1.32 |
| vegetacion_flotante | manglar_intacto | 1.34 | 1.34 | 1.59 | 1.60 | 1.78 | 1.79 |
| vegetacion_flotante | otro | 0.64 | 0.64 | 0.77 | 0.78 | 1.09 | 1.10 |
| humedal_herbaceo | manglar_degradado | 0.17 | 0.17 | 0.22 | 0.22 | 0.38 | 0.38 |
| humedal_herbaceo | manglar_intacto | 0.45 | 0.45 | 0.76 | 0.78 | 0.96 | 0.97 |
| humedal_herbaceo | otro | 0.12 | 0.12 | 0.17 | 0.17 | 0.43 | 0.43 |
| manglar_degradado | manglar_intacto | 0.30 | 0.30 | 0.91 | 0.92 | 1.04 | 1.04 |
| manglar_degradado | otro | 0.27 | 0.27 | 0.47 | 0.47 | 0.69 | 0.69 |
| manglar_intacto | otro | 0.56 | 0.56 | 0.54 | 0.54 | 0.89 | 0.89 |

## Clave de interpretación con los umbrales literales del informe

| Magnitud | Decididos de 720 | Coinciden con la referencia | Acierto entre decididos |
|---|---|---|---|
| σ⁰ | 606 | 415 | 68.5 % |
| γ⁰ (mismos umbrales) | 627 | 429 | 68.4 % |

En γ⁰ todos los niveles suben entre 0,8 y 1,4 dB (el término −10·log10 cos θ), así que los umbrales absolutos de la clave (−17, −25 y −12 dB) deben desplazarse en esa cantidad para equivaler a los de σ⁰; los umbrales sobre VV − VH y HH − HV no cambian.
