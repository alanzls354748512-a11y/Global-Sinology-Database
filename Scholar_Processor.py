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
    """從 GitHub Secrets 初始化 Google Drive 服務"""
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：GitHub Secrets 中找不到 GDRIVE_CREDENTIALS")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json, strict=False)
        print(f"🤖 執行帳號確認: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證初始化出錯: {str(e)}")
        return None

def upload_with_owner_transfer(service, title, content, folder_id):
    """
    核心修復：透過強制參數繞過 Service Account 空間限制
    """
    try:
        file_metadata = {
            'name': title,
            'parents': [folder_id]
        }
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain', resumable=True)
        
        # 關鍵：同時使用 supportsAllDrives 與 ignoreDefaultVisibility
        # 確保文件建立在父目錄空間中，而非服務帳號空間
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True,
            keepRevisionForever=True
        ).execute()
        
        print(f"✅ [寫入成功] 文件: {title} | 雲端 ID: {file.get('id')}")
        return file.get('id')
    except Exception as e:
        print(f"❌ [失敗] 無法寫入文件夾 {folder_id}。原因: {str(e)}")
        if "storageQuotaExceeded" in str(e):
            print("👉 核心障礙：Google 認定權限主體仍為機器人。請嘗試將文件夾改為『共享雲端硬碟』(Shared Drive) 模式。")
        return None

if __name__ == "__main__":
    print("🚀 全球學術資料庫：NSS 分類目錄最終路徑穿透測試...")
    service = get_gdrive_service()
    
    if service:
        # 已校準的精確 ID 映射
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa',
            'East_Asian_History': '14O9gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',
            'NSS_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W',
            'Thought_Gov': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU'
        }
        
        test_payload = [
            {
                'title': 'NSS_Final_Success_2025.txt', 
                'content': 'Status: System bypass confirmed. Strategic monitoring active.', 
                'cat': 'NSS_Analysis'
            }
        ]
        
        for item in test_payload:
            fid = FOLDER_MAP.get(item['cat'])
            if fid:
                upload_with_owner_transfer(service, item['title'], item['content'], fid)

    print("🏁 任務結束。")
