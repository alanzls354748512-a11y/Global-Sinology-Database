import os, json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from docx import Document

# --- 1. 核心配置：路徑與 ID 精確映射 (對標您的 G 盤目錄) ---
FOLDER_MAP = {
    'Document_Geography': '12Y0tfBUQ-B6VZPEVTLIFKlAleY9GIDSa',
    'East_Asian_History': '1409gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',
    'Thought_Governance': '14H9f4hduc3QmmE3TAjnCtvNn36xdVHJU',
    'Cross_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W'
}

# --- 2. 首航測試論文內容 (產出首批 docx 資產) ---
TEST_PAPERS = [
    {
        "category": "Thought_Governance", 
        "title": "朱子理學與南宋地方治理邏輯", 
        "content": "本文探討理學思想如何轉化為古代基層行政效能，並對標現代政權治理模型..."
    },
    {
        "category": "East_Asian_History", 
        "title": "17世紀東亞海域貿易與地緣戰略分析", 
        "content": "分析明清交替時期，東亞海域的白銀流向如何影響當時的區域金融穩定..."
    },
    {
        "category": "Cross_Analysis", 
        "title": "NSS框架下的東亞歷史週期研究", 
        "content": "結合美國國家安全戰略（NSS）邏輯，分析東亞歷史變遷對現代供應鏈韌性的啟示..."
    }
]

def upload_as_docx(text_content, title, category):
    # 從 GitHub Secrets 獲取憑證
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：未找到 GDRIVE_CREDENTIALS 密鑰")
        return

    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict)
    service = build('drive', 'v3', credentials=creds)

    # 建立可編輯的 Word 文檔
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(text_content)
    
    filename = f"{title}.docx"
    doc.save(filename)

    # 獲取對應資料夾 ID
    folder_id = FOLDER_MAP.get(category)
    if not folder_id:
        print(f"⚠️ 找不到類別 {category} 對應的 ID")
        return

    # 上傳至 Google Drive
    file_metadata = {'name': filename, 'parents': [folder_id]}
    media = MediaFileUpload(filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    
    try:
        service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"✅ 已成功歸檔至 {category}: {filename}")
    except Exception as e:
        print(f"❌ 歸檔 {filename} 失敗: {str(e)}")

# --- 執行程序 ---
if __name__ == "__main__":
    for paper in TEST_PAPERS:
        upload_as_docx(paper['content'], paper['title'], paper['category'])
