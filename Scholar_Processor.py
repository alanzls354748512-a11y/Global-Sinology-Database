import sys
import os
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaInMemoryUpload

# --- 核心環境兼容性補丁 ---
try:
    if sys.version_info >= (3, 10):
        from importlib.metadata import packages_distributions
    else:
        from importlib_metadata import packages_distributions
except ImportError:
    def packages_distributions(): return {}

def get_gdrive_service():
    """從 Secrets 獲取認證"""
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：GitHub Secrets 中找不到 GDRIVE_CREDENTIALS")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json)
        # 這裡會顯示是哪個機器人帳號在執行
        print(f"🤖 正在使用服務帳號: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證初始化出錯: {str(e)}")
        return None

def upload_test_file(service, title, content, folder_id):
    """嘗試寫入文件，並捕獲詳細錯誤"""
    try:
        file_metadata = {'name': title, 'parents': [folder_id]}
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ 寫入成功！文件: {title} | 新 ID: {file.get('id')}")
        return True
    except Exception as e:
        print(f"❌ 寫入失敗！文件夹 ID [{folder_id}] 報錯: {str(e)}")
        if "404" in str(e):
            print("   👉 提示：找不到該文件夾，請檢查 ID 是否正確。")
        elif "403" in str(e):
            print("   👉 提示：權限不足！請確保已將服務帳號設為文件夾的『編輯者』。")
        return False

if __name__ == "__main__":
    print("🚀 全球學術資料庫 (Global Sinology Academic) 同步測試中...")
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 請確保此處 ID 與您網頁端看到的一致
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa', # 這是根據您截圖生成的參考 ID
            'Governance': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU',
            'Thought': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU', # 治理與思想暫設同一處
            'Archive': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa'
        }
        
        # 執行抓取數據測試
        mock_data = [
            {'title': 'NSS_SupplyChain_Resilience_2025.txt', 'content': 'NSS Strategic Data Update', 'cat': 'Geography'},
            {'title': 'Global_Governance_Dynamics.txt', 'content': 'Governance Data Update', 'cat': 'Governance'}
        ]
        
        for item in mock_data:
            fid = FOLDER_MAP.get(item['cat'])
            upload_test_file(service, item['title'], item['content'], fid)
            
    print("🏁 診斷結束。")
