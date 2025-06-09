import streamlit as st
from services.supabase_client import supabase

def enrich_project_with_user_info(project):
    """Enrich the project with user information like creator and assigned analyst."""
    user_ids = filter(None, [project.get("created_by"), project.get("assigned_to")])
    profiles = supabase.table("user_profiles").select("auth_id, username, company").in_("auth_id", list(user_ids)).execute().data

    project["creator_name"] = next((u["username"] for u in profiles if u["auth_id"] == project.get("created_by")), None)
    project["creator_company"] = next((u["company"] for u in profiles if u["auth_id"] == project.get("created_by")), None)
    project["assigned_name"] = next((u["username"] for u in profiles if u["auth_id"] == project.get("assigned_to")), None)
    return project

def display_project_card(project, profile=None):  # profile stays for context if needed
    """Display a card-style UI with project details."""
    with st.expander(f"📌 {project['project_name']}"):
        st.markdown(f"**Type:** `{project['project_type']}`")
        st.markdown(f"**Country:** `{project['country']}`")
        st.markdown(f"**Status:** `{project['status']}`")

        if project.get("creator_name"):
            st.markdown(f"**Submitted By:** `{project['creator_name']}`")
        if project.get("creator_company"):
            st.markdown(f"**Organization:** `{project['creator_company']}`")
        if project.get("assigned_name"):
            st.markdown(f"**Assigned Analyst:** `{project['assigned_name']}`")

        if st.button("➡️ Open Project Cover", key=f"btn_{project['id']}"):
            st.session_state["project_id"] = project["id"]
            st.switch_page("pages/A1_cover.py")


import streamlit as st

def show_user_profile(profile):
    """Display user profile information in a clean format."""
    st.markdown(f"**Username:** {profile.get('username')}")
    st.markdown(f"**Email:** {profile.get('email')}")
    st.markdown(f"**Role:** {profile.get('role')}")
    st.markdown(f"**Organization:** {profile.get('organization', 'N/A')}")
