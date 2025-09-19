import streamlit as st
from circle_api import fetch_token, fetch_posts
from chat_model import generate_response
from utils import format_posts
from circle_scraper import scrape_circle

st.title("🔐 Circle Copilot Chat")

# Define inputs BEFORE using them
email = st.text_input("Circle Email", key="email_input")
password = st.text_input("Circle Password", type="password", key="password_input")
query = st.text_input("Ask me anything about the Circle community:", key="query_input")

if email and password and query:
    raw_html = scrape_circle(email, password)
    context = extract_text(raw_html)  # You’ll write this parser
    response = generate_response(query, context)
    st.write(response)

# Login UI
email = st.text_input("Circle Email")
password = st.text_input("Circle Password", type="password")
query = st.text_input("Ask me anything about the Circle community:")

if email and password and query:
    with st.spinner("Authenticating and fetching content..."):
        token = fetch_token(email, password)
        posts = fetch_posts(token)
        context = format_posts(posts)
        response = generate_response(query, context)
        st.success("Here's what I found:")
        st.write(response)
