# 📚 高考英语词汇背诵助手

[![npm version](https://img.shields.io/npm/v/@uoh56456/gaokao-vocab)](https://www.npmjs.com/package/@uoh56456/gaokao-vocab)
[![license](https://img.shields.io/npm/l/@uoh56456/gaokao-vocab)](LICENSE)
[![platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)](https://github.com/lu87460353/Vocabulary)

基于 **React 18 + TypeScript + Vite + Electron** 构建的跨平台英语词汇学习桌面应用。融合四大词汇库（高考 / 考研 / 四级 / 六级），每个单词配备英式音标、词性标注、中文释义和双语例句，支持卡片背诵与交互测验双模式。

---

## 📖 目录

- [安装方式](#-安装方式)
- [使用说明](#-使用说明)
- [功能特色](#-功能特色)
- [词汇库说明](#-词汇库说明)
- [快捷键](#-快捷键)
- [数据存储](#-数据存储)
- [开发指南](#-开发指南)
- [项目结构](#-项目结构)
- [技术栈](#-技术栈)
- [打包说明](#-打包说明)
- [常见问题](#-常见问题)
- [许可证](#-许可证)

---

## 📦 安装方式

### Windows

```bash
# npm 安装
npm install -g @uoh56456/gaokao-vocab
gaokao-vocab
```

或从 [Releases](https://github.com/lu87460353/Vocabulary/releases) 下载 `VocabularyApp.exe` 双击运行。

### macOS

从 [Actions → Build macOS App](https://github.com/lu87460353/Vocabulary/actions/workflows/build-mac.yml) → 最新绿勾 → **Artifacts** → 下载 `vocabulary-mac-dmg`。

解压后双击 `词汇背诵助手.dmg`，拖入 `/Applications` 即可。

> macOS 首次打开提示"无法验证开发者"，前往 **系统设置 → 隐私与安全性 → 仍要打开**。

### Web 版（任何系统）

```bash
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary
npm install && npm run dev
```

浏览器打开 http://localhost:5173 即可使用。

---

## 🚀 使用说明

### 1. 选择词汇库

| 类别 | 适用场景 |
|------|---------|
| 🎓 高考词汇 | 高考英语备考 |
| 📚 考研词汇 | 考研英语备考 |
| 🏅 四级词汇 | CET-4 备考 |
| 🏆 六级词汇 | CET-6 备考 |

### 2. 学习模式

- **背诵模式**：卡片翻转 — 正面英文+音标，背面释义+例句
- **测验模式**：英译中选择题 + 听音拼写

### 3. 操作

| 动作 | 方式 |
|------|------|
| 翻转卡片 | 点击卡片 |
| 朗读单词 | 点击 🔊 按钮 |
| 标记掌握 | 点击「已掌握」 |
| 需要复习 | 点击「还没记住」 |
| 设置目标 | 底部「设置」→ 10/20/30/50 词/天 |
| 查看统计 | 底部「统计」→ 各类别进度 |

---

## ✨ 功能特色

| 功能 | 说明 |
|------|------|
| 📖 四大词汇库 | 高考 / 考研 / 四级 / 六级，一键切换 |
| 🔤 完整数据 | 英式音标 + 词性 + 中文释义 + 双语例句 |
| 🔄 背诵模式 | 3D 卡片翻转动画 |
| 🧠 测验模式 | 选择题 + 拼写题，即时判分 |
| 🔊 TTS 发音 | Web Speech API 美式发音 |
| 📊 学习追踪 | 掌握/学习中/未学习 三状态持久化 |
| 🎯 每日目标 | 10/20/30/50 词可调 |
| 💻 跨平台 | Windows EXE + macOS DMG + Web 版 |

---

## ⌨️ 快捷键

| 键 | 功能 |
|----|------|
| `Space` | 翻转卡片 |
| `←` `→` | 上/下一词 |
| `Enter` | 确认答案 |

---

## 💾 数据存储

所有学习进度存储在浏览器 `localStorage` 中，离线可用。桌面版使用内置 WebView 的 localStorage。

---

## 🔧 开发指南

```bash
# 克隆
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary
npm install

# 开发（浏览器）
npm run dev

# 开发（Electron 桌面窗口）
npm run dev

# 构建
npm run build

# 打包 Windows
npm run dist:win

# 打包 macOS
npm run dist:mac
```

---

## 📁 项目结构

```
Vocabulary/
├── src/                     # React 前端
│   ├── App.tsx              # 主应用
│   ├── components/          # 组件
│   │   ├── WordCard.tsx     # 3D 翻转卡片
│   │   ├── QuizMode.tsx     # 测验模式
│   │   ├── CategorySelector.tsx
│   │   ├── ProgressBar.tsx
│   │   └── StatsPanel.tsx
│   ├── data/vocabulary.ts   # 词库数据
│   ├── types/               # TS 类型
│   └── utils/storage.ts     # 存储工具
├── electron/                # Electron 桌面壳
│   ├── main.js              # 主进程
│   └── preload.js           # 预加载
├── dist/                    # Vite 构建产物
├── .github/workflows/       # CI/CD
│   ├── publish.yml          # npm 自动发布
│   └── build-mac.yml        # macOS DMG 构建
├── VocabularyApp.exe        # Windows 可执行文件
└── package.json
```

---

## 🛠 技术栈

| 层 | 技术 |
|----|------|
| 前端 | React 18 + TypeScript |
| 构建 | Vite 5 |
| 样式 | TailwindCSS 3 |
| 桌面壳 | Electron 28 |
| 打包 | electron-builder (Mac) / PyInstaller (Win) |
| CI/CD | GitHub Actions |

---

## 📦 打包说明

### Windows (.exe)
```bash
# pywebview 方式（轻量，14MB）
pyinstaller --onefile --windowed --add-data "dist;dist" launcher.py

# Electron 方式
npm run dist:win
```

### macOS (.dmg)
```bash
npm run dist:mac
# 或通过 CI → Actions → build-mac.yml → Artifacts
```

---

## ❓ 常见问题

**Q: Mac 打不开 DMG？**
A: 系统设置 → 隐私与安全性 → 仍要打开。

**Q: 发音没有声音？**
A: 检查系统音量，Windows/Mac 自带美式英语语音。

**Q: 如何备份进度？**
A: 桌面版进度在 WebView localStorage 中，卸载会丢失。建议定期导出。

**Q: 可以自定义词汇吗？**
A: 编辑 `src/data/vocabulary.ts` 添加即可。

---

## 📄 许可证

MIT License © uoh56456
