"""Desktop entry point, including an optional packaged-runtime verification."""
import json
import sys
import tkinter as tk
from pathlib import Path

from workshop import Workshop


def main():
    root = tk.Tk()
    checking = len(sys.argv) == 3 and sys.argv[1] == '--self-test'
    if checking:
        root.withdraw()
    app = Workshop(root)
    if not checking:
        root.mainloop()
        return
    errors = []
    root.report_callback_exception = lambda kind, error, trace: errors.append(str(error))
    root.update()
    app.folio_cards[0].choose()
    root.update()
    app.load_case((1, 10, 9.81))
    app.advance(8)
    app.record()
    assert app.model.period and len(app.records) == 1
    assert len(app.task_records[0]) == 1
    for language in ('en', 'zh-TW', 'zh-CN'):
        app.switch_language(language)
        app.show_guide()
        for index in range(app.guide_nav.size()):
            app.guide_index = index
            app.render_guide()
            assert len(app.guide_body.get('1.0', 'end').strip()) > 100
        assert app.notebook.select() == str(app.guide_tab)
    assert len(app.records) == 1 and not errors
    Path(sys.argv[2]).write_text(json.dumps({
        'passed': True, 'frozen': bool(getattr(sys, 'frozen', False)),
        'title': root.title(), 'period': app.model.period,
        'records': len(app.records), 'languages': 3,
        'guide_chapters': app.guide_nav.size(),
        'runtime': sys.prefix, 'callback_errors': errors,
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    for callback in root.tk.call('after', 'info'):
        root.after_cancel(callback)
    root.destroy()


if __name__ == '__main__':
    main()
