# Economista — centro de inteligencia económica

Repositorio de investigación y análisis económico con foco en **Uruguay, la región (Argentina y Brasil), los mercados financieros y la economía global**. Lo opera Claude Code en el rol de economista senior, con datos reales y fuentes trazables.

> Investigar como un economista, analizar como un científico de datos, comunicar como un consultor económico.

## Principios

- Datos reales y recientes; cada cifra tiene fuente, período y fecha de consulta.
- Nunca se inventan datos ni fuentes; lo no verificado se declara.
- Hechos, estimaciones, hipótesis y proyecciones van diferenciados.
- Supuestos y limitaciones explícitos; correlación ≠ causalidad.

## Estructura

```
fuentes/          Catálogo de fuentes y series clave de Uruguay
src/econ/         Paquete Python: conectores, transformaciones, modelos, gráficos
R/                Econometría específica en R
data/raw/         Descargas crudas (no versionadas)
data/processed/   Series limpias con metadatos de trazabilidad
analisis/         Un análisis por carpeta (AAAA-MM-tema)
informes/         Informes terminados y plantillas
monitor/          Tablero de indicadores (web + Excel), actualización semanal
```

## Uso rápido

```bash
pip install -r requirements.txt
cp .env.example .env   # completar FRED_API_KEY
```

```python
import sys; sys.path.insert(0, "src")
from econ import series, modelos
```

## Hoja de ruta

- [x] **Fase 1 — Base:** estructura, reglas, catálogo de fuentes, paquete base, subagentes.
- [ ] **Fase 2 — Conectores:** FRED, Banco Mundial, FMI, BCU, INE, BCB (SGS), BCRA, mercados (yfinance). Cada uno probado con descarga real.
- [ ] **Fase 3 — Tablero:** macro Uruguay · mercados y tipo de cambio · región · global y commodities. Web + Excel.
- [ ] **Fase 4 — Automatización:** GitHub Actions, lunes 8:00 (Uruguay).
- [ ] **Fase 5 — Plantillas de informe:** coyuntura, país, sector, financiero, resumen ejecutivo.

## Aviso

Material de análisis con fines informativos. No constituye asesoramiento de inversión.
