"""Standard-library integration checks: python -m unittest test_workshop.py."""
import hashlib
import json
import tempfile
import tkinter as tk
import unittest
from pathlib import Path
from unittest.mock import patch

from workshop import Workshop
from user_guide import GUIDE_SECTIONS


class WorkshopTests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.errors = []
        self.root.report_callback_exception = lambda kind, error, trace: self.errors.append(error)
        self.app = Workshop(self.root)
        self.root.update()

    def tearDown(self):
        for callback in self.root.tk.call('after', 'info'):
            self.root.after_cancel(callback)
        self.root.destroy()
        self.assertEqual(self.errors, [], 'Tkinter callbacks must not fail silently')

    def select(self, index):
        self.app.folio_cards[index].choose()
        self.root.update()
        self.assertEqual(self.app.active_task, index)

    def measure(self, case):
        self.app.load_case(case)
        self.app.advance(12)
        self.app.record()

    def test_all_folios_and_completion(self):
        app = self.app
        for i, (_, cases, _) in enumerate(app.TASKS):
            self.select(i)
            self.assertEqual(len(app.preset_frame.grid_slaves()), len(cases))
            if i == 1:
                with patch('core.messagebox.showinfo') as prompt:
                    app.toggle()
                    self.assertFalse(app.running)
                    prompt.assert_called_once()
                app.predictions[i].set('Period doubles')
                app.toggle()
                app.toggle()
                self.assertTrue(app.prediction_locked)
            for case in cases:
                self.measure(case)
            self.assertEqual(len(app.task_records[i]), len(cases))
            app.conclusions[i].set('Evidence-based conclusion')
            app.complete_task()
            self.assertTrue(app.task_done[i])
        self.assertTrue(all(app.task_done))
        app.clear_records()
        self.assertFalse(any(app.task_records))
        self.assertFalse(any(app.task_done))

    def test_language_and_exports_preserve_state(self):
        app = self.app
        self.select(1)
        app.predictions[1].set('周期变为2倍')
        app.toggle()
        app.running = False
        for case in app.TASKS[1][1]:
            self.measure(case)
        app.conclusions[1].set('由数据可知周期约变为2倍')
        app.complete_task()
        snapshot = (app.model.t, list(app.records), dict(app.task_records[1]))
        app.running = True
        for language in ('en', 'zh-TW', 'zh-CN', 'en'):
            app.switch_language(language)
            self.assertEqual(snapshot, (app.model.t, app.records, app.task_records[1]))
            self.assertTrue(app.running)
            self.assertEqual(str(app.prediction_entry.cget('state')), 'readonly')
        self.assertEqual(app.tr('学者工坊'), "Scholar's Workshop")
        self.assertEqual(app.predictions[1].get(), '周期变为2倍')
        self.assertIn('Simulated period:', app.metrics.get() or app.tr('模拟周期：'))
        with tempfile.TemporaryDirectory() as folder:
            report, data = Path(folder)/'report.json', Path(folder)/'data.csv'
            with patch('core.filedialog.asksaveasfilename', side_effect=[str(report), str(data)]):
                app.export_tasks()
                app.export()
            self.assertEqual(json.loads(report.read_text(encoding='utf-8'))['Task'][1]['Prediction'], '周期变为2倍')
            self.assertIn('Length(m)', data.read_text(encoding='utf-8-sig'))
        app.free_mode()
        self.root.update()
        app.sliders[0].key_value(.5)
        self.assertEqual(app.model.length, .5)
        self.assertIsNone(app.active_task)

    def test_original_files_unchanged(self):
        folder = Path(__file__).resolve().parent
        hashes = json.loads((folder/'original_hashes.json').read_text(encoding='utf-8'))
        for filename, expected in hashes.items():
            self.assertEqual(hashlib.sha256((folder.parent/filename).read_bytes()).hexdigest(), expected)

    def test_guide_navigation_preserves_experiment_and_prediction(self):
        app = self.app
        self.select(1)
        app.predictions[1].set('周期将变为2倍')
        app.toggle()
        app.running = False
        self.measure(app.TASKS[1][1][0])
        app.conclusions[1].set('待完成第二组后比较')
        snapshot = (app.model.t, list(app.records), dict(app.task_records[1]), app.active_task)
        app.running = True
        app.show_guide()
        self.assertEqual(app.notebook.select(), str(app.guide_tab))
        # Chapter selection and language changes must not start a fresh experiment.
        app.guide_nav.selection_clear(0, 'end')
        app.guide_nav.selection_set(2)
        app.choose_guide_section()
        for language in ('en', 'zh-TW', 'zh-CN'):
            app.switch_language(language)
            self.assertEqual(app.guide_index, 2)
            self.assertEqual(app.guide_nav.curselection(), (2,))
            self.assertEqual(snapshot, (app.model.t, app.records, app.task_records[1], app.active_task))
            self.assertTrue(app.running)
            self.assertEqual(str(app.prediction_entry.cget('state')), 'readonly')
            self.assertEqual(str(app.guide_body.cget('state')), 'disabled')
            for index, (_, blocks) in enumerate(GUIDE_SECTIONS):
                app.guide_index = index
                app.render_guide()
                self.assertGreater(len(app.guide_body.get('1.0', 'end').strip()), 100)
                self.assertTrue(all(all(part.strip() for part in heading+body) for heading, body in blocks))
            app.guide_index = 2
        for button, tab in zip(app.guide_actions, (app.lab_tab, app.task_tab)):
            button.invoke()
            self.assertEqual(app.notebook.select(), str(tab))
            self.assertEqual(snapshot, (app.model.t, app.records, app.task_records[1], app.active_task))
        self.assertEqual(app.predictions[1].get(), '周期将变为2倍')
        self.assertEqual(app.conclusions[1].get(), '待完成第二组后比较')
        app.running = False
        self.root.update()


if __name__ == '__main__':
    unittest.main()
