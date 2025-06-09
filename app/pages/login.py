import streamlit as st
st.set_page_config(page_title="User Login / Sign Up", page_icon="🔐")  # MUST BE FIRST

from services.supabase_client import supabase
from services.user_data import create_user_profile
from services.utils import button_to
import time
from services.style_utils import apply_global_style
apply_global_style(skip_config=True)

# --- Connection Status ---
try:
    supabase.table("user_profiles").select("id").limit(1).execute()
    st.success("✅ Connected to Supabase database.")
except Exception as e:
    st.error("❌ Supabase connection failed.")
    st.stop()

# --- Toggle Login/Sign Up ---
mode = st.radio("Choose action", ["Log In", "Sign Up"], horizontal=True)
st.markdown("---")

# --- Login Form ---
if mode == "Log In":
    st.subheader("🔐 Enter your credentials")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    login_clicked = st.button("Log In")
    login_successful = False

    if login_clicked:
        try:
            result = supabase.auth.sign_in_with_password({
                "email": login_email,
                "password": login_password
            })
            if result.user:
                login_successful = True
                st.session_state["auth_id"] = result.user.id
                st.session_state["email"] = login_email
        except Exception as e:
            login_successful = False

        if login_successful:
            st.success("✅ Login successful! Redirecting...")
            time.sleep(1)
            st.switch_page("pages/dashboard.py")
        else:
            st.error("❌ Invalid login credentials or login error.")

# --- Sign Up Form ---
elif mode == "Sign Up":
    st.subheader("📝 Register a new account")
    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        try:
            supabase.auth.sign_up({
                "email": signup_email,
                "password": signup_password
            })
            result = supabase.auth.sign_in_with_password({
                "email": signup_email,
                "password": signup_password
            })

            if result.user:
                st.session_state["auth_id"] = result.user.id
                st.session_state["email"] = signup_email
                st.success("✅ Registration and login successful!")
            else:
                st.error("❌ Sign-up failed. Try again.")

        except Exception as e:
            st.error("❌ Sign-up error")

    # --- Profile Completion (only for Sign Up) ---
    if "auth_id" in st.session_state:
        st.info("Complete your profile below.")

        username = st.text_input("Enter your Full Name", key="profile_username")
        st.caption("Please enter your full name in the format: First Name, Last Name")
        company_name = st.text_input("Enter your Company Name", key="profile_company")
        st.caption("Please enter the full registered company name.")

        role = st.selectbox("Select your role", ["Project Owner", "Analyst", "IC"], key="profile_role")

        if role == "Analyst":
            pin = st.text_input("🔐 Enter internal PIN for Analyst role", type="password")
            if pin != "1234":
                st.warning("❌ Invalid PIN. Analyst role is for internal registration only.")
                st.stop()

        if role == "IC":
            pin = st.text_input("🔐 Enter internal PIN for Analyst role", type="password")
            if pin != "1234":
                st.warning("❌ Invalid PIN. Analyst role is for internal registration only.")
                st.stop()

        if st.button("Save Profile"):
            try:
                # Check if profile already exists for this auth_id
                existing = supabase.table("user_profiles").select("id").eq("auth_id", st.session_state["auth_id"]).execute()
                if existing.data:
                    st.warning("⚠️ Profile already exists for this user.")
                else:
                    profile_result = create_user_profile(
                        auth_id=st.session_state["auth_id"],
                        email=st.session_state["email"],
                        username=username,
                        role=role
                    )

                    if profile_result.data:
                        st.success("✅ Profile saved to user_profiles table. Redirecting...")
                        time.sleep(1)
                        st.switch_page("pages/project_register.py")
                    else:
                        st.error("❌ Insert failed.")
            except Exception as e:
                st.error("❌ Insert error")
