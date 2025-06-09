import streamlit as st
from services.supabase_client import supabase
from services.utils import goto_page
from services.utils import logout_button
from services.utils import (
    logout_button,
    show_connection_status,
    button_to,
    require_login,
    get_user_profile,
    show_user_profile,
)

st.set_page_config(page_title="📄 Project Cover", page_icon="📄")

# --- Always show connection status ---
show_connection_status()

# --- Require login ---
require_login()

# --- Load user profile ---
try:
    profile = get_user_profile()
    if not profile:
        st.error("⚠️ User profile not found. Please try logging in again.")
        button_to("🔐 Go to Login", "login")
        st.stop()
except Exception as e:
    st.error(f"❌ Failed to load user profile: {e}")
    st.stop()

# --- Load selected project ID ---
project_id = st.session_state.get("project_id")
if not project_id:
    st.warning("⚠️ No project ID in session.")
    button_to("📋 Go to Project Setup", "project_register")
    st.stop()

# --- Display Profile Info ---
st.title("📄 Project Cover")
st.write(f"Welcome, **{profile['username']}**!")

st.subheader("Your Profile")
show_user_profile(profile)

st.markdown("---")

# --- Project Cover Form ---
st.subheader("📑 A1: Project Cover")
st.info("This section records your role and confirms platform disclaimer acceptance.")

with st.form("cover_form"):
    user_role = profile['role']
    st.markdown(f"**Your Role:** `{user_role}`")
    disclaimer_ack = st.checkbox("I acknowledge the platform disclaimer.")
    submitted = st.form_submit_button("💾 Save and Continue")

if submitted:
    try:
        result = supabase.table("project_cover").upsert({
            "project_id": project_id,
            "user_role": user_role,
            "disclaimer_ack": disclaimer_ack
        }).execute()

        if result.data:
            st.success("✅ Project cover saved.")
            st.balloons()

            # Store the project_id in session state to pass it to the next page
            st.session_state["project_id"] = project_id

            # Redirect to the next page (B1_B3: Financial & Risk Snapshot)
            goto_page("B1_B3_financial_risk")

        else:
            st.error("❌ Failed to save project cover.")
    except Exception as e:
        st.error(f"❌ Submission error: {e}")

logout_button()