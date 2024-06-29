import requests
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE_URL"))

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[dict]
    temperature: float = 0.7
    max_tokens: int = 200
    top_p: float = 1
    frequency_penalty: float = 0
    presence_penalty: float = 0

def bing_search(query):
    bing_key = os.getenv("BING_SUBSCRIPTION_KEY")  # 替换为你的Bing搜索API密钥
    bing_endpoint = os.getenv("BING_SEARCH_URL")  # 替换为你的Bing搜索API终结点
    params = {
        "q": query,
        "textDecorations": True,
        "textFormat": "HTML",
        "safeSearch": "Moderate"
    }
    headers = {
        "Ocp-Apim-Subscription-Key": bing_key
    }
    response = requests.get(bing_endpoint, headers=headers, params=params)
    return response.json()

import langchain
from langchain_openai import ChatOpenAI
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    bing_response = bing_search(request.messages[0]["content"])
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_API_BASE_URL"),
        temperature=request.temperature, max_tokens=request.max_tokens, model=request.model
        )
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Please tell me about the Eiffel Tower."},
        {"role": "assistant", "content": f"According to Bing search, the Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It was built in 1889 and designed by Gustave Eiffel."}
    ]
    print(bing_response)
    for result in bing_response["webPages"]["value"]:
        messages.append({"role": "assistant", "content": f"Source: {result['name']}\n{result['snippet']}"})
    response = llm.invoke(messages)
    return {"choices": [{"message": {"role": "assistant", "content": response.content}}]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)