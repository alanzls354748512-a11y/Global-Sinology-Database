import sys
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload

# --- 環境兼容性補丁 ---
try:
    if sys.version_info >= (3, 10):
        from importlib.metadata import packages_distributions
    else:
        from importlib_metadata import packages_distributions
except ImportError:
    def packages_distributions(): return {}

def get_gdrive_service():
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：GitHub Secrets 中找不到 GDRIVE_CREDENTIALS")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json)
        print(f"🤖 正在使用的服務帳號: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證初始化失敗: {str(e)}")
        return None

def upload_and_report(service, title, content, folder_id):
    """執行寫入並即時回報"""
    try:
        file_metadata = {'name': title, 'parents': [folder_id]}
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ [確認] 文件已寫入成功！文件名: {title} | 新 ID: {file.get('id')}")
        return True
    except Exception as e:
        print(f"❌ [失敗] 寫入文件夾 {folder_id} 失敗。錯誤內容: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 全球學術資料庫：診斷性同步啟動...")
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 請再次核對這些 ID 是否與瀏覽器網址列 folders/ 後面的字符串完全一致 ⚠️
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa', 
            'Governance': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU',
            'Thought': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU',
            'Archive': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa'
        }
        
        test_data = [
            {'title': '診斷報告_地理_2025.txt', 'content': 'NSS Logic: Resilience Test', 'cat': 'Geography'},
            {'title': '診斷報告_治理_2025.txt', 'content': 'Global Governance Test', 'cat': 'Governance'}
        ]
        
        for item in test_data:
            fid = FOLDER_MAP.get(item['cat'])
            upload_and_report(service, item['title'], item['content'], fid)
    
    print("🏁 診斷任務執行完畢。")
