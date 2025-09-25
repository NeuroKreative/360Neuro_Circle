from openai import OpenAI
import streamlit as st

def generate_response(prompt, context, system_prompt="You are a helpful assistant for Circle community content."):
    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"],
        organization=st.secrets["OPENAI_ORG_ID"],
        project=st.secrets["OPENAI_PROJECT_ID"]
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"{prompt}\n\nContext:\n{context}"}
    ]

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=messages
    )

    return response.choices[0].message.content

