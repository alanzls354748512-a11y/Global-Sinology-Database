import os, json, requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# --- 1. 核心路徑配置 ---
# 請確保以下資料夾已在 Google Drive 介面中「共用」給 Service Account Email
FOLDER_MAP = {
    'Thought_Governance': '14H9f4hduc3QmmE3TAjnCtvNn36xdVHJU', 
    'Document_Geography': '12Y0tfBUQ-B6VZPEVTLIFKlAleY9GIDSa', 
    'East_Asian_History': '1409gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4', 
}

# --- 2. PDF 下載引擎 (Unpaywall API) ---
def get_pdf_link(doi):
    """透過 DOI 尋找合法的免費 PDF 下載鏈接"""
    email = "alanzls354748512@gmail.com" 
    url = f"https://api.unpaywall.org/v2/{doi}?email={email}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            best_link = data.get('best_oa_location', {})
            if best_link:
                return best_link.get('url_for_pdf')
    except Exception as e:
        print(f"⚠️ Unpaywall API 錯誤: {e}")
        return None
    return None

# --- 3. 執行抓取與上傳 ---
def process_academic_papers(keyword, folder_id):
    search_url = f"https://api.crossref.org/works?query={keyword}&sort=published&order=desc&rows=3"
    headers = {'User-Agent': 'GlobalSinologyBot/1.0'}
    
    try:
        response = requests.get(search_url, headers=headers)
        if response.status_code != 200: return

        items = response.json().get('message', {}).get('items', [])
        
        creds_json = os.environ.get('GDRIVE_CREDENTIALS')
        if not creds_json:
            print("❌ 找不到 GDRIVE_CREDENTIALS")
            return
            
        creds = service_account.Credentials.from_service_account_info(
            json.loads(creds_json),
            scopes=['https://www.googleapis.com/auth/drive']
        )
        service = build('drive', 'v3', credentials=creds)

        for item in items:
            title = item.get('title', ['Untitled'])[0]
            # 清理檔名特殊字符以防系統錯誤
            safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '.', '_')]).strip()
            doi = item.get('DOI')
            pdf_url = get_pdf_link(doi) if doi else None

            try:
                if pdf_url:
                    print(f"📥 下載 PDF: {safe_title}")
                    pdf_res = requests.get(pdf_url, timeout=20)
                    if pdf_res.status_code == 200:
                        pdf_data = pdf_res.content
                        file_metadata = {'name': f"{safe_title}.pdf", 'parents': [folder_id]}
                        media = MediaIoBaseUpload(io.BytesIO(pdf_data), mimetype='application/pdf')
                        # 核心修復：supportsAllDrives=True 確保寫入權限
                        service.files().create(
                            body=file_metadata, 
                            media_body=media,
                            supportsAllDrives=True 
                        ).execute()
                        print(f"✅ 上傳成功: {safe_title}")
                else:
                    print(f"📑 存儲索引: {safe_title}")
                    file_metadata = {'name': f"【索引】{safe_title}.txt", 'parents': [folder_id]}
                    idx_content = f"Title: {title}\nDOI: {doi}\nURL: {item.get('URL')}"
                    media = MediaIoBaseUpload(io.BytesIO(idx_content.encode()), mimetype='text/plain')
                    service.files().create(
                        body=file_metadata, 
                        media_body=media,
                        supportsAllDrives=True
                    ).execute()
                    print(f"✅ 索引已保存: {safe_title}")
            except Exception as e:
                print(f"❌ 檔案操作失敗: {e}")

    except Exception as e:
        print(f"❌ 腳本執行錯誤: {e}")

# --- 4. 24/7 調度進入點 ---
if __name__ == "__main__":
    TASKS = [
        {"cat": "Thought_Governance", "kws": ["Neo-Confucianism", "Chinese ancient administration"]},
        {"cat": "Document_Geography", "kws": ["Chinese Bibliography", "Historical Geography China"]},
        {"cat": "East_Asian_History", "kws": ["History of Korea", "Japanese History", "History of China"]}
    ]
    
    for task in TASKS:
        for kw in task['kws']:
            process_academic_papers(kw, FOLDER_MAP[task['cat']])
