# 📁 services/project_access.py
# This utility module centralizes project access control and analyst assignment UI.

import streamlit as st
from services.supabase_client import supabase

def fetch_projects_by_role(profile):
    """Return project list according to role-based access rules."""
    role = profile["role"]
    user_id = profile["auth_id"]

    if role == "Analyst":
        return supabase.table("projects").select("*").execute().data
    elif role == "IC":
        return supabase.table("projects").select("*").eq("status", "approved").execute().data
    elif role == "Project Owner":
        return supabase.table("projects").select("*").eq("created_by", user_id).execute().data
    else:
        return []

def display_assignment_ui_if_analyst(profile, project):
    """Render assignment dropdown for unassigned projects if user is Analyst."""
    if profile["role"] != "Analyst" or project.get("assigned_to"):
        return  # Skip if not eligible

    analyst_list = supabase.table("user_profiles").select("auth_id, username").eq("role", "Analyst").execute().data
    usernames = [a["username"] for a in analyst_list]
    selected_user = st.selectbox("Assign to Analyst", usernames, key=f"select_{project['id']}")

    if st.button("Assign", key=f"assign_{project['id']}"):
        assigned_id = next(a["auth_id"] for a in analyst_list if a["username"] == selected_user)
        supabase.table("projects").update({"assigned_to": assigned_id, "status": "in_review"}).eq("id", project["id"]).execute()
        st.success("✅ Project assigned.")

import streamlit as st
from services.supabase_client import supabase

# Get the current project ID from session state
def get_current_project_id():
    """Return the current project ID stored in session state."""
    return st.session_state.get("project_id", None)

# Fetch project details from the database by project ID
def get_project_by_id(project_id):
    """Fetch project data by ID from Supabase."""
    if not project_id:
        return None
    response = supabase.table("projects").select("*").eq("id", project_id).single().execute()
    return response.data



