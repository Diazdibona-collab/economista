"""Instituto Nacional de Estadística (Uruguay).

Las planillas se publican en www5.ine.gub.uy. Si una URL deja de funcionar (cambio de base o de ruta),
buscar el enlace nuevo en la portada https://www.gub.uy/instituto-nacional-estadistica/ y actualizarlo acá.
"""

from __future__ import annotations

import io

import pandas as pd

from ._http import get
from .base import Serie

IPC_URL = ("https://www5.ine.gub.uy/documents/Estad%C3%ADsticasecon%C3%B3micas/SERIES%20Y%20OTROS/IPC/"
           "Base%20Octubre%202022=100/IPC%20gral%20y%20variaciones_base%202022.xlsx")

_COLS_IPC = ["indice", "var_mensual", "var_acum_anio", "var_12m", "var_trimestre", "var_cuatrimestre", "var_semestre"]


def ipc_tabla() -> pd.DataFrame:
    """IPC general total país: índice (base oct-2022=100) y variaciones (%), mensual desde 1937."""
    r = get(IPC_URL)
    df = pd.read_excel(io.BytesIO(r.content), header=None)
    fechas = pd.to_datetime(df[0], errors="coerce", format="mixed")
    df = df[fechas.notna()].copy()
    df.index = pd.PeriodIndex(pd.to_datetime(df[0]), freq="M")
    df = df.iloc[:, 1:8]
    df.columns = _COLS_IPC
    df = df.apply(pd.to_numeric, errors="coerce")
    df.attrs["last_modified"] = r.headers.get("last-modified", "s/d")
    return df


def ipc(columna: str = "indice") -> Serie:
    """columna: indice | var_mensual | var_acum_anio | var_12m | var_trimestre | var_cuatrimestre | var_semestre"""
    t = ipc_tabla()
    unidad = "índice base oct-2022=100" if columna == "indice" else "%"
    return Serie(datos=t[columna].dropna(), fuente="INE", codigo_serie=f"IPC_{columna}",
                 nombre=f"IPC general total país — {columna}", unidad=unidad, frecuencia="M", url=IPC_URL,
                 notas=f"Planilla modificada por el INE: {t.attrs['last_modified']}.")
