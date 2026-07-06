"""
Funções utilitárias de formatação de endereço a partir do retorno da ViaCEP.
"""


def montar_endereco_completo(dados: dict) -> str:
    """
    Monta uma string única e legível de endereço completo, no formato:
    'Rua Exemplo, Complemento, Bairro - Cidade - UF, CEP 12345-678'
    """
    partes_endereco = [
        dados.get("logradouro"),
        dados.get("complemento"),
        dados.get("bairro"),
    ]
    linha1 = ", ".join(p for p in partes_endereco if p)

    partes_local = [dados.get("localidade"), dados.get("uf")]
    linha2 = " - ".join(p for p in partes_local if p)

    endereco = " - ".join(p for p in [linha1, linha2] if p)
    if dados.get("cep"):
        endereco = f"{endereco}, CEP {dados.get('cep')}" if endereco else dados.get("cep")
    return endereco


def formatar_cep_prefixo(base5: int) -> str:
    """Converte um inteiro (ex: 1000) no formato de 8 dígitos usado pela ViaCEP (ex: '01000000')."""
    return f"{base5:05d}000"
