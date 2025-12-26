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

# --- Google Drive 初始化 ---
def get_gdrive_service():
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：GitHub Secrets 中找不到 GDRIVE_CREDENTIALS")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json)
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('drive', 'v3', credentials=creds)
    except Exception as e:
        print(f"❌ 認證出錯: {str(e)}")
        return None

def upload_to_gdrive(service, title, content, folder_id):
    try:
        file_metadata = {'name': title, 'parents': [folder_id]}
        media = MediaInMemoryUpload(content.encode('utf-8'), mimetype='text/plain')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ 已成功寫入文件: {title} (ID: {file.get('id')})")
    except Exception as e:
        print(f"❌ 寫入失敗 [{title}]: {str(e)}")

if __name__ == "__main__":
    print("🚀 全球學術資料庫：同步測試開始...")
    service = get_gdrive_service()
    
    if service:
        # ⚠️ 重點：請將下方引號內的長字符串替換为您文件夾網址末尾的 ID
        # 例如網址是 folders/1abc... 則 ID 就是 1abc...
        FOLDER_MAP = {
            'Geography': '這裡填入您的Geography文件夾ID',
            'Governance': '這裡填入您的Governance文件夾ID',
            'Thought': '這裡填入您的Thought文件夾ID',
            'Archive': '這裡填入您的Archive文件夾ID'
        }
        
        # 測試數據
        test_items = [
            {'title': '系統測試_地理模塊.txt', 'content': '數據抓取測試 - 地理', 'cat': 'Geography'},
            {'title': '系統測試_治理模塊.txt', 'content': '數據抓取測試 - 治理', 'cat': 'Governance'}
        ]
        
        for item in test_items:
            fid = FOLDER_MAP.get(item['cat'])
            if fid and '這裡填入' not in fid:
                upload_to_gdrive(service, item['title'], item['content'], fid)
            else:
                print(f"⚠️ 警告：分類 [{item['cat']}] 的 ID 尚未正確設置，跳過上傳。")
    
    print("🏁 任務執行完畢。")
