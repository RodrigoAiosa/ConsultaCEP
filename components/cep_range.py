"""
Componente: Gera, ao vivo, uma tabela de bairros por faixa de CEP,
consultando a ViaCEP por amostragem ao longo da faixa informada.
"""
import io
import time

import pandas as pd
import requests
import streamlit as st

from config import (
    FAIXA_MAX_CONSULTAS,
    FAIXA_SLEEP_BETWEEN_REQUESTS,
    FAIXA_CEP_INICIAL_PADRAO,
    FAIXA_CEP_FINAL_PADRAO,
    FAIXA_PASSO_PADRAO,
)
from services.viacep import buscar_cep
from utils.address import formatar_cep_prefixo


def _consultar_faixa(cep_ini: int, cep_fim: int, passo: int) -> pd.DataFrame:
    pontos = list(range(cep_ini, cep_fim + 1, passo))
    resultados = []
    barra = st.progress(0.0, text="Iniciando...")

    for i, base in enumerate(pontos):
        cep = formatar_cep_prefixo(base)
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
        time.sleep(FAIXA_SLEEP_BETWEEN_REQUESTS)

    barra.empty()
    return pd.DataFrame(resultados)


def _agrupar_por_bairro(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values("cep_num")
    agrupado = (
        df.groupby(["bairro", "cidade", "uf"])
        .agg(cep_inicial=("cep", "first"), cep_final=("cep", "last"))
        .reset_index()
        .sort_values("cep_inicial")
    )
    agrupado.columns = ["Bairro", "Cidade", "Estado", "CEP Inicial", "CEP Final"]
    return agrupado


def render() -> None:
    """Renderiza a aba de bairros por faixa de CEP."""
    st.markdown(
        "<p style='color:#94a3b8; margin-bottom:1rem;'>Escolha uma faixa de CEP "
        "(os 5 primeiros dígitos, ex: 01000 a 05999 cobre boa parte da capital "
        "paulista) e o app consulta a ViaCEP ao longo da faixa, agrupando os "
        "bairros encontrados. É gerado na hora, direto da fonte oficial.</p>",
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1.3, 1.3, 1])
    with col1:
        cep_ini_str = st.text_input(
            "CEP inicial (5 dígitos)", value=FAIXA_CEP_INICIAL_PADRAO, max_chars=5, key="faixa_ini",
        )
    with col2:
        cep_fim_str = st.text_input(
            "CEP final (5 dígitos)", value=FAIXA_CEP_FINAL_PADRAO, max_chars=5, key="faixa_fim",
        )
    with col3:
        passo = st.number_input(
            "Passo (amostragem)", min_value=1, max_value=200,
            value=FAIXA_PASSO_PADRAO, step=1, key="faixa_passo",
        )

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

    total_estimado = (cep_fim - cep_ini) // passo + 1
    if total_estimado > FAIXA_MAX_CONSULTAS:
        passo = max(1, (cep_fim - cep_ini) // FAIXA_MAX_CONSULTAS)
        st.info(
            f"ℹ️ Faixa muito ampla — ajustando passo automaticamente para {passo} "
            f"(limite de {FAIXA_MAX_CONSULTAS} consultas por vez)."
        )

    df_bruto = _consultar_faixa(cep_ini, cep_fim, passo)

    if df_bruto.empty:
        st.warning("🔍 Nenhum bairro encontrado nessa faixa. Tente outra faixa de CEP.")
        return

    agrupado = _agrupar_por_bairro(df_bruto)

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
