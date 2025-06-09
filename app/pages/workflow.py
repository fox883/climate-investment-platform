import streamlit as st
from services.utils import goto_page

# Define the workflow pages
pages = {
    "Main": "main.py",
    "Login": "login.py",
    "Dashboard": "dashboard.py",
    "Project Register": "project_register.py",
    "A1: Project Cover": "A1_cover.py",
    "B1 B3: Financial & Risk Snapshot": "B1_B3_financial_risk.py",
    "C1 C3: Impact & Compliance": "C1_C3_impact_compliance.py",
    "Thank You": "thankyou.py"
}

# Sidebar navigation
selected_page = st.sidebar.radio("Navigate through the Workflow", list(pages.keys()))

# Based on the user's selection, display the corresponding content
if selected_page == "Main":
    st.write("Welcome to the **Main** page. Please start your process here.")
    # You can add more content or instructions here
elif selected_page == "Login":
    st.write("This is the **Login** page. Please log in to access your project data.")
    # Add the login form or call your login page here
elif selected_page == "Dashboard":
    st.write("This is the **Dashboard** page. View your project overview and progress here.")
    # Add the dashboard logic or call your dashboard page here
elif selected_page == "Project Register":
    st.write("This is the **Project Register** page. Register your project details here.")
    # Add your project register logic or call your project register page here
elif selected_page == "A1: Project Cover":
    st.write("This is the **A1: Project Cover** page. Fill out the details of your project here.")
    # Add your project cover logic or call your A1 cover page here
elif selected_page == "B1 B3: Financial & Risk Snapshot":
    st.write("This is the **B1 B3: Financial & Risk Snapshot** page. Enter your financial and risk data here.")
    # Add your financial & risk snapshot logic or call your B1 B3 page here
elif selected_page == "C1 C3: Impact & Compliance":
    st.write("This is the **C1 C3: Impact & Compliance** page. Provide your impact and compliance data here.")
    # Add your impact and compliance logic or call your C1 C3 page here
elif selected_page == "Thank You":
    st.write("Thank you for completing the demo! You have successfully submitted your project data.")
    # Add your thank you page logic or call your thank you page here
