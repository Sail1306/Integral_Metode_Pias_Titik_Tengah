import streamlit as st
import numpy as np
import sympy as sp
from PIL import Image
from scipy import special
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# ======================================================
#                 DARK MODE STATE
# ======================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.sidebar.title("⚙️ Pengaturan")
dark_switch = st.sidebar.checkbox("🌙 Mode Gelap", value=st.session_state.dark_mode)
st.session_state.dark_mode = dark_switch

# ======================================================
#                         CSS
# ======================================================
light_css = """
<style>
body { background-color: white; color: black; }
.stButton>button { width: 100%; background-color: #4CAF50; color: white; }
h1, h2, h3 { color: #1565C0; }
.highlight { background-color: #e8f5e9; color: #2E7D32; }
.result-box { background-color: #263238; color: #ECEFF1; border-left: 5px solid #FF9800; }
.function-guide { background-color: #1a1a1a; color: #fff; }
.angular-guide { background-color: #e8eaf6; border-left: 4px solid #3f51b5; }
</style>
"""

dark_css = """
<style>
body { background-color: #0e1117; color: #ffffff; }
.stApp { background-color: #0e1117; }
h1, h2, h3 { color: #90caf9; }
.stButton>button { background-color: #1f6feb; color: white; width: 100%; }
.stTextInput>div>div>input { background-color: #222; color: #4CAF50; }
.highlight { background-color: #1b2b1b; border-left: 5px solid #4CAF50; color: #a5d6a7; }
.result-box { background-color: #1e1e1e; color: #ffcc80; border-left: 5px solid #ffa726; }
.function-guide { background-color: #000; color: #4CAF50; }
.angular-guide { background-color: #2c2c54; border-left: 4px solid #7d5fff; }
.code-text { background-color: #333; color: #4CAF50; }
.sidebar .sidebar-content { background-color: #111; }
</style>
"""

# Terapkan CSS
st.markdown(dark_css if st.session_state.dark_mode else light_css, unsafe_allow_html=True)

# ======================================================
#                         TITLE
# ======================================================
st.title("🔢 Kalkulator Integral Lengkap – Simbolik, Numerik & Grafik")

# ======================================================
#                    INPUT PENGGUNA
# ======================================================
st.subheader("Masukkan Fungsi dan Batas Integral")

fungsi_str = st.text_input("Masukkan fungsi f(x):", "sin(x) + x**2")
a = st.text_input("Batas bawah (a):", "0")
b = st.text_input("Batas atas (b):", "3")

n_midpoint = st.number_input("Jumlah pembagian (Metode Titik Tengah):", 1, 10000, 10)

# Tombol trigger perhitungan
hitung = st.button("🔍 Hitung Integral")

# ======================================================
#             JIKA TOMBOL DITEKAN → MULAI HITUNG
# ======================================================
if hitung:

    # Konversi batas numerik
    try:
        a_val = float(a)
        b_val = float(b)
    except:
        st.error("❌ Batas integral harus berupa angka.")
        st.stop()

    # Parse fungsi sympy
    x = sp.symbols("x")
    try:
        f_sympy = sp.sympify(fungsi_str)
    except:
        st.error("❌ Fungsi tidak valid. Periksa kembali penulisan.")
        st.stop()

    f_numerik = sp.lambdify(x, f_sympy, "numpy")

    # ======================================================
    #        METODE TITIK TENGAH (MIDPOINT RULE)
    # ======================================================
    def midpoint_rule(func, a, b, n):
        h = (b - a) / n
        total = 0
        for i in range(n):
            mid = a + h * (i + 0.5)
            total += func(mid)
        return total * h

    midpoint_result = midpoint_rule(f_numerik, a_val, b_val, n_midpoint)

    # ======================================================
    #                INTEGRAL SIMBOLIK
    # ======================================================
    indefinite = sp.integrate(f_sympy, x)
    definite = sp.integrate(f_sympy, (x, a_val, b_val))

    # ======================================================
    #                    GRAFIK
    # ======================================================
    xx = np.linspace(a_val, b_val, 300)
    yy = f_numerik(xx)

    grafik = make_subplots()
    grafik.add_trace(go.Scatter(x=xx, y=yy, mode="lines", name="f(x)"))
    grafik.update_layout(
        title="Grafik Fungsi",
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_dark" if st.session_state.dark_mode else "plotly_white"
    )

    # ======================================================
    #                 OUTPUT HASIL
    # ======================================================
st.subheader("📌 Hasil Perhitungan")

# Integral Tak Tentu
st.markdown(
    """
    <div class='result-box'>
        <b>Integral umum (tak tentu):</b>
    </div>
    """,
    unsafe_allow_html=True
)

# Rumus LaTeX (MathJax)
indef_str = sp.latex(indefinite)
st.latex(r"\int f(x)\,dx = " + indef_str + r" + C")


# Integral Tentu
st.markdown(
    f"""
    <div class='result-box'>
        <b>Integral tentu simbolik:</b><br>
        ≈ {float(definite)}
    </div>
    """,
    unsafe_allow_html=True
)

# Midpoint Rule
st.markdown(
    f"""
    <div class='highlight'>
        <b>Hasil Metode Pias Titik Tengah</b><br>
        n = {n_midpoint}<br>
        ≈ {midpoint_result}
    </div>
    """,
    unsafe_allow_html=True
)

# Grafik
st.plotly_chart(grafik)

