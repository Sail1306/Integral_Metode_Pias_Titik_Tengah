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

/* Membuat tombol lebih rapi */
.stButton>button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
}

/* Warna teks pada input */
.stTextInput>div>div>input {
    font-weight: bold;
    color: green;
}

/* Warna judul */
h1, h2, h3 {
    text-align: center;
    color: #1565C0;
}

/* Kotak highlight sederhana */
.highlight {
    background-color: #e8f5e9;
    padding: 1rem;
    border-radius: 5px;
    border-left: 5px solid #4CAF50;
}

/* Kotak hasil */
.result-box {
    background-color: #263238;
    color: white;
    padding: 1rem;
    border-radius: 5px;
    border-left: 5px solid orange;
}

</style>
""", unsafe_allow_html=True)

