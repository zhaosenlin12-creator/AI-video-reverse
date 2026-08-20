@echo off
REM ============================================================
REM 抖音创作者主页数据抓取（AI四小只 账号）
REM 包装 MediaCrawler CLI 调用
REM ============================================================

setlocal
set "MC_HOME=%~dp0MediaCrawler"
set "SEC_UID=MS4wLjABAAAAQg5TgrTfWN0FphobcDhritBsLl8V3SS5H3ckUfdrXrI"
set "DATA_DIR=%~dp0datacreator"

if not exist "%DATA_DIR%" mkdir "%DATA_DIR%"

cd /d "%MC_HOME%"

echo ============================================================
echo 抖音创作者主页抓取 - AI四小只
echo sec_uid: %SEC_UID%
echo 输出: %DATA_DIR%
echo ============================================================

python main.py ^
  --platform dy ^
  --lt qrcode ^
  --type creator ^
  --creator_id "%SEC_UID%" ^
  --save_data_option jsonl ^
  --save_data_path "%DATA_DIR%" ^
  --get_comment true ^
  --crawler_max_notes_count 30

endlocal
