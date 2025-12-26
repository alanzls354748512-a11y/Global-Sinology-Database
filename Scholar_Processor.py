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
    """初始化 Google Drive API 服務"""
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：找不到環境變數 GDRIVE_CREDENTIALS。請檢查 GitHub Secrets。")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json)
        # 確認與 JSON 文件一致
        print(f"🤖 執行帳號: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證失敗: {str(e)}")
        return None

def upload_to_folder(service, title, content, folder_id):
    """執行數據寫入動作"""
    try:
        file_metadata = {'name': title, 'parents': [folder_id]}
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ [寫入成功] 文件: {title} | 目標 ID: {folder_id}")
        return True
    except Exception as e:
        print(f"❌ [寫入失敗] 文件夾 {folder_id} 報錯: {str(e)}")
        if "403" in str(e):
            print("👉 診斷：權限不足。請確保已將 finance-auto-sync 郵箱設為編輯者。")
        return False

if __name__ == "__main__":
    print("🚀 全球學術資料庫：24/7 最終校準同步開始...")
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 根據截圖 341-344 嚴格校對的 ID ⚠️
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa',     # 截圖 341
            'East_Asian_History': '14O9gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4', # 截圖 342
            'NSS_Cross': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W',      # 截圖 343
            'Thought_Gov': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU'    # 截圖 344
        }
        
        # 測試寫入數據
        test_items = [
            {'title': 'Geo_System_Test.txt', 'content': 'Geography data sync test.', 'cat': 'Geography'},
            {'title': 'History_System_Test.txt', 'content': 'History data sync test.', 'cat': 'East_Asian_History'},
            {'title': 'NSS_System_Test.txt', 'content': 'NSS Analysis sync test.', 'cat': 'NSS_Cross'},
            {'title': 'Gov_System_Test.txt', 'content': 'Governance data sync test.', 'cat': 'Thought_Gov'}
        ]
        
        for item in test_items:
            fid = FOLDER_MAP.get(item['cat'])
            if fid:
                upload_to_folder(service, item['title'], item['content'], fid)

    print("🏁 任務結束。請在 1 分鐘後刷新 Google Drive 查看結果。")
