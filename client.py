import requests

response = requests.post("http://localhost:8000/v1/chat/completions", json={
    "model": "gpt-3.5-turbo",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Please tell me about the Eiffel Tower."},
    ],
    "temperature": 0.7,
    "max_tokens": 200,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0
})

print(response.json())