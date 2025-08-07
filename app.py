import streamlit as st

st.set_page_config(page_title="ASEAN DIWA Dashboard", layout="wide")

# Sidebar content
st.sidebar.title("ASEAN DIWA")
st.sidebar.markdown("### 📚 Overview")
st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/Introduction.py", label="📘 Dashboard")
st.sidebar.page_link("pages/Indicators.py", label="📊 Regional Overview")
st.sidebar.markdown("### 📚 Analysis")
st.sidebar.page_link("pages/Introduction.py", label="📘 Countries")
st.sidebar.page_link("pages/Indicators.py", label="📊 Compare")
st.sidebar.page_link("pages/Introduction.py", label="📘 Explorer")
st.sidebar.markdown("### 📚 Insights")
st.sidebar.page_link("pages/Introduction.py", label="📘 Data Stories")
st.sidebar.page_link("pages/Indicators.py", label="📊 Key Insights")

# Main content
st.title("🌏 ASEAN DIWA Dashboard")
st.markdown("Welcome to the DIWA Initiative Dashboard – Empowering Women Across ASEAN.")


