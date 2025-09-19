import streamlit as st
from circle_api import fetch_token, fetch_posts
from chat_model import generate_response
from utils import format_posts

st.title("🔐 Circle Copilot Chat")

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
