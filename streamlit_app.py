import streamlit as st
import numpy as np

st.set_page_config(
    page_title="Integral Solution (Pias Titik Tengah)",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
# Style button
.stButton>button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}

# Warna teks input 
.stTextInput>div>div>input {
    font-weight: bold;
    color: green;
}

# Warna judul
h1, h2, h3 {
    text-align: center;
    color: #1565C0;
}

# Kotak highlight
.highlight {
    background-color: #e8f5e9;
    padding: 1rem;
    border-radius: 5px;
    border-left: 5px solid #4CAF50;
}

# Kotak hasil 
.result-box {
    background-color: #263238;
    color: white;
    padding: 1rem;
    border-radius: 5px;
    border-left: 5px solid orange;
}
</style>
""", unsafe_allow_html=True)

# Integrasi
def try_integration(expr, x):
    try:
        hasil = sp.integrate(expr, x, meijerg=True, risch=True)
        if hasil.has(sp.Integral):
            expr_str = str(expr)
            if "sin(x**2)" in expr_str:
                return sp.sqrt(sp.pi/2) * (sp.fresnels(x) + sp.fresnelc(x))
            if "exp(-x**2)" in expr_str:
                return sp.sqrt(sp.pi) * sp.erf(x) / 2
            # coba simplifikasi lain
            hasil = sp.integrate(sp.simplify(expr), x)
        return hasil
    except:
        # fallback sederhana
        try:
            return sp.integrate(expr, x, manual=True)
        except:
            return None


# Format PI
def format_angle(value):
    if abs(value) < 1e-10:
        return "0"
    k = value / np.pi
    if abs(k - round(k)) < 1e-10:
        if int(round(k)) == 1: return "π"
        if int(round(k)) == -1: return "-π"
        return f"{int(round(k))}π"
    frac = sp.Rational(str(k)).limit_denominator(12)
    return f"{frac.numerator}π/{frac.denominator}"

#  Plot
def create_plot(x_vals, y_vals, expr_str, a, b):
    try:
        fig = make_subplots()
        y_vals = np.array(y_vals, float)
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, name="f(x)",
                                 line=dict(color="#2962FF")))
        mask = (x_vals >= a) & (x_vals <= b)
        fig.add_trace(go.Scatter(
            x=x_vals[mask],
            y=y_vals[mask],
            fill='tozeroy',
            fillcolor='rgba(0,200,83,0.2)',
            name="Area"
        ))
        fig.update_layout(title=f"Grafik f(x) = {expr_str}")
        return fig
    except:
        st.error("Plot gagal ditampilkan")
        return None

# Main 
def main():

    st.title("Kalkulator Solusi Integral")
    st.title("Metode Pias Titik Tengah")

    st.markdown("""
    <div class='highlight'>
    <b>Welcome!</b> Aplikasi ini membantu menghitung integral tentu  
    dan tak tentu secara mudah. Dibuat oleh <b>Saila</b> ✨
    </div>
    """, unsafe_allow_html=True)

    input_col, guide_col = st.columns([2, 1])

# Kolom input
with input_col:
        st.markdown("### 📝 Masukkan Fungsi")
        expr_str = st.text_input("f(x):", "x**2")

        limit_type = st.radio("Jenis Input Limit:", ["Decimal", "Angular (π)"], horizontal=True)
    
# Batas bawah
col1, col2 = st.columns(2)
        with col1:
            if limit_type == "Decimal":
                a = st.number_input("Lower Limit", 0.0)
            else:
                s = st.text_input("Lower Limit", "0")
                try:
                    a = float(sp.sympify(s.replace("π", "pi")))
                except:
                    a = 0.0

# Batas atas
with col2:
            if limit_type == "Decimal":
                b = st.number_input("Upper Limit", 1.0)
            else:
                s2 = st.text_input("Upper Limit", "pi/2")
                try:
                    b = float(sp.sympify(s2.replace("π", "pi")))
                except:
                    b = np.pi/2

# Jumlah pias
n = st.number_input("Jumlah pembagian (n):", min_value=1, value=100)

