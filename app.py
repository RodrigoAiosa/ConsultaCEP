import streamlit as st
import requests
import pydeck as pdk
import pandas as pd
import time
import io

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

    .full-address-box {
        background: rgba(56, 189, 248, 0.08);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 12px;
        padding: 0.9rem 1.1rem;
        color: #e0f2fe;
        font-size: 1rem;
        font-weight: 500;
        line-height: 1.5;
        margin-bottom: 1.3rem;
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
def _geocode_query(query: str):
    """Chama o Nominatim (OpenStreetMap, gratuito) para uma única query."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": query, "format": "json", "limit": 1, "countrycodes": "br"}
    headers = {"User-Agent": "BuscaCEP-Streamlit-App/1.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=8)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        return None
    return float(results[0]["lat"]), float(results[0]["lon"])


def geocodificar_com_fallback(dados: dict):
    """
    Tenta geocodificar do nível mais preciso (rua) até o mais genérico (cidade),
    garantindo que o mapa sempre tenha uma localização para mostrar.
    Retorna (lat, lon, nivel_precisao).
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


# ----------------------------------------------------------------------------
# BUSCA INDIVIDUAL
# ----------------------------------------------------------------------------
def _busca_individual():
    col1, col2 = st.columns([4, 1.3], vertical_alignment="bottom")
    with col1:
        cep_input = st.text_input(
            "CEP",
            placeholder="Ex: 01310-100",
            label_visibility="collapsed",
            key="cep_individual",
        )
    with col2:
        buscar = st.button("Buscar", key="btn_individual")

    if not (buscar or cep_input):
        return

    cep_limpo = limpar_cep(cep_input)

    if len(cep_limpo) != 8:
        if buscar:
            st.error("⚠️ CEP inválido. Digite os 8 números do CEP (ex: 01310100).")
        return

    with st.spinner("Consultando endereço..."):
        try:
            dados = buscar_cep(cep_limpo)
        except requests.RequestException:
            dados = "erro_conexao"

    if dados == "erro_conexao":
        st.error("❌ Não foi possível conectar à API ViaCEP. Tente novamente.")
        return
    elif dados is None:
        st.warning("🔍 CEP não encontrado. Verifique o número digitado.")
        return

    partes_endereco = [
        dados.get("logradouro"),
        dados.get("complemento"),
        dados.get("bairro"),
    ]
    linha1 = ", ".join([p for p in partes_endereco if p])

    partes_local = [dados.get("localidade"), dados.get("uf")]
    linha2 = " - ".join([p for p in partes_local if p])

    endereco_completo = " - ".join([p for p in [linha1, linha2] if p])
    if dados.get("cep"):
        endereco_completo = f"{endereco_completo}, CEP {dados.get('cep')}" if endereco_completo else dados.get("cep")

    st.markdown(f"""
    <div class="result-card">
        <div class="result-title">📍 {dados.get('logradouro') or 'Endereço encontrado'}</div>
        <div class="full-address-box">{endereco_completo}</div>
        <div class="info-row"><span class="info-label">CEP</span><span class="info-value">{dados.get('cep', '-')}</span></div>
        <div class="info-row"><span class="info-label">Logradouro</span><span class="info-value">{dados.get('logradouro') or '-'}</span></div>
        <div class="info-row"><span class="info-label">Bairro</span><span class="info-value">{dados.get('bairro') or '-'}</span></div>
        <div class="info-row"><span class="info-label">Cidade</span><span class="info-value">{dados.get('localidade', '-')}</span></div>
        <div class="info-row"><span class="info-label">Estado</span><span class="info-value">{dados.get('uf', '-')}</span></div>
        <div class="info-row"><span class="info-label">Região (DDD)</span><span class="info-value">{dados.get('ddd') or '-'}</span></div>
        <div class="info-row"><span class="info-label">IBGE</span><span class="info-value">{dados.get('ibge') or '-'}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Geocodificação com fallback (rua -> bairro -> cidade -> estado)
    # para o mapa SEMPRE mostrar o endereço, mesmo que de forma aproximada.
    with st.spinner("Localizando no mapa..."):
        resultado_geo = geocodificar_com_fallback(dados)

    endereco_label = ", ".join(filter(None, [
        dados.get("logradouro"), dados.get("bairro"),
        dados.get("localidade"), dados.get("uf"),
    ])) or dados.get("cep", "")

    if resultado_geo:
        lat, lon, nivel = resultado_geo

        zoom_por_nivel = {"rua": 16, "bairro": 14, "cidade": 11, "estado": 6}
        zoom = zoom_por_nivel.get(nivel, 14)

        ponto = [{
            "lat": lat,
            "lon": lon,
            "endereco": endereco_label,
        }]

        st.markdown("<br>", unsafe_allow_html=True)
        st.pydeck_chart(pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v10",
            initial_view_state=pdk.ViewState(
                latitude=lat, longitude=lon, zoom=zoom, pitch=40,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=ponto,
                    get_position="[lon, lat]",
                    get_color="[56, 189, 248, 220]",
                    get_radius=60,
                    radius_min_pixels=8,
                    radius_max_pixels=20,
                    pickable=True,
                ),
                pdk.Layer(
                    "TextLayer",
                    data=ponto,
                    get_position="[lon, lat]",
                    get_text="endereco",
                    get_size=14,
                    get_color="[248, 250, 252, 255]",
                    get_pixel_offset="[0, -22]",
                    get_alignment_baseline="'bottom'",
                    billboard=True,
                ),
            ],
            tooltip={
                "html": "<b>📍 {endereco}</b>",
                "style": {
                    "backgroundColor": "#1e293b",
                    "color": "#f8fafc",
                    "fontSize": "0.85rem",
                    "padding": "6px 10px",
                    "borderRadius": "8px",
                },
            },
        ))

        if nivel != "rua":
            aviso = {
                "bairro": "Localização aproximada pelo bairro (rua não localizada no mapa).",
                "cidade": "Localização aproximada pela cidade (endereço exato não encontrado no mapa).",
                "estado": "Localização aproximada pelo estado (endereço não encontrado no mapa).",
            }.get(nivel, "Localização aproximada.")
            st.caption(f"ℹ️ {aviso}")
    else:
        st.warning("⚠️ Não foi possível localizar este endereço no mapa no momento.")


# ----------------------------------------------------------------------------
# BUSCA EM LOTE (PLANILHA)
# ----------------------------------------------------------------------------
def _ler_planilha_de_ceps(arquivo) -> list:
    """Lê .csv ou .xlsx e retorna lista de CEPs (procura coluna que pareça CEP,
    senão usa a primeira coluna)."""
    nome = arquivo.name.lower()
    if nome.endswith(".csv"):
        try:
            df = pd.read_csv(arquivo, sep=None, engine="python", dtype=str)
        except Exception:
            arquivo.seek(0)
            df = pd.read_csv(arquivo, dtype=str)
    else:
        try:
            df = pd.read_excel(arquivo, dtype=str)
        except ImportError:
            raise RuntimeError(
                "Para ler arquivos .xlsx é necessário instalar a biblioteca "
                "'openpyxl'. Rode: pip install openpyxl (ou pip install -r "
                "requirements.txt) e reinicie o app. Como alternativa, você "
                "pode salvar a planilha como .csv."
            )

    coluna_cep = None
    for col in df.columns:
        if "cep" in str(col).strip().lower():
            coluna_cep = col
            break
    if coluna_cep is None:
        coluna_cep = df.columns[0]

    ceps = df[coluna_cep].dropna().astype(str).tolist()
    return ceps


def _busca_em_lote():
    st.markdown(
        "<p style='color:#94a3b8; margin-bottom:1rem;'>Envie uma planilha "
        "(.csv ou .xlsx) com uma coluna de CEPs. O app consulta cada um na "
        "ViaCEP e gera um .csv para download com Bairro, Cidade, Estado, DDD e IBGE.</p>",
        unsafe_allow_html=True,
    )

    arquivo = st.file_uploader("Planilha de CEPs", type=["csv", "xlsx", "xls"], label_visibility="collapsed")

    if arquivo is None:
        return

    try:
        ceps = _ler_planilha_de_ceps(arquivo)
    except Exception as e:
        st.error(f"❌ Não foi possível ler a planilha: {e}")
        return

    if not ceps:
        st.warning("🔍 Nenhum CEP encontrado na planilha.")
        return

    st.info(f"📄 {len(ceps)} CEP(s) encontrados na planilha.")

    if st.button("Processar planilha", key="btn_lote"):
        linhas = []
        barra = st.progress(0.0, text="Iniciando...")
        total = len(ceps)

        for i, cep_bruto in enumerate(ceps):
            cep_limpo = limpar_cep(str(cep_bruto))

            if len(cep_limpo) != 8:
                linhas.append({
                    "CEP": cep_bruto, "Bairro": "", "Cidade": "",
                    "Estado": "", "DDD": "", "IBGE": "",
                })
            else:
                try:
                    dados = buscar_cep(cep_limpo)
                except requests.RequestException:
                    dados = None

                if dados:
                    linhas.append({
                        "CEP": dados.get("cep", cep_limpo),
                        "Bairro": dados.get("bairro", "") or "",
                        "Cidade": dados.get("localidade", "") or "",
                        "Estado": dados.get("uf", "") or "",
                        "DDD": dados.get("ddd", "") or "",
                        "IBGE": dados.get("ibge", "") or "",
                    })
                else:
                    linhas.append({
                        "CEP": cep_limpo, "Bairro": "", "Cidade": "",
                        "Estado": "", "DDD": "", "IBGE": "",
                    })

            barra.progress((i + 1) / total, text=f"Consultando {i + 1}/{total}...")
            time.sleep(0.05)  # evita sobrecarregar a API pública

        barra.empty()

        df_resultado = pd.DataFrame(linhas, columns=["CEP", "Bairro", "Cidade", "Estado", "DDD", "IBGE"])

        st.success(f"✅ Processamento concluído! {len(df_resultado)} CEP(s) processados.")
        st.dataframe(df_resultado, use_container_width=True)

        csv_buffer = io.StringIO()
        df_resultado.to_csv(csv_buffer, index=False, sep=";", encoding="utf-8-sig")

        st.download_button(
            label="⬇️ Baixar resultado (.csv)",
            data=csv_buffer.getvalue(),
            file_name="ceps_processados.csv",
            mime="text/csv",
        )


# ----------------------------------------------------------------------------
# BAIRROS POR FAIXA DE CEP (gerado ao vivo via ViaCEP, para qualquer cidade/UF)
# ----------------------------------------------------------------------------
def _formatar_cep(base5: int) -> str:
    return f"{base5:05d}000"


def _bairros_por_faixa():
    st.markdown(
        "<p style='color:#94a3b8; margin-bottom:1rem;'>Escolha uma faixa de CEP "
        "(os 5 primeiros dígitos, ex: 01000 a 05999 cobre boa parte da capital "
        "paulista) e o app consulta a ViaCEP ao longo da faixa, agrupando os "
        "bairros encontrados. É gerado na hora, direto da fonte oficial.</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1.3, 1.3, 1])
    with col1:
        cep_ini_str = st.text_input("CEP inicial (5 dígitos)", value="01000", max_chars=5, key="faixa_ini")
    with col2:
        cep_fim_str = st.text_input("CEP final (5 dígitos)", value="01999", max_chars=5, key="faixa_fim")
    with col3:
        passo = st.number_input("Passo (amostragem)", min_value=1, max_value=200, value=10, step=1, key="faixa_passo")

    st.caption(
        "ℹ️ Passo menor = mais preciso, porém mais lento (mais chamadas à API pública). "
        "O resultado é uma aproximação por amostragem, não uma tabela oficial exaustiva."
    )

    if not st.button("Gerar tabela de bairros", key="btn_faixa"):
        return

    if not (cep_ini_str.isdigit() and cep_fim_str.isdigit()):
        st.error("⚠️ Informe apenas números nos campos de CEP inicial/final.")
        return

    cep_ini, cep_fim = int(cep_ini_str), int(cep_fim_str)
    if cep_ini > cep_fim:
        st.error("⚠️ O CEP inicial deve ser menor ou igual ao CEP final.")
        return

    MAX_CONSULTAS = 500
    total_estimado = (cep_fim - cep_ini) // passo + 1
    if total_estimado > MAX_CONSULTAS:
        passo = max(1, (cep_fim - cep_ini) // MAX_CONSULTAS)
        st.info(f"ℹ️ Faixa muito ampla — ajustando passo automaticamente para {passo} (limite de {MAX_CONSULTAS} consultas por vez).")

    pontos = list(range(cep_ini, cep_fim + 1, passo))
    resultados = []
    barra = st.progress(0.0, text="Iniciando...")

    for i, base in enumerate(pontos):
        cep = _formatar_cep(base)
        try:
            dados = buscar_cep(cep)
        except requests.RequestException:
            dados = None

        if dados and dados.get("bairro"):
            resultados.append({
                "cep_num": int(dados.get("cep", cep).replace("-", "")),
                "cep": dados.get("cep", cep),
                "bairro": dados.get("bairro"),
                "cidade": dados.get("localidade", ""),
                "uf": dados.get("uf", ""),
            })

        barra.progress((i + 1) / len(pontos), text=f"Consultando {i + 1}/{len(pontos)}...")
        time.sleep(0.05)

    barra.empty()

    if not resultados:
        st.warning("🔍 Nenhum bairro encontrado nessa faixa. Tente outra faixa de CEP.")
        return

    df = pd.DataFrame(resultados).sort_values("cep_num")

    # Agrupa por bairro, pegando o menor e maior CEP observado dentro da amostragem
    agrupado = (
        df.groupby(["bairro", "cidade", "uf"])
        .agg(cep_inicial=("cep", "first"), cep_final=("cep", "last"))
        .reset_index()
        .sort_values("cep_inicial")
    )
    agrupado.columns = ["Bairro", "Cidade", "Estado", "CEP Inicial", "CEP Final"]

    st.success(f"✅ {len(agrupado)} bairro(s) encontrado(s) na faixa {cep_ini_str}-000 a {cep_fim_str}-999.")
    st.dataframe(agrupado, use_container_width=True, hide_index=True)

    csv_buffer = io.StringIO()
    agrupado.to_csv(csv_buffer, index=False, sep=";", encoding="utf-8-sig")
    st.download_button(
        label="⬇️ Baixar tabela (.csv)",
        data=csv_buffer.getvalue(),
        file_name="bairros_por_faixa_cep.csv",
        mime="text/csv",
    )



st.markdown('<div class="hero-badge">🇧🇷 API pública · ViaCEP</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-title">Encontre qualquer<br><span>endereço do Brasil</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-subtitle">Digite um CEP e descubra rua, bairro, cidade, estado — '
    'ou envie uma planilha inteira e baixe tudo processado em .csv.</div>',
    unsafe_allow_html=True,
)

tab_individual, tab_lote, tab_faixa = st.tabs([
    "🔍 Busca individual", "📂 Busca em lote (planilha)", "🏘️ Bairros por faixa de CEP",
])

with tab_individual:
    _busca_individual()

with tab_lote:
    _busca_em_lote()

with tab_faixa:
    _bairros_por_faixa()

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
