"""Transformaciones estándar de series económicas."""

from __future__ import annotations

import pandas as pd

PERIODOS_POR_ANIO = {"D": 252, "W": 52, "M": 12, "Q": 4, "A": 1}


def var_pct(s: pd.Series, periodos: int = 1) -> pd.Series:
    """Variación porcentual respecto de `periodos` atrás."""
    return s.pct_change(periodos, fill_method=None) * 100


def interanual(s: pd.Series, frecuencia: str) -> pd.Series:
    """Variación interanual (%) según frecuencia (M, Q, A)."""
    return var_pct(s, PERIODOS_POR_ANIO[frecuencia])


def acumulado_12m(s: pd.Series) -> pd.Series:
    """Suma móvil de 12 meses (flujos mensuales: fiscal, exportaciones)."""
    return s.rolling(12).sum()


def deflactar(nominal: pd.Series, indice_precios: pd.Series, base: str | None = None) -> pd.Series:
    """Serie real = nominal / índice * índice_base. Si base es None, usa el último dato del índice."""
    idx = indice_precios.reindex(nominal.index)
    ref = indice_precios.loc[base] if base else indice_precios.dropna().iloc[-1]
    return nominal / idx * ref


def rebasar(s: pd.Series, base: str) -> pd.Series:
    """Rebasa a 100 en la fecha/período `base`."""
    return s / s.loc[base] * 100


def desestacionalizar(s: pd.Series, periodo: int = 12) -> pd.Series:
    """Desestacionalización simple con STL (statsmodels). Para publicaciones oficiales, preferir la serie oficial."""
    from statsmodels.tsa.seasonal import STL

    res = STL(s.dropna(), period=periodo, robust=True).fit()
    return s.dropna() - res.seasonal
