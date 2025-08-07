import streamlit as st
import pandas as pd

st.set_page_config(page_title="ASEAN DIWA Platform", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Go to", ["Home", "Country Profiles", "Comparative View"])

# Home page
if page == "Home":
    st.title("🌏 ASEAN DIWA Data Platform")
    st.markdown("Welcome to the ASEAN Data and Information for Women in Action (DIWA) platform.")
    st.image("assets/map.png", use_column_width=True)
    st.markdown("""
    This platform showcases data on gender equality and women’s empowerment across ASEAN member states.
    """)

# Country Profiles page
elif page == "Country Profiles":
    st.title("📄 Country Profiles")
    df = pd.read_csv("data/country_profiles.csv")

    country = st.selectbox("Select a country", df["Country"].unique())
    st.write(df[df["Country"] == country])

# Comparative View page
elif page == "Comparative View":
    st.title("📊 Comparative View")
    df = pd.read_csv("data/country_profiles.csv")

    selected_countries = st.multiselect("Compare countries", df["Country"].unique(), default=df["Country"].unique()[:3])
    if selected_countries:
        comp_df = df[df["Country"].isin(selected_countries)]
        st.dataframe(comp_df)
