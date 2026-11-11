# Uruguay — series clave

Series objetivo para el monitor y los informes de coyuntura. La columna "Código / ubicación" se completa en Fase 2 al verificar cada conector; mientras diga "a verificar", **no se usa ningún dato de esa serie**.

## Actividad

| Indicador | Fuente | Frecuencia | Código / ubicación | Notas |
|---|---|---|---|---|
| PIB real (volumen, desestacionalizado) | BCU – Cuentas Nacionales | Trimestral | a verificar | Variación t/t-1 e interanual |
| PIB real trimestral (volumen, **sin** desestacionalizar) | FMI QNEA (dato BCU) | Trimestral | ✅ `imf.sta("QNEA", "URY.B1GQ.Q.NSA.XDC.Q")` — último 2026-T2 | Usar para variación interanual hasta tener la serie desestacionalizada del BCU |
| Crecimiento real del PIB anual + proyecciones | FMI WEO | Anual | ✅ `imf.weo("URY", "NGDP_RPCH")` | Años futuros = proyección FMI |
| Crecimiento real del PIB anual | Banco Mundial WDI | Anual | ✅ `worldbank.obtener("URY", "NY.GDP.MKTP.KD.ZG")` — último 2025: 1,78 % | |
| PIB por sector de actividad | BCU | Trimestral | a verificar | |
| Indicador mensual de actividad / líderes | CERES u otro | Mensual | a verificar | Fuente privada (C) |
| Índice de volumen físico de la industria manufacturera | INE | Mensual | a verificar | |

## Precios

| Indicador | Fuente | Frecuencia | Código / ubicación | Notas |
|---|---|---|---|---|
| IPC general, var. mensual e interanual | INE | Mensual | ✅ `ine.ipc("indice" / "var_mensual" / "var_12m")` — último oct-2026: 4,87 % i.a. | Base oct-2022 = 100. Contrastado con FMI CPI (coincide) |
| Inflación subyacente | BCU / INE | Mensual | a verificar | |
| Expectativas de inflación (empresariales y de analistas) | BCU / INE | Mensual | a verificar | Comparar con rango meta del BCU |

## Mercado laboral e ingresos

| Indicador | Fuente | Frecuencia | Código / ubicación | Notas |
|---|---|---|---|---|
| Tasa de desempleo, actividad y empleo | INE – ECH | Mensual / trimestral | a verificar | Cambio metodológico de la ECH en 2021: cuidar comparabilidad |
| Índice medio de salarios (IMS) nominal y real | INE | Mensual | a verificar | |

## Monetario, tasas y tipo de cambio

| Indicador | Fuente | Frecuencia | Código / ubicación | Notas |
|---|---|---|---|---|
| Tasa de política monetaria | BCU | Por decisión (COPOM) | a verificar | Sin acceso automático aún (BIS no la publica) |
| Tasa del mercado monetario (call) | FMI MFS_IR | Mensual | ✅ `imf.sta("MFS_IR", "URY.MMRT_RT_PT_A_PT.M")` — ago-2026: 5,75 % | **Proxy** de la TPM, no es la TPM oficial |
| Rendimiento de letras del gobierno | FMI MFS_IR | Mensual | ✅ `imf.sta("MFS_IR", "URY.GSTBILY_RT_PT_A_PT.M")` | |
| Tipo de cambio USD/UYU oficial | BCU (web service) | Diaria | ✅ `bcu.cotizacion(2222)` — 10-nov-2026: 40,519 | Tipo vendedor. NO usar Yahoo `UYU=X` |
| Curva soberana en pesos | BEVSA / BCU | Diaria | a verificar | |
| Riesgo país (spread soberano) | a definir | Diaria | a verificar | Fuente pública a confirmar |
| Reservas internacionales | BCU | Diaria | ✅ `bcu.reservas()` — 9-nov-2026: 18.282 MUSD | Activos de reserva, definición MBP5 |

## Sector externo

| Indicador | Fuente | Frecuencia | Código / ubicación | Notas |
|---|---|---|---|---|
| Exportaciones de bienes por producto y destino | Uruguay XXI / BCU | Mensual | a verificar | Soja, carne, celulosa, lácteos |
| Balanza de pagos (cuenta corriente) | BCU | Trimestral | a verificar | |
| Tipo de cambio real efectivo | BCU | Mensual | a verificar | Con Argentina, Brasil y extrarregionales |

## Fiscal

| Indicador | Fuente | Frecuencia | Código / ubicación | Notas |
|---|---|---|---|---|
| Resultado fiscal global y primario (% PIB, 12 meses) | MEF | Mensual | a verificar | Con y sin efecto "cincuentones" |
| Deuda bruta y neta del sector público (% PIB) | BCU / MEF | Trimestral | a verificar | |
| Recaudación DGI real | DGI | Mensual | a verificar | |
