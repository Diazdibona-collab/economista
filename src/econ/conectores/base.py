"""Estructura común a todas las series descargadas."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

import pandas as pd

from econ import DATA_PROCESSED


@dataclass
class Serie:
    """Serie temporal con trazabilidad completa.

    datos: pd.Series indexada por fecha (DatetimeIndex o PeriodIndex).
    """

    datos: pd.Series
    fuente: str
    codigo_serie: str
    nombre: str
    unidad: str
    frecuencia: str  # D, W, M, Q, A
    url: str
    fecha_consulta: str = field(default_factory=lambda: date.today().isoformat())
    notas: str = ""

    @property
    def periodo_inicio(self) -> str:
        return str(self.datos.index.min()) if len(self.datos) else ""

    @property
    def periodo_fin(self) -> str:
        return str(self.datos.index.max()) if len(self.datos) else ""

    def metadatos(self) -> dict:
        m = {k: v for k, v in asdict(self).items() if k != "datos"}
        m["periodo_inicio"] = self.periodo_inicio
        m["periodo_fin"] = self.periodo_fin
        return m

    def cita(self) -> str:
        """Texto de fuente para tablas y gráficos."""
        return (
            f"Fuente: {self.fuente} ({self.codigo_serie}). "
            f"Período: {self.periodo_inicio} a {self.periodo_fin}. "
            f"Consulta: {self.fecha_consulta}."
        )

    def guardar(self, carpeta: Path = DATA_PROCESSED) -> Path:
        """Guarda CSV + JSON de metadatos en data/processed/."""
        carpeta.mkdir(parents=True, exist_ok=True)
        base = carpeta / f"{self.fuente.lower().replace(' ', '_')}_{self.codigo_serie}"
        self.datos.rename(self.codigo_serie).to_csv(base.with_suffix(".csv"))
        base.with_suffix(".json").write_text(
            json.dumps(self.metadatos(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return base.with_suffix(".csv")
