import os, json, requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# --- 1. 核心路徑配置 ---
FOLDER_MAP = {
    'Thought_Governance': '14H9f4hduc3QmmE3TAjnCtvNn36xdVHJU', # 宋明理學、古代行政
    'Document_Geography': '12Y0tfBUQ-B6VZPEVTLIFKlAleY9GIDSa', # 版本目錄、經學、地理
    'East_Asian_History': '1409gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4', # 中、韓、日史
}

# --- 2. PDF 下載引擎 (Unpaywall API) ---
def get_pdf_link(doi):
    """透過 DOI 尋找合法的免費 PDF 下載鏈接"""
    email = "alanzls354748512@gmail.com" # 您的聯絡信箱，API 要求
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            best_link = data.get('best_oa_location', {})
            if best_link:
                return best_link.get('url_for_pdf')
    except:
        return None
    return None

# --- 3. 執行抓取與上傳 ---
def process_academic_papers(keyword, folder_id):
    # 使用 CrossRef 抓取最新論文元數據
    search_url = f"https://api.crossref.org/works?query={keyword}&sort=published&order=desc&rows=3"
    headers = {'User-Agent': 'GlobalSinologyBot/1.0'}
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200: return

    items = response.json().get('message', {}).get('items', [])
    
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    creds = service_account.Credentials.from_service_account_info(json.loads(creds_json))
    service = build('drive', 'v3', credentials=creds)

    for item in items:
        title = item.get('title', ['Untitled'])[0]
        doi = item.get('DOI')
        pdf_url = get_pdf_link(doi) if doi else None

        if pdf_url:
            # 執行 PDF 下載並上傳至 G 盤
            print(f"📥 發現 PDF: {title}")
            pdf_data = requests.get(pdf_url).content
            file_metadata = {'name': f"{title}.pdf", 'parents': [folder_id]}
            media = MediaIoBaseUpload(io.BytesIO(pdf_data), mimetype='application/pdf')
            service.files().create(body=file_metadata, media_body=media).execute()
        else:
            # 若無 PDF，則存儲文獻索引 (TXT)
            file_metadata = {'name': f"【索引】{title}.txt", 'parents': [folder_id]}
            idx_content = f"Title: {title}\nDOI: {doi}\nURL: {item.get('URL')}"
            media = MediaIoBaseUpload(io.BytesIO(idx_content.encode()), mimetype='text/plain')
            service.files().create(body=file_metadata, media_body=media).execute()

# --- 4. 24/7 任務調度 ---
if __name__ == "__main__":
    TASKS = [
        {"cat": "Thought_Governance", "kws": ["Neo-Confucianism", "Chinese ancient administration"]},
        {"cat": "Document_Geography", "kws": ["Chinese Bibliography", "Historical Geography China"]},
        {"cat": "East_Asian_History", "kws": ["History of Korea", "Japanese History", "History of China"]}
    ]
    
    for task in TASKS:
        for kw in task['kws']:
            process_academic_papers(kw, FOLDER_MAP[task['cat']])
