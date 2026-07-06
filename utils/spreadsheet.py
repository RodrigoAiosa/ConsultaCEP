"""
Funções utilitárias para ler planilhas (.csv/.xlsx) enviadas pelo usuário
e extrair a coluna de CEPs.
"""
import pandas as pd


def ler_planilha_de_ceps(arquivo) -> list:
    """
    Lê um arquivo .csv ou .xlsx e retorna a lista de CEPs encontrados.

    Procura uma coluna cujo nome contenha "cep"; se não encontrar, assume
    que a primeira coluna da planilha contém os CEPs.

    Levanta RuntimeError com mensagem amigável se faltar dependência (openpyxl).
    """
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

    coluna_cep = next((col for col in df.columns if "cep" in str(col).strip().lower()), None)
    if coluna_cep is None:
        coluna_cep = df.columns[0]

    return df[coluna_cep].dropna().astype(str).tolist()
