import streamlit as st
import requests
import pydeck as pdk

# ----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="BuscaCEP | Consulta de Endereços",
    page_icon="📍",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ----------------------------------------------------------------------------
# CSS CUSTOMIZADO (estilo landing page)
# ----------------------------------------------------------------------------
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background: linear-gradient(160deg, #0f172a 0%, #1e293b 45%, #0f172a 100%);
    }

    .block-container {
        padding-top: 3rem;
        max-width: 780px;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #f8fafc;
        line-height: 1.15;
        margin-bottom: 0.6rem;
        letter-spacing: -0.02em;
    }

    .hero-title span {
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 2.2rem;
        max-width: 520px;
    }

    div[data-testid="stTextInput"] input {
        background-color: #1e293b;
        color: #f8fafc;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        font-size: 1.05rem;
    }

    div[data-testid="stTextInput"] input:focus {
        border: 1px solid #38bdf8;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
    }

    .stButton > button {
        background: linear-gradient(90deg, #38bdf8, #6366f1);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.6rem;
        font-weight: 700;
        font-size: 1rem;
        width: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(99, 102, 241, 0.35);
    }

    .result-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid #334155;
        border-radius: 18px;
        padding: 1.8rem 2rem;
        margin-top: 2rem;
    }

    .result-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 0.55rem 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.15);
    }

    .info-row:last-child {
        border-bottom: none;
    }

    .info-label {
        color: #94a3b8;
        font-size: 0.92rem;
    }

    .info-value {
        color: #f1f5f9;
        font-weight: 600;
        font-size: 0.95rem;
        text-align: right;
    }

    .features-row {
        display: flex;
        gap: 1rem;
        margin-top: 2.5rem;
    }

    .feature-box {
        flex: 1;
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
    }

    .feature-box .icon {
        font-size: 1.5rem;
        margin-bottom: 0.4rem;
    }

    .feature-box .label {
        color: #cbd5e1;
        font-size: 0.85rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ----------------------------------------------------------------------------
def limpar_cep(cep: str) -> str:
    return "".join(filter(str.isdigit, cep))


@st.cache_data(show_spinner=False, ttl=3600)
def buscar_cep(cep: str):
    """Consulta a API pública ViaCEP (gratuita, sem chave)."""
    url = f"https://viacep.com.br/ws/{cep}/json/"
    resp = requests.get(url, timeout=8)
    resp.raise_for_status()
    data = resp.json()
    if data.get("erro"):
        return None
    return data


@st.cache_data(show_spinner=False, ttl=3600)
def geocodificar_endereco(endereco: str):
    """Converte endereço em latitude/longitude via Nominatim (OpenStreetMap, gratuito)."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": endereco, "format": "json", "limit": 1, "countrycodes": "br"}
    headers = {"User-Agent": "BuscaCEP-Streamlit-App/1.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=8)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        return None
    return float(results[0]["lat"]), float(results[0]["lon"])


# ----------------------------------------------------------------------------
# HERO / LANDING
# ----------------------------------------------------------------------------
st.markdown('<div class="hero-badge">🇧🇷 API pública · ViaCEP</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-title">Encontre qualquer<br><span>endereço do Brasil</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-subtitle">Digite um CEP e descubra rua, bairro, cidade, estado — '
    'e veja a localização exata no mapa em segundos.</div>',
    unsafe_allow_html=True,
)

col1, col2 = st.columns([4, 1.3], vertical_alignment="bottom")
with col1:
    cep_input = st.text_input(
        "CEP",
        placeholder="Ex: 01310-100",
        label_visibility="collapsed",
    )
with col2:
    buscar = st.button("Buscar")

# ----------------------------------------------------------------------------
# BUSCA E RESULTADO
# ----------------------------------------------------------------------------
if buscar or cep_input:
    cep_limpo = limpar_cep(cep_input)

    if len(cep_limpo) != 8:
        if buscar:
            st.error("⚠️ CEP inválido. Digite os 8 números do CEP (ex: 01310100).")
    else:
        with st.spinner("Consultando endereço..."):
            try:
                dados = buscar_cep(cep_limpo)
            except requests.RequestException:
                dados = "erro_conexao"

        if dados == "erro_conexao":
            st.error("❌ Não foi possível conectar à API ViaCEP. Tente novamente.")
        elif dados is None:
            st.warning("🔍 CEP não encontrado. Verifique o número digitado.")
        else:
            st.markdown(f"""
            <div class="result-card">
                <div class="result-title">📍 {dados.get('logradouro') or 'Endereço encontrado'}</div>
                <div class="info-row"><span class="info-label">CEP</span><span class="info-value">{dados.get('cep', '-')}</span></div>
                <div class="info-row"><span class="info-label">Bairro</span><span class="info-value">{dados.get('bairro') or '-'}</span></div>
                <div class="info-row"><span class="info-label">Cidade</span><span class="info-value">{dados.get('localidade', '-')}</span></div>
                <div class="info-row"><span class="info-label">Estado</span><span class="info-value">{dados.get('uf', '-')}</span></div>
                <div class="info-row"><span class="info-label">Região (DDD)</span><span class="info-value">{dados.get('ddd') or '-'}</span></div>
                <div class="info-row"><span class="info-label">IBGE</span><span class="info-value">{dados.get('ibge') or '-'}</span></div>
            </div>
            """, unsafe_allow_html=True)

            # Geocodificação para exibir no mapa
            partes = [dados.get("logradouro"), dados.get("bairro"), dados.get("localidade"), dados.get("uf"), "Brasil"]
            endereco_completo = ", ".join([p for p in partes if p])

            with st.spinner("Localizando no mapa..."):
                try:
                    coords = geocodificar_endereco(endereco_completo)
                except requests.RequestException:
                    coords = None

            if coords:
                lat, lon = coords
                st.markdown("<br>", unsafe_allow_html=True)
                st.pydeck_chart(pdk.Deck(
                    map_style="mapbox://styles/mapbox/dark-v10",
                    initial_view_state=pdk.ViewState(
                        latitude=lat, longitude=lon, zoom=15, pitch=40,
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=[{"lat": lat, "lon": lon}],
                            get_position="[lon, lat]",
                            get_color="[56, 189, 248, 200]",
                            get_radius=60,
                            pickable=True,
                        ),
                    ],
                ))
            else:
                st.info("ℹ️ Endereço encontrado, mas não foi possível localizá-lo no mapa.")

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
    "<p style='text-align:center; color:#475569; margin-top:2.5rem; font-size:0.8rem;'>"
    "Dados via ViaCEP e OpenStreetMap Nominatim · Sem necessidade de chave de API"
    "</p>",
    unsafe_allow_html=True,
)
