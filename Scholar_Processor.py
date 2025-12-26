import os
import datetime

# ========================================================
# 項目名稱：全球漢學學術抓取 (Global Sinology Academic Sync)
# 任務分組：當代儒學專項 (港臺新儒家 / 大陸新儒家)
# 核心邏輯：全球範圍掃描 + 特定流派領軍人物追蹤
# 存儲路徑：GitHub 倉庫 /Data_Archive/
# ========================================================

def save_academic_data(category, title, content, author="Unknown", is_leading_figure=False, school="General"):
    """
    保存漢學數據，新增『學術流派』標籤
    """
    base_folder = "Data_Archive"
    
    # 建立目錄結構：/分類/流派/人物權重
    if is_leading_figure:
        folder_path = f"{base_folder}/{category}/{school}/Leading_Figures"
    else:
        folder_path = f"{base_folder}/{category}/{school}/General_Research"
        
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    
    # 檔名規範：[日期]_[作者]_[標題前20字]
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    safe_author = "".join([c for c in author if c.isalnum()]).strip()
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')[:20]
    file_name = f"{folder_path}/{timestamp}_{safe_author}_{safe_title}.txt"
    
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write("【全球漢學學術抓取 - 儒學專項報告】\n")
            f.write(f"同步時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"學術流派: {school}\n")
            f.write(f"權重標註: {'⭐️ 領軍人物' if is_leading_figure else '🌐 常規監測'}\n")
            f.write(f"學者姓名: {author}\n")
            f.write(f"文章標題: {title}\n")
            f.write("-" * 50 + "\n")
            f.write(f"內容摘要:\n{content}\n")
            f.write("-" * 50 + "\n")
            f.write("獨立聲明：本數據與『全球金融數據庫』無關，嚴格隔離。\n")
        print(f"✅ [成功入庫] 流派: {school} | 作者: {author}")
    except Exception as e:
        print(f"❌ [寫入錯誤]: {str(e)}")

if __name__ == "__main__":
    print("🚀 全球漢學學術抓取：當代儒學流派監測啟動...")
    
    # 定義核心流派與領軍人物
    SCHOOLS_MAP = {
        "HK_TW_NeoConfucianism": ["杜維明", "劉述先", "成中英", "林安梧"],
        "Mainland_NeoConfucianism": ["蔣慶", "陳明", "張祥龍", "秋風"],
        "General_Sinology": ["葛兆光", "許倬雲", "汪暉"]
    }
    
    # 模擬抓取流：包含港臺與大陸新儒家的最新動態
    raw_data_stream = [
        {
            'cat': 'Thought_Gov',
            'author': '杜維明',
            'title': '精神人文主義與當代儒學的全球化路徑',
            'school': 'HK_TW_NeoConfucianism',
            'content': '論述儒家思想在現代文明對話中的核心價值。'
        },
        {
            'cat': 'Thought_Gov',
            'author': '蔣慶',
            'title': '廣義公羊學與大陸新儒家的政治實踐論',
            'school': 'Mainland_NeoConfucianism',
            'content': '針對大陸新儒家在政治哲學領域的體系化構建。'
        },
        {
            'cat': 'East_Asian_History',
            'author': '林安梧',
            'title': '血緣性角色與當代公民社會的張力',
            'school': 'HK_TW_NeoConfucianism',
            'content': '從新儒家視角分析東亞社會結構的變遷。'
        }
    ]
    
    for data in raw_data_stream:
        # 自動識別是否為領軍人物
        all_leaders = [name for sublist in SCHOOLS_MAP.values() for name in sublist]
        is_leader = data['author'] in all_leaders
        
        save_academic_data(
            category=data['cat'],
            title=data['title'],
            content=data['content'],
            author=data['author'],
            is_leading_figure=is_leader,
            school=data['school']
        )
    print("🏁 漢學儒學專項任務處理完成。")
