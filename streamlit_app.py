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
