import sys,toml,re
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt,QDateTime

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

class Window(QtWidgets.QMainWindow):
    try: BASE_DIR = Path(getattr(sys, "_MEIPASS"))
    except AttributeError: BASE_DIR = Path(__file__).parent 
    with open("config.toml") as f:
        options = toml.load(f)
    
    def msg(self, title, description, icon = QtWidgets.QMessageBox.Information):
        msgbox = QtWidgets.QMessageBox(self)
        msgbox.setWindowTitle(title)
        msgbox.setText(description)
        msgbox.setIcon(icon)
        return msgbox


    def check_font_size(self):
        text = self.font_size_input.text()
        if not text.isspace() and text != "":
            if not text.isnumeric():
                self.font_size_input.setText(str(self.options["font"]["size"]))
    def save_config(self):
        with open("config.toml", "w") as f:
            config = {
                "seconds": self.seconds_input.isChecked(),
                "twelve-hour": self.twelve_hour.isChecked(),
                "font": {
                    "color": rgb_to_hex((self.font_color.red(), self.font_color.green(), self.font_color.blue())),
                    "size": int(self.font_size_input.text()),
                }
            }
            toml.dump(config, f)
            self.msg("Success!", "Successfully saved to config.toml!").exec_()
            sys.exit(0)

    def get_new_color(self):
        font = QtWidgets.QColorDialog(self).getColor(QtGui.QColor(self.options["font-color"]))
        if font.isValid():
            self.font_color = font
            self.font_color_img.fill(self.font_color)
            self.font_color_vis.setPixmap(self.font_color_img)
    def __init__(self):
        super().__init__()
    
        self.central_widget = QtWidgets.QWidget()               
        self.setCentralWidget(self.central_widget)

        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowTitle("Config for Time Widget")
        self.setGeometry(400, 400, 400, 200)
        temp = self.BASE_DIR / "Montserrat.ttf"
        self.setFont(QtGui.QFont(temp.stem, 12))
        
        self.font_color = QtGui.QColor(self.options["font"]["color"])

        self.title = QtWidgets.QLabel(self)
        self.title.setText("Config for Time Widget")
        self.title.setFont(QtGui.QFont(temp.stem, 15, 500))
        self.title.move(80, 5)
        self.title.adjustSize()

        self.font_size_text = QtWidgets.QLabel(self)
        self.font_size_text.setText("Font Size:")
        self.font_size_text.move(10, 40)

        self.font_size_input = QtWidgets.QLineEdit(self)
        self.font_size_input.setText(str(self.options["font"]["size"]))
        self.font_size_input.move(100, 40)
        self.font_size_input.setMaximumWidth(50)
        self.font_size_input.setMinimumWidth(25)
        self.font_size_input.textChanged.connect(self.check_font_size)

        # self.seconds_text = QtWidgets.QLabel(self)
        # self.seconds_text.setText("Show Seconds on Widget:")
        # self.seconds_text.move(10, 80)
        # self.seconds_text.adjustSize()

        self.seconds_input = QtWidgets.QCheckBox("Show Seconds on Widget", self)
        self.seconds_input.adjustSize()
        self.seconds_input.move(10, 105)
        self.seconds_input.setChecked(self.options["seconds"])

        self.font_color_text = QtWidgets.QLabel(self)
        self.font_color_text.setText("Font Color:")
        self.font_color_text.move(10, 70)

        self.choose_font_color = QtWidgets.QPushButton(self)
        self.choose_font_color.setText("Choose")
        self.choose_font_color.setFont(QtGui.QFont(temp.stem, 10))
        self.choose_font_color.adjustSize()
        self.choose_font_color.move(140, 75)
        self.choose_font_color.clicked.connect(self.get_new_color)

        self.font_color_img = QtGui.QPixmap(25, 25)
        self.font_color_img.fill(self.font_color)

        self.font_color_vis = QtWidgets.QLabel(self)
        self.font_color_vis.setPixmap(self.font_color_img)
        self.font_color_vis.adjustSize()
        self.font_color_vis.move(105, 75)

        self.twelve_hour = QtWidgets.QCheckBox("Twelve Hour Clock", self)
        self.twelve_hour.adjustSize()
        self.twelve_hour.setChecked(self.options["twelve-hour"])
        self.twelve_hour.move(10, 125)

        self.save = QtWidgets.QPushButton(self)
        self.save.setText("Save")
        self.save.move(100,155)
        self.save.adjustSize()
        self.save.clicked.connect(self.save_config)

        self.cancel = QtWidgets.QPushButton(self)
        self.cancel.setText("Cancel")
        self.cancel.move(200, 155)
        self.cancel.clicked.connect(lambda: sys.exit(0))

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QtCore.QPoint (event.globalPos() - self.old_pos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()
app = QtWidgets.QApplication(sys.argv[1:])
win = Window()
sys.exit(app.exec_())