import os

from pathlib import Path

# ================= 配置区域 =================

# 目标扫描目录
TARGET_DIR = Path(__file__).parent

# 输出文件名
OUTPUT_FILE = "project_snapshot_lite.md"

# 【白名单】只包含这些核心代码后缀
INCLUDE_EXTENSIONS = {
    '.py', 
    # '.json', # 建议暂时注释掉json，因为你的config目录里有些json可能很大，除非你确定需要
}

# 【黑名单】忽略的目录（根据你的 tree 结构定制）
IGNORE_DIRS = {
    # 版本控制与环境
    '.git', '.idea', '.vscode', '__pycache__', 'venv', 'env', 
    
    # 输出产物（体积大，非源码）
    'html_output', 
    'html_debug', 
    'outputs', 
    'test_outputs', 
    'replicated_outputs', 
    'charts',
    
    # 文档（非代码逻辑）
    'docs', 
    
    # 示例与临时文件
    'examples',
    'debug',
    
    # 缓存
    'tests/__pycache__'
}

# 【黑名单】忽略的具体文件名
IGNORE_FILES = {
    'project_structure.txt', 
    'project_snapshot.md', 
    'project_snapshot_lite.md',
    'package-lock.json', 
    'generate_tree.py', 
    'generate_snapshot.py',
    'generate_snapshot_optimized.py',
    'requirements.txt',
    'README.md'
}

# 【黑名单】忽略的文件后缀
IGNORE_SUFFIXES = {
    '.log', '.pptx', '.docx', '.png', '.jpg', '.jpeg', '.gif'
}

# ===========================================

def is_ignored(path: Path):
    """检查路径是否应该被忽略"""
    # 1. 检查目录黑名单
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
            
    # 2. 检查文件名黑名单
    if path.name in IGNORE_FILES:
        return True
        
    # 3. 检查后缀黑名单
    if path.suffix.lower() in IGNORE_SUFFIXES:
        return True
        
    # 4. 特殊规则：忽略所有 debug 开头的文件
    if path.name.startswith('debug_') or path.name.startswith('quick_debug'):
        return True

    return False

def generate_snapshot():
    snapshot_content = []
    file_count = 0
    
    # 写入头部信息
    snapshot_content.append(f"# Project Snapshot (Lite): {TARGET_DIR.name}")
    snapshot_content.append("> Optimized for LLM Context Context\n")
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
                
            # 检查后缀（只在白名单内）
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
                lang = 'python' if ext == 'py' else ext
                
                code_content_buffer.append(f"\n## File: {rel_path}\n")
                code_content_buffer.append(f"```{lang}\n{content}\n```\n")
                
            except Exception as e:
                print(f"⚠️ 无法读取文件 {rel_path}: {e}")

    # 组装最终内容
    snapshot_content.extend(file_list_buffer)
    snapshot_content.append("\n---\n")
    snapshot_content.append("## 2. Code Contents")
    snapshot_content.extend(code_content_buffer)
    
    # 写入文件
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(snapshot_content))
        
    print(f"✅ 精简版代码快照已生成: {OUTPUT_FILE}")
    print(f"📊 共包含 {file_count} 个核心代码文件")

if __name__ == "__main__":
    generate_snapshot()

