import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QPushButton, QComboBox, QStyledItemDelegate)
from PySide6.QtGui import QFont, QColor, QIcon
from PySide6.QtCore import Qt
from datetime import datetime

class CustomFontDelegate(QStyledItemDelegate):
    def __init__(self, font_size=14, text_color="black"):
        super().__init__()
        self.font_size = font_size
        self.text_color = QColor(text_color)

    def paint(self, painter, option, index):
        painter.save()  # Sauvegarde l'état actuel du painter

        # Configuration de la police
        font = painter.font()
        font.setPointSize(self.font_size)
        painter.setFont(font)

        # Configuration de la couleur
        painter.setPen(self.text_color)

        # Dessin du texte
        painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignVCenter, index.data())

        painter.restore()  # Restaure l'état original du painter

class DateSelector(QWidget):
    def __init__(self, label, min_value, max_value, initial_value, update_callback):
        super().__init__()
        self.label_text = label
        self.min_value = min_value
        self.max_value = max_value
        self.update_callback = update_callback
        self._is_updating = False

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(f"{label}")
        # Définition d'un style pour l'élément sélectionné


        self.label.setStyleSheet(f"font-size: 20px; color: #b6b7fe;")
        self.combo = QComboBox()

        delegate = CustomFontDelegate(font_size=14, text_color="#b6b7fe")
        self.combo.setItemDelegate(delegate)

        self.combo.setFixedSize(90,30)

        self.combo.setStyleSheet("""
            QComboBox {
        font-size: 14px; color: #55557f; background-color: #ced1ff; /* Taille pour l'élément sélectionné */
            }
        """)

##        self.combo.setStyleSheet(f"color: #55557f ;background-color: #ced1ff;")
        self.combo.addItems([str(i) for i in range(self.min_value, self.max_value + 1)])
        self.combo.setCurrentText(str(initial_value))
        self.combo.currentTextChanged.connect(self.on_select)

        layout.addWidget(self.label)
        layout.addWidget(self.combo)

    def on_select(self):
        if not self._is_updating:
            self.update_callback()

    def value(self):
        return int(self.combo.currentText())

    def update_range(self, min_value, max_value):
        self._is_updating = True
        current_value = self.combo.currentText()
        self.combo.clear()
        self.combo.addItems([str(i) for i in range(min_value, max_value + 1)])
        if current_value in [self.combo.itemText(i) for i in range(self.combo.count())]:
            self.combo.setCurrentText(current_value)
        else:
            self.combo.setCurrentText(str(self.max_value))
        self._is_updating = False

class DateCodeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DateCode")
        self.setWindowIcon(QIcon("DateCode.ico"))
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        self.setStyleSheet(f"background-color: #55557f;")

        date_selector_layout = QHBoxLayout()
        current_date = datetime.now()

        self.year_selector = DateSelector("Year", current_date.year - 5, current_date.year + 2, current_date.year, self.update_result)
        self.month_selector = DateSelector("Month", 1, 12, current_date.month, self.update_result)
        self.day_selector = DateSelector("Day", 1, 31, current_date.day, self.update_result)

        self.month_selector.combo.setFixedWidth(100)

        date_selector_layout.addWidget(self.day_selector)
        date_selector_layout.addWidget(self.month_selector)
        date_selector_layout.addWidget(self.year_selector)

        main_layout.addLayout(date_selector_layout)

        self.date_English_label = QLabel()
        self.date_English_label.setAlignment(Qt.AlignCenter)
        self.date_English_label.setStyleSheet("font-size: 20px; color: #00FF80;")

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size: 25px; color: #66FFCC;")

        main_layout.addWidget(self.date_English_label)
        main_layout.addWidget(self.result_label)

        self.update_result()

    def is_leap_year(self, year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def update_result(self):
        try:
            date = datetime(self.year_selector.value(), self.month_selector.value(), self.day_selector.value())

            year = date.year % 100  # Get last two digits of the year
            week_number = date.isocalendar()[1]

            self.date_English_label.setText(date.strftime("%A, %B %d, %Y"))
            date_code = f"{year:02d}{week_number:02d}"
            self.result_label.setText(f'DateCode:    {date_code}')

            if self.month_selector.value() == 2:
                max_day = 29 if self.is_leap_year(self.year_selector.value()) else 28
                self.day_selector.update_range(1, max_day)
            elif self.month_selector.value() in [4, 6, 9, 11]:
                self.day_selector.update_range(1, 30)
            else:
                self.day_selector.update_range(1, 31)

            if self.year_selector.value() == self.year_selector.max_value:
                self.year_selector.update_range(self.year_selector.min_value + 4, self.year_selector.max_value + 4)
                self.year_selector.min_value += 4
                self.year_selector.max_value += 4

            if self.year_selector.value() == self.year_selector.min_value:
                self.year_selector.update_range(self.year_selector.min_value - 3, self.year_selector.max_value - 3)
                self.year_selector.min_value -= 3
                self.year_selector.max_value -= 3

        except ValueError:
            self.day_selector.combo.setCurrentText(str(self.day_selector.value() -1))
            self.update_result()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DateCodeApp()
    window.show()
    sys.exit(app.exec_())