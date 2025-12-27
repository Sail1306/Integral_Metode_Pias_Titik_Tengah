import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image

# ======================================================
#                KONFIGURASI HALAMAN
# ======================================================
st.set_page_config(
    page_title="Integral Solution – Metode Titik Tengah",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ======================================================
#                DARK MODE STATE
# ======================================================
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

st.sidebar.title("⚙️ Pengaturan")
st.session_state.dark_mode = st.sidebar.checkbox(
    "🌙 Mode Gelap",
    value=st.session_state.dark_mode
)

# ======================================================
#                BOOK GUIDE (SIDEBAR)
# ======================================================
st.sidebar.markdown("## 📘 Panduan Penulisan Input")
st.sidebar.markdown("""
**1. Penulisan Fungsi**
- Gunakan variabel `x`
- Gunakan operator Python  
  Contoh:
  - `x**2 + 3*x`
  - `sin(x)`
  - `exp(x)`

**2. Fungsi yang Didukung**
- sin(x), cos(x), tan(x)
- exp(x), log(x)
- Polinomial

**3. Batas Integral**
- Harus berupa bilangan real
- Contoh: 0, 1.5, -2

**4. Metode Titik Tengah**
- Semakin besar `n`, hasil semakin mendekati nilai eksak
""")

# ======================================================
#                CSS TEMA
# ======================================================
css_theme = """
<style>
.main, [data-testid="stAppViewContainer"] {
    background-color: %s;
}
</style>
""" % ("#0C132B" if st.session_state.dark_mode else "#F2F5FF")

st.markdown(css_theme, unsafe_allow_html=True)

# ======================================================
#                JUDUL APLIKASI
# ======================================================
st.title("🔢 Kalkulator Integral Simbolik dan Numerik")
st.subheader("Metode Pias Titik Tengah (Midpoint Rule)")

# ======================================================
#                INPUT PENGGUNA
# ======================================================
fungsi_str = st.text_input("Masukkan fungsi f(x):", "sin(x) + x**2")
a = st.text_input("Batas bawah (a):", "0")
b = st.text_input("Batas atas (b):", "3")
n_mid = st.number_input(
    "Jumlah subinterval (n):",
    min_value=1,
    max_value=10000,
    value=10
)

# ======================================================
#        OPSI UPLOAD GAMBAR (OCR SEDERHANA)
# ======================================================
st.markdown("### 📷 Unggah Gambar Fungsi (Opsional)")
uploaded_file = st.file_uploader(
    "Unggah gambar berisi fungsi f(x) (format .png / .jpg)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang diunggah", use_column_width=True)
    st.info(
        "Catatan: Fitur OCR matematika bersifat terbatas. "
        "Jika hasil tidak akurat, disarankan tetap menggunakan input teks."
    )

# ======================================================
#                TOMBOL EKSEKUSI
# ======================================================
if st.button("🔍 Hitung Integral"):

    # Validasi batas
    try:
        a_val = float(a)
        b_val = float(b)
    except ValueError:
        st.error("Batas integral harus berupa bilangan real.")
        st.stop()

    # Definisi simbol
    x = sp.symbols("x")

    # Validasi fungsi
    try:
        f_sym = sp.sympify(fungsi_str)
    except:
        st.error("Fungsi tidak valid sesuai sintaks matematika.")
        st.stop()

    f_num = sp.lambdify(x, f_sym, "numpy")

    # ==================================================
    #        METODE Pias Titik Tengah
    # ==================================================
    h = (b_val - a_val) / n_mid
    data_iterasi = []

    total = 0
    for i in range(n_mid):
        xi = a_val + i * h
        xi_mid = xi + 0.5 * h
        f_mid = f_num(xi_mid)
        luas = f_mid * h
        total += luas

        data_iterasi.append([
            i + 1,
            xi_mid,
            f_mid,
            luas
        ])

    df_iterasi = pd.DataFrame(
        data_iterasi,
        columns=["Iterasi", "x Titik Tengah", "f(x)", "Luas Pias"]
    )

    # ==================================================
    #        INTEGRAL SIMBOLIK
    # ==================================================
    integral_tak_tentu = sp.integrate(f_sym, x)
    integral_tentu = sp.integrate(f_sym, (x, a_val, b_val))

    # ==================================================
    #        OUTPUT HASIL
    # ==================================================
    st.subheader("📌 Hasil Analisis Integral")

    st.markdown("**Integral Tak Tentu:**")
    st.latex(r"\int f(x)\,dx = " + sp.latex(integral_tak_tentu) + r" + C")

    st.markdown("**Integral Tentu (Simbolik):**")
    st.latex(sp.latex(integral_tentu))

    st.markdown("**Pendekatan Numerik (Metode Titik Tengah):**")
    st.write(f"Nilai pendekatan = **{total}**")

    # ==================================================
    #        TABEL ITERASI
    # ==================================================
    st.subheader("📊 Tabel Iterasi Metode Titik Tengah")
    st.dataframe(df_iterasi, use_container_width=True)

    # ==================================================
    #        GRAFIK
    # ==================================================
    xx = np.linspace(a_val, b_val, 400)
    yy = f_num(xx)

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=xx, y=yy, mode="lines", name="f(x)"))
    fig.update_layout(
        title="Grafik Fungsi f(x)",
        xaxis_title="x",
        yaxis_title="f(x)",
        template="plotly_dark" if st.session_state.dark_mode else "plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)
