# -*- coding: utf-8 -*-
"""Paso 3, version preliminar: relacion entre la altura de marea en la pasada y la
retrodispersion NISAR del manglar, por traza, con el bosque como control.

REGLA DE LECTURA (escrita antes de mirar los numeros). Si la banda L ve la inundacion
bajo el dosel, dentro de cada traza el manglar debe mostrar mayor HH (y mayor HH-HV)
en marea alta que en baja, y el bosque no. Se compara la mediana de las pasadas por
encima de la mediana de marea contra las de abajo, y la correlacion de Spearman entre
marea y HH. El efecto estacional se descuenta restando, fecha a fecha, el valor del
bosque (que no se inunda) al del manglar.

Lee perfil_pacifico_24.csv (con marea_m) y escribe marea_vs_radar.csv y una figura.
"""
import os

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(AQUI, "perfil_pacifico_24.csv"), parse_dates=["fecha_utc"])
if df.marea_m.isna().all():
    raise SystemExit("perfil sin marea: corre primero mareas_buenaventura.py y perfil_pacifico_24.py")
pas = df.drop_duplicates("escena")[["escena", "traza", "hora_local", "marea_m"]].sort_values("escena")
print("marea en las pasadas (m respecto al nivel medio):")
print(pas.to_string(index=False))

filas = []
for traza, g in df.groupby("traza"):
    w = g.pivot(index="escena", columns="clase", values=["HH", "HV", "HHmHV"])
    marea = g.drop_duplicates("escena").set_index("escena").marea_m.reindex(w.index)
    alta = marea > marea.median()
    for var in ("HH", "HV", "HHmHV"):
        for clase in ("manglar", "bosque", "humedal_herbaceo", "agua"):
            y = w[(var, clase)]
            rho, p = spearmanr(marea, y)
            filas.append(dict(traza=traza, variable=var, clase=clase, n=len(y), marea_alta=y[alta].median(), marea_baja=y[~alta].median(),
                              dif_alta_menos_baja=y[alta].median() - y[~alta].median(), rho_spearman=rho, p=p))
        # manglar menos bosque, fecha a fecha: descuenta lo estacional
        y = w[(var, "manglar")] - w[(var, "bosque")]
        rho, p = spearmanr(marea, y)
        filas.append(dict(traza=traza, variable=var, clase="manglar_menos_bosque", n=len(y), marea_alta=y[alta].median(), marea_baja=y[~alta].median(),
                          dif_alta_menos_baja=y[alta].median() - y[~alta].median(), rho_spearman=rho, p=p))
res = pd.DataFrame(filas)
res.to_csv(os.path.join(AQUI, "marea_vs_radar.csv"), index=False)
print("\n== diferencia marea alta menos baja (dB) y correlacion de Spearman marea-senal, por traza ==")
for traza, g in res.groupby("traza"):
    print("\ntraza", traza, "| marea de las pasadas: %.2f a %.2f m" % (pas[pas.traza == traza].marea_m.min(), pas[pas.traza == traza].marea_m.max()))
    print(g.pivot(index="clase", columns="variable", values="dif_alta_menos_baja").round(2).to_string())
    print("rho:"); print(g.pivot(index="clase", columns="variable", values="rho_spearman").round(2).to_string())

fig, axes = plt.subplots(2, 3, figsize=(14, 7.5))
for r, traza in enumerate(sorted(df.traza.unique())):
    g = df[df.traza == traza]
    for c, var in enumerate(("HH", "HV", "HHmHV")):
        ax = axes[r, c]
        for clase, col in (("manglar", "#1b7837"), ("bosque", "#4d4d4d")):
            s = g[g.clase == clase]
            ax.scatter(s.marea_m, s[var], color=col, s=28, label="Mangrove" if clase == "manglar" else "Forest (control)")
        ax.set_title("%s, %s" % ("Ascending 004 (05:46)" if traza.startswith("A") else "Descending 087 (18:29)", var.replace("HHmHV", "HH − HV")), fontsize=9.5)
        ax.set_xlabel("Tide height at pass (m above mean level)"); ax.set_ylabel("dB"); ax.grid(alpha=0.3)
axes[0, 0].legend(fontsize=8)
fig.suptitle("NISAR backscatter of Bahía de Málaga mangrove vs predicted tide height at acquisition, by track", fontsize=11)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_marea_vs_radar.png"), dpi=160)
print("\nfigura: fig_marea_vs_radar.png | tabla: marea_vs_radar.csv")
