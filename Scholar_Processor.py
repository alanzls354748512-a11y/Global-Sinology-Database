import sys
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account

# --- 核心環境兼容性補丁 ---
try:
    if sys.version_info >= (3, 10):
        from importlib.metadata import packages_distributions
    else:
        from importlib_metadata import packages_distributions
except ImportError:
    def packages_distributions(): return {}

# --- Google Drive 認證初始化 ---
def get_gdrive_service():
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：找不到環境變數 GDRIVE_CREDENTIALS")
        return None
    
    scopes = ['https://www.googleapis.com/auth/drive']
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return build('drive', 'v3', credentials=creds)

def upload_to_gdrive(service, title, content, folder_id):
    """
    將抓取的數據上傳至特定的 Google Drive 文件夾
    """
    try:
        file_metadata = {
            'name': title,
            'parents': [folder_id],
            'mimeType': 'text/plain'
        }
        # 如果是文件內容，這裡可以根據您的抓取逻辑調整
        # 這裡假設 content 是字符串
        from googleapiclient.http import MediaInMemoryUpload
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ 同步成功: {title} | File ID: {file.get('id')}")
        return True
    except Exception as e:
        print(f"❌ 上傳失敗 [{title}]: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Global Sinology Academic Sync: 啟動數據寫入測試...")
    
    service = get_gdrive_service()
    if service:
        # ⚠️ 請在此處填入您截圖中對應文件夾的 ID
        FOLDER_MAP = {
            'Geography': '您的文件夾ID_1', 
            'Governance': '您的文件夾ID_2',
            'Thought': '您的文件夾ID_3'
        }
        
        # 模擬一次抓取測試
        test_data = [
            {'title': 'NSS_Strategic_Analysis_2025.txt', 'content': 'Sample Content', 'cat': 'Thought'}
        ]
        
        for item in test_data:
            target_id = FOLDER_MAP.get(item['cat'])
            if target_id:
                upload_to_gdrive(service, item['title'], item['content'], target_id)
            else:
                print(f"⚠️ 找不到分類 {item['cat']} 對應的文件夾 ID")
