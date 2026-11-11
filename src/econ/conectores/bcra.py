"""BCRA — API de Estadísticas v4.0 (la v3 fue dada de baja: responde 410).

`catalogo()` lista las ~1.600 variables con su idVariable. Ejemplo: idVariable=1 reservas internacionales (MUSD).
"""

from __future__ import annotations

import pandas as pd

from ._http import get
from .base import Serie

API = "https://api.bcra.gob.ar/estadisticas/v4.0/monetarias"


def catalogo() -> pd.DataFrame:
    filas, offset = [], 0
    while True:
        j = get(API, params={"limit": 1000, "offset": offset}).json()
        filas += j["results"]
        offset += 1000
        if offset >= j["metadata"]["resultset"]["count"]:
            break
    return pd.DataFrame(filas)


def obtener(id_variable: int, desde: str | None = None) -> Serie:
    cat = catalogo().set_index("idVariable").loc[id_variable]
    params = {"limit": 3000}
    if desde:
        params["desde"] = desde
    j = get(f"{API}/{id_variable}", params=params).json()
    res = j["results"]
    detalle = res[0]["detalle"] if res and "detalle" in res[0] else res
    s = pd.Series({pd.to_datetime(d["fecha"]): float(d["valor"]) for d in detalle}).sort_index()
    return Serie(datos=s, fuente="BCRA", codigo_serie=str(id_variable), nombre=cat["descripcion"],
                 unidad=cat.get("unidadExpresion", ""), frecuencia=cat.get("periodicidad", ""),
                 url=f"{API}/{id_variable}")
