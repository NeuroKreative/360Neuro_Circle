import streamlit as st
from circle_scraper import scrape_circle
from chat_model import generate_response

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="Circle Copilot", layout="wide")

# --- Initialize Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "circle_data" not in st.session_state:
    st.session_state.circle_data = ""

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

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    user_input = st.chat_input("Ask something about the Circle community...")
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Build context and system prompt
        context = st.session_state.circle_data
        system_prompt = (
            "You are a Circle Copilot AI. You must only use information retrieved from the Circle community. "
            "Do not use external sources. If the answer is not available in the Circle content, respond with: "
            "'I’m sorry, I can only provide information available within the Circle community.' "
            "Provide helpful suggestions and include references to where the information was found if possible."
        )

        # Generate response
        with st.spinner("Thinking..."):
            response = generate_response(user_input, context, system_prompt=system_prompt)

        # Display assistant message
        with st.chat_message("assistant"):
            st.markdown(response)

        # Update chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": response})

