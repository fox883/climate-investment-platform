import streamlit as st
from services.utils import switch_page  # make sure this is included

# Redirection trigger (already in canvas)
if "_redirect" in st.session_state:
    import os
    target = st.session_state.pop("_redirect")
    if not target.endswith(".py"):
        target += ".py"
    full_path = os.path.join("pages", target)
    if os.path.exists(full_path):
        st.switch_page(full_path)
    else:
        st.error(f"❌ Page '{target}' not found in /pages directory.")

st.markdown("---")
st.subheader("🔐 Access the Platform")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔓 Log In"):
        from services.utils import goto_page
        goto_page("login")

with col2:
    if st.button("📝 Sign Up"):
        from services.utils import goto_page
        goto_page("signup")  # you’ll need to create pages/signup.py if not already present
