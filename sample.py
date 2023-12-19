import requests

headers = {
        'Authorization': 'Bearer envepskcje',
    }
response = requests.post("https://asia-northeast2-kgavengers.cloudfunctions.net/openai-proxy/v1/chat/completions",headers=headers, json={"model": "gpt-4","messages": [{"role": "user", "content": "Hello world!"}]})

print(response.text)