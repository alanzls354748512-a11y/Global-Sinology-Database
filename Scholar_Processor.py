import sys
import os
import json
import base64
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload

# --- 全球學術資料庫：核心環境兼容性補丁 ---
try:
    if sys.version_info >= (3, 10):
        from importlib.metadata import packages_distributions
    else:
        from importlib_metadata import packages_distributions
except ImportError:
    def packages_distributions(): return {}

# --- Google Drive 認證與初始化 ---
def get_gdrive_service():
    # 從 GitHub Secrets 讀取變量
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：找不到 GDRIVE_CREDENTIALS。請檢查 GitHub Secrets 設置。")
        return None
    
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證初始化失敗: {str(e)}")
        return None

def upload_to_specific_folder(service, title, content, folder_id):
    """
    執行上傳動作並打印結果
    """
    try:
        file_metadata = {
            'name': title,
            'parents': [folder_id]
        }
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ 同步成功 | 文件: {title} | 目標 ID: {folder_id} | 新文件 ID: {file.get('id')}")
        return True
    except Exception as e:
        print(f"❌ 上傳失敗: {title} 到文件夾 {folder_id}。原因: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Global Sinology Academic Sync: 啟動數據寫入測試...")
    
    # 1. 初始化服務
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 這裡請根據排查清單第 1 點填入您真正的 Google Drive 文件夾 ID
        FOLDER_MAP = {
            'Geography': '請替換為 Geography 文件夾的 ID',
            'Governance': '請替換為 Governance 文件夾的 ID',
            'Thought': '請替換為 Thought 文件夾的 ID',
            'Archive': '請替換為 Archive 文件夾的 ID'
        }
        
        # 2. 測試抓取數據（這裡您可以接入原有的抓取函數）
        # 模擬一份抓取到的數據清單
        mock_data = [
            {'title': 'Geography_Test_Report.txt', 'content': 'NSS Logic: Supply Chain Resilience Data', 'cat': 'Geography'},
            {'title': 'Governance_Policy_Review.txt', 'content': 'Global Political Structure Analysis', 'cat': 'Governance'}
        ]
        
        # 3. 執行循環上傳
        for item in mock_data:
            target_folder_id = FOLDER_MAP.get(item['cat'])
            if target_folder_id and target_folder_id != '請替換為...':
                upload_to_specific_folder(service, item['title'], item['content'], target_folder_id)
            else:
                print(f"⚠️ 跳過項目: {item['title']}。原因：未設置有效的文件夾 ID。")

    print("🏁 任務結束。")
