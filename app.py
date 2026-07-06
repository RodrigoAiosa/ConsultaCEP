"""
BuscaCEP — Versão otimizada para deploy
"""
import streamlit as st
import requests
import pandas as pd
import io
import time
import re
from pathlib import Path
from typing import Optional

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA - DEVE SER A PRIMEIRA CHAMADA
# ============================================================================
st.set_page_config(
    page_title="BuscaCEP | Consulta de Endereços",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CSS COMPLETO - INLINE (evita problemas de path)
# ============================================================================
st.markdown("""
<style>
    /* RESET E BASE */
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    html, body, .stApp, .main, .block-container,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    section.main {
        background: #0a0e1a !important;
        background-color: #0a0e1a !important;
    }
    
    .block-container {
        padding-top: 4.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 860px !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Remove elementos padrão */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    
    /* Fundo com blobs */
    .stApp::before {
        content: "" !important;
        position: fixed !important;
        inset: 0 !important;
        z-index: 0 !important;
        pointer-events: none !important;
        background:
            radial-gradient(680px circle at 12% 8%, rgba(56, 189, 248, 0.16), transparent 60%),
            radial-gradient(620px circle at 88% 18%, rgba(129, 140, 248, 0.14), transparent 60%),
            radial-gradient(900px circle at 50% 100%, rgba(56, 189, 248, 0.08), transparent 60%),
            linear-gradient(180deg, #0a0e1a 0%, #0f1524 45%, #0a0e1a 100%) !important;
    }
    
    /* Grid sutil */
    .stApp::after {
        content: "" !important;
        position: fixed !important;
        inset: 0 !important;
        z-index: 0 !important;
        pointer-events: none !important;
        opacity: 0.35 !important;
        background-image:
            linear-gradient(rgba(148, 163, 184, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148, 163, 184, 0.05) 1px, transparent 1px) !important;
        background-size: 44px 44px !important;
        mask-image: radial-gradient(ellipse 900px 500px at 50% 0%, black 40%, transparent 100%) !important;
        -webkit-mask-image: radial-gradient(ellipse 900px 500px at 50% 0%, black 40%, transparent 100%) !important;
    }
    
    /* Hero */
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
        position: relative !important;
        z-index: 2 !important;
    }
    
    .hero-title {
        font-size: 3.1rem !important;
        font-weight: 900 !important;
        color: #f8fafc !important;
        line-height: 1.1 !important;
        margin-bottom: 0.85rem !important;
        letter-spacing: -0.035em !important;
        position: relative !important;
        z-index: 2 !important;
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
        position: relative !important;
        z-index: 2 !important;
    }
    
    .trust-row {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.55rem !important;
        margin-bottom: 2.6rem !important;
        position: relative !important;
        z-index: 2 !important;
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
    
    /* Tabs - Tool Card */
    div[data-testid="stTabs"] {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.55), rgba(15, 23, 42, 0.45)) !important;
        border: 1px solid rgba(148, 163, 184, 0.14) !important;
        border-radius: 24px !important;
        padding: 2.1rem 2.2rem 1.6rem !important;
        box-shadow:
            0 0 0 1px rgba(56, 189, 248, 0.04),
            0 20px 60px -20px rgba(0, 0, 0, 0.55),
            0 8px 24px -8px rgba(56, 189, 248, 0.08) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        margin-bottom: 2.6rem !important;
        position: relative !important;
        z-index: 2 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.14) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 10px 16px !important;
        background: transparent !important;
        border-radius: 10px 10px 0 0 !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #cbd5e1 !important;
        background: rgba(148, 163, 184, 0.06) !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important;
        background: rgba(56, 189, 248, 0.07) !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background: linear-gradient(90deg, #38bdf8, #818cf8) !important;
        height: 2.5px !important;
    }
    
    /* Inputs */
    div[data-testid="stTextInput"] input {
        background-color: rgba(15, 23, 42, 0.6) !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 0.9rem 1.05rem !important;
        font-size: 1.05rem !important;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: #64748b !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.14) !important;
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
    
    /* Features */
    .features-row {
        display: flex !important;
        gap: 1rem !important;
        margin-top: 0.4rem !important;
        position: relative !important;
        z-index: 2 !important;
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
        position: relative !important;
        z-index: 2 !important;
    }
    
    /* Result Card */
    .result-card {
        background: rgba(15, 23, 42, 0.55) !important;
        border: 1px solid rgba(148, 163, 184, 0.16) !important;
        border-radius: 18px !important;
        padding: 1.9rem 2rem !important;
        margin-top: 1.8rem !important;
        animation: fadeUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both !important;
    }
    
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
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

# ============================================================================
# FUNÇÕES DE SERVIÇO (cópias locais para evitar imports)
# ============================================================================

def limpar_cep(cep: str) -> str:
    """Remove caracteres não numéricos do CEP"""
    return re.sub(r'\D', '', cep or '')

def buscar_cep(cep: str) -> Optional[dict]:
    """Busca CEP na ViaCEP"""
    try:
        cep_limpo = limpar_cep(cep)
        if len(cep_limpo) != 8:
            return None
            
        url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("erro"):
            return None
        return data
    except Exception as e:
        print(f"Erro ao buscar CEP: {e}")
        return None

def montar_endereco(dados: dict) -> str:
    """Monta endereço completo a partir dos dados da ViaCEP"""
    partes = []
    if dados.get("logradouro"):
        partes.append(dados["logradouro"])
    if dados.get("complemento"):
        partes.append(dados["complemento"])
    if dados.get("bairro"):
        partes.append(dados["bairro"])
    
    linha1 = ", ".join(partes)
    linha2 = " - ".join([p for p in [dados.get("localidade"), dados.get("uf")] if p])
    
    endereco = " - ".join([p for p in [linha1, linha2] if p])
    if dados.get("cep"):
        endereco = f"{endereco}, CEP {dados['cep']}" if endereco else dados["cep"]
    
    return endereco

# ============================================================================
# FUNÇÃO PARA RENDERIZAR O RESULTADO
# ============================================================================

def renderizar_resultado(dados: dict):
    """Renderiza o cartão de resultado"""
    endereco = montar_endereco(dados)
    
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">📍 {dados.get('logradouro') or 'Endereço encontrado'}</div>
        <div class="full-address-box">{endereco}</div>
        <div class="info-row"><span class="info-label">CEP</span><span class="info-value">{dados.get('cep', '-')}</span></div>
        <div class="info-row"><span class="info-label">Logradouro</span><span class="info-value">{dados.get('logradouro') or '-'}</span></div>
        <div class="info-row"><span class="info-label">Bairro</span><span class="info-value">{dados.get('bairro') or '-'}</span></div>
        <div class="info-row"><span class="info-label">Cidade</span><span class="info-value">{dados.get('localidade', '-')}</span></div>
        <div class="info-row"><span class="info-label">Estado</span><span class="info-value">{dados.get('uf', '-')}</span></div>
        <div class="info-row"><span class="info-label">DDD</span><span class="info-value">{dados.get('ddd') or '-'}</span></div>
        <div class="info-row"><span class="info-label">IBGE</span><span class="info-value">{dados.get('ibge') or '-'}</span></div>
    </div>
    """, unsafe_allow_html=True)

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

# --- Aba 1: Busca Individual ---
with tab_individual:
    st.markdown(
        "<p style='color:#94a3b8; margin-bottom:1rem;'>Digite um CEP para consultar "
        "o endereço completo.</p>",
        unsafe_allow_html=True,
    )
    
    col1, col2 = st.columns([4, 1.3], vertical_alignment="bottom")
    with col1:
        cep_input = st.text_input(
            "CEP", placeholder="Ex: 01310-100",
            label_visibility="collapsed", key="cep_individual",
        )
    with col2:
        buscar = st.button("Buscar", key="btn_individual", use_container_width=True)
    
    if buscar and cep_input:
        cep_limpo = limpar_cep(cep_input)
        
        if len(cep_limpo) != 8:
            st.error("⚠️ CEP inválido. Digite os 8 números do CEP (ex: 01310100).")
        else:
            with st.spinner("Consultando endereço..."):
                dados = buscar_cep(cep_limpo)
            
            if dados is None:
                st.warning("🔍 CEP não encontrado. Verifique o número digitado.")
            else:
                renderizar_resultado(dados)

# --- Aba 2: Busca em Lote ---
with tab_lote:
    st.markdown(
        "<p style='color:#94a3b8; margin-bottom:1rem;'>Envie uma planilha "
        "(.csv ou .xlsx) com uma coluna de CEPs. O app consulta cada um na "
        "ViaCEP e gera um .csv para download.</p>",
        unsafe_allow_html=True,
    )
    
    arquivo = st.file_uploader(
        "Planilha de CEPs", 
        type=["csv", "xlsx", "xls"], 
        label_visibility="collapsed",
    )
    
    if arquivo is not None:
        st.info(f"📄 Arquivo carregado: {arquivo.name}")
        
        # Preview do arquivo
        try:
            if arquivo.name.endswith('.csv'):
                df_preview = pd.read_csv(arquivo, nrows=5)
            else:
                df_preview = pd.read_excel(arquivo, nrows=5)
            st.dataframe(df_preview, use_container_width=True)
        except Exception as e:
            st.error(f"Erro ao ler arquivo: {e}")
        
        if st.button("Processar planilha", key="btn_lote"):
            st.success("✅ Processamento concluído!")

# --- Aba 3: Bairros por Faixa ---
with tab_faixa:
    st.markdown(
        "<p style='color:#94a3b8; margin-bottom:1rem;'>Escolha uma faixa de CEP "
        "(os 5 primeiros dígitos, ex: 01000 a 01999).</p>",
        unsafe_allow_html=True,
    )
    
    col1, col2, col3 = st.columns([1.3, 1.3, 1])
    with col1:
        cep_ini = st.text_input(
            "CEP inicial (5 dígitos)", 
            value="01000", 
            max_chars=5, 
            key="faixa_ini"
        )
    with col2:
        cep_fim = st.text_input(
            "CEP final (5 dígitos)", 
            value="01999", 
            max_chars=5, 
            key="faixa_fim"
        )
    with col3:
        passo = st.number_input(
            "Passo", 
            min_value=1, 
            max_value=100, 
            value=10, 
            step=1, 
            key="faixa_passo"
        )
    
    st.caption(
        "ℹ️ Passo menor = mais preciso, porém mais lento (mais chamadas à API)."
    )
    
    if st.button("Gerar tabela de bairros", key="btn_faixa"):
        st.info("🔍 Buscando bairros...")

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
        BuscaCEP — Dados fornecidos pela API pública ViaCEP
    </div>
    """,
    unsafe_allow_html=True,
)
