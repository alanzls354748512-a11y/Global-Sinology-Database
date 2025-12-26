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
        print("❌ 錯誤：找不到環境變量 GDRIVE_CREDENTIALS")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json)
        print(f"🤖 執行帳號: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證失敗: {str(e)}")
        return None

def upload_to_folder(service, title, content, folder_id):
    """執行數據寫入並驗證結果"""
    try:
        file_metadata = {'name': title, 'parents': [folder_id]}
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ [寫入成功] 文件: {title} | 目標 ID: {folder_id} | 文件 ID: {file.get('id')}")
        return True
    except Exception as e:
        print(f"❌ [寫入失敗] 分類對應 ID [{folder_id}] 報錯: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 全球學術資料庫：24/7 最終校準同步開始...")
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 根據截圖 341-344 嚴格對齊的 ID 映射表 ⚠️
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa',     # 对应截图 341 (地理)
            'East_Asian_History': '14O9gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4', # 对应截图 342 (東亞史)
            'NSS_Cross': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W',      # 对应截图 343 (NSS 交叉分析)
            'Thought_Gov': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU'    # 对应截图 344 (思想與治理)
        }
        
        # 準備校準測試數據
        test_items = [
            {'title': 'Geo_Resilience_Update.txt', 'content': 'NSS Logic: Geography resilience data.', 'cat': 'Geography'},
            {'title': 'History_Strategy_Review.txt', 'content': 'East Asian strategic history data.', 'cat': 'East_Asian_History'},
            {'title': 'NSS_Cross_Analysis_2025.txt', 'content': 'NSS cross-sectional research update.', 'cat': 'NSS_Cross'},
            {'title': 'Gov_Thought_Evolution.txt', 'content': 'Governance and policy evolution research.', 'cat': 'Thought_Gov'}
        ]
        
        for item in test_items:
            fid = FOLDER_MAP.get(item['cat'])
            if fid:
                upload_to_folder(service, item['title'], item['content'], fid)
            else:
                print(f"⚠️ 警告：分類標籤 [{item['cat']}] 找不到對應 ID，請檢查 FOLDER_MAP。")

    print("🏁 任務結束。請在 Google Drive 中分別按 F5 刷新查看。")
