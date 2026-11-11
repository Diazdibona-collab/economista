"""FRED (Federal Reserve Bank of St. Louis). Requiere FRED_API_KEY en .env o en el entorno."""

from __future__ import annotations

import os

import pandas as pd
from dotenv import load_dotenv

from econ import RAIZ
from ._http import get
from .base import Serie

API = "https://api.stlouisfed.org/fred"
_FREQ = {"Daily": "D", "Weekly": "W", "Monthly": "M", "Quarterly": "Q", "Annual": "A"}


def _key() -> str:
    load_dotenv(RAIZ / ".env")
    k = os.environ.get("FRED_API_KEY")
    if not k:
        raise RuntimeError("Falta FRED_API_KEY (en .env o como variable de entorno).")
    return k


def obtener(series_id: str, desde: str | None = None) -> Serie:
    """Descarga una serie de FRED con sus metadatos oficiales."""
    k = _key()
    meta = get(f"{API}/series", params={"series_id": series_id, "api_key": k, "file_type": "json"}).json()["seriess"][0]
    params = {"series_id": series_id, "api_key": k, "file_type": "json"}
    if desde:
        params["observation_start"] = desde
    obs = get(f"{API}/series/observations", params=params).json()["observations"]
    s = pd.Series(
        pd.to_numeric([o["value"] for o in obs], errors="coerce"),  # FRED marca faltantes con "."
        index=pd.to_datetime([o["date"] for o in obs]),
        name=series_id,
    ).dropna()
    return Serie(
        datos=s,
        fuente="FRED",
        codigo_serie=series_id,
        nombre=meta["title"],
        unidad=meta["units"],
        frecuencia=_FREQ.get(meta["frequency"].split(",")[0], meta["frequency_short"]),
        url=f"https://fred.stlouisfed.org/series/{series_id}",
        notas=f"FRED last_updated: {meta['last_updated']}. Ajuste estacional: {meta['seasonal_adjustment_short']}.",
    )
