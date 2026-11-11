# Catálogo de fuentes

Estado del acceso: **✅ verificado** (conector probado con descarga real, con fecha) · **⏳ a verificar** (se prueba en Fase 2) · **📄 manual** (sin API; descarga de planilla/PDF).

Confiabilidad: **A** oficial primaria · **B** organismo internacional / compilador reconocido · **C** privada / agregador (contrastar con A o B).

## Uruguay

Ver detalle de series en [`uruguay.md`](uruguay.md).

| Fuente | Qué aporta | Acceso | Conf. | Estado |
|---|---|---|---|---|
| Banco Central del Uruguay (BCU) — bcu.gub.uy | Cuentas nacionales, tipo de cambio, tasas, agregados monetarios, balanza de pagos, deuda, expectativas de inflación | Planillas Excel en web; servicios web de cotizaciones | A | ⏳ |
| Instituto Nacional de Estadística (INE) — gub.uy/instituto-nacional-estadistica | IPC, mercado laboral (ECH), salarios, IMS | Planillas en web | A | ⏳ |
| Ministerio de Economía y Finanzas (MEF) — gub.uy/ministerio-economia-finanzas | Resultado fiscal, deuda, presupuesto | Planillas / PDF | A | ⏳ 📄 |
| MIEM — gub.uy/ministerio-industria-energia-mineria | Energía, industria | Planillas / PDF | A | ⏳ 📄 |
| Uruguay XXI — uruguayxxi.gub.uy | Exportaciones por producto y destino | Informes, planillas | A | ⏳ 📄 |
| DGI — gub.uy/direccion-general-impositiva | Recaudación | Planillas | A | ⏳ 📄 |
| OPP — gub.uy/oficina-planeamiento-presupuesto | Planificación, datos territoriales | Web / PDF | A | ⏳ 📄 |
| CERES, CPA Ferrere, Exante (y otras consultoras) | Indicadores líderes, análisis | Publicaciones | C | 📄 |

## Región

| Fuente | Qué aporta | Acceso | Conf. | Estado |
|---|---|---|---|---|
| BCRA (Argentina) | Tipo de cambio, reservas, tasas | API pública de estadísticas | A | ⏳ |
| INDEC (Argentina) | IPC, EMAE, empleo | Planillas / series | A | ⏳ |
| Banco Central do Brasil — SGS | Selic, IPCA, tipo de cambio, miles de series | API SGS (JSON/CSV) | A | ⏳ |
| IBGE (Brasil) | PIB, IPCA, empleo | API SIDRA | A | ⏳ |
| CEPAL — CEPALSTAT | Estadísticas comparadas de América Latina | API / descarga | B | ⏳ |
| BID | Estudios, datos regionales | Publicaciones / datos | B | 📄 |

## Global e instituciones internacionales

| Fuente | Qué aporta | Acceso | Conf. | Estado |
|---|---|---|---|---|
| FRED (Fed St. Louis) | Series de EE.UU. y muchas globales (tasas, Treasuries, DXY, commodities) | API (requiere key) + CSV público | B | ⏳ |
| Banco Mundial — World Bank Data | WDI: indicadores de desarrollo por país, anuales | API v2 abierta | B | ⏳ |
| FMI — WEO / DataMapper / IFS | Proyecciones WEO, estadísticas financieras | API DataMapper / SDMX | B | ⏳ |
| OCDE | Indicadores de miembros y socios | API SDMX | B | ⏳ |
| UN Data / UN Comtrade | Comercio internacional por producto | API (Comtrade con registro) | B | ⏳ |
| BIS | Crédito, tipos de cambio reales efectivos, precios de vivienda | API SDMX | B | ⏳ |
| BCE, Fed (Board) | Política monetaria de la Eurozona y EE.UU. | Web / SDMX | A | ⏳ |
| Trading Economics | Calendario, consenso, series diversas | Web (API paga) | C | 📄 |

## Mercados financieros

| Fuente | Qué aporta | Acceso | Conf. | Estado |
|---|---|---|---|---|
| Yahoo Finance (vía `yfinance`) | Acciones, índices, ETFs, futuros de commodities, tipos de cambio | Librería Python (no oficial) | C | ⏳ |
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
