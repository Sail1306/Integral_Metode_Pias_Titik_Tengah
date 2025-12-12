import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Integral Solution (Pias Titik Tengah)",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
# Style button
.stButton>button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}

# Warna teks input 
.stTextInput>div>div>input {
    font-weight: bold;
    color: green;
}

# Warna judul
h1, h2, h3 {
    text-align: center;
    color: #1565C0;
}

# Kotak highlight
.highlight {
    background-color: #e8f5e9;
    padding: 1rem;
    border-radius: 5px;
    border-left: 5px solid #4CAF50;
}

# Kotak hasil 
.result-box {
    background-color: #263238;
    color: white;
    padding: 1rem;
    border-radius: 5px;
    border-left: 5px solid orange;
}
</style>
""", unsafe_allow_html=True)

# Integrasi
def try_integration(expr, x):
    try:
        hasil = sp.integrate(expr, x, meijerg=True, risch=True)
        if hasil.has(sp.Integral):
            expr_str = str(expr)
            if "sin(x**2)" in expr_str:
                return sp.sqrt(sp.pi/2) * (sp.fresnels(x) + sp.fresnelc(x))
            if "exp(-x**2)" in expr_str:
                return sp.sqrt(sp.pi) * sp.erf(x) / 2
            # coba simplifikasi lain
            hasil = sp.integrate(sp.simplify(expr), x)
        return hasil
    except:
        # fallback sederhana
        try:
            return sp.integrate(expr, x, manual=True)
        except:
            return None
