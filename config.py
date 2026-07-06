"""
Configurações centrais do app: constantes, URLs de APIs, limites e textos fixos.
Mantenha aqui qualquer valor "mágico" para facilitar manutenção futura.
"""

# ---------------------------------------------------------------------------
# Metadados da página
# ---------------------------------------------------------------------------
APP_TITLE = "BuscaCEP | Consulta de Endereços"
APP_ICON = "📍"

# ---------------------------------------------------------------------------
# APIs públicas utilizadas (ambas gratuitas, sem necessidade de chave)
# ---------------------------------------------------------------------------
VIACEP_BASE_URL = "https://viacep.com.br/ws/{cep}/json/"
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_USER_AGENT = "BuscaCEP-Streamlit-App/1.0"

REQUEST_TIMEOUT_SECONDS = 8
CACHE_TTL_SECONDS = 3600  # 1 hora

# ---------------------------------------------------------------------------
# Busca em lote (planilha)
# ---------------------------------------------------------------------------
BATCH_SLEEP_BETWEEN_REQUESTS = 0.05  # evita sobrecarregar a API pública
BATCH_OUTPUT_COLUMNS = ["CEP", "Endereço Completo", "Bairro", "Cidade", "Estado", "DDD", "IBGE"]

# ---------------------------------------------------------------------------
# Bairros por faixa de CEP
# ---------------------------------------------------------------------------
FAIXA_MAX_CONSULTAS = 500
FAIXA_SLEEP_BETWEEN_REQUESTS = 0.05
FAIXA_CEP_INICIAL_PADRAO = "01000"
FAIXA_CEP_FINAL_PADRAO = "01999"
FAIXA_PASSO_PADRAO = 10

# ---------------------------------------------------------------------------
# Geocodificação (níveis de precisão, do mais específico ao mais genérico)
# ---------------------------------------------------------------------------
ZOOM_POR_NIVEL_PRECISAO = {"rua": 16, "bairro": 14, "cidade": 11, "estado": 6}

AVISOS_PRECISAO = {
    "bairro": "Localização aproximada pelo bairro (rua não localizada no mapa).",
    "cidade": "Localização aproximada pela cidade (endereço exato não encontrado no mapa).",
    "estado": "Localização aproximada pelo estado (endereço não encontrado no mapa).",
}
