from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_response(prompt, context):
    messages = [
        {"role": "system", "content": "You are a helpful assistant for Circle community content."},
        {"role": "user", "content": f"{prompt}\n\nContext:\n{context}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content


