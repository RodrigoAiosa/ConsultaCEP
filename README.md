# BuscaCEP

Consulta de endereços brasileiros a partir do CEP, com mapa interativo,
processamento em lote via planilha e geração de tabelas de bairros por
faixa de CEP — tudo usando **APIs públicas e gratuitas**, sem chave de API.

## Funcionalidades

- **Busca individual**: digite um CEP e veja o endereço completo, cartão
  estilizado com todos os campos, e um mapa interativo (com fallback de
  precisão: rua → bairro → cidade → estado).
- **Busca em lote (planilha)**: envie um `.csv` ou `.xlsx` com uma coluna
  de CEPs e baixe o resultado processado em `.csv` (CEP, Endereço Completo,
  Bairro, Cidade, Estado, DDD, IBGE).
- **Bairros por faixa de CEP**: informe uma faixa (ex: `01000` a `01999`)
  e o app gera, na hora, uma tabela de bairros observados naquela faixa,
  consultando a ViaCEP por amostragem.

## APIs utilizadas

| API | Uso | Custo |
|---|---|---|
| [ViaCEP](https://viacep.com.br) | Dados de endereço a partir do CEP | Gratuita, sem chave |
| [Nominatim (OpenStreetMap)](https://nominatim.org) | Geocodificação (endereço → lat/lon) | Gratuita, sem chave |

## Estrutura do projeto

```
cep_app/
├── app.py                     # Ponto de entrada — orquestra a página e as abas
├── config.py                  # Constantes e configurações centralizadas
├── requirements.txt
├── .streamlit/
│   └── config.toml            # Tema do Streamlit
├── assets/
│   └── styles.css             # CSS da landing page
├── services/                  # Acesso a APIs externas (camada de dados)
│   ├── viacep.py
│   └── geocoding.py
├── utils/                     # Funções auxiliares puras (sem UI)
│   ├── address.py
│   └── spreadsheet.py
└── components/                # Uma aba = um componente de UI
    ├── individual_search.py
    ├── batch_search.py
    └── cep_range.py
```

### Por que essa separação?

- **`services/`** isola toda chamada de rede. Se um dia trocar a ViaCEP por
  outra API, só mexe aqui.
- **`utils/`** tem funções puras (sem `st.*`), fáceis de testar isoladamente.
- **`components/`** cada aba é independente — adicionar uma nova aba não
  exige tocar nas outras.
- **`config.py`** elimina "números mágicos" espalhados pelo código.
- **`assets/styles.css`** separa estilo de lógica; qualquer dev de front
  consegue mexer no visual sem tocar em Python.

## Como rodar

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Possíveis evoluções

- Testes unitários para `utils/` e `services/` (ex: com `pytest` + `responses`
  para mockar chamadas HTTP).
- Cache mais robusto (ex: Redis) se o uso crescer.
- Internacionalização (i18n) caso precise suportar outros idiomas.
