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
# STATE MODE
# ======================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ======================================================
# SIDEBAR
# ======================================================
st.sidebar.title("⚙️ Pengaturan Tampilan")
st.session_state.dark_mode = st.sidebar.toggle(
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
- Nilai n besar → akurasi meningkat
""")

# ======================================================
# CSS TEMA (KONSISTEN)
# ======================================================
dark_css = """
<style>
[data-testid="stAppViewContainer"] { background-color: #0B1023; }
[data-testid="stSidebar"] { background-color: #0F172A; }
h1,h2,h3,h4,h5,h6 { color: #E5EDFF; }
label, p, span, div { color: #E5EDFF !important; }

input, textarea {
    background-color: #111827 !important;
    color: #E5EDFF !important;
    border: 1px solid #3B82F6 !important;
}

[data-baseweb="select"] > div {
    background-color: #111827 !important;
    color: #E5EDFF !important;
}

button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
}

[data-testid="stDataFrame"] {
    background-color: #020617;
    color: #E5EDFF;
}

.result-box {
    background-color: #020617;
    border-left: 4px solid #60A5FA;
    padding: 12px;
    border-radius: 8px;
}
</style>
"""

light_css = """
<style>
[data-testid="stAppViewContainer"] { background-color: #F8FAFF; }
[data-testid="stSidebar"] { background-color: #EEF2FF; }
h1,h2,h3,h4,h5,h6 { color: #1E3A8A; }
label, p, span, div { color: #0A1A40 !important; }

input, textarea {
    background-color: #FFFFFF !important;
    color: #0A1A40 !important;
    border: 1px solid #1E3A8A !important;
}

[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    color: #0A1A40 !important;
}

button {
    background-color: #1E40AF !important;
    color: #FFFFFF !important;
}

[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    color: #0A1A40;
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

# ======================================================
# INPUT MANUAL
# ======================================================
fungsi_str = st.text_input("Masukkan fungsi f(x):", "sin(x) + x**2")
a = st.text_input("Batas bawah (a):", "0")
b = st.text_input("Batas atas (b):", "3")
n = st.number_input("Jumlah subinterval (n):", 1, 10000, 10)

# ======================================================
# UNGGAH FOTO SOAL
# ======================================================
st.markdown("### 📷 Unggah Foto Soal Integral (Opsional)")
uploaded = st.file_uploader(
    "Unggah foto soal (.png / .jpg)",
    ["png", "jpg", "jpeg"]
)

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Foto soal terunggah", use_container_width=True)
    st.info(
        "Gambar digunakan sebagai referensi visual. "
        "Ekstraksi otomatis (OCR matematika) dapat dikembangkan pada tahap lanjutan."
    )

# ======================================================
# PROSES PERHITUNGAN
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
    data = []
    total = 0

    for i in range(n):
        xm = a_val + (i + 0.5) * h
        fxm = f_num(xm)
        area = fxm * h
        total += area
        data.append([i + 1, xm, fxm, area])

    df = pd.DataFrame(
        data,
        columns=["Iterasi", "x Titik Tengah", "f(x)", "Luas Pias"]
    )

    int_umum = sp.integrate(f_sym, x)
    int_tentu = sp.integrate(f_sym, (x, a_val, b_val))

    # ==================================================
    # OUTPUT
    # ==================================================
    st.subheader("📌 Hasil Perhitungan")

    st.markdown("<div class='result-box'><b>Integral Tak Tentu</b></div>", unsafe_allow_html=True)
    st.latex(r"\int f(x)\,dx = " + sp.latex(int_umum) + r" + C")

    st.markdown("<div class='result-box'><b>Integral Tentu (Simbolik)</b></div>", unsafe_allow_html=True)
    st.latex(sp.latex(int_tentu))

    st.markdown("<div class='result-box'><b>Metode Titik Tengah</b></div>", unsafe_allow_html=True)
    st.write(f"Nilai pendekatan numerik = **{total}**")

    st.subheader("📊 Tabel Iterasi")
    st.dataframe(df, use_container_width=True)

    xx = np.linspace(a_val, b_val, 400)
    yy = f_num(xx)

    fig = make_subplots()
    fig.add_trace_
