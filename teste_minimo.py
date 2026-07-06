# teste_minimo.py
import streamlit as st

st.set_page_config(
    page_title="Teste Mínimo",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS mais agressivo possível
st.markdown("""
<style>
    /* Força o fundo escuro em TODOS os elementos */
    html, body, .stApp, .main, .block-container, [data-testid="stAppViewContainer"] {
        background-color: #0a0e1a !important;
        background: #0a0e1a !important;
    }
    
    /* Força a cor do texto */
    * {
        color: #f8fafc !important;
    }
    
    /* Tenta forçar o fundo de cada elemento */
    div, section, main, header, footer {
        background-color: #0a0e1a !important;
    }
    
    /* Título de teste */
    .teste-grande {
        font-size: 3rem !important;
        color: #38bdf8 !important;
        text-align: center !important;
        padding: 2rem !important;
        background: linear-gradient(90deg, #38bdf8, #818cf8) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    .caixa-teste {
        background: rgba(56, 189, 248, 0.1) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 16px !important;
        padding: 2rem !important;
        margin: 2rem 0 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="teste-grande">🎯 TESTE VISUAL</h1>', unsafe_allow_html=True)

st.markdown("""
<div class="caixa-teste">
    <h3>Se você está vendo:</h3>
    <ul>
        <li>✅ Fundo escuro</li>
        <li>✅ Texto "TESTE VISUAL" com gradiente azul</li>
        <li>✅ Esta caixa com borda azul</li>
    </ul>
    <p><strong>O CSS está funcionando!</strong></p>
</div>
""", unsafe_allow_html=True)

# Mostra informações do sistema
with st.expander("🔍 Informações de debug"):
    st.write("Streamlit version:", st.__version__)
    st.write("Theme config:", st.get_option("theme.base"))
