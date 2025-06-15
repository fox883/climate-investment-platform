import streamlit as st
from services.utils import show_connection_status, goto_page
from services.style_utils import apply_global_style

apply_global_style(skip_config=True)
show_connection_status()

# --- Futuristic Banner with Gradient Overlay ---
st.markdown("""
    <div style="position:relative;height:300px;background:linear-gradient(to right, #001f3f, #0074D9);border-radius:10px;box-shadow:0 4px 20px rgba(0,0,0,0.2);margin-bottom:2rem;">
        <img src="https://images.unsplash.com/photo-1581090700227-1e8e601c2d4b?fit=crop&w=1400&q=80" style="width:100%;height:300px;object-fit:cover;border-radius:10px;opacity:0.3;position:absolute;top:0;left:0;z-index:0;" />
        <h1 style="position:absolute;top:50%;left:5%;transform:translateY(-50%);color:white;font-size:2.5em;z-index:1;font-weight:600;font-family:Segoe UI, sans-serif;">🌿 Climate Investment Platform</h1>
    </div>
""", unsafe_allow_html=True)

# --- Welcome Text ---
st.markdown("""
Welcome to the internal prototype of the **Carbon Investment Platform**.

This platform empowers climate finance stakeholders to explore, register, and evaluate carbon investment opportunities through a unified, secure interface. It is built to streamline project design, facilitate due diligence, and accelerate decision-making.

---
### 🛡️ Disclaimer
- This is a **prototype environment** under development.
- Data entered may be stored for testing and analysis.
- Unauthorized use is prohibited.
- Use implies acknowledgment of internal terms.
""")

# --- Access Button ---
st.markdown("---")
st.subheader("🔐 Access the Platform")

if st.button("🔐 Log In / Sign Up"):
    goto_page("login")  # Navigate to the combined login/signup page

# --- Footer ---
st.markdown("---")
st.caption("© 2025 Carbon Investment Platform – All rights reserved. Unauthorized use is strictly prohibited.")
