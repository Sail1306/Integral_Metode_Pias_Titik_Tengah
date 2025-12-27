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
# CSS TEMA
# ======================================================
dark_css = """
<style>
[data-testid="stAppViewContainer"] { background-color: #0C132B; }
[data-testid="stSidebar"] { background-color: #0F172A; border-right: 2px solid #1E3A8A; }
h1,h2,h3,h4,h5,h6 { color: #93B4FF; }
p, label, span, div { color: #E5EDFF; }
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
[data-testid="stDataFrame"] {
    background-color: #0F172A;
    color: #E5EDFF;
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
p, label, span, div { color: #0A1A40; }
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
[data-testid="stDataFrame"] {
    background-color: white;
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
# INPUT
# ======================================================
fungsi_str = st.text_input("Masukkan fungsi f(x):", "sin(x) + x**2")
a = st.text_input("Batas bawah (a):", "0")
b = st.text_input("Batas atas (b):", "3")
n = st.number_input("Jumlah subinterval (n):", 1, 10000, 10)

# ======================================================
# UPLOAD GAMBAR
# ======================================================
st.markdown("### 📷 Unggah Gambar Soal (Opsional)")
uploaded = st.file_uploader("Unggah gambar (.png/.jpg)", ["png", "jpg", "jpeg"])
if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Gambar terunggah", use_container_width=True)
    st.info("Gambar digunakan sebagai referensi visual soal.")

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

    # Metode Titik Tengah
    h = (b_val - a_val) / n
    data = []
    total = 0.0

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

    # ==================================================
    # GRAFIK (FIX FINAL)
    # ==================================================
    try:
        xx = np.linspace(a_val, b_val, 400)
        yy = np.array(f_num(xx), dtype=float)

        mask = np.isfinite(yy)
        xx = xx[mask]
        yy = yy[mask]

        if len(xx) == 0:
            st.warning("Grafik tidak dapat ditampilkan karena fungsi tidak terdefinisi.")
        else:
            fig = make_subplots()
            fig.add_trace(go.Scatter(
                x=xx,
                y=yy,
                mode="lines",
                name="f(x)",
                line=dict(width=3)
            ))

            fig.update_layout(
                template="plotly_dark" if st.session_state.dark_mode else "plotly_white",
                title="Grafik Fungsi f(x)",
                xaxis_title="x",
                yaxis_title="f(x)",
                font=dict(
                    color="#E5EDFF" if st.session_state.dark_mode else "#0A1A40"
                )
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception:
        st.error("Terjadi kesalahan saat menampilkan grafik.")
