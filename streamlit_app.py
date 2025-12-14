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

body { 
    background: linear-gradient(180deg, #0d1117, #0b0f16);
    color: #e3f2fd; 
}

.stApp { 
    background: linear-gradient(180deg, #0d1117, #0b0f16);
}

/* ===========================
   TITLE (H1, H2) GLOSSY BLUE
   =========================== */
h1, h2, h3 { 
    color: #82cfff !important;
    text-shadow: 0px 0px 10px rgba(100,170,255,0.55);
    font-weight: 700;
}



/* ===========================
   BUTTON GLOSSY BLUE
   =========================== */
.stButton>button { 
    width: 100%;
    background: linear-gradient(90deg, #1e88e5, #42a5f5);
    color: white;
    border-radius: 8px;
    border: 1px solid #90caf9;
    box-shadow: 0px 0px 12px rgba(33,150,243,0.6);
    transition: 0.2s;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #2196f3, #64b5f6);
    box-shadow: 0px 0px 16px rgba(100,181,246,0.7);
}



/* ===========================
   TEXT INPUT GLOSSY BLUE
   =========================== */
.stTextInput>div>div>input {
    background: #121926;
    color: #bbdefb;
    border: 1px solid #64b5f6;
    border-radius: 6px;
    padding: 8px;
    box-shadow: inset 0px 0px 6px rgba(100,181,246,0.25);
}



/* ===========================
   NUMBER INPUT GLOSSY BLUE
   (untuk jumlah pembagian)
   =========================== */
.stNumberInput > div > input {
    background: #121926 !important;
    color: #bbdefb !important;
    border: 1px solid #64b5f6 !important;
    border-radius: 6px;
    padding: 6px;
    box-shadow: inset 0px 0px 6px rgba(100,181,246,0.25) !important;
    font-weight: bold;
}

.stNumberInput label {
    color: #90caf9 !important;
}



/* ===========================
   HIGHLIGHT BOX
   =========================== */
.highlight { 
    background: #11263b;
    border-left: 5px solid #4FC3F7;
    color: #E1F5FE;
    box-shadow: 0px 0px 10px rgba(79,195,247,0.3);
}



/* ===========================
   RESULT BOX
   =========================== */
.result-box { 
    background: #162032;
    color: #FFECB3;
    border-left: 5px solid #FFB74D;
    box-shadow: 0px 0px 10px rgba(255,183,77,0.3);
    padding: 1rem;
    border-radius: 6px;
}



/* ===========================
   FUNCTION GUIDE
   =========================== */
.function-guide { 
    background: #0d1824;
    color: #90caf9;
    border-left: 4px solid #64b5f6;
    box-shadow: 0px 0px 8px rgba(100,181,246,0.3);
}



/* ===========================
   ANGULAR GUIDE
   =========================== */
.angular-guide { 
    background: #1a2235;
    border-left: 4px solid #82B1FF;
    color: #E3F2FD;
    box-shadow: 0px 0px 10px rgba(130,177,255,0.3);
}



/* ===========================
   CODE TEXT
   =========================== */
.code-text { 
    background: #1e1e1e;
    color: #81D4FA;
    border-radius: 4px;
    padding: 2px 4px;
    box-shadow: inset 0px 0px 4px rgba(129,212,250,0.3);
}



/* ===========================
   SIDEBAR
   =========================== */
.sidebar .sidebar-content { 
    background: linear-gradient(180deg, #0b0f16, #101827);
    color: #e3f2fd;
    border-right: 1px solid #263238;
}

</style>
"""

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
