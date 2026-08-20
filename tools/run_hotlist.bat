@echo off
REM ============================================================
REM 抖音 AI 关键词热榜抓取
REM ============================================================

setlocal
set "MC_HOME=%~dp0MediaCrawler"
set "DATA_DIR=%~dp0datahotlist"

if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"

cd /d "%MC_HOME%"

echo ============================================================
echo 抖音 AI 关键词热榜抓取
echo ============================================================

python main.py ^
  --platform dy ^
  --lt qrcode ^
  --type search ^
  --keywords "AI工具,AI编程,WorkBuddy,AI Agent" ^
  --save_data_option jsonl ^
  --save_data_path "%DATA_DIR%" ^
  --get_comment false ^
  --crawler_max_notes_count 50

endlocal
