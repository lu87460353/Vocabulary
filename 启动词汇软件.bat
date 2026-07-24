@echo off
chcp 65001 >nul
echo ============================================
echo   高考英语词汇背诵软件 GaokaoVocab
echo   基于《普通高中英语课程标准(2017-2025)》
echo ============================================
echo.
echo 词汇来源: 3100+ 高考课标词汇
echo 功能: 每日计划 / 间隔重复 / 错题本 / TTS发音
echo       写作模板 / 听力练习 / 学习进度
echo.
echo 正在启动...
start "" "%~dp0dist\GaokaoVocab.exe"
