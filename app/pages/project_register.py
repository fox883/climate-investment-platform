import streamlit as st
st.set_page_config(page_title="Register Project", page_icon="📝")  # MUST BE FIRST

from services.supabase_client import supabase
from services.utils import require_login, get_user_profile, logout_button, show_connection_status, goto_page, switch_page
from services.style_utils import apply_global_style
from uuid import uuid4

apply_global_style(skip_config=True)

# --- Always show Supabase connection status ---
show_connection_status()

# --- Require login and refresh session ---
require_login()
session = supabase.auth.get_session()
if session and session.user:
    st.session_state["auth_id"] = session.user.id
    st.session_state["email"] = session.user.email
else:
    st.warning("🔒 Session expired. Please log in again.")
    if st.button("🔐 Go to Login"):
        goto_page("login")
    st.stop()

# --- Load User Profile ---
profile = get_user_profile()
if not profile:
    st.error("⚠️ User profile not found. Please try logging in again.")
    if st.button("🔐 Go to Login"):
        switch_page("pages/login.py")
    st.stop()

# --- Display User Profile Header ---
from services.utils import show_user_profile
show_user_profile(profile)

logout_button()

# --- Register New Project Form ---
st.markdown("---")
st.subheader("📋 Register Your Project")
project_name = st.text_input("Project Name")
project_type = st.selectbox("Project Type", ["Afforestation", "REDD+", "Biochar", "Mangrove", "Other"])
country = st.text_input("Country")
user_role = profile["role"]
st.markdown(f"**User Role:** `{user_role}`")  # display only
disclaimer_ack = st.checkbox("I acknowledge the platform disclaimer.")
status = "draft"

if st.button("Submit Project"):
    project_id = str(uuid4())
    try:
        # Insert into 'projects' table
        supabase.table("projects").insert({
            "id": project_id,
            "project_name": project_name,
            "project_type": project_type,
            "country": country,
            "status": status,
            "created_by": st.session_state["auth_id"]
        }).execute()

        # Insert into 'project_cover' table
        response = supabase.table("project_cover").insert({
            "project_id": project_id,
            "user_role": user_role,
            "disclaimer_ack": disclaimer_ack
        }).execute()

        if response.data is None:
            st.error("❌ Failed to save project cover.")
        else:
            st.success("✅ Project cover saved successfully.")
            st.code(f"🔑 Project ID: {project_id}")
            st.session_state["project_id"] = project_id

            # Redirect to dashboard
            goto_page("dashboard")

    except Exception as e:
        st.error(f"❌ Project registration failed: {e}")


