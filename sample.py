import requests


#ここを編集#
user_id = ""
host = "https://asia-northeast2-kgavengers.cloudfunctions.net/openai-proxy"
path = "/v1/chat/completions"
data = {"model": "gpt-4","messages": [{"role": "user", "content": "Hello world!"}]}
###########


headers = {
        'Authorization': f'Bearer {user_id}',
    }

response = requests.post(host+path,headers=headers, json=data)

print(response.json())