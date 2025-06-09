import streamlit as st
from services.supabase_client import supabase

def assign_user_to_project(
    project,
    profile,
    role_to_assign="Analyst",
    column_name="assigned_to",
    label="Assign to Analyst",
    status_on_assign="in_review"
):
    if profile["role"] != "Analyst" or project.get(column_name):
        return

    users = supabase.table("user_profiles").select("auth_id, username").eq("role", role_to_assign).execute().data
    usernames = [u["username"] for u in users]
    selected_user = st.selectbox(label, usernames, key=f"select_{project['id']}")

    if st.button(f"Assign {role_to_assign}", key=f"assign_{project['id']}"):
        user_id = next(u["auth_id"] for u in users if u["username"] == selected_user)
        update_payload = {column_name: user_id}
        if status_on_assign:
            update_payload["status"] = status_on_assign
        supabase.table("projects").update(update_payload).eq("id", project["id"]).execute()
        st.success(f"✅ {role_to_assign} assigned to {selected_user}.")
