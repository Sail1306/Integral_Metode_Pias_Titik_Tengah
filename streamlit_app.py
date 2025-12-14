import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go

# -------------------------------------------------------------------
# PART 1 — CSS & UI (DARI ANDA, TIDAK ADA YANG DIUBAH)
# -------------------------------------------------------------------
st.markdown("""
<style>
body { overflow-x: hidden !important; }

.stButton>button { 
    width: 100%; 
    background-color: #4CAF50; 
    color: white; 
    height: 3em; 
    font-weight: bold; 
    border-radius: 5px; 
}

.stTextInput>div>div>input { 
    color: #4CAF50; 
    font-weight: bold; 
}

h1, h2, h3 { 
    color: #1565C0; 
    text-align: center; 
}

.highlight { 
    background-color: #e8f5e9; 
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    margin: 1rem 0; 
    border-left: 5px solid #4CAF50; 
    color: #2E7D32; 
    font-size: 1.1em; 
    font-weight: 500; 
}

.result-box { 
    background-color: #263238; 
    color: #ECEFF1; 
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    border-left: 5px solid #FF9800; 
    margin: 1rem 0; 
    font-size: 1.1em; 
    font-weight: bold; 
}

.function-guide { 
    background-color: #1a1a1a; 
    color: #ffffff; 
    padding: 1.5rem; 
    border-radius: 0.5rem; 
    border-left: 5px solid #4CAF50; 
    margin: 1rem 0; 
}

.angular-guide { 
    background-color: #e8eaf6; 
    padding: 1rem; 
    border-radius: 4px; 
    border-left: 4px solid #3f51b5; 
    margin: 0.5rem 0; 
    width: 100%; 
    box-sizing: border-box; 
}

.angular-button { 
    width: 100%; 
    margin: 0.2rem 0; 
}

.code-text { 
    font-family: monospace; 
    background-color: #333333; 
    padding: 0.2rem 0.4rem; 
    border-radius: 3px; 
    color: #4CAF50; 
}
</style>
""", unsafe_allow_html=True)


# -------------------------------------------------------------------
# PART 2 — FUNGSI PENDUKUNG
# -------------------------------------------------------------------

x = sp.Symbol("x")

# symbolic integration with fail-safety
def try_integration(expr, var):
    try:
        return sp.integrate(expr, var)
    except:
        return None

# plot generator
def create_plot(xs, ys, expr_str, a, b):
    try:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=xs, y=ys, mode='lines', name="f(x)"))
        fig.update_layout(
            title=f"Grafik f(x) = {expr_str}",
            xaxis_title="x",
            yaxis_title="f(x)",
            template="plotly_dark"
        )
        return fig
    except:
        return None


# -------------------------------------------------------------------
# PART 3 — MAIN EXECUTION + METODE PIAS TITIK TENGAH
# -------------------------------------------------------------------

st.title("🔢 Kalkulator Integral (Simbolik & Numerik + Pias Titik Tengah)")

# Input user
expr_str = st.text_input("Masukkan fungsi f(x):", "sin(x)*cos(x)")
lower_limit = st.text_input("Batas bawah integral:", "0")
upper_limit = st.text_input("Batas atas integral:", "pi/2")
n_midpoint = st.number_input("Jumlah pias (untuk metode titik tengah):", min_value=1, value=10)

# Convert input numeric
try:
    a_val = float(sp.N(lower_limit))
    b_val = float(sp.N(upper_limit))
except:
    a_val, b_val = None, None
    st.error("Batas integral tidak valid.")


# Parsing fungsi
try:
    expr = sp.sympify(expr_str)
    f_lambdified = sp.lambdify(x, expr, modules=["numpy"])
except:
    expr = None
    st.error("Fungsi tidak valid.")


# MIDPOINT RULE
def midpoint_rule(func, a, b, n):
    try:
        h = (b - a) / n
        total = 0
        for i in range(n):
            mid = a + (i + 0.5) * h
            total += func(mid)
        return total * h
    except:
        return None


# --------------------------
# BUTTON – EXECUTION
# --------------------------
if st.button("Hitung Integral"):

    if expr is None or a_val is None or b_val is None:
        st.error("Tidak dapat menghitung. Periksa input Anda.")
    else:
        st.subheader("📘 Hasil Perhitungan:")

        # Symbolic
        symbolic_result = try_integration(expr, x)
        if symbolic_result is not None:
            sst.success(
    f"Integral umum: ∫ f(x) dx = {sp.simplify(symbolic_result)}"
)
        else:
            st.warning("Integral simbolik tidak dapat diselesaikan sistem.")

        # Numerical values
        try:
            xs = np.linspace(a_val, b_val, 2000)
            ys = [f_lambdified(xx) for xx in xs]
        except:
            xs, ys = None, None
            st.error("Gagal menghitung nilai fungsi.")

        # MIDPOINT result
        midpoint_result = midpoint_rule(f_lambdified, a_val, b_val, n_midpoint)
        if midpoint_result is not None:
            st.info(f"Hasil Metode Pias Titik Tengah (n = {n_midpoint}):  
**≈ {midpoint_result}**")
        else:
            st.error("Perhitungan titik tengah gagal.")

        # Symbolic definite
        if symbolic_result is not None:
            try:
                definite = symbolic_result.subs(x, b_val) - symbolic_result.subs(x, a_val)
                st.success(f"Integral tentu simbolik:  
**≈ {float(definite)}**")
            except:
                st.warning("Integral tentu simbolik tidak dapat dievaluasi.")

        # Plot
        if xs is not None:
            fig = create_plot(xs, ys, expr_str, a_val, b_val)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
