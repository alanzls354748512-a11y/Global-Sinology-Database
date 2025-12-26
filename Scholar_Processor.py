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
        print("❌ 錯誤：找不到環境變數 GDRIVE_CREDENTIALS")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json, strict=False)
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證初始化失敗: {str(e)}")
        return None

def upload_with_owner_fix(service, title, content, folder_id):
    """
    核心修復：透過強制指定父級目錄解決 Service Account 空間不足問題
    """
    try:
        file_metadata = {
            'name': title,
            'parents': [folder_id]
        }
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        
        # 關鍵：加入 supportsAllDrives=True 確保權限穿透
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True 
        ).execute()
        
        print(f"✅ [寫入成功] 文件: {title} | 雲端 ID: {file.get('id')}")
    except Exception as e:
        print(f"❌ [失敗] 文件夾 {folder_id} 報錯: {str(e)}")

if __name__ == "__main__":
    print("🚀 全球學術資料庫：NSS 分類目錄精確校準與寫入...")
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 請從截圖 351 中的文件夾網址提取最新的 ID 並填入下方 ⚠️
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa',
            'East_Asian_History': '14O9gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',
            'NSS_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W', # 請確保此處為截圖 351 中新文件夾的 ID
            'Thought_Gov': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU'
        }
        
        test_data = [
            {'title': 'NSS_Cross_Final_Test.txt', 'content': 'NSS Logic: Quota fix and path verify.', 'cat': 'NSS_Analysis'}
        ]
        
        for item in test_data:
            fid = FOLDER_MAP.get(item['cat'])
            if fid:
                upload_with_owner_fix(service, item['title'], item['content'], fid)

    print("🏁 診斷任務執行完畢。")
