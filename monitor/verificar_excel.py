"""Verifica un tablero.xlsx YA RECALCULADO (p. ej. con LibreOffice):
1) ninguna celda con error (#N/A, #VALUE!, #REF!, #NAME?, #DIV/0!...);
2) cada "Último valor" del Resumen coincide con el valor de datos.json.

Uso:  python monitor/verificar_excel.py ruta/tablero_recalculado.xlsx
Sale con código 1 si algo falla.
"""

import json
import sys
from pathlib import Path

from openpyxl import load_workbook

RAIZ = Path(__file__).resolve().parents[1]
ERRORES = ("#N/A", "#VALUE!", "#REF!", "#NAME?", "#DIV/0!", "#NUM!", "#NULL!", "Err:")


def main(ruta: str) -> int:
    wb = load_workbook(ruta, data_only=True)
    fallas = []
    for ws in wb.worksheets:
        for fila in ws.iter_rows():
            for c in fila:
                if isinstance(c.value, str) and c.value.startswith(ERRORES):
                    fallas.append(f"{ws.title}!{c.coordinate} = {c.value}")

    datos = json.loads((RAIZ / "monitor" / "datos.json").read_text(encoding="utf-8"))
    esperado = {i["nombre"]: i for b in datos["bloques"] for i in b["indicadores"] if i["estado"] == "ok"}
    res = wb["Resumen"]
    comparados = 0
    for r in range(5, res.max_row + 1):
        nombre, valor = res.cell(r, 1).value, res.cell(r, 2).value
        if nombre in esperado:
            ref = esperado[nombre]["valor"]
            if not isinstance(valor, (int, float)):
                fallas.append(f"Resumen!B{r} ({nombre}) sin valor calculado: {valor!r}")
            elif abs(valor - ref) > 1e-6 * max(1, abs(ref)):
                fallas.append(f"Resumen!B{r} ({nombre}) = {valor} ≠ datos.json {ref}")
            comparados += 1

    print(f"Indicadores comparados: {comparados}/{len(esperado)}")
    if comparados != len(esperado):
        fallas.append("No se encontraron todos los indicadores en el Resumen.")
    for f in fallas:
        print("FALLA", f)
    print("OK" if not fallas else f"{len(fallas)} fallas")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
