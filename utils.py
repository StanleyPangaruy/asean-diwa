import streamlit as st
import plotly.express as px
import pandas as pd

def load_map():
    df = pd.read_csv("data/summary.csv")
    return px.scatter_geo(df, locations="iso_alpha", hover_name="country", size="score")

def nav_card(title, description, page_name):
    if st.button(title):
        st.switch_page(f"{page_name}.py")
    st.caption(description)

def country_card(name, flag_url, score, page_path):
    st.image(flag_url, width=50)
    st.write(f"**{name}** — Score: {score}")
    if st.button(f"View {name}"):
        st.switch_page(page_path)

def download_buttons(country_name):
    file_format = st.radio("Choose format", ["PDF", "PNG"])
    st.download_button(f"Download {country_name} Data", b"", file_name=f"{country_name.lower()}_data.{file_format.lower()}")