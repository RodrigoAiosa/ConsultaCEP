"""
BuscaCEP — ponto de entrada da aplicação Streamlit.

Este arquivo cuida apenas de:
  1. Configuração da página
  2. Carregamento do CSS externo
  3. Hero / landing
  4. Orquestração das abas (delegando a renderização a components/)

Toda a lógica de negócio vive em services/ e utils/;
toda a UI de cada funcionalidade vive em components/.
"""
from pathlib import Path

import streamlit as st

from config import APP_TITLE, APP_ICON
from components import individual_search, batch_search, cep_range

BASE_DIR = Path(__file__).parent


# ----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="centered",
    initial_sidebar_state="collapsed",
)


def carregar_css(caminho: Path) -> None:
    """Injeta um arquivo .css externo na página."""
    css = caminho.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


carregar_css(BASE_DIR / "assets" / "styles.css")


# ----------------------------------------------------------------------------
# HERO / LANDING
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="hero-title">Encontre qualquer<br><span>endereço do Brasil</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-subtitle">Digite um CEP e descubra rua, bairro, cidade, estado — '
    'ou envie uma planilha inteira e baixe tudo processado em .csv.</div>',
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# ABAS
# ----------------------------------------------------------------------------
tab_individual, tab_lote, tab_faixa = st.tabs([
    "🔍 Busca individual",
    "📂 Busca em lote (planilha)",
    "🏘️ Bairros por faixa de CEP",
])

with tab_individual:
    individual_search.render()

with tab_lote:
    batch_search.render()

with tab_faixa:
    cep_range.render()

# ----------------------------------------------------------------------------
# RODAPÉ / FEATURES
# ----------------------------------------------------------------------------
st.markdown("""
<div class="features-row">
    <div class="feature-box"><div class="icon">⚡</div><div class="label">Busca instantânea</div></div>
    <div class="feature-box"><div class="icon">🗺️</div><div class="label">Mapa interativo</div></div>
    <div class="feature-box"><div class="icon">🔓</div><div class="label">100% gratuito</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<p class="footnote">Dados via ViaCEP e OpenStreetMap Nominatim · '
    'Sem necessidade de chave de API</p>',
    unsafe_allow_html=True,
)
