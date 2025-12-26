import sys
import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_sheets_service():
    """初始化 Google Sheets API 服務"""
    creds_json = os.environ.get('GDRIVE_CREDENTIALS')
    if not creds_json:
        print("❌ 錯誤：Secrets 未配置")
        return None
    try:
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds_dict = json.loads(creds_json, strict=False)
        print(f"🤖 執行帳號: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"❌ 認證失敗: {str(e)}")
        return None

def write_to_sheet(service, spreadsheet_id, sheet_name, title, content):
    """將學術數據精確追加到指定的分頁"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        values = [[timestamp, title, content]]
        body = {'values': values}
        
        # 使用更寬鬆的範圍定義 'SheetName'!A1
        range_name = f"'{sheet_name}'!A1"
        
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, 
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        
        print(f"✅ [寫入成功] 分頁: {sheet_name} | 數據已入庫")
    except Exception as e:
        print(f"❌ [寫入失敗] 分頁 {sheet_name} 報錯: {str(e)}")
        if "404" in str(e):
            print(f"👉 建議：請手動重命名試算表下方的 '{sheet_name}' 標籤，確保沒有前後空格。")

if __name__ == "__main__":
    print("🚀 全球學術資料庫：數據入庫最終校準...")
    service = get_sheets_service()
    
    if service:
        # 已校對的試算表 ID (來自截圖 366/381)
        SPREADSHEET_ID = '1APWo1JMaI5R2WAIr2le2AIBF6m3PMmDaXptszX_fDIc'
        
        # 嚴格對應截圖 381 下方標籤頁
        test_payload = [
            {'title': 'Geography_NSS_Strategic_Update', 'content': 'Supply chain resilience data.', 'cat': 'Geography'},
            {'title': 'East_Asian_History_Summary', 'content': 'Regional security architecture history.', 'cat': 'East_Asian_History'},
            {'title': 'NSS_Cross_Analysis_2025', 'content': 'Technological decoupling monitoring.', 'cat': 'NSS_Analysis'},
            {'title': 'Thought_Gov_Policy_Review', 'content': 'Governance thought evolution.', 'cat': 'Thought_Gov'}
        ]
        
        for item in test_payload:
            write_to_sheet(service, SPREADSHEET_ID, item['cat'], item['title'], item['content'])

    print("🏁 診斷任務執行結束。")
