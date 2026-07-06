"""
BuscaCEP — Versão de teste simplificada
"""
from pathlib import Path
import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="BuscaCEP - Teste",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Tenta carregar o CSS
BASE_DIR = Path(__file__).parent
css_path = BASE_DIR / "assets" / "styles.css"

try:
    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        st.success(f"✅ CSS carregado de: {css_path}")
    else:
        st.error(f"❌ Arquivo CSS não encontrado em: {css_path}")
        
        # Lista os arquivos na pasta assets
        assets_dir = BASE_DIR / "assets"
        if assets_dir.exists():
            arquivos = list(assets_dir.iterdir())
            st.write(f"Arquivos encontrados em assets/: {[f.name for f in arquivos]}")
        else:
            st.write("Pasta assets/ não encontrada!")
            
except Exception as e:
    st.error(f"❌ Erro ao carregar CSS: {e}")

# Hero simples para teste
st.markdown("""
<style>
    /* CSS inline para teste */
    .hero-title {
        font-size: 3.1rem;
        font-weight: 900;
        color: #f8fafc;
        line-height: 1.1;
    }
    .hero-title span {
        background: linear-gradient(90deg, #38bdf8, #818cf8 60%, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .test-box {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(56, 189, 248, 0.3);
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        color: #f8fafc;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="hero-title">Teste de CSS<br><span>Funcionou! 🎉</span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="test-box">
        <h3>Se você está vendo este box com fundo escuro e borda azul,</h3>
        <p style="color: #94a3b8; font-size: 1.2rem;">
            o CSS está funcionando corretamente!
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Mostra informações de debug
with st.expander("🔍 Informações de debug"):
    st.write(f"Diretório base: {BASE_DIR}")
    st.write(f"Arquivo CSS existe? {css_path.exists()}")
    if css_path.exists():
        st.write(f"Tamanho do CSS: {css_path.stat().st_size} bytes")
    
    st.write("---")
    st.write("Estrutura de diretórios:")
    for item in BASE_DIR.iterdir():
        if item.is_dir():
            st.write(f"📁 {item.name}/")
            for subitem in item.iterdir():
                st.write(f"  📄 {subitem.name}")
        else:
            st.write(f"📄 {item.name}")
