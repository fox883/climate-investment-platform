import streamlit as st
from services.supabase_client import supabase
from services.utils import require_login, get_user_profile, logout_button, show_connection_status, button_to
from uuid import uuid4

st.set_page_config(page_title="Register Project", page_icon="📝")

# --- Always show Supabase connection status ---
show_connection_status()

# --- Refresh Auth User Session ---
session = supabase.auth.get_session()
if session and session.user:
    st.session_state["auth_id"] = session.user.id
    st.session_state["email"] = session.user.email
else:
    st.warning("🔒 Session expired. Please log in again.")
    button_to("🔐 Go to Login", "login")
    st.stop()

# --- Session Check ---
require_login()

# --- Load User Profile ---
user_profile = get_user_profile()
if not user_profile:
    st.error("⚠️ User profile not found. Please try logging in again.")
    button_to("🔐 Go to Login", "login")
    st.stop()

logout_button()

# --- Check if project already exists ---
if user_profile.get("project_id"):
    st.success("✅ Project already registered. Go to dashboard.")
    button_to("📊 Go to Dashboard", "main_dashboard")
    st.stop()

# --- Register New Project ---
st.markdown("---")
st.subheader("📋 Register Your Project")
project_name = st.text_input("Project Name")
project_type = st.selectbox("Project Type", ["Afforestation", "REDD+", "Biochar", "Mangrove", "Other"])
country = st.text_input("Country")
user_role = st.selectbox("User Role", ["Project Owner", "Analyst", "Investment Committee"])
disclaimer_ack = st.checkbox("I acknowledge the platform disclaimer.")
status = "draft"

if st.button("Submit Project"):
    project_id = str(uuid4())
    try:
        # Insert to 'projects' table
        supabase.table("projects").insert({
            "id": project_id,
            "project_name": project_name,
            "project_type": project_type,
            "country": country,
            "status": status,
            "created_by": st.session_state["auth_id"]
        }).execute()

        # Insert to 'project_cover' table
        supabase.table("project_cover").insert({
            "project_id": project_id,
            "user_role": user_role,
            "disclaimer_ack": disclaimer_ack
        }).execute()

        # Update user profile
        supabase.table("user_profiles").update({"project_id": project_id}).eq("auth_id", st.session_state["auth_id"]).execute()

        st.session_state["project_id"] = project_id
        st.success("✅ Project registered successfully!")
        button_to("📊 Go to Dashboard", "main_dashboard")

    except Exception as e:
        st.error(f"❌ Project registration failed: {e}")
