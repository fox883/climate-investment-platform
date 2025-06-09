import streamlit as st
from services.supabase_client import supabase

# Force Streamlit-native navigation fallback instead of message
try:
    from streamlit_extras.switch_page_button import switch_page
except ImportError:
    def switch_page(page_name):
        st.session_state["_redirect"] = page_name
        st.experimental_rerun()

# Redirection handler — run this in app.py or at top of each page
if "_redirect" in st.session_state:
    import os
    target = st.session_state.pop("_redirect")
    if not target.endswith(".py"):
        target += ".py"
    full_path = os.path.join("pages", target)
    if os.path.exists(full_path):
        st.switch_page(full_path)
    else:
        st.error(f"❌ Page '{target}' not found in /pages directory.")


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
        if st.button("🔐 Go to Login"):
            goto_page("login")
        st.stop()


def get_user_profile():
    if "auth_id" not in st.session_state:
        return None
    res = supabase.table("user_profiles") \
        .select("*") \
        .eq("auth_id", st.session_state["auth_id"]) \
        .limit(1) \
        .execute()
    return res.data[0] if res.data else None



def require_project():
    profile = get_user_profile()
    if not profile or not profile.get("project_id"):
        if st.button("📋 Register Project"):
            goto_page("register")
        st.stop()
    return profile["project_id"]


def logout_button():
    if st.button("🚪 Logout"):
        st.session_state.clear()
        goto_page("login")


# Define a consistent mapping of page keys to filenames
# Define a consistent mapping of page keys to filenames
PAGE_MAP = {
    "main": "pages/main.py",  # Add this for main entry point
    "login": "pages/login.py",
    "dashboard": "pages/dashboard.py",
    "register": "pages/project_register.py",
    "cover": "pages/A1_cover.py",  # Project Cover
    "B1_B3_financial_risk": "pages/B1_B3_financial_risk.py",  # Financial & Risk Snapshot
    "C1_C3_impact_compliance": "pages/C1_C3_impact_compliance.py",  # Impact & Compliance
    "thank_you": "pages/thankyou.py"
}



def goto_page(key):
    if key in PAGE_MAP:
        st.switch_page(PAGE_MAP[key])
    else:
        st.error(f"❌ Unknown page key: '{key}' — check PAGE_MAP in utils.py")


# Optional: legacy support cleanup for pages still importing button_to
# This will avoid ImportError while you clean references

def button_to(label, target_page):
    if st.button(label):
        goto_page(target_page)

def show_user_profile(profile):
    st.subheader("👤 Your Profile")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Username:** `{profile['username']}`")
        st.markdown(f"**Email:** `{profile['email']}`")
        st.markdown(f"**Role:** `{profile['role']}`")
        st.markdown(f"**Company:** `{profile.get('company', 'N/A')}`")
    with col2:
        st.markdown(f"**User ID:** `{profile['id']}`")
        st.markdown(f"**Auth ID:** `{profile['auth_id']}`")
        st.markdown(f"**Created At:** `{profile['created_at']}`")



