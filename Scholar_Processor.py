import sys
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload

def get_gdrive_service():
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：Secrets 為空")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json, strict=False)
        print(f"🤖 執行帳號: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證失敗: {str(e)}")
        return None

def upload_with_quota_fix(service, title, content, folder_id):
    """
    解決 403 storageQuotaExceeded 的核心修復邏輯
    """
    try:
        file_metadata = {
            'name': title,
            'parents': [folder_id]
        }
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        
        # 關鍵：使用 supportsAllDrives=True 並確保目標文件夾已分享權限
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True 
        ).execute()
        
        print(f"✅ [寫入成功] 文件: {title} | 文件 ID: {file.get('id')}")
    except Exception as e:
        print(f"❌ [失敗] 文件夾 {folder_id} 報錯: {str(e)}")
        if "storageQuotaExceeded" in str(e):
            print("👉 診斷：空間配額問題。請確認該文件夾是由您的個人帳號 (@gmail.com) 創建，而非機器人帳號。")

if __name__ == "__main__":
    print("🚀 全球學術資料庫：針對 Quota 問題進行最終修復...")
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 請確保 ID 絕對準確且文件夾存在 ⚠️
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa', 
            'NSS_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W'
        }
        
        mock_data = [
            {'title': 'Geography_Quota_Test.txt', 'content': 'Testing fix for 403 error.', 'cat': 'Geography'},
            {'title': 'NSS_Analysis_Quota_Test.txt', 'content': 'Testing Shared Drive support.', 'cat': 'NSS_Analysis'}
        ]
        
        for item in mock_data:
            fid = FOLDER_MAP.get(item['cat'])
            if fid:
                upload_with_quota_fix(service, item['title'], item['content'], fid)

    print("🏁 診斷任務結束。請查看 GitHub 日誌輸出。")
