from typing import List
import json
import random


from aqt.gui_hooks import (
    browser_menus_did_init,
    editor_did_init_buttons,
)
import aqt
from aqt.qt import *
from aqt.browser.browser import Browser
from aqt.editor import Editor
from aqt.utils import showText, tooltip, showWarning
from aqt.operations import CollectionOp

from .consts import *
from .dialog import BkrsDownloaderDialog
from .bkrs_downloader import BkrsDownloader
from .yellowbridge_downloader import YellowBridgeDownloader

bkrs_downloader = BkrsDownloader()
yellowbridge_downloader = YellowBridgeDownloader()


def on_bulk_updated_notes(browser: Browser, errors: List[str], updated_count: int):
    # browser.mw.progress.finish()
    msg = f"Updated {updated_count} note(s)."
    if errors:
        msg += " The following issues happened during the process:\n"
        msg += "\n".join(errors)
        showText(msg, parent=browser, title=ADDON_NAME)
    else:
        tooltip(msg, parent=browser)


def on_browser_action_triggered(browser: Browser) -> None:
    notes = [browser.mw.col.get_note(nid) for nid in browser.selected_notes()]
    dialog = BkrsDownloaderDialog(
        browser.mw, browser, bkrs_downloader, yellowbridge_downloader, notes
    )
    if dialog.exec():
        updated_notes = dialog.updated_notes
        errors = dialog.errors
        CollectionOp(
            parent=browser,
            op=lambda col: col.update_notes(updated_notes),
        ).success(
            lambda out: on_bulk_updated_notes(browser, errors, len(updated_notes)),
        ).run_in_background()


def on_browser_menus_did_init(browser: Browser):
    a = QAction("Bulk-define using Bkrs Downloader", browser)
    qconnect(a.triggered, lambda: on_browser_action_triggered(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)


def on_editor_button_clicked(editor: Editor, highlight_color: str) -> None:
    def cb(text: str):
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
            "document.execCommand('inserthtml', false, {});".format(json.dumps(example))
        )

    editor.web.evalWithCallback("getSelection().toString()", cb)

    #     dialog = BkrsDownloaderDialog(
    #         editor.mw, editor.parentWindow, downloader, [editor.note]
    #     )
    #     if dialog.exec():
    #         editor.loadNoteKeepingFocus()


def on_editor_did_init_buttons(buttons: List[str], editor: Editor):
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
