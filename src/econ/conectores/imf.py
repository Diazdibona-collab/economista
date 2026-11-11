"""FMI — API SDMX 3.0 (api.imf.org).

La API vieja DataMapper (imf.org/external/datamapper/api) bloquea clientes automatizados (403);
por eso se usa SDMX 3.0, que expone WEO (IMF.RES) y las bases estadísticas (IMF.STA: CPI, QNEA, MFS_IR, ER...).

Claves verificadas para Uruguay (2026-11-10):
  weo("URY", "NGDP_RPCH")                                   crecimiento real PIB, % (incluye proyecciones)
  sta("CPI", "URY.CPI._T.IX.M")                             IPC índice mensual
  sta("CPI", "URY.CPI._T.YOY_PCH_PA_PT.M")                  inflación interanual mensual, %
  sta("QNEA", "URY.B1GQ.Q.NSA.XDC.Q")                       PIB trimestral en volumen, moneda nacional, sin desestacionalizar
  sta("MFS_IR", "URY.MMRT_RT_PT_A_PT.M")                    tasa del mercado monetario (call), %
  sta("MFS_IR", "URY.GSTBILY_RT_PT_A_PT.M")                 rendimiento de letras del gobierno, %
  sta("ER", "URY.XDC_USD.PA_RT.M")                          pesos por dólar, promedio del período
"""

from __future__ import annotations

import pandas as pd

from ._http import get
from .base import Serie

API = "https://api.imf.org/external/sdmx/3.0"
H = {"Accept": "application/json"}


def _periodo(p: str) -> pd.Period:
    p = p.replace("-M", "-").replace("-Q", "Q")
    if "Q" in p:
        return pd.Period(p, freq="Q")
    if "-" in p:
        return pd.Period(p, freq="M")
    return pd.Period(p, freq="Y")


def _consultar(agencia: str, flujo: str, clave: str) -> tuple[pd.Series, str]:
    url = f"{API}/data/dataflow/{agencia}/{flujo}/+/{clave}"
    j = get(url, headers=H, params={"dimensionAtObservation": "TIME_PERIOD", "attributes": "none", "measures": "all"}).json()
    series = j["data"]["dataSets"][0]["series"]
    if len(series) != 1:
        raise ValueError(f"FMI {flujo}/{clave}: se esperaba 1 serie, llegaron {len(series)}. Precisar la clave.")
    tiempos = j["data"]["structures"][0]["dimensions"]["observation"][0]["values"]
    obs = next(iter(series.values())).get("observations", {})
    s = pd.Series({_periodo(tiempos[int(i)]["value"]): float(v[0]) for i, v in obs.items() if v[0] is not None}).sort_index()
    return s, url


def weo(pais: str, indicador: str) -> Serie:
    """World Economic Outlook (anual, incluye proyecciones del FMI)."""
    s, url = _consultar("IMF.RES", "WEO", f"{pais}.{indicador}.A")
    return Serie(
        datos=s, fuente="FMI WEO", codigo_serie=f"{pais}.{indicador}", nombre=f"WEO {indicador} — {pais}",
        unidad="ver definición WEO", frecuencia="A", url=url,
        notas="Los años posteriores al último dato observado son PROYECCIONES del FMI.",
    )


def sta(flujo: str, clave: str, nombre: str = "", unidad: str = "") -> Serie:
    """Bases estadísticas IMF.STA (CPI, QNEA, MFS_IR, ER, IRFCL...). La clave debe identificar una sola serie."""
    s, url = _consultar("IMF.STA", flujo, clave)
    frec = {"A": "A", "Q": "Q", "M": "M"}.get(clave.rsplit(".", 1)[-1], "")
    return Serie(datos=s, fuente="FMI", codigo_serie=f"{flujo}.{clave}", nombre=nombre or f"{flujo} {clave}",
                 unidad=unidad, frecuencia=frec, url=url)
