# ```text
# Copyright (c) 2025 Sam Afzali

# Permission is granted to use, copy, and distribute this software for personal, educational, and non-commercial purposes, provided the original author (Sam Afzali) is credited.

# Modification, resale, commercial use, or claiming authorship of the code is strictly prohibited.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.


from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QSizePolicy, QComboBox
)
from PyQt5.QtGui import QFont, QColor, QPainter, QPolygon, QBrush
from PyQt5.QtCore import Qt, QPoint
from deep_translator import GoogleTranslator
import sys

class ArrowLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(24, 24)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor("#0ea480")))
        painter.setPen(Qt.NoPen)
        points = QPolygon([
            QPoint(6, 9),
            QPoint(18, 9),
            QPoint(12, 16)
        ])
        painter.drawPolygon(points)


class ComboWithArrow(QWidget):
    def __init__(self, items=None):
        super().__init__()
        self.setFixedHeight(36)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.combo = QComboBox()
        self.combo.setStyleSheet("""
            QComboBox {
                border: 1.5px solid #0ea480;
                border-radius: 12px;
                padding-left: 10px;
                padding-right: 36px;
                background-color: white;
                font-size: 12pt;
                color: #333;
                qproperty-icon: none;
            }
            QComboBox::drop-down {
                width: 0px;
                border: none;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #0ea480;
                background-color: white;
                font-size: 11pt;
                selection-background-color: #0ea480;
                selection-color: white;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 10px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #a3d8c8;
                color: #0a6040;
            }
        """)

        if items:
            self.combo.addItems(items)

        self.arrow = ArrowLabel()
        self.arrow.mousePressEvent = self.open_combo

        layout.addWidget(self.combo)
        layout.addWidget(self.arrow)
        self.setLayout(layout)

    def open_combo(self, event):
        self.combo.showPopup()

    def currentText(self):
        return self.combo.currentText()

    def setCurrentText(self, text):
        index = self.combo.findText(text)
        if index >= 0:
            self.combo.setCurrentIndex(index)

    def addItems(self, items):
        self.combo.addItems(items)

    def currentIndex(self):
        return self.combo.currentIndex()

    def setCurrentIndex(self, idx):
        self.combo.setCurrentIndex(idx)


class SmartTranslator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("مترجم هوشمند | Smart translator")
        self.setGeometry(300, 200, 620, 520)
        self.setLayoutDirection(Qt.RightToLeft)

        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor("#f1f1f1"))
        self.setPalette(palette)

        font_family = "IRANSans"
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(22)

        label_style = f"color: #333; font-family: {font_family}; font-size: 12pt; margin-bottom: 6px;"

        label_from = QLabel("زبان مبدا: | Original language:")
        label_from.setStyleSheet(label_style)

        label_to = QLabel("زبان مقصد: | Destination language:")
        label_to.setStyleSheet(label_style)

        temp_translator = GoogleTranslator(source="auto", target="en")
        languages_dict = temp_translator.get_supported_languages(as_dict=True)
        languages_list = [name.capitalize() for name in languages_dict.keys()]

        self.from_lang = ComboWithArrow(languages_list)
        self.to_lang = ComboWithArrow(languages_list)

        self.from_lang.setCurrentText("Persian")
        self.to_lang.setCurrentText("English")

        lang_layout = QHBoxLayout()
        lang_layout.setSpacing(40)

        from_layout = QVBoxLayout()
        from_layout.addWidget(label_from)
        from_layout.addWidget(self.from_lang)

        to_layout = QVBoxLayout()
        to_layout.addWidget(label_to)
        to_layout.addWidget(self.to_lang)

        lang_layout.addLayout(from_layout)
        lang_layout.addLayout(to_layout)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("متن را وارد کنید... | Enter text...")
        self.input_text.setFont(QFont(font_family, 11))
        self.input_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #ccc;
                border-radius: 12px;
                background-color: white;
                font-family: IRANSans;
                font-size: 12pt;
                color: #222;
            }
        """)
        self.input_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.translate_btn = QPushButton("ترجمه | Translate")
        self.translate_btn.setFont(QFont(font_family, 13))
        self.translate_btn.setStyleSheet("""
            QPushButton {
                background-color: #0ea480;
                color: white;
                border-radius: 14px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #0cc191;
            }
            QPushButton:pressed {
                background-color: #0b7a5e;
            }
        """)
        self.translate_btn.clicked.connect(self.translate)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont(font_family, 11))
        self.output_text.setStyleSheet("""
            QTextEdit {
                padding: 12px;
                border: 1px solid #ddd;
                border-radius: 12px;
                background-color: white;
                font-family: IRANSans;
                font-size: 12pt;
                color: #333;
            }
        """)
        self.output_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout.addLayout(lang_layout)
        main_layout.addWidget(self.input_text)
        main_layout.addWidget(self.translate_btn)
        main_layout.addWidget(self.output_text)

        footer_label = QLabel("برنامه نویسی شده توسط سام افضلی | Programmed by Sam Afzali")
        footer_label.setStyleSheet("""
            color: #0ea480;
            font-family: IRANSans;
            font-size: 10pt;
        """)
        footer_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        footer_layout.addWidget(footer_label)

        main_layout.addLayout(footer_layout)

        self.setLayout(main_layout)

    def translate(self):
        source_lang = self.from_lang.currentText().lower()
        target_lang = self.to_lang.currentText().lower()
        text = self.input_text.toPlainText().strip()

        if not text:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "خطا | Error", "لطفاً متنی وارد کنید. | Please enter some text.")
            return

        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            result = translator.translate(text)
            self.output_text.setPlainText(result)
        except Exception as e:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "خطا | Error", f"مشکلی در ترجمه رخ داد: | There was a problem with the translation: \n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SmartTranslator()
    window.show()
    sys.exit(app.exec_())
