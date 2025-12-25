import os, json, requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from docx import Document

# --- 1. 配置資料夾 ID (已填入您的專屬坐標) ---
FOLDER_MAP = {
    'Document_Geography': '12Y0tfBUQ-B6VZPEVTLIFKlAleY9GIDSa',
    'East_Asian_History': '1409gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',
    'Thought_Governance': '14H9f4hduc3QmmE3TAjnCtvNn36xdVHJU',
    'Cross_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W'
}

def upload_as_docx(text_content, title, category):
    # 初始化 Google Drive API
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict)
    service = build('drive', 'v3', credentials=creds)

    # 建立可編輯的 Word 文檔
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(text_content)
    
    filename = f"{title}.docx"
    doc.save(filename)

    # 上傳至對應子資料夾
    folder_id = FOLDER_MAP.get(category)
    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileUpload(filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
    try:
        service.files().create(body=file_metadata, media_body=media).execute()
        print(f"✅ {category} 歸檔成功: {filename}")
    except Exception as e:
        print(f"❌ 歸檔失敗: {str(e)}")

# 腳本後續將自動執行學術檢索迴圈...
