import json
import random
from typing import List

import aqt
from aqt.browser.browser import Browser
from aqt.editor import Editor
from aqt.gui_hooks import browser_menus_did_init, editor_did_init_buttons
from aqt.operations import CollectionOp
from aqt.qt import *
from aqt.utils import showText, showWarning, tooltip

from .bkrs_downloader import BkrsDownloader
from .consts import *
from .dialog import BkrsDownloaderDialog
from .yellowbridge_downloader import YellowBridgeDownloader

bkrs_downloader = BkrsDownloader()
yellowbridge_downloader = YellowBridgeDownloader()


def on_bulk_updated_notes(browser: Browser, updated_count: int) -> None:
    if updated_count:
        tooltip(f"Updated {updated_count} note(s).", parent=browser)


def on_browser_action_triggered(browser: Browser) -> None:
    notes = [browser.mw.col.get_note(nid) for nid in browser.selected_notes()]
    dialog = BkrsDownloaderDialog(
        browser.mw, browser, bkrs_downloader, yellowbridge_downloader, notes
    )
    if dialog.exec():
        updated_notes = dialog.updated_notes
        CollectionOp(
            parent=browser,
            op=lambda col: col.update_notes(updated_notes),
        ).success(
            lambda out: on_bulk_updated_notes(browser, len(updated_notes)),
        ).run_in_background()


def on_browser_menus_did_init(browser: Browser) -> None:
    action = QAction("Bulk-define using Bkrs Downloader", browser)
    qconnect(action.triggered, lambda: on_browser_action_triggered(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(action)


def on_editor_button_clicked(editor: Editor, highlight_color: str) -> None:
    def lookup_selection(text: str) -> None:
        text = text.strip()
        if not text:
            return
        try:
            examples = bkrs_downloader.get_examples(text, highlight_color)
        except Exception as exc:
            showWarning(str(exc), title=ADDON_NAME)
            return
        example = (
            text + "<br><br>" + examples[random.randrange(0, len(examples))]
            if examples
            else text
        )
        editor.web.eval(
            f"document.execCommand('inserthtml', false, {json.dumps(example)});"
        )

    editor.web.evalWithCallback("getSelection().toString()", lookup_selection)

    #     dialog = BkrsDownloaderDialog(
    #         editor.mw, editor.parentWindow, downloader, [editor.note]
    #     )
    #     if dialog.exec():
    #         editor.loadNoteKeepingFocus()


def on_editor_did_init_buttons(buttons: List[str], editor: Editor) -> None:
    config = aqt.mw.addonManager.getConfig(__name__)
    shortcut = config["shortcut"]
    button = editor.addButton(
        icon=os.path.join(ICONS_DIR, "favicon-32x32.png"),
        cmd="bkrs_downloader",
        tip=f"{ADDON_NAME} ({shortcut})" if shortcut else ADDON_NAME,
        func=lambda e: on_editor_button_clicked(e, config["highlight_color"]),
        keys=shortcut,
    )
    buttons.append(button)


browser_menus_did_init.append(on_browser_menus_did_init)
editor_did_init_buttons.append(on_editor_did_init_buttons)
