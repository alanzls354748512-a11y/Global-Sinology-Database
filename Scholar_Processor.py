import os, json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from docx import Document

# --- 1. 核心配置：漢學資料夾 ID 映射 (已對標您的 G 盤目錄) ---
FOLDER_MAP = {
    'Document_Geography': '12Y0tfBUQ-B6VZPEVTLIFKlAleY9GIDSa',
    'East_Asian_History': '1409gDpMZT0Ew3-J2t6Sbr-6BffZH4gZ4',
    'Thought_Governance': '14H9f4hduc3QmmE3TAjnCtvNn36xdVHJU',
    'Cross_Analysis': '1BxkNCkitbw-YMO0BDcQzdOG6KmXEXR0W'
}

# --- 2. 漢學自動化採集引擎 (純學術邏輯，不涉及經濟) ---
def generate_sinology_report(keyword):
    """
    根據關鍵字自動生成漢學學術監測簡報。
    未來可在此函數內對接特定漢學數據庫的爬蟲邏輯。
    """
    content = f"""
    【漢學學術每日監測 - 關鍵字：{keyword}】
    
    1. 研究領域動態：
    當前針對「{keyword}」的研究正聚焦於新出土文獻與海外漢學家的新詮釋。
    
    2. 核心學術重點：
    涉及該課題在傳統目錄學中的定位、史料來源的考辨，以及跨地域文史互證的研究方法。
    
    3. 檔案庫建議：
    此內容已自動分類並存檔，建議定期查閱相關領域的最新期刊論文摘要。
    """
    return content

def upload_as_docx(text_content, title, category):
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        return
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
    
    try:
        service.files().create(body=file_metadata, media_body=media).execute()
        print(f"✅ 漢學資產已歸檔: {filename}")
    except Exception as e:
        print(f"❌ 歸檔失敗: {str(e)}")

# --- 3. 每日採集任務清單 (純漢學關鍵字設定) ---
if __name__ == "__main__":
    SINOLOGY_TASKS = [
        {"kw": "出土文獻與簡帛文字研究", "cat": "Document_Geography"},
        {"kw": "唐代政治體制與官職演變", "cat": "East_Asian_History"},
        {"kw": "宋明理學中的基層倫理建構", "cat": "Thought_Governance"},
        {"kw": "明清筆記中的東亞史料考證", "cat": "Cross_Analysis"}
    ]
    
    for task in SINOLOGY_TASKS:
        report = generate_sinology_report(task['kw'])
        upload_as_docx(report, f"漢學監測_{task['kw']}", task['cat'])
