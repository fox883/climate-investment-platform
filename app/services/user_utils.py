import streamlit as st

# Show user profile information in the UI
def show_user_profile(profile):
    st.markdown(f"**Username:** {profile.get('username')}")
    st.markdown(f"**Email:** {profile.get('email')}")
    st.markdown(f"**Role:** {profile.get('role')}")
    st.markdown(f"**Organization:** {profile.get('organization', 'N/A')}")
