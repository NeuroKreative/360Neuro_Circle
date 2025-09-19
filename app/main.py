import streamlit as st
from circle_api import get_auth_token, fetch_posts
from app.chat_model import generate_response
from app.utils import format_posts

st.title("Circle Copilot Chat")

query = st.text_input("Ask me anything about the Circle community:")
if query:
    token = get_auth_token()
    posts = fetch_posts(token)
    context = format_posts(posts)
    response = generate_response(query, context)
    st.write(response)
