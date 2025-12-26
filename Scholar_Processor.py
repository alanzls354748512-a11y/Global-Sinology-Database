import sys
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_sheets_service():
    """初始化 Google Sheets API 服務"""
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：Secrets 未配置")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds_dict = json.loads(creds_json, strict=False)
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"❌ 認證失敗: {str(e)}")
        return None

def write_to_sheet(service, spreadsheet_id, sheet_name, title, content):
    """將學術抓取數據寫入指定的工作表"""
    try:
        # 準備寫入的行數據：時間、標題、內容摘要
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = [[timestamp, title, content[:500]]] # 寫入前 500 字作為摘要
        
        body = {'values': values}
        range_name = f"{sheet_name}!A:C"
        
        service.spreadsheets().values().append(
            spreadsheet_id=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        
        print(f"✅ [寫入成功] 分類: {sheet_name} | 標題: {title}")
    except Exception as e:
        print(f"❌ [寫入失敗] 分類 {sheet_name} 報錯: {str(e)}")

if __name__ == "__main__":
    print("🚀 全球學術資料庫：Sheets 兼容模式啟動 (繞過配額限制)...")
    service = get_sheets_service()
    
    if service:
        # ⚠️ 請在此處填入您新建的 Google Sheets 網址中的長 ID ⚠️
        # 網址格式：https://docs.google.com/spreadsheets/d/您的ID/edit
        SPREADSHEET_ID = '在此填入您的試算表ID' 
        
        test_payload = [
            {'title': 'NSS_Final_Success_2025', 'content': 'Status: Sheets channel active. Strategic monitoring stabilized.', 'cat': 'NSS_Analysis'},
            {'title': 'Geography_Resilience_Update', 'content': 'Supply chain resilience data via Sheets.', 'cat': 'Geography'}
        ]
        
        for item in test_payload:
            write_to_sheet(service, SPREADSHEET_ID, item['cat'], item['title'], item['content'])

    print("🏁 任務結束。請查看 Google Sheets 內容。")
