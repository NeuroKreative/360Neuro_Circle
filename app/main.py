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
    <div style="text-align: center; margin-bottom: 20px;">
    https://scontent-sea5-1.cdninstagram.com/v/t51.2885-19/499884850_17851448808452837_5907511648837705268_n.jpg?efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLmRqYW5nby4xMDgwLmMyIn0&_nc_ht=scontent-sea5-1.cdninstagram.com&_nc_cat=105&_nc_oc=Q6cZ2QFMHv8tL5wAx-HICaGgzuwsZESeKiRt7ICzcECrr6BlUDVmTZnNwOb4VacYZZ3S-cotijHnhpydVKBZMjASUaP-&_nc_ohc=aUJxnoGj04EQ7kNvwGXIB0a&_nc_gid=ke-u3wM63AG6za7hTXc7wQ&edm=AP4sbd4BAAAA&ccb=7-5&oh=00_Afal6R0LWa5dgPOZK9izvZugAzwQrw-x9n2Bv4O_Etzrew&oe=68DB7BF4&_nc_sid=7a9f4b
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
    st.title("💬 360Vestie Chat")

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
    user_input = st.chat_input("Hi Im your 360Vestie, what would you like to know?")
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
