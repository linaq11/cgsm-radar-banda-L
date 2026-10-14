# -*- coding: utf-8 -*-
"""Dos gráficas reales para el panel 4 del flujo (forzante hidrológico), con rótulos en español:

11_marea_malaga_ene2026.png : marea de la DIMAR en Buenaventura, enero de 2026, respecto al nivel
                              medio del año, con las pasadas NISAR de ese mes (A004 7 y 19 de enero,
                              D087 9 de enero) marcadas a su hora.
12_nivel_rio_lluvia_cgsm.png: nivel del Magdalena en Remolino (IDEAM, media diaria) de octubre de
                              2025 a septiembre de 2026, con la lluvia acumulada de 30 días de
                              ERA5-Land en cada pasada NISAR D083 (barras) y las pasadas marcadas.

USO: python exportar_series.py
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
RADAR = os.path.dirname(AQUI)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})

# 11. marea
mar = pd.read_csv(os.path.join(RADAR, "mareas_dimar_serie.csv"), parse_dates=["t"])
mar = mar[(mar.t >= "2026-01-01") & (mar.t < "2026-02-01")]
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax.plot(mar.t, mar.altura_m, color="black", lw=0.8)
for d, h, c, n in [("2026-01-07", 10.75, "#c0504d", "A004"), ("2026-01-19", 10.75, "#c0504d", None), ("2026-01-09", 23.5, "#e9a23b", "D087")]:
    t0 = pd.Timestamp(d) + pd.Timedelta(hours=h)
    v = np.interp(t0.value, mar.t.astype("int64"), mar.altura_m)
    ax.plot(t0, v, "o", ms=5, color=c, mec="black", mew=0.5, label=("pasada NISAR " + n) if n else None)
ax.set_ylabel("Marea (m, respecto al nivel medio)")
ax.set_xlabel("Fecha")
ax.set_xticks(pd.to_datetime(["2026-01-01", "2026-01-15", "2026-02-01"])); ax.set_xticklabels(["01-01", "15-01", "01-02"])
ax.set_title("Bahía de Málaga: marea DIMAR, enero de 2026", fontsize=9.5)
ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.3), ncol=2)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.savefig(os.path.join(AQUI, "11_marea_malaga_ene2026.png"), dpi=250, bbox_inches="tight", facecolor="white")
plt.close(fig)

# 12. nivel del río y lluvia
niv = pd.read_csv(os.path.join(RADAR, "nivel_ideam_instantaneo.csv")).drop_duplicates("fechaobservacion")
niv["t"] = pd.to_datetime(niv.fechaobservacion)
niv = niv[(niv.t >= "2025-10-01") & (niv.t <= "2026-10-01")].set_index("t").valorobservado.resample("D").mean()
nis = pd.read_csv(os.path.join(RADAR, "cgsm_temporada_nisar.csv"))
nis = nis[nis.escena.str.contains("083")].drop_duplicates("escena")
nis["t"] = pd.to_datetime(nis.fecha_utc)
fig, ax = plt.subplots(figsize=(4.6, 2.6))
ax2 = ax.twinx()
ax2.bar(nis.t, nis.p30, width=7, color="#bdbdbd", label="Lluvia 30 días en la pasada (ERA5-Land)")
ax.plot(niv.index, niv.values, color="black", lw=0.9, label="Nivel del río en Remolino (IDEAM)")
ax.plot(nis.t, np.interp(nis.t.astype("int64"), niv.index.astype("int64"), niv.values), "o", ms=4, color="#c0504d", mec="black", mew=0.5, label="Pasadas NISAR D083")
ax.set_ylabel("Nivel (m)"); ax2.set_ylabel("Lluvia (mm)")
ax.set_xlabel("Fecha")
ax.set_xticks(pd.to_datetime(["2025-10-01", "2026-01-01", "2026-04-01", "2026-07-01", "2026-10-01"])); ax.set_xticklabels(["oct-25", "ene-26", "abr-26", "jul-26", "oct-26"])
ax.set_zorder(ax2.get_zorder() + 1); ax.patch.set_visible(False)
ax.set_title("Ciénaga Grande: nivel del Magdalena y lluvia, oct-2025 a sep-2026", fontsize=9.5)
h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=7.5, loc="upper right")
for s in ["top"]:
    ax.spines[s].set_visible(False); ax2.spines[s].set_visible(False)
fig.savefig(os.path.join(AQUI, "12_nivel_rio_lluvia_cgsm.png"), dpi=250, bbox_inches="tight", facecolor="white")
plt.close(fig)
with open(os.path.join(AQUI, "FUENTES.txt"), "a", encoding="utf-8") as fh:
    fh.write("\nSeries del forzante (exportar_series.py):\n11_marea_malaga_ene2026.png: mareas_dimar_serie.csv (DIMAR Buenaventura 2026, respecto al nivel medio), enero de 2026, pasadas NISAR marcadas.\n"
             "12_nivel_rio_lluvia_cgsm.png: nivel_ideam_instantaneo.csv (Remolino, media diaria) oct-2025 a sep-2026 y p30 de cgsm_temporada_nisar.csv en cada pasada D083.\n")
print("ok")
