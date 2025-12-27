import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image

# ======================================================
# KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Integral Solution – Metode Titik Tengah",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ======================================================
# STATE DARK MODE
# ======================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("⚙️ Pengaturan")
st.sidebar.checkbox("🌙 Mode Gelap", key="dark_mode")

st.sidebar.markdown("## 📘 Panduan Penulisan Input")
st.sidebar.markdown("""
**Penulisan Fungsi**
- Gunakan variabel `x`
- Operator: `+ - * / **`
- Contoh:
  - `x**2 + 3*x`
  - `sin(x)`
  - `exp(x)`

**Fungsi Didukung**
- sin, cos, tan
- exp, log
- Polinomial

**Batas Integral**
- Bilangan real
- Contoh: 0, 2.5, -1

**Jumlah Subinterval**
- Semakin besar n → hasil lebih akurat
""")

# ======================================================
# CSS TEMA (AMAN)
# ======================================================
dark_css = """
<style>
[data-testid="stAppViewContainer"] { background-color: #0C132B; }
[data-testid="stSidebar"] { background-color: #0F172A; border-right: 2px solid #1E3A8A; }
h1,h2,h3,h4,h5,h6 { color: #93B4FF; }
label, p { color: #E5EDFF; }
input, textarea {
    background-color: #152044 !important;
    color: #E5EDFF !important;
    border: 1px solid #3E5FBF !important;
}
[data-baseweb="select"] > div {
    background-color: #152044 !important;
    color: #E5EDFF !important;
}
button {
    background-color: #1E3A8A !important;
    color: white !important;
}
.result-box {
    background-color: #10182F;
    border-left: 4px solid #3F66FF;
    padding: 12px;
    border-radius: 8px;
}
</style>
"""

light_css = """
<style>
[data-testid="stAppViewContainer"] { background-color: #F2F5FF; }
[data-testid="stSidebar"] { background-color: #EEF2FF; border-right: 2px solid #1E3A8A; }
h1,h2,h3,h4,h5,h6 { color: #1E3A8A; }
label, p { color: #0A1A40; }
input, textarea {
    background-color: white !important;
    color: #0A1A40 !important;
    border: 1px solid #1E3A8A !important;
}
[data-baseweb="select"] > div {
    background-color: white !important;
    color: #0A1A40 !important;
}
button {
    background-color: #1E40AF !important;
    color: white !important;
}
.result-box {
    background-color: #E9EEFF;
    border-left: 4px solid #1E3A8A;
    padding: 12px;
    border-radius: 8px;
}
</style>
"""

st.markdown(dark_css if st.session_state.dark_mode else light_css, unsafe_allow_html=True)

# ======================================================
# JUDUL
# ======================================================
st.title("🔢 Kalkulator Integral Simbolik dan Numerik")
st.subheader("Metode Pias Titik Tengah (Midpoint Rule)")

# ==================
