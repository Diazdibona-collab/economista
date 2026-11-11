"""Banco Central del Uruguay.

- `cotizacion()`: web service SOAP oficial de cotizaciones (cotizaciones.bcu.gub.uy). Moneda 2222 = dólar USA billete.
- `reservas()`: planilla diaria de activos de reserva (MonedayCredito/Activos-de-Reserva/reservas.xls).

La web de estadísticas del BCU (SharePoint) carga casi todas sus planillas con componentes dinámicos y
algunas solo en Power BI; para PIB, IPC y tasas se usan, por ahora, INE y FMI (ver fuentes/uruguay.md).
"""

from __future__ import annotations

import io
import re
from datetime import date, timedelta

import pandas as pd

from ._http import get, post
from .base import Serie

WS = "https://cotizaciones.bcu.gub.uy/wscotizaciones/servlet/awsbcucotizaciones"
RESERVAS = "https://www.bcu.gub.uy/Estadisticas-e-Indicadores/MonedayCredito/Activos-de-Reserva/reservas.xls"

_SOAP = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cot="Cotiza">
<soapenv:Body><cot:wsbcucotizaciones.Execute><cot:Entrada>
<cot:Moneda><cot:item>{moneda}</cot:item></cot:Moneda>
<cot:FechaDesde>{desde}</cot:FechaDesde><cot:FechaHasta>{hasta}</cot:FechaHasta><cot:Grupo>0</cot:Grupo>
</cot:Entrada></cot:wsbcucotizaciones.Execute></soapenv:Body></soapenv:Envelope>"""


def cotizacion(moneda: int = 2222, desde: str | None = None, hasta: str | None = None) -> Serie:
    """Cotización oficial BCU (pesos por unidad de moneda). Se consulta por tramos de 6 meses."""
    fin = pd.Timestamp(hasta).date() if hasta else date.today()
    ini = pd.Timestamp(desde).date() if desde else fin - timedelta(days=365)
    datos, nombre = {}, ""
    while ini <= fin:
        tope = min(fin, ini + timedelta(days=182))
        xml = post(WS, data=_SOAP.format(moneda=moneda, desde=ini, hasta=tope).encode(),
                   headers={"Content-Type": "text/xml;charset=utf-8", "SOAPAction": "Cotizaaction/AWSBCUCOTIZACIONES.Execute"}).text
        status = re.search(r"<status>(\d+)</status>", xml)
        if status and status.group(1) != "1" and "<datoscotizaciones.dato" not in xml:
            msg = re.search(r"<mensaje>(.*?)</mensaje>", xml)
            if msg and "no existen" not in msg.group(1).lower():
                raise RuntimeError(f"BCU WS: {msg.group(1)}")
        for f, n, tcv in re.findall(r"<Fecha>([\d-]+)</Fecha>.*?<Nombre>(.*?)</Nombre>.*?<TCV>([\d.]+)</TCV>", xml, re.S):
            datos[pd.Timestamp(f)] = float(tcv)
            nombre = n
        ini = tope + timedelta(days=1)
    s = pd.Series(datos).sort_index()
    return Serie(datos=s, fuente="BCU", codigo_serie=f"COT{moneda}", nombre=f"Cotización {nombre.strip()} (BCU)",
                 unidad="pesos uruguayos por unidad", frecuencia="D", url=WS,
                 notas="Web service oficial de cotizaciones del BCU. Tipo vendedor (TCV).")


def reservas() -> Serie:
    """Activos de reserva del BCU, millones de USD, diario."""
    r = get(RESERVAS)
    df = pd.read_excel(io.BytesIO(r.content), header=None)
    df = df[pd.to_datetime(df[3], errors="coerce", format="mixed").notna()]
    s = pd.Series(pd.to_numeric(df[4], errors="coerce").values, index=pd.to_datetime(df[3])).dropna().sort_index()
    return Serie(datos=s, fuente="BCU", codigo_serie="RESERVAS", nombre="Activos de reserva del BCU",
                 unidad="millones de USD", frecuencia="D", url=RESERVAS,
                 notas=f"Planilla modificada por el BCU: {r.headers.get('last-modified', 's/d')}. Definición MBP5 del FMI.")
