@echo off

rem 切换到脚本所在目录
cd /d "%~dp0"

rem 激活Python环境（如果需要）
rem call activate your_env

rem 运行爬虫脚本
python crawl_hot_search.py

rem 暂停查看结果（可选）
rem pause