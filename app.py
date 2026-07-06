"""
BuscaCEP — ponto de entrada da aplicação Streamlit.
"""
import streamlit as st
from pathlib import Path

# Configuração da página DEVE ser a primeira chamada Streamlit
st.set_page_config(
    page_title="BuscaCEP | Consulta de Endereços",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CARREGAR CSS
# ============================================================================
BASE_DIR = Path(__file__).parent

def carregar_css():
    """Carrega o CSS do arquivo ou usa fallback inline"""
    css_path = BASE_DIR / "assets" / "styles.css"
    
    if css_path.exists():
        try:
            css = css_path.read_text(encoding="utf-8")
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
            print(f"✅ CSS carregado de: {css_path}")
            return True
        except Exception as e:
            print(f"❌ Erro ao ler CSS: {e}")
    
    # Fallback: CSS inline completo
    print("⚠️ Usando CSS inline fallback")
    st.markdown("""
    <style>
        /* Reset completo */
        html, body, .stApp, .main, .block-container {
            background: #0a0e1a !important;
            background-color: #0a0e1a !important;
        }
        
        .block-container {
            padding-top: 4.5rem !important;
            padding-bottom: 4rem !important;
            max-width: 860px !important;
        }
        
        #MainMenu { visibility: hidden !important; }
        footer { visibility: hidden !important; }
        header { visibility: hidden !important; }
        
        .hero-badge {
            display: inline-flex !important;
            align-items: center !important;
            gap: 6px !important;
            background: rgba(56, 189, 248, 0.10) !important;
            color: #7dd3fc !important;
            border: 1px solid rgba(56, 189, 248, 0.30) !important;
            padding: 6px 16px !important;
            border-radius: 999px !important;
            font-size: 0.76rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.03em !important;
            margin-bottom: 1.4rem !important;
        }
        
        .hero-title {
            font-size: 3.1rem !important;
            font-weight: 900 !important;
            color: #f8fafc !important;
            line-height: 1.1 !important;
            margin-bottom: 0.85rem !important;
            letter-spacing: -0.035em !important;
        }
        
        .hero-title span {
            background: linear-gradient(90deg, #38bdf8, #818cf8 60%, #a78bfa) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        
        .hero-subtitle {
            font-size: 1.12rem !important;
            color: #94a3b8 !important;
            margin-bottom: 1.8rem !important;
            max-width: 560px !important;
            line-height: 1.65 !important;
        }
        
        .trust-row {
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 0.55rem !important;
            margin-bottom: 2.6rem !important;
        }
        
        .trust-chip {
            display: inline-flex !important;
            align-items: center !important;
            gap: 6px !important;
            background: rgba(148, 163, 184, 0.06) !important;
            border: 1px solid rgba(148, 163, 184, 0.16) !important;
            color: #cbd5e1 !important;
            padding: 6px 13px !important;
            border-radius: 999px !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
        }
        
        div[data-testid="stTabs"] {
            background: linear-gradient(180deg, rgba(30, 41, 59, 0.55), rgba(15, 23, 42, 0.45)) !important;
            border: 1px solid rgba(148, 163, 184, 0.14) !important;
            border-radius: 24px !important;
            padding: 2.1rem 2.2rem 1.6rem !important;
            box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.04), 0 20px 60px -20px rgba(0, 0, 0, 0.55), 0 8px 24px -8px rgba(56, 189, 248, 0.08) !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            margin-bottom: 2.6rem !important;
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #38bdf8, #6366f1) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.85rem 1.6rem !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            width: 100% !important;
            letter-spacing: -0.01em !important;
            box-shadow: 0 4px 14px -4px rgba(99, 102, 241, 0.4) !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 28px -6px rgba(99, 102, 241, 0.5) !important;
            filter: brightness(1.06) !important;
        }
        
        .features-row {
            display: flex !important;
            gap: 1rem !important;
            margin-top: 0.4rem !important;
        }
        
        .feature-box {
            flex: 1 !important;
            background: rgba(30, 41, 59, 0.4) !important;
            border: 1px solid rgba(148, 163, 184, 0.14) !important;
            border-radius: 16px !important;
            padding: 1.2rem 1rem !important;
            text-align: center !important;
            transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease !important;
        }
        
        .feature-box:hover {
            transform: translateY(-3px) !important;
            border-color: rgba(56, 189, 248, 0.35) !important;
            background: rgba(30, 41, 59, 0.6) !important;
        }
        
        .feature-box .icon {
            font-size: 1.6rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .feature-box .label {
            color: #cbd5e1 !important;
            font-size: 0.85rem !important;
            font-weight: 600 !important;
        }
        
        .footnote {
            text-align: center !important;
            color: #475569 !important;
            margin-top: 2.8rem !important;
            font-size: 0.8rem !important;
        }
        
        .result-card {
            background: rgba(15, 23, 42, 0.55) !important;
            border: 1px solid rgba(148, 163, 184, 0.16) !important;
            border-radius: 18px !important;
            padding: 1.9rem 2rem !important;
            margin-top: 1.8rem !important;
        }
        
        .result-title {
            font-size: 1.35rem !important;
            font-weight: 700 !important;
            color: #f8fafc !important;
            margin-bottom: 1.1rem !important;
            display: flex !important;
            align-items: center !important;
            gap: 8px !important;
        }
        
        .full-address-box {
            background: rgba(56, 189, 248, 0.08) !important;
            border: 1px solid rgba(56, 189, 248, 0.28) !important;
            border-radius: 12px !important;
            padding: 0.9rem 1.1rem !important;
            color: #e0f2fe !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            line-height: 1.5 !important;
            margin-bottom: 1.3rem !important;
        }
        
        .info-row {
            display: flex !important;
            justify-content: space-between !important;
            padding: 0.6rem 0 !important;
            border-bottom: 1px solid rgba(148, 163, 184, 0.12) !important;
        }
        
        .info-row:last-child {
            border-bottom: none !important;
        }
        
        .info-label {
            color: #94a3b8 !important;
            font-size: 0.9rem !important;
        }
        
        .info-value {
            color: #f1f5f9 !important;
            font-weight: 600 !important;
            font-size: 0.94rem !important;
            text-align: right !important;
            font-variant-numeric: tabular-nums !important;
        }
        
        @media (max-width: 640px) {
            .hero-title { font-size: 2.2rem !important; }
            .hero-subtitle { font-size: 1rem !important; }
            div[data-testid="stTabs"] { padding: 1.4rem 1.2rem 1.1rem !important; border-radius: 18px !important; }
            .features-row { flex-direction: column !important; }
        }
    </style>
    """, unsafe_allow_html=True)
    return False

# Carrega o CSS
carregar_css()

# ============================================================================
# IMPORTAR COMPONENTES
# ============================================================================
# Importa depois do CSS para garantir que não há conflitos
from components import individual_search, batch_search, cep_range

# ============================================================================
# HERO / LANDING
# ============================================================================
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

# ============================================================================
# ABAS
# ============================================================================
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

# ============================================================================
# RODAPÉ
# ============================================================================
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
