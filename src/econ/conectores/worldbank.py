"""Banco Mundial — API v2 (World Development Indicators y otras bases). Datos anuales."""

from __future__ import annotations

import pandas as pd

from ._http import get
from .base import Serie

API = "https://api.worldbank.org/v2"


def obtener(pais: str, indicador: str, desde: int | None = None) -> Serie:
    """pais: código ISO3 (URY, ARG, BRA) o agregado (WLD, LCN). indicador: p. ej. NY.GDP.MKTP.KD.ZG."""
    params = {"format": "json", "per_page": 20000}
    if desde:
        params["date"] = f"{desde}:2100"
    cab, filas = get(f"{API}/country/{pais}/indicator/{indicador}", params=params).json()
    filas = [f for f in (filas or []) if f["value"] is not None]
    if not filas:
        raise ValueError(f"Banco Mundial: sin datos para {pais}/{indicador}")
    s = pd.Series(
        [f["value"] for f in filas],
        index=pd.PeriodIndex([f["date"] for f in filas], freq="Y"),
        name=indicador,
    ).sort_index()
    return Serie(
        datos=s,
        fuente="Banco Mundial",
        codigo_serie=f"{pais}.{indicador}",
        nombre=f"{filas[0]['indicator']['value']} — {filas[0]['country']['value']}",
        unidad=filas[0].get("unit") or "ver definición del indicador",
        frecuencia="A",
        url=f"https://data.worldbank.org/indicator/{indicador}?locations={filas[0]['country']['id']}",
        notas=f"Base actualizada por el Banco Mundial: {cab.get('lastupdated', 's/d')}.",
    )
