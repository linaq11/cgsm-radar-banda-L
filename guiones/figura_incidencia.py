# -*- coding: utf-8 -*-
"""Rehace fig_doble_rebote_incidencia.png desde doble_rebote_incidencia.csv, con los
tercios en posiciones fijas (T1 a T3) y los rotulos sin superposicion."""
import os

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

AQUI = os.path.dirname(os.path.abspath(__file__))
res = pd.read_csv(os.path.join(AQUI, "doble_rebote_incidencia.csv"))
fig, axes = plt.subplots(2, 3, figsize=(14, 7.6))
for r_, traza in enumerate(sorted(res.traza.unique())):
    for c, var in enumerate(("HH", "HV", "HHmHV")):
        ax = axes[r_, c]
        g = res[(res.traza == traza) & (res.variable == var)].sort_values("tercio")
        x = g.tercio.to_numpy()
        ax.bar(x, g.dif_alta_menos_baja, color=["#1b7837" if p < 0.05 else "#a6dba0" for p in g.p], width=0.7)
        ymax = max(0.9, g.dif_alta_menos_baja.abs().max() * 1.6)
        ax.set_ylim(-0.5 if var == "HV" else -0.2, ymax)
        for xi, (d_, rho, p, inc) in enumerate(zip(g.dif_alta_menos_baja, g.rho, g.p, g.incidencia)):
            ax.text(xi, ymax * 0.93, "ρ = %.2f\np = %.2f" % (rho, p), ha="center", va="top", fontsize=8.5)
        ax.set_xticks(x); ax.set_xticklabels(["T%d\n%s" % (k + 1, inc) for k, inc in zip(x, g.incidencia)], fontsize=8.5)
        ax.axhline(0, color="k", lw=0.8); ax.grid(axis="y", alpha=0.3)
        ax.set_title("%s, %s" % ("Ascending 004 (05:46)" if traza.startswith("A") else "Descending 087 (18:29)", var.replace("HHmHV", "HH − HV")), fontsize=9.5)
        if c == 0:
            ax.set_ylabel("Mangrove − forest,\nhigh minus low tide (dB)")
        ax.set_xlabel("Incidence-angle tercile of the mangrove points")
fig.suptitle("Double-bounce test by incidence angle: tide response of mangrove relative to forest, 12 passes per track (dark bars: p < 0.05)", fontsize=10.5)
fig.tight_layout()
fig.savefig(os.path.join(AQUI, "fig_doble_rebote_incidencia.png"), dpi=160)
print("ok")
