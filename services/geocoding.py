"""
Serviço de geocodificação via Nominatim (OpenStreetMap), gratuito e sem chave.
Converte um endereço textual em coordenadas (latitude, longitude).
"""
import requests
import streamlit as st

from config import NOMINATIM_URL, NOMINATIM_USER_AGENT, REQUEST_TIMEOUT_SECONDS, CACHE_TTL_SECONDS


@st.cache_data(show_spinner=False, ttl=CACHE_TTL_SECONDS)
def _geocode_query(query: str) -> tuple[float, float] | None:
    """Chama o Nominatim para uma única query textual de endereço."""
    params = {"q": query, "format": "json", "limit": 1, "countrycodes": "br"}
    headers = {"User-Agent": NOMINATIM_USER_AGENT}
    resp = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        return None
    return float(results[0]["lat"]), float(results[0]["lon"])


def geocodificar_com_fallback(dados: dict) -> tuple[float, float, str] | None:
    """
    Tenta geocodificar do nível mais preciso (rua) até o mais genérico (estado),
    garantindo que o mapa sempre tenha uma localização para mostrar.

    Retorna (lat, lon, nivel_precisao) ou None se nada for encontrado.
    """
    logradouro = dados.get("logradouro")
    bairro = dados.get("bairro")
    cidade = dados.get("localidade")
    uf = dados.get("uf")

    tentativas = []
    if logradouro and bairro and cidade and uf:
        tentativas.append((f"{logradouro}, {bairro}, {cidade}, {uf}, Brasil", "rua"))
    if logradouro and cidade and uf:
        tentativas.append((f"{logradouro}, {cidade}, {uf}, Brasil", "rua"))
    if bairro and cidade and uf:
        tentativas.append((f"{bairro}, {cidade}, {uf}, Brasil", "bairro"))
    if cidade and uf:
        tentativas.append((f"{cidade}, {uf}, Brasil", "cidade"))
    if uf:
        tentativas.append((f"{uf}, Brasil", "estado"))

    for query, nivel in tentativas:
        try:
            resultado = _geocode_query(query)
        except requests.RequestException:
            continue
        if resultado:
            lat, lon = resultado
            return lat, lon, nivel

    return None
