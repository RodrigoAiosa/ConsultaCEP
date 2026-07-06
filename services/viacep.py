"""
Serviço de acesso à API pública ViaCEP (https://viacep.com.br).
Gratuita, sem necessidade de chave de API.
"""
import requests
import streamlit as st

from config import VIACEP_BASE_URL, REQUEST_TIMEOUT_SECONDS, CACHE_TTL_SECONDS


def limpar_cep(cep: str) -> str:
    """Remove qualquer caractere não numérico de um CEP."""
    return "".join(filter(str.isdigit, cep or ""))


@st.cache_data(show_spinner=False, ttl=CACHE_TTL_SECONDS)
def buscar_cep(cep: str) -> dict | None:
    """
    Consulta um CEP na API ViaCEP.

    Retorna o dicionário de dados do endereço, ou None se o CEP não existir.
    Propaga requests.RequestException em caso de falha de conexão.
    """
    url = VIACEP_BASE_URL.format(cep=cep)
    resp = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
    resp.raise_for_status()
    data = resp.json()
    if data.get("erro"):
        return None
    return data
