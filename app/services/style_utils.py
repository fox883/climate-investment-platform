import streamlit as st

# Reusable Styling Function for Modern UI

def apply_global_style(skip_config=False):
    if not skip_config:
        st.set_page_config(page_title="Carbon Platform", page_icon="🌿", layout="centered")
    st.markdown("""
        <style>
        html, body, .main, .block-container {
            background-color: #f5f7fa;
            font-family: 'Inter', sans-serif;
            color: #2c3e50;
        }
        .block-container {
            padding: 3rem 3rem 2rem 3rem;
            background-color: #ffffff;
            border-radius: 14px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
        }
        h1, h2, h3, h4, h5 {
            color: #102a43;
        }
        .stButton button {
            background-color: #1a4f8b;
            color: #ffffff;
            border-radius: 8px;
            padding: 0.65em 1.4em;
            font-weight: 600;
            border: none;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #256cc0;
        }
        .stTextInput>div>div>input {
            border-radius: 6px;
        }
        .stSelectbox>div>div {
            border-radius: 6px;
        }
        </style>
    """, unsafe_allow_html=True)
