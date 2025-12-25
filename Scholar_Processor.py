import os, json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from docx import Document

# --- 1. 資料夾 ID 映射 (對標屏幕截图 315) ---
FOLDER_MAP = {
    'Document_Geography': '12Y0tfBUQ-B6VZPEVTLIFKlAleY9GIDSa', 
    'East_Asian_History': '1409gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4', 
    'Thought_Governance': '14H9f4hduc3QmmE3TAjnCtvNn36xdVHJU', 
    'Cross_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W' 
}

# --- 2. 首航測試論文內容 (示範數據) ---
TEST_PAPERS = [
    {"category": "Thought_Governance", "title": "宋代政治體制與理學傳播", "content": "本文探討朱子理學如何通過書院系統轉化為地方行政效能..."},
    {"category": "East_Asian_History", "title": "17世紀東亞海域貿易規律", "content": "研究明末清初東亞海域的地緣政治與白銀流向對比..."},
]

def upload_as_docx(text_content, title, category):
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict)
    service = build('drive', 'v3', credentials=creds)

    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(text_content)
    
    filename = f"{title}.docx"
    doc.save(filename)

    folder_id = FOLDER_MAP.get(category)
    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileUpload(filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
    service.files().create(body=file_metadata, media_body=media).execute()
    print(f"✅ 已成功歸檔至 {category}: {filename}")

# --- 執行自動化循環 ---
for paper in TEST_PAPERS:
    upload_as_docx(paper['content'], paper['title'], paper['category'])
