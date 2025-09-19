import streamlit as st
from openai import OpenAI

def generate_response(prompt, context):
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        organization_id=st.secrets["OPENAI_ORG_ID"],
        project_id=st.secrets["OPENAI_PROJECT_ID"]
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant for Circle community content."},
        {"role": "user", "content": f"{prompt}\n\nContext:\n{context}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content
