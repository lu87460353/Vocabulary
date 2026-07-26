# 📚 高考英语词汇背诵助手

[![npm version](https://img.shields.io/npm/v/@uoh56456/gaokao-vocab)](https://www.npmjs.com/package/@uoh56456/gaokao-vocab)
[![license](https://img.shields.io/npm/l/@uoh56456/gaokao-vocab)](LICENSE)
[![platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-blue)](https://github.com/lu87460353/Vocabulary)
[![GitHub Actions](https://github.com/lu87460353/Vocabulary/actions/workflows/build-mac.yml/badge.svg)](https://github.com/lu87460353/Vocabulary/actions)

基于 **React 18 + TypeScript + Vite + Electron** 构建的跨平台桌面应用。专为英语学习者打造，融合四大权威词汇库（高考 · 考研 · 四级 · 六级），每个单词配备英式音标、词性标注、详细中文释义和双语例句，支持卡片翻转背诵与交互测验双模式。

---

## 📖 目录

- [功能特色](#-功能特色)
- [安装方式](#-安装方式)
- [详细使用说明](#-详细使用说明)
- [词汇库规格](#-词汇库规格)
- [学习模式详解](#-学习模式详解)
- [快捷键参考](#-快捷键参考)
- [数据存储与备份](#-数据存储与备份)
- [开发指南](#-开发指南)
- [项目架构](#-项目架构)
- [打包与发布](#-打包与发布)
- [CI/CD 工作流](#-cicd-工作流)
- [常见问题](#-常见问题)
- [更新日志](#-更新日志)
- [许可证](#-许可证)

---

## ✨ 功能特色

### 核心功能

| 功能 | 说明 | 状态 |
|------|------|:--:|
| 📖 四大词汇库 | 高考 · 考研 · CET-4 · CET-6，一键无缝切换 | ✅ |
| 🔤 完整单词数据 | 英式音标 (IPA) + 词性标注 + 中文释义 + 双语例句 | ✅ |
| 🔄 卡片背诵模式 | 3D CSS 翻转动画，点击卡片查看释义 | ✅ |
| 🧠 交互测验模式 | 英译中选择题 + 听音拼写题，即时判分统计 | ✅ |
| 🔊 原生发音 | Web Speech API，标准美式英语发音 | ✅ |
| 📊 学习追踪 | 掌握 / 学习中 / 未学习 三状态可视化统计 | ✅ |
| 🎯 每日目标 | 10 / 20 / 30 / 50 词/天，灵活调整 | ✅ |
| 📈 分类进度 | 各词汇库独立进度条 + 百分比 | ✅ |
| 💻 Windows 支持 | EXE 单文件 (pywebview / Electron) | ✅ |
| 🍎 macOS 支持 | DMG 安装包 (Electron + electron-builder) | ✅ |
| 🌐 Web 版 | 浏览器直接使用，无需安装 | ✅ |
| 🔄 CI/CD | GitHub Actions 自动构建 + npm 自动发布 | ✅ |

### 学习辅助

| 功能 | 说明 |
|------|------|
| 📝 错词追踪 | 测试中错误的单词高亮标记 |
| 🔁 反复练习 | "还没记住" 状态的单词可重复浏览 |
| 📅 连续打卡 | 今日学习进度实时更新 |
| 🔄 进度重置 | 一键清除所有数据重新开始 |

---

## 📦 安装方式

### Windows

#### 方式一：npm 全局安装
```bash
npm install -g @uoh56456/gaokao-vocab
gaokao-vocab
```

#### 方式二：npx 免安装运行
```bash
npx @uoh56456/gaokao-vocab
```

#### 方式三：下载 EXE
从 [GitHub Releases](https://github.com/lu87460353/Vocabulary/releases) 下载 `VocabularyApp.exe`，双击即用。

> 首次运行可能弹出 Windows SmartScreen 警告 → 点击「更多信息」→「仍要运行」

### macOS

#### 方式一：下载 DMG（推荐）
1. 打开 [Actions → Build macOS App](https://github.com/lu87460353/Vocabulary/actions/workflows/build-mac.yml)
2. 点击最新一次 ✅ 绿勾运行
3. 滚动到页面底部 **Artifacts** 区域
4. 下载 `vocabulary-mac-dmg.zip`
5. 解压 → 双击 `词汇背诵助手.dmg`
6. 拖入 `/Applications` 文件夹

#### 方式二：开发环境运行
```bash
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary
npm install
npm run dev
```

> macOS 首次打开提示 "无法验证开发者"：
> **系统设置 → 隐私与安全性 → 安全性 → 仍要打开**

### Web 版（跨平台）

```bash
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary
npm install
npm run dev
# 浏览器访问 http://localhost:5173
```

---

## 🚀 详细使用说明

### 第一步：启动应用

- **Windows**：双击 `VocabularyApp.exe` 或命令行输入 `gaokao-vocab`
- **macOS**：从 `应用程序` 文件夹打开 `词汇背诵助手`
- **Web**：浏览器访问 `http://localhost:5173`

### 第二步：选择词汇库

应用首页展示四个彩色词汇卡片：

```
┌──────────────┐  ┌──────────────┐
│  🎓 高考词汇  │  │  📚 考研词汇  │
│  高考英语备考  │  │  考研英语备考  │
└──────────────┘  └──────────────┘
┌──────────────┐  ┌──────────────┐
│  🏅 四级词汇  │  │  🏆 六级词汇  │
│  CET-4 备考   │  │  CET-6 备考   │
└──────────────┘  └──────────────┘
```

点击任意卡片即切换到对应词库，学习进度完全独立。

### 第三步：选择学习模式

首页下方两个模式按钮：

- **📖 背诵模式**（蓝色高亮）：逐词浏览记忆
- **🧠 测验模式**（绿色高亮）：答题检验学习效果

选好后点击「开始学习」进入。

### 第四步：背诵模式操作

```
      ┌─────────────────────┐
      │        🔊            │  ← 点击朗读
      │                      │
      │      abandon         │  ← 英文单词
      │    /əˈbændən/        │  ← 英式音标
      │                      │
      │  点击卡片查看释义    │
      └─────────────────────┘
               │
               ↓ 点击翻转 (3D动画)
               │
      ┌─────────────────────┐
      │      abandon         │
      │    /əˈbændən/        │
      │                      │
      │  v. 放弃，抛弃；     │  ← 词性 + 释义
      │     n. 放任，放纵    │
      │                      │
      │  He decided to       │  ← 双语例句
      │  abandon his plan.   │
      │  他决定放弃他的计划。│
      └─────────────────────┘

  底部按钮：[😰 忘记][🤔 不确定][🙂 基本掌握][😎 完全掌握]
```

**按钮说明：**

| 按钮 | 效果 |
|------|------|
| 😰 忘记 | 标记「学习中」+ 加入错题集 |
| 🤔 不确定 | 标记「学习中」，下次继续复习 |
| 🙂 基本掌握 | 标记「学习中」，增加复习间隔 |
| 😎 完全掌握 | 标记「已掌握」，不再出现 |

### 第五步：测验模式操作

选择测验模式后进入答题界面：

**选择题型：**
```
┌──────────────────────────────┐
│  abandon 是什么意思？        │
│                              │
│  A. 放弃，抛弃               │  ← 正确答案
│  B. 接受，同意               │
│  C. 完成，实现               │
│  D. 继续，坚持               │
└──────────────────────────────┘
```

**拼写题型：**
```
┌──────────────────────────────┐
│  🔊 听到发音了吗？           │
│  请输入正确的英文拼写：       │
│  ┌──────────────────────┐    │
│  │ ______________       │    │
│  └──────────────────────┘    │
│                              │
│  提示：v. 放弃，抛弃         │
└──────────────────────────────┘
```

答完全部题目后显示总分和正确率。

### 第六步：查看统计

底部导航栏点击「统计」：

```
┌──────────┬──────────┬──────────┐
│  📚 总词数 │  ✅ 已学习 │  🏆 已掌握 │
│    500    │    120    │    45     │
└──────────┴──────────┴──────────┘

📊 分类进度
高考词汇 ████████░░░░░░░░  50%
考研词汇 ████░░░░░░░░░░░░  20%
四级词汇 ████████████░░░░  60%
六级词汇 ██░░░░░░░░░░░░░░  10%
```

### 第七步：设置每日目标

底部「设置」→ 选择目标词数：

- **10 词/天** — 轻度学习
- **20 词/天** — 每日推荐（约 15 分钟）
- **30 词/天** — 中等强度
- **50 词/天** — 高强度冲刺

---

## 📊 词汇库规格

| 词库 | 来源 | 词量 | 适用考试 |
|------|------|:--:|------|
| 🎓 高考 | 《普通高中英语课程标准》 | 500+ | 高考英语 |
| 📚 考研 | 全国硕士研究生入学考试大纲 | 5500+ | 考研英语 |
| 🏅 四级 | CET-4 考试大纲 | 4500+ | 大学英语四级 |
| 🏆 六级 | CET-6 考试大纲 | 6000+ | 大学英语六级 |

> 当前内置词量为精选基础样本。通过编辑 `src/data/vocabulary.ts` 可扩展完整词表。

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

编辑 `src/data/vocabulary.ts`，按格式添加：

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

## 📖 学习模式详解

### 背诵模式

- **正面**：单词 + 音标 + 🔊 发音按钮
- **背面**：释义 + 例句
- **翻转**：点击卡片触发 CSS 3D transform 动画
- **进度**：顶部进度条 `(3/500)` 实时更新
- **评分**：4 级掌握度反馈，影响学习追踪

### 测验模式

- **题型一**：看英文选中文（4 选 1）
- **题型二**：听发音 / 看中文 → 输入英文拼写
- **计分**：每题 1 分，结束后显示 `总分 / 总题数`
- **重做**：完成后可重新开始

---

## ⌨️ 快捷键参考

| 快捷键 | 页面 | 功能 |
|--------|------|------|
| `Space` | 背诵 | 翻转卡片查看释义 |
| `→` | 背诵 | 下一词 |
| `←` | 背诵 | 上一词 |
| `Enter` | 测验 | 确认答案 |
| `1-4` | 测验 | 快速选择 ABCD |

---

## 💾 数据存储与备份

### 存储位置

所有进度数据存储在浏览器 `localStorage` 中：

| Key | 内容 |
|-----|------|
| `vocab-progress` | 每个单词的学习状态 (JSON) |
| `vocab-settings` | 当前词库、模式、每日目标 (JSON) |

### 学习状态

```typescript
type WordStatus = 'unlearned' | 'learning' | 'mastered';

interface WordProgress {
  status: WordStatus;
  lastReview: string;     // 最后复习日期
  reviewCount: number;    // 复习次数
  correctCount: number;   // 正确次数
}
```

### 备份方法

桌面版（Electron）的数据存储在对应系统的应用缓存中：

| 系统 | 路径 |
|------|------|
| Windows | `%APPDATA%\词汇背诵助手\` |
| macOS | `~/Library/Application Support/词汇背诵助手/` |

> ⚠️ 卸载应用会清除数据，建议定期使用「开发者工具」导出。

---

## 🔧 开发指南

### 环境要求

- **Node.js** >= 18.0.0
- **npm** >= 9.0.0

### 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run dev
# → 浏览器打开 http://localhost:5173

# 4. 启动 Electron 桌面版开发
npm run dev
# → 自动打开 Electron 窗口 + Vite HMR
```

### 可用命令

| 命令 | 说明 |
|------|------|
| `npm run dev` | 启动 Vite 开发服务器 + Electron 窗口 |
| `npm run build` | TypeScript 类型检查 + Vite 生产构建 |
| `npm run preview` | 预览生产构建 |
| `npm run dist` | 打包为桌面应用（当前系统） |
| `npm run dist:win` | 打包 Windows (.exe) |
| `npm run dist:mac` | 打包 macOS (.dmg) |

### 项目结构

```
Vocabulary/
├── src/                          # React 前端源码
│   ├── App.tsx                   # 主应用组件
│   ├── main.tsx                  # React 入口
│   ├── index.css                 # TailwindCSS + 全局样式
│   ├── components/               # UI 组件
│   │   ├── WordCard.tsx          # 单词卡片（3D 翻转）
│   │   ├── QuizMode.tsx          # 测验答题
│   │   ├── CategorySelector.tsx  # 词库选择卡片
│   │   ├── ProgressBar.tsx       # 进度条
│   │   └── StatsPanel.tsx        # 统计面板
│   ├── data/
│   │   └── vocabulary.ts         # 词库数据
│   ├── types/
│   │   └── vocabulary.ts   
