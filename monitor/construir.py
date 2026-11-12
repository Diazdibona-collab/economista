"""Construye los datos del tablero de indicadores (monitor/datos.json).

Uso:  python monitor/construir.py
Cada indicador se descarga de forma independiente: si una fuente falla, el indicador queda con
estado "error" y el resto del tablero se genera igual. Nunca se reemplaza un dato faltante por uno inventado.
"""

from __future__ import annotations

import json
import sys
import warnings
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
warnings.filterwarnings("ignore")

from econ import series as tr  # noqa: E402
from econ.conectores import bcb, bcra, bcu, fred, imf, ine, mercados  # noqa: E402

SALIDA = RAIZ / "monitor" / "datos.json"
ANIOS_HISTORIA = 5


def _yoy(serie, frec):
    serie.datos = tr.interanual(serie.datos, frec).dropna()
    return serie


# Cada indicador: id, nombre, función que devuelve una Serie, unidad a mostrar,
# tipo de cambio ("pp" = puntos porcentuales, "pct" = variación %), decimales y nota opcional.
BLOQUES = [
    {
        "id": "uy", "titulo": "Macro Uruguay",
        "indicadores": [
            dict(id="uy_ipc", nombre="Inflación (IPC, interanual)", f=lambda: ine.ipc("var_12m"), unidad="%", cambio="pp", dec=2,
                 nota="Rango meta del BCU: verificar vigente en el último comunicado del COPOM."),
            dict(id="uy_ipc_m", nombre="Inflación mensual (IPC)", f=lambda: ine.ipc("var_mensual"), unidad="%", cambio="pp", dec=2),
            dict(id="uy_pib", nombre="PIB real, variación interanual", unidad="%", cambio="pp", dec=1,
                 f=lambda: _yoy(imf.sta("QNEA", "URY.B1GQ.Q.NSA.XDC.Q", "PIB real trimestral Uruguay", "%"), "Q"),
                 nota="Volumen sin desestacionalizar (dato BCU vía FMI)."),
            dict(id="uy_pib_weo", nombre="Crecimiento del PIB — FMI WEO", f=lambda: imf.weo("URY", "NGDP_RPCH"), unidad="%", cambio="pp",
                 dec=1, tipo="weo", nota="Los años sin dato observado son proyecciones del FMI."),
            dict(id="uy_call", nombre="Tasa call (aprox. de la TPM)", unidad="%", cambio="pp", dec=2,
                 f=lambda: imf.sta("MFS_IR", "URY.MMRT_RT_PT_A_PT.M", "Tasa del mercado monetario Uruguay", "%"),
                 nota="APROXIMACIÓN: no es la tasa de política monetaria oficial del BCU."),
            dict(id="uy_reservas", nombre="Reservas internacionales BCU", f=bcu.reservas, unidad="MUSD", cambio="pct", dec=0),
        ],
    },
    {
        "id": "mercados", "titulo": "Mercados y tipo de cambio",
        "indicadores": [
            dict(id="uyu", nombre="Dólar en Uruguay (BCU)", f=lambda: bcu.cotizacion(2222, desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="UYU por USD", cambio="pct", dec=3),
            dict(id="uy_letras", nombre="Letras del gobierno uruguayo", unidad="%", cambio="pp", dec=2,
                 f=lambda: imf.sta("MFS_IR", "URY.GSTBILY_RT_PT_A_PT.M", "Rendimiento letras gobierno Uruguay", "%")),
            dict(id="fed", nombre="Tasa Fed (efectiva)", f=lambda: fred.obtener("DFF", desde=_hace_anios(ANIOS_HISTORIA)), unidad="%", cambio="pp", dec=2),
            dict(id="ust2", nombre="Bono del Tesoro EE.UU. 2 años", f=lambda: fred.obtener("DGS2", desde=_hace_anios(ANIOS_HISTORIA)), unidad="%", cambio="pp", dec=2),
            dict(id="ust10", nombre="Bono del Tesoro EE.UU. 10 años", f=lambda: fred.obtener("DGS10", desde=_hace_anios(ANIOS_HISTORIA)), unidad="%", cambio="pp", dec=2),
            dict(id="spx", nombre="S&P 500", f=lambda: mercados.precio("^GSPC", "S&P 500", "puntos", "5y"), unidad="puntos", cambio="pct", dec=0),
            dict(id="vix", nombre="Volatilidad (VIX)", f=lambda: fred.obtener("VIXCLS", desde=_hace_anios(ANIOS_HISTORIA)), unidad="índice", cambio="pct", dec=1),
            dict(id="usd", nombre="Dólar global (índice amplio)", f=lambda: fred.obtener("DTWEXBGS", desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="índice ene-2006=100", cambio="pct", dec=1),
        ],
    },
    {
        "id": "region", "titulo": "Región",
        "indicadores": [
            dict(id="br_selic", nombre="Brasil — meta Selic", f=lambda: bcb.sgs(432, "Meta Selic", "% a.a.", "D", desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="%", cambio="pp", dec=2),
            dict(id="br_ipca", nombre="Brasil — inflación IPCA 12 meses", f=lambda: bcb.sgs(13522, "IPCA acumulado 12 meses", "%", "M", desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="%", cambio="pp", dec=2),
            dict(id="br_fx", nombre="Brasil — reales por dólar", f=lambda: bcb.sgs(1, "Dólar comercial venta", "BRL/USD", "D", desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="BRL por USD", cambio="pct", dec=3),
            dict(id="ar_fx", nombre="Argentina — dólar mayorista", f=lambda: bcra.obtener(5, desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="ARS por USD", cambio="pct", dec=1),
            dict(id="ar_ipc", nombre="Argentina — inflación interanual", f=lambda: bcra.obtener(28, desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="%", cambio="pp", dec=1),
            dict(id="ar_badlar", nombre="Argentina — tasa BADLAR privados", f=lambda: bcra.obtener(7, desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="% TNA", cambio="pp", dec=2, nota="El BCRA dejó de publicar una tasa de política en jul-2025."),
            dict(id="ar_reservas", nombre="Argentina — reservas BCRA", f=lambda: bcra.obtener(1, desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="MUSD", cambio="pct", dec=0),
            dict(id="br_weo", nombre="Brasil — crecimiento PIB (FMI WEO)", f=lambda: imf.weo("BRA", "NGDP_RPCH"), unidad="%", cambio="pp", dec=1, tipo="weo"),
            dict(id="ar_weo", nombre="Argentina — crecimiento PIB (FMI WEO)", f=lambda: imf.weo("ARG", "NGDP_RPCH"), unidad="%", cambio="pp", dec=1, tipo="weo"),
        ],
    },
    {
        "id": "global", "titulo": "Global y commodities",
        "indicadores": [
            dict(id="mundo_weo", nombre="Crecimiento mundial (FMI WEO)", f=lambda: imf.weo("G001", "NGDP_RPCH"), unidad="%", cambio="pp", dec=1, tipo="weo"),
            dict(id="us_cpi", nombre="EE.UU. — inflación (CPI, interanual)", f=lambda: _yoy(fred.obtener("CPIAUCSL", desde=_hace_anios(ANIOS_HISTORIA + 1)), "M"),
                 unidad="%", cambio="pp", dec=1),
            dict(id="bce", nombre="BCE — tasa de depósito", f=lambda: fred.obtener("ECBDFR", desde=_hace_anios(ANIOS_HISTORIA)), unidad="%", cambio="pp", dec=2),
            dict(id="soja", nombre="Soja (precio global, FMI)", f=lambda: fred.obtener("PSOYBUSDM", desde=_hace_anios(ANIOS_HISTORIA)), unidad="USD/t", cambio="pct", dec=0),
            dict(id="carne", nombre="Carne vacuna (precio global, FMI)", f=lambda: fred.obtener("PBEEFUSDM", desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="¢USD/lb", cambio="pct", dec=0),
            dict(id="lana", nombre="Lana fina (precio global, FMI)", f=lambda: fred.obtener("PWOOLFUSDM", desde=_hace_anios(ANIOS_HISTORIA)),
                 unidad="¢USD/kg", cambio="pct", dec=0),
            dict(id="brent", nombre="Petróleo Brent (FMI)", f=lambda: fred.obtener("POILBREUSDM", desde=_hace_anios(ANIOS_HISTORIA)), unidad="USD/barril", cambio="pct", dec=1),
            dict(id="oro", nombre="Oro (futuro, diario)", f=lambda: mercados.precio("GC=F", "Oro, futuro COMEX", "USD/oz", "5y"), unidad="USD/oz", cambio="pct", dec=0),
            dict(id="celulosa", nombre="Celulosa", f=None, unidad="", cambio="pct", dec=0,
                 nota="PENDIENTE: no se encontró aún una fuente pública y gratuita de precio de celulosa."),
        ],
    },
]


def _hace_anios(n: int) -> str:
    return (pd.Timestamp.today() - pd.DateOffset(years=n)).strftime("%Y-%m-%d")


def _a_timestamp(idx) -> pd.DatetimeIndex:
    return idx.to_timestamp(how="end").normalize() if isinstance(idx, pd.PeriodIndex) else pd.DatetimeIndex(idx)


def _fecha_txt(i, frec: str) -> str:
    if isinstance(i, pd.Period):
        return str(i)
    ts = pd.Timestamp(i)
    return ts.strftime("%Y-%m") if frec in ("M",) else ts.strftime("%Y-%m-%d")


def _valor_en(s: pd.Series, fecha: pd.Timestamp):
    """Último valor disponible en o antes de `fecha`."""
    st = s.copy()
    st.index = _a_timestamp(st.index)
    st = st[st.index <= fecha]
    return (float(st.iloc[-1]), st.index[-1]) if len(st) else (None, None)


def _cambio(actual, previo, tipo):
    if actual is None or previo is None:
        return None
    return round(actual - previo, 4) if tipo == "pp" else round((actual / previo - 1) * 100, 4)


def procesar(ind: dict) -> dict:
    base = {k: ind.get(k) for k in ("id", "nombre", "unidad", "cambio", "dec", "nota")}
    base["tipo"] = ind.get("tipo", "serie")
    if ind["f"] is None:
        return {**base, "estado": "pendiente"}
    try:
        s = ind["f"]()
    except Exception as e:  # noqa: BLE001
        return {**base, "estado": "error", "error": f"{type(e).__name__}: {str(e)[:200]}"}

    d = s.datos.dropna()
    meta = {"fuente": s.fuente, "codigo": s.codigo_serie, "nombre_fuente": s.nombre, "url": s.url,
            "fecha_consulta": s.fecha_consulta, "notas_fuente": s.notas, "frecuencia": s.frecuencia}

    if base["tipo"] == "weo":
        anio = pd.Timestamp.today().year
        valores = {str(p.year): round(float(v), 2) for p, v in d.items() if anio - 6 <= p.year <= anio + 2}
        return {**base, **meta, "estado": "ok", "valor": valores.get(str(anio)), "fecha": str(anio),
                "proyecciones": valores, "serie": [[k, v] for k, v in valores.items()]}

    ultimo_idx = d.index[-1]
    valor = float(d.iloc[-1])
    fin = _a_timestamp(pd.Index([ultimo_idx]) if not isinstance(d.index, pd.PeriodIndex) else d.index[-1:])[0]
    frec = s.frecuencia
    # Comparación corta: observación previa (M, Q, A) o 7 días antes (diarias/semanales)
    if frec in ("D", "W"):
        previo, fprev = _valor_en(d, fin - pd.Timedelta(days=7))
        desc_corto = "vs. hace 1 semana"
    else:
        previo, fprev = float(d.iloc[-2]), d.index[-2]
        desc_corto = {"M": "vs. mes anterior", "Q": "vs. trimestre anterior", "A": "vs. año anterior"}.get(frec, "vs. dato anterior")
    anual, _ = _valor_en(d, fin - pd.DateOffset(years=1))

    hist = d.copy()
    hist.index = _a_timestamp(hist.index)
    hist = hist[hist.index >= fin - pd.DateOffset(years=ANIOS_HISTORIA)]
    if frec == "D":  # último dato de cada semana, con su fecha real (aliviana el JSON)
        hist = hist.groupby(hist.index.to_period("W-FRI")).tail(1)
    serie = [[ts.strftime("%Y-%m-%d"), round(float(v), 4)] for ts, v in hist.items()]

    return {**base, **meta, "estado": "ok", "valor": round(valor, 4), "fecha": _fecha_txt(ultimo_idx, frec),
            "cambio_corto": _cambio(valor, previo, ind["cambio"]), "desc_corto": desc_corto,
            "cambio_anual": _cambio(valor, anual, ind["cambio"]), "serie": serie}


def main() -> int:
    salida = {"generado": datetime.now(timezone.utc).isoformat(timespec="seconds"), "bloques": []}
    errores = 0
    for b in BLOQUES:
        inds = []
        for ind in b["indicadores"]:
            r = procesar(ind)
            errores += r["estado"] == "error"
            print(f"{r['estado']:9} {b['id']:8} {r['id']:12} {r.get('valor')!s:>12} {r.get('fecha', '')}  {r.get('error', '')}")
            inds.append(r)
        salida["bloques"].append({"id": b["id"], "titulo": b["titulo"], "indicadores": inds})
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n-> {SALIDA}  ({errores} errores)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
