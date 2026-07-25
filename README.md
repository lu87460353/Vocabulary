# 📚 高考英语词汇背诵助手

[![npm version](https://img.shields.io/npm/v/@uoh56456/gaokao-vocab)](https://www.npmjs.com/package/@uoh56456/gaokao-vocab)
[![license](https://img.shields.io/npm/l/@uoh56456/gaokao-vocab)](LICENSE)
[![platform](https://img.shields.io/badge/platform-Windows-blue)](https://github.com/lu87460353/Vocabulary)

基于 **React 18 + TypeScript + Vite** 构建的英语词汇学习桌面应用。融合四大词汇库（高考 / 考研 / 四级 / 六级），每个单词配备英式音标、词性标注、中文释义和双语例句，支持卡片背诵与交互测验双模式。

---

## 📖 目录

- [功能特色](#-功能特色)
- [安装方式](#-安装方式)
- [使用说明](#-使用说明)
- [词汇库说明](#-词汇库说明)
- [学习模式](#-学习模式)
- [快捷键](#-快捷键)
- [数据存储](#-数据存储)
- [开发指南](#-开发指南)
- [项目结构](#-项目结构)
- [技术栈](#-技术栈)
- [打包说明](#-打包说明)
- [常见问题](#-常见问题)
- [许可证](#-许可证)

---

## ✨ 功能特色

| 功能 | 说明 |
|------|------|
| 📖 **四大词汇库** | 高考 · 考研 · 四级 · 六级，一键切换 |
| 🔤 **完整单词数据** | 英式音标 + 词性标注 + 中文释义 + 双语例句 |
| 🔄 **背诵模式** | 卡片翻转动画 — 正面英文，背面释义例句 |
| 🧠 **测验模式** | 英译中选择题 + 听音拼写，即时判分 |
| 🔊 **TTS 发音** | Web Speech API 原生美式发音 |
| 📊 **学习追踪** | 掌握 / 学习中 / 未学习 三状态持久化 |
| 🎯 **每日目标** | 10 / 20 / 30 / 50 词/天，可随时调整 |
| 📈 **进度统计** | 各分类掌握百分比 + 今日完成数可视化 |
| 💻 **桌面应用** | pywebview 原生 Windows 窗口，14.6 MB 单文件 |
| 🌐 **Web 版** | 浏览器直接打开 `dist/index.html` 即可使用 |

---

## 📦 安装方式

### 方式一：npm 全局安装（推荐）

```bash
npm install -g @uoh56456/gaokao-vocab
```

安装完成后，在终端输入以下命令启动：

```bash
gaokao-vocab
```

或使用 npx 免安装运行：

```bash
npx @uoh56456/gaokao-vocab
```

### 方式二：直接下载 EXE

从 [Releases](https://github.com/lu87460353/Vocabulary/releases) 下载 `VocabularyApp.exe`，双击即可运行。

> 首次运行 Windows 可能弹出 SmartScreen 警告，点击「更多信息」→「仍要运行」即可。

### 方式三：浏览器 Web 版

克隆仓库后，直接用浏览器打开 `dist/index.html`：

```bash
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary
# 直接用浏览器打开 dist/index.html
# 或者启动开发服务器：
npm install && npm run dev
```

---

## 🚀 使用说明

### 1. 选择词汇库

打开应用后，首页展示四个词汇类别卡片：

| 类别 | 适用场景 | 词量示例 |
|------|---------|----------|
| 🎓 高考词汇 | 高考英语备考 | abandon, ability, abnormal... |
| 📚 考研词汇 | 考研英语备考 | abbreviate, abide, abolish... |
| 🏅 四级词汇 | CET-4 备考 | academic, accompany, accomplish... |
| 🏆 六级词汇 | CET-6 备考 | abdomen, abound, absurd... |

点击卡片即可切换，进度独立追踪。

### 2. 选择学习模式

首页下方有两个模式按钮：

- **背诵模式**（默认）：逐词浏览，点击卡片翻转查看释义
- **测验模式**：选择题 + 拼写题，完成后显示得分

### 3. 背诵模式操作

```
┌──────────────────────────┐
│         🔊 发音           │
│                          │
│      abandon             │
│      /əˈbændən/          │
│                          │
│   点击卡片查看释义       │
└──────────────────────────┘
         ↓ 点击翻转
┌──────────────────────────┐
│      abandon             │
│      /əˈbændən/          │
│                          │
│  v. 放弃，抛弃；         │
│     n. 放任，放纵        │
│                          │
│  He decided to abandon   │
│  his plan.               │
│  他决定放弃他的计划。    │
└──────────────────────────┘

操作按钮：
[还没记住]  [已掌握]  [再看一次]
```

- **还没记住**：标记为「学习中」，进入下一词
- **已掌握**：标记为「已掌握」，进入下一词
- **再看一次**：翻回正面重新记忆
- **🔊 按钮**：朗读当前单词

### 4. 测验模式操作

选择「测验模式」后进入答题界面：

- **选择题**：看到英文单词，从 4 个选项中选出正确的中文释义
- **拼写题**：听到单词发音（或看到中文），输入正确的英文拼写
- 答完所有题目后显示得分和正确率

### 5. 查看统计

底部导航栏点击「统计」：

- 总词数 / 已学习 / 已掌握 三项核心指标
- 今日完成进度（进度条 + 数字）
- 各分类独立进度条（高考 / 考研 / 四级 / 六级）

### 6. 设置每日目标

点击「设置」：

- 选择每日学习目标：10 / 20 / 30 / 50 词
- 查看当前词汇库和学习模式
- **重置所有数据**：清除全部学习进度

### 7. 学习建议

1. **每天坚持**：设置合理的每日目标（建议 20 词）
2. **先背后测**：先用背诵模式浏览，再用测验模式检验
3. **多次复习**：标记为「学习中」的词汇会在统计中高亮提醒
4. **逐个击破**：每攻克一个词汇库再切换到下一个

---

## 📊 词汇库说明

词汇数据来源于各大考试官方大纲：

| 词汇库 | 来源 | 词量参考 |
|--------|------|----------|
| 高考 | 《普通高中英语课程标准》 | ~500 词 |
| 考研 | 考研英语大纲 | ~5500 词 |
| 四级 | CET-4 考试大纲 | ~4500 词 |
| 六级 | CET-6 考试大纲 | ~6000 词 |

> 当前内置词量为基础样本。可通过编辑 `src/data/vocabulary.ts` 扩充词汇。

---

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| `←` / `→` | 上一词 / 下一词（背诵模式） |
| `Space` | 翻转卡片 |
| `Enter` | 确认答案（测验模式） |

---

## 💾 数据存储

所有学习进度保存在浏览器 `localStorage` 中，无需登录或联网。

| Key | 内容 |
|-----|------|
| `vocab-progress` | 每个单词的学习状态 |
| `vocab-settings` | 当前词汇库、模式、每日目标 |

> 点击「设置 → 重置所有数据」可清空全部进度。

---

## 🔧 开发指南

```bash
# 克隆仓库
git clone https://github.com/lu87460353/Vocabulary.git
cd Vocabulary

# 安装依赖
npm install

# 启动开发服务器（热更新）
npm run dev

# 生产构建
npm run build

# 预览构建产物
npm run preview
```

### 添加新词汇

编辑 `src/data/vocabulary.ts`，在对应分类的数组中添加：

```typescript
{
  id: 'gaokao-xxx',           // 唯一 ID
  word: 'example',            // 英文单词
  phonetic: '/ɪɡˈzæmpəl/',   // 英式音标
  meaning: 'n. 例子，范例',   // 词性 + 中文释义
  example: 'This is an example. 这是一个例子。',
  category: 'gaokao',         // 分类: gaokao/kaoyan/cet4/cet6
}
```

---

## 📁 项目结构

```
Vocabulary/
├── src/
│   ├── App.tsx                    # 主应用：标签页路由、状态管理
│   ├── main.tsx                   # React 入口
│   ├── index.css                  # TailwindCSS 全局样式
│   ├── components/
│   │   ├── WordCard.tsx           # 单词卡片（3D 翻转动画 + 发音）
│   │   ├── QuizMode.tsx           # 测验模式（选择 + 拼写）
│   │   ├── CategorySelector.tsx   # 词汇库选择卡片
│   │   ├── ProgressBar.tsx        # 通用进度条组件
│   │   └── StatsPanel.tsx         # 统计面板（总量/掌握/今日）
│   ├── data/
│   │   └── vocabulary.ts          # 词汇数据（4 大类）
│   ├── types/
│   │   └── vocabulary.ts          # TypeScript 类型定义
│   └── utils/
│       └── storage.ts             # localStorage 读写封装
├── dist/                          # Vite 构建产物
├── launcher.py                    # pywebview 桌面启动器
├── VocabularyApp.exe              # Windows 可执行文件 (14.6 MB)
├── index.html                     # 入口 HTML
├── package.json                   # npm 包配置
├── vite.config.ts                 # Vite 配置
├── tailwind.config.js             # TailwindCSS 配置
├── tsconfig.json                  # TypeScript 配置
├── postcss.config.js              # PostCSS 配置
└── README.md
```

---

## 🛠 技术栈

| 层 | 技术 | 版本 |
|----|------|------|
| 前端框架 | React | 18.2 |
| 类型系统 | TypeScript | 5.2 |
| 构建工具 | Vite | 5.0 |
| CSS 框架 | TailwindCSS | 3.4 |
| 图标库 | Lucide React | 0.294 |
| 数据持久化 | localStorage | — |
| 语音合成 | Web Speech API | — |
| 桌面打包 | pywebview + PyInstaller | — |
| 包管理 | npm | — |

---

## 📦 打包说明

### Web 构建

```bash
npm run build
# 产物在 dist/ 目录
```

### Windows EXE 打包

```bash
# 1. 安装 Python 依赖
pip install pywebview pyinstaller

# 2. 打包
pyinstaller --onefile --windowed \
  --name VocabularyApp \
  --add-data "dist;dist" \
  --hidden-import webview \
  --collect-all webview \
  launcher.py

# 产物: dist/VocabularyApp.exe
```

---

## ❓ 常见问题

### Q: 双击 EXE 后窗口一闪而过？

A: 可能是杀毒软件拦截。尝试将文件加入白名单，或从命令行运行查看错误信息。

### Q: 发音没有声音？

A: Web Speech API 需要系统安装了语音包。Windows 10/11 自带美式英语语音。确保系统音量未静音。

### Q: 如何备份学习进度？

A: 进度存储在浏览器 localStorage 中（EXE 版使用内置 WebView 的 localStorage）。清除浏览器数据或重置应用会丢失进度。

### Q: 可以自己加词汇吗？

A: 可以。编辑 `src/data/vocabulary.ts`，按格式添加后重新 `npm run build`。

### Q: macOS 能用吗？

A: 当前 EXE 仅支持 Windows。macOS 用户可通过 Web 版使用（`npm run dev` 或直接打开 `dist/index.html`）。

---

## 📄 许可证

MIT License © uoh56456

---

<p align="center">
  <sub>Made with ❤️ for English learners</sub>
</p>
