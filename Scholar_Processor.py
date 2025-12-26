import os
import datetime

# ========================================================
# 項目名稱：全球漢學學術抓取 (Global Sinology Academic Sync)
# 任務分組：當代儒學專項 + 中國政治經濟學研究 (王滬寧專項)
# 核心邏輯：全球廣域掃描 + 代表人物學術脈絡追蹤
# 存儲路徑：GitHub 倉庫 /Data_Archive/
# ========================================================

def save_academic_data(category, title, content, author="Unknown", is_leading_figure=False, school="General"):
    """
    保存漢學數據，新增『政治經濟學』與『代表人物』標籤
    """
    base_folder = "Data_Archive"
    
    # 建立階層目錄：/分類/流派或專項/人物等級
    folder_type = "Leading_Figures" if is_leading_figure else "General_Research"
    folder_path = f"{base_folder}/{category}/{school}/{folder_type}"
        
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    
    # 檔名規範：[日期]_[作者]_[標題前20字].txt
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    safe_author = "".join([c for c in author if c.isalnum()]).strip()
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')[:20]
    file_name = f"{folder_path}/{timestamp}_{safe_author}_{safe_title}.txt"
    
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write("【全球漢學學術抓取 - 政經與思想專項】\n")
            f.write(f"同步時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"學術領域: {school}\n")
            f.write(f"權重標註: {'⭐️ 核心代表人物/理論源頭' if is_leading_figure else '🌐 常規監測'}\n")
            f.write(f"學者/機構: {author}\n")
            f.write(f"研究標題: {title}\n")
            f.write("-" * 50 + "\n")
            f.write(f"核心摘要:\n{content}\n")
            f.write("-" * 50 + "\n")
            f.write("獨立聲明：本數據僅供漢學與政治思想研究，與『全球金融數據庫』嚴格隔離。\n")
        print(f"✅ [入庫成功] 領域: {school} | 作者: {author}")
    except Exception as e:
        print(f"❌ [系統報錯]: {str(e)}")

if __name__ == "__main__":
    print("🚀 全球漢學學術抓取：政治經濟學與儒學雙軌任務啟動...")
    
    # 定義核心人物與流派雷達
    MASTERS_RADAR = {
        "China_Political_Economy": ["王滬寧", "林毅夫", "溫鐵軍"],
        "HK_TW_NeoConfucianism": ["杜維明", "林安梧"],
        "Mainland_NeoConfucianism": ["蔣慶", "陳明"],
        "General_Sinology": ["葛兆光", "汪暉"]
    }
    
    # 模擬全球抓取流：涵蓋政治經濟學與新儒家
    raw_data_stream = [
        {
            'cat': 'Thought_Gov',
            'author': 'Fudan_Academic_Review',
            'title': '從《比較政治分析》看當代中國治理結構的演進',
            'school': 'China_Political_Economy',
            'content': '回溯與分析王滬寧政治學思想對現代化國家治理的長期影響。',
            'is_leader': True
        },
        {
            'cat': 'Thought_Gov',
            'author': '杜維明',
            'title': '儒家學說與全球倫理的對話',
            'school': 'HK_TW_NeoConfucianism',
            'content': '論述當代儒學在國際政經秩序中的精神價值。',
            'is_leader': True
        },
        {
            'cat': 'NSS_Analysis',
            'author': 'Mainland_Scholar_Group',
            'title': '新權威主義理論在數字經濟時代的實踐與反思',
            'school': 'China_Political_Economy',
            'content': '探討政治經濟學中權力配置與經濟效率的關係。',
            'is_leader': False
        }
    ]
    
    for data in raw_data_stream:
        save_academic_data(
            category=data['cat'],
            title=data['title'],
            content=data['content'],
            author=data['author'],
            is_leading_figure=data.get('is_leader', False),
            school=data['school']
        )
    print("🏁 漢學與政經專項任務同步結束。")
