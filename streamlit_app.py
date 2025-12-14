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
limit_col1, limit_col2 = st.columns(2)
with limit_col1:
            if limit_type == "Decimal":
                lower_limit = st.number_input('Lower Limit:', value=0.0, step=0.1, format="%.4f")
            else:
                lower_limit_str = st.text_input('Lower Limit:', value="0", help="Enter as multiples of π (e.g., pi/2, -pi)")
                try:
                    expr_val = lower_limit_str.replace('π', 'pi')
                    lower_limit = float(sp.sympify(expr_val).evalf())
                except:
                    st.error("Invalid input. Examples: pi/2, -pi, 1, 0.5")
                    lower_limit = 0.0

# Batas atas
with limit_col2:
            if limit_type == "Decimal":
                upper_limit = st.number_input('Upper Limit:', value=1.0, step=0.1, format="%.4f")
            else:
                upper_limit_str = st.text_input('Upper Limit:', value="pi/2", help="Enter as multiples of π (e.g., pi/2, -pi)")
                try:
                    expr_val = upper_limit_str.replace('π', 'pi')
                    upper_limit = float(sp.sympify(expr_val).evalf())
                except:
                    st.error("Invalid input. Examples: pi/2, -pi, 1, 0.5")
                    upper_limit = np.pi / 2

# Jumlah pias
n = st.number_input(
    "Jumlah Pembagian (n):",
    min_value=1,
    value=100,
    step=1,
    help="Semakin besar n, semakin akurat (tapi lebih lama komputasinya)."
)

# Guide
with guide_col:
        st.markdown("""
        <div class='function-guide' style='padding: 1rem; margin-bottom: 0.5rem;'>
        <h3 style='margin-bottom: 0.5rem; font-size: 1.1em;'>💡 Quick Examples:</h3>
        <ul style='list-style-type: none; padding-left: 0; margin-bottom: 0;'>
            <li style='margin-bottom: 5px; font-size: 0.8em;'>📊 Basic <span class='code-text'>x**2</span></li>
            <li style='margin-bottom: 5px; font-size: 0.8em;'>📐 Trigonometric <span class='code-text'>sin(x)</span></li>
            <li style='margin-bottom: 5px; font-size: 0.8em;'>📈 Exponential <span class='code-text'>exp(-x)</span></li>
            <li style='margin-bottom: 5px; font-size: 0.8em;'>🔄 Complex <span class='code-text'>sin(x**2)</span></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📚 Function Guide", expanded=False):
            st.markdown("""
            <div class='function-guide'>
            <h3>🔢 Basic Operations</h3>
            • Addition: <span class='code-text'>+</span> (x + 1)<br>
            • Multiplication: <span class='code-text'>*</span> (2*x)<br>
            • Power: <span class='code-text'>**</span> (x**2)<br>
            • Division: <span class='code-text'>/</span> (x/2)<br>
            <h3>🎯 Advanced Functions</h3>
            • Trig: <span class='code-text'>sin(x)</span>, <span class='code-text'>cos(x)</span><br>
            • Exp/Log: <span class='code-text'>exp(x)</span>, <span class='code-text'>log(x)</span><br>
            <h3>🎲 Special</h3>
            • Fresnel: <span class='code-text'>sin(x**2)</span><br>
            • Error func: <span class='code-text'>exp(-x**2)</span><br>
            <h3>Constants</h3> • π: <span class='code-text'>pi</span> • e: <span class='code-text'>E</span>
            </div>
            """, unsafe_allow_html=True)

# Button hitung
colA, colB, colC = st.columns([1, 2, 1])
    hitung = colB.button("🔢 Calculate Integral")

    if not hitung:
        return

    if a >= b:
        st.error("Upper limit harus lebih besar dari lower limit")
        return

x = symbols('x')
try:
    expr = sympify(expr_str)
except:
    st.error("Fungsi tidak valid!")
    return

try:
        f_num = sp.lambdify(x, expr, 'numpy')
    except:
        st.error("Fungsi tidak bisa diubah menjadi bentuk numerik")
        return

xs = np.linspace(a - (b - a)*0.2, b + (b - a)*0.2, 600)
    try:
        ys = f_num(xs)
    except:
        st.error("Gagal menghitung grafik fungsi")
        return

fig = create_plot(xs, ys, expr_str, a, b)
    if fig:
        st.plotly_chart(fig, use_container_width=True)

    sim = try_integration(expr, x)
    if sim is not None:
        st.markdown(f"### Indefinite Integral\n$$ \\int {sp.latex(expr)} dx = {sp.latex(sim)} + C $$")
    else:
        st.warning("Integral simbolik tidak ditemukan")

    def f_scalar(t):
        val = f_num(t)
        if isinstance(val, (np.ndarray, list, tuple)):
            return float(np.array(val).flatten()[0])
        return float(val)

    hasil = midpoint_rule(f_scalar, a, b, int(n))
