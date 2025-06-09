import streamlit as st
from services.utils import goto_page  # <-- Ensure this is imported

st.set_page_config(page_title="Thank You!", page_icon="🎉")

# Display Thank You message
st.title("🎉 Thank You for Seeing the Demo!")
st.markdown("""
    We appreciate your time and effort in filling out the project data.

    You have successfully submitted your project information.

    ### What's Next:
    - Our team will review your submission.
    - You can return to the dashboard or register another project.

    Feel free to navigate back to the **Dashboard** or proceed with further actions below.

    ---
    ### This product was designed by **Xinzhi Yao**
    - Contact me now to book a demo: [xinzhi.yao@pm.me](mailto:xinzhi.yao@pm.me)

    ### Next Updates:
    Here are the upcoming updates and features that will be implemented:
    - **Financial Modeling Module**: Advanced financial analysis, including scenario and sensitivity testing.
    - **Risk Assessment Tools**: Comprehensive ESG and legal compliance risk assessments.
    - **Carbon Sequestration Modeling**: Detailed models for estimating carbon sequestration potential.
    - **Project Portfolio Dashboard**: Visualize and track your project's progress across multiple metrics.
    - **AI-Driven Decision Support**: AI tools for auto-generating investment summaries and insights.
    - **User and Role Management**: Enhancements for team collaboration, project assignment, and reporting.
    - **Fundraising Support**: Tools for managing investor engagement and reporting.
""")

# Navigation options
if st.button("🚀 Go to Dashboard"):
    st.session_state["project_id"] = None  # Clear the current project ID
    st.session_state["project_name"] = None  # Clear the current project name (optional)
    goto_page("dashboard")  # Redirect to the dashboard page

if st.button("📋 Register Another Project"):
    st.session_state["project_id"] = None  # Clear the current project ID
    st.session_state["project_name"] = None  # Clear the current project name (optional)
    goto_page("register")  # Redirect to the project registration page
