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
    """從 GitHub Secrets 獲取認證並初始化服務"""
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

def upload_to_gdrive(service, title, content, folder_id):
    """執行寫入並回報結果"""
    try:
        file_metadata = {'name': title, 'parents': [folder_id]}
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ 寫入成功: {title} | 目標 ID: {folder_id} | 文件 ID: {file.get('id')}")
        return True
    except Exception as e:
        print(f"❌ 寫入失敗 [{title}]: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 全球學術資料庫：校準同步啟動...")
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 已根據截圖 341-344 更新的精確 ID 映射 ⚠️
        FOLDER_MAP = {
            'Geography': '12Y0tfBUQ-B6VZPEVTLIFKIALeY9GIDSa',     # 对应截图 341
            'History': '14O9gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',       # 对应截图 342
            'NSS_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W',  # 对应截图 343
            'Thought_Gov': '14H9f4hduc3QmmE3TAjnCtVNn36xdVHJU'    # 对应截图 344
        }
        
        # 準備校準測試數據
        test_items = [
            {'title': 'Geography_NSS_Resilience_2025.txt', 'content': '地理模塊：供應鏈韌性測試數據', 'cat': 'Geography'},
            {'title': 'History_East_Asian_Strategic_Review.txt', 'content': '歷史模塊：東亞戰略史測試數據', 'cat': 'History'},
            {'title': 'NSS_Cross_Analysis_Report.txt', 'content': 'NSS 交叉分析模塊：技術脫鉤測試數據', 'cat': 'NSS_Analysis'},
            {'title': 'Governance_Thought_Summary.txt', 'content': '治理與思想模塊：政策演變測試數據', 'cat': 'Thought_Gov'}
        ]
        
        for item in test_items:
            fid = FOLDER_MAP.get(item['cat'])
            if fid:
                upload_to_gdrive(service, item['title'], item['content'], fid)
            else:
                print(f"⚠️ 分類 [{item['cat']}] 缺少 ID 配置，跳過。")

    print("🏁 數據同步任務完成。請刷新 Google Drive 查看。")
