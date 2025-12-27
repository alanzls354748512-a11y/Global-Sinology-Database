import os, json, requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# --- 1. 核心路徑配置 ---
# 請確保這些資料夾已在 Google Drive 中「共用」給您的 Service Account Email (編輯者權限)
FOLDER_MAP = {
    'Thought_Governance': '14H9f4hduc3QmmE3TAjnCtvNn36xdVHJU', # 宋明理學、古代行政
    'Document_Geography': '12Y0tfBUQ-B6VZPEVTLIFKlAleY9GIDSa', # 版本目錄、經學、地理
    'East_Asian_History': '1409gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4', # 中、韓、日史
}

# --- 2. PDF 下載引擎 (Unpaywall API) ---
def get_pdf_link(doi):
    """透過 DOI 尋找合法的免費 PDF 下載鏈接 (Open Access)"""
    email = "alanzls354748512@gmail.com" 
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            data = r.json()
            # 優先獲取最佳 OA 位置的 PDF 鏈接
            best_link = data.get('best_oa_location', {})
            if best_link:
                return best_link.get('url_for_pdf')
    except Exception as e:
        print(f"⚠️ Unpaywall API 請求異常: {e}")
        return None
    return None

# --- 3. 執行抓取與上傳 ---
def process_academic_papers(keyword, folder_id):
    # 使用 CrossRef 抓取最新論文元數據
    search_url = f"https://api.crossref.org/works?query={keyword}&sort=published&order=desc&rows=3"
    headers = {'User-Agent': 'GlobalSinologyBot/1.1 (mailto:alanzls354748512@gmail.com)'}
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200: 
            print(f"❌ CrossRef API 錯誤: {response.status_code}")
            return

        items = response.json().get('message', {}).get('items', [])
        
        # 認證 Google Drive
        creds_json = os.environ.get('GDRIVE_CREDENTIALS')
        if not creds_json:
            print("❌ 環境變量 GDRIVE_CREDENTIALS 缺失")
            return
            
        creds = service_account.Credentials.from_service_account_info(
            json.loads(creds_json),
            scopes=['https://www.googleapis.com/auth/drive']
        )
        service = build('drive', 'v3', credentials=creds)

        for item in items:
            title = item.get('title', ['Untitled'])[0]
            # 清理檔名，移除不合法字符
            safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '.', '_', '-')]).strip()
            doi = item.get('DOI')
            pdf_url = get_pdf_link(doi) if doi else None

            try:
                if pdf_url:
                    # 嘗試下載 PDF 實體
                    print(f"📥 偵測到開放文獻，開始下載 PDF: {safe_title}")
                    pdf_res = requests.get(pdf_url, timeout=30)
                    if pdf_res.status_code == 200:
                        pdf_data = pdf_res.content
                        file_metadata = {'name': f"{safe_title}.pdf", 'parents': [folder_id]}
                        media = MediaIoBaseUpload(io.BytesIO(pdf_data), mimetype='application/pdf')
                        
                        service.files().create(
                            body=file_metadata, 
                            media_body=media,
                            supportsAllDrives=True # 關鍵：支持寫入他人分享的空間
                        ).execute()
                        print(f"✅ PDF 上傳成功: {safe_title}")
                    else:
                        print(f"⚠️ PDF 下載失敗 (HTTP {pdf_res.status_code})，轉為索引模式")
                        save_index(service, safe_title, doi, item.get('URL'), folder_id)
                else:
                    # 無 PDF 則存儲文獻索引 (TXT)
                    print(f"📑 無開放 PDF，保存索引文件: {safe_title}")
                    save_index(service, safe_title, doi, item.get('URL'), folder_id)
            except Exception as e:
                print(f"❌ 處理文件時出錯 ({safe_title}): {e}")

    except Exception as e:
        print(f"❌ 腳本運行崩潰: {e}")

def save_index(service, title, doi, url, folder_id):
    """保存索引 TXT 文件的輔助函數"""
    file_metadata = {'name': f"【索引】{title}.txt", 'parents': [folder_id]}
    idx_content = f"Title: {title}\nDOI: {doi}\nURL: {url}\nStatus: No Open Access PDF found."
    media = MediaIoBaseUpload(io.BytesIO(idx_content.encode('utf-8')), mimetype='text/plain')
    service.files().create(
        body=file_metadata, 
        media_body=media,
        supportsAllDrives=True
    ).execute()
    print(f"✅ 索引上傳成功: {title}")

# --- 4. 任務啟動 ---
if __name__ == "__main__":
    # 定義抓取任務與關鍵字
    TASKS = [
        {"cat": "Thought_Governance", "kws": ["Neo-Confucianism", "Chinese ancient administration"]},
        {"cat": "Document_Geography", "kws": ["Chinese Bibliography", "Historical Geography China"]},
        {"cat": "East_Asian_History", "kws": ["History of Korea", "Japanese History", "History of China"]}
    ]
    
    for task in TASKS:
        print(f"--- 正在處理分類: {task['cat']} ---")
        for kw in task['kws']:
            process_academic_papers(kw, FOLDER_MAP[task['cat']])
