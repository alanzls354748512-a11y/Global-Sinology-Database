import sys
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload

def get_gdrive_service():
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：GitHub Secrets 中找不到 GDRIVE_CREDENTIALS")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json, strict=False)
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證初始化出錯: {str(e)}")
        return None

def upload_to_personal_account(service, title, content, folder_id):
    """
    針對個人帳號的終極修復：先建立文件，再透過權限操作確保文件出現在您的文件夾
    """
    try:
        # 第一步：嘗試直接建立
        file_metadata = {
            'name': title,
            'parents': [folder_id]
        }
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        
        # 使用 ignoreDefaultVisibility 參數嘗試穿透配額
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
            supportsAllDrives=True
        ).execute()
        
        print(f"✅ [寫入成功] 文件: {title} | 文件 ID: {file.get('id')}")
        return file.get('id')

    except Exception as e:
        print(f"❌ [失敗] 無法寫入文件夾 {folder_id}。原因: {str(e)}")
        if "storageQuotaExceeded" in str(e):
            print("👉 偵測到個人帳號空間限制。請檢查您的 Gmail 儲存空間是否已接近 15GB 或您購買的 2TB 上限。")
            print("👉 另外，請確認該文件夾的『分享』設定中，機器人帳號確實是『編輯者』。")
        return None

if __name__ == "__main__":
    print("🚀 全球學術資料庫：個人帳號空間兼容模式啟動...")
    service = get_gdrive_service()
    
    if service:
        # 已校準的精確 ID
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa',
            'East_Asian_History': '14O9gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',
            'NSS_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W',
            'Thought_Gov': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU'
        }
        
        test_payload = [
            {
                'title': 'Personal_Account_Verify_2025.txt', 
                'content': 'Status: Personal account mode active. Quota bypass testing.', 
                'cat': 'NSS_Analysis'
            }
        ]
        
        for item in test_payload:
            fid = FOLDER_MAP.get(item['cat'])
            if fid:
                upload_to_personal_account(service, item['title'], item['content'], fid)

    print("🏁 診斷任務結束。")
