"""Precios de mercado vía yfinance (Yahoo Finance, fuente NO oficial — confiabilidad C).

ADVERTENCIA verificada 2026-11-10: el ticker UYU=X de Yahoo difiere del BCU (~39,07 vs ~40,3 UYU/USD).
Para el peso uruguayo usar SIEMPRE bcu.cotizacion(). Para tasas de EE.UU. preferir FRED (DGS10, DGS2...).

Tickers útiles: ^GSPC (S&P 500), DX-Y.NYB (índice dólar DXY), BRL=X, ARS=X, ZS=F (soja CBOT, ¢/bushel),
LE=F (ganado vivo CME), BZ=F (Brent), GC=F (oro), ^VIX.
"""

from __future__ import annotations

import pandas as pd

from .base import Serie


def precio(ticker: str, nombre: str, unidad: str, periodo: str = "2y") -> Serie:
    import yfinance as yf

    d = yf.Ticker(ticker).history(period=periodo, auto_adjust=False)
    if d.empty:
        raise ValueError(f"yfinance: sin datos para {ticker}")
    s = d["Close"].copy()
    s.index = pd.DatetimeIndex(s.index.tz_localize(None)).normalize()
    return Serie(datos=s.dropna(), fuente="Yahoo Finance", codigo_serie=ticker, nombre=nombre, unidad=unidad,
                 frecuencia="D", url=f"https://finance.yahoo.com/quote/{ticker}",
                 notas="Fuente no oficial (confiabilidad C). Cierre diario.")
