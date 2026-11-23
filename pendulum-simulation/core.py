"""交互式单摆实验室：仅使用 Python 标准库。"""
import csv
import json
import math
import time
import tkinter as tk
from dataclasses import dataclass
from functools import partial
from tkinter import filedialog, messagebox, ttk
from language_support import translate, capture_widgets


@dataclass
class Pendulum:
    length: float = 1.0
    angle: float = 15.0
    gravity: float = 9.81

    def __post_init__(self):
        self.reset()

    def reset(self):
        self.theta = math.radians(self.angle)
        self.omega = self.t = 0.0
        self.last_crossing = None
        self.period = None
        self.crossings = 0
        self.cycles = 0

    @property
    def theoretical_period(self):
        return 2 * math.pi * math.sqrt(self.length / self.gravity)

    def step(self, dt):
        # 非线性运动方程；四阶 Runge–Kutta 积分。
        old_theta, old_t = self.theta, self.t
        def derivative(theta, omega):
            return omega, -self.gravity / self.length * math.sin(theta)
        a, b = derivative(self.theta, self.omega)
        c, d = derivative(self.theta + dt*a/2, self.omega + dt*b/2)
        e, f = derivative(self.theta + dt*c/2, self.omega + dt*d/2)
        h, j = derivative(self.theta + dt*e, self.omega + dt*f)
        self.theta += dt * (a + 2*c + 2*e + h) / 6
        self.omega += dt * (b + 2*d + 2*f + j) / 6
        self.t += dt
        # 每次从右向左经过平衡位置，插值定位；相邻同向过零间隔为周期。
        if old_theta > 0 >= self.theta:
            crossing = old_t + dt * old_theta / (old_theta - self.theta)
            if self.last_crossing is not None:
                self.period = crossing - self.last_crossing
            self.last_crossing = crossing
            self.crossings += 1
        self.cycles = max(0, self.crossings - 1)


class Lab:
    BG = '#edf2f7'
    INK = '#183047'
    BLUE = '#1676c4'
    DT = 1 / 240
    TASKS = [
        ('1. 找规律', [(v, 10, 9.81) for v in (.25, .5, 1, 1.5, 2)],
         '固定初始角度10°、地球重力，测试5种摆长。记录周期后，解释摆长与周期的关系。'),
        ('2. 检验猜想', [(.25, 10, 9.81), (1, 10, 9.81)],
         '先写下预测：摆长从0.25 m增至1 m（4倍），周期会变为几倍？再运行两组实验，用数据检验。'),
        ('3. 评价模型', [(1, v, 9.81) for v in (5, 15, 30, 60)],
         '固定1 m、地球重力，逐渐增大角度。此任务以偏差超过2%作为“明显偏离”的课堂标准，并非通用物理边界。'),
        ('4. 地球与月球', [(1, 10, g) for g in (9.81, 1.62)],
         '保持1 m、初始角度10°不变，比较地球与月球的周期，并解释重力的影响。')]

    def __init__(self, root):
        self.root = root
        self.language = 'zh-CN'
        root.title(self.tr('单摆实验室 · Python Physics Lab'))
        root.geometry('1180x820')
        root.minsize(960, 720)
        root.configure(bg=self.BG)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('.', font=('Microsoft YaHei UI', 10))
        style.configure('TFrame', background=self.BG)
        style.configure('TLabel', background=self.BG, foreground=self.INK)
        style.configure('Title.TLabel', font=('Microsoft YaHei UI', 20, 'bold'))
        style.configure('TButton', padding=7)
        self.model = Pendulum()
        self.running = False
        self.drag_resume = False
        self.dragging = False
        self.accumulator = 0.0
        self.history = [(0, self.model.angle)]
        self.records = []
        self.task_records = [{} for _ in self.TASKS]
        self.task_done = [False] * len(self.TASKS)
        self.predictions = [tk.StringVar() for _ in self.TASKS]
        self.conclusions = [tk.StringVar() for _ in self.TASKS]
        self.prediction_locked = False
        self.active_task = None
        self.last_wall = time.perf_counter()
        self.length = tk.DoubleVar(value=1)
        self.angle = tk.DoubleVar(value=15)
        self.gravity = tk.DoubleVar(value=9.81)
        self.speed = tk.StringVar(value='1×')
        self.status = tk.StringVar(value=self.tr('先预测，再拖动滑块。点击“开始”释放单摆。'))
        self.metrics = tk.StringVar()
        self.build()
        self.localized_widgets = capture_widgets(root)
        self.heading_sources = [(tree, column, tree.heading(column, 'text'))
                                for tree in (self.table, self.task_list) for column in tree['columns']]
        self.root.after(30, self.tick)

    def tr(self, text):
        return translate(text, self.language)

    def switch_language(self, language):
        self.language = language
        self.root.title(self.tr('单摆实验室 · Python Physics Lab'))
        for widget, original in self.localized_widgets:
            if widget.winfo_exists():
                widget.configure(text=self.tr(original))
        for tree, column, original in self.heading_sources:
            tree.heading(column, text=self.tr(original))
        for tab, original in [(self.lab_tab, '单摆实验'), (self.task_tab, '递进任务清单')]:
            self.notebook.tab(tab, text=self.tr(original))
        if self.active_task is not None:
            self.task_instruction.set(self.tr(self.TASKS[self.active_task][2]))
        self.update_labels()
        self.update_play()
        self.refresh_tasks()
        self.draw()
        self.status.set(self.tr('语言已切换，实验与任务数据已保留。'))
        for code, button in self.language_buttons.items():
            button.state(['disabled'] if code == language else ['!disabled'])

    def build(self):
        header = ttk.Frame(self.root, padding=(22, 14))
        header.pack(fill='x')
        ttk.Label(header, text=self.tr('单摆实验室'), style='Title.TLabel').pack(side='left')
        self.language_buttons = {}
        for code, label in [('zh-CN', '简中'), ('zh-TW', '繁中'), ('en', 'English')]:
            button = ttk.Button(header, text=label, command=partial(self.switch_language, code))
            button.pack(side='left', padx=(8, 0))
            self.language_buttons[code] = button
        self.language_buttons['zh-CN'].state(['disabled'])
        ttk.Label(header, text=self.tr('预测 → 调参 → 观察 → 解释')).pack(side='right')
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=12)
        self.lab_tab = ttk.Frame(self.notebook)
        self.task_tab = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(self.lab_tab, text=self.tr('单摆实验'))
        self.notebook.add(self.task_tab, text=self.tr('递进任务清单'))
        body = ttk.Frame(self.lab_tab, padding=(6, 0))
        body.pack(fill='both', expand=True)
        controls = ttk.Frame(body, padding=12, width=260)
        controls.pack(side='left', fill='y')
        controls.pack_propagate(False)
        ttk.Label(controls, text=self.tr('实验参数'), font=('Microsoft YaHei UI', 13, 'bold')).pack(anchor='w')
        self.value_labels = []
        for name, variable, low, high, unit in [
            (self.tr('摆长'), self.length, .2, 2, 'm'),
            (self.tr('初始角度'), self.angle, 5, 60, '°'),
            (self.tr('重力加速度'), self.gravity, 1.6, 20, 'm/s²')]:
            label = ttk.Label(controls)
            label.pack(anchor='w', pady=(19, 2))
            self.value_labels.append((label, name, variable, unit))
            slider = ttk.Scale(controls, from_=low, to=high, variable=variable,
                               command=self.parameters_changed)
            slider.pack(fill='x')
            slider.bind('<ButtonPress-1>', self.begin_drag)
            slider.bind('<ButtonRelease-1>', self.end_drag)
        presets = ttk.Frame(controls)
        presets.pack(fill='x', pady=16)
        ttk.Button(presets, text=self.tr('地球'), command=lambda: self.set_gravity(9.81)).pack(side='left')
        ttk.Button(presets, text=self.tr('月球'), command=lambda: self.set_gravity(1.62)).pack(side='left', padx=6)
        self.play = ttk.Button(controls, text=self.tr('▶ 开始'), command=self.toggle)
        self.play.pack(fill='x', pady=4)
        ttk.Button(controls, text=self.tr('重置本次实验'), command=self.reset).pack(fill='x', pady=4)
        ttk.Button(controls, text=self.tr('单步前进 0.02 s'), command=self.single_step).pack(fill='x', pady=4)
        ttk.Label(controls, text=self.tr('播放速度（不改变物理周期）')).pack(anchor='w', pady=(16, 4))
        ttk.Combobox(controls, textvariable=self.speed, values=['0.25×', '0.5×', '1×', '2×'],
                     state='readonly', width=12).pack(anchor='w')
        ttk.Button(controls, text=self.tr('恢复默认参数'), command=self.defaults).pack(fill='x', pady=(18, 8))
        ttk.Label(controls, text=self.tr('模型假设\n无空气阻力；绳不可伸长；\n摆球视为质点。\n\n滑块改变后重新释放，\n已有实验记录保留。\n\n提示：先保持角度不变，\n只改变摆长。'), justify='left').pack(anchor='w', pady=10)
        right = ttk.Frame(body)
        right.pack(side='left', fill='both', expand=True)
        self.canvas = tk.Canvas(right, bg='white', highlightthickness=0, height=285)
        self.canvas.pack(fill='both', expand=True)
        ttk.Label(right, textvariable=self.metrics, padding=8, font=('Microsoft YaHei UI', 11)).pack(fill='x')
        self.chart = tk.Canvas(right, bg='white', height=155, highlightthickness=0)
        self.chart.pack(fill='x')
        bar = ttk.Frame(right, padding=(0, 7))
        bar.pack(fill='x')
        ttk.Button(bar, text=self.tr('记录本次实验'), command=self.record).pack(side='left')
        ttk.Button(bar, text=self.tr('导出 CSV'), command=self.export).pack(side='left', padx=8)
        ttk.Button(bar, text=self.tr('清空记录'), command=self.clear_records).pack(side='right')
        columns = ('n', 'length', 'angle', 'gravity', 'measured', 'theory', 'difference')
        self.table = ttk.Treeview(right, columns=columns, show='headings', height=4)
        for col, title, width in zip(columns,
            [self.tr('序号'), self.tr('摆长 / m'), self.tr('初始角 / °'), 'g / m/s²', self.tr('模拟周期 / s'), self.tr('小角度公式 / s'), self.tr('偏差 / %')],
            [45, 85, 85, 90, 110, 125, 85]):
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor='center')
        self.table.pack(fill='x')
        ttk.Label(self.root, textvariable=self.status, padding=(22, 10)).pack(fill='x')
        self.update_labels()
        self.build_tasks()
        for child in controls.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(wraplength=230)
        for child in self.task_tab.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(wraplength=850)

    def build_tasks(self):
        page = self.task_tab
        ttk.Label(page, text=self.tr('递进探究任务'), style='Title.TLabel').pack(anchor='w')
        ttk.Label(page, text=self.tr('选择任务 → 填写预测 → 加载参数并运行 → 记录本次实验 → 写结论并完成任务')).pack(anchor='w', pady=8)
        self.task_list = ttk.Treeview(page, columns=('name', 'progress', 'state'), show='headings', height=4)
        for col, title in [('name', self.tr('任务')), ('progress', self.tr('数据进度')), ('state', self.tr('完成状态'))]:
            self.task_list.heading(col, text=title)
            self.task_list.column(col, width=220)
        self.task_list.pack(fill='x', pady=8)
        for i, (name, _, _) in enumerate(self.TASKS):
            self.task_list.insert('', 'end', iid=str(i), values=(name, '', ''))
        self.task_list.bind('<<TreeviewSelect>>', self.select_task)
        self.task_instruction = tk.StringVar()
        ttk.Label(page, textvariable=self.task_instruction, wraplength=850).pack(anchor='w', pady=10)
        ttk.Label(page, text=self.tr('我的预测（任务2必须先填写；首次开始实验后锁定，避免事后修改）')).pack(anchor='w')
        self.prediction_entry = ttk.Entry(page)
        self.prediction_entry.pack(fill='x', pady=5)
        self.preset_frame = ttk.Frame(page)
        self.preset_frame.pack(fill='x', pady=8)
        self.task_feedback = tk.StringVar()
        ttk.Label(page, textvariable=self.task_feedback, wraplength=850, justify='left').pack(anchor='w', pady=10)
        ttk.Label(page, text=self.tr('我的结论（引用数据，解释规律或模型局限）')).pack(anchor='w')
        self.conclusion_entry = ttk.Entry(page)
        self.conclusion_entry.pack(fill='x', pady=5)
        buttons = ttk.Frame(page)
        buttons.pack(fill='x', pady=12)
        ttk.Button(buttons, text=self.tr('检查并完成当前任务'), command=self.complete_task).pack(side='left')
        ttk.Button(buttons, text=self.tr('导出任务报告'), command=self.export_tasks).pack(side='left', padx=10)
        ttk.Button(buttons, text=self.tr('自由实验模式'), command=self.free_mode).pack(side='left')
        ttk.Label(page, text=self.tr('任务进度只接受在该任务下新记录的数据；自由实验数据不计入。\n任务报告可导出保存；关闭程序后不会自动恢复进度。'), wraplength=850).pack(anchor='w', pady=8)
        self.refresh_tasks()
        self.task_list.selection_set('0')

    def select_task(self, event=None):
        selected = self.task_list.selection()
        if not selected:
            return
        self.active_task = int(selected[0])
        i = self.active_task
        name, cases, instruction = self.TASKS[i]
        name = self.tr(name)
        self.task_instruction.set(self.tr(instruction))
        self.prediction_entry.configure(textvariable=self.predictions[i],
            state='readonly' if i == 1 and self.prediction_locked else 'normal')
        self.conclusion_entry.configure(textvariable=self.conclusions[i])
        for child in self.preset_frame.winfo_children():
            child.destroy()
        for case in cases:
            length, angle, gravity = case
            text = f'{length:g} m / {angle:g}° / g={gravity:g}'
            ttk.Button(self.preset_frame, text=text,
                       command=partial(self.load_case, case)).pack(side='left', padx=3)
        self.running = False
        self.reset_state()
        self.update_play()
        self.status.set(f"{self.tr('当前任务：')}{name}{self.tr('。请加载一组参数后开始实验。')}")
        self.refresh_tasks()

    def load_case(self, case):
        self.running = False
        for variable, value in zip((self.length, self.angle, self.gravity), case):
            variable.set(value)
        self.parameters_changed()
        self.update_play()
        self.notebook.select(self.lab_tab)

    def allow_experiment(self):
        if self.active_task == 1:
            if not self.predictions[1].get().strip():
                self.notebook.select(self.task_tab)
                messagebox.showinfo(self.tr('先预测，再实验'), self.tr('请先在任务2填写周期将变为几倍及你的理由，再运行或单步。'))
                return False
            self.prediction_locked = True
            self.prediction_entry.configure(state='readonly')
        return True

    def refresh_tasks(self):
        for i, (name, cases, _) in enumerate(self.TASKS):
            name = self.tr(name)
            self.task_list.item(str(i), values=(name, f"{len(self.task_records[i])}/{len(cases)}{self.tr(' 组')}",
                                self.tr('✓ 已完成') if self.task_done[i] else self.tr('待完成')))
        i = self.active_task
        if i is None:
            self.task_feedback.set(self.tr('当前为自由实验模式。选择上方任务开始探究。'))
            return
        evidence = self.task_records[i]
        lines = []
        for case in self.TASKS[i][1]:
            row = evidence.get(case)
            label = f'L={case[0]:g} m，θ₀={case[1]:g}°，g={case[2]:g}'
            lines.append(f"✓ {label}：T={row[4]}{self.tr(' s，偏差=')}{row[6]}%" if row else f"□ {label}{self.tr('：待记录')}")
        if len(evidence) == len(self.TASKS[i][1]):
            cases = self.TASKS[i][1]
            if i in (1, 3):
                ratio = float(evidence[cases[1]][4]) / float(evidence[cases[0]][4])
                lines.append(f"{self.tr('第二组 / 第一组的周期比 = ')}{ratio:.3f}{self.tr('。请与你的预测或解释比较。')}")
            elif i == 2:
                angles = [case[1] for case in cases if abs(float(evidence[case][6])) > 2]
                lines.append(f"{self.tr('已测角度中首次超过2%偏差：')}{min(angles):g}{self.tr('°。可进一步细测临界范围。')}" if angles else self.tr('已测角度均未超过2%。'))
        self.task_feedback.set('\n'.join(lines))

    def complete_task(self):
        i = self.active_task
        if i is None:
            return
        if len(self.task_records[i]) != len(self.TASKS[i][1]) or not self.conclusions[i].get().strip():
            messagebox.showinfo(self.tr('任务尚未完成'), self.tr('请记录该任务的全部参数组，并填写自己的结论。'))
            return
        self.task_done[i] = True
        self.refresh_tasks()
        self.status.set(self.tr('任务已完成！结论由学生填写，教师可结合数据评价。'))

    def free_mode(self):
        self.active_task = None
        self.running = False
        self.update_play()
        self.refresh_tasks()
        self.status.set(self.tr('自由实验模式：记录不计入任务进度。'))
        self.notebook.select(self.lab_tab)

    def export_tasks(self):
        path = filedialog.asksaveasfilename(defaultextension='.json', initialfile=self.tr('单摆探究任务报告.json'),
                                           filetypes=[(self.tr('任务报告 JSON'), '*.json')])
        if not path:
            return
        report = [{self.tr('任务'): self.tr(name), self.tr('说明'): self.tr(instruction), self.tr('预测'): self.predictions[i].get(),
                   self.tr('结论'): self.conclusions[i].get(), self.tr('已完成'): self.task_done[i],
                   self.tr('实验数据'): list(self.task_records[i].values())}
                  for i, (name, _, instruction) in enumerate(self.TASKS)]
        try:
            with open(path, 'w', encoding='utf-8') as file:
                json.dump({self.tr('列名'): [self.tr('序号'), self.tr('摆长(m)'), self.tr('初始角(°)'), 'g(m/s²)', self.tr('模拟周期(s)'), self.tr('小角度周期(s)'), self.tr('偏差(%)')],
                           self.tr('任务'): report}, file, ensure_ascii=False, indent=2)
            self.status.set(self.tr('已导出任务报告（含预测、结论、数据和完成状态）。'))
        except OSError as exc:
            messagebox.showerror(self.tr('导出失败'), str(exc))

    def update_labels(self):
        for label, name, var, unit in self.value_labels:
            name = self.tr(name)
            label.config(text=f'{name}  {var.get():.2f} {unit}')

    def begin_drag(self, event):
        self.dragging = True
        self.drag_resume = self.running
        self.running = False

    def end_drag(self, event):
        self.dragging = False
        self.running = self.drag_resume and self.allow_experiment()
        self.last_wall = time.perf_counter()
        self.update_play()

    def parameters_changed(self, value=None):
        self.update_labels()
        self.model.length = round(self.length.get(), 4)
        self.model.angle = round(self.angle.get(), 4)
        self.model.gravity = round(self.gravity.get(), 4)
        self.reset_state()
        self.status.set(self.tr('参数已更新，本次实验重新开始。周期由模拟中相邻两次同向过零测得。'))

    def reset_state(self):
        self.model.reset()
        self.history = [(0, self.model.angle)]
        self.accumulator = 0
        self.last_wall = time.perf_counter()

    def reset(self):
        self.running = False
        self.reset_state()
        self.update_play()
        self.status.set(self.tr('已回到当前参数的释放位置。'))

    def defaults(self):
        self.running = False
        self.length.set(1)
        self.angle.set(15)
        self.gravity.set(9.81)
        self.parameters_changed()
        self.update_play()

    def set_gravity(self, value):
        self.gravity.set(value)
        self.parameters_changed()

    def update_play(self):
        self.play.config(text=self.tr('Ⅱ 暂停') if self.running else self.tr('▶ 开始 / 继续'))

    def toggle(self):
        if not self.running and not self.allow_experiment():
            return
        self.running = not self.running
        self.last_wall = time.perf_counter()
        self.update_play()

    def advance(self, duration):
        self.accumulator += duration
        while self.accumulator >= self.DT:
            self.model.step(self.DT)
            self.accumulator -= self.DT
        self.history.append((self.model.t, math.degrees(self.model.theta)))
        cutoff = self.model.t - 15
        self.history = [(t, a) for t, a in self.history if t >= cutoff]

    def single_step(self):
        if not self.allow_experiment():
            return
        self.running = False
        self.update_play()
        self.advance(.02)

    def tick(self):
        now = time.perf_counter()
        elapsed = min(now - self.last_wall, .1)
        self.last_wall = now
        if self.running:
            self.advance(elapsed * float(self.speed.get().rstrip('×')))
        self.draw()
        self.root.after(16, self.tick)

    def draw(self):
        m, c = self.model, self.canvas
        c.delete('all')
        w, h = c.winfo_width(), c.winfo_height()
        px, py = w/2, 35
        scale = min((h-70)/2, (w-100)/3.6)
        radius = m.length * scale
        x, y = px + radius*math.sin(m.theta), py + radius*math.cos(m.theta)
        c.create_text(16, 18, anchor='w', text=self.tr('非线性单摆 · 固定空间比例'), fill=self.INK)
        c.create_line(px, py, px, py+2*scale, dash=(4, 5), fill='#cad5e0')
        bound = math.radians(m.angle)
        points = []
        for i in range(81):
            a = -bound + 2*bound*i/80
            points += [px+radius*math.sin(a), py+radius*math.cos(a)]
        c.create_line(*points, fill='#c4e3f6', width=3)
        c.create_line(px-30, py, px+30, py, width=5, fill=self.INK)
        c.create_line(px, py, x, y, width=3, fill=self.INK)
        c.create_oval(x-13, y-13, x+13, y+13, fill=self.BLUE, outline='')
        c.create_oval(px-4, py-4, px+4, py+4, fill=self.INK)
        c.create_text((px+x)/2+35, (py+y)/2, text=f'{m.length:.2f} m', fill=self.INK)
        period = self.tr('等待测量') if m.period is None else f'{m.period:.3f} s'
        self.metrics.set(f"{self.tr('时间 ')}{m.t:.2f}{self.tr(' s    当前角度 ')}{math.degrees(m.theta):+.1f}{self.tr('°    完整周期数 ')}{m.cycles}\n"
                         f"{self.tr('模拟周期：')}{period}{self.tr('     小角度公式：')}{m.theoretical_period:.3f} s")
        self.draw_chart()

    def draw_chart(self):
        c = self.chart
        c.delete('all')
        w, h = c.winfo_width(), c.winfo_height()
        left, right, top, bottom = 50, w-20, 30, h-30
        amplitude = max(20, self.model.angle*1.15)
        start = max(0, self.model.t-15)
        def xy(t, a):
            return left+(t-start)/15*(right-left), (top+bottom)/2-a/amplitude*(bottom-top)/2
        c.create_text(12, 13, text=self.tr('摆角 θ（°）— 模拟时间 t（s）｜最近15秒'), anchor='w', fill=self.INK)
        for angle in [-amplitude, 0, amplitude]:
            yy = xy(start, angle)[1]
            c.create_line(left, yy, right, yy, fill='#e5ebf0')
            c.create_text(left-7, yy, text=f'{angle:.0f}', anchor='e', fill='#607080')
        for i in range(6):
            t = start+i*3
            xx = xy(t, 0)[0]
            c.create_text(xx, bottom+15, text=f'{t:.1f}', fill='#607080')
        points = [value for t, a in self.history for value in xy(t, a)]
        if len(points) >= 4:
            c.create_line(*points, fill=self.BLUE, width=2)

    def record(self):
        m = self.model
        if m.period is None:
            messagebox.showinfo(self.tr('还没有测得周期'), self.tr('请先运行至完成两次从右向左的平衡位置穿越，再记录。'))
            return
        values = (len(self.records)+1, f'{m.length:.4f}', f'{m.angle:.4f}', f'{m.gravity:.4f}',
                  f'{m.period:.5f}', f'{m.theoretical_period:.5f}',
                  f'{100*(m.period/m.theoretical_period-1):.3f}')
        self.records.append(values)
        item = self.table.insert('', 'end', values=values)
        self.table.see(item)
        self.status.set(self.tr('实验已记录。偏差 =（模拟周期 − 小角度公式周期）/ 小角度公式周期 × 100%。'))
        i = self.active_task
        if i is not None:
            case = next((case for case in self.TASKS[i][1]
                         if all(abs(a-b) < .0001 for a, b in zip(case, (m.length, m.angle, m.gravity)))), None)
            if case is not None and (i != 1 or self.prediction_locked):
                self.task_records[i][case] = values
                self.task_done[i] = False
                self.status.set(self.tr('已更新当前任务的数据进度。前往“递进任务清单”查看结果并写结论。'))
            else:
                self.status.set(self.tr('已存入实验表，但不计入任务进度：请使用任务参数预设，并先完成预测。'))
            self.refresh_tasks()

    def export(self):
        if not self.records:
            messagebox.showinfo(self.tr('暂无记录'), self.tr('先点击“记录本次实验”保存至少一组数据。'))
            return
        path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile=self.tr('单摆实验记录.csv'),
                                           filetypes=[(self.tr('CSV 文件'), '*.csv')])
        if path:
            try:
                with open(path, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    writer.writerow([self.tr('序号'), self.tr('摆长(m)'), self.tr('初始角度(°)'), self.tr('重力加速度(m/s²)'),
                                     self.tr('模拟周期(s)'), self.tr('小角度公式周期(s)'), self.tr('偏差(%)')])
                    writer.writerows(self.records)
                self.status.set(f"{self.tr('已导出 ')}{len(self.records)}{self.tr(' 组实验数据。')}")
            except OSError as exc:
                messagebox.showerror(self.tr('导出失败'), str(exc))

    def clear_records(self):
        self.records.clear()
        self.table.delete(*self.table.get_children())
        self.task_records = [{} for _ in self.TASKS]
        self.task_done = [False] * len(self.TASKS)
        self.refresh_tasks()
        self.status.set(self.tr('实验记录已清空。'))


if __name__ == '__main__':
    root = tk.Tk()
    Lab(root)
    root.mainloop()
