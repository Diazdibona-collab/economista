"""Genera el sitio estático del monitor: <salida>/index.html con los datos incrustados.

Uso:  python monitor/web.py [carpeta_salida]   (por defecto _site/)
"""

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


def main(salida: Path) -> None:
    datos = json.loads((RAIZ / "monitor" / "datos.json").read_text(encoding="utf-8"))
    js = json.dumps(datos, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = (RAIZ / "monitor" / "plantilla.html").read_text(encoding="utf-8").replace("__DATOS__", js)
    salida.mkdir(parents=True, exist_ok=True)
    (salida / "index.html").write_text(html, encoding="utf-8")
    (salida / ".nojekyll").write_text("", encoding="utf-8")
    print(f"-> {salida / 'index.html'} ({len(html) // 1024} KB)")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "_site")
