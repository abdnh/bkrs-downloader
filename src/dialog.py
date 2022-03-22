from typing import List

from aqt.qt import *
from aqt.main import AnkiQt
from aqt.utils import showWarning
from anki.notes import Note
from aqt.operations import QueryOp

from .form import Ui_Dialog
from .consts import *
from .bkrs_downloader import BkrsDownloader
from .yellowbridge_downloader import YellowBridgeDownloader

PROGRESS_LABEL = "Updated {count} out of {total} note(s)"


class BkrsDownloaderDialog(QDialog):
    def __init__(
        self,
        mw: AnkiQt,
        parent,
        bkrs_downloader: BkrsDownloader,
        yellowbridge_downloader: YellowBridgeDownloader,
        notes: List[Note],
    ):
        super().__init__(parent)
        self.form = Ui_Dialog()
        self.form.setupUi(self)
        self.mw = mw
        self.bkrs_downloader = bkrs_downloader
        self.yellowbridge_downloader = yellowbridge_downloader
        self.config = mw.addonManager.getConfig(__name__)
        self.highlight_color = self.config["highlight_color"].strip()
        self.notes = notes
        self.combos = [
            self.form.wordFieldComboBox,
            self.form.definitionFieldComboBox,
            self.form.exampleFieldComboBox,
            self.form.headTailWordFieldComboBox,
        ]
        self.setWindowTitle(ADDON_NAME)
        self.form.icon.setPixmap(
            QPixmap(os.path.join(ICONS_DIR, "favicon-194x194.png"))
        )
        self.form.numberOfDefinitionsSpinBox.setValue(
            int(self.config["number_of_definitions"])
        )
        qconnect(
            self.form.numberOfDefinitionsSpinBox.valueChanged,
            self.on_number_of_defs_changed,
        )
        self.form.numberOfExamplesSpinBox.setValue(
            int(self.config["number_of_examples"])
        )
        qconnect(
            self.form.numberOfExamplesSpinBox.valueChanged,
            self.on_number_of_examples_changed,
        )
        qconnect(
            self.form.numberOfDefinitionsCheckBox.stateChanged,
            lambda s: self.form.numberOfDefinitionsSpinBox.setEnabled(s),
        )
        qconnect(
            self.form.numberOfExamplesCheckBox.stateChanged,
            lambda s: self.form.numberOfExamplesSpinBox.setEnabled(s),
        )

        self._fill_fields()
        qconnect(self.form.addButton.clicked, self.on_add)

    def _fill_fields(self):
        mids = set(note.mid for note in self.notes)
        if len(mids) > 1:
            showWarning(
                "Please select notes from only one notetype.",
                parent=self,
                title=ADDON_NAME,
            )
            self.done(0)
            return
        self.field_names = ["None"] + self.notes[0].keys()
        for i, combo in enumerate(self.combos):
            combo.addItems(self.field_names)
            selected = 0
            if len(self.field_names) - 1 > i:
                selected = i + 1
            combo.setCurrentIndex(selected)
            qconnect(
                combo.currentIndexChanged,
                lambda field_index, combo_index=i: self.on_selected_field_changed(
                    combo_index, field_index
                ),
            )

    def on_selected_field_changed(self, combo_index, field_index):
        if field_index == 0:
            return
        for i, combo in enumerate(self.combos):
            if i != combo_index and combo.currentIndex() == field_index:
                combo.setCurrentIndex(0)

    def on_number_of_defs_changed(self, value: int):
        self.config["number_of_definitions"] = value
        self.mw.addonManager.writeConfig(__name__, self.config)

    def on_number_of_examples_changed(self, value: int):
        self.config["number_of_examples"] = value
        self.mw.addonManager.writeConfig(__name__, self.config)

    def on_add(self):
        if self.form.wordFieldComboBox.currentIndex == 0:
            self.done(0)
            return

        if self.form.wordFieldComboBox.currentIndex() == 0:
            showWarning("No word field selected.", parent=self, title=ADDON_NAME)
            return
        word_field = self.form.wordFieldComboBox.currentText()
        definition_field_i = self.form.definitionFieldComboBox.currentIndex()
        example_field_i = self.form.exampleFieldComboBox.currentIndex()
        head_tail_word_field_i = self.form.headTailWordFieldComboBox.currentIndex()

        def on_success(ret):
            if len(self.updated_notes) > 0:
                self.done(1)
            else:
                self.done(0)

        op = QueryOp(
            parent=self,
            op=lambda col: self._fill_notes(
                word_field,
                definition_field_i,
                example_field_i,
                head_tail_word_field_i,
            ),
            success=on_success,
        )
        self.mw.progress.start(
            max=len(self.notes),
            label=PROGRESS_LABEL.format(count=0, total=len(self.notes)),
            parent=self,
            immediate=True,
        )
        self.mw.progress.set_title(ADDON_NAME)
        op.run_in_background()

    def _fill_notes(
        self,
        word_field,
        definition_field_i,
        example_field_i,
        head_tail_word_field_i,
    ):
        self.errors = []
        self.updated_notes = []
        for note in self.notes:
            word = note[word_field]
            try:
                need_updating = False
                if definition_field_i:
                    definitions = self._get_definitions(word)
                    note[self.field_names[definition_field_i]] = definitions
                    need_updating = True
                if example_field_i:
                    examples = self._get_examples(word)
                    note[self.field_names[example_field_i]] = examples
                    need_updating = True
                if head_tail_word_field_i:
                    note[
                        self.field_names[head_tail_word_field_i]
                    ] = self._get_head_tail_words(word)
                    need_updating = True
            except Exception as exc:
                self.mw.taskman.run_on_main(lambda: self.mw.progress.finish())
                showWarning(str(exc), parent=self, title=ADDON_NAME)
                return
            finally:
                if need_updating:
                    self.updated_notes.append(note)
                    self.mw.taskman.run_on_main(
                        lambda: self.mw.progress.update(
                            label=PROGRESS_LABEL.format(
                                count=len(self.updated_notes), total=len(self.notes)
                            ),
                            value=len(self.updated_notes),
                            max=len(self.notes),
                        )
                    )
        self.mw.taskman.run_on_main(lambda: self.mw.progress.finish())

    def _get_definitions(self, word: str) -> str:
        field_contents = []
        defs = self.bkrs_downloader.get_definitions(word)
        for definition in defs[
            : self.form.numberOfDefinitionsSpinBox.value()
            if self.form.numberOfDefinitionsCheckBox.isChecked()
            else len(defs)
        ]:
            field_contents.append(definition)
        return "<br>".join(field_contents)

    def _get_examples(self, word: str) -> str:
        field_contents = []
        examples = self.bkrs_downloader.get_examples(word, self.highlight_color)
        for example in examples[
            : self.form.numberOfExamplesSpinBox.value()
            if self.form.numberOfExamplesCheckBox.isChecked()
            else len(examples)
        ]:
            field_contents.append(example)
        return "<br>".join(field_contents)

    # def _get_head_words(self, word: str) -> str:
    #     return self.yellowbridge_downloader.get_words_with_same_head(word)

    # def _get_tail_words(self, word: str) -> str:
    #     return self.yellowbridge_downloader.get_words_with_same_tail(word)

    def _get_head_tail_words(self, word: str) -> str:
        # <div style="width: 790px; margin: 5px auto;">
        contents = '<div style="width: 790px; margin: 5px auto;">'
        head = self.yellowbridge_downloader.get_words_with_same_head(word)
        tail = self.yellowbridge_downloader.get_words_with_same_tail(word)
        contents += head
        contents += tail
        contents += "</div>"
        if not (head or tail):
            return ""
        # <style> doesn't work in latest versions
        #         contents += """
        #             <style>
        #             #sameHead {
        #   float: left;
        #   width: 380px;
        #   margin: 5px 0 0 5px;
        # }

        # table.grid {
        #   border-style: none;
        #   border-collapse: collapse;
        #   background: white;
        #   margin: 5px auto;
        #   padding: 0;
        # }

        # TABLE {
        #   border-spacing: 1px;
        #   border-width: 1px;
        # }

        # #sameTail {
        #   float: right;
        #   width: 380px;
        #   margin: 5px 5px 0 0;
        # }

        # TABLE.grid CAPTION {
        #   font-size: 1.0;
        #   font-weight: bold;
        #   padding: 4px 5px 3px 5px;
        #   color: #009;
        #   background: #fc0;
        #   border-style: none;
        #   border-radius: 5px 5px 0 0;
        # }
        #             </style>
        #         """
        return contents

    # def _get_head_words(self, word: str) -> str:
    #     field_contents = "<table><tbody>"
    #     rows = self.yellowbridge_downloader.get_words_with_same_head(word)
    #     if not rows:
    #         return ""
    #     for row in rows:
    #         field_contents += row
    #     field_contents += "</tbody></table>"
    #     return field_contents

    # def _get_tail_words(self, word: str) -> str:
    #     field_contents = "<table><tbody>"
    #     rows = self.yellowbridge_downloader.get_words_with_same_tail(word)
    #     if not rows:
    #         return ""
    #     for row in rows:
    #         field_contents += row
    #     field_contents += "</tbody></table>"
    #     return field_contents
