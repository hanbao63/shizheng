#!/bin/zsh

cd "$(dirname "$0")"

# 1. 重新生成 index.html
/usr/bin/python3 build.py

# 2. 暂存所有变更
git add .

# 3. 自动提交（有变更才提交）
git diff --cached --quiet || git commit -m "sync: update pages $(date '+%Y-%m-%d %H:%M')"

# 4. 推送到远程
git push

echo ""
echo "按 Enter 键关闭此窗口"
read
