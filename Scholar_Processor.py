import os
import sys

# --- 核心兼容性修复：针对独立学术数据库环境 ---
# 解决 importlib.metadata.packages_distributions 报错
try:
    if sys.version_info >= (3, 10):
        from importlib.metadata import packages_distributions
    else:
        # 如果环境低于 3.10，则调用后备库
        from importlib_metadata import packages_distributions
except ImportError:
    # 极简回退方案，防止程序彻底中断
    def packages_distributions():
        return {}
# ----------------------------------------------

def upload_to_gdrive(title, url, folder_id):
    """
    将抓取的独立学术数据同步至 Google Drive。
    修正了报错截图 Line 46 处的 service 调用逻辑。
    """
    try:
        # 确保 service 已经初始化
        if 'service' not in globals():
            print("Error: Google Drive API service is not defined.")
            return

        file_metadata = {
            'name': title,
            'parents': [folder_id]
        }
        
        # 执行上传任务
        file = service.files().create(
            body=file_metadata, 
            fields='id'
        ).execute()
        
        print(f"✅ 学术条目同步成功: {title} (ID: {file.get('id')})")

    except Exception as e:
        print(f"❌ 抓取条目上传失败: {title}")
        print(f"报错详情: {str(e)}")
        # 独立运行模式下，单个错误不应阻塞后续数据的抓取
        pass

if __name__ == "__main__":
    print("🚀 Global Sinology Academic Sync: 独立抓取任务启动...")
    # 这里接入您原本的 Google Scholar 抓取或 API 调用逻辑
