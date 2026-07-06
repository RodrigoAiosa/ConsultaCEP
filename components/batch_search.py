"""
Componente: Busca em lote de CEPs a partir de uma planilha (.csv/.xlsx),
com exportação do resultado em .csv.
"""
import io
import time

import pandas as pd
import requests
import streamlit as st

from config import BATCH_SLEEP_BETWEEN_REQUESTS, BATCH_OUTPUT_COLUMNS
from services.viacep import limpar_cep, buscar_cep
from utils.address import montar_endereco_completo
from utils.spreadsheet import ler_planilha_de_ceps


def _processar_ceps(ceps: list) -> pd.DataFrame:
    linhas = []
    barra = st.progress(0.0, text="Iniciando...")
    total = len(ceps)

    for i, cep_bruto in enumerate(ceps):
        cep_limpo = limpar_cep(str(cep_bruto))

        if len(cep_limpo) != 8:
            linhas.append({
                "CEP": cep_bruto, "Endereço Completo": "", "Bairro": "",
                "Cidade": "", "Estado": "", "DDD": "", "IBGE": "",
            })
        else:
            try:
                dados = buscar_cep(cep_limpo)
            except requests.RequestException:
                dados = None

            if dados:
                linhas.append({
                    "CEP": dados.get("cep", cep_limpo),
                    "Endereço Completo": montar_endereco_completo(dados),
                    "Bairro": dados.get("bairro", "") or "",
                    "Cidade": dados.get("localidade", "") or "",
                    "Estado": dados.get("uf", "") or "",
                    "DDD": dados.get("ddd", "") or "",
                    "IBGE": dados.get("ibge", "") or "",
                })
            else:
                linhas.append({
                    "CEP": cep_limpo, "Endereço Completo": "", "Bairro": "",
                    "Cidade": "", "Estado": "", "DDD": "", "IBGE": "",
                })

        barra.progress((i + 1) / total, text=f"Consultando {i + 1}/{total}...")
        time.sleep(BATCH_SLEEP_BETWEEN_REQUESTS)

    barra.empty()
    return pd.DataFrame(linhas, columns=BATCH_OUTPUT_COLUMNS)


def render() -> None:
    """Renderiza a aba de busca em lote via planilha."""
    st.markdown(
        "<p style='color:#94a3b8; margin-bottom:1rem;'>Envie uma planilha "
        "(.csv ou .xlsx) com uma coluna de CEPs. O app consulta cada um na "
        "ViaCEP e gera um .csv para download com Endereço Completo, Bairro, "
        "Cidade, Estado, DDD e IBGE.</p>",
        unsafe_allow_html=True,
    )

    arquivo = st.file_uploader(
        "Planilha de CEPs", type=["csv", "xlsx", "xls"], label_visibility="collapsed",
    )
    if arquivo is None:
        return

    try:
        ceps = ler_planilha_de_ceps(arquivo)
    except Exception as e:
        st.error(f"❌ Não foi possível ler a planilha: {e}")
        return

    if not ceps:
        st.warning("🔍 Nenhum CEP encontrado na planilha.")
        return

    st.info(f"📄 {len(ceps)} CEP(s) encontrados na planilha.")

    if not st.button("Processar planilha", key="btn_lote"):
        return

    df_resultado = _processar_ceps(ceps)

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
