import functions_framework
import requests
import time
import GCS

OPENAI_API_URL = "https://api.openai.com"
BUCKET_NAME = "routinet-openai-proxy"

def get_name_by_user_id(in_user_id):
    users = GCS.read_from_storage(BUCKET_NAME, "users.txt")
    users_list = users.split("\n")
    del users_list[0]
    for line in users_list:
        name, user_id, api_key = line.split(":")
        if user_id == in_user_id:
            return name

def get_api_key_by_user_id(in_user_id):
    users = GCS.read_from_storage(BUCKET_NAME, "users.txt")
    users_list = users.split("\n")
    del users_list[0]
    for line in users_list:
        name, user_id, api_key = line.split(":")
        if user_id == in_user_id:
            return api_key

def init():
    #log.txtとusage.txtを初期化する
    GCS.write_to_storage(BUCKET_NAME, "log.txt", "")
    users = GCS.read_from_storage(BUCKET_NAME, "users.txt")
    users_list = users.split("\n")
    del users_list[0]
    for line in users_list:
        name, user_id, api_key = line.split(":")
        GCS.write_to_storage(BUCKET_NAME, f"{name}_usage.txt", "Total Prompt Tokens:0\nTotal Completion Tokens:0\n")

def log(request):
    pass

@functions_framework.http
def main(request):
    # Track token usage and any other required logic
    auth_header = request.headers.get("Authorization")
    user_id = auth_header.split(" ")[-1] if auth_header else None
    
    if user_id:
        api_key = get_api_key_by_user_id(user_id)
        api_key = api_key[:-1] 
        headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        }
        data = request.get_json()
        response = requests.post(OPENAI_API_URL+request.path, headers=headers, json=data)
        
        if response.status_code == 200:
            json_response = response.json()
            usage = json_response.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)

            user_name = get_name_by_user_id(user_id)
            log_entry = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | User: {user_name} | Prompt Tokens: {prompt_tokens} | Completion Tokens: {completion_tokens}\n"
            GCS.add_text_to_file(BUCKET_NAME, "log.txt", log_entry)
            file_name = f"{user_name}_usage.txt"
            usage = GCS.read_from_storage(BUCKET_NAME, file_name)
            lines = usage.split("\n")
            total_prompt_tokens = int(lines[0].split(":")[1])
            total_completion_tokens = int(lines[1].split(":")[1])
            total_prompt_tokens += prompt_tokens
            total_completion_tokens += completion_tokens
            usage = f"Total Prompt Tokens:{total_prompt_tokens}\nTotal Completion Tokens:{total_completion_tokens}\n"
            GCS.write_to_storage(BUCKET_NAME, file_name, usage)    
            
            # Return the response from OpenAI's API
            return response.json()
        else:
            return response.text, response.status_code
    else:
        return "Unauthorized", 401