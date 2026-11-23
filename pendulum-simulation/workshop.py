"""A parchment-and-brass pendulum workshop, using only the Python standard library.

Run this file directly. The sibling core.py is an independent snapshot of the
original lab; the original application outside this folder is never modified.
"""
import math
import tkinter as tk
import tkinter.font as tkfont
from functools import partial
from tkinter import ttk

from core import Lab
from user_guide import GUIDE_UI, GUIDE_SECTIONS, localized as guide_localized


PAPER = '#F3E7CF'
SHEET = '#FFF8E8'
EDGE = '#CFB88C'
INK = '#352B24'
MUTED = '#76634E'
WINE = '#843E3B'
GOLD = '#B48A49'
GREEN = '#49634D'

# Only the workshop's additional wording lives here; inherited text uses the
# independent translations.json next to this file.
WORDS = {
    '单摆实验室': ('学者工坊', '學者工坊', "Scholar's Workshop"),
    '单摆实验室 · Python Physics Lab': ('学者工坊 · Python', '學者工坊 · Python', "Scholar's Workshop · Python"),
    '单摆实验': ('实验工坊', '實驗工坊', 'The workshop'),
    '递进任务清单': ('探究卷册', '探究卷冊', 'Inquiry folios'),
    '实验参数': ('实验设定', '實驗設定', 'Experiment settings'),
    '递进探究任务': ('探究卷册', '探究卷冊', 'Inquiry folios'),
    '1. 找规律': ('卷一 · 寻找规律', '卷一 · 尋找規律', 'I · Find patterns'),
    '2. 检验猜想': ('卷二 · 检验猜想', '卷二 · 檢驗猜想', 'II · Test a prediction'),
    '3. 评价模型': ('卷三 · 审视模型', '卷三 · 審視模型', 'III · Evaluate the model'),
    '4. 地球与月球': ('卷四 · 两地之摆', '卷四 · 兩地之擺', 'IV · Earth and Moon'),
    '自然哲学 · 交互实验手稿': ('自然哲学 · 交互实验手稿', '自然哲學 · 互動實驗手稿', 'NATURAL PHILOSOPHY · AN INTERACTIVE NOTEBOOK'),
    '运动观察': ('运动观察', '運動觀察', 'Motion study'),
    '实验手稿': ('实验手稿', '實驗手稿', 'Experiment notebook'),
    '观测曲线': ('观测曲线', '觀測曲線', 'Observation trace'),
    '模型札记': ('模型札记', '模型札記', 'Model notes'),
    '无阻力 · 定长绳 · 质点模型': ('无阻力 · 定长绳 · 质点模型', '無阻力 · 定長繩 · 質點模型', 'No drag · fixed string · point mass'),
    '记录后，前往卷册写下你的发现。': ('记录后，前往卷册写下你的发现。', '記錄後，前往卷冊寫下你的發現。', 'Record an experiment, then write your findings in the folios.'),
    '选择一卷，开始探究。': ('选择一卷，开始探究。', '選擇一卷，開始探究。', 'Choose a folio to begin.'),
    '完成': ('完成', '完成', 'DONE'),
    '当前卷页': ('当前卷页', '當前卷頁', 'Selected folio'),
    '待记录': ('待记录', '待記錄', 'Not recorded'),
    '数据齐全 · 请写结论': ('数据齐全 · 请写结论', '資料齊全 · 請寫結論', 'Data ready · write a conclusion'),
    '先预测，再动手': ('先预测，再动手', '先預測，再動手', 'Predict before you experiment'),
}
WORDS.update(GUIDE_UI)


class BrassSlider(tk.Canvas):
    """A keyboard-operable, vector-drawn slider with a circular brass thumb."""

    def __init__(self, parent, variable, low, high, command, begin, end):
        super().__init__(parent, height=32, bg=SHEET, highlightthickness=0,
                         takefocus=True, cursor='hand2')
        self.variable, self.low, self.high = variable, low, high
        self.command, self.begin, self.end = command, begin, end
        self.trace = variable.trace_add('write', lambda *_: self.draw())
        self.bind('<Configure>', lambda _: self.draw())
        self.bind('<FocusIn>', lambda _: self.draw())
        self.bind('<FocusOut>', lambda _: self.draw())
        self.bind('<ButtonPress-1>', self.press)
        self.bind('<B1-Motion>', self.move)
        self.bind('<ButtonRelease-1>', self.release)
        for key, direction in [('Left', -1), ('Down', -1), ('Right', 1), ('Up', 1)]:
            self.bind(f'<{key}>', partial(self.key, direction))
        self.bind('<Home>', lambda event: self.key_value(self.low))
        self.bind('<End>', lambda event: self.key_value(self.high))

    def draw(self):
        self.delete('all')
        width = max(40, self.winfo_width())
        fraction = (self.variable.get()-self.low)/(self.high-self.low)
        x = 13 + max(0, min(1, fraction))*(width-26)
        self.create_line(13, 16, width-13, 16, fill=EDGE, width=4)
        self.create_line(13, 16, x, 16, fill=GOLD, width=4)
        for i in range(5):
            tick = 13+(width-26)*i/4
            self.create_line(tick, 23, tick, 26, fill=EDGE)
        if self.focus_get() == self:
            self.create_oval(x-12, 4, x+12, 28, outline=WINE, dash=(2, 2))
        self.create_oval(x-8, 8, x+8, 24, fill=GOLD, outline='#76572D', width=1)
        self.create_oval(x-5, 10, x+3, 17, fill='#E6CB8E', outline='')

    def set_from_x(self, x):
        fraction = max(0, min(1, (x-13)/max(1, self.winfo_width()-26)))
        self.variable.set(round(self.low+fraction*(self.high-self.low), 4))
        self.command()

    def press(self, event):
        self.focus_set()
        self.begin(event)
        self.set_from_x(event.x)

    def move(self, event):
        self.set_from_x(event.x)

    def release(self, event):
        self.end(event)

    def key(self, direction, event):
        return self.key_value(self.variable.get()+direction*(self.high-self.low)/100)

    def key_value(self, value):
        self.begin(None)
        self.variable.set(max(self.low, min(self.high, value)))
        self.command()
        self.end(None)
        return 'break'

    def destroy(self):
        self.variable.trace_remove('write', self.trace)
        super().destroy()


class FolioCard(tk.Canvas):
    """One selectable folio with progress and a completion seal."""

    def __init__(self, parent, lab, index):
        super().__init__(parent, height=117, width=244, bg=PAPER,
                         highlightthickness=0, cursor='hand2', takefocus=True)
        self.lab, self.index = lab, index
        self.bind('<Configure>', lambda _: self.draw())
        self.bind('<Button-1>', self.choose)
        self.bind('<Return>', self.choose)
        self.bind('<space>', self.choose)
        self.bind('<FocusIn>', lambda _: self.draw())
        self.bind('<FocusOut>', lambda _: self.draw())

    def choose(self, event=None):
        self.focus_set()
        self.lab.task_list.selection_set(str(self.index))

    def draw(self):
        self.delete('all')
        lab, i = self.lab, self.index
        width = max(180, self.winfo_width())
        selected = lab.active_task == i
        border = WINE if selected or self.focus_get() == self else EDGE
        self.create_rectangle(4, 5, width-3, 114, fill='#DED0B3', outline='')
        self.create_polygon(1, 1, width-20, 1, width-7, 14, width-7, 109, 1, 109,
                            fill=SHEET if selected else '#F8EEDB', outline=border, width=2 if selected else 1)
        self.create_polygon(width-20, 1, width-20, 14, width-7, 14, fill='#E6D3AC', outline=EDGE)
        self.create_rectangle(2, 2, 6, 108, fill=WINE if selected else GOLD, outline='')
        self.create_text(18, 22, anchor='w', text=lab.tr(lab.TASKS[i][0]),
                         fill=INK, font=(lab.ui_font, 11, 'bold'))
        count, total = len(lab.task_records[i]), len(lab.TASKS[i][1])
        state = lab.tr('✓ 已完成') if lab.task_done[i] else lab.tr('数据齐全 · 请写结论') if count == total else lab.tr('待完成')
        self.create_text(18, 48, anchor='w', text=state, fill=GREEN if lab.task_done[i] else MUTED,
                         font=(lab.ui_font, 9))
        self.create_text(18, 78, anchor='w', text=f'{count:02d} / {total:02d}',
                         fill=WINE, font=('Georgia', 13))
        self.create_line(93, 79, width-23, 79, fill=EDGE, width=4)
        if count:
            self.create_line(93, 79, 93+(width-116)*count/total, 79, fill=GREEN, width=4)
        if lab.task_done[i]:
            self.create_oval(width-64, 45, width-17, 92, fill=SHEET, outline=GREEN, width=2)
            self.create_oval(width-60, 49, width-21, 88, outline=GREEN)
            self.create_text(width-40, 68, text=lab.tr('完成'), fill=GREEN,
                             font=(lab.ui_font, 8, 'bold'), angle=12)


class Workshop(Lab):
    BG, INK, BLUE = PAPER, INK, WINE

    def __init__(self, root):
        available = set(tkfont.families(root))
        self.ui_font = next((font for font in ('Microsoft JhengHei UI', 'Microsoft YaHei UI','Noto Sans CJK SC') if font in available), 'TkDefaultFont')
        self.folio_cards = []
        self.stage_key = None
        super().__init__(root)
        # Card selection intentionally drives the inherited task controller.
        self.task_list.selection_remove(self.task_list.selection())
        self.active_task = None
        self.refresh_tasks()
        self.status.set(self.tr('先预测，再拖动滑块。点击“开始”释放单摆。'))

    def tr(self, text):
        entry = WORDS.get(text)
        if entry is None:
            # Static widgets are captured in their initial Chinese presentation.
            entry = next((value for value in WORDS.values() if value[0] == text), None)
        if entry is not None:
            return entry[{'zh-CN': 0, 'zh-TW': 1, 'en': 2}[self.language]]
        return super().tr(text)

    def setup_style(self):
        style = ttk.Style(self.root)
        style.configure('.', font=(self.ui_font, 10), background=PAPER, foreground=INK)
        style.configure('TFrame', background=PAPER)
        style.configure('Sheet.TFrame', background=SHEET)
        style.configure('TLabel', background=PAPER, foreground=INK)
        style.configure('Sheet.TLabel', background=SHEET, foreground=INK)
        style.configure('Muted.TLabel', background=PAPER, foreground=MUTED, font=(self.ui_font, 9))
        style.configure('Note.TLabel', background=SHEET, foreground=MUTED, font=(self.ui_font, 9))
        style.configure('Title.TLabel', font=(self.ui_font, 22, 'bold'), foreground=WINE)
        style.configure('Section.TLabel', background=SHEET, foreground=WINE, font=(self.ui_font, 12, 'bold'))
        style.configure('TButton', background='#EFE0C1', foreground=INK, bordercolor=EDGE,
                        lightcolor=SHEET, darkcolor=EDGE, padding=(10, 7), relief='flat')
        style.map('TButton', background=[('pressed', '#D8BF93'), ('active', '#E6D1AC')],
                  foreground=[('disabled', '#9B8970')])
        style.configure('Primary.TButton', background=WINE, foreground=SHEET, bordercolor=WINE,
                        lightcolor=WINE, darkcolor=WINE, font=(self.ui_font, 10, 'bold'))
        style.map('Primary.TButton', background=[('pressed', '#612D2B'), ('active', '#9B504A')],
                  foreground=[('disabled', '#D9C4B9')])
        style.configure('Bookmark.TButton', padding=(12, 9), background='#EAD5B0')
        style.map('Bookmark.TButton', background=[('disabled', WINE), ('active', '#DEC395')],
                  foreground=[('disabled', SHEET)])
        style.configure('TNotebook', background=PAPER, borderwidth=0, tabmargins=(0, 5, 0, 0))
        style.configure('TNotebook.Tab', background='#E8D5B1', foreground=MUTED, padding=(22, 9),
                        bordercolor=EDGE, lightcolor=SHEET)
        style.map('TNotebook.Tab', background=[('selected', SHEET)], foreground=[('selected', WINE)])
        style.configure('TEntry', fieldbackground=SHEET, foreground=INK, bordercolor=EDGE,
                        lightcolor=EDGE, darkcolor=EDGE, padding=7)
        style.map('TEntry', fieldbackground=[('readonly', '#EEE0C4')])
        style.configure('TCombobox', fieldbackground=SHEET, background='#EAD5B0', foreground=INK,
                        bordercolor=EDGE, arrowcolor=WINE, padding=5)
        style.map('TCombobox', fieldbackground=[('readonly', SHEET)], foreground=[('readonly', INK)])
        style.configure('Treeview', background=SHEET, fieldbackground=SHEET, foreground=INK,
                        bordercolor=EDGE, rowheight=26, font=(self.ui_font, 9))
        style.configure('Treeview.Heading', background='#EBD9B7', foreground=INK,
                        bordercolor=EDGE, font=(self.ui_font, 9, 'bold'), padding=(4, 5))
        style.map('Treeview', background=[('selected', '#E3C996')], foreground=[('selected', INK)])
        style.configure('TScrollbar', background='#DEC69D', troughcolor=PAPER, arrowcolor=MUTED)
        self.root.option_add('*TCombobox*Listbox.background', SHEET)
        self.root.option_add('*TCombobox*Listbox.foreground', INK)

    def label(self, parent, text, style='Sheet.TLabel', **options):
        return ttk.Label(parent, text=self.tr(text), style=style, **options)

    def build(self):
        self.setup_style()
        screen_w, screen_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        width, height = min(1280, screen_w-70), min(900, screen_h-90)
        self.root.geometry(f'{width}x{height}')
        self.root.minsize(min(1060, width), min(760, height))
        header = ttk.Frame(self.root, padding=(24, 16, 24, 10))
        header.pack(fill='x')
        emblem = tk.Canvas(header, width=62, height=64, bg=PAPER, highlightthickness=0)
        emblem.pack(side='left', padx=(0, 14))
        emblem.create_oval(5, 6, 57, 58, outline=GOLD, width=2)
        emblem.create_oval(9, 10, 53, 54, outline=EDGE)
        emblem.create_line(31, 15, 42, 43, fill=INK, width=2)
        emblem.create_line(31, 15, 31, 49, fill=GOLD, dash=(2, 3))
        emblem.create_oval(36, 37, 48, 49, fill=GOLD, outline='#76572D')
        emblem.create_line(22, 15, 40, 15, fill=WINE, width=3)
        title = ttk.Frame(header)
        title.pack(side='left', fill='x', expand=True)
        self.label(title, '自然哲学 · 交互实验手稿', 'Muted.TLabel').pack(anchor='w')
        self.label(title, '单摆实验室', 'Title.TLabel').pack(anchor='w', pady=(2, 0))
        self.language_buttons = {}
        for code, text in [('zh-CN', '简中'), ('zh-TW', '繁中'), ('en', 'English')]:
            button = ttk.Button(header, text=text, style='Bookmark.TButton', command=partial(self.switch_language, code))
            button.pack(side='left', padx=3)
            self.language_buttons[code] = button
        self.language_buttons['zh-CN'].state(['disabled'])
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=22)
        self.lab_tab = ttk.Frame(self.notebook, style='Sheet.TFrame', padding=12)
        self.task_tab = ttk.Frame(self.notebook, style='Sheet.TFrame', padding=12)
        self.notebook.add(self.lab_tab, text=self.tr('单摆实验'))
        self.notebook.add(self.task_tab, text=self.tr('递进任务清单'))
        self.lab_tab.columnconfigure(1, weight=1)
        self.lab_tab.rowconfigure(0, weight=1)
        controls = ttk.Frame(self.lab_tab, style='Sheet.TFrame', width=250)
        controls.grid(row=0, column=0, sticky='nsew', padx=(0, 14))
        controls.grid_propagate(False)
        controls.columnconfigure(0, weight=1)
        self.label(controls, '实验参数', 'Section.TLabel').grid(row=0, sticky='w', pady=(5, 9))
        self.value_labels, self.sliders = [], []
        row = 1
        for name, variable, low, high, unit in [('摆长', self.length, .2, 2, 'm'),
                                               ('初始角度', self.angle, 5, 60, '°'),
                                               ('重力加速度', self.gravity, 1.6, 20, 'm/s²')]:
            label = ttk.Label(controls, style='Sheet.TLabel')
            label.grid(row=row, sticky='w', pady=(8, 0))
            self.value_labels.append((label, name, variable, unit))
            slider = BrassSlider(controls, variable, low, high, self.parameters_changed,
                                 self.begin_drag, self.end_drag)
            slider.grid(row=row+1, sticky='ew', pady=(0, 3))
            self.sliders.append(slider)
            row += 2
        planets = ttk.Frame(controls, style='Sheet.TFrame')
        planets.grid(row=row, sticky='ew', pady=(6, 12))
        for text, g in [('地球', 9.81), ('月球', 1.62)]:
            ttk.Button(planets, text=self.tr(text), command=partial(self.set_gravity, g)).pack(side='left', expand=True, fill='x', padx=2)
        row += 1
        self.play = ttk.Button(controls, text=self.tr('▶ 开始'), style='Primary.TButton', command=self.toggle)
        self.play.grid(row=row, sticky='ew', pady=3)
        row += 1
        actions = ttk.Frame(controls, style='Sheet.TFrame')
        actions.grid(row=row, sticky='ew', pady=3)
        ttk.Button(actions, text=self.tr('重置本次实验'), command=self.reset).pack(fill='x')
        ttk.Button(actions, text=self.tr('单步前进 0.02 s'), command=self.single_step).pack(fill='x', pady=(5, 0))
        row += 1
        self.label(controls, '播放速度（不改变物理周期）', 'Note.TLabel', wraplength=240).grid(row=row, sticky='w', pady=(12, 5))
        row += 1
        ttk.Combobox(controls, textvariable=self.speed, values=['0.25×', '0.5×', '1×', '2×'], state='readonly', width=12).grid(row=row, sticky='w')
        row += 1
        ttk.Button(controls, text=self.tr('恢复默认参数'), command=self.defaults).grid(row=row, sticky='ew', pady=(12, 8))
        row += 1
        self.label(controls, '模型札记', 'Section.TLabel').grid(row=row, sticky='w', pady=(8, 4))
        row += 1
        self.label(controls, '无阻力 · 定长绳 · 质点模型', 'Note.TLabel', wraplength=238).grid(row=row, sticky='w')
        row += 1
        self.label(controls, '记录后，前往卷册写下你的发现。', 'Note.TLabel', wraplength=238).grid(row=row, sticky='w', pady=8)
        right = ttk.Frame(self.lab_tab, style='Sheet.TFrame')
        right.grid(row=0, column=1, sticky='nsew')
        right.columnconfigure(0, weight=1)
        right.rowconfigure(0, weight=3, minsize=220)
        right.rowconfigure(2, weight=1, minsize=150)
        self.canvas = tk.Canvas(right, bg=SHEET, highlightthickness=0, height=270)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.metrics_label = ttk.Label(right, textvariable=self.metrics, style='Sheet.TLabel', font=(self.ui_font, 10), padding=(8, 6))
        self.metrics_label.grid(row=1, column=0, sticky='ew')
        self.chart = tk.Canvas(right, bg=SHEET, highlightthickness=0, height=160)
        self.chart.grid(row=2, column=0, sticky='nsew', pady=(0, 7))
        self.label(right, '实验手稿', 'Section.TLabel').grid(row=3, column=0, sticky='w', pady=(2, 5))
        record_frame = ttk.Frame(right, style='Sheet.TFrame')
        record_frame.grid(row=4, column=0, sticky='ew')
        record_frame.columnconfigure(0, weight=1)
        columns = ('n', 'length', 'angle', 'gravity', 'measured', 'theory', 'difference')
        self.table = ttk.Treeview(record_frame, columns=columns, show='headings', height=3)
        self.table.grid(row=0, column=0, sticky='ew')
        for column, title, column_width in zip(columns,
                ['序号', '摆长 / m', '初始角 / °', 'g / m/s²', '模拟周期 / s', '小角度公式 / s', '偏差 / %'],
                [42, 83, 98, 86, 125, 130, 105]):
            self.table.heading(column, text=self.tr(title))
            self.table.column(column, width=column_width, minwidth=35, anchor='center')
        scroll = ttk.Scrollbar(record_frame, orient='vertical', command=self.table.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        self.table.configure(yscrollcommand=scroll.set)
        self.table.tag_configure('alternate', background='#F4E9D2')
        bar = ttk.Frame(right, style='Sheet.TFrame')
        bar.grid(row=5, column=0, sticky='ew', pady=(8, 0))
        ttk.Button(bar, text=self.tr('记录本次实验'), style='Primary.TButton', command=self.record).pack(side='left')
        ttk.Button(bar, text=self.tr('导出 CSV'), command=self.export).pack(side='left', padx=7)
        ttk.Button(bar, text=self.tr('清空记录'), command=self.clear_records).pack(side='right')
        self.build_tasks()
        self.build_guide()
        footer = ttk.Frame(self.root, padding=(24, 9))
        footer.pack(fill='x')
        self.status_label = ttk.Label(footer, textvariable=self.status, style='Muted.TLabel', wraplength=width-70)
        self.status_label.pack(anchor='w')
        self.root.bind('<Configure>', self.resize_text, add='+')
        self.update_labels()

    def resize_text(self, event):
        if event.widget == self.root:
            self.status_label.configure(wraplength=max(600, event.width-70))

    def build_guide(self):
        self.guide_tab = ttk.Frame(self.notebook, style='Sheet.TFrame', padding=16)
        self.notebook.add(self.guide_tab, text=self.tr('如何使用'))
        self.guide_tab.columnconfigure(1, weight=1)
        self.guide_tab.rowconfigure(0, weight=1)
        rail = ttk.Frame(self.guide_tab, padding=(12, 14, 18, 12))
        rail.grid(row=0, column=0, sticky='ns')
        self.label(rail, '使用指引', 'Title.TLabel').pack(anchor='w', pady=(0, 12))
        self.label(rail, '选择章节查看说明；也可以随时按 F1 打开指引。',
                   'Muted.TLabel', wraplength=218, justify='left').pack(anchor='w', pady=(0, 16))
        self.guide_index = 0
        self.guide_nav = tk.Listbox(rail, width=23, height=len(GUIDE_SECTIONS),
                                  bg=SHEET, fg=INK, selectbackground=WINE,
                                  selectforeground=SHEET, activestyle='none',
                                  highlightthickness=1, highlightbackground=EDGE,
                                  highlightcolor=GOLD, relief='flat', borderwidth=0,
                                  exportselection=False, font=(self.ui_font, 11))
        self.guide_nav.pack(fill='x', ipady=8)
        self.guide_nav.bind('<<ListboxSelect>>', self.choose_guide_section)
        self.label(rail, '查阅指引会保留当前实验；若要停住运动，请先点击“暂停”。',
                   'Muted.TLabel', wraplength=218, justify='left').pack(anchor='w', pady=(20, 0))
        content = ttk.Frame(self.guide_tab, style='Sheet.TFrame')
        content.grid(row=0, column=1, sticky='nsew', padx=(8, 0))
        content.columnconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)
        self.label(content, '如何使用这个项目', 'Section.TLabel',
                   font=(self.ui_font, 18, 'bold')).grid(row=0, column=0, sticky='w', pady=(2, 14))
        text_frame = ttk.Frame(content, style='Sheet.TFrame')
        text_frame.grid(row=1, column=0, sticky='nsew')
        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)
        self.guide_body = tk.Text(text_frame, wrap='word', width=55, height=20,
                                  bg=SHEET, fg=INK, insertbackground=INK,
                                  relief='flat', borderwidth=0, highlightthickness=1,
                                  highlightbackground=EDGE, highlightcolor=GOLD,
                                  padx=22, pady=18, font=(self.ui_font, 11),
                                  spacing1=2, spacing3=7, selectbackground='#E3C996')
        self.guide_body.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(text_frame, orient='vertical', command=self.guide_body.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.guide_body.configure(yscrollcommand=scrollbar.set)
        self.guide_body.tag_configure('chapter', foreground=WINE,
                                      font=(self.ui_font, 17, 'bold'), spacing3=18)
        self.guide_body.tag_configure('heading', foreground=WINE,
                                      font=(self.ui_font, 12, 'bold'), spacing1=6, spacing3=6)
        actions = ttk.Frame(content, style='Sheet.TFrame')
        actions.grid(row=2, column=0, sticky='ew', pady=(12, 0))
        self.guide_actions = []
        for title, tab in [('前往实验工坊', self.lab_tab), ('前往探究卷册', self.task_tab)]:
            button = ttk.Button(actions, text=self.tr(title), command=partial(self.notebook.select, tab))
            button.pack(side='left', padx=(0, 8))
            self.guide_actions.append(button)
        self.root.bind('<F1>', self.show_guide)
        self.refresh_guide()

    def show_guide(self, event=None):
        self.notebook.select(self.guide_tab)
        return 'break'

    def choose_guide_section(self, event=None):
        selected = self.guide_nav.curselection()
        if selected and selected[0] != self.guide_index:
            self.guide_index = selected[0]
            self.render_guide()

    def refresh_guide(self):
        position = self.guide_body.yview()[0]
        self.guide_nav.delete(0, 'end')
        for title, _ in GUIDE_SECTIONS:
            self.guide_nav.insert('end', guide_localized(title, self.language))
        self.guide_nav.selection_set(self.guide_index)
        self.guide_nav.activate(self.guide_index)
        self.notebook.tab(self.guide_tab, text=self.tr('如何使用'))
        self.render_guide()
        self.guide_body.yview_moveto(position)

    def render_guide(self):
        title, blocks = GUIDE_SECTIONS[self.guide_index]
        self.guide_body.configure(state='normal')
        self.guide_body.delete('1.0', 'end')
        self.guide_body.insert('end', guide_localized(title, self.language)+'\n', 'chapter')
        for heading, body in blocks:
            self.guide_body.insert('end', guide_localized(heading, self.language)+'\n', 'heading')
            self.guide_body.insert('end', guide_localized(body, self.language)+'\n\n')
        self.guide_body.configure(state='disabled')
        self.guide_body.yview_moveto(0)

    def build_tasks(self):
        self.task_tab.columnconfigure(1, weight=1)
        self.task_tab.rowconfigure(0, weight=1)
        rail = ttk.Frame(self.task_tab, padding=(0, 8, 14, 0))
        rail.grid(row=0, column=0, sticky='ns')
        self.label(rail, '递进探究任务', 'Title.TLabel').pack(anchor='w', pady=(0, 6))
        self.label(rail, '选择一卷，开始探究。', 'Muted.TLabel').pack(anchor='w', pady=(0, 12))
        for i in range(4):
            card = FolioCard(rail, self, i)
            card.pack(fill='x', pady=(0, 8))
            self.folio_cards.append(card)
        # Keep the original task-selection controller, with cards as its view.
        self.task_list = ttk.Treeview(self.task_tab, columns=('name', 'progress', 'state'), show='headings')
        for col, title in [('name', '任务'), ('progress', '数据进度'), ('state', '完成状态')]:
            self.task_list.heading(col, text=self.tr(title))
        for i, (name, _, _) in enumerate(self.TASKS):
            self.task_list.insert('', 'end', iid=str(i), values=(name, '', ''))
        self.task_list.bind('<<TreeviewSelect>>', self.select_task)
        area = ttk.Frame(self.task_tab, style='Sheet.TFrame')
        area.grid(row=0, column=1, sticky='nsew')
        area.rowconfigure(0, weight=1)
        area.columnconfigure(0, weight=1)
        self.folio_scroll = tk.Canvas(area, bg=SHEET, highlightthickness=0)
        self.folio_scroll.grid(row=0, column=0, sticky='nsew')
        scrollbar = ttk.Scrollbar(area, orient='vertical', command=self.folio_scroll.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.folio_scroll.configure(yscrollcommand=scrollbar.set)
        self.detail = ttk.Frame(self.folio_scroll, style='Sheet.TFrame', padding=(20, 12, 16, 16))
        self.detail_window = self.folio_scroll.create_window(0, 0, window=self.detail, anchor='nw')
        self.detail.bind('<Configure>', lambda _: self.folio_scroll.configure(scrollregion=self.folio_scroll.bbox('all')))
        self.folio_scroll.bind('<Configure>', self.resize_folio)
        self.root.bind('<MouseWheel>', self.scroll_folio, add='+')
        page = self.detail
        self.label(page, '当前卷页', 'Note.TLabel').pack(anchor='w')
        self.selected_folio = tk.StringVar(value=self.tr('选择一卷，开始探究。'))
        ttk.Label(page, textvariable=self.selected_folio, style='Section.TLabel', font=(self.ui_font, 18, 'bold')).pack(anchor='w', pady=(5, 10))
        self.task_instruction = tk.StringVar()
        self.instruction_label = ttk.Label(page, textvariable=self.task_instruction, style='Sheet.TLabel', wraplength=700, justify='left')
        self.instruction_label.pack(fill='x', pady=(0, 12))
        self.label(page, '先预测，再动手', 'Section.TLabel').pack(anchor='w', pady=(0, 4))
        self.prediction_hint = self.label(page, '我的预测（任务2必须先填写；首次开始实验后锁定，避免事后修改）', 'Note.TLabel', wraplength=700)
        self.prediction_hint.pack(anchor='w')
        self.prediction_entry = ttk.Entry(page)
        self.prediction_entry.pack(fill='x', pady=(6, 10))
        self.preset_frame = ttk.Frame(page, style='Sheet.TFrame')
        self.preset_frame.pack(fill='x', pady=(0, 10))
        self.task_feedback = tk.StringVar()
        self.feedback_label = ttk.Label(page, textvariable=self.task_feedback, style='Note.TLabel', wraplength=700, justify='left')
        self.feedback_label.pack(fill='x', pady=(0, 14))
        self.conclusion_hint = self.label(page, '我的结论（引用数据，解释规律或模型局限）', 'Section.TLabel', wraplength=700)
        self.conclusion_hint.pack(anchor='w')
        self.conclusion_entry = ttk.Entry(page)
        self.conclusion_entry.pack(fill='x', pady=(7, 12))
        buttons = ttk.Frame(page, style='Sheet.TFrame')
        buttons.pack(fill='x')
        ttk.Button(buttons, text=self.tr('检查并完成当前任务'), style='Primary.TButton', command=self.complete_task).grid(row=0, column=0, sticky='w', padx=(0, 7))
        ttk.Button(buttons, text=self.tr('导出任务报告'), command=self.export_tasks).grid(row=0, column=1, sticky='w')
        ttk.Button(buttons, text=self.tr('自由实验模式'), command=self.free_mode).grid(row=1, column=0, sticky='w', pady=(7, 0))
        self.persistence_note = self.label(page, '任务进度只接受在该任务下新记录的数据；自由实验数据不计入。\n任务报告可导出保存；关闭程序后不会自动恢复进度。', 'Note.TLabel', wraplength=700)
        self.persistence_note.pack(fill='x', pady=(12, 0))
        self.prediction_entry.configure(state='disabled')
        self.conclusion_entry.configure(state='disabled')
        self.refresh_tasks()

    def resize_folio(self, event):
        self.folio_scroll.itemconfigure(self.detail_window, width=event.width)
        for label in (self.instruction_label, self.prediction_hint, self.feedback_label,
                      self.conclusion_hint, self.persistence_note):
            label.configure(wraplength=max(300, event.width-45))

    def scroll_folio(self, event):
        if str(event.widget).startswith(str(self.folio_scroll)):
            self.folio_scroll.yview_scroll(-int(event.delta/120), 'units')

    def select_task(self, event=None):
        if not self.task_list.selection():
            return
        self.conclusion_entry.configure(state='normal')
        super().select_task(event)
        self.prediction_entry.configure(state='readonly' if self.active_task == 1 and self.prediction_locked else 'normal')
        buttons = self.preset_frame.winfo_children()
        for button in buttons:
            button.pack_forget()
        for index, button in enumerate(buttons):
            button.grid(row=index//3, column=index%3, sticky='ew', padx=(0, 5), pady=3)
        for column in range(3):
            self.preset_frame.columnconfigure(column, weight=1)
        self.folio_scroll.yview_moveto(0)

    def refresh_tasks(self):
        super().refresh_tasks()
        if hasattr(self, 'selected_folio'):
            self.selected_folio.set(self.tr(self.TASKS[self.active_task][0]) if self.active_task is not None else self.tr('选择一卷，开始探究。'))
        for card in self.folio_cards:
            card.draw()

    def switch_language(self, language):
        super().switch_language(language)
        self.refresh_guide()
        # Derived card titles and artwork are not ordinary Label widgets.
        self.stage_key = None
        self.draw()

    def free_mode(self):
        super().free_mode()
        self.task_list.selection_remove(self.task_list.selection())
        self.prediction_entry.configure(state='disabled')
        self.conclusion_entry.configure(state='disabled')

    def record(self):
        super().record()
        for index, item in enumerate(self.table.get_children()):
            self.table.item(item, tags=('alternate',) if index%2 else ())

    @staticmethod
    def paper_border(canvas, width, height):
        canvas.create_rectangle(1, 1, width-2, height-2, outline=EDGE, tags='paper')
        for x, y, dx, dy in [(7, 7, 1, 1), (width-8, 7, -1, 1),
                             (7, height-8, 1, -1), (width-8, height-8, -1, -1)]:
            canvas.create_line(x, y+dy*13, x, y, x+dx*13, y, fill=GOLD, tags='paper')

    def stage_background(self, w, h, px, py, scale):
        c, m = self.canvas, self.model
        c.delete('all')
        self.paper_border(c, w, h)
        c.create_text(20, 23, text=self.tr('运动观察'), anchor='w', fill=WINE, font=(self.ui_font, 12, 'bold'))
        c.create_text(w-22, 23, text='FIG. I', anchor='e', fill=MUTED, font=('Georgia', 10))
        # Architectural construction lines, kept faint behind the apparatus.
        c.create_oval(px-90, py+12, px+90, py+192, outline='#F0E3C8')
        c.create_line(px-145, py+102, px+145, py+102, fill='#F0E3C8')
        for x in (44, w-54):
            c.create_rectangle(x, py-20, x+10, h-30, fill='#9D7850', outline='#795735')
            c.create_line(x+3, py-10, x+3, h-35, fill='#B89365')
            c.create_rectangle(x-13, h-32, x+23, h-26, fill='#795735', outline='')
        c.create_rectangle(40, py-25, w-40, py-9, fill='#916A42', outline='#795735')
        c.create_line(44, py-21, w-44, py-21, fill='#B49162')
        c.create_line(44, py-14, w-44, py-14, fill='#7A5734')
        for x in (49, w-49):
            c.create_oval(x-3, py-20, x+3, py-14, fill=GOLD, outline='#634A30')
        c.create_rectangle(px-10, py-27, px+10, py-7, fill=GOLD, outline='#77572F')
        c.create_line(px, py-7, px, py, fill=INK, width=3)
        c.create_line(px, py, px, py+2*scale+12, fill='#CAB991', dash=(3, 5))
        for degrees in range(-60, 61, 15):
            a = math.radians(degrees)
            c.create_line(px+36*math.sin(a), py+36*math.cos(a),
                          px+43*math.sin(a), py+43*math.cos(a), fill='#BDA57A')
        radius = m.length*scale
        bound = math.radians(m.angle)
        points = [value for i in range(81) for value in
                  (px+radius*math.sin(-bound+2*bound*i/80), py+radius*math.cos(-bound+2*bound*i/80))]
        c.create_line(*points, fill='#D6BC86', width=2, dash=(3, 4))
        c.create_text(w-22, h-16, text=self.tr('无阻力 · 定长绳 · 质点模型'), anchor='e',
                      fill=MUTED, font=(self.ui_font, 8))

    def draw(self):
        c, m = self.canvas, self.model
        w, h = c.winfo_width(), c.winfo_height()
        if w < 100 or h < 100:
            return
        px, py = w/2, 73
        scale = max(15, min((h-115)/2, (w-180)/3.6))
        key = (w, h, self.language, m.length, m.angle)
        if key != self.stage_key:
            self.stage_background(w, h, px, py, scale)
            self.stage_key = key
        c.delete('motion')
        radius = m.length*scale
        x, y = px+radius*math.sin(m.theta), py+radius*math.cos(m.theta)
        c.create_line(px, py, x, y, fill='#54432E', width=2, tags='motion')
        c.create_oval(px-4, py-4, px+4, py+4, fill=INK, outline=GOLD, tags='motion')
        c.create_oval(x-15, y-15, x+15, y+15, fill='#85612F', outline='#694C29', tags='motion')
        c.create_oval(x-13, y-14, x+12, y+11, fill=GOLD, outline='', tags='motion')
        c.create_oval(x-10, y-11, x+6, y+3, fill='#D6B56F', outline='', tags='motion')
        c.create_oval(x-7, y-9, x-1, y-4, fill='#F2DDA2', outline='', tags='motion')
        c.create_text(px+radius*math.sin(m.theta)/2+38, py+radius*math.cos(m.theta)/2,
                      text=f'{m.length:.2f} m', fill=INK, font=('Georgia', 10), tags='motion')
        period = self.tr('等待测量') if m.period is None else f'{m.period:.3f} s'
        self.metrics.set(f"{self.tr('时间 ')}{m.t:.2f}{self.tr(' s    当前角度 ')}{math.degrees(m.theta):+.1f}"
                         f"{self.tr('°    完整周期数 ')}{m.cycles}\n"
                         f"{self.tr('模拟周期：')}{period}{self.tr('     小角度公式：')}{m.theoretical_period:.3f} s")
        self.draw_chart()

    def draw_chart(self):
        c, m = self.chart, self.model
        w, h = c.winfo_width(), c.winfo_height()
        if w < 100 or h < 70:
            return
        c.delete('all')
        self.paper_border(c, w, h)
        left, right, top, bottom = 48, w-25, 42, h-28
        c.create_text(18, 20, text=self.tr('摆角 θ（°）— 模拟时间 t（s）｜最近15秒'),
                      anchor='w', fill=INK, font=(self.ui_font, 9))
        amplitude = max(20, m.angle*1.15)
        start = max(0, m.t-15)
        def xy(t, a):
            return left+(t-start)/15*(right-left), (top+bottom)/2-a/amplitude*(bottom-top)/2
        for angle in [-amplitude, 0, amplitude]:
            yy = xy(start, angle)[1]
            c.create_line(left, yy, right, yy, fill='#E6D9BE', dash=(2, 4))
            c.create_text(left-8, yy, text=f'{angle:.0f}', anchor='e', fill=MUTED, font=('Georgia', 9))
        for i in range(6):
            t = start+i*3
            xx = xy(t, 0)[0]
            c.create_line(xx, top, xx, bottom, fill='#F0E5CE')
            c.create_text(xx, bottom+14, text=f'{t:.1f}', fill=MUTED, font=('Georgia', 9))
        points = [value for t, a in self.history for value in xy(t, a)]
        if len(points) >= 4:
            c.create_line(*points, fill=WINE, width=2)


if __name__ == '__main__':
    window = tk.Tk()
    Workshop(window)
    window.mainloop()
