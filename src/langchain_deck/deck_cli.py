import sys
from pathlib import Path

# 添加项目根目录到路径，以便导入 cli.py
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from cli import main

if __name__ == "__main__":
    main()

