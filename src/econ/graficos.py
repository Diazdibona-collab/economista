"""Estilo único para gráficos estáticos (matplotlib). Para web, ver skill dataviz."""

from __future__ import annotations

import matplotlib.pyplot as plt

PALETA = ["#2a6f97", "#c8553d", "#588157", "#8d6a9f", "#d4a017", "#5c677d"]


def estilo():
    plt.rcParams.update(
        {
            "figure.figsize": (9, 4.8),
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "axes.prop_cycle": plt.cycler(color=PALETA),
            "font.size": 10,
        }
    )


def linea(series: dict, titulo: str, unidad: str, fuente: str, ruta=None):
    """Gráfico de líneas con título, unidad y nota de fuente (obligatoria)."""
    estilo()
    fig, ax = plt.subplots()
    for nombre, s in series.items():
        ax.plot(s.index, s.values, label=nombre, linewidth=1.8)
    ax.set_title(titulo, loc="left", fontweight="bold")
    ax.set_ylabel(unidad)
    if len(series) > 1:
        ax.legend(frameon=False)
    fig.text(0.01, 0.01, fuente, fontsize=8, color="#555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    if ruta:
        fig.savefig(ruta, dpi=150)
    return fig
