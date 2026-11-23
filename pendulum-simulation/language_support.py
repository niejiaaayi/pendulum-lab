"""Local UI translations; no external dependencies or machine-specific paths."""
import json
from pathlib import Path

CATALOG = json.loads(Path(__file__).with_name('translations.json').read_text(encoding='utf-8'))


def translate(text, language):
    return CATALOG.get(language, {}).get(text, text)


def capture_widgets(root):
    items = []
    def walk(widget):
        if 'text' in widget.keys() and not ('textvariable' in widget.keys() and widget.cget('textvariable')):
            text = str(widget.cget('text'))
            if text:
                items.append((widget, text))
        for child in widget.winfo_children():
            walk(child)
    walk(root)
    return items
