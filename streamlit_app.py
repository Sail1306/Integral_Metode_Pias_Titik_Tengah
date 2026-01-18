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
/* =============================== */
/* BACKGROUND UTAMA */
/* =============================== */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #0B122B 0%, #0E163A 100%);
}

/* =============================== */
/* SIDEBAR */
/* =============================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1026 0%, #0E1538 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* =============================== */
/* TEKS */
/* =============================== */
html, body, p, span, label, div, li {
    color: #E5E7EB !important;
}

h1, h2, h3, h4, h5, h6 {
    color: #F9FAFB !important;
}

/* =============================== */
/* HEADER ATAS */
/* =============================== */
header, [data-testid="stHeader"] {
    background: #0B122B !important;
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
}

header svg {
    fill: #E5E7EB !important;
}

/* =============================== */
/* INPUT FIELD */
/* =============================== */
input, textarea {
    background: rgba(255,255,255,0.06) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
    padding: 0.6em 0.8em !important;
}

input::placeholder,
textarea::placeholder {
    color: rgba(255,255,255,0.6) !important;
}

input:focus,
textarea:focus {
    outline: none !important;
    box-shadow: none !important;
    border: 1px solid rgba(255,255,255,0.5) !important;
}

/* =============================== */
/* BUTTON */
/* =============================== */
button {
    background: rgba(255,255,255,0.08) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
    padding: 0.6em 1.3em !important;
    font-weight: 500 !important;
}

button:hover {
    background: rgba(255,255,255,0.15) !important;
}

/* =============================== */
/* NUMBER INPUT (+ / -) */
/* =============================== */
[data-testid="stNumberInput"] button {
    background: rgba(255,255,255,0.08) !important;
    border: none !important;
    color: #FFFFFF !important;
}

/* =============================== */
/* RESULT BOX */
/* =============================== */
.result-box {
    background: rgba(255,255,255,0.05);
    border-left: 4px solid #60A5FA;
    border-radius: 10px;
}

/* =============================== */
/* GRAFIK */
/* =============================== */
.plotly .modebar {
    background: transparent !important;
    box-shadow: none !important;
}

.plotly .modebar-btn {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
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

/* Header */
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

/* Tombol */
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

/* ================================================= */
/* FIX LIGHT MODE: HILANGKAN OUTLINE TOOLBAR PLOTLY */
/* ================================================= */

.plotly .modebar {
    background: transparent !important;
    box-shadow: none !important;
}

.plotly .modebar-btn {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

.plotly .modebar-btn:hover,
.plotly .modebar-btn:focus,
.plotly .modebar-btn:focus-visible,
.plotly .modebar-btn:active {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
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
