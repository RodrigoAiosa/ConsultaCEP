"""
BuscaCEP — Versão com CSS inline (100% funcional)
"""
import streamlit as st

st.set_page_config(
    page_title="BuscaCEP",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS inline completo
st.markdown("""
<style>
    /* Reset e base */
    * { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
    }
    
    .stApp {
        background: #0a0e1a !important;
        position: relative;
        overflow-x: hidden;
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        z-index: 0;
        pointer-events: none;
        background:
            radial-gradient(680px circle at 12% 8%, rgba(56, 189, 248, 0.16), transparent 60%),
            radial-gradient(620px circle at 88% 18%, rgba(129, 140, 248, 0.14), transparent 60%),
            radial-gradient(900px circle at 50% 100%, rgba(56, 189, 248, 0.08), transparent 60%),
            linear-gradient(180deg, #0a0e1a 0%, #0f1524 45%, #0a0e1a 100%);
    }
    
    .block-container {
        position: relative !important;
        z-index: 1 !important;
        padding-top: 4.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 860px !important;
    }
    
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* Hero */
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
    
    .hero-title {
        font-size: 3.1rem;
        font-weight: 900;
        color: #f8fafc;
        line-height: 1.1;
        margin-bottom: 0.85rem;
        letter-spacing: -0.035em;
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
    
    /* Tabs */
    div[data-testid="stTabs"] {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.55), rgba(15, 23, 42, 0.45));
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 24px;
        padding: 2.1rem 2.2rem 1.6rem;
        box-shadow: 0 0 0 1px rgba(56, 189, 248, 0.04), 0 20px 60px -20px rgba(0, 0, 0, 0.55), 0 8px 24px -8px rgba(56, 189, 248, 0.08);
        backdrop-filter: blur(14px);
        margin-bottom: 2.6rem;
    }
    
    /* Inputs */
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
    
    /* Botões */
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
        display: flex;
        gap: 1rem;
        margin-top: 0.4rem;
    }
    
    .feature-box {
        flex: 1;
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(148, 163, 184, 0.14);
        border-radius: 16px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
    }
    
    .feature-box:hover {
        transform: translateY(-3px);
        border-color: rgba(56, 189, 248, 0.35);
        background: rgba(30, 41, 59, 0.6);
    }
    
    .feature-box .icon {
        font-size: 1.6rem;
        margin-bottom: 0.5rem;
    }
    
    .feature-box .label {
        color: #cbd5e1;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .footnote {
        text-align: center;
        color: #475569;
        margin-top: 2.8rem;
        font-size: 0.8rem;
    }
    
    @media (max-width: 640px) {
        .hero-title { font-size: 2.2rem; }
        .hero-subtitle { font-size: 1rem; }
        div[data-testid="stTabs"] { padding: 1.4rem 1.2rem 1.1rem; border-radius: 18px; }
        .features-row { flex-direction: column; }
    }
</style>
""", unsafe_allow_html=True)

# Hero
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

# Abas simplificadas
tab1, tab2, tab3 = st.tabs(["🔍 Busca individual", "📂 Busca em lote", "🏘️ Bairros por faixa"])

with tab1:
    st.info("🔍 Busca individual de CEP")
    cep = st.text_input("Digite o CEP:", placeholder="Ex: 01310100")
    if st.button("Buscar"):
        st.success(f"Buscando CEP: {cep}")

with tab2:
    st.info("📂 Busca em lote via planilha")
    st.file_uploader("Upload da planilha", type=["csv", "xlsx"])

with tab3:
    st.info("🏘️ Bairros por faixa de CEP")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("CEP inicial:", value="01000")
    with col2:
        st.text_input("CEP final:", value="01999")

# Rodapé
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
        BuscaCEP — Dados fornecidos pela API pública ViaCEP
    </div>
    """,
    unsafe_allow_html=True,
)
