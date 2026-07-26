# 📚 高考英语词汇背诵助手

[![npm version](https://img.shields.io/npm/v/@uoh56456/gaokao-vocab)](https://www.npmjs.com/package/@uoh56456/gaokao-vocab)
[![license](https://img.shields.io/npm/l/@uoh56456/gaokao-vocab)](LICENSE)
[![platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](https://github.com/lu87460353/Vocabulary)

基于 **React 18 + TypeScript + Vite + Electron** 构建的跨平台桌面应用。专为英语学习者打造，融合四大权威词汇库（高考 / 考研 / 四级 / 六级），每个单词配备英式音标、词性标注、详细中文释义和双语例句，支持卡片翻转背诵与交互测验双模式。

---

## 目录

- [功能特色](#功能特色)
- [安装方式](#安装方式)
- [详细使用说明](#详细使用说明)
- [词汇库规格](#词汇库规格)
- [学习模式详解](#学习模式详解)
- [快捷键参考](#快捷键参考)
- [数据存储与备份](#数据存储与备份)
- [开发指南](#开发指南)
- [项目架构](#项目架构)
- [打包与发布](#打包与发布)
- [CI/CD 工作流](#cicd-工作流)
- [常见问题](#常见问题)
- [更新日志](#更新日志)
- [许可证](#许可证)

---

## 功能特色

### 核心功能

| 功能 | 说明 |
|------|------|
| 四大词汇库 | 高考 · 考研 · CET-4 · CET-6，一键无缝切换 |
| 完整单词数据 | 英式音标 (IPA) + 词性标注 + 中文释义 + 双语例句 |
| 卡片背诵模式 | 3D CSS 翻转动画，点击卡片查看释义 |
| 交互测验模式 | 英译中选择题 + 听音拼写题，即时判分统计 |
| 原生发音 | Web Speech API，标准美式英语发音 |
| 学习追踪 | 掌握 / 学习中 / 未学习 三状态可视化统计 |
| 每日目标 | 10 / 20 / 30 / 50 词/天，灵活调整 |
| 分类进度 | 各词汇库独立进度条 + 百分比 |
| Windows 支持 | EXE 单文件 (pywebview / Electron) |
| macOS 支持 | DMG 安装包 (Electron + electron-builder) |
| Linux 支持 | AppImage + deb (Electron + electron-builder) |
| Web 版 | 浏览器直接使用，无需安装 |

---

## 安装方式

### Windows

**npm 全局安装：**
```bash
npm install -g @uoh56456/gaokao-vocab
gaokao-vocab
```

**npx 免安装运行：**
```bash
npx @uoh56456/gaokao-vocab
```

**下载 EXE：**
从 [Releases](https://github.com/lu87460353/Vocabulary/releases) 下载 `VocabularyApp.exe`，双击运行。

首次运行可能弹出 Windows SmartScreen 警告：点击「更多信息」→「仍要运行」。

### macOS

1. 打开 [Actions → Build macOS App](https://github.com/lu87460353/Vocabulary/actions/workflows/build-mac.yml)
2. 点击最新一条绿勾运行
3. 滚动到底部 **Artifacts** 区域
4. 下载 `vocabulary-mac-dmg.zip`
5. 解压后双击 `词汇背诵助手.dmg`
6. 拖入 `/Applications` 文件夹

首次打开提示"无法验证开发者"：**系统设置 → 隐私与安全性 → 安全性 → 仍要打开**。

### Linux

1. [Actions - Build Linux App](https://github.com/lu87460353/Vocabulary/actions/workflows/build-linux.yml)
2. 最新绿勾 - Artifacts - 下载 `vocabulary-linux-appimage` 或 `vocabulary-linux-deb`
3. **AppImage**: `chmod +x *.AppImage && ./*.AppImage`
4. **deb**: `sudo dpkg -i *.deb`

### Web 版

```bash
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary
npm install
npm run dev
```

浏览器访问 http://localhost:5173。

---

## 详细使用说明

### 第一步：选择词汇库

首页四个彩色卡片：

- 高考词汇 — 高考英语备考
- 考研词汇 — 考研英语备考
- 四级词汇 — CET-4 备考
- 六级词汇 — CET-6 备考

点击卡片切换，每个词库学习进度独立。

### 第二步：选择学习模式

- **背诵模式**（默认）：逐词浏览，点击卡片翻转查看释义
- **测验模式**：选择题 + 拼写题，完成后显示得分

### 第三步：背诵模式操作

正面显示：单词 + 音标 + 发音按钮
背面显示：释义 + 例句（翻转 3D 动画）

底部四个评分按钮：

| 按钮 | 效果 |
|------|------|
| 忘记 | 标记「学习中」+ 加入错题集 |
| 不确定 | 标记「学习中」，下次复习 |
| 基本掌握 | 标记「学习中」，增加间隔 |
| 完全掌握 | 标记「已掌握」，不再出现 |

### 第四步：测验模式操作

- 选择题：看英文选中文释义（4 选 1）
- 拼写题：听发音 / 看中文 → 输入英文拼写
- 完成后显示总分和正确率

### 第五步：查看统计

底部「统计」页面：
- 总词数 / 已学习 / 已掌握 三项核心数据
- 今日完成进度实时更新
- 各分类独立进度条（百分比可视化）

### 第六步：设置每日目标

底部「设置」→ 选择：
- 10 词/天 — 轻度学习
- 20 词/天 — 推荐（约 15 分钟）
- 30 词/天 — 中等强度
- 50 词/天 — 高强度冲刺

---

## 词汇库规格

| 词库 | 来源 | 适用考试 |
|------|------|------|
| 高考 | 普通高中英语课程标准 | 高考英语 |
| 考研 | 全国硕士研究生入学考试大纲 | 考研英语 |
| 四级 | CET-4 考试大纲 | 大学英语四级 |
| 六级 | CET-6 考试大纲 | 大学英语六级 |

### 单词数据结构

```typescript
interface Word {
  id: string;          // 唯一标识，如 "gaokao-1"
  word: string;        // 英文单词
  phonetic: string;    // 英式音标 (IPA)
  meaning: string;     // 词性 + 中文释义
  example: string;     // 双语例句（英文 + 中文翻译）
  category: Category;  // 所属词库
}
```

### 自定义添加词汇

编辑 `src/data/vocabulary.ts`：

```typescript
{
  id: 'gaokao-xxx',
  word: 'perseverance',
  phonetic: '/ˌpɜːsɪˈvɪərəns/',
  meaning: 'n. 坚持不懈，毅力',
  example: 'Perseverance leads to success. 坚持就是胜利。',
  category: 'gaokao',
}
```

---

## 快捷键参考

| 快捷键 | 页面 | 功能 |
|--------|------|------|
| Space | 背诵 | 翻转卡片查看释义 |
| → | 背诵 | 下一词 |
| ← | 背诵 | 上一词 |
| Enter | 测验 | 确认答案 |

---

## 数据存储与备份

所有进度存储在 `localStorage` 中：

| Key | 内容 |
|-----|------|
| `vocab-progress` | 每个单词的学习状态 |
| `vocab-settings` | 当前词库、模式、每日目标 |

桌面版（Electron）缓存路径：

| 系统 | 路径 |
|------|------|
| Windows | `%APPDATA%\词汇背诵助手\` |
| macOS | `~/Library/Application Support/词汇背诵助手/` |

卸载应用会清除数据。可点击「设置 → 重置所有数据」清空进度。

---

## 开发指南

### 环境要求

- Node.js >= 18.0.0
- npm >= 9.0.0

### 快速开始

```bash
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary
npm install
npm run dev
```

### 可用命令

| 命令 | 说明 |
|------|------|
| `npm run dev` | 启动开发服务器 + Electron 窗口 |
| `npm run build` | TypeScript 类型检查 + Vite 生产构建 |
| `npm run preview` | 预览生产构建 |
| `npm run dist:win` | 打包 Windows .exe |
| `npm run dist:mac` | 打包 macOS .dmg |
| `npm run dist:linux` | 打包 Linux AppImage/deb |

### 项目结构

```
Vocabulary/
├── src/                     # React 前端源码
│   ├── App.tsx              # 主应用组件
│   ├── components/          # UI 组件
│   │   ├── WordCard.tsx     # 单词卡片（3D 翻转）
│   │   ├── QuizMode.tsx     # 测验答题
│   │   ├── CategorySelector.tsx
│   │   ├── ProgressBar.tsx
│   │   └── StatsPanel.tsx
│   ├── data/vocabulary.ts   # 词库数据
│   ├── types/vocabulary.ts  # TS 类型定义
│   └── utils/storage.ts     # localStorage 工具
├── electron/                # Electron 桌面壳
│   ├── main.js              # 主进程
│   └── preload.js           # 预加载脚本
├── dist/                    # Vite 构建产物
├── .github/workflows/       # CI/CD
│   ├── publish.yml          # npm 自动发布
│   └── build-mac.yml        # macOS DMG 构建
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
└── README.md
```

---

## 项目架构

```
+-------------------------------------+
|           Electron Shell            |
|  +-------------------------------+  |
|  |      React Application        |  |
|  |  App.tsx -> Components        |  |
|  |  WordCard / QuizMode / Stats  |  |
|  |          localStorage         |  |
|  +-------------------------------+  |
|  Web Speech API | WebView         |
+-------------------------------------+
```

- **展示层**：React 组件 + TailwindCSS 样式
- **数据层**：localStorage 键值存储
- **桌面层**：Electron 提供原生窗口、菜单
- **发音层**：Web Speech API（浏览器内置）

---

## 打包与发布

### Windows (.exe)

```bash
# pywebview（轻量 ~14 MB）
pip install pywebview pyinstaller
pyinstaller --onefile --windowed --add-data "dist;dist" --name VocabularyApp launcher.py

# Electron
npm run dist:win
```

### macOS (.dmg)

```bash
npm run dist:mac
```

### npm 发布

```bash
npm publish
# 或通过 CI — push 到 main 自动触发
```

---

## CI/CD 工作流

### npm 自动发布

push main + package.json 变更 → 自动 `npm publish`

### macOS DMG 构建

push main/master 或手动触发 → macos-latest → 构建 .dmg → 上传 Artifacts

状态查看：https://github.com/lu87460353/Vocabulary/actions

---

## 常见问题

**Q: Windows EXE 没反应？**
A: 杀毒软件可能拦截。加入白名单或以管理员身份运行。

**Q: macOS "无法验证开发者"？**
A: 系统设置 → 隐私与安全性 → 仍要打开。

**Q: 发音没有声音？**
A: 检查系统音量。Windows 和 macOS 都自带美式英语语音。

**Q: 如何重置数据？**
A: 底部「设置」→ 重置所有数据。

**Q: 可以离线使用吗？**
A: 可以。所有数据存储在本地。

**Q: 如何添加新词汇？**
A: 编辑 `src/data/vocabulary.ts`，按格式添加后重新 `npm run build`。

---

## 更新日志

| 版本 | 日期 | 内容 |
|------|------|------|
| 3.3.x | 2026-07 | 跨平台支持、Electron 桌面壳、macOS DMG CI |
| 3.2.x | 2026-07 | React 重构、四大词库、测验模式、npm 发布 |
| 1.0.0 | 2026-07 | 初始版本 |

---

## 许可证

MIT License © uoh56456
