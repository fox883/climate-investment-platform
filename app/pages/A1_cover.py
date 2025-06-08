import streamlit as st
from services.supabase_client import supabase
from services.utils import logout_button, show_connection_status, button_to, require_login, get_user_profile

st.set_page_config(page_title="📄 Project Cover", page_icon="📄")

# --- Always show connection status ---
show_connection_status()

# --- Require login ---
require_login()

# --- Load user profile ---
profile = get_user_profile()
if not profile:
    st.error("❌ Failed to load user profile.")
    st.stop()

# --- Load selected project ID ---
project_id = st.session_state.get("project_id")
if not project_id:
    st.warning("⚠️ Please register a project first.")
    button_to("📋 Go to Project Setup", "project_register")
    st.stop()

# --- Display Profile Info ---
st.title("📄 Project Cover")
st.write(f"Welcome, **{profile['username']}**!")

st.subheader("Your Profile")
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**Username:** `{profile['username']}`")
    st.markdown(f"**Email:** `{profile['email']}`")
    st.markdown(f"**Role:** `{profile['role']}`")
with col2:
    st.markdown(f"**User ID:** `{profile['id']}`")
    st.markdown(f"**Auth ID:** `{profile['auth_id']}`")
    st.markdown(f"**Created At:** `{profile['created_at']}`")

st.markdown("---")

# --- Display Project ID ---
st.subheader("Linked Project")
st.markdown(f"**Project ID:** `{project_id}`")

st.markdown("---")

# --- Project Cover Form ---
st.subheader("📑 A1: Project Cover")
st.info("This section records your role and confirms platform disclaimer acceptance.")

with st.form("cover_form"):
    user_role = st.selectbox("Your Role", ["Project Owner", "Analyst", "Investment Committee"], index=0, disabled=True if profile['role'] else False)
    disclaimer_ack = st.checkbox("I acknowledge the platform disclaimer.")
    submitted = st.form_submit_button("💾 Save and Continue")

if submitted:
    try:
        result = supabase.table("project_cover").upsert({
            "project_id": project_id,
            "user_role": user_role,
            "disclaimer_ack": disclaimer_ack
        }).execute()
        if result.data:
            st.success("✅ Project cover saved.")
            st.balloons()
        else:
            st.error("❌ Failed to save project cover.")
    except Exception as e:
        st.error(f"❌ Submission error: {e}")

logout_button()
