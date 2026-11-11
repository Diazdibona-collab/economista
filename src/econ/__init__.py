"""Paquete econ: obtención, procesamiento, modelado y visualización de datos económicos."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DATA_RAW = RAIZ / "data" / "raw"
DATA_PROCESSED = RAIZ / "data" / "processed"

__version__ = "0.1.0"
