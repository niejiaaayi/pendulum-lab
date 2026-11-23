"""Three-language handbook content, bundled as Python data with the desktop app."""

LANGUAGES = {'zh-CN': 0, 'zh-TW': 1, 'en': 2}

GUIDE_UI = {
    '如何使用': ('如何使用', '如何使用', 'How to use'),
    '如何使用这个项目': ('如何使用这个项目', '如何使用這個專案', 'How to use this project'),
    '使用指引': ('使用指引', '使用指引', 'User guide'),
    '选择章节查看说明；也可以随时按 F1 打开指引。': (
        '选择章节查看说明；也可以随时按 F1 打开指引。',
        '選擇章節查看說明；也可以隨時按 F1 開啟指引。',
        'Choose a chapter. Press F1 at any time to open this guide.'),
    '前往实验工坊': ('前往实验工坊', '前往實驗工坊', 'Go to workshop'),
    '前往探究卷册': ('前往探究卷册', '前往探究卷冊', 'Go to inquiry folios'),
    '查阅指引会保留当前实验；若要停住运动，请先点击“暂停”。': (
        '查阅指引会保留当前实验；若要停住运动，请先点击“暂停”。',
        '查閱指引會保留目前實驗；若要停住運動，請先點擊「暫停」。',
        'Opening the guide keeps your experiment. Click Pause first if you want the motion to stop.'),
}

# Each chapter contains a localized title and localized (heading, body) blocks.
GUIDE_SECTIONS = [
    (('1. 快速上手', '1. 快速上手', '1. Quick start'), [
        (('认识两个工作区', ' 認識兩個工作區', 'Meet the two workspaces'),
         ('“实验工坊”用于调节参数、观察单摆和记录数据；“探究卷册”用于选择任务、填写预测和结论、检查进度。右上角可切换简中、繁中、英文。',
          '「實驗工坊」用於調節參數、觀察單擺和記錄資料；「探究卷冊」用於選擇任務、填寫預測和結論、檢查進度。右上角可切換簡中、繁中、英文。',
          'Use The workshop to adjust parameters, observe the pendulum and record data. Use Inquiry folios to choose tasks, write predictions and conclusions, and check progress. The top-right buttons switch between Simplified Chinese, Traditional Chinese and English.')),
        (('第一步：设置并运行', '第一步：設定並執行', 'Step 1 · Set up and run'),
         ('拖动摆长、初始角度和重力加速度滑块，然后点击“开始”。首次体验可以保持默认的1 m、15°和地球重力9.81 m/s²。',
          '拖動擺長、初始角度和重力加速度滑桿，然後點擊「開始」。初次體驗可以保持預設的1 m、15°和地球重力9.81 m/s²。',
          'Drag the length, initial-angle and gravity sliders, then click Start. For your first run, keep the defaults: 1 m, 15° and Earth gravity of 9.81 m/s².')),
        (('第二步：观察并记录', '第二步：觀察並記錄', 'Step 2 · Observe and record'),
         ('观察单摆动画、摆角—时间曲线及周期读数。出现模拟周期后，点击“记录本次实验”，数据才会进入实验手稿表格。只点击开始或暂停不会保存一条记录。',
          '觀察單擺動畫、擺角—時間曲線及週期讀數。出現模擬週期後，點擊「記錄本次實驗」，資料才會進入實驗手稿表格。只點擊開始或暫停不會儲存一筆記錄。',
          'Watch the animation, angle–time trace and period readings. Once a simulated period appears, click Record experiment to add it to the notebook table. Starting or pausing alone does not create a record.')),
        (('第三步：开展任务并导出', '第三步：開展任務並匯出', 'Step 3 · Investigate and export'),
         ('打开“探究卷册”，选择一卷，使用预设参数逐组运行和记录；回到卷册写结论并检查完成状态。离开程序前，导出CSV实验数据和JSON任务报告。',
          '開啟「探究卷冊」，選擇一卷，使用預設參數逐組執行和記錄；回到卷冊寫結論並檢查完成狀態。離開程式前，匯出CSV實驗資料和JSON任務報告。',
          'Open Inquiry folios, choose a folio, and run and record each parameter preset. Return to write a conclusion and check completion. Before closing, export CSV experiment data and a JSON task report.')),
    ]),
    (('2. 按键与滑块', '2. 按鍵與滑桿', '2. Buttons and sliders'), [
        (('三个参数滑块', '三個參數滑桿', 'The three parameter sliders'),
         ('摆长：0.2–2.0 m，表示悬挂点到摆球重心的距离。\n初始角度：5–60°，表示从平衡位置偏开的释放角度。\n重力加速度：1.6–20 m/s²，用于比较不同重力条件。\n点击滑块后可用方向键微调；Home和End跳到最小、最大值。',
          '擺長：0.2–2.0 m，表示懸掛點到擺球重心的距離。\n初始角度：5–60°，表示從平衡位置偏開的釋放角度。\n重力加速度：1.6–20 m/s²，用於比較不同重力條件。\n點擊滑桿後可用方向鍵微調；Home和End跳到最小、最大值。',
          'Length: 0.2–2.0 m, measured from the pivot to the centre of the bob.\nInitial angle: 5–60°, the release angle from equilibrium.\nGravity: 1.6–20 m/s², for comparing gravitational conditions.\nClick a slider and use arrow keys for fine adjustments; Home and End select its minimum and maximum.')),
        (('调整参数时会发生什么', '調整參數時會發生甚麼', 'What happens when parameters change'),
         ('调整任一参数都会重置本次模拟的时间和曲线，并从新的释放位置开始。运行时拖动滑块会先暂停预览，松开后自动重新运行；原来已暂停则保持暂停。已记录的数据不会因此删除。',
          '調整任何參數都會重設本次模擬的時間和曲線，並從新的釋放位置開始。執行時拖動滑桿會先暫停預覽，放開後自動重新執行；原來已暫停則保持暫停。已記錄的資料不會因此刪除。',
          'Changing any parameter resets the current simulation time and trace to a new release. Dragging during a run pauses for a preview and restarts on release; a paused experiment stays paused. Existing records are kept.')),
        (('地球／月球', '地球／月球', 'Earth / Moon'),
         ('将重力加速度设为9.81或1.62 m/s²，保留当前摆长和角度，并重置本次模拟。若当前正在运行，会按新参数继续运行。',
          '將重力加速度設為9.81或1.62 m/s²，保留目前擺長和角度，並重設本次模擬。若目前正在執行，會按新參數繼續執行。',
          'Set gravity to 9.81 or 1.62 m/s² while keeping length and angle, and reset the current simulation. If it is running, it continues with the new parameters.')),
        (('开始／继续、暂停', '開始／繼續、暫停', 'Start / Resume and Pause'),
         ('开始或继续运动；运行时按钮变为“暂停”。暂停会停住当前画面，再点击可从当前位置继续。卷二必须先填写预测才能开始。',
          '開始或繼續運動；執行時按鈕變為「暫停」。暫停會停住目前畫面，再點擊可從目前位置繼續。卷二必須先填寫預測才能開始。',
          'Start or resume motion; the button becomes Pause during a run. Pause holds the current position so you can resume from it. Folio II requires a prediction before starting.')),
        (('重置本次实验、单步前进', '重設本次實驗、單步前進', 'Reset simulation and Step forward'),
         ('重置：停止运动，保留当前参数，回到释放位置，清空本次时间与曲线。\n单步前进0.02 s：暂停连续运动，推进约0.02秒模拟时间，适合逐步观察。两者均不删除已记录的数据。',
          '重設：停止運動，保留目前參數，回到釋放位置，清空本次時間與曲線。\n單步前進0.02 s：暫停連續運動，推進約0.02秒模擬時間，適合逐步觀察。兩者均不刪除已記錄的資料。',
          'Reset: stop motion, keep the current parameters, return to the release position, and clear the current time and trace.\nStep forward 0.02 s: pause continuous motion and advance about 0.02 seconds of simulation time. Neither action deletes existing records.')),
        (('播放速度、恢复默认参数', '播放速度、恢復預設參數', 'Playback speed and Restore defaults'),
         ('播放速度可选0.25×、0.5×、1×、2×，只改变观看速度，不改变物理周期。\n恢复默认参数：停止运动，将参数恢复为1 m、15°、9.81 m/s²，并重置本次模拟；播放速度不变。',
          '播放速度可選0.25×、0.5×、1×、2×，只改變觀看速度，不改變物理週期。\n恢復預設參數：停止運動，將參數恢復為1 m、15°、9.81 m/s²，並重設本次模擬；播放速度不變。',
          'Choose 0.25×, 0.5×, 1× or 2× playback. This changes viewing speed, not the physical period.\nRestore defaults stops motion, restores 1 m, 15° and 9.81 m/s², and resets the current simulation. Playback speed is unchanged.')),
        (('记录本次实验、导出CSV', '記錄本次實驗、匯出CSV', 'Record experiment and Export CSV'),
         ('记录本次实验：周期测得后，将当前参数、模拟周期、小角度公式周期和偏差加入表格。任务进度只接受与当前任务预设匹配的新记录。\n导出CSV：将表格中的全部记录保存到你选择的位置，可用Excel等软件打开。',
          '記錄本次實驗：週期測得後，將目前參數、模擬週期、小角度公式週期和偏差加入表格。任務進度只接受與目前任務預設相符的新記錄。\n匯出CSV：將表格中的全部記錄儲存到你選擇的位置，可用Excel等軟體開啟。',
          'Record experiment adds the current parameters, simulated period, small-angle period and deviation to the table once a period is available. Task progress accepts only new records matching the selected task presets.\nExport CSV saves every table record to a location you choose, for use in Excel or other software.')),
        (('清空记录', '清空記錄', 'Clear records'),
         ('清除整个实验表格，同时清除四个任务的数据进度和完成标记。预测与结论文字会保留，卷二已锁定的预测仍然锁定。需要保留数据时，请先导出。',
          '清除整個實驗表格，同時清除四個任務的資料進度和完成標記。預測與結論文字會保留，卷二已鎖定的預測仍然鎖定。需要保留資料時，請先匯出。',
          'Clear the whole experiment table and all four tasks’ data progress and completion marks. Written predictions and conclusions remain; a locked Folio II prediction stays locked. Export first if you need to keep your data.')),
        (('语言按钮、页面与F1', '語言按鈕、頁面與F1', 'Language buttons, pages and F1'),
         ('简中／繁中／English：切换界面与本指引的语言，保留当前实验、记录和任务进度；不会翻译你自己填写的文字。\n点击顶部页签切换工作区，或按F1打开本指引。切换页签本身不会暂停或重置运动。',
          '簡中／繁中／English：切換介面與本指引的語言，保留目前實驗、記錄和任務進度；不會翻譯你自己填寫的文字。\n點擊頂部分頁切換工作區，或按F1開啟本指引。切換分頁本身不會暫停或重設運動。',
          '简中 / 繁中 / English changes the interface and guide language while keeping your experiment, records and task progress. Your own writing is not translated.\nUse the top tabs to change workspaces, or press F1 to open this guide. Changing tabs alone does not pause or reset motion.')),
    ]),
    (('3. 任务清单指引', '3. 任務清單指引', '3. Task checklist'), [
        (('每个任务的操作顺序', '每個任務的操作順序', 'The workflow for every task'),
         ('① 在探究卷册点击一张任务卡。\n② 阅读说明并填写预测；卷二为必填，首次开始或单步后锁定。\n③ 点击一组参数预设，自动跳到实验工坊；再点开始。\n④ 周期出现后点“记录本次实验”。\n⑤ 返回卷册，检查对应参数组是否出现勾选；重复③④直到全部记录。\n⑥ 引用数据填写结论，点击“检查并完成当前任务”，最后导出任务报告。',
          '① 在探究卷冊點擊一張任務卡。\n② 閱讀說明並填寫預測；卷二為必填，首次開始或單步後鎖定。\n③ 點擊一組參數預設，自動跳到實驗工坊；再點開始。\n④ 週期出現後點「記錄本次實驗」。\n⑤ 返回卷冊，檢查對應參數組是否出現勾選；重複③④直到全部記錄。\n⑥ 引用資料填寫結論，點擊「檢查並完成目前任務」，最後匯出任務報告。',
          '1. Click a task card in Inquiry folios.\n2. Read the instructions and enter a prediction. It is required in Folio II and locks on the first start or step.\n3. Click a parameter preset to open The workshop, then click Start.\n4. Once a period appears, click Record experiment.\n5. Return to the folio and check that the matching set is ticked. Repeat steps 3–4 for all sets.\n6. Write a conclusion using your data, click Check and complete task, then export the task report.')),
        (('卷一 · 寻找规律', '卷一 · 尋找規律', 'Folio I · Find patterns'),
         ('固定10°和地球重力9.81 m/s²，依次记录0.25、0.5、1、1.5、2 m共五种摆长的周期。结论要说明摆长增加时周期怎样变化，并引用至少两组数据。',
          '固定10°和地球重力9.81 m/s²，依次記錄0.25、0.5、1、1.5、2 m共五種擺長的週期。結論要說明擺長增加時週期怎樣變化，並引用至少兩組資料。',
          'Keep the angle at 10° and Earth gravity at 9.81 m/s². Record periods for five lengths: 0.25, 0.5, 1, 1.5 and 2 m. Explain how period changes with length, citing at least two data sets.')),
        (('卷二 · 检验猜想', '卷二 · 檢驗猜想', 'Folio II · Test a prediction'),
         ('先预测：摆长从0.25 m变为1 m（四倍），周期会变为几倍？写下理由，再运行两组实验，保持10°和地球重力不变。数据齐全后会显示第二组／第一组的周期比，用它检验原来的预测。卷一的旧数据不会自动计入卷二。',
          '先預測：擺長從0.25 m變為1 m（四倍），週期會變為幾倍？寫下理由，再執行兩組實驗，保持10°和地球重力不變。資料齊全後會顯示第二組／第一組的週期比，用它檢驗原來的預測。卷一的舊資料不會自動計入卷二。',
          'First predict the period ratio when length increases from 0.25 m to 1 m (four times), and explain why. Then run both sets at 10° and Earth gravity. Once both are recorded, compare the displayed second/first period ratio with your original prediction. Old Folio I data do not automatically count towards Folio II.')),
        (('卷三 · 审视模型', '卷三 · 審視模型', 'Folio III · Evaluate the model'),
         ('固定1 m和地球重力，依次记录5°、15°、30°、60°。比较模拟周期与小角度公式的偏差，找出已测角度中首次超过2%的角度。这是课堂判据，并非通用物理边界；还可以自行测试中间角度，细化范围。',
          '固定1 m和地球重力，依次記錄5°、15°、30°、60°。比較模擬週期與小角度公式的偏差，找出已測角度中首次超過2%的角度。這是課堂判據，並非通用物理邊界；還可以自行測試中間角度，細化範圍。',
          'Keep length at 1 m and Earth gravity. Record 5°, 15°, 30° and 60°. Compare simulated and small-angle periods and find the first tested angle with deviation above 2%. This is a classroom criterion, not a universal boundary. Try intermediate angles to narrow the range.')),
        (('卷四 · 两地之摆', '卷四 · 兩地之擺', 'Folio IV · Earth and Moon'),
         ('固定1 m和10°，记录地球g=9.81与月球g=1.62 m/s²两组数据。比较周期比，并解释重力变化对摆动快慢的影响。',
          '固定1 m和10°，記錄地球g=9.81與月球g=1.62 m/s²兩組資料。比較週期比，並解釋重力變化對擺動快慢的影響。',
          'Keep length at 1 m and angle at 10°. Record Earth gravity g=9.81 and Moon gravity g=1.62 m/s². Compare the period ratio and explain how gravity affects the motion.')),
        (('进度、完成印章与自由实验', '進度、完成印章與自由實驗', 'Progress, completion seals and free exploration'),
         ('任务卡的“已记录／所需组数”只统计不同的预设参数组；重复记录同一组会更新该组数据，不会增加组数。\n全部组数齐全且结论非空，才会出现完成印章；印章表示已提交，不代表程序判断结论正确。\n“自由实验模式”退出当前任务并暂停运动；自由实验记录不会计入任何任务。选择另一卷也会暂停并重置当前模拟，但保留已有记录。',
          '任務卡的「已記錄／所需組數」只統計不同的預設參數組；重複記錄同一組會更新該組資料，不會增加組數。\n全部組數齊全且結論非空，才會出現完成印章；印章表示已提交，不代表程式判斷結論正確。\n「自由實驗模式」退出目前任務並暫停運動；自由實驗記錄不會計入任何任務。選擇另一卷也會暫停並重設目前模擬，但保留已有記錄。',
          'The recorded/required count tracks distinct preset sets. Recording the same set again updates its evidence without increasing the count.\nThe seal appears only after all sets are recorded and a non-empty conclusion is submitted. It indicates submission, not automatic grading of your conclusion.\nFree exploration exits the current task and pauses motion; its records do not count towards tasks. Choosing another folio also pauses and resets the current simulation while keeping existing records.')),
    ]),
    (('4. 读懂实验结果', '4. 讀懂實驗結果', '4. Reading results'), [
        (('时间、当前角度与曲线', '時間、目前角度與曲線', 'Time, angle and trace'),
         ('时间使用模拟秒；当前角度带正负号，表示摆球位于平衡位置的两侧。曲线只显示最近15秒，观察相邻波峰之间的时间可帮助理解周期。',
          '時間使用模擬秒；目前角度帶正負號，表示擺球位於平衡位置的兩側。曲線只顯示最近15秒，觀察相鄰波峰之間的時間可幫助理解週期。',
          'Time is measured in simulation seconds. The angle’s sign indicates the side of equilibrium. The trace shows the most recent 15 seconds. The interval between consecutive peaks helps you understand the period.')),
        (('为什么显示“等待测量”', '為甚麼顯示「等待測量」', 'Why does it say Awaiting measurement?'),
         ('程序根据连续两次从右向左经过平衡位置的时间差测量周期，所以刚开始时还没有读数。保持运行，直到出现模拟周期再记录。重置或调整参数后需要重新等待；较长的摆或月球重力下通常要等更久。',
          '程式根據連續兩次從右向左經過平衡位置的時間差測量週期，所以剛開始時還沒有讀數。保持執行，直到出現模擬週期再記錄。重設或調整參數後需要重新等待；較長的擺或月球重力下通常要等更久。',
          'A period is measured between two consecutive right-to-left equilibrium crossings, so no reading is available immediately. Keep running until one appears, then record it. After a reset or parameter change, wait again. Longer pendulums and Moon gravity generally need more time.')),
        (('完整周期数', '完整週期數', 'Full-cycle count'),
         ('按相邻同向过零之间的完整区间计数，并非从释放瞬间开始计数；因此它可能比直观上从释放开始数的摆动次数少。',
          '按相鄰同向過零之間的完整區間計數，並非從釋放瞬間開始計數；因此它可能比直觀上從釋放開始數的擺動次數少。',
          'The count tracks completed intervals between same-direction zero crossings, not cycles counted from the release instant. It may therefore lag a visual count started at release.')),
        (('模拟周期、小角度公式与偏差', '模擬週期、小角度公式與偏差', 'Simulated period, small-angle formula and deviation'),
         ('模拟周期来自非线性单摆运动；小角度对照公式为T₀=2π√(L/g)。表格偏差=(模拟周期−T₀)/T₀×100%。大角度下两者可能不同，这反映模型近似的适用条件，不是对真实实验测量误差的统计。',
          '模擬週期來自非線性單擺運動；小角度對照公式為T₀=2π√(L/g)。表格偏差=(模擬週期−T₀)/T₀×100%。大角度下兩者可能不同，這反映模型近似的適用條件，不是對真實實驗測量誤差的統計。',
          'The simulated period comes from nonlinear pendulum motion. The small-angle reference is T₀=2π√(L/g). Deviation=(simulated period−T₀)/T₀×100%. Differences at larger angles show the limits of the approximation; they are not measured real-world experimental errors.')),
    ]),
    (('5. 保存与常见问题', '5. 儲存與常見問題', '5. Saving and questions'), [
        (('CSV和任务报告分别保存什么', 'CSV和任務報告分別儲存甚麼', 'What do CSV and the task report save?'),
         ('“导出CSV”保存实验表格中全部参数和周期记录，适合继续绘图分析。\n“导出任务报告”保存四卷的预测、结论、完成状态和分任务数据，格式为JSON。两者均让你选择保存位置；建议使用能区分学生或小组的文件名。',
          '「匯出CSV」儲存實驗表格中全部參數和週期記錄，適合繼續繪圖分析。\n「匯出任務報告」儲存四卷的預測、結論、完成狀態和分任務資料，格式為JSON。兩者均讓你選擇儲存位置；建議使用能區分學生或小組的檔名。',
          'Export CSV saves every parameter and period record in the table for further plotting and analysis.\nExport task report saves all four folios’ predictions, conclusions, completion status and task-specific data as JSON. Both let you choose a save location. Use filenames that identify the student or group.')),
        (('关闭后能否继续原来的进度', '關閉後能否繼續原來的進度', 'Can I resume after closing?'),
         ('当前版本不自动保存，也不能导入任务报告恢复进度。关闭前请导出CSV和JSON，保留本次学习成果；重新启动会从空记录开始。',
          '目前版本不自動儲存，也不能匯入任務報告恢復進度。關閉前請匯出CSV和JSON，保留本次學習成果；重新啟動會從空記錄開始。',
          'This version does not autosave or import task reports to restore progress. Export CSV and JSON before closing to keep your work. A new launch starts with empty records.')),
        (('为什么记录了却没有增加任务进度', '為甚麼記錄了卻沒有增加任務進度', 'Why did my record not increase task progress?'),
         ('检查是否先选择了正确任务，以及摆长、初始角度、重力是否与该任务预设完全匹配。建议直接点击预设按钮。旧任务或自由实验数据不会自动转入当前任务；同一参数组重复记录也不会增加组数。',
          '檢查是否先選擇了正確任務，以及擺長、初始角度、重力是否與該任務預設完全相符。建議直接點擊預設按鈕。舊任務或自由實驗資料不會自動轉入目前任務；同一參數組重複記錄也不會增加組數。',
          'Check that the correct task is selected and that length, initial angle and gravity match its preset exactly. Use preset buttons for accuracy. Old-task and free-exploration records do not transfer automatically, and repeated records of one set do not increase the count.')),
        (('为什么预测不能修改，或任务无法完成', '為甚麼預測不能修改，或任務無法完成', 'Why is my prediction locked, or my task incomplete?'),
         ('卷二首次开始或单步后会锁定原预测，请在结论中比较结果并说明是否改变想法。若任务无法完成，先检查所有预设参数组是否已记录、结论是否已填写，再点击完成按钮。程序不会自动判断结论的科学正确性。',
          '卷二首次開始或單步後會鎖定原預測，請在結論中比較結果並說明是否改變想法。若任務無法完成，先檢查所有預設參數組是否已記錄、結論是否已填寫，再點擊完成按鈕。程式不會自動判斷結論的科學正確性。',
          'Folio II locks the original prediction on the first start or step. Compare it with your results in the conclusion and explain any change of mind. For an incomplete task, check that every preset is recorded and your conclusion is filled in, then click the completion button. Scientific correctness is not graded automatically.')),
        (('窗口较小时怎样查看内容', '視窗較小時怎樣查看內容', 'How do I read content in a smaller window?'),
         ('可以放大窗口；探究卷册右侧和本指引均可使用滚动条或鼠标滚轮。指引文字可选中并复制。底部“前往实验工坊／前往探究卷册”只切换页面，不会替你加载参数或清空数据。',
          '可以放大視窗；探究卷冊右側和本指引均可使用捲動條或滑鼠滾輪。指引文字可選取並複製。底部「前往實驗工坊／前往探究卷冊」只切換頁面，不會替你載入參數或清空資料。',
          'Enlarge the window or use the scrollbar or mouse wheel in the folio detail area and this guide. Guide text can be selected and copied. Go to workshop / Go to inquiry folios only changes tabs; these buttons do not load parameters or clear data.')),
    ]),
]


def localized(texts, language):
    return texts[LANGUAGES[language]]


def markdown(language='zh-CN'):
    """Generate the offline handbook from the same content as the in-app guide."""
    lines = ['# '+localized(GUIDE_UI['如何使用这个项目'], language), '']
    for title, blocks in GUIDE_SECTIONS:
        lines.extend(['## '+localized(title, language), ''])
        for heading, body in blocks:
            lines.extend(['### '+localized(heading, language), '', localized(body, language), ''])
    return '\n'.join(lines)
