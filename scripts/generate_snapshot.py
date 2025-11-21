import os

from pathlib import Path
from datetime import datetime

# ================= 配置区域 =================

# 目标扫描目录
TARGET_DIR = Path(__file__).parent

# 输出文件名
OUTPUT_FILE = "project_snapshot.md"

# 需要包含的文件后缀 (只抓取这些代码文件)
INCLUDE_EXTENSIONS = {
    '.py', '.html', '.css', '.js', '.json', '.md', '.txt', '.yaml', '.yml'
}

# 需要忽略的文件夹
IGNORE_DIRS = {
    '.git', '.idea', '.vscode', '__pycache__', 'venv', 'env', 
    'html_output', 'logs', 'output', 'tests/__pycache__'
}

# 需要忽略的具体文件
IGNORE_FILES = {
    'project_structure.txt', OUTPUT_FILE, 'package-lock.json', 
    'generate_tree.py', 'generate_snapshot.py'
}

# ===========================================

def is_ignored(path: Path):
    """检查路径是否应该被忽略"""
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
    if path.name in IGNORE_FILES:
        return True
    return False

def generate_snapshot():
    snapshot_content = []
    file_count = 0
    
    # 写入头部信息
    snapshot_content.append(f"# Project Snapshot: {TARGET_DIR.name}")
    snapshot_content.append(f"> Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    snapshot_content.append("## 1. File List")
    
    file_list_buffer = []
    code_content_buffer = []
    
    # 遍历目录
    for root, dirs, files in os.walk(TARGET_DIR):
        # 修改 dirs 列表以跳过忽略的目录 (原地修改影响 walk)
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in sorted(files):
            file_path = Path(root) / file
            
            # 检查是否忽略
            if is_ignored(file_path):
                continue
                
            # 检查后缀
            if file_path.suffix.lower() not in INCLUDE_EXTENSIONS:
                continue
                
            # 获取相对路径
            rel_path = file_path.relative_to(TARGET_DIR)
            
            file_count += 1
            file_list_buffer.append(f"- `{rel_path}`")
            
            # 读取内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 添加文件头和代码块
                ext = file_path.suffix.lstrip('.')
                # 映射 markdown 语言标识
                if ext == 'py': lang = 'python'
                elif ext == 'js': lang = 'javascript'
                elif ext == 'html': lang = 'html'
                else: lang = ''
                
                code_content_buffer.append(f"\n## File: {rel_path}\n")
                code_content_buffer.append(f"```{lang}\n{content}\n```\n")
                
            except Exception as e:
                print(f"⚠️ 无法读取文件 {rel_path}: {e}")
                code_content_buffer.append(f"\n## File: {rel_path}\n(Error reading file: {e})\n")
    
    # 组装最终内容
    snapshot_content.extend(file_list_buffer)
    snapshot_content.append("\n---\n")
    snapshot_content.append("## 2. Code Contents")
    snapshot_content.extend(code_content_buffer)
    
    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(snapshot_content))
        
    print(f"✅ 代码快照已生成: {OUTPUT_FILE}")
    print(f"📊 共包含 {file_count} 个文件")

if __name__ == "__main__":
    generate_snapshot()

