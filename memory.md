# Memoria de criterio — Economista

Criterio validado por el usuario. Prevalece sobre la lectura propia. Si algo parece incorrecto, se plantea con AskUserQuestion; no se contradice en silencio.

## Decisiones de arquitectura (2026-11-10)

- Repo público `Diazdibona-collab/economista`. Clientes y material confidencial en `privado/` (excluido de git). Claves en `.env`.
- Foco: Uruguay + región (Argentina, Brasil) + mercados financieros + global/internacional.
- Primer producto: tablero de indicadores en web (Artifact) + Excel, con 4 bloques: macro Uruguay, mercados y tipo de cambio, región, global y commodities.
- Actualización del tablero: semanal, lunes 8:00 (Uruguay), con GitHub Actions.
- Formatos de informe: Word (doc-jmd), Markdown, web (Artifact), Excel.
- Python: paquetes en el Python global (sin venv).
- R: por ruta completa, sin tocar el PATH.
- `github.com/TheEconomist` (el semanario) se usa solo como **fuente de lectura** (big-mac-data, gdp-per-hour, etc.), nunca como destino.

## Criterio económico validado

_(se completa a medida que el usuario valide supuestos, definiciones y preferencias)_

## Preferencias de comunicación

- Toda pregunta al usuario, con AskUserQuestion.
- Español rioplatense, registro profesional.
