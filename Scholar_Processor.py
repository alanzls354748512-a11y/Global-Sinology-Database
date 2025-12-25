import os, json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from docx import Document

# 1. 您的專屬 ID 配置
FOLDER_MAP = {
    'Document_Geography': '12Y0tfBUQ-B6VZPEVTLIFKlAleY9GIDSa',
    'East_Asian_History': '1409gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',
    'Thought_Governance': '14H9f4hduc3QmmE3TAjnCtvNn36xdVHJU',
    'Cross_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W'
}

def upload_test_file(category, title, content):
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict)
    service = build('drive', 'v3', credentials=creds)

    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(content)
    filename = f"{title}.docx"
    doc.save(filename)

    folder_id = FOLDER_MAP.get(category)
    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileUpload(filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
    service.files().create(body=file_metadata, media_body=media).execute()
    print(f"✅ 已存入 {category}: {filename}")

# 2. 執行首航採集測試
if __name__ == "__main__":
    upload_test_file('Thought_Governance', '朱子理學與南宋地方治理', '測試內容：探討理學思想如何轉化為基層行政邏輯...')
    upload_test_file('East_Asian_History', '17世紀東亞海域與地緣戰略', '測試內容：分析德川幕府與明清更替下的貿易規律...')
