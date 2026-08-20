@echo off
REM ============================================================
REM 小红书 AI 关键词抓取
REM ============================================================

setlocal
set "MC_HOME=%~dp0MediaCrawler"
set "DATA_DIR=%~dp0datahotlist_xhs"

if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"

cd /d "%MC_HOME%"

echo ============================================================
echo 小红书 AI 关键词抓取
echo ============================================================

python main.py ^
  --platform xhs ^
  --lt qrcode ^
  --type search ^
  --keywords "AI工具,AI编程,WorkBuddy,提示词" ^
  --save_data_option jsonl ^
  --save_data_path "%DATA_DIR%" ^
  --get_comment false ^
  --crawler_max_notes_count 50

endlocal
