import os

from pathlib import Path

# ================= 配置区域 =================

# 目标扫描目录 (默认为当前脚本所在目录)
TARGET_DIR = Path(__file__).parent

# 扫描深度限制
MAX_DEPTH = 4

# 需要忽略的文件夹和文件
IGNORE_LIST = {
    '.git', '.idea', '.vscode', '__pycache__', 'venv', 'env', 
    'node_modules', '.DS_Store', 'html_output', 'logs', 'dist', 'build',
    'generate_tree.py', 'generate_snapshot.py' # 忽略脚本自身
}

# ===========================================

def generate_tree(dir_path: Path, prefix: str = "", depth: int = 0):
    if depth > MAX_DEPTH:
        return ""
    
    output = ""
    
    try:
        # 获取目录下所有内容并排序（文件夹在前，文件在后）
        items = sorted(
            [x for x in dir_path.iterdir()],
            key=lambda x: (not x.is_dir(), x.name.lower())
        )
    except PermissionError:
        return ""
    # 过滤忽略项
    items = [i for i in items if i.name not in IGNORE_LIST]
    
    total_items = len(items)
    
    for index, item in enumerate(items):
        is_last = (index == total_items - 1)
        connector = "└── " if is_last else "├── "
        
        # 添加当前项
        output += f"{prefix}{connector}{item.name}\n"
        
        # 如果是文件夹，递归处理
        if item.is_dir():
            extension = "    " if is_last else "│   "
            output += generate_tree(item, prefix + extension, depth + 1)
            
    return output

if __name__ == "__main__":
    print(f"🔍 正在扫描目录结构: {TARGET_DIR.name} (深度: {MAX_DEPTH})...\n")
    
    tree_str = f"{TARGET_DIR.name}/\n"
    tree_str += generate_tree(TARGET_DIR)
    
    # 保存到文件
    output_file = "project_structure.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(tree_str)
        
    print(tree_str)
    print(f"\n✅ 目录树已保存到: {output_file}")

