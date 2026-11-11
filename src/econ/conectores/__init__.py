"""Conectores a fuentes de datos.

Cada conector devuelve una `Serie`: datos + metadatos de trazabilidad.
Regla: una serie sin metadatos completos no se usa en informes.
Los conectores concretos (fred, worldbank, imf, bcu, ine, bcb, bcra, mercados) se agregan en Fase 2.
"""

from .base import Serie

__all__ = ["Serie"]
