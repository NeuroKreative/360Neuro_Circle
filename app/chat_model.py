import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt, context):
    messages = [
        {"role": "system", "content": "You are a helpful assistant for Circle community content."},
        {"role": "user", "content": f"{prompt}\n\nContext:\n{context}"}
    ]
    completion = openai.ChatCompletion.create(model="gpt-4", messages=messages)
    return completion.choices[0].message.content
