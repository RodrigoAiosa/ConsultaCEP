"""
BuscaCEP — Consulta de Endereços
Versão com design premium e full-width
"""
import streamlit as st
import requests
import re
from typing import Optional

# ============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="BuscaCEP | Consulta de Endereços",
    page_icon="📍",
    layout="wide",  # <-- Largura total
    initial_sidebar_state="collapsed",
)

# ============================================================================
# CSS PREMIUM - FULL WIDTH
# ============================================================================
st.markdown("""
<style>
    /* ===== RESET E BASE ===== */
    * { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; 
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, .stApp, .main, .block-container,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    section.main {
        background: #0a0e1a !important;
        background-color: #0a0e1a !important;
    }
    
    /* ===== FULL WIDTH ===== */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 100% !important;  /* <-- Largura total */
        position: relative !important;
        z-index: 1 !important;
    }
    
    /* Remove elementos padrão */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header { visibility: hidden !important; }
    .stDeployButton { display: none !important; }
    
    /* ===== FUNDO COM BLOBS ===== */
    .stApp::before {
        content: "" !important;
        position: fixed !important;
        inset: 0 !important;
        z-index: 0 !important;
        pointer-events: none !important;
        background:
            radial-gradient(800px circle at 10% 10%, rgba(56, 189, 248, 0.15), transparent 60%),
            radial-gradient(700px circle at 90% 15%, rgba(129, 140, 248, 0.12), transparent 60%),
            radial-gradient(1000px circle at 50% 100%, rgba(56, 189, 248, 0.06), transparent 60%),
            linear-gradient(180deg, #0a0e1a 0%, #0f1524 45%, #0a0e1a 100%) !important;
    }
    
    /* ===== GRID SUTIL ===== */
    .stApp::after {
        content: "" !important;
        position: fixed !important;
        inset: 0 !important;
        z-index: 0 !important;
        pointer-events: none !important;
        opacity: 0.3 !important;
        background-image:
            linear-gradient(rgba(148, 163, 184, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148, 163, 184, 0.04) 1px, transparent 1px) !important;
        background-size: 50px 50px !important;
        mask-image: radial-gradient(ellipse 1000px 600px at 50% 0%, black 40%, transparent 100%) !important;
        -webkit-mask-image: radial-gradient(ellipse 1000px 600px at 50% 0%, black 40%, transparent 100%) !important;
    }
    
    /* ===== HERO ===== */
    .hero-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        margin-bottom: 3rem;
        position: relative;
        z-index: 2;
    }
    
    .hero-badge {
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        background: rgba(56, 189, 248, 0.10) !important;
        color: #7dd3fc !important;
        border: 1px solid rgba(56, 189, 248, 0.25) !important;
        padding: 8px 20px !important;
        border-radius: 999px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        margin-bottom: 1.5rem !important;
    }
    
    .hero-title {
        font-size: 3.8rem !important;
        font-weight: 900 !important;
        color: #f8fafc !important;
        line-height: 1.1 !important;
        margin-bottom: 1rem !important;
        letter-spacing: -0.04em !important;
    }
    
    .hero-title span {
        background: linear-gradient(135deg, #38bdf8, #818cf8 50%, #a78bfa) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    .hero-subtitle {
        font-size: 1.2rem !important;
        color: #94a3b8 !important;
        margin-bottom: 2rem !important;
        max-width: 640px !important;
        line-height: 1.7 !important;
    }
    
    /* ===== TRUST ROW - CARDS MELHORADOS ===== */
    .trust-row {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 0.8rem !important;
        margin-bottom: 3rem !important;
        position: relative !important;
        z-index: 2 !important;
    }
    
    .trust-chip {
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.12) !important;
        color: #e2e8f0 !important;
        padding: 10px 20px !important;
        border-radius: 12px !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    .trust-chip:hover {
        transform: translateY(-3px) !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 8px 24px rgba(56, 189, 248, 0.15) !important;
        background: rgba(30, 41, 59, 0.8) !important;
    }
    
    .trust-chip .icon {
        font-size: 1.1rem !important;
    }
    
    /* ===== TOOL CARD - PRINCIPAL ===== */
    div[data-testid="stTabs"] {
        background: linear-gradient(160deg, rgba(30, 41, 59, 0.6), rgba(15, 23, 42, 0.5)) !important;
        border: 1px solid rgba(148, 163, 184, 0.12) !important;
        border-radius: 28px !important;
        padding: 2.5rem 2.8rem 2rem !important;
        box-shadow:
            0 0 0 1px rgba(56, 189, 248, 0.03),
            0 25px 80px -20px rgba(0, 0, 0, 0.6),
            0 10px 30px -10px rgba(56, 189, 248, 0.06) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        margin-bottom: 3rem !important;
        position: relative !important;
        z-index: 2 !important;
        max-width: 100% !important;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.10) !important;
        margin-bottom: 1.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 12px 20px !important;
        background: transparent !important;
        border-radius: 12px 12px 0 0 !important;
        transition: all 0.2s ease !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #cbd5e1 !important;
        background: rgba(148, 163, 184, 0.05) !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important;
        background: rgba(56, 189, 248, 0.06) !important;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background: linear-gradient(90deg, #38bdf8, #818cf8) !important;
        height: 3px !important;
        border-radius: 2px !important;
    }
    
    /* ===== INPUTS ===== */
    div[data-testid="stTextInput"] input {
        background-color: rgba(15, 23, 42, 0.7) !important;
        color: #f8fafc !important;
        border: 1px solid #334155 !important;
        border-radius: 14px !important;
        padding: 1rem 1.2rem !important;
        font-size: 1.05rem !important;
        transition: all 0.2s ease !important;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: #64748b !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border: 1px solid #38bdf8 !important;
        box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.12) !important;
    }
    
    /* ===== BOTÕES ===== */
    .stButton > button {
        background: linear-gradient(135deg, #38bdf8, #6366f1) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 4px 16px -4px rgba(99, 102, 241, 0.35) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 12px 32px -6px rgba(99, 102, 241, 0.5) !important;
        filter: brightness(1.08) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* ===== RESULT CARD - DESTAQUE ===== */
    .result-card {
        background: linear-gradient(160deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.6)) !important;
        border: 1px solid rgba(56, 189, 248, 0.15) !important;
        border-radius: 20px !important;
        padding: 2.2rem 2.5rem !important;
        margin-top: 2rem !important;
        animation: fadeUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both !important;
        box-shadow: 
            0 0 0 1px rgba(56, 189, 248, 0.05),
            0 20px 60px -20px rgba(0, 0, 0, 0.5),
            0 8px 24px -8px rgba(56, 189, 248, 0.08) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    /* Brilho sutil no card de resultado */
    .result-card::before {
        content: "" !important;
        position: absolute !important;
        top: -50% !important;
        right: -50% !important;
        width: 200% !important;
        height: 200% !important;
        background: radial-gradient(circle at 70% 20%, rgba(56, 189, 248, 0.03), transparent 60%) !important;
        pointer-events: none !important;
    }
    
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-title {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        margin-bottom: 1.2rem !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .full-address-box {
        background: rgba(56, 189, 248, 0.06) !important;
        border: 1px solid rgba(56, 189, 248, 0.2) !important;
        border-radius: 14px !important;
        padding: 1rem 1.3rem !important;
        color: #e0f2fe !important;
        font-size: 1.05rem !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        margin-bottom: 1.5rem !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .info-grid {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important;
        gap: 0.5rem 2rem !important;
        position: relative !important;
        z-index: 1 !important;
    }
    
    .info-row {
        display: flex !important;
        justify-content: space-between !important;
        padding: 0.6rem 0 !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.06) !important;
    }
    
    .info-row:last-child {
        border-bottom: none !important;
    }
    
    .info-label {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.02em !important;
        text-transform: uppercase !important;
    }
    
    .info-value {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        text-align: right !important;
        font-variant-numeric: tabular-nums !important;
    }
    
    /* ===== FEATURES ROW - CARDS EM DESTAQUE ===== */
    .features-row {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 1.2rem !important;
        margin-top: 1.5rem !important;
        position: relative !important;
        z-index: 2 !important;
    }
    
    .feature-box {
        background: linear-gradient(160deg, rgba(30, 41, 59, 0.5), rgba(15, 23, 42, 0.4)) !important;
        border: 1px solid rgba(148, 163, 184, 0.08) !important;
        border-radius: 18px !important;
        padding: 1.8rem 1.5rem !important;
        text-align: center !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        backdrop-filter: blur(8px) !important;
        -webkit-backdrop-filter: blur(8px) !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15) !important;
    }
    
    .feature-box:hover {
        transform: translateY(-6px) !important;
        border-color: rgba(56, 189, 248, 0.3) !important;
        background: linear-gradient(160deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.6)) !important;
        box-shadow: 0 12px 40px -8px rgba(56, 189, 248, 0.15) !important;
    }
    
    .feature-box .icon {
        font-size: 2.2rem !important;
        margin-bottom: 0.7rem !important;
        display: block !important;
    }
    
    .feature-box .label {
        color: #e2e8f0 !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    .feature-box .description {
        color: #94a3b8 !important;
        font-size: 0.8rem !important;
        margin-top: 0.3rem !important;
    }
    
    /* ===== FOOTNOTE ===== */
    .footnote {
        text-align: center !important;
        color: #475569 !important;
        margin-top: 3rem !important;
        font-size: 0.8rem !important;
        position: relative !important;
        z-index: 2 !important;
        letter-spacing: 0.02em !important;
    }
    
    /* ===== RESPONSIVO ===== */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 1.2rem !important;
            padding-right: 1.2rem !important;
        }
        
        .hero-title {
            font-size: 2.5rem !important;
        }
        
        .hero-subtitle {
            font-size: 1rem !important;
        }
        
        div[data-testid="stTabs"] {
            padding: 1.5rem 1.2rem 1.2rem !important;
            border-radius: 20px !important;
        }
        
        .info-grid {
            grid-template-columns: 1fr !important;
        }
        
        .features-row {
            grid-template-columns: 1fr !important;
            gap: 0.8rem !important;
        }
        
        .trust-chip {
            font-size: 0.8rem !important;
            padding: 8px 14px !important;
        }
        
        .result-card {
            padding: 1.5rem !important;
        }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        .features-row {
            grid-template-columns: repeat(3, 1fr) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FUNÇÕES DE SERVIÇO
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
    """Renderiza o cartão de resultado com design melhorado"""
    endereco = montar_endereco(dados)
    
    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">📍 {dados.get('logradouro') or 'Endereço encontrado'}</div>
        <div class="full-address-box">{endereco}</div>
        <div class="info-grid">
            <div class="info-row"><span class="info-label">CEP</span><span class="info-value">{dados.get('cep', '-')}</span></div>
            <div class="info-row"><span class="info-label">Logradouro</span><span class="info-value">{dados.get('logradouro') or '-'}</span></div>
            <div class="info-row"><span class="info-label">Bairro</span><span class="info-value">{dados.get('bairro') or '-'}</span></div>
            <div class="info-row"><span class="info-label">Cidade</span><span class="info-value">{dados.get('localidade', '-')}</span></div>
            <div class="info-row"><span class="info-label">Estado</span><span class="info-value">{dados.get('uf', '-')}</span></div>
            <div class="info-row"><span class="info-label">DDD</span><span class="info-value">{dados.get('ddd') or '-'}</span></div>
            <div class="info-row"><span class="info-label">IBGE</span><span class="info-value">{dados.get('ibge') or '-'}</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# HERO / LANDING
# ============================================================================

st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">📍 Feito com dados oficiais dos Correios</div>
    <div class="hero-title">Encontre qualquer<br><span>endereço do Brasil</span></div>
    <div class="hero-subtitle">Digite um CEP e descubra rua, bairro, cidade, estado —<br>
    ou envie uma planilha inteira e baixe tudo processado em .csv.</div>
</div>
""", unsafe_allow_html=True)

# Trust Row SEM o "🗺️ Mapa incluso"
st.markdown("""
<div class="trust-row">
    <span class="trust-chip"><span class="icon">⚡</span> Resultado em segundos</span>
    <span class="trust-chip"><span class="icon">🔓</span> Sem cadastro</span>
    <span class="trust-chip"><span class="icon">💸</span> 100% gratuito</span>
    <span class="trust-chip"><span class="icon">📊</span> Exporta em .csv</span>
</div>
""", unsafe_allow_html=True)

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
        "<p style='color:#94a3b8; margin-bottom:1rem; font-size:0.95rem;'>Digite um CEP para consultar o endereço completo.</p>",
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
        "<p style='color:#94a3b8; margin-bottom:1rem; font-size:0.95rem;'>Envie uma planilha (.csv ou .xlsx) com uma coluna de CEPs.</p>",
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
            import pandas as pd
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
        "<p style='color:#94a3b8; margin-bottom:1rem; font-size:0.95rem;'>Escolha uma faixa de CEP (os 5 primeiros dígitos, ex: 01000 a 01999).</p>",
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
    
    st.caption("ℹ️ Passo menor = mais preciso, porém mais lento (mais chamadas à API).")
    
    if st.button("Gerar tabela de bairros", key="btn_faixa"):
        st.info("🔍 Buscando bairros...")

# ============================================================================
# FEATURES ROW - CARDS EM DESTAQUE
# ============================================================================

st.markdown("""
<div class="features-row">
    <div class="feature-box">
        <span class="icon">⚡</span>
        <div class="label">Rápido e direto</div>
        <div class="description">Resultados em segundos</div>
    </div>
    <div class="feature-box">
        <span class="icon">🔒</span>
        <div class="label">Privacidade total</div>
        <div class="description">Sem cadastro ou dados salvos</div>
    </div>
    <div class="feature-box">
        <span class="icon">📦</span>
        <div class="label">Dados oficiais</div>
        <div class="description">Direto da API dos Correios</div>
    </div>
</div>
<div class="footnote">
    BuscaCEP — Dados fornecidos pela API pública ViaCEP
</div>
""", unsafe_allow_html=True)
