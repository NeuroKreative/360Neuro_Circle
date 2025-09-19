import streamlit as st
import subprocess
from circle_scraper import scrape_circle
from chat_model import generate_response

# --- Ensure Playwright browsers are installed ---
try:
    subprocess.run(["playwright", "install"], check=True)
except Exception as e:
    print(f"Playwright install failed: {e}")

# --- Streamlit UI ---
st.set_page_config(page_title="Circle Copilot", layout="centered")
st.title("🔐 Circle Copilot Chat")

with st.form("login_form"):
    email = st.text_input("Circle Email", key="email_input")
    password = st.text_input("Circle Password", type="password", key="password_input")
    query = st.text_input("Ask me anything about the Circle community:", key="query_input")
    submitted = st.form_submit_button("Submit")

# --- Main Logic ---
if submitted and email and password and query:
    with st.spinner("Logging in and fetching content..."):
        try:
            raw_html = scrape_circle(email, password)

            # Placeholder: Extract text from HTML (you’ll expand this later)
            context = raw_html[:3000]  # Limit to avoid token overflow

            response = generate_response(query, context)
            st.success("✅ Here's what I found:")
            st.write(response)

        except Exception as e:
            st.error(f"❌ Something went wrong:\n{e}")
