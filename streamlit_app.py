import streamlit as st
import numpy as np
import sympy as sp
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
# ------------------ MODE TERANG & GELAP (SIDEBAR + PAGE) ------------------

dark_css = """
    <style>
        /* Background halaman */
        .main {
            background-color: #0C132B !important;
            color: #E8F0FF !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #0C132B !important;
            border-right: 2px solid #1E3A8A !important;
        }

        /* Teks sidebar */
        section[data-testid="stSidebar"] * {
            color: #C5D3FF !important;
        }

        /* Judul */
        h1,h2,h3,h4,h5,h6 {
            color: #82A0FF !important;
        }

        /* Kotak input */
        .stTextInput>div>div>input,
        .stNumberInput input,
        .stTextArea textarea {
            background-color: #152044 !important;
            color: #DCE6FF !important;
            border: 1px solid #3E5FBF !important;
        }

        /* Selectbox */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: #152044 !important;
            color: #DCE6FF !important;
            border: 1px solid #3E5FBF !important;
        }

        /* Tombol */
        .stButton>button {
            background-color: #1E3A8A !important;
            color: white !important;
            border-radius: 6px !important;
            border: 1px solid #3F66FF !important;
        }

        .stButton>button:hover {
            background-color: #294AA8 !important;
        }

        /* Kotak hasil */
        .result-box {
            background-color: #10182F !important;
            color: #E3EAFF !important;
            border-left: 4px solid #3F66FF !important;
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
        }
    </style>
    """

light_css = """
    <style>
        /* Background halaman */
        .main {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #E9EEFF !important;
            border-right: 2px solid #1E3A8A !important;
        }

        /* Teks sidebar */
        section[data-testid="stSidebar"] * {
            color: #0A1A40 !important;
        }

        /* Judul */
        h1,h2,h3,h4,h5,h6 {
            color: #1E3A8A !important;
        }

        /* Kotak input */
        .stTextInput>div>div>input,
        .stNumberInput input,
        .stTextArea textarea {
            background-color: white !important;
            color: black !important;
            border: 1px solid #1E3A8A !important;
        }

        /* Selectbox */
        .stSelectbox div[data-baseweb="select"] > div {
            background-color: white !important;
            color: black !important;
            border: 1px solid #1E3A8A !important;
        }

        /* Tombol */
        .stButton>button {
            background-color: #1E40AF !important;
            color: white !important;
            border-radius: 6px !important;
        }

        .stButton>button:hover {
            background-color: #2A4CCF !important;
        }

        /* Kotak hasil */
        .result-box {
            background-color: #F0F4FF !important;
            color: #0A1A40 !important;
            border-left: 4px solid #1E3A8A !important;
            padding: 12px;
            border-radius: 8px;
            margin-top: 15px;
        }
    </style>
    """

if st.session_state.dark_mode:
    css_theme = f"<style>{dark_css}</style>"
else:
    css_theme = f"<style>{light_css}</style>"

st.markdown(css_theme, unsafe_allow_html=True)

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
#        BLOK PERHITUNGAN HARUS DI DALAM if hitung:
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

    st.latex(r"\int f(x)\,dx = " + sp.latex(indefinite) + r" + C")

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

    st.plotly_chart(grafik)
