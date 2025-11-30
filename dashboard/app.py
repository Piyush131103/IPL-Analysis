import streamlit as st
import pandas as pd

st.title("IPL Dashboard Test")

# Load a sample dataset
st.subheader("Matches Dataset Sample")
try:
    matches = pd.read_csv("data/matches.csv")
    st.dataframe(matches.head())
except Exception as e:
    st.error(f"Could not load data: {e}")
