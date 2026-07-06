"""
Componente: Busca individual de CEP, com cartão de endereço e mapa interativo.
"""
import requests
import streamlit as st
import pydeck as pdk

from config import ZOOM_POR_NIVEL_PRECISAO, AVISOS_PRECISAO
from services.viacep import limpar_cep, buscar_cep
from services.geocoding import geocodificar_com_fallback
from utils.address import montar_endereco_completo


def _renderizar_cartao_endereco(dados: dict) -> None:
    endereco_completo = montar_endereco_completo(dados)

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


def _renderizar_mapa(dados: dict) -> None:
    with st.spinner("Localizando no mapa..."):
        resultado_geo = geocodificar_com_fallback(dados)

    endereco_label = ", ".join(filter(None, [
        dados.get("logradouro"), dados.get("bairro"),
        dados.get("localidade"), dados.get("uf"),
    ])) or dados.get("cep", "")

    if not resultado_geo:
        st.warning("⚠️ Não foi possível localizar este endereço no mapa no momento.")
        return

    lat, lon, nivel = resultado_geo
    zoom = ZOOM_POR_NIVEL_PRECISAO.get(nivel, 14)
    ponto = [{"lat": lat, "lon": lon, "endereco": endereco_label}]

    st.markdown("<br>", unsafe_allow_html=True)
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/dark-v10",
        initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom, pitch=40),
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
        st.caption(f"ℹ️ {AVISOS_PRECISAO.get(nivel, 'Localização aproximada.')}")


def render() -> None:
    """Renderiza a aba de busca individual de CEP."""
    col1, col2 = st.columns([4, 1.3], vertical_alignment="bottom")
    with col1:
        cep_input = st.text_input(
            "CEP", placeholder="Ex: 01310-100",
            label_visibility="collapsed", key="cep_individual",
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
    if dados is None:
        st.warning("🔍 CEP não encontrado. Verifique o número digitado.")
        return

    _renderizar_cartao_endereco(dados)
    _renderizar_mapa(dados)
