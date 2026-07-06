"""
Componente: Busca individual de CEP, com cartão de endereço completo.
"""
import requests
import streamlit as st

from services.viacep import limpar_cep, buscar_cep
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
