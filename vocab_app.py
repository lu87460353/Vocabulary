"""
高考英语词汇背诵软件 - 主程序 v2.0
基于《普通高中英语课程标准（2017年版2025年修订）》
功能：每日学习计划、间隔重复复习、错题本、翻译、TTS拼读、
      写作真题范文、听力练习、AI助手、学习进度跟踪
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys, os, random, json, threading, math, time
from datetime import date, datetime, timedelta

# ---- 路径 ----
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

try:
    import database as db
    from dictionary import CORE_DICT, get_translation
except ImportError as e:
    root = tk.Tk(); root.withdraw()
    messagebox.showerror("错误", f"模块加载失败: {e}")
    sys.exit(1)

# ---- TTS ----
try:
    import pythoncom, win32com.client as win32
    pythoncom.CoInitialize()
    TTS_AVAILABLE = True
except:
    TTS_AVAILABLE = False

# ---- 颜色 ----
C = {
    'bg': '#f0f2f5',
    'card': '#ffffff',
    'nav_bg': '#ffffff',
    'primary': '#1a73e8',
    'accent': '#4285f4',
    'success': '#0f9d58',
    'warning': '#f4b400',
    'danger': '#db4437',
    'text': '#202124',
    'text2': '#5f6368',
    'text3': '#9aa0a6',
    'border': '#dadce0',
    'hover': '#e8f0fe',
    'progress_bg': '#e8eaed',
}

FONT_TITLE = ('Microsoft YaHei UI', 18, 'bold')
FONT_H2 = ('Microsoft YaHei UI', 13, 'bold')
FONT_BODY = ('Microsoft YaHei UI', 11)
FONT_SMALL = ('Microsoft YaHei UI', 9)
FONT_WORD = ('Segoe UI', 28, 'bold')
FONT_MEAN = ('Microsoft YaHei UI', 15)

# ===================== 动画效果 =====================
class AnimatedFrame(tk.Frame):
    """带动画效果的Frame"""
    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self._anim_job = None
    
    def pulse(self, widget, color_start, color_end, steps=10, step=0):
        """颜色脉冲动画"""
        if step >= steps:
            widget.configure(bg=color_start)
            return
        t = step / (steps - 1)
        r1, g1, b1 = self._hex_to_rgb(color_start)
        r2, g2, b2 = self._hex_to_rgb(color_end)
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        widget.configure(bg=f'#{r:02x}{g:02x}{b:02x}')
        self._anim_job = self.after(30, lambda: self.pulse(widget, color_start, color_end, steps, step + 1))
    
    def _hex_to_rgb(self, h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    
    def scale_font(self, widget, base_size, target_size, steps=8, step=0):
        """字体缩放动画"""
        if step >= steps:
            return
        t = step / (steps - 1)
        s = int(base_size + (target_size - base_size) * math.sin(t * math.pi / 2))
        cur = widget.cget('font')
        if isinstance(cur, tuple):
            widget.configure(font=(cur[0], s, cur[2] if len(cur) > 2 else 'normal'))
        self._anim_job = self.after(20, lambda: self.scale_font(widget, base_size, target_size, steps, step + 1))

    def emoji_bounce(self, label, emoji, count=3):
        """表情弹跳"""
        if count <= 0:
            label.configure(text='')
            return
        label.configure(text=emoji * count)
        self._anim_job = self.after(200, lambda: self.emoji_bounce(label, emoji, count - 1))

# ===================== 圆角按钮 =====================
class RoundedButton(tk.Canvas):
    """圆角按钮"""
    def __init__(self, parent, text, command=None, bg=C['primary'], fg='white',
                 font=None, width=100, height=36, radius=18, **kw):
        super().__init__(parent, width=width, height=height, 
                        bg=parent.cget('bg') if hasattr(parent, 'cget') else C['bg'],
                        highlightthickness=0, **kw)
        self.command = command
        self.bg = bg
        self.fg = fg
        self.font = font or FONT_BODY
        self.radius = radius
        self.width = width
        self.height = height
        self._enabled = True
        
        self._draw(bg)
        self.bind('<Button-1>', self._on_click)
        self.bind('<Enter>', lambda e: self._draw(self._lighten(bg)))
        self.bind('<Leave>', lambda e: self._draw(bg))
    
    def _lighten(self, color):
        """颜色变亮"""
        h = color.lstrip('#')
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        r = min(255, r + 20); g = min(255, g + 20); b = min(255, b + 20)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _draw(self, bg_color):
        self.delete('all')
        r = self.radius
        w, h = self.width, self.height
        self.create_rounded_rect(0, 0, w, h, r, fill=bg_color, outline=bg_color)
        self.create_text(w//2, h//2, text=self.cget('text') if hasattr(self, 'cget') else '',
                        fill=self.fg, font=self.font)
    
    def create_rounded_rect(self, x1, y1, x2, y2, r, **kw):
        """绘制圆角矩形"""
        return self.create_polygon(
            x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
            x2, y2-r, x2, y2, x2-r, y2,
            x1+r, y2, x1, y2, x1, y2-r,
            x1, y1+r, x1, y1, smooth=True, **kw)
    
    def configure(self, **kw):
        if 'text' in kw:
            super().configure(text=kw.pop('text'))
        if 'bg' in kw:
            self.bg = kw.pop('bg')
        if 'state' in kw and kw['state'] == 'disabled':
            self._enabled = False
        elif 'state' in kw:
            self._enabled = True
        self._draw(self.bg)
    
    def _on_click(self, e):
        if self._enabled and self.command:
            self.command()

# ===================== 主应用 =====================
class VocabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 高考英语词汇背诵 - GaokaoVocab")
        self.root.geometry("960x720")
        self.root.minsize(860, 640)
        self.root.configure(bg=C['bg'])
        
        # 初始化
        self._ensure_database()
        db.init_db()
        db.init_writing_templates()
        self._load_vocab_if_needed()
        
        # TTS
        self.tts = None
        if TTS_AVAILABLE:
            try: self.tts = win32.Dispatch("SAPI.SpVoice")
            except: pass
        
        # 状态
        self.current_plan = []
        self.current_index = 0
        self.current_page = 'study'
        self._listen_word = None
        self._listen_correct = 0
        self._listen_total = 0
        self._listen_wrong = []  # 听错的词列表
        self._listen_round = []  # 当前轮待听词
        
        # 动画
        self._anim = AnimatedFrame(root, bg=C['bg'])
        self._anim.place(x=0, y=0, width=1, height=1)  # 隐藏动画控制器
        
        # 构建UI
        self._build_main()
        self._build_pages()
        self._show_page('study')
        self._load_today()
        
        # 居中
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f'+{(sw-w)//2}+{(sh-h)//2}')
    
    def _ensure_database(self):
        import shutil
        target_db = db.DB_PATH
        init_db_path = os.path.join(BASE_DIR, 'vocab_data_initial.db')
        if not os.path.exists(target_db) and os.path.exists(init_db_path):
            shutil.copy(init_db_path, target_db)
    
    def _load_vocab_if_needed(self):
        conn = db.get_db()
        count = conn.execute('SELECT COUNT(*) as c FROM words').fetchone()['c']
        conn.close()
        if count == 0:
            vocab_path = os.path.join(BASE_DIR, 'vocab_words.json')
            if os.path.exists(vocab_path):
                with open(vocab_path, 'r', encoding='utf-8') as f:
                    words = json.load(f)
                conn = db.get_db()
                for w in words:
                    trans = get_translation(w['word'])
                    conn.execute('INSERT OR IGNORE INTO words (word, level, translation) VALUES (?,?,?)',
                               (w['word'], w['level'], trans))
                conn.commit(); conn.close()
    
    # ===================== 主布局 =====================
    def _build_main(self):
        # 内容区域
        self.content = tk.Frame(self.root, bg=C['bg'])
        self.content.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # 底部导航栏
        self._build_bottom_nav()
    
    def _build_bottom_nav(self):
        """底部导航栏 - 圆角按钮均匀分布"""
        nav = tk.Frame(self.root, bg=C['nav_bg'], height=60)
        nav.pack(side=tk.BOTTOM, fill=tk.X)
        nav.pack_propagate(False)
        
        # 顶部分隔线
        tk.Frame(nav, bg=C['border'], height=1).pack(fill=tk.X)
        
        # 按钮容器 - 均匀分布
        btn_frame = tk.Frame(nav, bg=C['nav_bg'])
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # 6个等宽列
        for i in range(6):
            btn_frame.columnconfigure(i, weight=1, uniform='nav')
        
        pages = [
            ('📝', '学习', 'study'),
            ('📊', '统计', 'stats'),
            ('📕', '错题本', 'errors'),
            ('✍️', '写作', 'writing'),
            ('🎧', '听力', 'listening'),
            ('🤖', 'AI', 'ai'),
        ]
        
        self.nav_btns = {}
        for i, (icon, text, page) in enumerate(pages):
            frame = tk.Frame(btn_frame, bg=C['nav_bg'])
            frame.grid(row=0, column=i, sticky='nsew')
            
            btn = tk.Button(frame, text=f"{icon} {text}", 
                          command=lambda p=page: self._show_page(p),
                          bg=C['nav_bg'], fg=C['text2'], font=FONT_SMALL,
                          bd=0, cursor='hand2', padx=12, pady=8,
                          activebackground=C['hover'], activeforeground=C['primary'])
            btn.pack(expand=True)
            self.nav_btns[page] = btn
    
    def _show_page(self, page):
        self.current_page = page
        for p in self.pages.values():
            p.pack_forget()
        self.pages[page].pack(fill=tk.BOTH, expand=True, padx=16, pady=12)
        
        # 导航高亮
        for name, btn in self.nav_btns.items():
            if name == page:
                btn.configure(fg=C['primary'], font=('Microsoft YaHei UI', 10, 'bold'))
            else:
                btn.configure(fg=C['text2'], font=FONT_SMALL)
        
        if page == 'stats': self._refresh_stats()
        if page == 'errors': self._refresh_errors()
    
    # ===================== 页面构建 =====================
    def _build_pages(self):
        self.pages = {}
        for name in ['study', 'stats', 'errors', 'writing', 'listening', 'ai']:
            self.pages[name] = tk.Frame(self.content, bg=C['bg'])
        
        self._build_study_page()
        self._build_stats_page()
        self._build_errors_page()
        self._build_writing_page()
        self._build_listening_page()
        self._build_ai_page()
    
    # ========== 学习页面 ==========
    def _build_study_page(self):
        page = self.pages['study']
        
        # 每日目标卡片
        goal_card = tk.Frame(page, bg=C['primary'])
        goal_card.pack(fill=tk.X, pady=(0, 12))
        
        goal_inner = tk.Frame(goal_card, bg=C['primary'])
        goal_inner.pack(fill=tk.X, padx=20, pady=12)
        
        tk.Label(goal_inner, text="📅 今日目标", font=FONT_H2, bg=C['primary'], fg='white').pack(side=tk.LEFT)
        
        self.goal_total_label = tk.Label(goal_inner, text="0 词", font=('Segoe UI', 22, 'bold'),
                                         bg=C['primary'], fg='#ffeb3b')
        self.goal_total_label.pack(side=tk.RIGHT, padx=(0, 15))
        
        self.goal_done_label = tk.Label(goal_inner, text="已完成 0", font=FONT_BODY,
                                        bg=C['primary'], fg='#b3d4fc')
        self.goal_done_label.pack(side=tk.RIGHT, padx=10)
        
        # 进度条
        self.study_progress_frame = tk.Frame(page, bg=C['progress_bg'], height=8)
        self.study_progress_frame.pack(fill=tk.X, pady=(0, 12))
        self.study_progress_bar = tk.Frame(self.study_progress_frame, bg=C['primary'], height=8, width=0)
        self.study_progress_bar.place(x=0, y=0, height=8)
        
        # 单词卡片
        card = tk.Frame(page, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True, pady=(0, 12))
        
        card_inner = tk.Frame(card, bg=C['card'])
        card_inner.pack(fill=tk.BOTH, expand=True, padx=30, pady=25)
        
        # 类型标签
        self.mode_label = tk.Label(card_inner, text="", font=FONT_SMALL, fg=C['primary'], bg=C['card'])
        self.mode_label.pack(pady=(0, 12))
        
        # 动画标签
        self.anim_label = tk.Label(card_inner, text="", font=('Segoe UI', 48),
                                   bg=C['card'], fg=C['primary'])
        self.anim_label.pack()
        
        # 单词
        self.word_label = tk.Label(card_inner, text="点击下方按钮\n开始学习", 
                                   font=FONT_WORD, bg=C['card'], fg=C['text'])
        self.word_label.pack(pady=(5, 8))
        
        # 音标
        self.phonetic_label = tk.Label(card_inner, text="", font=('Segoe UI', 13),
                                       fg=C['text3'], bg=C['card'])
        self.phonetic_label.pack()
        
        # 发音按钮
        self.speak_btn = tk.Button(card_inner, text="🔊 发音", command=self._speak_word,
                                   bg=C['hover'], fg=C['primary'], bd=0,
                                   font=FONT_SMALL, cursor='hand2', padx=14, pady=4)
        self.speak_btn.pack(pady=(8, 0))
        self.speak_btn.pack_forget()
        
        # 释义区
        tk.Frame(card_inner, bg=C['border'], height=1).pack(fill=tk.X, pady=12)
        
        self.meaning_label = tk.Label(card_inner, text="", font=FONT_MEAN,
                                      fg=C['success'], bg=C['card'], wraplength=600)
        self.meaning_label.pack()
        
        self.example_label = tk.Label(card_inner, text="", font=('Microsoft YaHei UI', 10),
                                      fg=C['text3'], bg=C['card'], wraplength=600)
        self.example_label.pack(pady=(4, 0))
        
        # 底部评分按钮
        btn_frame = tk.Frame(page, bg=C['bg'])
        btn_frame.pack(fill=tk.X, pady=(0, 6))
        
        ratings = [
            ("😰 忘记\n加入错题本", 0, C['danger']),
            ("🤔 不确定\n再学一遍", 2, C['warning']),
            ("🙂 基本掌握", 4, C['accent']),
            ("😎 完全掌握", 5, C['success']),
        ]
        
        for text, q, color in ratings:
            btn = tk.Button(btn_frame, text=text,
                          command=lambda qq=q, cc=color: self._rate_word(qq, cc),
                          bg=color, fg='white', font=FONT_SMALL, bd=0,
                          cursor='hand2', padx=10, pady=10, wraplength=90,
                          activebackground=color)
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        
        # 显示答案按钮
        self.show_btn = tk.Button(page, text="👁️ 点击显示释义",
                                 command=self._show_answer,
                                 bg=C['text'], fg='white', font=FONT_BODY, bd=0,
                                 cursor='hand2', padx=20, pady=10)
        self.show_btn.pack(fill=tk.X)
    
    def _load_today(self):
        today = date.today().isoformat()
        plan = db.get_today_plan(today)
        if not plan:
            db.generate_plan(today)
            plan = db.get_today_plan(today)
        self.current_plan = [p for p in plan if not p['completed']]
        self.current_index = 0
        self._update_goal_display()
        
        if self.current_plan:
            self._show_current_word()
        else:
            self.word_label.configure(text="🎉 今日学习完成！")
            self.meaning_label.configure(text="你真棒！明天继续加油！")
            self.phonetic_label.configure(text="")
            self.anim_label.configure(text="🏆")
            self.mode_label.configure(text="")
            self.speak_btn.pack_forget()
            self.show_btn.configure(text="✅ 今日任务已完成", state='disabled')
    
    def _update_goal_display(self):
        today = date.today().isoformat()
        stats = db.get_today_progress()
        total = len(self.current_plan) + stats['done']
        self.goal_total_label.configure(text=f"{total} 词")
        self.goal_done_label.configure(text=f"已完成 {stats['done']}")
        
        if total > 0:
            pct = stats['done'] / total * 100
            w = self.study_progress_frame.winfo_width()
            if w > 1:
                self.study_progress_bar.place(width=int(w * pct / 100))
    
    def _show_current_word(self):
        if not self.current_plan or self.current_index >= len(self.current_plan):
            self.word_label.configure(text="🎉 今日学习完成！")
            self.meaning_label.configure(text="干得漂亮！明天继续加油！")
            self.phonetic_label.configure(text="")
            self.mode_label.configure(text="")
            self.anim_label.configure(text="🏆")
            self.speak_btn.pack_forget()
            self.show_btn.configure(text="✅ 今日任务已完成", state='disabled')
            self._update_goal_display()
            return
        
        item = self.current_plan[self.current_index]
        
        # 模式标签
        mode_text = "🆕 新单词" if item['plan_type'] == 'new' else "🔄 复习"
        mode_color = C['accent'] if item['plan_type'] == 'new' else C['warning']
        self.mode_label.configure(text=mode_text, fg=mode_color)
        
        # 序列号
        seq = f"({self.current_index + 1}/{len(self.current_plan)})"
        
        # 单词
        self.word_label.configure(text=f"{item['word']}  {seq}", font=FONT_WORD)
        self.phonetic_label.configure(text=item.get('phonetic', '') or '')
        
        # 隐藏释义，显示emoji
        self.meaning_label.configure(text="点击下方 👁️ 按钮查看释义")
        self.example_label.configure(text="")
        self.anim_label.configure(text="📖")
        
        if TTS_AVAILABLE:
            self.speak_btn.pack(pady=(8, 0))
        else:
            self.speak_btn.pack_forget()
        
        self.show_btn.configure(text="👁️ 点击显示释义", state='normal')
        self._update_goal_display()
    
    def _show_answer(self):
        if not self.current_plan or self.current_index >= len(self.current_plan):
            return
        item = self.current_plan[self.current_index]
        trans = item.get('translation', '') or get_translation(item['word'])
        self.meaning_label.configure(text=trans, font=FONT_MEAN, fg=C['success'])
        self.anim_label.configure(text="💡")
    
    def _rate_word(self, quality, color):
        if not self.current_plan or self.current_index >= len(self.current_plan):
            return
        item = self.current_plan[self.current_index]
        word_id = item['word_id']
        word = item['word']
        
        # 先显示答案
        self._show_answer()
        
        # 动画
        emojis = {0: '😰', 2: '🤔', 4: '🙂', 5: '😎'}
        self._anim.emoji_bounce(self.anim_label, emojis.get(quality, '📝'))
        
        # 记录评分
        db.record_review(word_id, quality)
        
        # 错题本
        if quality < 3:
            trans = item.get('translation', '') or get_translation(word)
            db.add_to_error_book(word_id, 'meaning', f'评分{quality}/5', trans)
        
        # 标记完成
        conn = db.get_db()
        conn.execute('UPDATE daily_plan SET completed=1, score=? WHERE id=?',
                    (quality * 20, item['plan_id']))
        conn.commit(); conn.close()
        
        # 更新连续天数
        today = date.today().isoformat()
        last = db.get_setting('last_study_date', '')
        if last != today:
            if last and (date.today() - datetime.strptime(last, '%Y-%m-%d').date()).days == 1:
                db.set_setting('streak_days', str(int(db.get_setting('streak_days', '0')) + 1))
            else:
                db.set_setting('streak_days', '1')
            db.set_setting('last_study_date', today)
        
        self.current_index += 1
        self.root.after(350, self._show_current_word)
    
    def _speak_word(self):
        if not TTS_AVAILABLE or not self.tts:
            messagebox.showinfo("提示", "需要 pywin32: pip install pywin32")
            return
        if not self.current_plan or self.current_index >= len(self.current_plan):
            return
        word = self.current_plan[self.current_index]['word']
        def speak():
            try: self.tts.Speak(word, 3)
            except: pass
        self.root.after(50, speak)
        self.anim_label.configure(text="🔊")
    
    # ========== 统计页面 ==========
    def _build_stats_page(self):
        page = self.pages['stats']
        tk.Label(page, text="📊 学习统计", font=FONT_TITLE, bg=C['bg']).pack(anchor='w', pady=(0, 12))
        
        cards_frame = tk.Frame(page, bg=C['bg'])
        cards_frame.pack(fill=tk.X)
        
        card_info = [
            ("总词汇", 'total', '📚'), ("已学习", 'learned', '✅'),
            ("已掌握", 'mastered', '🏆'), ("错题数", 'errors', '📕'),
            ("连续天数", 'streak', '🔥'), ("待复习", 'due_today', '📅'),
        ]
        
        self.stat_cards = {}
        for i, (text, key, icon) in enumerate(card_info):
            card = tk.Frame(cards_frame, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
            card.grid(row=i//3, column=i%3, padx=4, pady=4, sticky='nsew')
            cards_frame.columnconfigure(i%3, weight=1)
            
            tk.Label(card, text=f"{icon} {text}", font=FONT_SMALL, fg=C['text2'], bg=C['card']).pack(pady=(12, 4))
            lbl = tk.Label(card, text="0", font=('Segoe UI', 26, 'bold'), fg=C['primary'], bg=C['card'])
            lbl.pack(pady=(0, 12))
            self.stat_cards[key] = lbl
        
        # 进度
        pf = tk.Frame(page, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
        pf.pack(fill=tk.X, pady=10)
        pi = tk.Frame(pf, bg=C['card']); pi.pack(fill=tk.X, padx=18, pady=14)
        tk.Label(pi, text="总体进度", font=FONT_H2, bg=C['card']).pack(anchor='w')
        self.overall_pct = tk.Label(pi, text="0%", font=('Segoe UI', 32, 'bold'), fg=C['primary'], bg=C['card'])
        self.overall_pct.pack(pady=(8, 4))
        self.overall_bar_frame = tk.Frame(pi, bg=C['progress_bg'], height=14)
        self.overall_bar_frame.pack(fill=tk.X)
        self.overall_bar = tk.Frame(self.overall_bar_frame, bg=C['primary'], height=14, width=0)
        self.overall_bar.place(x=0, y=0, height=14)
    
    def _refresh_stats(self):
        stats = db.get_stats()
        streak = db.get_setting('streak_days', '0')
        for key, lbl in self.stat_cards.items():
            lbl.configure(text=str(streak if key == 'streak' else stats.get(key, 0)))
        pct = stats['progress']
        self.overall_pct.configure(text=f"{pct}%")
        w = self.overall_bar_frame.winfo_width()
        if w > 1: self.overall_bar.place(width=int(w * pct / 100))
    
    # ========== 错题本 ==========
    def _build_errors_page(self):
        page = self.pages['errors']
        tf = tk.Frame(page, bg=C['bg']); tf.pack(fill=tk.X, pady=(0, 8))
        tk.Label(tf, text="📕 错题本", font=FONT_TITLE, bg=C['bg']).pack(side=tk.LEFT)
        tk.Button(tf, text="🔄 复习错题", command=self._review_errors,
                 bg=C['danger'], fg='white', font=FONT_SMALL, bd=0, cursor='hand2',
                 padx=14, pady=6).pack(side=tk.RIGHT)
        
        lf = tk.Frame(page, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
        lf.pack(fill=tk.BOTH, expand=True)
        
        cols = ('word', 'translation', 'type', 'time')
        self.error_tree = ttk.Treeview(lf, columns=cols, show='headings', height=14)
        for c in cols:
            self.error_tree.heading(c, text={'word':'单词','translation':'释义','type':'类型','time':'时间'}[c])
        self.error_tree.column('word', width=100); self.error_tree.column('translation', width=180)
        self.error_tree.column('type', width=80); self.error_tree.column('time', width=150)
        
        sb = ttk.Scrollbar(lf, orient=tk.VERTICAL, command=self.error_tree.yview)
        self.error_tree.configure(yscrollcommand=sb.set)
        self.error_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8,0), pady=8)
        sb.pack(side=tk.RIGHT, fill=tk.Y, padx=(0,8), pady=8)
        
        tk.Button(page, text="清空错题本", command=self._clear_errors,
                 bg=C['bg'], fg=C['text3'], font=FONT_SMALL, bd=0).pack(anchor='e', pady=(4,0))
    
    def _refresh_errors(self):
        for row in self.error_tree.get_children():
            self.error_tree.delete(row)
        for e in db.get_error_book(50):
            self.error_tree.insert('', 'end', values=(e['word'], e['translation'], e['error_type'], e['error_time'][:19]))
    
    def _review_errors(self):
        errors = db.get_error_book(20)
        if not errors:
            messagebox.showinfo("提示", "错题本为空！")
            return
        self.current_plan = [{'plan_id':-1, 'word_id':-1, 'word':e['word'],
                              'translation':e['translation'], 'phonetic':'', 'level':0,
                              'plan_type':'review', 'completed':0} for e in errors]
        self.current_index = 0
        self.mode_label.configure(text="📕 错题复习", fg=C['danger'])
        self._show_page('study')
        if self.current_plan: self._show_current_word()
    
    def _clear_errors(self):
        if messagebox.askyesno("确认", "确定清空所有错题记录吗？"):
            conn = db.get_db(); conn.execute('DELETE FROM error_book'); conn.commit(); conn.close()
            self._refresh_errors()
    
    # ========== 写作页面（真题 + 范文）==========
    def _build_writing_page(self):
        page = self.pages['writing']
        tk.Label(page, text="✍️ 写作练习 - 高考真题", font=FONT_TITLE, bg=C['bg']).pack(anchor='w', pady=(0, 8))
        
        # 真题选择
        sf = tk.Frame(page, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
        sf.pack(fill=tk.X, pady=(0, 8))
        si = tk.Frame(sf, bg=C['card']); si.pack(fill=tk.X, padx=14, pady=10)
        
        tk.Label(si, text="选择真题:", font=FONT_BODY, bg=C['card']).pack(side=tk.LEFT)
        
        self.exam_var = tk.StringVar(value='2024新高考I卷-应用文')
        exams = [
            '2024新高考I卷-应用文', '2024新高考I卷-读后续写',
            '2024全国甲卷-发言稿', '2023新高考I卷-应用文',
            '2023新高考I卷-读后续写', '2023全国乙卷-建议信',
            '建议信模板', '邀请信模板', '申请信模板',
            '道歉信模板', '感谢信模板', '议论文模板',
        ]
        cb = ttk.Combobox(si, textvariable=self.exam_var, values=exams, state='readonly', width=22)
        cb.pack(side=tk.LEFT, padx=8)
        tk.Button(si, text="📋 加载", command=self._load_exam,
                 bg=C['primary'], fg='white', font=FONT_SMALL, bd=0, cursor='hand2',
                 padx=12, pady=4).pack(side=tk.LEFT, padx=4)
        
        # 文本区
        self.writing_text = scrolledtext.ScrolledText(page, font=('Microsoft YaHei UI', 11),
                                                       wrap=tk.WORD)
        self.writing_text.pack(fill=tk.BOTH, expand=True)
        
        self._load_exam()
    
    def _load_exam(self):
        topic = self.exam_var.get()
        self.writing_text.delete('1.0', tk.END)
        exams = EXAM_TOPICS
        if topic in exams:
            data = exams[topic]
            text = f"【{topic}】\n{'='*55}\n\n"
            text += f"📝 题目:\n{data['question']}\n\n"
            text += f"📌 关键词提示: {data.get('keywords', '')}\n\n"
            text += f"{'='*55}\n"
            text += f"📖 参考范文:\n\n{data['essay']}\n\n"
            if 'essay2' in data:
                text += f"{'='*55}\n📖 范文二:\n\n{data['essay2']}\n\n"
            self.writing_text.insert('1.0', text)
    
    # ========== 听力页面（重构）==========
    def _build_listening_page(self):
        page = self.pages['listening']
        tk.Label(page, text="🎧 听力练习 - 听音识词", font=FONT_TITLE, bg=C['bg']).pack(anchor='w', pady=(0, 10))
        
        # 说明卡片
        info = tk.Frame(page, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
        info.pack(fill=tk.X, pady=(0, 10))
        ii = tk.Frame(info, bg=C['card']); ii.pack(fill=tk.X, padx=16, pady=10)
        tk.Label(ii, text="点击「下一题」自动播放单词发音，输入拼写后按回车提交。拼错的词会重新出现。",
                font=FONT_SMALL, bg=C['card'], fg=C['text2']).pack(anchor='w')
        
        # 播放/下一题区
        pf = tk.Frame(page, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
        pf.pack(fill=tk.X, pady=(0, 10))
        pi = tk.Frame(pf, bg=C['card']); pi.pack(padx=25, pady=18)
        
        self.listen_status = tk.Label(pi, text="准备开始...", font=FONT_H2, bg=C['card'], fg=C['primary'])
        self.listen_status.pack()
        
        # 输入
        inp = tk.Frame(page, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
        inp.pack(fill=tk.X, pady=(0, 10))
        ii2 = tk.Frame(inp, bg=C['card']); ii2.pack(padx=25, pady=16)
        
        tk.Label(ii2, text="输入你听到的单词:", font=FONT_BODY, bg=C['card']).pack(anchor='w')
        
        self.listen_entry = tk.Entry(ii2, font=('Segoe UI', 16), bd=1, relief='solid')
        self.listen_entry.pack(fill=tk.X, pady=(6, 12))
        self.listen_entry.bind('<Return>', lambda e: self._check_listening())
        
        # 按钮行
        br = tk.Frame(ii2, bg=C['card']); br.pack(fill=tk.X)
        
        tk.Button(br, text="✅ 提交并显示答案", command=self._check_and_show,
                 bg=C['success'], fg='white', font=FONT_BODY, bd=0, cursor='hand2',
                 padx=18, pady=8).pack(side=tk.LEFT, padx=(0, 4))
        
        self.listen_next_btn = tk.Button(br, text="➡️ 下一题（自动播放）", command=self._next_listening,
                                        bg=C['primary'], fg='white', font=FONT_BODY, bd=0, cursor='hand2',
                                        padx=18, pady=8)
        self.listen_next_btn.pack(side=tk.RIGHT)
        
        # 结果
        self.listen_result = tk.Label(ii2, text="", font=('Microsoft YaHei UI', 13, 'bold'), bg=C['card'])
        self.listen_result.pack(pady=(12, 0))
        
        # 统计 + 错词
        self.listen_stats = tk.Label(page, text="正确: 0/0", font=FONT_SMALL, fg=C['text2'], bg=C['bg'])
        self.listen_stats.pack()
    
    def _play_listening_word(self):
        """播放听力单词"""
        # 从错词列表或新词中选择
        candidates = []
        if self._listen_wrong:
            # 错词优先（乱序）
            random.shuffle(self._listen_wrong)
            candidates = self._listen_wrong.copy()
        else:
            # 随机新词
            conn = db.get_db()
            rows = conn.execute('SELECT word FROM words ORDER BY RANDOM() LIMIT 10').fetchall()
            conn.close()
            candidates = [r['word'] for r in rows]
        
        if self._listen_round:
            # 当前轮还有词
            pass
        else:
            self._listen_round = candidates[:5]  # 每轮5个词
            random.shuffle(self._listen_round)
        
        if self._listen_round:
            self._listen_word = self._listen_round.pop(0)
        else:
            self._listen_word = random.choice(candidates) if candidates else 'hello'
        
        self.listen_entry.delete(0, tk.END)
        self.listen_result.configure(text="")
        self.listen_status.configure(text="🔊 播放中... 仔细听！")
        
        if TTS_AVAILABLE and self.tts:
            word = self._listen_word
            def speak():
                try: self.tts.Speak(word, 3)
                except: pass
            self.root.after(100, speak)
    
    def _check_and_show(self):
        """检查答案并显示"""
        self._check_listening(show_answer=True)
    
    def _check_listening(self, show_answer=False):
        if not self._listen_word:
            return
        answer = self.listen_entry.get().strip().lower()
        correct = self._listen_word.lower()
        self._listen_total += 1
        
        if answer == correct:
            self._listen_correct += 1
            result = "✅ 正确！太棒了！"
            fg = C['success']
            # 从错词列表移除
            if self._listen_word in self._listen_wrong:
                self._listen_wrong.remove(self._listen_word)
        elif len(answer) >= 2 and (answer == correct or self._similar(answer, correct, 0.75)):
            self._listen_correct += 1
            result = f"✅ 基本正确！答案: {correct}"
            fg = C['accent']
            if self._listen_word in self._listen_wrong:
                self._listen_wrong.remove(self._listen_word)
        else:
            result = f"❌ 错误。正确答案: {correct}"
            fg = C['danger']
            # 加入错词列表（乱序重排）
            if self._listen_word not in self._listen_wrong:
                self._listen_wrong.append(self._listen_word)
            random.shuffle(self._listen_wrong)
        
        if show_answer:
            self.listen_result.configure(text=result, fg=fg)
            self.listen_entry.delete(0, tk.END)
            self.listen_entry.insert(0, correct)
        
        self.listen_stats.configure(
            text=f"正确: {self._listen_correct}/{self._listen_total}  |  待重练错词: {len(self._listen_wrong)}")
        self.listen_status.configure(text="👆 已显示答案，点击「下一题」继续")
    
    def _similar(self, a, b, threshold=0.7):
        shorter = min(len(a), len(b))
        if shorter == 0: return False
        matches = sum(1 for i in range(shorter) if a[i] == b[i])
        return matches / max(len(a), len(b)) >= threshold
    
    def _next_listening(self):
        """下一题：自动播放"""
        self._play_listening_word()

    # ========== AI 助手页面 ==========
    def _build_ai_page(self):
        page = self.pages['ai']
        
        # 顶部标题行 + API设置
        tf = tk.Frame(page, bg=C['bg']); tf.pack(fill=tk.X, pady=(0, 8))
        tk.Label(tf, text="🤖 AI 学习助手", font=FONT_TITLE, bg=C['bg']).pack(side=tk.LEFT)
        tk.Button(tf, text="⚙️ API设置", command=self._ai_settings,
                 bg=C['text2'], fg='white', font=FONT_SMALL, bd=0, cursor='hand2',
                 padx=12, pady=5).pack(side=tk.RIGHT)
        
        # 对话显示区
        chat_frame = tk.Frame(page, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        
        self.ai_chat_text = tk.Text(chat_frame, font=('Microsoft YaHei UI', 11), wrap=tk.WORD,
                                     bg=C['card'], fg=C['text'], bd=0, padx=14, pady=14,
                                     state='disabled')
        self.ai_chat_text.pack(fill=tk.BOTH, expand=True)
        
        # 滚动到底
        scrollbar = tk.Scrollbar(chat_frame, command=self.ai_chat_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ai_chat_text.configure(yscrollcommand=scrollbar.set)
        
        # 输入区
        input_frame = tk.Frame(page, bg=C['card'], highlightbackground=C['border'], highlightthickness=1)
        input_frame.pack(fill=tk.X)
        input_inner = tk.Frame(input_frame, bg=C['card'])
        input_inner.pack(fill=tk.X, padx=14, pady=12)
        
        # 快捷提问按钮
        quick_frame = tk.Frame(input_inner, bg=C['card'])
        quick_frame.pack(fill=tk.X, pady=(0, 8))
        
        quick_questions = [
            ("语法辨析", "请帮我辨析以下语法点："),
            ("词汇用法", "请解释这个单词的用法："),
            ("写作润色", "请帮我润色这段英文："),
            ("翻译", "请翻译以下内容："),
            ("学习建议", "请给我一些英语学习建议："),
        ]
        for text, prompt in quick_questions:
            tk.Button(quick_frame, text=text, command=lambda p=prompt: self._ai_quick(p),
                     bg=C['hover'], fg=C['primary'], font=FONT_SMALL, bd=0, cursor='hand2',
                     padx=8, pady=3).pack(side=tk.LEFT, padx=2)
        
        # 输入行
        entry_frame = tk.Frame(input_inner, bg=C['card'])
        entry_frame.pack(fill=tk.X)
        
        self.ai_entry = tk.Text(entry_frame, font=('Microsoft YaHei UI', 11), height=3,
                                bd=1, relief='solid', wrap=tk.WORD)
        self.ai_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.ai_entry.bind('<Control-Return>', lambda e: self._ai_send())
        
        tk.Button(entry_frame, text="发送 ➤", command=self._ai_send,
                 bg=C['primary'], fg='white', font=FONT_BODY, bd=0, cursor='hand2',
                 padx=14, pady=8).pack(side=tk.RIGHT, padx=(8, 0))
        
        # 状态
        self.ai_status = tk.Label(input_inner, text="请先在 ⚙️ API设置 中配置API Key（支持OpenAI兼容接口）",
                                  font=FONT_SMALL, fg=C['text3'], bg=C['card'])
        self.ai_status.pack(pady=(4, 0))
        
        # 欢迎消息
        self._ai_append("AI助手", "你好！我是AI学习助手 🤖\n\n"
                       "我可以帮你：\n"
                       "• 解释单词用法和例句\n"
                       "• 辨析语法难点\n"
                       "• 润色英文写作\n"
                       "• 翻译中英文\n"
                       "• 提供学习建议\n\n"
                       "请在 ⚙️ API设置 中填入你的API Key（支持OpenAI、DeepSeek、通义千问等兼容接口）\n"
                       "开始对话吧！Ctrl+Enter 快速发送。")
    
    def _ai_settings(self):
        """API设置对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("API 设置")
        dialog.geometry("500x400")
        dialog.configure(bg=C['card'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 居中
        dialog.update_idletasks()
        w, h = dialog.winfo_width(), dialog.winfo_height()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        dialog.geometry(f'+{(sw-w)//2}+{(sh-h)//2}')
        
        inner = tk.Frame(dialog, bg=C['card'])
        inner.pack(fill=tk.BOTH, padx=24, pady=20)
        
        tk.Label(inner, text="⚙️ AI API 配置", font=FONT_H2, bg=C['card']).pack(anchor='w', pady=(0, 16))
        
        # API Base URL
        tk.Label(inner, text="API 地址 (Base URL):", font=FONT_BODY, bg=C['card']).pack(anchor='w')
        url_var = tk.StringVar(value=db.get_setting('ai_api_url', 'https://api.openai.com/v1'))
        url_entry = tk.Entry(inner, textvariable=url_var, font=('Consolas', 10), bd=1, relief='solid')
        url_entry.pack(fill=tk.X, pady=(4, 12))
        
        # API Key
        tk.Label(inner, text="API Key:", font=FONT_BODY, bg=C['card']).pack(anchor='w')
        key_var = tk.StringVar(value=db.get_setting('ai_api_key', ''))
        key_entry = tk.Entry(inner, textvariable=key_var, font=('Consolas', 10), bd=1, relief='solid', show='*')
        key_entry.pack(fill=tk.X, pady=(4, 12))
        
        # Model
        tk.Label(inner, text="模型名称:", font=FONT_BODY, bg=C['card']).pack(anchor='w')
        model_var = tk.StringVar(value=db.get_setting('ai_model', 'gpt-3.5-turbo'))
        model_combo = ttk.Combobox(inner, textvariable=model_var, 
                                    values=['gpt-3.5-turbo', 'gpt-4', 'gpt-4o', 'gpt-4o-mini',
                                           'deepseek-chat', 'qwen-turbo', 'glm-4'])
        model_combo.pack(fill=tk.X, pady=(4, 16))
        
        # 提示
        tk.Label(inner, text="💡 支持所有 OpenAI 兼容接口\n"
                            "  如 DeepSeek、通义千问、智谱GLM等\n"
                            "  API Key 仅保存在本地",
                font=FONT_SMALL, fg=C['text3'], bg=C['card'], justify=tk.LEFT).pack(anchor='w')
        
        # 按钮
        btn_frame = tk.Frame(inner, bg=C['card'])
        btn_frame.pack(fill=tk.X, pady=(16, 0))
        
        def save_settings():
            db.set_setting('ai_api_url', url_var.get())
            db.set_setting('ai_api_key', key_var.get())
            db.set_setting('ai_model', model_var.get())
            self.ai_status.configure(text="✅ API设置已保存！", fg=C['success'])
            dialog.destroy()
        
        tk.Button(btn_frame, text="💾 保存", command=save_settings,
                 bg=C['primary'], fg='white', font=FONT_BODY, bd=0, cursor='hand2',
                 padx=24, pady=8).pack(side=tk.LEFT)
        
        tk.Button(btn_frame, text="取消", command=dialog.destroy,
                 bg=C['bg'], fg=C['text2'], font=FONT_BODY, bd=0, cursor='hand2',
                 padx=24, pady=8).pack(side=tk.RIGHT)
    
    def _ai_quick(self, prompt):
        """快捷问题"""
        self.ai_entry.delete('1.0', tk.END)
        self.ai_entry.insert('1.0', prompt + ' ')
        self.ai_entry.focus_set()
    
    def _ai_append(self, role, text):
        """追加消息到对话区"""
        self.ai_chat_text.configure(state='normal')
        if role == 'user':
            self.ai_chat_text.insert(tk.END, f"\n🧑 你:\n{text}\n\n", 'user')
        else:
            self.ai_chat_text.insert(tk.END, f"🤖 AI:\n{text}\n\n", 'ai')
        self.ai_chat_text.tag_config('user', foreground=C['primary'], font=('Microsoft YaHei UI', 11, 'bold'))
        self.ai_chat_text.tag_config('ai', foreground=C['text'])
        self.ai_chat_text.configure(state='disabled')
        self.ai_chat_text.see(tk.END)
    
    def _ai_send(self):
        """发送消息到AI"""
        user_msg = self.ai_entry.get('1.0', tk.END).strip()
        if not user_msg:
            return
        
        api_key = db.get_setting('ai_api_key', '')
        if not api_key:
            messagebox.showwarning("提示", "请先在 ⚙️ API设置 中配置API Key")
            return
        
        self._ai_append('user', user_msg)
        self.ai_entry.delete('1.0', tk.END)
        self.ai_status.configure(text="⏳ AI思考中...", fg=C['warning'])
        
        # 异步调用API
        import threading
        def call_api():
            try:
                import urllib.request, urllib.error
                api_url = db.get_setting('ai_api_url', 'https://api.openai.com/v1')
                model = db.get_setting('ai_model', 'gpt-3.5-turbo')
                
                url = api_url.rstrip('/') + '/chat/completions'
                data = json.dumps({
                    'model': model,
                    'messages': [
                        {'role': 'system', 'content': '你是一个高考英语学习助手。请用中文回复，帮助用户学习英语词汇、语法、写作等。回复简洁实用。'},
                        {'role': 'user', 'content': user_msg}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 2000
                }).encode('utf-8')
                
                req = urllib.request.Request(url, data=data, headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {api_key}'
                })
                
                with urllib.request.urlopen(req, timeout=60) as resp:
                    result = json.loads(resp.read().decode('utf-8'))
                    reply = result['choices'][0]['message']['content']
                
                self.root.after(0, lambda: self._ai_append('ai', reply))
                self.root.after(0, lambda: self.ai_status.configure(text="✅ 就绪", fg=C['success']))
                
            except urllib.error.HTTPError as e:
                err_body = e.read().decode('utf-8', errors='replace')
                self.root.after(0, lambda: self._ai_append('ai', f"❌ API错误 ({e.code}):\n{err_body[:300]}"))
                self.root.after(0, lambda: self.ai_status.configure(text=f"❌ HTTP {e.code}", fg=C['danger']))
            except Exception as e:
                self.root.after(0, lambda: self._ai_append('ai', f"❌ 请求失败: {str(e)}"))
                self.root.after(0, lambda: self.ai_status.configure(text="❌ 连接失败", fg=C['danger']))
        
        threading.Thread(target=call_api, daemon=True).start()


# ===================== 高考真题题库 =====================
EXAM_TOPICS = {
    '2024新高考I卷-应用文': {
        'question': '假设你是李华，你校英文报正在举办主题为"公园印象"(Impression of Parks)的摄影展。请你写一封邮件邀请你的英国朋友Chris参加。\n\n注意：1. 词数80左右；2. 可适当增加细节。',
        'keywords': 'invitation, photography exhibition, park, participate, submit works',
        'essay': '''Dear Chris,

I'm writing to invite you to participate in a photography exhibition with the theme "Impression of Parks", which will be held by our school's English newspaper.

The exhibition aims to showcase the beauty of parks through photos. You can submit your best photos of parks, whether in your hometown or from your travels. Each photo should come with a brief caption in English.

The deadline for submission is next Friday. I'm sure your participation will make the exhibition more wonderful.

Looking forward to your reply.

Yours,
Li Hua''',
        'essay2': '''Dear Chris,

How are you doing? I'm excited to tell you that our school English paper is organizing a photo exhibition called "Impression of Parks", and I'd love you to join us.

You can send one or two photos you've taken in any park, along with a short English description. It's a great chance to share your unique perspective and appreciate the beauty of nature.

The exhibition opens on June 15th. Please send your works before June 10th. I really hope you can take part!

Best wishes,
Li Hua'''
    },
    '2024新高考I卷-读后续写': {
        'question': '阅读下面材料，根据其内容和所给段落开头语续写两段，使之构成一篇完整的短文。\n\n材料大意：一位名叫Gunter的出租车司机在暴风雪中帮助了一位赶飞机的乘客，多年后该乘客专程回到维也纳感谢他。\n\nParagraph 1: When I got back to Vienna years later, I decided to find Gunter.\nParagraph 2: Seeing Gunter again, I felt a wave of warmth.',
        'keywords': 'gratitude, kindness, reunion, taxi driver, snowstorm, Vienna',
        'essay': '''When I got back to Vienna years later, I decided to find Gunter. The memory of that snowy night had never faded — how a stranger went out of his way to help me catch my flight. I asked around at the airport taxi stand, describing the kind driver who had driven through a snowstorm for a desperate passenger. "Gunter? Everyone knows Gunter!" a young driver said with a smile, and gave me his phone number. My heart raced as I dialed.

Seeing Gunter again, I felt a wave of warmth. He recognized me immediately, his eyes widening in disbelief. "You came back!" he exclaimed, pulling me into a bear hug. Over coffee, I learned he had been driving taxis for 30 years and had helped countless passengers, but rarely heard from them again. I thanked him from the bottom of my heart, not just for getting me to the airport that night, but for restoring my faith in human kindness. Some debts can never be repaid — they can only be paid forward.'''
    },
    '2024全国甲卷-发言稿': {
        'question': '你校将举办"用英语讲好中国故事"活动。请你写一篇发言稿，介绍一个中国传统节日或文化元素。\n\n注意：1. 词数100左右；2. 可适当增加细节。',
        'keywords': 'Chinese traditional festival, cultural element, speech, Mid-Autumn Festival, Spring Festival',
        'essay': '''Dear fellow students,

Today I'd like to share with you one of the most beautiful Chinese traditions — the Mid-Autumn Festival.

Celebrated on the 15th day of the 8th lunar month, this festival symbolizes family reunion. Families gather to admire the full moon, enjoy mooncakes, and share stories. The most famous legend is about Chang'e, who flew to the moon after drinking an elixir of immortality.

What makes this festival special is its emphasis on togetherness. In our fast-paced world, it reminds us to pause and cherish the people around us. The round moon and round mooncakes both represent completeness and harmony.

I hope you'll experience this magical festival someday. Thank you!''',
        'essay2': '''Good morning, everyone!

I'm honored to talk about the Spring Festival, the most important traditional holiday in China.

The Spring Festival, or Chinese New Year, marks the beginning of the lunar new year. Families gather for a reunion dinner on New Year's Eve, children receive red envelopes, and fireworks light up the sky. Red decorations are everywhere because red symbolizes good fortune.

Behind these customs lies a deeper meaning: the celebration of family bonds and the hope for a fresh start. It teaches us to be grateful for what we have and optimistic about what lies ahead.

That's all. Thank you for listening!'''
    },
    '2023新高考I卷-应用文': {
        'question': '假设你是李华，外教Ryan准备将学生随机分为两人一组进行口语练习，你认为这样分组有问题。请写一封建议信，指出问题并提出建议。',
        'keywords': 'suggestion letter, grouping, oral practice, random pairing, proficiency levels',
        'essay': '''Dear Ryan,

I'm writing to share my thoughts on the grouping plan for oral practice.

While random pairing seems fair, it may create problems. Students with lower speaking proficiency might feel anxious when paired with advanced speakers, while stronger students may not be sufficiently challenged. This could reduce the effectiveness of practice.

I suggest grouping students based on their speaking levels. Beginners could work together with extra teacher support, while intermediate and advanced students could be paired to discuss more complex topics. We could also rotate partners every two weeks to ensure diversity.

I hope you'll consider my suggestions. Thank you for your dedication to improving our spoken English.

Yours sincerely,
Li Hua'''
    },
    '2023新高考I卷-读后续写': {
        'question': '阅读材料后续写：一名学生在老师的鼓励下参加写作比赛并获奖的故事。\n\nParagraph 1: I never thought I could write, until Mrs. Thompson saw something in me.\nParagraph 2: When I stood on the stage holding the first-place certificate, I looked for her in the crowd.',
        'keywords': 'encouragement, writing contest, teacher, self-discovery, confidence',
        'essay': '''I never thought I could write, until Mrs. Thompson saw something in me. She was my English teacher, and one day she kept me after class. "Your journal entries are remarkable," she said, handing me a flyer for a citywide writing contest. I laughed nervously — me, a writer? But her eyes held such conviction that I found myself nodding. For weeks, she stayed after school, reading my drafts, pushing me to dig deeper. "Write what you truly feel," she would say. And slowly, I found my voice.

When I stood on the stage holding the first-place certificate, I looked for her in the crowd. There she was, in the back row, tears streaming down her face, clapping harder than anyone. In that moment, I understood — the greatest teachers don't just teach subjects; they see the potential we cannot see in ourselves. Mrs. Thompson didn't just teach me English; she taught me to believe.'''
    },
    '2023全国乙卷-建议信': {
        'question': '你的英国朋友David计划来中国旅游，请你写一封邮件给他一些建议。内容包括：1.推荐旅游城市；2.提出旅行建议。',
        'keywords': 'travel advice, China, recommendation, attractions, tips',
        'essay': '''Dear David,

I'm thrilled to hear you're planning a trip to China! Let me offer some suggestions.

I highly recommend starting with Beijing. The Forbidden City and the Great Wall are must-sees that will give you a deep insight into Chinese history. Then, take the high-speed train to Xi'an to see the Terracotta Warriors — it's absolutely breathtaking.

Here are some tips: First, download a translation app as it will be very helpful. Second, try the local street food — Beijing's roast duck and Xi'an's hand-pulled noodles are unforgettable. Finally, book your tickets online in advance, especially during holidays.

I'm sure you'll have an amazing time. Let me know if you need more details!

Best,
Li Hua'''
    },
    '建议信模板': {
        'question': '【建议信通用模板】适用于给朋友/老师/学校提出建议的场景。可替换其中的{name}、{topic}等占位符。',
        'keywords': 'suggest, recommend, advise, helpful, consider, improve',
        'essay': '''Dear {name},

I'm writing to offer some suggestions on {topic}.

First of all, I think it would be better to {point1}. This way, {benefit1}. Secondly, why not {point2}? It could help {benefit2}. Last but not least, {point3} might be a good choice because {benefit3}.

I hope my suggestions will be helpful. I would be happy to discuss this further if needed.

Yours sincerely,
Li Hua'''
    },
    '邀请信模板': {
        'question': '【邀请信通用模板】适用于邀请他人参加活动。',
        'keywords': 'invite, participate, event, held, looking forward',
        'essay': '''Dear {name},

I'm writing to invite you to {event}, which will be held {time and place}.

The event will feature {activities}. I'm sure you will find it {adjective}. It would be wonderful if you could join us.

Please let me know if you can make it. Looking forward to your reply.

Yours,
Li Hua'''
    },
    '申请信模板': {
        'question': '【申请信通用模板】适用于申请职位/学校/志愿者等场景。',
        'keywords': 'apply, position, experience, skills, opportunity',
        'essay': '''Dear Sir/Madam,

I'm writing to apply for {position} advertised on {source}.

I'm currently a {grade} student at {school}. I have experience in {experience}, and I'm good at {skills}. Moreover, I'm passionate about {interest}.

I believe I'm a suitable candidate because {reason}. I would be grateful if you could consider my application.

Looking forward to your reply.

Yours faithfully,
Li Hua'''
    },
    '道歉信模板': {
        'question': '【道歉信通用模板】',
        'keywords': 'apologize, sorry, forgive, promise, accept',
        'essay': '''Dear {name},

I'm writing to sincerely apologize for {reason}.

The truth is that {explanation}. I understand this may have caused you {inconvenience}, and I feel terrible about it. Please accept my heartfelt apology.

I promise I will {solution} to make up for it. I hope you can forgive me.

Yours sincerely,
Li Hua'''
    },
    '感谢信模板': {
        'question': '【感谢信通用模板】',
        'keywords': 'gratitude, thank, appreciate, kindness, help',
        'essay': '''Dear {name},

I'm writing to express my sincere gratitude for {reason}.

Your {kindness/help} has made a great difference to me. Without your support, I couldn't have {achievement}. I truly appreciate everything you have done.

Please accept this small token of my appreciation. Thanks again for your generosity.

Yours sincerely,
Li Hua'''
    },
    '议论文模板': {
        'question': '【议论文通用模板】适用于表达观点、讨论话题。',
        'keywords': 'opinion, believe, argue, reason, conclusion',
        'essay': '''Recently, {topic} has become a hot topic of discussion.

Some people believe that {view1}. They argue that {reason1}. However, others hold the opposite opinion. They think {view2} because {reason2}.

In my opinion, {my_view}. On one hand, {pro}. On the other hand, {con}. Therefore, I suggest that {suggestion}.

All in all, {conclusion}. Only by doing so can we {goal}.'''
    },
}


def main():
    root = tk.Tk()
    app = VocabApp(root)
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()

if __name__ == '__main__':
    main()
