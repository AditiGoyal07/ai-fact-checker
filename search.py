import os
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")

@st.cache_data(show_spinner=False)
def search_web(query, num_results=5):
    """
    Perform a Google search using SerpAPI.
    Returns a list of dicts: [{"title": ..., "link": ..., "snippet": ...}]
    """
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "engine": "google",
        "num": num_results,
        "api_key": SERPAPI_KEY,
    }

    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for item in data.get("organic_results", []):
        title = item.get("title") or ""
        link = item.get("link") or ""
        snippet = item.get("snippet") or ""
        if snippet:
            results.append({"title": title, "link": link, "snippet": snippet})
    return results
