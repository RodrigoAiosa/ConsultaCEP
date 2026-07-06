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
    layout="wide",
    initial_sidebar_state="collapsed",
)


def carregar_css(caminho: Path) -> bool:
    """
    Injeta um arquivo .css externo na página.
    
    Returns:
        bool: True se o CSS foi carregado com sucesso, False caso contrário.
    """
    try:
        if not caminho.exists():
            st.error(f"❌ Arquivo CSS não encontrado em: {caminho}")
            return False
            
        css = caminho.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        
        # Log de sucesso (visível no terminal do Streamlit)
        print(f"✅ CSS carregado com sucesso de: {caminho}")
        return True
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar CSS: {e}")
        print(f"❌ Erro ao carregar CSS: {e}")
        return False


# ----------------------------------------------------------------------------
# CARREGAR CSS COM VERIFICAÇÃO
# ----------------------------------------------------------------------------
# Tenta carregar o CSS do caminho esperado
css_path = BASE_DIR / "assets" / "styles.css"
css_carregado = carregar_css(css_path)

# Se não encontrou no caminho esperado, tenta na raiz
if not css_carregado:
    css_path_fallback = BASE_DIR / "styles.css"
    if css_path_fallback.exists():
        carregar_css(css_path_fallback)
    else:
        # Fallback: CSS inline mínimo para garantir que a página não fique em branco
        st.markdown("""
        <style>
            /* CSS de fallback caso o arquivo não seja encontrado */
            .stApp {
                background: #0a0e1a !important;
            }
            .block-container {
                padding-top: 4.5rem !important;
                padding-bottom: 4rem !important;
                max-width: 860px !important;
            }
            .hero-title {
                font-size: 3.1rem;
                font-weight: 900;
                color: #f8fafc;
                line-height: 1.1;
                margin-bottom: 0.85rem;
            }
            .hero-title span {
                background: linear-gradient(90deg, #38bdf8, #818cf8 60%, #a78bfa);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .hero-subtitle {
                font-size: 1.12rem;
                color: #94a3b8;
                margin-bottom: 1.8rem;
                max-width: 560px;
                line-height: 1.65;
            }
            .hero-badge {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: rgba(56, 189, 248, 0.10);
                color: #7dd3fc;
                border: 1px solid rgba(56, 189, 248, 0.30);
                padding: 6px 16px;
                border-radius: 999px;
                font-size: 0.76rem;
                font-weight: 600;
                letter-spacing: 0.03em;
                margin-bottom: 1.4rem;
            }
            .trust-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
                margin-bottom: 2.6rem;
            }
            .trust-chip {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                background: rgba(148, 163, 184, 0.06);
                border: 1px solid rgba(148, 163, 184, 0.16);
                color: #cbd5e1;
                padding: 6px 13px;
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 500;
            }
            div[data-testid="stTabs"] {
                background: linear-gradient(180deg, rgba(30, 41, 59, 0.55), rgba(15, 23, 42, 0.45));
                border: 1px solid rgba(148, 163, 184, 0.14);
                border-radius: 24px;
                padding: 2.1rem 2.2rem 1.6rem;
                box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.04), 0 20px 60px -20px rgba(0, 0, 0, 0.55), 0 8px 24px -8px rgba(56, 189, 248, 0.08);
                backdrop-filter: blur(14px);
                margin-bottom: 2.6rem;
            }
            .stButton > button {
                background: linear-gradient(90deg, #38bdf8, #6366f1);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 0.85rem 1.6rem;
                font-weight: 700;
                font-size: 1rem;
                width: 100%;
                letter-spacing: -0.01em;
                box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.4);
                transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 28px -6px rgba(99, 102, 241, 0.5);
                filter: brightness(1.06);
            }
            div[data-testid="stTextInput"] input {
                background-color: rgba(15, 23, 42, 0.6);
                color: #f8fafc;
                border: 1px solid #334155;
                border-radius: 12px;
                padding: 0.9rem 1.05rem;
                font-size: 1.05rem;
                transition: border-color 0.15s ease, box-shadow 0.15s ease;
            }
            div[data-testid="stTextInput"] input:focus {
                border: 1px solid #38bdf8;
                box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.14);
            }
            .result-card {
                background: rgba(15, 23, 42, 0.55);
                border: 1px solid rgba(148, 163, 184, 0.16);
                border-radius: 18px;
                padding: 1.9rem 2rem;
                margin-top: 1.8rem;
                animation: fadeUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
            }
            @keyframes fadeUp {
                from { opacity: 0; transform: translateY(14px); }
                to   { opacity: 1; transform: translateY(0); }
            }
            #MainMenu { visibility: hidden; }
            footer { visibility: hidden; }
            header { visibility: hidden; }
        </style>
        """, unsafe_allow_html=True)
        print("⚠️ Usando CSS de fallback (inline)")


# ----------------------------------------------------------------------------
# HERO / LANDING
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="hero-badge">📍 Feito com dados oficiais dos Correios</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-title">Encontre qualquer<br><span>endereço do Brasil</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-subtitle">Digite um CEP e descubra rua, bairro, cidade, estado — '
    'ou envie uma planilha inteira e baixe tudo processado em .csv.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="trust-row">
        <span class="trust-chip">⚡ Resultado em segundos</span>
        <span class="trust-chip">🔓 Sem cadastro</span>
        <span class="trust-chip">💸 100% gratuito</span>
        <span class="trust-chip">📊 Exporta em .csv</span>
        <span class="trust-chip">🗺️ Mapa incluso</span>
    </div>
    """,
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
st.markdown(
    """
    <div class="features-row">
        <div class="feature-box">
            <div class="icon">⚡</div>
            <div class="label">Rápido e direto</div>
        </div>
        <div class="feature-box">
            <div class="icon">🔒</div>
            <div class="label">Privacidade total</div>
        </div>
        <div class="feature-box">
            <div class="icon">📦</div>
            <div class="label">Dados oficiais</div>
        </div>
    </div>
    <div class="footnote">
        BuscaCEP — Dados fornecidos pela API pública ViaCEP e geocodificação pelo OpenStreetMap
    </div>
    """,
    unsafe_allow_html=True,
)
