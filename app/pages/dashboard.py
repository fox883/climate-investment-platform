import streamlit as st
st.set_page_config(page_title="📊 Dashboard", page_icon="📊")  # MUST BE FIRST

from services.supabase_client import supabase
from services.utils import logout_button, show_connection_status, button_to, require_login, get_user_profile, goto_page
from services.style_utils import apply_global_style
from services.project_access import fetch_projects_by_role
from services.project_display import enrich_project_with_user_info, display_project_card
from services.assignment_utils import assign_user_to_project

apply_global_style(skip_config=True)
show_connection_status()

# --- Require login ---
require_login()

# --- Load user profile ---
profile = get_user_profile()
if not profile:
    st.error("⚠️ User profile not found. Please try logging in again.")
    if st.button("🔐 Go to Login"):
        goto_page("login")
    st.stop()

# --- Display Profile Info ---
from services.utils import show_user_profile

st.title("📊 Dashboard")
st.success(f"Welcome, **{profile['username']}**!")

show_user_profile(profile)

# --- Display Projects ---
st.markdown("---")
st.subheader("📁 Project Status")

try:
    projects = fetch_projects_by_role(profile)

    if projects:
        for idx, project in enumerate(projects):
            project = enrich_project_with_user_info(project)
            display_project_card(project, profile)  # ✅ Fixed: pass profile

            # Show universal assignment interface for Analyst role
            assign_user_to_project(
                project,
                profile,
                role_to_assign="Analyst",
                column_name="assigned_to",
                label="Assign to Analyst",
                status_on_assign="in_review"
            )
    else:
        st.info("📝 No project registered yet.")
        if st.button("📋 Register a Project"):
            goto_page("register")

except Exception as e:
    st.error(f"❌ Failed to load project details: {e}")

logout_button()
st.markdown("---")
st.subheader("Want to register another project?")
if st.button("➕ Register New Project"):
    goto_page("register")
