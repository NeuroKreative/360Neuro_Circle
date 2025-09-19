from openai import OpenAI
import streamlit as st

def generate_response(prompt, context):
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        organization=st.secrets["OPENAI_ORG_ID"],  # ✅ renamed from organization_id
        project=st.secrets["OPENAI_PROJECT_ID"]     # ✅ renamed from project_id
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant for Circle community content."},
        {"role": "user", "content": f"{prompt}\n\nContext:\n{context}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )
    return response.choices[0].message.content

