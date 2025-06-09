import streamlit as st
st.set_page_config(page_title="💰 Financial & Risk Snapshot", page_icon="💰")  # MUST BE FIRST

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

# Load user profile from the session
profile = get_user_profile()
if not profile:
    st.error("⚠️ User profile not found. Please try logging in again.")
    if st.button("🔐 Go to Login"):
        goto_page("login")
    st.stop()

# Fetch the project ID and data
try:
    project_id = get_current_project_id()
    if not project_id:
        st.error("⚠️ No project selected. Please register or select a project first.")
        if st.button("📋 Register Project"):
            goto_page("project_register")
        st.stop()

    # Get project details using the project ID
    project = get_project_by_id(project_id)
except Exception as e:
    st.error(f"❌ Error loading project or user profile: {e}")
    st.stop()

# Display the user profile and project info
show_user_profile(profile)
display_project_card(project, profile)  # Show project details with context for the user
logout_button()

# Display financial and risk information form
st.subheader("💰 Financial & Risk Information")

with st.form("financial_risk_form"):
    capex_usd = st.number_input("CAPEX (USD)", step=1000.0)
    opex_usd_annual = st.number_input("Annual OPEX (USD)", step=1000.0)
    expected_irr = st.number_input("Expected IRR (%)")
    expected_npv = st.number_input("Expected NPV (USD)", step=1000.0)
    revenue_sources = st.text_area("Revenue Sources (e.g. carbon credits, co-benefits)")
    revenue_estimate_annual = st.number_input("Annual Revenue Estimate (USD)", step=1000.0)
    financial_risks = st.text_area("Financial Risks")
    esg_risks = st.text_area("ESG Risks")
    legal_risks = st.text_area("Legal & Regulatory Risks")

    submitted = st.form_submit_button("💾 Save & Continue")

    if submitted:
        # Ensure all fields have valid data
        if not (
                capex_usd and opex_usd_annual and expected_irr and expected_npv and revenue_sources and revenue_estimate_annual and financial_risks and esg_risks and legal_risks):
            st.error("❌ All fields must be filled out.")
        else:
            # Prepare data for saving to the database
            data = {
                "project_id": project_id,
                "capex_usd": capex_usd,
                "opex_usd_annual": opex_usd_annual,
                "expected_irr": expected_irr,
                "expected_npv": expected_npv,
                "revenue_sources": revenue_sources,
                "revenue_estimate_annual": revenue_estimate_annual,
                "financial_risks": financial_risks,
                "esg_risks": esg_risks,
                "legal_risks": legal_risks,
            }
            try:
                # Upsert the data into the 'demo_financial_risk' table
                upsert_row("demo_financial_risk", data)
                st.success("✅ Financial & Risk data saved.")
                st.balloons()

                # Redirect to the next step (Impact Compliance)
                goto_page("C1_C3_impact_compliance")  # <-- Adjust the page key if needed

            except Exception as e:
                st.error(f"❌ Failed to save data: {e}")

