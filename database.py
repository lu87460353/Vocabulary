"""
高考英语词汇背诵软件 - 数据库模块
基于《普通高中英语课程标准（2017年版2025年修订）》词汇表
"""
import sqlite3
import json
import os
import sys
from datetime import datetime, date, timedelta

# 数据库路径：打包后在用户目录，开发时在脚本目录
if getattr(sys, 'frozen', False):
    DB_PATH = os.path.join(os.path.expanduser('~'), 'GaokaoVocab_data.db')
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'GaokaoVocab_data.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # 词汇表
    c.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE NOT NULL,
            level INTEGER DEFAULT 0,       -- 0=基础 1=必修* 2=选择性必修**
            translation TEXT DEFAULT '',
            phonetic TEXT DEFAULT '',
            example TEXT DEFAULT ''
        )
    ''')
    
    # 学习记录
    c.execute('''
        CREATE TABLE IF NOT EXISTS learning_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,
            ease_factor REAL DEFAULT 2.5,   -- SM-2 算法参数
            interval_days INTEGER DEFAULT 0,
            repetitions INTEGER DEFAULT 0,
            next_review_date TEXT,
            last_review_date TEXT,
            correct_count INTEGER DEFAULT 0,
            wrong_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'new',       -- new/learning/review/mastered
            first_seen_date TEXT,
            FOREIGN KEY (word_id) REFERENCES words(id)
        )
    ''')
    
    # 错题本
    c.execute('''
        CREATE TABLE IF NOT EXISTS error_book (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER NOT NULL,
            error_type TEXT,                 -- spelling/meaning/listening
            error_time TEXT,
            user_answer TEXT,
            correct_answer TEXT,
            FOREIGN KEY (word_id) REFERENCES words(id)
        )
    ''')
    
    # 每日计划
    c.execute('''
        CREATE TABLE IF NOT EXISTS daily_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plan_date TEXT NOT NULL,
            word_id INTEGER NOT NULL,
            plan_type TEXT DEFAULT 'new',    -- new/review
            completed INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,         -- 0-100
            FOREIGN KEY (word_id) REFERENCES words(id)
        )
    ''')
    
    # 设置/统计
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    # 写作模板
    c.execute('''
        CREATE TABLE IF NOT EXISTS writing_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            template TEXT,
            keywords TEXT
        )
    ''')
    
    # 初始化设置
    defaults = [
        ('daily_new_words', '20'),
        ('review_algorithm', 'sm2'),
        ('daily_goal_minutes', '30'),
        ('streak_days', '0'),
        ('last_study_date', ''),
        ('total_words_learned', '0'),
    ]
    for k, v in defaults:
        c.execute('INSERT OR IGNORE INTO settings(key, value) VALUES(?, ?)', (k, v))
    
    conn.commit()
    conn.close()

def get_setting(key, default=''):
    conn = get_db()
    row = conn.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
    conn.close()
    return row['value'] if row else default

def set_setting(key, value):
    conn = get_db()
    conn.execute('INSERT OR REPLACE INTO settings(key, value) VALUES(?, ?)', (key, str(value)))
    conn.commit()
    conn.close()

# ---- SM-2 间隔重复算法 ----
def sm2_update(ease_factor, interval, repetitions, quality):
    """
    quality: 0-5 (0=完全忘记, 5=完美)
    返回 (new_ef, new_interval, new_repetitions)
    """
    if quality >= 3:
        if repetitions == 0:
            new_interval = 1
        elif repetitions == 1:
            new_interval = 3  # 改小一些
        else:
            new_interval = int(round(interval * ease_factor))
        new_repetitions = repetitions + 1
    else:
        new_interval = 0  # 需要重新学习
        new_repetitions = 0
    
    # 更新 ease factor
    new_ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if new_ef < 1.3:
        new_ef = 1.3
    
    return new_ef, new_interval, new_repetitions

def get_due_review_words(today_str=None):
    """获取今天需要复习的单词"""
    if today_str is None:
        today_str = date.today().isoformat()
    conn = get_db()
    rows = conn.execute('''
        SELECT w.id, w.word, w.translation, w.phonetic, w.level,
               lr.ease_factor, lr.interval_days, lr.repetitions,
               lr.correct_count, lr.wrong_count, lr.status
        FROM words w
        JOIN learning_records lr ON w.id = lr.word_id
        WHERE lr.next_review_date <= ? AND lr.status != 'mastered'
        ORDER BY lr.next_review_date ASC
        LIMIT 50
    ''', (today_str,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_new_words_for_today(count=20):
    """获取今天要学的新词"""
    conn = get_db()
    # 获取还没有学习记录的单词
    rows = conn.execute('''
        SELECT w.id, w.word, w.translation, w.phonetic, w.level
        FROM words w
        WHERE w.id NOT IN (SELECT word_id FROM learning_records)
        ORDER BY w.level ASC, w.word ASC
        LIMIT ?
    ''', (count,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def ensure_learning_record(word_id):
    conn = get_db()
    row = conn.execute('SELECT id FROM learning_records WHERE word_id=?', (word_id,)).fetchone()
    if not row:
        today = date.today().isoformat()
        conn.execute('''
            INSERT INTO learning_records (word_id, first_seen_date, next_review_date, status)
            VALUES (?, ?, ?, 'learning')
        ''', (word_id, today, today))
        conn.commit()
    conn.close()

def record_review(word_id, quality):
    """记录一次复习结果"""
    conn = get_db()
    r = conn.execute('SELECT * FROM learning_records WHERE word_id=?', (word_id,)).fetchone()
    if not r:
        ensure_learning_record(word_id)
        r = conn.execute('SELECT * FROM learning_records WHERE word_id=?', (word_id,)).fetchone()
    
    ef = r['ease_factor']
    iv = r['interval_days']
    rep = r['repetitions']
    
    new_ef, new_iv, new_rep = sm2_update(ef, iv, rep, quality)
    
    today = date.today().isoformat()
    next_date = (date.today() + timedelta(days=new_iv)).isoformat() if new_iv > 0 else today
    
    correct = 1 if quality >= 3 else 0
    wrong = 1 if quality < 3 else 0
    
    new_status = 'learning'
    if new_rep >= 5 and quality >= 4:
        new_status = 'mastered'
    elif new_rep >= 1:
        new_status = 'review'
    
    conn.execute('''
        UPDATE learning_records SET
            ease_factor=?, interval_days=?, repetitions=?,
            next_review_date=?, last_review_date=?,
            correct_count=correct_count+?, wrong_count=wrong_count+?,
            status=?
        WHERE word_id=?
    ''', (new_ef, new_iv, new_rep, next_date, today, correct, wrong, new_status, word_id))
    conn.commit()
    conn.close()
    
    return {'next_review': next_date, 'status': new_status}

def add_to_error_book(word_id, error_type, user_answer, correct_answer):
    conn = get_db()
    conn.execute('''
        INSERT INTO error_book (word_id, error_type, error_time, user_answer, correct_answer)
        VALUES (?, ?, ?, ?, ?)
    ''', (word_id, error_type, datetime.now().isoformat(), user_answer, correct_answer))
    conn.commit()
    conn.close()

def get_error_book(limit=100):
    conn = get_db()
    rows = conn.execute('''
        SELECT w.word, w.translation, eb.error_type, eb.error_time,
               eb.user_answer, eb.correct_answer, eb.id
        FROM error_book eb
        JOIN words w ON eb.word_id = w.id
        ORDER BY eb.error_time DESC
        LIMIT ?
    ''', (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_stats():
    conn = get_db()
    total_words = conn.execute('SELECT COUNT(*) as c FROM words').fetchone()['c']
    learned = conn.execute('SELECT COUNT(*) as c FROM learning_records WHERE repetitions > 0').fetchone()['c']
    mastered = conn.execute("SELECT COUNT(*) as c FROM learning_records WHERE status='mastered'").fetchone()['c']
    reviewing = conn.execute("SELECT COUNT(*) as c FROM learning_records WHERE status IN ('learning','review')").fetchone()['c']
    errors = conn.execute('SELECT COUNT(*) as c FROM error_book').fetchone()['c']
    today = date.today().isoformat()
    due_today = conn.execute('SELECT COUNT(*) as c FROM learning_records WHERE next_review_date <= ? AND status != "mastered"', (today,)).fetchone()['c']
    conn.close()
    return {
        'total': total_words,
        'learned': learned,
        'mastered': mastered,
        'reviewing': reviewing,
        'errors': errors,
        'due_today': due_today,
        'progress': round(learned / total_words * 100, 1) if total_words > 0 else 0
    }

def get_daily_history(days=30):
    conn = get_db()
    result = []
    for i in range(days):
        d = (date.today() - timedelta(days=days-1-i)).isoformat()
        count = conn.execute('''
            SELECT COUNT(*) as c FROM learning_records
            WHERE last_review_date = ?
        ''', (d,)).fetchone()['c']
        result.append({'date': d, 'count': count})
    conn.close()
    return result

def generate_plan(date_str=None, new_words_count=None):
    """生成每日学习计划"""
    if date_str is None:
        date_str = date.today().isoformat()
    if new_words_count is None:
        new_words_count = int(get_setting('daily_new_words', '20'))
    
    conn = get_db()
    
    # 检查是否已有计划
    existing = conn.execute('SELECT COUNT(*) as c FROM daily_plan WHERE plan_date=?', (date_str,)).fetchone()['c']
    if existing > 0:
        conn.close()
        return False  # 已有计划
    
    # 复习单词 - 使用同一个连接
    review_rows = conn.execute('''
        SELECT w.id, w.word
        FROM words w
        JOIN learning_records lr ON w.id = lr.word_id
        WHERE lr.next_review_date <= ? AND lr.status != 'mastered'
        ORDER BY lr.next_review_date ASC
        LIMIT 50
    ''', (date_str,)).fetchall()
    
    for r in review_rows:
        conn.execute('INSERT INTO daily_plan (plan_date, word_id, plan_type) VALUES (?, ?, ?)',
                    (date_str, r['id'], 'review'))
    
    # 新单词 - 使用同一个连接
    new_rows = conn.execute('''
        SELECT w.id
        FROM words w
        WHERE w.id NOT IN (SELECT word_id FROM learning_records)
        ORDER BY w.level ASC, w.word ASC
        LIMIT ?
    ''', (new_words_count,)).fetchall()
    
    today = date.today().isoformat()
    for w in new_rows:
        conn.execute('INSERT INTO daily_plan (plan_date, word_id, plan_type) VALUES (?, ?, ?)',
                    (date_str, w['id'], 'new'))
        # 确保有学习记录
        lr = conn.execute('SELECT id FROM learning_records WHERE word_id=?', (w['id'],)).fetchone()
        if not lr:
            conn.execute('''
                INSERT INTO learning_records (word_id, first_seen_date, next_review_date, status)
                VALUES (?, ?, ?, 'learning')
            ''', (w['id'], today, today))
    
    conn.commit()
    conn.close()
    return True

def get_today_plan(date_str=None):
    if date_str is None:
        date_str = date.today().isoformat()
    conn = get_db()
    rows = conn.execute('''
        SELECT dp.id as plan_id, dp.plan_type, dp.completed, dp.score,
               w.id as word_id, w.word, w.translation, w.phonetic, w.level
        FROM daily_plan dp
        JOIN words w ON dp.word_id = w.id
        WHERE dp.plan_date = ?
        ORDER BY dp.plan_type DESC, w.word ASC
    ''', (date_str,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_today_progress():
    today = date.today().isoformat()
    conn = get_db()
    total = conn.execute('SELECT COUNT(*) as c FROM daily_plan WHERE plan_date=?', (today,)).fetchone()['c']
    done = conn.execute('SELECT COUNT(*) as c FROM daily_plan WHERE plan_date=? AND completed=1', (today,)).fetchone()['c']
    conn.close()
    return {'total': total, 'done': done, 'pct': round(done/total*100, 1) if total > 0 else 0}

def init_writing_templates():
    """初始化一些写作模板"""
    conn = get_db()
    count = conn.execute('SELECT COUNT(*) as c FROM writing_templates').fetchone()['c']
    if count == 0:
        templates = [
            ('建议信', 'Dear {name},\n\nI\'m writing to give you some suggestions on {topic}.\n\nFirst of all, {point1}.\nSecondly, {point2}.\nLast but not least, {point3}.\n\nI hope my suggestions will be helpful to you.\n\nYours sincerely,\n{your_name}',
             'suggest,advise,recommend,helpful,consider'),
            ('邀请信', 'Dear {name},\n\nI\'m writing to invite you to {event}.\n\nThe event will be held {time_place}.\n\nDuring the event, we will {activities}.\n\nI\'m sure you will have a great time.\n\nLooking forward to your reply.\n\nYours,\n{your_name}',
             'invite,event,hold,activity,look forward to'),
            ('申请信', 'Dear Sir/Madam,\n\nI\'m writing to apply for {position}.\n\nI\'m {age} years old and I\'m good at {skills}.\n\nI have experience in {experience}.\n\nI would be grateful if you could give me this opportunity.\n\nLooking forward to your reply.\n\nYours faithfully,\n{your_name}',
             'apply,position,experience,opportunity,grateful'),
            ('道歉信', 'Dear {name},\n\nI\'m writing to apologize for {reason}.\n\nThe reason is that {explanation}.\n\nI sincerely hope you can accept my apology.\n\nI promise it won\'t happen again.\n\nYours sincerely,\n{your_name}',
             'apologize,sorry,forgive,promise,accept'),
            ('感谢信', 'Dear {name},\n\nI\'m writing to express my sincere gratitude for {reason}.\n\nWithout your help, I couldn\'t have {achievement}.\n\nYour kindness means a lot to me.\n\nThanks again for everything.\n\nYours sincerely,\n{your_name}',
             'gratitude,thank,kindness,help,appreciate'),
            ('议论文模板', '{topic} has become a hot topic recently.\n\nSome people think that {view1}, while others believe that {view2}.\n\nIn my opinion, {my_view}.\n\nOn one hand, {reason1}.\nOn the other hand, {reason2}.\n\nIn conclusion, {conclusion}.\n\nOnly in this way can we {goal}.',
             'opinion,believe,reason,conclusion,argue'),
        ]
        for t in templates:
            conn.execute('INSERT INTO writing_templates (topic, template, keywords) VALUES (?, ?, ?)', t)
        conn.commit()
    conn.close()

print("数据库模块加载完成")
