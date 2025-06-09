import streamlit as st
st.set_page_config(page_title="🌿 Impact & Compliance Snapshot", page_icon="🌿")  # MUST BE FIRST

# Import necessary services and functions
from services.supabase_client import supabase
from services.utils import (
    logout_button, show_connection_status, button_to,
    require_login, get_user_profile, goto_page
)
from services.style_utils import apply_global_style
from services.project_access import get_current_project_id, get_project_by_id
from services.project_display import show_user_profile, display_project_card
from services.supabase_utils import upsert_row

# Apply global styles and show connection status
apply_global_style(skip_config=True)
show_connection_status()

# Ensure the user is logged in
require_login()

# Load user profile
profile = get_user_profile()
if not profile:
    st.error("⚠️ User profile not found. Please try logging in again.")
    if st.button("🔐 Go to Login"):
        goto_page("login")
    st.stop()

# Fetch the current project ID and details
try:
    project_id = get_current_project_id()
    if not project_id:
        st.error("⚠️ No project selected. Please register or select a project first.")
        if st.button("📋 Register Project"):
            goto_page("project_register")
        st.stop()
    project = get_project_by_id(project_id)
except Exception as e:
    st.error(f"❌ Error loading project or user profile: {e}")
    st.stop()

# Display user profile and project card
show_user_profile(profile)
display_project_card(project, profile)
logout_button()

# Display Impact & Compliance form
st.subheader("🌿 Impact & Compliance Information")

with st.form("impact_compliance_form"):
    estimated_emission_reduction = st.number_input("Estimated Annual Emission Reduction (tons CO₂e)", step=10.0)
    mrv_plan = st.text_area("MRV Plan (Monitoring, Reporting, Verification)")
    sdg_targets = st.text_input("Targeted SDGs (comma-separated, e.g., 13,15,7)")
    social_benefits = st.text_area("Social & Community Benefits")
    regulatory_clearance = st.checkbox("✅ Regulatory Clearance Secured")
    methodology_reference = st.text_input("Carbon Methodology Reference (e.g., Verra, Gold Standard)")

    submitted = st.form_submit_button("💾 Save & Continue")

    if submitted:
        # Validation: ensure all required fields are filled
        if not mrv_plan or not sdg_targets or not social_benefits or not methodology_reference:
            st.error("❌ Please complete all required fields.")
        else:
            # Prepare data for saving to the database
            data = {
                "project_id": project_id,
                "estimated_emission_reduction": estimated_emission_reduction,
                "mrv_plan": mrv_plan,
                "sdg_targets": sdg_targets,
                "social_benefits": social_benefits,
                "regulatory_clearance": regulatory_clearance,
                "methodology_reference": methodology_reference,
            }
            try:
                # Upsert the data into the 'demo_impact_compliance' table
                upsert_row("demo_impact_compliance", data)
                st.success("✅ Impact & Compliance data saved.")
                st.balloons()

                # Redirect to the next page (e.g., Thank You or Dashboard)
                goto_page("thank_you")  # Replace with actual next page key

            except Exception as e:
                st.error(f"❌ Failed to save data: {e}")
