#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
聖誕交換禮物抽籤系統 - Christmas Gift Exchange Lottery System
支援隨機抽取、避免重複、歷史記錄和郵件通知功能
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, font
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import math


class LotterySystem:
    """抽籤系統核心類別"""

    def __init__(self):
        self.participants = []  # 參與者清單 - 現在每個參與者都有自己的關鍵字: {name, email, keywords: [...]}
        self.drawn_items = []   # 已抽取的參與者
        self.history = []       # 歷史記錄
        self.config = {}        # SMTP設定

        # 關鍵字抽籤相關
        self.keyword_history = []  # 關鍵字抽籤歷史

        # 檔案路徑
        self.participants_file = 'participants.json'
        self.history_file = 'lottery_history.json'
        self.config_file = 'config.json'
        self.keyword_history_file = 'keyword_lottery_history.json'

        # 載入資料
        self.load_participants()
        self.load_history()
        self.load_config()
        self.load_keyword_history()

    # ========== 參與者管理 ==========

    def load_participants(self):
        """從 JSON 檔案載入參與者資料"""
        try:
            if os.path.exists(self.participants_file):
                with open(self.participants_file, 'r', encoding='utf-8') as f:
                    self.participants = json.load(f)
                    # 確保每個參與者都有 keywords 欄位(向後相容)
                    for p in self.participants:
                        if 'keywords' not in p:
                            p['keywords'] = []
            else:
                self.participants = []
        except Exception as e:
            print(f"載入參與者失敗: {e}")
            self.participants = []

    def save_participants(self):
        """儲存參與者資料到 JSON 檔案"""
        try:
            with open(self.participants_file, 'w', encoding='utf-8') as f:
                json.dump(self.participants, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"儲存參與者失敗: {e}")
            return False

    def add_participant(self, name, email, keywords=None):
        """新增參與者

        Args:
            name: 參與者姓名
            email: 參與者郵箱
            keywords: 參與者的關鍵字清單(可選)
        """
        if not name or not email:
            return False, "姓名和郵箱不能為空"

        # 檢查是否已存在
        for p in self.participants:
            if p['email'] == email:
                return False, "該郵箱已存在"

        self.participants.append({
            'name': name,
            'email': email,
            'keywords': keywords if keywords else []
        })
        self.save_participants()
        return True, "新增成功"

    def remove_participant(self, email):
        """刪除參與者"""
        self.participants = [p for p in self.participants if p['email'] != email]
        # 同時從已抽取清單中移除
        self.drawn_items = [p for p in self.drawn_items if p['email'] != email]
        self.save_participants()

    def batch_import_participants(self, text_data):
        """批次匯入參與者
        格式: 姓名,郵箱 (每行一個)
        """
        success_count = 0
        fail_count = 0

        lines = text_data.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            parts = line.split(',')
            if len(parts) != 2:
                fail_count += 1
                continue

            name = parts[0].strip()
            email = parts[1].strip()

            success, _ = self.add_participant(name, email)
            if success:
                success_count += 1
            else:
                fail_count += 1

        return success_count, fail_count

    # ========== 抽籤邏輯 ==========

    def get_available_count(self):
        """取得可抽取人數"""
        available = [p for p in self.participants if p not in self.drawn_items]
        return len(available)

    def draw(self, count, avoid_repeat=True):
        """執行抽籤

        Args:
            count: 抽取數量
            avoid_repeat: 是否避免重複抽取

        Returns:
            (success, result, message)
        """
        if not self.participants:
            return False, [], "參與者清單為空"

        # 確定可抽取的參與者池
        if avoid_repeat:
            available = [p for p in self.participants if p not in self.drawn_items]
        else:
            available = self.participants.copy()

        if len(available) < count:
            return False, [], f"可抽取人數不足（可抽取: {len(available)}, 需要: {count}）"

        # 隨機抽取
        selected = random.sample(available, count)

        # 更新已抽取清單
        if avoid_repeat:
            self.drawn_items.extend(selected)

        return True, selected, "抽籤成功"

    def reset_drawn(self):
        """重置已抽取清單"""
        self.drawn_items = []

    def is_drawn(self, participant):
        """檢查參與者是否已被抽取"""
        return participant in self.drawn_items

    # ========== 历史记录 ==========

    def save_history(self, selected, count, mode):
        """保存历史记录"""
        record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'selected': selected,
            'count': count,
            'mode': mode
        }
        self.history.append(record)

        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"儲存歷史記錄失敗: {e}")

    def load_history(self):
        """從檔案載入歷史記錄"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception as e:
            print(f"載入歷史記錄失敗: {e}")
            self.history = []

    def get_history(self):
        """取得歷史記錄清單"""
        return self.history

    def clear_history(self):
        """清空歷史記錄"""
        self.history = []
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
        except Exception as e:
            print(f"清空歷史記錄失敗: {e}")

    # ========== 設定管理 ==========

    def load_config(self):
        """載入 SMTP 設定"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'smtp_user': '',
                    'smtp_password': '',
                    'from_email': ''
                }
        except Exception as e:
            print(f"載入設定失敗: {e}")
            self.config = {}

    def save_config(self, config):
        """儲存 SMTP 設定"""
        self.config = config
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"儲存設定失敗: {e}")
            return False

    def validate_config(self):
        """驗證設定是否完整"""
        required_keys = ['smtp_server', 'smtp_port', 'smtp_user', 'smtp_password', 'from_email']
        for key in required_keys:
            if key not in self.config or not self.config[key]:
                return False
        return True

    # ========== 郵件傳送 ==========

    def send_email(self, to_email, to_name, timestamp):
        """傳送郵件通知

        Args:
            to_email: 收件人郵箱
            to_name: 收件人姓名
            timestamp: 抽籤時間

        Returns:
            (success, message)
        """
        if not self.validate_config():
            return False, "郵件設定不完整,請先在設定頁面設定 SMTP"

        try:
            # 建立郵件
            msg = MIMEMultipart()
            msg['From'] = self.config['from_email']
            msg['To'] = to_email
            msg['Subject'] = '抽籤通知'

            # 郵件正文
            body = f"""您好 {to_name},

恭喜您在本次抽籤中被抽中!

抽籤時間: {timestamp}

此郵件由抽籤系統自動傳送。
"""
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 連接 SMTP 伺服器並傳送
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['smtp_user'], self.config['smtp_password'])
            server.send_message(msg)
            server.quit()

            return True, "郵件傳送成功"

        except Exception as e:
            return False, f"郵件傳送失敗: {str(e)}"

    def send_test_email(self, test_email):
        """傳送測試郵件"""
        if not self.validate_config():
            return False, "郵件設定不完整"

        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['from_email']
            msg['To'] = test_email
            msg['Subject'] = '抽籤系統 - 測試郵件'

            body = """這是一封測試郵件。

如果您收到此郵件,說明 SMTP 設定正確。

此郵件由抽籤系統自動傳送。
"""
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['smtp_user'], self.config['smtp_password'])
            server.send_message(msg)
            server.quit()

            return True, "測試郵件傳送成功"

        except Exception as e:
            return False, f"測試郵件傳送失敗: {str(e)}"

    # ========== 參與者關鍵字管理 ==========

    def add_keyword_to_participant(self, email, keyword):
        """為指定參與者新增關鍵字

        Args:
            email: 參與者郵箱
            keyword: 關鍵字

        Returns:
            (success, message)
        """
        if not keyword:
            return False, "關鍵字不能為空"

        # 找到參與者
        participant = None
        for p in self.participants:
            if p['email'] == email:
                participant = p
                break

        if not participant:
            return False, "找不到該參與者"

        # 檢查關鍵字是否已存在
        if keyword in participant['keywords']:
            return False, "該參與者已有此關鍵字"

        participant['keywords'].append(keyword)
        self.save_participants()
        return True, "新增成功"

    def remove_keyword_from_participant(self, email, keyword):
        """從指定參與者移除關鍵字

        Args:
            email: 參與者郵箱
            keyword: 關鍵字
        """
        for p in self.participants:
            if p['email'] == email:
                if keyword in p['keywords']:
                    p['keywords'].remove(keyword)
                self.save_participants()
                break

    def batch_import_keywords_for_participant(self, email, text_data):
        """為指定參與者批次匯入關鍵字
        格式: 每行一個關鍵字

        Args:
            email: 參與者郵箱
            text_data: 關鍵字文本數據

        Returns:
            (success_count, fail_count)
        """
        success_count = 0
        fail_count = 0

        lines = text_data.strip().split('\n')
        for line in lines:
            keyword = line.strip()
            if not keyword:
                continue

            success, _ = self.add_keyword_to_participant(email, keyword)
            if success:
                success_count += 1
            else:
                fail_count += 1

        return success_count, fail_count

    def get_participant_by_email(self, email):
        """根據郵箱取得參與者

        Args:
            email: 參與者郵箱

        Returns:
            participant dict or None
        """
        for p in self.participants:
            if p['email'] == email:
                return p
        return None

    # ========== 關鍵字抽籤邏輯 ==========

    def draw_keywords(self, participant_count):
        """執行關鍵字抽籤 - 每人抽取2個關鍵字（分兩輪進行）

        新規則:
        - 每位參與者從其他所有參與者的關鍵字中抽取
        - 不會抽到自己的關鍵字
        - 兩輪抽籤中都不會出現重複的關鍵字（第一輪抽過的關鍵字，第二輪不會再出現）

        Args:
            participant_count: 參與人數

        Returns:
            (success, result_dict, message)
            result_dict 格式: {email: {name, email, keywords: [kw1, kw2]}, ...}
        """
        if not self.participants:
            return False, {}, "參與者清單為空"

        # 確定參與抽籤的人員
        if participant_count > len(self.participants):
            return False, {}, f"參與人數超過總參與者數（總數: {len(self.participants)}）"

        # 隨機選擇參與者
        selected_participants = random.sample(self.participants, participant_count)

        # 建立全域關鍵字池 (所有參與者的關鍵字)
        all_keywords = []
        for p in self.participants:
            all_keywords.extend(p['keywords'])

        if len(all_keywords) < participant_count * 2:
            return False, {}, f"關鍵字總數不足（總數: {len(all_keywords)}, 需要: {participant_count * 2}）"

        # 初始化結果字典
        result_dict = {}
        for participant in selected_participants:
            result_dict[participant['email']] = {
                'name': participant['name'],
                'email': participant['email'],
                'keywords': []
            }

        # 全域已使用關鍵字（兩輪共用，確保完全不重複）
        used_keywords_global = []

        # 第一輪抽籤 - 每人抽 1 個關鍵字
        for participant in selected_participants:
            # 建立當前參與者可用的關鍵字池:
            # 1. 排除自己的關鍵字
            # 2. 排除全域已使用的關鍵字
            available_for_this_participant = []
            for p in self.participants:
                if p['email'] != participant['email']:  # 不抽自己的關鍵字
                    for keyword in p['keywords']:
                        if keyword not in used_keywords_global:  # 避免重複
                            available_for_this_participant.append(keyword)

            if len(available_for_this_participant) < 1:
                return False, {}, f"第一輪: 參與者 {participant['name']} 的可用關鍵字不足（可用: {len(available_for_this_participant)}, 需要: 1）"

            # 為當前參與者抽取 1 個關鍵字
            keyword = random.choice(available_for_this_participant)
            result_dict[participant['email']]['keywords'].append(keyword)
            used_keywords_global.append(keyword)

        # 第二輪抽籤 - 每人再抽 1 個關鍵字
        for participant in selected_participants:
            # 建立當前參與者可用的關鍵字池:
            # 1. 排除自己的關鍵字
            # 2. 排除全域已使用的關鍵字（包含第一輪）
            available_for_this_participant = []
            for p in self.participants:
                if p['email'] != participant['email']:  # 不抽自己的關鍵字
                    for keyword in p['keywords']:
                        if keyword not in used_keywords_global:  # 避免重複
                            available_for_this_participant.append(keyword)

            if len(available_for_this_participant) < 1:
                return False, {}, f"第二輪: 參與者 {participant['name']} 的可用關鍵字不足（可用: {len(available_for_this_participant)}, 需要: 1）"

            # 為當前參與者抽取 1 個關鍵字
            keyword = random.choice(available_for_this_participant)
            result_dict[participant['email']]['keywords'].append(keyword)
            used_keywords_global.append(keyword)

        return True, result_dict, "抽籤成功"

    # ========== 關鍵字抽籤歷史記錄 ==========

    def save_keyword_history(self, result_dict, participant_count, mode, display_mode):
        """保存關鍵字抽籤歷史記錄"""
        record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'participant_count': participant_count,
            'mode': mode,  # 'display', 'email', 'both'
            'display_mode': display_mode,  # 'with_name', 'anonymous'
            'results': result_dict
        }
        self.keyword_history.append(record)

        try:
            with open(self.keyword_history_file, 'w', encoding='utf-8') as f:
                json.dump(self.keyword_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"儲存關鍵字抽籤歷史記錄失敗: {e}")

    def load_keyword_history(self):
        """從檔案載入關鍵字抽籤歷史記錄"""
        try:
            if os.path.exists(self.keyword_history_file):
                with open(self.keyword_history_file, 'r', encoding='utf-8') as f:
                    self.keyword_history = json.load(f)
            else:
                self.keyword_history = []
        except Exception as e:
            print(f"載入關鍵字抽籤歷史記錄失敗: {e}")
            self.keyword_history = []

    def get_keyword_history(self):
        """取得關鍵字抽籤歷史記錄清單"""
        return self.keyword_history

    def clear_keyword_history(self):
        """清空關鍵字抽籤歷史記錄"""
        self.keyword_history = []
        try:
            if os.path.exists(self.keyword_history_file):
                os.remove(self.keyword_history_file)
        except Exception as e:
            print(f"清空關鍵字抽籤歷史記錄失敗: {e}")

    # ========== 關鍵字抽籤郵件傳送 ==========

    def send_keyword_email(self, to_email, to_name, keywords, timestamp):
        """傳送關鍵字抽籤郵件通知

        Args:
            to_email: 收件人郵箱
            to_name: 收件人姓名
            keywords: 抽到的關鍵字列表 [keyword1, keyword2]
            timestamp: 抽籤時間

        Returns:
            (success, message)
        """
        if not self.validate_config():
            return False, "郵件設定不完整,請先在設定頁面設定 SMTP"

        try:
            # 建立郵件
            msg = MIMEMultipart()
            msg['From'] = self.config['from_email']
            msg['To'] = to_email
            msg['Subject'] = '關鍵字抽籤通知'

            # 郵件正文
            body = f"""您好 {to_name},

恭喜您在本次關鍵字抽籤中抽到以下關鍵字:

1. {keywords[0]}
2. {keywords[1]}

抽籤時間: {timestamp}

此郵件由抽籤系統自動傳送。
"""
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 連接 SMTP 伺服器並傳送
            server = smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port'])
            server.starttls()
            server.login(self.config['smtp_user'], self.config['smtp_password'])
            server.send_message(msg)
            server.quit()

            return True, "郵件傳送成功"

        except Exception as e:
            return False, f"郵件傳送失敗: {str(e)}"


class Snowflake:
    """雪花類別 - 用於創建雪花動畫"""
    def __init__(self, canvas, x, y, size, speed):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.swing = random.uniform(-1, 1)
        self.swing_speed = random.uniform(0.02, 0.05)
        self.swing_angle = random.uniform(0, 2 * math.pi)

        # 創建雪花 (使用 * 符號)
        self.id = canvas.create_text(
            x, y, text='❄', fill='white',
            font=('Arial', size), tags='snowflake'
        )

    def move(self):
        """移動雪花"""
        self.y += self.speed
        self.swing_angle += self.swing_speed
        swing_x = math.sin(self.swing_angle) * 2
        self.x += swing_x

        self.canvas.coords(self.id, self.x, self.y)

        # 如果雪花落到底部,重置到頂部
        canvas_height = self.canvas.winfo_height()
        if self.y > canvas_height:
            self.y = -20
            self.x = random.randint(0, self.canvas.winfo_width())
            self.canvas.coords(self.id, self.x, self.y)


class ChristmasTheme:
    """聖誕主題配置"""
    # 聖誕色彩方案
    BG_COLOR = '#0d1b2a'  # 深藍色背景
    SNOW_BG = '#1b263b'  # 雪夜藍
    ACCENT_RED = '#c1121f'  # 聖誕紅
    ACCENT_GREEN = '#2d6a4f'  # 聖誕綠
    ACCENT_GOLD = '#ffd700'  # 金色
    TEXT_WHITE = '#f8f9fa'  # 白色文字
    TEXT_LIGHT = '#dee2e6'  # 淺色文字
    BUTTON_RED = '#c1121f'  # 紅色按鈕
    BUTTON_GREEN = '#2d6a4f'  # 綠色按鈕
    BUTTON_GOLD = '#d4a137'  # 金色按鈕
    FRAME_BG = '#1b263b'  # 框架背景

    @staticmethod
    def configure_style():
        """配置ttk樣式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 配置Notebook (標籤頁)
        style.configure('TNotebook', background=ChristmasTheme.BG_COLOR, borderwidth=0)
        style.configure('TNotebook.Tab',
                       background=ChristmasTheme.ACCENT_GREEN,
                       foreground=ChristmasTheme.TEXT_WHITE,
                       padding=[20, 10],
                       font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', ChristmasTheme.ACCENT_RED)],
                 foreground=[('selected', ChristmasTheme.TEXT_WHITE)],
                 padding=[('selected', [20, 10])])

        # 配置Frame
        style.configure('TFrame', background=ChristmasTheme.BG_COLOR)
        style.configure('TLabelframe',
                       background=ChristmasTheme.FRAME_BG,
                       foreground=ChristmasTheme.TEXT_WHITE,
                       borderwidth=2,
                       relief='ridge')
        style.configure('TLabelframe.Label',
                       background=ChristmasTheme.FRAME_BG,
                       foreground=ChristmasTheme.ACCENT_GOLD,
                       font=('Arial', 11, 'bold'))

        # 配置Button
        style.configure('Red.TButton',
                       background=ChristmasTheme.BUTTON_RED,
                       foreground=ChristmasTheme.TEXT_WHITE,
                       borderwidth=0,
                       font=('Arial', 10, 'bold'),
                       padding=[15, 8])
        style.map('Red.TButton',
                 background=[('active', '#a01018')])

        style.configure('Green.TButton',
                       background=ChristmasTheme.BUTTON_GREEN,
                       foreground=ChristmasTheme.TEXT_WHITE,
                       borderwidth=0,
                       font=('Arial', 10, 'bold'),
                       padding=[15, 8])
        style.map('Green.TButton',
                 background=[('active', '#245940')])

        style.configure('Gold.TButton',
                       background=ChristmasTheme.BUTTON_GOLD,
                       foreground='#1b263b',
                       borderwidth=0,
                       font=('Arial', 10, 'bold'),
                       padding=[15, 8])
        style.map('Gold.TButton',
                 background=[('active', '#b8860b')])

        # 配置Label
        style.configure('TLabel',
                       background=ChristmasTheme.FRAME_BG,
                       foreground=ChristmasTheme.TEXT_LIGHT,
                       font=('Arial', 10))

        style.configure('Title.TLabel',
                       background=ChristmasTheme.BG_COLOR,
                       foreground=ChristmasTheme.ACCENT_GOLD,
                       font=('Arial', 16, 'bold'))

        # 配置Radiobutton
        style.configure('TRadiobutton',
                       background=ChristmasTheme.FRAME_BG,
                       foreground=ChristmasTheme.TEXT_LIGHT,
                       font=('Arial', 10))
        style.map('TRadiobutton',
                 background=[('active', ChristmasTheme.FRAME_BG)],
                 foreground=[('active', ChristmasTheme.TEXT_WHITE)])

        # 配置Checkbutton
        style.configure('TCheckbutton',
                       background=ChristmasTheme.FRAME_BG,
                       foreground=ChristmasTheme.TEXT_LIGHT,
                       font=('Arial', 10))
        style.map('TCheckbutton',
                 background=[('active', ChristmasTheme.FRAME_BG)],
                 foreground=[('active', ChristmasTheme.TEXT_WHITE)])


class LotteryGUI:
    """聖誕交換禮物抽籤系統 GUI 介面"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎄 聖誕交換禮物抽籤系統 🎁")
        self.root.geometry("1000x750")
        self.root.configure(bg=ChristmasTheme.BG_COLOR)

        # 配置主題樣式
        ChristmasTheme.configure_style()

        # 建立抽籤系統實例
        self.lottery = LotterySystem()

        # 雪花列表
        self.snowflakes = []

        # 創建雪花畫布背景(先創建畫布)
        self.create_snow_canvas()

        # 創建頂部裝飾區域
        self.create_header()

        # 建立標籤頁
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        # 建立各個頁面
        self.create_draw_page()
        self.create_participant_page()
        self.create_history_page()
        self.create_keyword_draw_page()
        self.create_keyword_manage_page()
        self.create_keyword_history_page()
        self.create_settings_page()

        # 啟動雪花動畫
        self.animate_snow()

    def create_header(self):
        """創建頂部聖誕裝飾"""
        header = tk.Frame(self.root, bg=ChristmasTheme.BG_COLOR, height=80)
        header.pack(fill='x', padx=15, pady=(15, 10))
        header.pack_propagate(False)

        # 聖誕標題
        title_font = font.Font(family='Arial', size=24, weight='bold')
        title = tk.Label(header,
                        text="🎅 聖誕交換禮物抽籤系統 🎄",
                        font=title_font,
                        bg=ChristmasTheme.BG_COLOR,
                        fg=ChristmasTheme.ACCENT_GOLD)
        title.pack(pady=10)

        # 副標題
        subtitle = tk.Label(header,
                          text="✨ Merry Christmas & Happy Gift Exchange! ✨",
                          font=('Arial', 12, 'italic'),
                          bg=ChristmasTheme.BG_COLOR,
                          fg=ChristmasTheme.TEXT_LIGHT)
        subtitle.pack()

    def create_snow_canvas(self):
        """創建雪花背景畫布"""
        self.snow_canvas = tk.Canvas(self.root,
                                     bg=ChristmasTheme.BG_COLOR,
                                     highlightthickness=0)
        # 使用place將畫布放在背景
        self.snow_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # 創建雪花
        for _ in range(50):
            x = random.randint(0, 1000)
            y = random.randint(-500, 750)
            size = random.randint(12, 24)
            speed = random.uniform(1, 3)
            snowflake = Snowflake(self.snow_canvas, x, y, size, speed)
            self.snowflakes.append(snowflake)

    def animate_snow(self):
        """雪花動畫循環"""
        for snowflake in self.snowflakes:
            snowflake.move()

        # 每30毫秒更新一次
        self.root.after(30, self.animate_snow)

    # ========== 抽籤頁面 ==========

    def create_draw_page(self):
        """建立抽籤頁面"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎁 禮物抽籤")

        # 模式選擇
        mode_frame = ttk.LabelFrame(frame, text="🎅 抽籤模式", padding=10)
        mode_frame.pack(fill='x', padx=10, pady=10)

        self.draw_mode = tk.StringVar(value="display")
        ttk.Radiobutton(mode_frame, text="📺 顯示在畫面上", variable=self.draw_mode,
                       value="display").pack(anchor='w', pady=3)
        ttk.Radiobutton(mode_frame, text="📧 僅傳送郵件通知", variable=self.draw_mode,
                       value="email").pack(anchor='w', pady=3)

        # 抽籤設定
        settings_frame = ttk.LabelFrame(frame, text="⚙️ 抽籤設定", padding=10)
        settings_frame.pack(fill='x', padx=10, pady=10)

        # 抽取數量
        count_frame = ttk.Frame(settings_frame)
        count_frame.pack(fill='x', pady=5)
        ttk.Label(count_frame, text="🎯 抽取數量:").pack(side='left')
        self.draw_count = tk.IntVar(value=1)
        spinbox = ttk.Spinbox(count_frame, from_=1, to=100, textvariable=self.draw_count,
                             width=10, font=('Arial', 10))
        spinbox.pack(side='left', padx=10)

        # 避免重複
        self.avoid_repeat = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="🔒 避免重複抽取",
                       variable=self.avoid_repeat).pack(anchor='w', pady=3)

        # 狀態資訊
        status_frame = ttk.Frame(settings_frame)
        status_frame.pack(fill='x', pady=5)
        self.status_label = ttk.Label(status_frame, text="", font=('Arial', 10, 'bold'))
        self.status_label.pack(anchor='w')
        self.update_status()

        # 操作按鈕
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_frame, text="🎁 開始抽籤", style='Red.TButton',
                  command=self.do_draw).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔄 重置已抽取清單", style='Green.TButton',
                  command=self.reset_drawn).pack(side='left', padx=5)

        # 結果顯示區域
        result_frame = ttk.LabelFrame(frame, text="🎄 抽籤結果", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.result_text = scrolledtext.ScrolledText(
            result_frame, height=15,
            bg=ChristmasTheme.SNOW_BG,
            fg=ChristmasTheme.TEXT_WHITE,
            font=('Courier New', 11),
            insertbackground=ChristmasTheme.TEXT_WHITE
        )
        self.result_text.pack(fill='both', expand=True)

    def update_status(self):
        """更新狀態資訊"""
        total = len(self.lottery.participants)
        available = self.lottery.get_available_count()
        drawn = len(self.lottery.drawn_items)
        self.status_label.config(
            text=f"👥 總參與者: {total} | 🎯 可抽取: {available} | ✅ 已抽取: {drawn}",
            foreground=ChristmasTheme.ACCENT_GOLD
        )

    def do_draw(self):
        """執行抽籤"""
        count = self.draw_count.get()
        avoid_repeat = self.avoid_repeat.get()
        mode = self.draw_mode.get()

        # 執行抽籤
        success, selected, message = self.lottery.draw(count, avoid_repeat)

        if not success:
            messagebox.showerror("❌ 錯誤", message)
            return

        # 記錄時間
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 顯示模式
        if mode == "display":
            result = f"\n{'🎄'*25}\n"
            result += f"🎅 抽籤時間: {timestamp}\n"
            result += f"🎁 抽取數量: {count}\n"
            result += f"{'='*50}\n"
            result += f"🎉 恭喜以下幸運兒獲得禮物:\n"
            result += f"{'='*50}\n"
            for i, p in enumerate(selected, 1):
                result += f"  🎁 {i}. {p['name']} ({p['email']})\n"
            result += f"{'🎄'*25}\n\n"

            self.result_text.insert('1.0', result)
            messagebox.showinfo("🎉 成功", "抽籤完成!恭喜所有中獎者!")

        # 郵件模式
        elif mode == "email":
            success_count = 0
            fail_count = 0

            for p in selected:
                success, msg = self.lottery.send_email(p['email'], p['name'], timestamp)
                if success:
                    success_count += 1
                else:
                    fail_count += 1

            result_msg = f"郵件傳送完成\n✅ 成功: {success_count} | ❌ 失敗: {fail_count}"

            if fail_count > 0:
                messagebox.showwarning("⚠️ 部分失敗", result_msg)
            else:
                messagebox.showinfo("✅ 成功", result_msg)

        # 儲存歷史記錄
        self.lottery.save_history(selected, count, mode)

        # 更新狀態
        self.update_status()

    def reset_drawn(self):
        """重置已抽取清單"""
        if messagebox.askyesno("🔄 確認", "確定要重置已抽取清單嗎?"):
            self.lottery.reset_drawn()
            self.update_status()
            messagebox.showinfo("✅ 成功", "已抽取清單已重置")

    # ========== 參與者管理頁面 ==========

    def create_participant_page(self):
        """建立參與者管理頁面"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👥 參與者管理")

        # 單個新增區域
        add_frame = ttk.LabelFrame(frame, text="➕ 新增參與者", padding=10)
        add_frame.pack(fill='x', padx=10, pady=10)

        # 姓名
        name_frame = ttk.Frame(add_frame)
        name_frame.pack(fill='x', pady=5)
        ttk.Label(name_frame, text="👤 姓名:", width=10).pack(side='left')
        self.participant_name = tk.StringVar()
        entry = ttk.Entry(name_frame, textvariable=self.participant_name, width=30, font=('Arial', 10))
        entry.pack(side='left', padx=5)

        # 郵箱
        email_frame = ttk.Frame(add_frame)
        email_frame.pack(fill='x', pady=5)
        ttk.Label(email_frame, text="📧 郵箱:", width=10).pack(side='left')
        self.participant_email = tk.StringVar()
        entry = ttk.Entry(email_frame, textvariable=self.participant_email, width=30, font=('Arial', 10))
        entry.pack(side='left', padx=5)

        # 新增按鈕
        ttk.Button(add_frame, text="➕ 新增", style='Green.TButton',
                  command=self.add_participant).pack(pady=5)

        # 批次匯入區域
        import_frame = ttk.LabelFrame(frame, text="📋 批次匯入（格式: 姓名,郵箱）", padding=10)
        import_frame.pack(fill='x', padx=10, pady=10)

        self.import_text = scrolledtext.ScrolledText(
            import_frame, height=5,
            bg=ChristmasTheme.SNOW_BG,
            fg=ChristmasTheme.TEXT_WHITE,
            font=('Courier New', 10),
            insertbackground=ChristmasTheme.TEXT_WHITE
        )
        self.import_text.pack(fill='x', pady=5)

        ttk.Button(import_frame, text="📥 批次匯入", style='Gold.TButton',
                  command=self.batch_import).pack(pady=5)

        # 參與者清單
        list_frame = ttk.LabelFrame(frame, text="📜 參與者清單", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 建立表格
        columns = ('name', 'email', 'status')
        self.participant_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        self.participant_tree.heading('name', text='👤 姓名')
        self.participant_tree.heading('email', text='📧 郵箱')
        self.participant_tree.heading('status', text='📊 狀態')

        self.participant_tree.column('name', width=150)
        self.participant_tree.column('email', width=250)
        self.participant_tree.column('status', width=100)

        # 捲軸
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical',
                                 command=self.participant_tree.yview)
        self.participant_tree.configure(yscrollcommand=scrollbar.set)

        self.participant_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # 操作按鈕
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', pady=5)

        ttk.Button(button_frame, text="🗑️ 刪除選中", style='Red.TButton',
                  command=self.remove_participant).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔄 重新整理清單", style='Green.TButton',
                  command=self.refresh_participant_list).pack(side='left', padx=5)

        # 初始載入清單
        self.refresh_participant_list()

    def add_participant(self):
        """新增參與者"""
        name = self.participant_name.get().strip()
        email = self.participant_email.get().strip()

        success, message = self.lottery.add_participant(name, email)

        if success:
            self.participant_name.set('')
            self.participant_email.set('')
            self.refresh_participant_list()
            self.update_status()
            # 更新關鍵字管理頁面的下拉選單
            self.refresh_participant_combobox()
            messagebox.showinfo("成功", message)
        else:
            messagebox.showerror("錯誤", message)

    def batch_import(self):
        """批次匯入參與者"""
        text_data = self.import_text.get('1.0', 'end').strip()

        if not text_data:
            messagebox.showwarning("警告", "請輸入要匯入的資料")
            return

        success_count, fail_count = self.lottery.batch_import_participants(text_data)

        self.import_text.delete('1.0', 'end')
        self.refresh_participant_list()
        self.update_status()
        # 更新關鍵字管理頁面的下拉選單
        self.refresh_participant_combobox()

        messagebox.showinfo("完成", f"匯入完成\n成功: {success_count} | 失敗: {fail_count}")

    def remove_participant(self):
        """刪除選中的參與者"""
        selected = self.participant_tree.selection()
        if not selected:
            messagebox.showwarning("警告", "請先選擇要刪除的參與者")
            return

        if not messagebox.askyesno("確認", "確定要刪除選中的參與者嗎?"):
            return

        for item in selected:
            values = self.participant_tree.item(item)['values']
            email = values[1]
            self.lottery.remove_participant(email)

        self.refresh_participant_list()
        self.update_status()
        # 更新關鍵字管理頁面的下拉選單
        self.refresh_participant_combobox()
        messagebox.showinfo("成功", "刪除成功")

    def refresh_participant_list(self):
        """重新整理參與者清單"""
        # 清空現有清單
        for item in self.participant_tree.get_children():
            self.participant_tree.delete(item)

        # 重新載入
        for p in self.lottery.participants:
            status = "已抽取" if self.lottery.is_drawn(p) else "未抽取"
            self.participant_tree.insert('', 'end', values=(p['name'], p['email'], status))

    # ========== 歷史記錄頁面 ==========

    def create_history_page(self):
        """建立歷史記錄頁面"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📖 歷史記錄")

        # 操作按鈕
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_frame, text="🔄 重新整理", style='Green.TButton',
                  command=self.refresh_history).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🗑️ 清空歷史", style='Red.TButton',
                  command=self.clear_history).pack(side='left', padx=5)

        # 顯示區域
        display_frame = ttk.LabelFrame(frame, text="📜 歷史記錄", padding=10)
        display_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.history_text = scrolledtext.ScrolledText(
            display_frame, height=25,
            bg=ChristmasTheme.SNOW_BG,
            fg=ChristmasTheme.TEXT_WHITE,
            font=('Courier New', 10),
            insertbackground=ChristmasTheme.TEXT_WHITE
        )
        self.history_text.pack(fill='both', expand=True)

        # 初始載入
        self.refresh_history()

    def refresh_history(self):
        """重新整理歷史記錄"""
        self.history_text.delete('1.0', 'end')

        history = self.lottery.get_history()

        if not history:
            self.history_text.insert('1.0', "暫無歷史記錄")
            return

        # 倒序顯示（最新的在前）
        for record in reversed(history):
            text = f"時間: {record['timestamp']}\n"
            text += f"抽取數量: {record['count']}\n"
            text += f"模式: {'顯示模式' if record['mode'] == 'display' else '郵件模式'}\n"
            text += f"抽中名單:\n"
            for i, p in enumerate(record['selected'], 1):
                text += f"  {i}. {p['name']} ({p['email']})\n"
            text += "-" * 60 + "\n\n"

            self.history_text.insert('end', text)

    def clear_history(self):
        """清空歷史記錄"""
        if messagebox.askyesno("確認", "確定要清空所有歷史記錄嗎?"):
            self.lottery.clear_history()
            self.refresh_history()
            messagebox.showinfo("成功", "歷史記錄已清空")

    # ========== 設定頁面 ==========

    def create_settings_page(self):
        """建立設定頁面"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ 設定")

        # SMTP 設定
        smtp_frame = ttk.LabelFrame(frame, text="📧 SMTP 郵件設定", padding=10)
        smtp_frame.pack(fill='x', padx=10, pady=10)

        # SMTP 伺服器
        server_frame = ttk.Frame(smtp_frame)
        server_frame.pack(fill='x', pady=5)
        ttk.Label(server_frame, text="SMTP伺服器:", width=15).pack(side='left')
        self.smtp_server = tk.StringVar(value=self.lottery.config.get('smtp_server', ''))
        ttk.Entry(server_frame, textvariable=self.smtp_server, width=40).pack(side='left', padx=5)

        # SMTP 連接埠
        port_frame = ttk.Frame(smtp_frame)
        port_frame.pack(fill='x', pady=5)
        ttk.Label(port_frame, text="SMTP連接埠:", width=15).pack(side='left')
        self.smtp_port = tk.IntVar(value=self.lottery.config.get('smtp_port', 587))
        ttk.Entry(port_frame, textvariable=self.smtp_port, width=40).pack(side='left', padx=5)

        # SMTP 使用者名稱
        user_frame = ttk.Frame(smtp_frame)
        user_frame.pack(fill='x', pady=5)
        ttk.Label(user_frame, text="SMTP使用者名稱:", width=15).pack(side='left')
        self.smtp_user = tk.StringVar(value=self.lottery.config.get('smtp_user', ''))
        ttk.Entry(user_frame, textvariable=self.smtp_user, width=40).pack(side='left', padx=5)

        # SMTP 密碼
        password_frame = ttk.Frame(smtp_frame)
        password_frame.pack(fill='x', pady=5)
        ttk.Label(password_frame, text="SMTP密碼:", width=15).pack(side='left')
        self.smtp_password = tk.StringVar(value=self.lottery.config.get('smtp_password', ''))
        ttk.Entry(password_frame, textvariable=self.smtp_password, width=40,
                 show='*').pack(side='left', padx=5)

        # 寄件人郵箱
        from_frame = ttk.Frame(smtp_frame)
        from_frame.pack(fill='x', pady=5)
        ttk.Label(from_frame, text="寄件人郵箱:", width=15).pack(side='left')
        self.from_email = tk.StringVar(value=self.lottery.config.get('from_email', ''))
        ttk.Entry(from_frame, textvariable=self.from_email, width=40).pack(side='left', padx=5)

        # 儲存按鈕
        ttk.Button(smtp_frame, text="儲存設定",
                  command=self.save_config).pack(pady=10)

        # 測試功能
        test_frame = ttk.LabelFrame(frame, text="測試郵件", padding=10)
        test_frame.pack(fill='x', padx=10, pady=10)

        test_input_frame = ttk.Frame(test_frame)
        test_input_frame.pack(fill='x', pady=5)
        ttk.Label(test_input_frame, text="測試郵箱:", width=15).pack(side='left')
        self.test_email = tk.StringVar()
        ttk.Entry(test_input_frame, textvariable=self.test_email, width=40).pack(side='left', padx=5)

        ttk.Button(test_frame, text="傳送測試郵件",
                  command=self.send_test_email).pack(pady=5)

        # 常用 SMTP 設定說明
        help_frame = ttk.LabelFrame(frame, text="常用 SMTP 設定參考", padding=10)
        help_frame.pack(fill='x', padx=10, pady=10)

        help_text = """Gmail: smtp.gmail.com:587 (需要應用專用密碼)
注意: 大多數郵件服務商需要在帳戶設定中開啟SMTP服務並產生專用密碼或授權碼。"""

        ttk.Label(help_frame, text=help_text, justify='left').pack(anchor='w')

    def save_config(self):
        """儲存設定"""
        config = {
            'smtp_server': self.smtp_server.get(),
            'smtp_port': self.smtp_port.get(),
            'smtp_user': self.smtp_user.get(),
            'smtp_password': self.smtp_password.get(),
            'from_email': self.from_email.get()
        }

        if self.lottery.save_config(config):
            messagebox.showinfo("成功", "設定儲存成功")
        else:
            messagebox.showerror("錯誤", "設定儲存失敗")

    def send_test_email(self):
        """傳送測試郵件"""
        test_email = self.test_email.get().strip()

        if not test_email:
            messagebox.showwarning("警告", "請輸入測試郵箱")
            return

        success, message = self.lottery.send_test_email(test_email)

        if success:
            messagebox.showinfo("成功", message)
        else:
            messagebox.showerror("錯誤", message)

    # ========== 關鍵字抽籤頁面 ==========

    def create_keyword_draw_page(self):
        """建立關鍵字抽籤頁面"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎲 關鍵字抽籤")

        # 模式選擇
        mode_frame = ttk.LabelFrame(frame, text="通知模式", padding=10)
        mode_frame.pack(fill='x', padx=10, pady=10)

        self.keyword_mode = tk.StringVar(value="display")
        ttk.Radiobutton(mode_frame, text="顯示在畫面上", variable=self.keyword_mode,
                       value="display").pack(anchor='w')
        ttk.Radiobutton(mode_frame, text="僅傳送郵件通知", variable=self.keyword_mode,
                       value="email").pack(anchor='w')
        ttk.Radiobutton(mode_frame, text="畫面顯示且傳送郵件", variable=self.keyword_mode,
                       value="both").pack(anchor='w')

        # 顯示模式選擇
        display_frame = ttk.LabelFrame(frame, text="顯示模式", padding=10)
        display_frame.pack(fill='x', padx=10, pady=10)

        self.keyword_display_mode = tk.StringVar(value="with_name")
        ttk.Radiobutton(display_frame, text="顯示人名與關鍵字", variable=self.keyword_display_mode,
                       value="with_name").pack(anchor='w')
        ttk.Radiobutton(display_frame, text="僅顯示關鍵字組合(匿名)", variable=self.keyword_display_mode,
                       value="anonymous").pack(anchor='w')

        # 抽籤設定
        settings_frame = ttk.LabelFrame(frame, text="⚙️ 抽籤設定", padding=10)
        settings_frame.pack(fill='x', padx=10, pady=10)

        # 參與人數
        count_frame = ttk.Frame(settings_frame)
        count_frame.pack(fill='x', pady=5)
        ttk.Label(count_frame, text="🎯 參與人數:").pack(side='left')
        self.keyword_participant_count = tk.IntVar(value=1)
        ttk.Spinbox(count_frame, from_=1, to=100, textvariable=self.keyword_participant_count,
                   width=10, font=('Arial', 10)).pack(side='left', padx=10)

        # 說明標籤
        info_label = ttk.Label(settings_frame,
                               text="💡 每位參與者會抽取2個來自其他參與者的關鍵字(不會抽到自己的關鍵字)",
                               foreground=ChristmasTheme.ACCENT_GOLD,
                               wraplength=550)
        info_label.pack(anchor='w', pady=5)

        # 狀態資訊
        status_frame = ttk.Frame(settings_frame)
        status_frame.pack(fill='x', pady=5)
        self.keyword_status_label = ttk.Label(status_frame, text="", font=('Arial', 10, 'bold'))
        self.keyword_status_label.pack(anchor='w')
        self.update_keyword_status()

        # 操作按鈕
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_frame, text="🎲 開始抽籤", style='Red.TButton',
                  command=self.do_keyword_draw).pack(side='left', padx=5)

        # 結果顯示區域
        result_frame = ttk.LabelFrame(frame, text="抽籤結果", padding=10)
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.keyword_result_text = scrolledtext.ScrolledText(result_frame, height=15)
        self.keyword_result_text.pack(fill='both', expand=True)

    def update_keyword_status(self):
        """更新關鍵字抽籤狀態資訊"""
        total_participants = len(self.lottery.participants)
        # 計算總關鍵字數
        total_keywords = sum(len(p['keywords']) for p in self.lottery.participants)

        self.keyword_status_label.config(
            text=f"👥 總參與者: {total_participants} | 🔤 總關鍵字數: {total_keywords}",
            foreground=ChristmasTheme.ACCENT_GOLD
        )

    def do_keyword_draw(self):
        """執行關鍵字抽籤"""
        participant_count = self.keyword_participant_count.get()
        mode = self.keyword_mode.get()
        display_mode = self.keyword_display_mode.get()

        # 執行抽籤(新版本不需要 avoid_repeat 參數,總是避免重複和自己)
        success, result_dict, message = self.lottery.draw_keywords(participant_count)

        if not success:
            messagebox.showerror("❌ 錯誤", message)
            return

        # 記錄時間
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 顯示模式
        if mode in ["display", "both"]:
            result = f"\n{'='*50}\n"
            result += f"抽籤時間: {timestamp}\n"
            result += f"參與人數: {participant_count}\n"
            result += f"抽籤結果:\n"

            if display_mode == "with_name":
                # 顯示人名與關鍵字
                for i, (email, data) in enumerate(result_dict.items(), 1):
                    result += f"  {i}. {data['name']} ({data['email']})\n"
                    result += f"     關鍵字: {data['keywords'][0]}, {data['keywords'][1]}\n"
            else:
                # 僅顯示關鍵字組合(匿名)
                for i, (email, data) in enumerate(result_dict.items(), 1):
                    result += f"  {i}. 關鍵字組合: {data['keywords'][0]}, {data['keywords'][1]}\n"

            result += f"{'='*50}\n"
            self.keyword_result_text.insert('1.0', result)

        # 郵件模式
        if mode in ["email", "both"]:
            success_count = 0
            fail_count = 0

            for email, data in result_dict.items():
                success, msg = self.lottery.send_keyword_email(
                    data['email'], data['name'], data['keywords'], timestamp
                )
                if success:
                    success_count += 1
                else:
                    fail_count += 1

            result_msg = f"郵件傳送完成\n成功: {success_count} | 失敗: {fail_count}"

            if mode == "email":
                # 僅郵件模式才顯示完成訊息
                if fail_count > 0:
                    messagebox.showwarning("部分失敗", result_msg)
                else:
                    messagebox.showinfo("成功", result_msg)

        # 顯示成功訊息(非僅郵件模式)
        if mode == "display":
            messagebox.showinfo("🎉 成功", "抽籤完成!")
        elif mode == "both":
            messagebox.showinfo("🎉 成功", f"抽籤完成!\n郵件傳送: 成功 {success_count} | 失敗 {fail_count}")

        # 儲存歷史記錄
        self.lottery.save_keyword_history(result_dict, participant_count, mode, display_mode)

        # 更新狀態
        self.update_keyword_status()

    # ========== 關鍵字管理頁面 ==========

    def create_keyword_manage_page(self):
        """建立關鍵字管理頁面 - 以參與者為中心"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔤 關鍵字管理")

        # 參與者選擇區域
        select_frame = ttk.LabelFrame(frame, text="👤 選擇參與者", padding=10)
        select_frame.pack(fill='x', padx=10, pady=10)

        # 參與者下拉選單
        participant_frame = ttk.Frame(select_frame)
        participant_frame.pack(fill='x', pady=5)
        ttk.Label(participant_frame, text="參與者:", width=10).pack(side='left')

        self.selected_participant_email = tk.StringVar()
        self.participant_combobox = ttk.Combobox(participant_frame,
                                                 textvariable=self.selected_participant_email,
                                                 state='readonly',
                                                 width=40,
                                                 font=('Arial', 10))
        self.participant_combobox.pack(side='left', padx=5)
        self.participant_combobox.bind('<<ComboboxSelected>>', self.on_participant_selected)

        # 新增關鍵字區域
        add_frame = ttk.LabelFrame(frame, text="➕ 為選中參與者新增關鍵字", padding=10)
        add_frame.pack(fill='x', padx=10, pady=10)

        # 關鍵字輸入
        keyword_frame = ttk.Frame(add_frame)
        keyword_frame.pack(fill='x', pady=5)
        ttk.Label(keyword_frame, text="🔤 關鍵字:", width=10).pack(side='left')
        self.new_keyword = tk.StringVar()
        ttk.Entry(keyword_frame, textvariable=self.new_keyword, width=40, font=('Arial', 10)).pack(side='left', padx=5)

        # 新增按鈕
        ttk.Button(add_frame, text="➕ 新增", style='Green.TButton',
                  command=self.add_keyword_to_participant).pack(pady=5)

        # 批次匯入區域
        import_frame = ttk.LabelFrame(frame, text="📋 批次匯入關鍵字（每行一個）", padding=10)
        import_frame.pack(fill='x', padx=10, pady=10)

        self.keyword_import_text = scrolledtext.ScrolledText(
            import_frame, height=5,
            bg=ChristmasTheme.SNOW_BG,
            fg=ChristmasTheme.TEXT_WHITE,
            font=('Courier New', 10),
            insertbackground=ChristmasTheme.TEXT_WHITE
        )
        self.keyword_import_text.pack(fill='x', pady=5)

        ttk.Button(import_frame, text="📥 批次匯入", style='Gold.TButton',
                  command=self.batch_import_keywords_for_participant).pack(pady=5)

        # 關鍵字清單
        list_frame = ttk.LabelFrame(frame, text="📜 該參與者的關鍵字清單", padding=10)
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # 建立表格
        columns = ('keyword',)
        self.keyword_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        self.keyword_tree.heading('keyword', text='🔤 關鍵字')

        self.keyword_tree.column('keyword', width=400)

        # 捲軸
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical',
                                 command=self.keyword_tree.yview)
        self.keyword_tree.configure(yscrollcommand=scrollbar.set)

        self.keyword_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # 操作按鈕
        button_frame = ttk.Frame(list_frame)
        button_frame.pack(fill='x', pady=5)

        ttk.Button(button_frame, text="🗑️ 刪除選中", style='Red.TButton',
                  command=self.remove_keyword_from_participant).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🔄 重新整理清單", style='Green.TButton',
                  command=self.refresh_keyword_list).pack(side='left', padx=5)

        # 初始載入
        self.refresh_participant_combobox()
        self.refresh_keyword_list()

    def refresh_participant_combobox(self):
        """更新參與者下拉選單"""
        participants = self.lottery.participants
        if participants:
            values = [f"{p['name']} ({p['email']})" for p in participants]
            self.participant_combobox['values'] = values

            # 檢查當前選中的參與者是否還存在
            current_email = self.selected_participant_email.get()
            participant_exists = any(p['email'] == current_email for p in participants)

            if not current_email or not participant_exists:
                # 如果沒有選中或選中的參與者已被刪除,選擇第一個
                self.participant_combobox.current(0)
                self.selected_participant_email.set(participants[0]['email'])
                self.refresh_keyword_list()
        else:
            self.participant_combobox['values'] = []
            self.selected_participant_email.set('')

    def on_participant_selected(self, event=None):
        """當選擇參與者時觸發"""
        selection = self.participant_combobox.get()
        if selection:
            # 從 "姓名 (email)" 格式中提取 email
            import re
            match = re.search(r'\((.+?)\)', selection)
            if match:
                email = match.group(1)
                self.selected_participant_email.set(email)
                self.refresh_keyword_list()

    def add_keyword_to_participant(self):
        """為選中的參與者新增關鍵字"""
        email = self.selected_participant_email.get()
        if not email:
            messagebox.showwarning("⚠️ 警告", "請先選擇一個參與者")
            return

        keyword = self.new_keyword.get().strip()
        success, message = self.lottery.add_keyword_to_participant(email, keyword)

        if success:
            self.new_keyword.set('')
            self.refresh_keyword_list()
            self.update_keyword_status()
            messagebox.showinfo("✅ 成功", message)
        else:
            messagebox.showerror("❌ 錯誤", message)

    def batch_import_keywords_for_participant(self):
        """為選中的參與者批次匯入關鍵字"""
        email = self.selected_participant_email.get()
        if not email:
            messagebox.showwarning("⚠️ 警告", "請先選擇一個參與者")
            return

        text_data = self.keyword_import_text.get('1.0', 'end').strip()

        if not text_data:
            messagebox.showwarning("⚠️ 警告", "請輸入要匯入的關鍵字")
            return

        success_count, fail_count = self.lottery.batch_import_keywords_for_participant(email, text_data)

        self.keyword_import_text.delete('1.0', 'end')
        self.refresh_keyword_list()
        self.update_keyword_status()

        messagebox.showinfo("✅ 完成", f"匯入完成\n✅ 成功: {success_count} | ❌ 失敗: {fail_count}")

    def remove_keyword_from_participant(self):
        """從選中的參與者移除關鍵字"""
        email = self.selected_participant_email.get()
        if not email:
            messagebox.showwarning("⚠️ 警告", "請先選擇一個參與者")
            return

        selected = self.keyword_tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ 警告", "請先選擇要刪除的關鍵字")
            return

        if not messagebox.askyesno("🔄 確認", "確定要刪除選中的關鍵字嗎?"):
            return

        for item in selected:
            values = self.keyword_tree.item(item)['values']
            keyword = values[0]
            self.lottery.remove_keyword_from_participant(email, keyword)

        self.refresh_keyword_list()
        self.update_keyword_status()
        messagebox.showinfo("✅ 成功", "刪除成功")

    def refresh_keyword_list(self):
        """重新整理關鍵字清單"""
        # 清空現有清單
        for item in self.keyword_tree.get_children():
            self.keyword_tree.delete(item)

        # 重新載入選中參與者的關鍵字
        email = self.selected_participant_email.get()
        if email:
            participant = self.lottery.get_participant_by_email(email)
            if participant and 'keywords' in participant:
                for keyword in participant['keywords']:
                    self.keyword_tree.insert('', 'end', values=(keyword,))

    # ========== 關鍵字抽籤歷史頁面 ==========

    def create_keyword_history_page(self):
        """建立關鍵字抽籤歷史記錄頁面"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 關鍵字歷史")

        # 操作按鈕
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_frame, text="重新整理",
                  command=self.refresh_keyword_history).pack(side='left', padx=5)
        ttk.Button(button_frame, text="清空歷史",
                  command=self.clear_keyword_history).pack(side='left', padx=5)

        # 顯示區域
        display_frame = ttk.LabelFrame(frame, text="關鍵字抽籤歷史記錄", padding=10)
        display_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.keyword_history_text = scrolledtext.ScrolledText(display_frame, height=25)
        self.keyword_history_text.pack(fill='both', expand=True)

        # 初始載入
        self.refresh_keyword_history()

    def refresh_keyword_history(self):
        """重新整理關鍵字抽籤歷史記錄"""
        self.keyword_history_text.delete('1.0', 'end')

        history = self.lottery.get_keyword_history()

        if not history:
            self.keyword_history_text.insert('1.0', "暫無關鍵字抽籤歷史記錄")
            return

        # 倒序顯示(最新的在前)
        for record in reversed(history):
            text = f"時間: {record['timestamp']}\n"
            text += f"參與人數: {record['participant_count']}\n"

            mode_text = {
                'display': '顯示模式',
                'email': '郵件模式',
                'both': '顯示+郵件模式'
            }.get(record['mode'], record['mode'])
            text += f"通知模式: {mode_text}\n"

            display_mode_text = {
                'with_name': '顯示人名',
                'anonymous': '匿名'
            }.get(record['display_mode'], record['display_mode'])
            text += f"顯示模式: {display_mode_text}\n"
            text += f"抽籤結果:\n"

            for i, (email, data) in enumerate(record['results'].items(), 1):
                if record['display_mode'] == 'with_name':
                    text += f"  {i}. {data['name']} ({data['email']})\n"
                    text += f"     關鍵字: {data['keywords'][0]}, {data['keywords'][1]}\n"
                else:
                    text += f"  {i}. 關鍵字組合: {data['keywords'][0]}, {data['keywords'][1]}\n"

            text += "-" * 60 + "\n\n"

            self.keyword_history_text.insert('end', text)

    def clear_keyword_history(self):
        """清空關鍵字抽籤歷史記錄"""
        if messagebox.askyesno("確認", "確定要清空所有關鍵字抽籤歷史記錄嗎?"):
            self.lottery.clear_keyword_history()
            self.refresh_keyword_history()
            messagebox.showinfo("成功", "關鍵字抽籤歷史記錄已清空")

    # ========== 設定頁面 ==========


def main():
    """主函数"""
    root = tk.Tk()
    app = LotteryGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
