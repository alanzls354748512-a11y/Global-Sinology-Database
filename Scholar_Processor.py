import sys
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload

def get_gdrive_service():
    """初始化 Google Drive API 並確認執行帳號"""
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：GitHub Secrets 中找不到 GDRIVE_CREDENTIALS")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json, strict=False)
        print(f"🤖 正在使用的服務帳號: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證初始化出錯: {str(e)}")
        return None

def upload_with_quota_fix(service, title, content, folder_id):
    """
    核心修復：使用 supportsAllDrives 並強制父級權限
    解決 403 storageQuotaExceeded 問題
    """
    try:
        file_metadata = {
            'name': title,
            'parents': [folder_id]
        }
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        
        # 執行寫入，並設定 supportsAllDrives=True 穿透空間限制
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True 
        ).execute()
        
        print(f"✅ [寫入成功] 文件: {title} | 目標 ID: {folder_id} | 文件 ID: {file.get('id')}")
    except Exception as e:
        print(f"❌ [失敗] 寫入文件夾 {folder_id} 報錯: {str(e)}")
        if "storageQuotaExceeded" in str(e):
            print("👉 診斷：空間限制。請確認您已在 Google Drive 網頁端將該文件夾分享給服務帳號並設為『編輯者』。")

if __name__ == "__main__":
    print("🚀 全球學術資料庫：針對 NSS 分類進行校準寫入...")
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 根據您的提供，已精確校準 NSS_Analysis 的 ID ⚠️
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa', 
            'East_Asian_History': '14O9gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',
            'NSS_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W', # 精確 ID
            'Thought_Gov': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU'
        }
        
        # 測試抓取內容
        test_data = [
            {'title': 'NSS_Cross_Final_Test_2025.txt', 'content': 'NSS Logic: Quota fix and path verify.', 'cat': 'NSS_Analysis'}
        ]
        
        for item in test_data:
            fid = FOLDER_MAP.get(item['cat'])
            if fid:
                upload_with_quota_fix(service, item['title'], item['content'], fid)
            else:
                print(f"⚠️ 分類 [{item['cat']}] 缺少 ID 配置。")

    print("🏁 任務結束。")
