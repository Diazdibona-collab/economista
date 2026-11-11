"""Modelos cuantitativos de uso frecuente. Cada función documenta sus supuestos."""

from __future__ import annotations

import numpy as np
import pandas as pd


def ols(y: pd.Series, X: pd.DataFrame, robusto: str = "HC3"):
    """MCO con constante y errores estándar robustos a heterocedasticidad.

    Supuestos: relación lineal, exogeneidad de X. NO implica causalidad.
    Para series temporales, considerar errores HAC (robusto='HAC').
    """
    import statsmodels.api as sm

    datos = pd.concat([y, X], axis=1).dropna()
    modelo = sm.OLS(datos.iloc[:, 0], sm.add_constant(datos.iloc[:, 1:]))
    if robusto == "HAC":
        return modelo.fit(cov_type="HAC", cov_kwds={"maxlags": 4})
    return modelo.fit(cov_type=robusto)


def pronostico_arima(s: pd.Series, orden=(1, 1, 1), pasos: int = 12, alfa: float = 0.05) -> pd.DataFrame:
    """Pronóstico ARIMA con intervalo de confianza.

    Supuestos: estructura estable, sin quiebres. Es un pronóstico estadístico,
    no un escenario económico: complementar con juicio y supuestos explícitos.
    """
    from statsmodels.tsa.arima.model import ARIMA

    res = ARIMA(s.dropna(), order=orden).fit()
    fc = res.get_forecast(pasos)
    ic = fc.conf_int(alpha=alfa)
    return pd.DataFrame({"pronostico": fc.predicted_mean, "inf": ic.iloc[:, 0], "sup": ic.iloc[:, 1]})


def montecarlo(funcion, distribuciones: dict, n: int = 10_000, semilla: int = 42) -> pd.Series:
    """Simulación Monte Carlo.

    funcion: recibe un dict {variable: array} y devuelve un array de resultados.
    distribuciones: {variable: callable(rng, n) -> array}, p. ej. lambda r, n: r.normal(0.03, 0.01, n).
    Devuelve la serie de resultados simulados; resumir con .describe() o percentiles.
    """
    rng = np.random.default_rng(semilla)
    draws = {k: f(rng, n) for k, f in distribuciones.items()}
    return pd.Series(funcion(draws), name="resultado")


def sensibilidad(funcion, base: dict, variable: str, valores) -> pd.Series:
    """Análisis de sensibilidad univariado: evalúa `funcion(**params)` variando una sola variable."""
    out = {}
    for v in valores:
        p = dict(base, **{variable: v})
        out[v] = funcion(**p)
    return pd.Series(out, name=variable)


def van(flujos, tasa: float) -> float:
    """Valor actual neto. flujos[0] es el período 0."""
    return float(sum(f / (1 + tasa) ** t for t, f in enumerate(flujos)))


def tir(flujos) -> float:
    """Tasa interna de retorno (bisección). Supone un único cambio de signo en los flujos."""
    from scipy.optimize import brentq

    return float(brentq(lambda r: van(flujos, r), -0.99, 10))
