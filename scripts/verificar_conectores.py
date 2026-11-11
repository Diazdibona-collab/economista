"""Prueba cada conector con una descarga real y muestra el último dato.

Uso:  python scripts/verificar_conectores.py
Sale con código 1 si algún conector falla (útil en GitHub Actions).
"""

import sys
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from econ.conectores import bcb, bcra, bcu, fred, imf, ine, mercados, worldbank  # noqa: E402

PRUEBAS = [
    ("FRED", lambda: fred.obtener("DFF", desde="2026-01-01")),
    ("Banco Mundial", lambda: worldbank.obtener("URY", "NY.GDP.MKTP.KD.ZG", desde=2015)),
    ("FMI WEO", lambda: imf.weo("URY", "NGDP_RPCH")),
    ("FMI STA (CPI)", lambda: imf.sta("CPI", "URY.CPI._T.YOY_PCH_PA_PT.M", "Inflación interanual Uruguay", "%")),
    ("BCB SGS", lambda: bcb.sgs(432, "Meta Selic", "% a.a.", "D", desde="2026-01-01")),
    ("BCRA v4", lambda: bcra.obtener(1, desde="2026-10-01")),
    ("BCU cotización", lambda: bcu.cotizacion(2222, desde="2026-10-01")),
    ("BCU reservas", lambda: bcu.reservas()),
    ("INE IPC", lambda: ine.ipc("var_12m")),
    ("Yahoo Finance", lambda: mercados.precio("^GSPC", "S&P 500", "puntos", "1mo")),
]

fallas = 0
for nombre, f in PRUEBAS:
    try:
        s = f()
        print(f"OK   {nombre:16} {s.codigo_serie:32} último: {s.datos.iloc[-1]:>12,.4f}  ({s.periodo_fin[:10]})  n={len(s.datos)}")
    except Exception as e:  # noqa: BLE001
        fallas += 1
        print(f"FALLA {nombre:15} {type(e).__name__}: {str(e)[:150]}")
        traceback.print_exc(limit=1, file=sys.stderr)

print(f"\n{len(PRUEBAS) - fallas}/{len(PRUEBAS)} conectores OK")
sys.exit(1 if fallas else 0)
