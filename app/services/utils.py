import streamlit as st
from services.supabase_client import supabase

# fallback: prevent import error from switch_page
try:
    from streamlit_extras.switch_page_button import switch_page
except Exception:
    def switch_page(page_name):
        st.info(f"🔁 Please use the sidebar to go to '{page_name}'.")


def show_connection_status():
    try:
        ping = supabase.table("user_profiles").select("id").limit(1).execute()
        if ping.data is not None:
            st.success("✅ Connected to Supabase database.")
        else:
            st.warning("⚠️ Connected, but no data returned.")
    except Exception as e:
        st.error(f"❌ Supabase connection failed: {e}")
        st.stop()


def show_disclaimer():
    st.title("🌿 Climate Investment Platform")
    st.markdown("""
    Welcome to the internal prototype platform.  
    Please read carefully:
    - Only registered Fusers may access protected areas
    - All data interactions are logged
    - Do not share credentials or sensitive project data externally
    @Demo Xinzhi Yao
    """)


def require_login():
    if "auth_id" not in st.session_state:
        st.warning("🔒 Please log in to continue.")
        button_to("🔐 Go to Login", "login")
        st.stop()


def get_user_profile():
    if "auth_id" not in st.session_state:
        return None
    res = supabase.table("user_profiles").select("*").eq("auth_id", st.session_state["auth_id"]).single().execute()
    return res.data if res.data else None


def require_project():
    profile = get_user_profile()
    if not profile or not profile.get("project_id"):
        button_to("📋 Register Project", "project_register")
        st.stop()
    return profile["project_id"]


def logout_button():
    if st.button("🚪 Logout"):
        st.session_state.clear()
        button_to("🔐 Back to Login", "login")


def button_to(label: str, target_page: str):
    if st.button(label):
        st.success(f"👉 Please open **{target_page}** from the sidebar.")
        st.stop()
