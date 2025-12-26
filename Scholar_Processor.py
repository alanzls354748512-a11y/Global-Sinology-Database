import os
import datetime

# ========================================================
# 項目名稱：全球漢學學術抓取 (獨立項目)
# 功能：自動化對接 CNKI, NCPSS 及全球漢學中心，強化領軍人物監控
# 存儲邏輯：GitHub 倉庫本地存儲 (Data_Archive/)
# ========================================================

def save_academic_data(category, title, content, author="Unknown", is_leading_figure=False):
    """
    將抓取到的漢學數據保存到本地倉庫，並標註領軍人物
    """
    # 建立存儲路徑 (確保與金融數據庫完全隔離)
    base_folder = "Data_Archive"
    if is_leading_figure:
        folder_path = f"{base_folder}/{category}/Leading_Figures"
    else:
        folder_path = f"{base_folder}/{category}/General_Research"
        
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # 檔名處理：[時間戳]_[作者]_[標題].txt
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    safe_author = "".join([c for c in author if c.isalnum()]).strip()
    safe_title = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')[:50]
    file_name = f"{folder_path}/{timestamp}_{safe_author}_{safe_title}.txt"
    
    # 寫入學術規範格式內容
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(f"【全球漢學學術抓取 - 每日監控報告】\n")
        f.write(f"同步時間: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"學術分類: {category}\n")
        f.write(f"領軍人物: {'是 (High Priority)' if is_leading_figure else '否'}\n")
        f.write(f"作者/學科帶頭人: {author}\n")
        f.write(f"文章標題: {title}\n")
        f.write("="*40 + "\n")
        f.write(f"摘要內容:\n{content}\n")
        f.write("="*40 + "\n")
        f.write(f"數據來源預計對接: CNKI(知網海外版), NCPSS(國家哲社中心), 各大漢學中心\n")
    
    print(f"✅ [漢學數據入庫] {file_name}")

if __name__ == "__main__":
    print("🚀 全球漢學學術抓取：學科帶頭人監控模式啟動...")
    
    # 模擬當前強化的抓取荷載 (包含領軍人物定向追蹤)
    # 這些數據與 NSS 框架對齊，但獨立於金融邏輯
    academic_payload = [
        {
            'cat': 'Thought_Gov',
            'author': '葛兆光',
            'title': '從「宅茲中國」看傳統治理思想的現代轉向',
            'content': '本文深度探討了中國傳統空間觀念與現代治理邏輯的互動，屬於漢學大師定向監控成果。',
            'is_leader': True
        },
        {
            'cat': 'NSS_Analysis',
            'author': '閻學通',
            'title': '數字時代下的地緣政治競爭與學術定調',
            'content': '針對技術脫鉤背景下的國際關係演變進行了最新學術研判。',
            'is_leader': True
        },
        {
            'cat': 'East_Asian_History',
            'author': '許倬雲',
            'title': '萬古江河：亞太安全架構的歷史長河演變',
            'content': '從長時段歷史視角審視亞太地區的穩定與衝突脈絡。',
            'is_leader': True
        },
        {
            'cat': 'Geography',
            'author': 'CNKI_Regional_Team',
            'title': '一帶一路沿線關鍵節點的區域地理韌性研究',
            'content': '基於知網與中國地學期刊網的最新區域地理研究摘要。',
            'is_leader
