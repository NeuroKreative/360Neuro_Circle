import streamlit as st
from circle_scraper import scrape_circle
from chat_model import generate_response
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
            # Scrape Circle content using provided credentials
            raw_html = scrape_circle(email, password)

            # Extract and limit context to avoid token overflow
            context = raw_html[:3000]

            # Add system prompt to enforce Circle-only responses
            system_prompt = (
                "You are a Circle Copilot AI. You must only use information "
                "retrieved from the Circle community. Do not use external sources. "
                "If the answer is not available in the Circle content, respond with: "
                "'I’m sorry, I can only provide information available within the Circle community.'"
            )

            # Generate response using Circle-only context
            response = generate_response(query, context, system_prompt=system_prompt)
            st.success("✅ Here's what I found:")
            st.write(response)

        except Exception as e:
            st.error(f"❌ Something went wrong:\n{e}")
