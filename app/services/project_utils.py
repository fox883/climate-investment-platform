import streamlit as st
from services.supabase_client import supabase

# Get current project ID from session state
def get_current_project_id():
    return st.session_state.get("project_id", None)

# Fetch project details by ID
def get_project_by_id(project_id):
    if not project_id:
        return None
    response = supabase.table("projects").select("*").eq("id", project_id).single().execute()
    return response.data

# Enrich project with user details (creator, assigned analyst, etc.)
def enrich_project_with_user_info(project):
    user_ids = filter(None, [project.get("created_by"), project.get("assigned_to")])
    profiles = supabase.table("user_profiles").select("auth_id, username, company").in_("auth_id", list(user_ids)).execute().data

    project["creator_name"] = next((u["username"] for u in profiles if u["auth_id"] == project.get("created_by")), None)
    project["creator_company"] = next((u["company"] for u in profiles if u["auth_id"] == project.get("created_by")), None)
    project["assigned_name"] = next((u["username"] for u in profiles if u["auth_id"] == project.get("assigned_to")), None)
    return project
