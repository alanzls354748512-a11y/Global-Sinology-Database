import os, json, requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# --- 1. 核心路徑配置 ---
FOLDER_MAP = {
    'Thought_Governance': '14H9f4hduc3QmmE3TAjnCtvNn36xdVHJU', # 宋明理學、古代行政
    'Document_Geography': '12Y0tfBUQ-B6VZPEVTLIFKlAleY9GIDSa', # 版本目錄、經學、地理
    'East_Asian_History': '1409gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4', # 中韓日史
    'Cross_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W'
}

# --- 2. 跨平台學術檢索函數 (CrossRef API) ---
def fetch_latest_papers(keyword):
    """
    透過 CrossRef API 檢索最新的學術論文元數據與下載鏈接
    """
    url = f"https://api.crossref.org/works?query={keyword}&sort=published&order=desc&rows=2"
    headers = {'User-Agent': 'GlobalSinologyBot/1.0 (mailto:your-email@example.com)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            items = response.json().get('message', {}).get('items', [])
            return items
    except Exception as e:
        print(f"檢索 {keyword} 出錯: {e}")
    return []

# --- 3. 上傳 PDF/文獻信息至 G 盤 ---
def upload_to_gdrive(title, content_url, folder_id):
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict)
    service = build('drive', 'v3', credentials=creds)

    # 建立簡要的文獻索引文件 (若無法直接獲取 PDF 則存儲鏈接與摘要)
    file_metadata = {'name': f"{title}.txt", 'parents': [folder_id]}
    file_content = f"文獻標題: {title}\n來源鏈接: {content_url}\n自動採集時間: 2025-12-25"
    
    fh = io.BytesIO(file_content.encode('utf-8'))
    media = MediaIoBaseUpload(fh, mimetype='text/plain')
    
    service.files().create(body=file_metadata, media_body=media, fields='id').execute()

# --- 4. 主程序：分類執行任務 ---
if __name__ == "__main__":
    # 定義分類任務
    TASKS = [
        {"cat": "Thought_Governance", "keywords": ["Neo-Confucianism", "Ancient Administration China"]},
        {"cat": "Document_Geography", "keywords": ["Chinese Bibliography", "Historical Geography China"]},
        {"cat": "East_Asian_History", "keywords": ["History of Korea", "Japanese History", "Sinology"]}
    ]

    for task in TASKS:
        for kw in task['keywords']:
            papers = fetch_latest_papers(kw)
            for paper in papers:
                title = paper.get('title', ['Untitled'])[0]
                url = paper.get('URL', '')
                upload_to_gdrive(title, url, FOLDER_MAP[task['cat']])
                print(f"✅ 已歸檔: {title}")
