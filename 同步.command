#!/bin/zsh
 cd "$(dirname "$0")"
/usr/bin/python3 build.py
echo ""
echo "按 Enter 键关闭此窗口"
read
