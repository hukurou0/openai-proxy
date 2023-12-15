from google.cloud import storage
from google.oauth2 import service_account

def create_bucket(bucket_name):
    """新しいバケットを作成する関数"""
    storage_client = storage.Client()
    
    # バケットの作成
    bucket = storage_client.bucket(bucket_name)
    new_bucket = storage_client.create_bucket(bucket, location="us-central1")
    
def update_storage_file(bucket_name, file_name, new_data):
    # Google Cloud Storageクライアントを初期化
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # 既存のファイルを取得し、新しいデータで上書き
    blob = bucket.blob(file_name)
    blob.upload_from_string(new_data)
    
def read_from_storage(bucket_name, file_name):
    # Google Cloud Storageクライアントを初期化
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # ファイルを読み込む
    blob = bucket.blob(file_name)
    return blob.download_as_text()

def add_text_to_file(bucket_name, file_name, new_data):
    text = read_from_storage(bucket_name, file_name)
    text += new_data
    update_storage_file(bucket_name, file_name, text)

def write_to_storage(bucket_name, file_name, data):
    # Google Cloud Storageクライアントを初期化
    client = storage.Client()
    bucket = client.bucket(bucket_name)

    # ファイルにデータを書き込む
    blob = bucket.blob(file_name)
    blob.upload_from_string(data)