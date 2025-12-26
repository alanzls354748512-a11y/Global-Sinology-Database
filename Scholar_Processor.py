import os
import datetime

# ========================================================
# 項目名稱：全球漢學學術抓取 (獨立項目)
# 核心邏輯：全球範圍掃描 + 領軍人物權重匹配
# 存儲邏輯：GitHub 倉庫本地存儲 (Data_Archive/)
# ========================================================

def save_academic_data(category, title, content, author="Unknown", is_leading_figure=False, source="Global_Network"):
    """
    兼顧全球抓取與領軍人物動態的保存函數
    """
    # 建立基礎目錄
    base_folder = "Data_Archive"
    
    # 根據是否為領軍人物決定存儲權重路徑
    if is_leading_figure:
        folder_path = f"{base_folder}/{category}/Leading_Figures_Focus"
    else:
        folder_path = f"{base_folder}/{category}/Global_General_Research"
        
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    
    # 檔名規範：[日期]_[作者]_[來源簡寫]_[標題摘要].txt
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    safe_author = "".join([c for c in author if c.isalnum()]).strip()
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')[:25]
    file_name = f"{folder_path}/{timestamp}_{safe_author}_{source}_{safe_title}.txt"
    
    # 寫入結構化學術摘要
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write("【全球漢學學術抓取 - 24/7 自動化監測報告】\n")
            f.write(f"同步時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"數據來源: {source}\n")
            f.write(f"學術分類: {category}\n")
            f.write(f"權重標註: {'⭐️ 領軍人物/學科帶頭人' if is_leading_figure else '🌐 全球常規掃描'}\n")
            f.write(f"學者/團隊: {author}\n")
            f.write(f"文章/動態標題: {title}\n")
            f.write("-" * 50 + "\n")
            f.write(f"學術摘要/內容細節:\n{content}\n")
            f.write("-" * 50 + "\n")
            f.write("獨立項目標記：本數據與『全球金融數據庫』完全隔離，僅供漢學研究參考。\n")
        print(f"✅ [入庫成功] 分類: {category} | 來源: {source} | 檔案: {file_name}")
    except Exception as e:
        print(f"❌ [寫入出錯]: {str(e)}")

if __name__ == "__main__":
    print("🚀 全球漢學學術抓取：雙軌並行監測模式啟動...")
    
    # 1. 定義監控大師名單 (用於自動權重匹配)
    MASTERS_LIST = ["葛兆光", "許倬雲", "閻學通", "茅海建", "汪暉"]
    
    # 2. 模擬全球抓取到的數據流 (涵蓋全球平臺與本土知網/哲社中心)
    raw_data_stream = [
        {
            'cat': 'Thought_Gov',
            'author': '葛兆光',
            'title': '傳統中國的天下觀與當代治理啟示',
            'content': '本文深度剖析了漢學脈絡下的政治哲學。',
            'source': 'CNKI_CN'
        },
        {
            'cat': 'NSS_Analysis',
            'author': 'Harvard_Sinology_Group',
            'title': 'Analysis of Supply Chain Resilience in East Asian History',
            'content': 'A comprehensive study on historical trade route stability.',
            'source': 'JSTOR_Global'
        },
        {
            'cat': 'East_Asian_History',
            'author': 'SOAS_London',
            'title': 'New Archaeological Findings in Maritime Silk Road',
            'content': 'Recent academic updates on maritime trade dynamics.',
            'source': 'Scholar_Global'
        },
        {
            'cat': 'Geography',
            'author': 'NCPSS_Researcher',
            'title': '邊疆地理與國家安全邊界的學術演進',
            'content': '基於國家哲社中心的最新地緣研究報告。',
            'source': 'NCPSS_CN'
        }
    ]
    
    # 3. 執行匹配與入庫邏輯
    for data in raw_data_stream:
        # 自動識別是否為領軍人物
        is_leader = any(master in data['author'] for master in MASTERS_LIST)
        
        save_academic_data(
            category=data['cat'],
            title=data['title'],
            content=data['content'],
            author=data['author'],
            is_leading_figure=is_leader,
            source=data['source']
        )

    print(f"🏁 漢學同步任務結束。數據已歸檔至 Data_Archive/ 目錄。")
