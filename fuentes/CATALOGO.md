# Catálogo de fuentes

Estado del acceso: **✅ verificado** (conector probado con descarga real, con fecha) · **⏳ a verificar** (se prueba en Fase 2) · **📄 manual** (sin API; descarga de planilla/PDF).

Confiabilidad: **A** oficial primaria · **B** organismo internacional / compilador reconocido · **C** privada / agregador (contrastar con A o B).

## Uruguay

Ver detalle de series en [`uruguay.md`](uruguay.md).

| Fuente | Qué aporta | Acceso | Conf. | Estado |
|---|---|---|---|---|
| BCU — web service de cotizaciones | Tipo de cambio oficial diario (2222 = dólar billete) | SOAP `cotizaciones.bcu.gub.uy` · `bcu.cotizacion()` | A | ✅ 2026-11-10 |
| BCU — reservas internacionales | Activos de reserva diarios (MUSD) | Planilla `reservas.xls` · `bcu.reservas()` | A | ✅ 2026-11-10 |
| BCU — resto de estadísticas (bcu.gub.uy) | Cuentas nacionales, tasas, agregados, balanza de pagos, deuda, expectativas | Web SharePoint con enlaces dinámicos y Power BI; **no hay enlaces directos estables**. Requiere certificados intermedios (incluidos en `conectores/certs/`) | A | ⚠️ pendiente: por ahora se cubre con FMI |
| Instituto Nacional de Estadística (INE) — IPC | IPC general total país, índice y variaciones, desde 1937 | Planilla `www5.ine.gub.uy` (base oct-2022) · `ine.ipc()` | A | ✅ 2026-11-10 |
| Instituto Nacional de Estadística (INE) — mercado laboral y salarios | ECH (desempleo, empleo), IMS | Planillas en `www5.ine.gub.uy` | A | ⏳ |
| Ministerio de Economía y Finanzas (MEF) — gub.uy/ministerio-economia-finanzas | Resultado fiscal, deuda, presupuesto | Planillas / PDF | A | ⏳ 📄 |
| MIEM — gub.uy/ministerio-industria-energia-mineria | Energía, industria | Planillas / PDF | A | ⏳ 📄 |
| Uruguay XXI — uruguayxxi.gub.uy | Exportaciones por producto y destino | Informes, planillas | A | ⏳ 📄 |
| DGI — gub.uy/direccion-general-impositiva | Recaudación | Planillas | A | ⏳ 📄 |
| OPP — gub.uy/oficina-planeamiento-presupuesto | Planificación, datos territoriales | Web / PDF | A | ⏳ 📄 |
| CERES, CPA Ferrere, Exante (y otras consultoras) | Indicadores líderes, análisis | Publicaciones | C | 📄 |

## Región

| Fuente | Qué aporta | Acceso | Conf. | Estado |
|---|---|---|---|---|
| BCRA (Argentina) | Tipo de cambio, reservas, tasas (~1.600 variables) | API Estadísticas **v4.0** (la v3 responde 410) · `bcra.obtener()` | A | ✅ 2026-11-10 |
| INDEC (Argentina) | IPC, EMAE, empleo | Planillas / series | A | ⏳ |
| Banco Central do Brasil — SGS | Selic, IPCA, tipo de cambio, miles de series | API SGS (JSON) · `bcb.sgs()`. La meta Selic (432) trae fechas futuras: se recortan a hoy | A | ✅ 2026-11-10 |
| IBGE (Brasil) | PIB, IPCA, empleo | API SIDRA | A | ⏳ |
| CEPAL — CEPALSTAT | Estadísticas comparadas de América Latina | API / descarga | B | ⏳ |
| BID | Estudios, datos regionales | Publicaciones / datos | B | 📄 |

## Global e instituciones internacionales

| Fuente | Qué aporta | Acceso | Conf. | Estado |
|---|---|---|---|---|
| FRED (Fed St. Louis) | Series de EE.UU. y muchas globales (tasas, Treasuries, DXY, commodities) | API con key (`.env` / secreto del repo) · `fred.obtener()` | B | ✅ 2026-11-10 |
| Banco Mundial — World Bank Data | WDI: indicadores de desarrollo por país, anuales | API v2 abierta (lenta: timeout 90 s) · `worldbank.obtener()` | B | ✅ 2026-11-10 |
| FMI — WEO y bases IMF.STA (CPI, QNEA, MFS_IR, ER, IRFCL…) | Proyecciones WEO; IPC, PIB trimestral, tasas y tipo de cambio por país | API **SDMX 3.0** `api.imf.org` · `imf.weo()`, `imf.sta()`. La API DataMapper bloquea clientes automatizados (403) | B | ✅ 2026-11-10 |
| OCDE | Indicadores de miembros y socios | API SDMX | B | ⏳ |
| UN Data / UN Comtrade | Comercio internacional por producto | API (Comtrade con registro) | B | ⏳ |
| BIS | Crédito, tipos de cambio reales efectivos, precios de vivienda | API SDMX v2 (`stats.bis.org`). **No incluye la tasa de política de Uruguay** (WS_CBPOL sin UY) | B | ⏳ |
| BCE, Fed (Board) | Política monetaria de la Eurozona y EE.UU. | Web / SDMX | A | ⏳ |
| Trading Economics | Calendario, consenso, series diversas | Web (API paga) | C | 📄 |

## Mercados financieros

| Fuente | Qué aporta | Acceso | Conf. | Estado |
|---|---|---|---|---|
| Yahoo Finance (vía `yfinance`) | Acciones, índices, ETFs, futuros de commodities, tipos de cambio | Librería Python (no oficial) · `mercados.precio()`. **`UYU=X` no coincide con el BCU (39,07 vs 40,3): no usar para el peso** | C | ✅ 2026-11-10 |
| FRED | Treasuries, spreads, VIX, petróleo, oro | API / CSV | B | ⏳ |
| BEVSA (Uruguay) | Bonos y letras en pesos, tipo de cambio interbancario | Web | A | ⏳ 📄 |
| JP Morgan EMBI (riesgo país) | Spread soberano | No es público; buscar vía BCU/republica AFISA/prensa | C | ⏳ |

## Datos y modelos de referencia

| Fuente | Qué aporta | Acceso | Conf. | Estado |
|---|---|---|---|---|
| The Economist — github.com/TheEconomist | Índice Big Mac (`big-mac-data`), PIB por hora (`the-economist-gdp-per-hour-estimates`), otros modelos replicables | Repos públicos (lectura) | B | ⏳ |
| Penn World Table, Maddison Project | Series largas comparables de PIB y productividad | Descarga | B | 📄 |

## Regla de registro

Cada serie descargada se guarda con metadatos: `fuente`, `codigo_serie`, `unidad`, `frecuencia`, `periodo_inicio`, `periodo_fin`, `fecha_consulta`, `url`. Sin metadatos, la serie no se usa en un informe.
