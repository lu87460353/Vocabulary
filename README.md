# 📚 高考英语词汇背诵软件 - GaokaoVocab

[![npm version](https://img.shields.io/npm/v/@uoh56456/gaokao-vocab)](https://www.npmjs.com/package/@uoh56456/gaokao-vocab)
[![License](https://img.shields.io/npm/l/@uoh56456/gaokao-vocab)](LICENSE)

基于《普通高中英语课程标准（2017 年版 2025 年修订）》的Windows英语词汇学习软件。

> **🎯 适用于**: 高考备战、高中英语学习、词汇积累

---

## ✨ 功能特色

| 功能 | 说明 |
|------|------|
| 📖 **2514课标词汇** | 完整音标、词性、中文释义，覆盖新课标全部词汇 |
| 📅 **每日学习计划** | 自动生成新词+复习计划，SM-2间隔重复算法 |
| 📕 **错题本** | 答错自动记录，支持单独复习 |
| 🔊 **TTS发音** | Windows原生语音朗读 |
| ✍️ **写作真题** | 2023-2024高考真题+范文（12篇），6种书信模板 |
| 🎧 **听力练习** | 听音识词，错词乱序重练 |
| 🤖 **AI助手** | 支持OpenAI/DeepSeek/通义千问等API，语法辨析/翻译/润色 |
| 📊 **学习统计** | 进度条、连续学习天数、掌握率可视化 |

## 📦 安装

```bash
# 全局安装（推荐）
npm install -g @uoh56456/gaokao-vocab

# 或使用npx直接运行
npx @uoh56456/gaokao-vocab
```

## 🚀 使用

安装后运行：

```bash
gaokao-vocab
```

或者直接双击 `dist/GaokaoVocab.exe`。

### 首次使用

1. 软件自动创建数据库，无需手动配置
2. 在 **⚙️ 设置** 中可调整每日新词数量（默认20个/天）
3. 如需AI助手，在 **🤖 AI** → **⚙️ API设置** 中填入API Key
4. AI助手支持：OpenAI、DeepSeek、通义千问、智谱GLM等

### 系统要求

- **操作系统**: Windows 10/11 (64位)
- **运行时**: Python 3.9+（使用exe无需安装Python）
- **发音功能**: 需 Windows TTS（系统自带）

## 📁 项目结构

```
GaokaoVocab/
├── dist/GaokaoVocab.exe   # Windows可执行文件
├── vocab_app.py           # Tkinter GUI主程序
├── database.py            # SQLite数据库模块
├── dictionary.py          # 内置词典（2700+词条）
├── parsed_words.json      # 2514词汇完整数据(音标/词性/释义)
├── vocab_words.json       # 课标词汇表
├── bin/gaokao-vocab.js    # npm启动脚本
├── package.json           # npm包配置
└── 启动词汇软件.bat        # Windows快捷启动
```

## 📄 词汇来源

- 《普通高中英语课程标准（2017 年版 2025 年修订）》词汇表
- 共 2514 个单词，含音标、词性、中文释义
- 标注等级：基础 (1600) / 必修* (500) / 选择性必修** (1000)

## 📊 技术栈

- **前端**: Python Tkinter (原生GUI)
- **数据库**: SQLite (本地存储)
- **打包**: PyInstaller (单文件exe)
- **算法**: SM-2 间隔重复 (Spaced Repetition)
- **TTS**: Windows SAPI (语音合成)
- **AI**: OpenAI 兼容 API (可插拔)

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📝 许可证

MIT License

Copyright (c) 2025 uoh56456
