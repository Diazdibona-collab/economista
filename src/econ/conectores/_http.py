"""Sesión HTTP común: reintentos, timeouts y cadena de certificados para sitios .gub.uy."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import certifi
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

UA = "Mozilla/5.0 (compatible; economista-research/0.1)"
TIMEOUT = 90

# El servidor de www.bcu.gub.uy no envía sus certificados intermedios (Abitab OV -> Certum Global
# Services CA SHA2). En lugar de desactivar la verificación SSL, se agregan esos intermedios públicos
# (descargados de repository.certum.pl, vía AIA del propio certificado) al bundle de certifi.
_INTERMEDIOS = Path(__file__).with_name("certs") / "intermedios_gub_uy.pem"


@lru_cache(maxsize=1)
def bundle_gub_uy() -> str:
    destino = Path(os.environ.get("TEMP", "/tmp")) / "econ_bundle_gub_uy.pem"
    destino.write_text(
        Path(certifi.where()).read_text(encoding="utf-8") + "\n" + _INTERMEDIOS.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return str(destino)


@lru_cache(maxsize=1)
def sesion() -> requests.Session:
    s = requests.Session()
    s.headers["User-Agent"] = UA
    reintentos = Retry(total=4, backoff_factor=2, status_forcelist=(429, 500, 502, 503, 504), allowed_methods=None)
    s.mount("https://", HTTPAdapter(max_retries=reintentos))
    s.mount("http://", HTTPAdapter(max_retries=reintentos))
    return s


def get(url: str, **kw) -> requests.Response:
    kw.setdefault("timeout", TIMEOUT)
    if "bcu.gub.uy" in url:
        kw.setdefault("verify", bundle_gub_uy())
    r = sesion().get(url, **kw)
    r.raise_for_status()
    return r


def post(url: str, **kw) -> requests.Response:
    kw.setdefault("timeout", TIMEOUT)
    if "bcu.gub.uy" in url:
        kw.setdefault("verify", bundle_gub_uy())
    r = sesion().post(url, **kw)
    r.raise_for_status()
    return r
