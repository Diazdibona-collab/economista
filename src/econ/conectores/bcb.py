"""Banco Central do Brasil — SGS (Sistema Gerenciador de Séries Temporais).

Códigos de uso frecuente (verificar el nombre en https://www3.bcb.gov.br/sgspub):
  432  Meta Selic (% a.a.)              433  IPCA variación mensual (%)
  13522 IPCA acumulado 12 meses (%)     1    Dólar comercial venta (BRL/USD)
  24364 IBC-Br desestacionalizado

Ojo: la serie 432 (meta Selic) trae fechas FUTURAS hasta la próxima reunión del Copom;
se recortan en la fecha de hoy.
"""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd

from ._http import get
from .base import Serie

API = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"


def sgs(codigo: int, nombre: str, unidad: str, frecuencia: str, desde: str | None = None) -> Serie:
    """Las series diarias admiten como máximo 10 años por consulta: se piden por tramos."""
    hoy = date.today()
    inicio = pd.Timestamp(desde).date() if desde else hoy - timedelta(days=365 * 10 - 1)
    partes = []
    while inicio <= hoy:
        fin = min(hoy, inicio + timedelta(days=365 * 10 - 1))
        r = get(API.format(codigo=codigo), params={"formato": "json", "dataInicial": inicio.strftime("%d/%m/%Y"),
                                                   "dataFinal": fin.strftime("%d/%m/%Y")})
        partes += r.json()
        inicio = fin + timedelta(days=1)
    s = pd.Series({pd.to_datetime(d["data"], dayfirst=True): float(d["valor"]) for d in partes if d["valor"] != ""}).sort_index()
    s = s[s.index <= pd.Timestamp(hoy)]
    return Serie(datos=s, fuente="BCB SGS", codigo_serie=str(codigo), nombre=nombre, unidad=unidad,
                 frecuencia=frecuencia, url=f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados")
