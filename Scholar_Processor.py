import os
import datetime

# ========================================================
# 項目名稱：全球漢學學術抓取 (Global Sinology Academic Sync)
# 項目屬性：獨立項目 (與全球金融數據庫完全隔離)
# 核心邏輯：全球範圍掃描 + 領軍人物權重匹配
# 存儲路徑：GitHub 倉庫 /Data_Archive/
# ========================================================

def save_academic_data(category, title, content, author="Unknown", is_leading_figure=False, source="Global_Network"):
    """
    兼顧全球抓取與領軍人物動態的保存函數
    """
    base_folder = "Data_Archive"
    
    # 根據權重決定存儲子目錄
    if is_leading_figure:
        folder_path = f"{base_folder}/{category}/Leading_Figures_Focus"
    else:
        folder_path = f"{base_folder}/{category}/Global_General_Research"
        
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)
    
    # 檔名規範：[日期]_[作者]_[來源簡寫]_[標題前20字]
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    safe_author = "".join([c for c in author if c.isalnum()]).strip()
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')[:20]
    file_name = f"{folder_path}/{timestamp}_{safe_author}_{source}_{safe_title}.txt"
    
    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write("【全球漢學學術抓取 - 獨立監測報告】\n")
            f.write(f"同步時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"數據來源: {source}\n")
            f.write(f"學術分類: {category}\n")
            f.write(f"權重標註: {'⭐️ 領軍人物/學科帶頭人' if is_leading_figure else '🌐 全球廣域掃描'}\n")
            f.write(f"學者/團隊: {author}\n")
            f.write(f"文章/動態標題: {title}\n")
            f.write("-" * 50 + "\n")
            f.write(f"學術摘要/內容細節:\n{content}\n")
            f.write("-" * 50 + "\n")
            f.write("聲明：本項目數據獨立於『全球金融數據庫』，專注於漢學與地緣歷史研究。\n")
        print(f"✅ [入庫成功] 分類: {category} | 來源: {source} | 檔案: {file_name}")
    except Exception as e:
        print(f"❌ [寫入出錯]: {str(e)}")

if __name__ == "__main__":
    print("🚀 全球漢學學術抓取任務啟動...")
    
    # 定義監控大師名單 (學術雷達)
    MASTERS_LIST = ["葛兆光", "許倬雲", "閻學通", "茅海建", "汪暉", "許紀霖"]
    
    # 模擬全球雙軌抓取流 (JSTOR, CNKI, NCPSS, Scholar)
    raw_data_stream = [
        {
            'cat': 'Thought_Gov',
            'author': '葛兆光',
            'title': '宅茲中國：傳統治理觀的現代重構',
            'content': '本文論述了中國傳統空間意識與國家治理的內在邏輯。',
            'source': 'CNKI_Overseas'
        },
        {
            'cat': 'NSS_Analysis',
            'author': 'CFR_Sinology_Panel',
            'title': 'Strategic Shifts in East Asian Security History',
            'content': 'Analysis of regional stability patterns through a historical lens.',
            'source': 'Scholar_Global'
        },
        {
            'cat': 'Geography',
            'author': 'NCPSS_Researcher',
            'title': '邊疆地理與環境韌性研究綜述',
            'content': '基於國家哲社中心的最新學術產出。',
            'source': 'NCPSS_CN'
        }
    ]
    
    for data in raw_data_stream:
        # 自動權重匹配
        is_leader = any(master in data['author'] for master in MASTERS_LIST)
        save_academic_data(
            category=data['cat'],
            title=data['title'],
            content=data['content'],
            author=data['author'],
            is_leading_figure=is_leader,
            source=data['source']
        )
    print("🏁 漢學任務處理完成。")
