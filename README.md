# trae-bug-0907
复现 Trae 生成的 bat 在 Win11 乱码、手动启动失败的全过程。

## 环境
- Win11 家庭中文版 24H2 (Build 26100.4061)
- Python 3.13.7 安装路径：D:\Dev\Python311
- Trae 0.9.3

## 复现步骤
1. 双击 `start.bat` → PowerShell 出现乱码
2. 手动执行 `2048.py` → 报错“此应用无法在你的电脑上使用”

## 报错信息
## 已尝试（未解决）
- 把 Trae 默认路径改到 D 盘
- 用 chcp 65001 切换代码页

## 下一步
- 验证 bat 文件编码是否为 UTF-8-BOM
- 用 `call` 命令包装 python 路径
