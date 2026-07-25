# 📚 高考英语词汇背诵助手

[![npm version](https://img.shields.io/npm/v/@uoh56456/gaokao-vocab)](https://www.npmjs.com/package/@uoh56456/gaokao-vocab)
[![license](https://img.shields.io/npm/l/@uoh56456/gaokao-vocab)](LICENSE)

基于 React + TypeScript + Vite 构建的英语词汇学习桌面应用。支持高考、考研、四级、六级四大词汇库，涵盖音标、词性、中文释义和例句，提供背诵与测验双模式。

## ✨ 功能特色

| 功能 | 说明 |
|------|------|
| 📖 四大词汇库 | 高考 / 考研 / 四级 / 六级，自由切换 |
| 🔄 双学习模式 | 背诵模式（卡片翻转）+ 测验模式（选择/拼写） |
| 🔊 TTS 发音 | Web Speech API 原生发音 |
| 📊 学习追踪 | 掌握 / 学习中 / 未学习 三状态统计 |
| 🎯 每日目标 | 可设置 10/20/30/50 词/天 |
| 💻 桌面应用 | pywebview 原生窗口，14.6MB 单文件 EXE |

## 📦 安装

```bash
# npm 全局安装
npm install -g @uoh56456/gaokao-vocab

# 启动
gaokao-vocab
```

或者直接下载 [VocabularyApp.exe](https://github.com/lu87460353/Vocabulary/releases) 双击运行。

## 🚀 开发

```bash
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary
npm install
npm run dev       # 开发服务器
npm run build     # 生产构建
```

## 🛠 技术栈

| 层 | 技术 |
|----|------|
| 框架 | React 18 + TypeScript |
| 构建 | Vite 5 |
| 样式 | TailwindCSS 3 |
| 图标 | Lucide React |
| 打包 | pywebview + PyInstaller |

## 📁 项目结构

```
Vocabulary/
├── src/
│   ├── App.tsx                    # 主应用组件
│   ├── components/
│   │   ├── WordCard.tsx           # 单词卡片（翻转动画）
│   │   ├── QuizMode.tsx           # 测验模式
│   │   ├── CategorySelector.tsx   # 词汇库选择器
│   │   ├── ProgressBar.tsx        # 进度条
│   │   └── StatsPanel.tsx         # 统计面板
│   ├── data/
│   │   └── vocabulary.ts          # 词汇数据
│   ├── types/
│   │   └── vocabulary.ts          # TypeScript 类型
│   └── utils/
│       └── storage.ts             # localStorage 存储
├── dist/                          # 构建产物
├── launcher.py                    # 桌面启动器
├── VocabularyApp.exe              # Windows 可执行文件
└── package.json
```

## 📄 许可证

MIT License © uoh56456
