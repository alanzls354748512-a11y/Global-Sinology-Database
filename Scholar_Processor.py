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
        print("❌ 錯誤：GitHub Secrets 中找不到 GDRIVE_CREDENTIALS")
        return None
    try:
        # 需要同時具備 Sheets 和 Drive 讀寫權限
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file'
        ]
        creds_dict = json.loads(creds_json, strict=False)
        print(f"🤖 執行帳號確認: {creds_dict.get('client_email')}")
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
        return build('sheets', 'v4', credentials=creds)
    except Exception as e:
        print(f"❌ 認證初始化失敗: {str(e)}")
        return None

def write_to_sheet(service, spreadsheet_id, sheet_name, title, content):
    """將抓取的學術數據追加到 Google Sheets 的下一列"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 準備寫入的三欄數據：時間戳、文章標題、內容摘要
        values = [[timestamp, title, content]]
        body = {'values': values}
        
        # A:C 代表寫入前三欄
        range_name = f"'{sheet_name}'!A:C"
        
        service.spreadsheets().values().append(
            spreadsheet_id=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        
        print(f"✅ [寫入成功] 分類: {sheet_name} | 標題: {title}")
    except Exception as e:
        print(f"❌ [寫入失敗] 分類 {sheet_name} 報錯: {str(e)}")
        print("👉 提示：請確認 Sheet 名稱是否與試算表下方的標籤完全一致。")

if __name__ == "__main__":
    print("🚀 全球學術資料庫：Sheets 自動化模式啟動...")
    service = get_sheets_service()
    
    if service:
        # ⚠️ 根據截圖 366 提取的長 ID ⚠️
        SPREADSHEET_ID = '1APWo1JMaI5R2WAIr2le2AIBF6m3PMmDaXptszX_fDIc'
        
        # 這裡模擬正式抓取後的數據分配邏輯
        test_payload = [
            {
                'title': 'NSS_Strategic_Supply_Chain_Report_2025', 
                'content': 'Strategic Analysis: Global supply chain resilience under NSS framework.', 
                'cat': 'Geography'
            },
            {
                'title': 'East_Asian_History_Dynamics_Q4', 
                'content': 'Historical review: Regional security architecture evolution.', 
                'cat': 'East_Asian_History'
            },
            {
                'title': 'Cross_Analysis_Technological_Decoupling', 
                'content': 'NSS Cross-sectional data: Monitoring semi-conductor decoupling trends.', 
                'cat': 'NSS_Analysis'
            },
            {
                'title': 'Thought_Governance_Policy_Brief', 
                'content': 'Policy evolution and governance thought in modern geopolitics.', 
                'cat': 'Thought_Gov'
            }
        ]
        
        for item in test_payload:
            write_to_sheet(service, SPREADSHEET_ID, item['cat'], item['title'], item['content'])

    print("🏁 任務結束。請查看 Google Sheets 內容。")
