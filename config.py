import sys,json,re
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt,QDateTime

class Window(QtWidgets.QMainWindow):
    try: BASE_DIR = Path(getattr(sys, "_MEIPASS"))
    except AttributeError: BASE_DIR = Path(__file__).parent 
    with open("config.json") as f:
        options = json.load(f)
    
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
                self.font_size_input.setText(str(self.options["font-size"]))
    def save_config(self):
        with open("config.json", "w") as f:
            config = {
                "font-size": int(self.font_size_input.text()),
                "seconds": self.seconds_input.isChecked()
            }
            json.dump(config, f, indent=4, sort_keys=True)
            self.msg("Success!", "Successfully saved to config.json!").exec_()
            sys.exit(0)
    def __init__(self):
        super().__init__()
    
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setWindowTitle("Config for Time Widget")
        self.setGeometry(400, 400, 400, 200)
        temp = self.BASE_DIR / "Montserrat.ttf"
        self.setFont(QtGui.QFont(temp.stem, 12))

        self.title = QtWidgets.QLabel(self)
        self.title.setAlignment(Qt.AlignHCenter)
        self.title.setText("Config for Time Widget")
        self.title.setFont(QtGui.QFont(temp.stem, 15, 500))
        self.title.move(80, 5)
        self.title.adjustSize()

        self.font_size_text = QtWidgets.QLabel(self)
        self.font_size_text.setText("Font Size:")
        self.font_size_text.move(10, 50)

        self.font_size_input = QtWidgets.QLineEdit(self)
        self.font_size_input.setText(str(self.options["font-size"]))
        self.font_size_input.move(100, 50)
        self.font_size_input.setMaximumWidth(50)
        self.font_size_input.setMinimumWidth(25)
        self.font_size_input.textChanged.connect(self.check_font_size)

        self.seconds_text = QtWidgets.QLabel(self)
        self.seconds_text.setText("Show Seconds on Widget:")
        self.seconds_text.move(10, 80)
        self.seconds_text.adjustSize()

        self.seconds_input = QtWidgets.QCheckBox(self)
        self.seconds_input.move(230, 78)
        self.seconds_input.setChecked(self.options["seconds"])

        self.save = QtWidgets.QPushButton(self)
        self.save.setText("Save")
        self.save.move(100,150)
        self.save.adjustSize()
        self.save.clicked.connect(self.save_config)

        self.cancel = QtWidgets.QPushButton(self)
        self.cancel.setText("Cancel")
        self.cancel.move(200, 150)
        self.cancel.clicked.connect(lambda: sys.exit(0))

        self.show()

app = QtWidgets.QApplication(sys.argv[1:])
win = Window()
sys.exit(app.exec_())