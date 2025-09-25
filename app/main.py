import streamlit as st
from circle_scraper import scrape_circle
from chat_model import generate_response
import re
from datetime import datetime

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Circle Copilot", layout="wide")

# --- Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "circle_data" not in st.session_state:
    st.session_state.circle_data = ""

# --- Helper Functions ---
def extract_urls(text):
    url_pattern = r"https?://[^\s]+"
    return re.findall(url_pattern, text)

def suggest_followups(query, response):
    return [
        f"Can you elaborate more on '{query}'?",
        "What are the latest updates on this topic?",
        "Are there any related discussions in the Circle community?",
        "Can you provide examples or case studies?",
        "What are the expert opinions shared in the community?"
    ]

def format_message(role, content, timestamp):
    icon = "👤" if role == "user" else "🤖"
    return f"{icon} **{role.capitalize()}** ({timestamp}):\n\n{content}"

# --- Logo and Branding ---
st.markdown(
    """
    https://www.360neurogo.com
        https://www.360neurogo.com/wp-content/uploads/2022/03/360NeuroGO-Logo.png
    </a>
    """,
    unsafe_allow_html=True
)

# --- Login Interface ---
if not st.session_state.logged_in:
    st.title("🔐 Circle Copilot Login")
    st.markdown("Please log in to access your Circle community content.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        with st.spinner("Logging in and scraping Circle content..."):
            try:
                scraped_text = scrape_circle(email, password, max_pages=10)
                st.session_state.circle_data = scraped_text
                st.session_state.logged_in = True
                st.success("✅ Logged in and content loaded!")
            except Exception as e:
                st.error(f"❌ Login failed: {e}")

# --- Chat Interface ---
else:
    st.title("💬 Circle Copilot Chat")

    # Clear chat button
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        timestamp = msg.get("timestamp", "")
        formatted = format_message(msg["role"], msg["content"], timestamp)
        with st.chat_message(msg["role"]):
            st.markdown(formatted)

    # Chat input
    user_input = st.chat_input("Ask something about the Circle community...")
    if user_input:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with st.chat_message("user"):
            st.markdown(format_message("user", user_input, timestamp))

        context = st.session_state.circle_data
        system_prompt = (
            "You are a Circle Copilot AI. You must only use information retrieved from the Circle community. "
            "Do not use external sources. If the answer is not available in the Circle content, respond with: "
            "'I’m sorry, I can only provide information available within the Circle community.' "
            "Provide helpful suggestions and include references to where the information was found if possible."
        )

        with st.spinner("Thinking..."):
            response = generate_response(user_input, context, system_prompt=system_prompt)

        response_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with st.chat_message("assistant"):
            st.markdown(format_message("assistant", response, response_timestamp))

            # 🔗 References
            urls = extract_urls(response)
            if urls:
                st.markdown("🔗 **References:**")
                for url in urls:
                    st.markdown(f"- {url}")

            # 💡 Follow-up Suggestions (clickable)
            suggestions
