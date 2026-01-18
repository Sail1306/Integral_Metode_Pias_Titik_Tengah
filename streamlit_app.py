import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

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
# STATE MODE
# ======================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("⚙️ Pengaturan")
st.session_state.dark_mode = st.sidebar.checkbox(
    "🌙 Mode Gelap",
    value=st.session_state.dark_mode
)

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

**Jumlah Subinterval**
- Semakin besar n → hasil lebih akurat
""")

# ======================================================
# CSS MODE GELAP 
# ======================================================

dark_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0C132B;
}
[data-testid="stSidebar"] {
    background-color: #0F172A;
    border-right: 2px solid #1E3A8A;
}

/* Teks */
html, body, p, span, label, div, li {
    color: #FFFFFF !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #E6ECFF !important;
}

/* Input – HILANGKAN GARIS HITAM */
input, textarea {
    background-color: #152044 !important;
    color: #FFFFFF !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Wrapper input Streamlit (penyebab outline hitam) */
div[data-baseweb="input"] *,
div[data-baseweb="textarea"] * {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Saat fokus */
input:focus,
textarea:focus {
    outline: none !important;
    box-shadow: none !important;
}

/* Tombol */
button {
    background-color: #1F2A5A !important;
    color: #FFFFFF !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 0.6em 1.3em !important;
    font-weight: 600 !important;
}
button:hover {
    background-color: #2F3E8F !important;
}

/* Box hasil */
.result-box {
    background-color: #10182F;
    border-left: 4px solid #3F66FF;
    padding: 12px;
    border-radius: 8px;
}

/* Plotly toolbar – dark mode tanpa kotak */
.plotly .modebar {
    background: transparent !important;
}
.plotly .modebar-btn {
    background: transparent !important;
    border: none !important;
}
.plotly .modebar-btn svg {
    fill: #FFFFFF !important;
}
.plotly .modebar-btn:hover {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 6px !important;
}
</style>
"""


# ======================================================
# CSS MODE TERANG 
# ======================================================
light_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: #F9FAFB;
}
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #9CA3AF;
}

/* Teks */
html, body, p, span, label, div, li {
    color: #111827 !important;
}
h1, h2, h3, h4, h5, h6 {
    color: #111827 !important;
}

/* Toolbar atas */
header, [data-testid="stHeader"] {
    background-color: #FFFFFF !important;
    border-bottom: 1px solid #9CA3AF !important;
}
header svg {
    fill: #374151 !important;
}

/* Input */
input, textarea {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #9CA3AF !important;
}

/* Sidebar tools */
[data-testid="stSidebar"] button,
[data-testid="stSidebar"] input[type="checkbox"] + div {
    background-color: #FFFFFF !important;
    border: 1px solid #9CA3AF !important;
    color: #111827 !important;
}

/* Tombol utama */
button {
    background-color: #FFFFFF !important;
    color: #111827 !important;
    border: 1px solid #9CA3AF !important;
    border-radius: 8px !important;
    padding: 0.6em 1.3em !important;
    font-weight: 500 !important;
}
button:hover {
    background-color: #F3F4F6 !important;
}
</style>
"""

st.markdown(
    dark_css if st.session_state.dark_mode else light_css,
    unsafe_allow_html=True
)

# ======================================================
# JUDUL
# ======================================================
st.title("🔢 Kalkulator Integral")
st.subheader("Metode Pias Titik Tengah (Midpoint Rule)")

# ======================================================
# INPUT
# ======================================================
fungsi_str = st.text_input("Masukkan fungsi f(x):", "sin(x) + x**2")
a = st.text_input("Batas bawah (a):", "0")
b = st.text_input("Batas atas (b):", "3")
n = st.number_input("Jumlah subinterval (n):", 1, 10000, 10)

# ======================================================
# PROSES
# ======================================================
if st.button("🔍 Hitung Integral"):
    a_val = float(a)
    b_val = float(b)

    x = sp.symbols("x")
    f_sym = sp.sympify(fungsi_str)
    f_num = sp.lambdify(x, f_sym, "numpy")

    h = (b_val - a_val) / n
    total = 0.0
    data = []

    for i in range(n):
        xm = a_val + (i + 0.5) * h
        fxm = float(f_num(xm))
        area = fxm * h
        total += area
        data.append([i + 1, xm, fxm, area])

    df = pd.DataFrame(
        data,
        columns=["Iterasi", "x Titik Tengah", "f(x)", "Luas Pias"]
    )

    st.subheader("📌 Hasil Perhitungan")
    st.markdown("<div class='result-box'><b>Metode Titik Tengah</b></div>", unsafe_allow_html=True)
    st.write(f"Nilai pendekatan numerik = **{total}**")

    st.dataframe(df, use_container_width=True)

    xx = np.linspace(a_val, b_val, 400)
    yy = np.array(f_num(xx), dtype=float)

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=xx, y=yy, mode="lines", name="f(x)"))
    fig.update_layout(
        template="plotly_dark" if st.session_state.dark_mode else "plotly_white",
        title="Grafik Fungsi f(x)",
        xaxis_title="x",
        yaxis_title="f(x)"
    )

    st.plotly_chart(fig, use_container_width=True)
