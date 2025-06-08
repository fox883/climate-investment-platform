import streamlit as st
from services.supabase_client import supabase
from services.utils import logout_button, show_connection_status, button_to, require_login, get_user_profile

st.set_page_config(page_title="📊 Dashboard", page_icon="📊")

# --- Always show connection status ---
show_connection_status()

# --- Require login ---
require_login()

# --- Load user profile ---
profile = get_user_profile()
if not profile:
    st.error("❌ Failed to load user profile.")
    st.stop()

# --- Display Profile Info ---
st.title("📊 Dashboard")
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

# --- Display Projects ---
st.markdown("---")
st.subheader("Project Status")
try:
    projects = supabase.table("projects").select("id, project_name, project_type, country, status").eq("created_by", profile["auth_id"]).execute()
    if projects.data:
        for idx, project in enumerate(projects.data):
            with st.expander(f"📌 {project['project_name']}"):
                st.markdown(f"**Type:** `{project['project_type']}`")
                st.markdown(f"**Country:** `{project['country']}`")
                st.markdown(f"**Status:** `{project['status']}`")
                if st.button("➡️ Open Project Cover", key=f"btn_{project['id']}"):
                    st.session_state["project_id"] = project["id"]
                    st.switch_page("pages/A1_cover.py")
    else:
        st.info("📝 No project registered yet.")
        button_to("📋 Register a Project", "project_register")
except Exception as e:
    st.error(f"❌ Failed to load project details: {e}")

logout_button()
