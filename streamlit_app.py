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
# STATE DARK MODE (AMAN)
# ======================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("⚙️ Pengaturan")
st.sidebar.checkbox(
    "🌙 Mode Gelap",
    key="dark_mode"
)

st.sidebar.markdown("## 📘 Panduan Penulisan Input")
st.sidebar.markdown("""
- Gunakan variabel `x`
- Operator: `+ - * / **`
- Contoh: `x**2 + sin(x)`
- Batas integral harus bilangan real
""")

# ======================================================
# CSS TEMA (AMAN & STABIL)
# ======================================================
dark_css = """
<style>
[data-testid="stAppViewContainer"] { background-color: #0C132B; }
[data-testid="stSidebar"] { background-color: #0F172A; }
h1,h2,h3 { color: #93B4FF; }
label, p { color: #E5EDFF; }
input, textarea {
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
[data-testid="stSidebar"] { background-color: #EEF2FF; }
h1,h2,h3 { color: #1E3A8A; }
label, p { color: #0A1A40; }
input, textarea {
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
st.subheader("Metode Pias Titik Tengah")

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

    try:
        a_val = float(a)
        b_val = float(b)
    except ValueError:
        st.error("Batas integral harus berupa bilangan real.")
        st.stop()

    x = sp.symbols("x")
    try:
        f_sym = sp.sympify(fungsi_str)
    except:
        st.error("Sintaks fungsi tidak valid.")
        st.stop()

    f_num = sp.lambdify(x, f_sym, "numpy")

    h = (b_val - a_val) / n
    total = 0
    rows = []

    for i in range(n):
        xm = a_val + (i + 0.5) * h
        fxm = float(f_num(xm))
        area = fxm * h
        total += area
        rows.append([i + 1, xm, fxm, area])

    df = pd.DataFrame(
        rows,
        columns=["Iterasi", "x Titik Tengah", "f(x)", "Luas Pias"]
    )

    # Integral simbolik
    int_umum = sp.integrate(f_sym, x)
    int_tentu = sp.integrate(f_sym, (x, a_val, b_val))

    # OUTPUT
    st.subheader("📌 Hasil Perhitungan")

    st.markdown("<div class='result-box'><b>Integral Tak Tentu</b></div>", unsafe_allow_html=True)
    st.latex(r"\int f(x)\,dx = " + sp.latex(int_umum) + r" + C")

    st.markdown("<div class='result-box'><b>Integral Tentu</b></div>", unsafe_allow_html=True)
    st.latex(sp.latex(int_tentu))

    st.markdown("<div class='result-box'><b>Metode Titik Tengah</b></div>", unsafe_allow_html=True)
    st.write(f"Nilai pendekatan numerik = **{total}**")

    st.subheader("📊 Tabel Iterasi")
    st.dataframe(df, use_container_width=True)

    xx = np.linspace(a_val, b_val, 400)
    yy = f_num(xx)

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=xx, y=yy, mode="lines", name="f(x)"))
    fig.update_layout(
        template="plotly_dark" if st.session_state.dark_mode else "plotly_white",
        xaxis_title="x",
        yaxis_title="f(x)"
    )

    st.plotly_chart(fig, use_container_width=True)
