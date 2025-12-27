import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
import pytesseract
import cv2
import re

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
**Format Foto yang Disarankan**
- ∫_0^3 (x^2 + sin(x)) dx
- ∫_1^2 x^2 dx

**Fungsi Didukung**
- sin, cos, tan
- exp, log
- Polinomial

**Catatan**
- Tulisan jelas
- Kontras tinggi
- Tidak miring
""")

# ======================================================
# CSS TEMA
# ======================================================
dark_css = """
<style>
[data-testid="stAppViewContainer"] { background-color: #0C132B; color: #E5EDFF; }
[data-testid="stSidebar"] { background-color: #0F172A; border-right: 2px solid #1E3A8A; }
h1,h2,h3,h4,h5,h6 { color: #93B4FF; }
p, label, span, div { color: #E5EDFF; }
input, textarea {
    background-color: #152044 !important;
    color: #E5EDFF !important;
    border: 1px solid #3E5FBF !important;
}
button {
    background-color: #1E3A8A !important;
    color: white !important;
}
[data-testid="stFileUploader"] section {
    background-color: #152044 !important;
    border: 2px dashed #3E5FBF !important;
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
[data-testid="stAppViewContainer"] { background-color: #F2F5FF; color: #0A1A40; }
[data-testid="stSidebar"] { background-color: #EEF2FF; border-right: 2px solid #1E3A8A; }
h1,h2,h3,h4,h5,h6 { color: #1E3A8A; }
p, label, span, div { color: #0A1A40; }
input, textarea {
    background-color: white !important;
    color: #0A1A40 !important;
    border: 1px solid #1E3A8A !important;
}
button {
    background-color: #1E40AF !important;
    color: white !important;
}
[data-testid="stFileUploader"] section {
    background-color: white !important;
    border: 2px dashed #1E3A8A !important;
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
# OCR FUNCTION
# ======================================================
def extract_math_from_image(image):
    img_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(img_gray)

    text = text.replace(" ", "").replace("dx", "")
    pattern = r"∫_?([-\d\.]+)\^([-\d\.]+)\(?([a-zA-Z0-9\+\-\*/\^\(\)x]+)\)?"
    match = re.search(pattern, text)

    if match:
        a = match.group(1)
        b = match.group(2)
        func = match.group(3).replace("^", "**")
        return func, a, b

    return None, None, None

# ======================================================
# JUDUL
# ======================================================
st.title("🔢 Kalkulator Integral Simbolik & Numerik")
st.subheader("Metode Pias Titik Tengah (Midpoint Rule)")

# ======================================================
# UPLOAD FOTO
# ======================================================
st.markdown("### 📷 Unggah Foto Soal Integral")
uploaded = st.file_uploader("Unggah gambar (.png / .jpg)", ["png", "jpg", "jpeg"])

auto_input = False
fungsi_str, a, b = "sin(x)+x**2", "0", "3"

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Gambar Soal", use_container_width=True)

    func_img, a_img, b_img = extract_math_from_image(img)

    if func_img:
        fungsi_str, a, b = func_img, a_img, b_img
        auto_input = True
        st.success("Soal berhasil dikenali dan dihitung otomatis.")
    else:
        st.warning("OCR gagal. Gunakan input manual.")

# ======================================================
# INPUT MANUAL
# ======================================================
fungsi_str = st.text_input("Fungsi f(x):", fungsi_str)
a = st.text_input("Batas bawah (a):", a)
b = st.text_input("Batas atas (b):", b)
n = st.number_input("Jumlah subinterval (n):", 1, 10000, 10)

# ======================================================
# PROSES
# ======================================================
if st.button("🔍 Hitung Integral") or auto_input:

    try:
        a_val, b_val = float(a), float(b)
    except:
        st.error("Batas tidak valid.")
        st.stop()

    x = sp.symbols("x")
    f_sym = sp.sympify(fungsi_str)
    f_num = sp.lambdify(x, f_sym, "numpy")

    h = (b_val - a_val) / n
    data, total = [], 0.0

    for i in range(n):
        xm = a_val + (i + 0.5) * h
        fxm = float(f_num(xm))
        area = fxm * h
        total += area
        data.append([i + 1, xm, fxm, area])

    df = pd.DataFrame(data, columns=["Iterasi", "x Tengah", "f(x)", "Luas Pias"])

    st.subheader("📌 Hasil")
    st.latex(r"\int f(x)\,dx = " + sp.latex(sp.integrate(f_sym, x)) + r" + C")
    st.latex(sp.latex(sp.integrate(f_sym, (x, a_val, b_val))))
    st.write(f"Pendekatan Numerik = **{total}**")

    st.subheader("📊 Tabel Iterasi")
    st.dataframe(df, use_container_width=True)

    xx = np.linspace(a_val, b_val, 400)
    yy = np.array(f_num(xx), dtype=float)
    mask = np.isfinite(yy)

    fig = make_subplots()
    fig.add_trace(go.Scatter(x=xx[mask], y=yy[mask], mode="lines", name="f(x)"))
    fig.update_layout(
        template="plotly_dark" if st.session_state.dark_mode else "plotly_white",
        title="Grafik Fungsi f(x)",
        xaxis_title="x",
        yaxis_title="f(x)"
    )

    st.plotly_chart(fig, use_container_width=True)
