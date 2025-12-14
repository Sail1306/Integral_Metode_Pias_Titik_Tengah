import streamlit as st
import numpy as np

try:
    icon = Image.open("assets/icon.png")
except:
    icon = "📈"

st.set_page_config(
    page_title="Integral Solution (Pias Titik Tengah)",
    page_icon=icon,
    layout="centered",
    initial_sidebar_state="expanded"
)


# --- custom styles ---
st.markdown("""
    <style>
    body { overflow-x: hidden !important; }
    .stButton>button { width: 100%; background-color: #4CAF50; color: white; height: 3em; font-weight: bold; border-radius: 5px; }
    .stTextInput>div>div>input { color: #4CAF50; font-weight: bold; }
    h1, h2, h3 { color: #1565C0; text-align: center; }
    .highlight { background-color: #e8f5e9; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0; border-left: 5px solid #4CAF50; color: #2E7D32; font-size: 1.1em; font-weight: 500; }
    .result-box { background-color: #263238; color: #ECEFF1; padding: 1.5rem; border-radius: 0.5rem; border-left: 5px solid #FF9800; margin: 1rem 0; font-size: 1.1em; font-weight: bold; }
    .function-guide { background-color: #1a1a1a; color: #ffffff; padding: 1.5rem; border-radius: 0.5rem; border-left: 5px solid #4CAF50; margin: 1rem 0; }
    .angular-guide { background-color: #e8eaf6; padding: 1rem; border-radius: 4px; border-left: 4px solid #3f51b5; margin: 0.5rem 0; width: 100%; box-sizing: border-box; }
    .angular-button { width: 100%; margin: 0.2rem 0; }
    .code-text { font-family: monospace; background-color: #333333; padding: 0.2rem 0.4rem; border-radius: 3px; color: #4CAF50; }
    </style>
""", unsafe_allow_html=True)


# --------------------------
# Helper: Midpoint rule
# --------------------------
def midpoint_rule(f, a, b, n):
    """Composite midpoint rule. f expects scalar input and returns scalar."""
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x_mid = a + h * (i + 0.5)
        y = f(x_mid)
        total += y
    return total * h


# --------------------------
# NEW: Pias Titik Tengah
# --------------------------
def pias_titik_tengah(f, a, b, n):
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x_mid = a + (i + 0.5) * h
        total += f(x_mid)
    return total * h

# --------------------------
# Symbolic integration helpers (from your original code)
# --------------------------
def try_integration(expr, x):
    try:
        result = sp.integrate(expr, x, meijerg=True, risch=True)
        if result.has(sp.Integral):
            expr_str = str(expr)
            if 'sin(x**2)' in expr_str:
                S, C = sp.fresnels(x), sp.fresnelc(x)
                result = sp.sqrt(sp.pi/2) * (S + C)
            elif 'exp(-x**2)' in expr_str:
                result = sp.sqrt(sp.pi) * sp.erf(x) / 2
            else:
                simplified = sp.trigsimp(sp.apart(expr))
                result = sp.integrate(simplified, x)
                if result.has(sp.Integral):
                    raise ValueError("Direct integration failed")
        return result
    except:
        try:
            if isinstance(expr, sp.Basic):
                expr_str = str(expr)
                if 'sin(x**2)' in expr_str:
                    return sp.sqrt(sp.pi/2) * (sp.fresnels(x) + sp.fresnelc(x))
                elif 'exp(-x**2)' in expr_str:
                    return sp.sqrt(sp.pi) * sp.erf(x) / 2
            result = sp.integrate(expr, x, manual=True)
            if result.has(sp.Integral):
                raise ValueError("Manual integration failed")
            return result
        except:
            return None


def evaluate_special_function(expr_str, x_val):
    try:
        if 'sin(x**2)' in expr_str:
            s, c = special.fresnel(x_val)
            return np.sqrt(np.pi/2) * (s + c)
        elif 'exp(-x**2)' in expr_str:
            return np.sqrt(np.pi) * special.erf(x_val) / 2
        return None
    except:
        return None


def format_angle(value):
    if abs(value) < 1e-10:
        return "0"
    frac = value / np.pi
    if abs(frac - round(frac)) < 1e-10:
        if abs(frac) == 1:
            return "π" if frac > 0 else "-π"
        return f"{int(frac)}π"
    rational = sp.Rational(str(frac)).limit_denominator(12)
    num, den = rational.numerator, rational.denominator
    if abs(num) == 1:
        return f"π/{den}" if num > 0 else f"-π/{den}"
    return f"{num}π/{den}"


# --------------------------
# Plotting helper (uses plotly)
# --------------------------
def create_plot(x_vals, y_vals, expr_str, lower_limit, upper_limit):
    try:
        y_vals = np.asarray(y_vals, dtype=np.float64)
        fig = make_subplots()

        mask = np.isfinite(y_vals)

        fig.add_trace(go.Scatter(
            x=x_vals[mask],
            y=y_vals[mask],
            name="f(x)",
            line=dict(color='#2962FF', width=1.5),
            mode='lines',
            hovertemplate="<b>x</b>: %{x:.4f}<br><b>f(x)</b>: %{y:.4f}",
            hoverlabel=dict(bgcolor="#1565C0", font=dict(size=12, color='white'))
        ))

        fill_mask = (x_vals >= lower_limit) & (x_vals <= upper_limit) & np.isfinite(y_vals)
        if np.any(fill_mask):
            fig.add_trace(go.Scatter(
                x=x_vals[fill_mask],
                y=y_vals[fill_mask],
                fill='tozeroy',
                name="Integration Area",
                line=dict(color='#00C853'),
                fillcolor='rgba(0, 200, 83, 0.2)',
                hoverinfo='skip'
            ))

        fig.add_vline(x=lower_limit, line_width=2, line_dash="dash", line_color="red")
        fig.add_vline(x=upper_limit, line_width=2, line_dash="dash", line_color="red")

        fig.update_layout(
            title=dict(text=f"Integration of f(x) = {expr_str}", font=dict(size=14, color='#1565C0'), x=0.5),
            xaxis_title="x",
            yaxis_title="f(x)",
            hovermode='closest',
            dragmode='pan',
            showlegend=True,
            plot_bgcolor='white',
        )
        return fig

    except Exception:
        st.error("Error creating plot: The function might be undefined in some regions")
        return None

# --------------------------
# MAIN EXECUTION (UI + Logic)
# --------------------------

st.title("🔢 Kalkulator Integral (Simbolik & Numerik + Pias Titik Tengah)")

# Input user
expr_str = st.text_input("Masukkan fungsi f(x):", "sin(x)*cos(x)")
lower_limit = st.text_input("Batas bawah integral:", "0")
upper_limit = st.text_input("Batas atas integral:", "pi/2")
n_midpoint = st.number_input("Jumlah pias (untuk metode titik tengah):", min_value=1, value=10)


# Convert user inputs
try:
    a_val = float(sp.N(lower_limit))
    b_val = float(sp.N(upper_limit))
except:
    a_val, b_val = None, None
    st.error("Batas integral tidak valid.")


# Parse function
try:
    expr = sp.sympify(expr_str)
    f_lambdified = sp.lambdify(x, expr, modules=["numpy", "scipy"])
except:
    expr = None
    st.error("Fungsi tidak valid.")


# --------------------------
# NUMERICAL MIDPOINT RULE
# --------------------------
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
# Execute when button clicked
# --------------------------
if st.button("Hitung Integral"):

    if expr is None or a_val is None or b_val is None:
        st.error("Tidak dapat menghitung. Periksa input Anda.")
    else:
        st.subheader("📘 Hasil Perhitungan:")

        # symbolic integration
        symbolic_result = try_integration(expr, x)
        if symbolic_result is not None:
            st.success(f"Hasil integral simbolik:  
**∫ f(x) dx = {sp.simplify(symbolic_result)}**")
        else:
            st.warning("Integral simbolik tidak dapat diselesaikan oleh sistem.")

        # numerical evaluation using lambdify
        try:
            numeric_vals = [f_lambdified(t) for t in np.linspace(a_val, b_val, 2000)]
        except:
            numeric_vals = None
            st.error("Gagal menghitung nilai numerik fungsi.")

        # midpoint rule result
        midpoint_result = midpoint_rule(f_lambdified, a_val, b_val, n_midpoint)
        if midpoint_result is not None:
            st.info(f"Metode Pias Titik Tengah (n = {n_midpoint}):  
**≈ {midpoint_result}**")
        else:
            st.error("Perhitungan titik tengah gagal.")

        # If symbolic definite integral possible
        if symbolic_result is not None:
            try:
                definite_symbolic = symbolic_result.subs(x, b_val) - symbolic_result.subs(x, a_val)
                st.success(f"Hasil integral tentu secara simbolik:  
**≈ {float(definite_symbolic)}**")
            except:
                st.warning("Tidak dapat mengevaluasi integral tentu simbolik.")

        # plot
        if numeric_vals is not None:
            x_vals = np.linspace(a_val, b_val, 2000)
            fig = create_plot(x_vals, numeric_vals, expr_str, a_val, b_val)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
