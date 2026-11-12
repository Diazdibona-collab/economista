"""Genera monitor/tablero.xlsx a partir de monitor/datos.json.

Hojas:
  Resumen            último valor y variaciones, calculados con FÓRMULAS sobre las hojas de series
  Uruguay, Mercados, Región, Global   series históricas (Fecha | Valor por indicador)
  Proyecciones FMI   crecimiento del PIB por año (WEO)
  Fuentes            trazabilidad de cada indicador

Uso:  python monitor/excel.py [ruta_salida]
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "monitor" / "datos.json"

F = "Arial"
AZUL = "1F3B57"
GRIS = "5F6670"
BANDA = "E8EDF2"
LINEA = Side(style="thin", color="C9D1DA")

HOJA = {"uy": "Uruguay", "mercados": "Mercados", "region": "Región", "global": "Global"}
PRIMERA_FILA = 6  # primera fila de datos en las hojas de series
ULTIMA_FILA = 3000


def fmt_num(dec: int) -> str:
    return "#,##0" if dec == 0 else "#,##0." + "0" * dec


def titulo(ws, texto, sub):
    ws["A1"] = texto
    ws["A1"].font = Font(name=F, size=14, bold=True, color=AZUL)
    ws["A2"] = sub
    ws["A2"].font = Font(name=F, size=9, color=GRIS)


def encabezado(celda, texto):
    celda.value = texto
    celda.font = Font(name=F, size=9, bold=True, color="FFFFFF")
    celda.fill = PatternFill("solid", fgColor=AZUL)
    celda.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def hoja_series(wb, bloque, generado):
    """Escribe las series de un bloque y devuelve {id_indicador: (col_fecha, col_valor)}."""
    ws = wb.create_sheet(HOJA[bloque["id"]])
    titulo(ws, f"Series — {bloque['titulo']}",
           "Series diarias: último dato de cada semana. Mensuales y trimestrales: fecha = fin del período. "
           f"Datos al {generado}.")
    cols = {}
    c = 1
    for ind in bloque["indicadores"]:
        if ind["estado"] != "ok" or ind["tipo"] == "weo":
            continue
        cf, cv = c, c + 1
        ws.merge_cells(start_row=4, start_column=cf, end_row=4, end_column=cv)
        encabezado(ws.cell(4, cf), ind["nombre"])
        for col, txt in ((cf, "Fecha"), (cv, ind["unidad"])):
            h = ws.cell(5, col, txt)
            h.font = Font(name=F, size=8, bold=True, color=GRIS)
            h.alignment = Alignment(horizontal="center")
        for i, (fecha, valor) in enumerate(ind["serie"]):
            r = PRIMERA_FILA + i
            d = ws.cell(r, cf, datetime.strptime(fecha, "%Y-%m-%d"))
            d.number_format = "dd/mm/yyyy" if ind["frecuencia"] in ("D", "W") else "mm/yyyy"
            d.font = Font(name=F, size=9)
            v = ws.cell(r, cv, valor)
            v.number_format = fmt_num(ind["dec"])
            v.font = Font(name=F, size=9)
        ws.column_dimensions[get_column_letter(cf)].width = 11
        ws.column_dimensions[get_column_letter(cv)].width = 13
        ws.column_dimensions[get_column_letter(c + 2)].width = 3
        cols[ind["id"]] = (get_column_letter(cf), get_column_letter(cv))
        c += 3
    ws.row_dimensions[4].height = 42
    ws.freeze_panes = ws.cell(PRIMERA_FILA, 1)
    return ws.title, cols


def hoja_weo(wb, weos):
    ws = wb.create_sheet("Proyecciones FMI")
    titulo(ws, "Crecimiento del PIB real (%) — FMI, World Economic Outlook",
           "El año en curso y los siguientes son PROYECCIONES del FMI.")
    anios = sorted({a for w in weos for a in w["proyecciones"]})
    encabezado(ws.cell(4, 1), "Economía")
    for j, a in enumerate(anios, start=2):
        encabezado(ws.cell(4, j), int(a))
    filas = {}
    for i, w in enumerate(weos, start=5):
        ws.cell(i, 1, w["nombre"]).font = Font(name=F, size=9)
        for j, a in enumerate(anios, start=2):
            if a in w["proyecciones"]:
                c = ws.cell(i, j, w["proyecciones"][a])
                c.number_format = "0.0"
                proy = int(a) >= datetime.now().year
                c.font = Font(name=F, size=9, italic=proy, color=GRIS if proy else "000000")
        filas[w["id"]] = i
    ws.column_dimensions["A"].width = 40
    ultima = get_column_letter(len(anios) + 1)
    return ws.title, filas, f"$B$4:${ultima}$4", ultima


def main(salida: Path) -> None:
    datos = json.loads(DATOS.read_text(encoding="utf-8"))
    generado = datos["generado"][:10]
    wb = Workbook()
    res = wb.active
    res.title = "Resumen"

    ubic = {}
    for b in datos["bloques"]:
        nombre, cols = hoja_series(wb, b, generado)
        for k, v in cols.items():
            ubic[k] = (nombre, *v)
    weos = [i for b in datos["bloques"] for i in b["indicadores"] if i.get("tipo") == "weo" and i["estado"] == "ok"]
    hoja_w, filas_w, rango_anios, col_ultima = hoja_weo(wb, weos)

    titulo(res, "Monitor económico — Uruguay, región y mercados",
           f"Datos al {generado}. Fuentes y fechas por indicador en la hoja 'Fuentes'. "
           "Los valores se calculan con fórmulas sobre las hojas de series.")
    cab = ["Indicador", "Último valor", "Unidad", "Período", "Cambio corto", "Comparado con", "Cambio 12 meses", "Fuente", "Nota"]
    for j, t in enumerate(cab, start=1):
        encabezado(res.cell(4, j), t)
    leyenda = res.cell(3, 1, "Cambio en pp = puntos porcentuales (tasas); en % = variación porcentual (niveles y precios).")
    leyenda.font = Font(name=F, size=8, italic=True, color=GRIS)

    r = 5
    anio = datetime.now().year
    for b in datos["bloques"]:
        res.merge_cells(start_row=r, start_column=1, end_row=r, end_column=len(cab))
        s = res.cell(r, 1, b["titulo"])
        s.font = Font(name=F, size=10, bold=True, color=AZUL)
        s.fill = PatternFill("solid", fgColor=BANDA)
        r += 1
        for ind in b["indicadores"]:
            res.cell(r, 1, ind["nombre"])
            res.cell(r, 3, ind["unidad"])
            res.cell(r, 8, ind.get("fuente", ""))
            res.cell(r, 9, ind.get("nota") or "")
            fmt = fmt_num(ind["dec"])
            if ind["estado"] != "ok":
                res.cell(r, 2, "pendiente" if ind["estado"] == "pendiente" else "sin dato")
                res.cell(r, 9, ind.get("nota") or ind.get("error", ""))
            elif ind["tipo"] == "weo":
                fila = filas_w[ind["id"]]
                res.cell(r, 2, f"=IFERROR(INDEX('{hoja_w}'!$B${fila}:${col_ultima}${fila},MATCH({anio},'{hoja_w}'!{rango_anios},0)),\"\")")
                res.cell(r, 2).number_format = "0.0"
                res.cell(r, 4, f"{anio} (proyección)")
                res.cell(r, 7, f"=IFERROR(B{r}-INDEX('{hoja_w}'!$B${fila}:${col_ultima}${fila},MATCH({anio - 1},'{hoja_w}'!{rango_anios},0)),\"\")")
                res.cell(r, 7).number_format = '+0.0" pp";-0.0" pp";0.0" pp"'
                res.cell(r, 6, f"vs. {anio - 1}")
            else:
                h, cf, cv = ubic[ind["id"]]
                V = f"'{h}'!${cv}${PRIMERA_FILA}:${cv}${ULTIMA_FILA}"
                D = f"'{h}'!${cf}${PRIMERA_FILA}:${cf}${ULTIMA_FILA}"
                n = f"COUNT({V})"
                res.cell(r, 2, f"=INDEX({V},{n})").number_format = fmt
                fecha = res.cell(r, 4, f"=INDEX({D},{n})")
                fecha.number_format = "dd/mm/yyyy" if ind["frecuencia"] in ("D", "W") else "mm/yyyy"
                prev = f"INDEX({V},{n}-1)"
                hace12 = f"INDEX({V},MATCH(EDATE(D{r},-12),{D},1))"
                if ind["cambio"] == "pp":
                    res.cell(r, 5, f"=IFERROR(B{r}-{prev},\"\")")
                    res.cell(r, 7, f"=IFERROR(B{r}-{hace12},\"\")")
                    for c in (5, 7):
                        res.cell(r, c).number_format = '+0.00" pp";-0.00" pp";0.00" pp"'
                else:
                    res.cell(r, 5, f"=IFERROR(B{r}/{prev}-1,\"\")")
                    res.cell(r, 7, f"=IFERROR(B{r}/{hace12}-1,\"\")")
                    for c in (5, 7):
                        res.cell(r, c).number_format = "+0.0%;-0.0%;0.0%"
                res.cell(r, 6, "semana anterior" if ind["frecuencia"] in ("D", "W") else
                         {"M": "mes anterior", "Q": "trimestre anterior"}.get(ind["frecuencia"], "dato anterior"))
                res.cell(r, 2).comment = Comment(f"Fórmula sobre la hoja '{h}', columnas {cf}:{cv}.", "monitor")
            for c in range(1, len(cab) + 1):
                cel = res.cell(r, c)
                cel.font = Font(name=F, size=9, bold=(c == 2))
                cel.border = Border(bottom=LINEA)
                cel.alignment = Alignment(vertical="center", wrap_text=(c in (1, 9)),
                                          horizontal="right" if c in (2, 4, 5, 7) else "left")
            r += 1
        r += 1
    for col, w in zip("ABCDEFGHI", (36, 14, 18, 12, 13, 18, 15, 16, 48)):
        res.column_dimensions[col].width = w
    res.freeze_panes = "B5"

    fu = wb.create_sheet("Fuentes")
    titulo(fu, "Fuentes y trazabilidad", "Cada dato con su fuente, código de serie, URL y fecha de consulta.")
    cab_f = ["Indicador", "Fuente", "Código", "Nombre en la fuente", "Frecuencia", "Último dato", "Fecha de consulta", "URL", "Notas"]
    for j, t in enumerate(cab_f, start=1):
        encabezado(fu.cell(4, j), t)
    r = 5
    for b in datos["bloques"]:
        for ind in b["indicadores"]:
            vals = [ind["nombre"], ind.get("fuente", ""), ind.get("codigo", ""), ind.get("nombre_fuente", ""),
                    ind.get("frecuencia", ""), ind.get("fecha", ""), ind.get("fecha_consulta", ""), ind.get("url", ""),
                    " ".join(x for x in (ind.get("notas_fuente"), ind.get("nota"), ind.get("error")) if x)]
            for j, v in enumerate(vals, start=1):
                c = fu.cell(r, j, v)
                c.font = Font(name=F, size=9)
                c.alignment = Alignment(vertical="top", wrap_text=j in (4, 9))
            r += 1
    for col, w in zip("ABCDEFGHI", (36, 14, 30, 40, 10, 12, 14, 50, 60)):
        fu.column_dimensions[col].width = w
    fu.freeze_panes = "A5"

    wb.calculation.fullCalcOnLoad = True  # Excel recalcula al abrir
    salida.parent.mkdir(parents=True, exist_ok=True)
    wb.save(salida)
    print(f"-> {salida}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "monitor" / "tablero.xlsx")
