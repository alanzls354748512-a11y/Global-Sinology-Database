import os
import datetime

def save_data_locally(category, title, content):
    """將數據保存到本地倉庫文件夾中"""
    # 建立存儲目錄
    folder_path = f"Data_Archive/{category}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # 檔名處理（加入時間戳防重複）
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')
    file_name = f"{folder_path}/{timestamp}_{safe_title}.txt"
    
    # 寫入內容
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(f"Timestamp: {datetime.datetime.now()}\n")
        f.write(f"Category: {category}\n")
        f.write(f"Title: {title}\n")
        f.write("-" * 30 + "\n")
        f.write(content)
    
    print(f"✅ [本地保存成功] 路徑: {file_name}")

if __name__ == "__main__":
    print("🚀 全球學術資料庫：GitHub 倉庫本地存儲模式啟動...")
    
    # 模擬正式抓取數據邏輯
    academic_data = [
        {'cat': 'Geography', 'title': 'NSS Supply Chain Resilience', 'content': 'Strategic analysis of energy sovereignty.'},
        {'cat': 'NSS_Analysis', 'title': 'Technological Decoupling Trend', 'content': 'Monitoring semi-conductor policy shifts.'},
        {'cat': 'East_Asian_History', 'title': 'Security Architecture Review', 'content': 'Historical dynamics in Asia-Pacific.'},
        {'cat': 'Thought_Gov', 'title': 'Governance Policy Brief', 'content': 'Evolution of modern governance thought.'}
    ]
    
    for item in academic_data:
        save_data_locally(item['cat'], item['title'], item['content'])

    print("🏁 數據處理完成，等待 GitHub Action 執行提交...")
