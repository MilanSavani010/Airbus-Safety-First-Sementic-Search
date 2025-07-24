import streamlit as st
import requests
from pathlib import Path

st.set_page_config(page_title="🔍 Document Search", layout="wide")
st.title("📘 Semantic PDF Search")

query = st.text_input("Enter your query")
match_count = st.slider("Results to show", 1, 10, 5)

if st.button("Search") and query:
    res = requests.get("http://localhost:5000/api/search", params={
        "query": query,
        "top_k": match_count
    })

    results = res.json()

    for item in results:
        file = item["filepath"]
        page = item["page"]
        snippet = item["text"]
        file_api = f"http://localhost:5000/api/open-pdf?file={file}#page={page}"

        col1, col2 = st.columns([1, 5])
        with col2:
            st.subheader(f"{file} — Page {page}")
            st.markdown(f"`{snippet}`")
            st.markdown(f"[Open PDF File]({file_api})", unsafe_allow_html=True)
            st.markdown("---")

