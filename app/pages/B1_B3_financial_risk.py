import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

st.set_page_config(page_title="💰 Financial & Risk Snapshot", page_icon="💰")

from services.supabase_client import supabase
from services.utils import logout_button, show_connection_status, button_to, require_login, get_user_profile, goto_page
from services.style_utils import apply_global_style
from services.project_access import get_current_project_id, get_project_by_id, fetch_projects_by_role
from services.project_display import show_user_profile, display_project_card
from services.supabase_utils import upsert_row

apply_global_style(skip_config=True)
show_connection_status()
require_login()

profile = get_user_profile()
if not profile:
    st.error("⚠️ User profile not found. Please try logging in again.")
    if st.button("🔐 Go to Login"):
        goto_page("login")
    st.stop()

# Project selector
project_options = fetch_projects_by_role(profile)
project_dict = {proj['project_name']: proj['id'] for proj in project_options}
selected_name = st.selectbox("Select a project to view:", list(project_dict.keys()))
project_id = project_dict[selected_name]

project = get_project_by_id(project_id)
show_user_profile(profile)
display_project_card(project, profile)
logout_button()

existing_data = supabase.table("demo_financial_risk").select("*").eq("project_id", project_id).execute()
data = existing_data.data[0] if existing_data.data else {}
is_editable = st.session_state.get("allow_edit", False)

if data and not is_editable:
    st.markdown("### 🔒 Data is locked")
    password = st.text_input("Enter password to edit:", type="password")
    if st.button("🔓 Enable Edit Mode"):
        if password == "1234":
            st.session_state.allow_edit = True
            st.rerun()
        else:
            st.warning("Incorrect password.")

st.markdown("---")
st.subheader("💰 Financial & Risk Information")

with st.form("financial_risk_form"):
    capex = st.number_input("CAPEX (USD)", value=data.get("capex_usd", 0.0), disabled=not is_editable)
    opex = st.number_input("Annual OPEX (USD)", value=data.get("opex_usd_annual", 0.0), disabled=not is_editable)
    revenue_sources = st.text_area("Revenue Sources", value=data.get("revenue_sources", ""), disabled=not is_editable)
    revenue_est = st.number_input("Annual Revenue Estimate (USD)", value=data.get("revenue_estimate_annual", 0.0), disabled=not is_editable)
    fin_risks = st.text_area("Financial Risks", value=data.get("financial_risks", ""), disabled=not is_editable)
    esg_risks = st.text_area("ESG Risks", value=data.get("esg_risks", ""), disabled=not is_editable)
    legal_risks = st.text_area("Legal & Regulatory Risks", value=data.get("legal_risks", ""), disabled=not is_editable)

    vol = st.number_input("Annual Carbon Credit Volume (tCO₂)", value=data.get("credit_volume_annual", 0.0), disabled=not is_editable)
    price = st.number_input("Carbon Price (USD/tCO₂)", value=data.get("credit_price_usd", 0.0), disabled=not is_editable)
    years = st.number_input("Credit Lifespan (Years)", step=1, value=data.get("credit_lifespan_years", 0), disabled=not is_editable)
    buffer = st.number_input("Buffer Deduction (%)", value=data.get("buffer_percentage", 0.0), disabled=not is_editable)
    mrv = st.number_input("Verification Cost (USD/tCO₂)", value=data.get("verification_cost_per_ton", 0.0), disabled=not is_editable)
    growth = st.number_input("Price Escalation Rate (%/year)", value=data.get("price_escalation_rate", 0.0), disabled=not is_editable)
    discount = st.number_input("Discount Rate for Carbon Cashflows (%)", value=data.get("carbon_discount_rate", 0.0), disabled=not is_editable)

    cert = st.number_input("Project Certification Cost (USD)", value=data.get("project_certification_cost", 0.0), disabled=not is_editable)
    registry_fee = st.number_input("Annual Registry Fee (USD)", value=data.get("registry_fee_annual", 0.0), disabled=not is_editable)
    dev_fee_pct = st.number_input("Developer Fee (% of revenue)", value=data.get("developer_fee_percentage", 0.0), disabled=not is_editable)
    local_share_pct = st.number_input("Community Revenue Share (%)", value=data.get("revenue_share_local", 0.0), disabled=not is_editable)
    buffer_cost = st.number_input("Implicit Buffer Cost (USD)", value=data.get("buffer_cost_implicit", 0.0), disabled=not is_editable)
    standard = st.text_input("Carbon Standard", value=data.get("carbon_standard", ""), disabled=not is_editable)
    buyer_type = st.text_input("Buyer Market Type", value=data.get("credit_buyer_type", ""), disabled=not is_editable)
    memo = st.text_area("Analyst Memo", value=data.get("memo_notes", ""), disabled=not is_editable)

    submitted = st.form_submit_button("Save & Continue")

# Collapsible dashboard
with st.expander("📊 View Analysis Dashboard"):
    if data:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**💼 Financial Rating:** `{data.get('financial_rating', '-')}`")
            st.markdown(f"**💰 Total Revenue (Nominal):** ${data.get('total_revenue_nominal', 0):,.0f}")
            st.markdown(f"**📈 NPV:** ${data.get('npv_total', 0):,.0f}")
            st.markdown(f"**📉 IRR:** {data.get('irr_estimate', 0):.2f}%")
            st.markdown(f"**⚖️ Break-even Carbon Price:** ${data.get('break_even_carbon_price', 0):,.2f} /tCO₂")

            # New: Carbon revenue over time
            if data.get("credit_lifespan_years", 0) > 0:
                carbon_revs = [(data['credit_volume_annual'] * (1 - data['buffer_percentage'] / 100)) * (data['credit_price_usd'] - data['verification_cost_per_ton']) * ((1 + data['price_escalation_rate'] / 100) ** t) for t in range(1, data['credit_lifespan_years'] + 1)]
                fig_rev = go.Figure()
                fig_rev.add_trace(go.Bar(x=[f"Year {t}" for t in range(1, data['credit_lifespan_years'] + 1)], y=carbon_revs, name="Carbon Revenue"))
                fig_rev.update_layout(title="Carbon Revenue by Year", xaxis_title="Year", yaxis_title="USD", showlegend=True)
                st.plotly_chart(fig_rev, use_container_width=True)

        with col2:
            st.markdown("**🧪 Scenario Test:**")
            test_price = st.slider("Test Carbon Price (USD)", 0, 100, int(data.get("credit_price_usd", 10)))
            test_buffer = st.slider("Buffer Deduction (%)", 0, 50, int(data.get("buffer_percentage", 10)))
            test_discount = st.slider("Discount Rate (%)", 0, 30, int(data.get("carbon_discount_rate", 10)))
            vol = data.get("credit_volume_annual", 0.0)
            years = data.get("credit_lifespan_years", 1)
            net_price = test_price - data.get("verification_cost_per_ton", 0.0)
            net_volume = vol * (1 - test_buffer / 100)
            cashflows = [(net_volume * net_price) * ((1 + data.get("price_escalation_rate", 0.0) / 100) ** t) for t in range(1, years + 1)]
            npv_test = sum(cf / ((1 + test_discount / 100) ** t) for t, cf in enumerate(cashflows, start=1))
            st.markdown(f"**🔄 Scenario Carbon NPV:** ${npv_test:,.0f}")

            fig_scen = go.Figure()
            fig_scen.add_trace(go.Bar(x=[f"Year {t}" for t in range(1, years + 1)], y=cashflows, name="Scenario Carbon Cashflow"))
            fig_scen.update_layout(title="Scenario Carbon Revenue by Year", xaxis_title="Year", yaxis_title="USD", showlegend=True)
            st.plotly_chart(fig_scen, use_container_width=True)

        labels = ['Carbon Revenue', 'Other Revenue']
        values = [data.get('carbon_revenue_total', 0), data.get('revenue_estimate_annual', 0) * data.get('credit_lifespan_years', 1)]
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4, textinfo='label+percent')])
        fig.update_layout(title_text="Revenue Composition", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📜 No financial data to display yet.")
