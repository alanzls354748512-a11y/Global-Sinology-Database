import sys
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload

def get_gdrive_service():
    """初始化 Google Drive API，並打印帳號以便確認"""
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：GitHub Secrets 中找不到 GDRIVE_CREDENTIALS。")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        # 處理 JSON 字符串可能存在的格式問題
        creds_dict = json.loads(creds_json, strict=False)
        print(f"🤖 執行帳號確認: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證初始化出錯: {str(e)}")
        return None

def force_sync_to_folder(service, title, content, folder_id):
    """執行強制寫入並回報最終雲端 ID"""
    try:
        # 強制指定 parents 參數以穿透路徑
        file_metadata = {
            'name': title,
            'parents': [folder_id]
        }
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        
        # 執行 API 創建命令
        file = service.files().create(
            body=file_metadata, 
            media_body=media, 
            fields='id'
        ).execute()
        
        file_id = file.get('id')
        print(f"✅ [確認] 寫入成功！文件: {title} | 目標 ID: {folder_id} | 雲端文件 ID: {file_id}")
        return file_id
    except Exception as e:
        print(f"❌ [失敗] 無法寫入文件夾 {folder_id}。原因: {str(e)}")
        return None

if __name__ == "__main__":
    print("🚀 全球學術資料庫：路徑校正與數據寫入開始...")
    service = get_gdrive_service()
    
    if service:
        # 根據您的截圖 341-344 嚴格校對的 ID 映射表
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa', 
            'History': '14O9gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',
            'NSS_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W',
            'Thought_Gov': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU'
        }
        
        # 準備強制寫入的測試內容
        test_items = [
            {'title': 'Geography_NSS_2025_Update.txt', 'content': 'NSS Logic: Geography resilience data update.', 'cat': 'Geography'},
            {'title': 'NSS_Cross_Analysis_Summary.txt', 'content': 'Technological decoupling research summary.', 'cat': 'NSS_Analysis'}
        ]
        
        for item in test_items:
            fid = FOLDER_MAP.get(item['cat'])
            if fid:
                force_sync_to_folder(service, item['title'], item['content'], fid)
            else:
                print(f"⚠️ 跳過分類 [{item['cat']}]：ID 未配置。")

    print("🏁 診斷任務結束。請查看日誌中是否有 ✅ 字樣。")
