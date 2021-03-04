import sys,json,toml
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt,QDateTime
from subprocess import Popen

def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

class Window(QtWidgets.QMainWindow):
    try: BASE_DIR = Path(getattr(sys, "_MEIPASS"))
    except AttributeError: BASE_DIR = Path(__file__).parent 
    with open("config.json") as f:
        options = toml.load(f)
    if not options["twelve-hour"]:
        if options["seconds"]:
            fmt = "hh:mm:ss"
        else:
            fmt = "hh:mm"
    else:
        if options["seconds"]:
            fmt = "h:mm:ss                                  a"
        else:
            fmt = "h:mm                                     a"
    current_time = QDateTime.currentDateTime().toLocalTime().toString(fmt)

    def open_config(self):
        Popen("config.exe")
        sys.exit(0)
    def update_time(self):
        self.time.setText(QDateTime.currentDateTime().toLocalTime().toString(self.fmt))
        self.time.adjustSize()
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        width, height = int(self.options["font"]["size"] * 6.667), int(self.options["font"]["size"] * 3.333)
        print(width, height)
        self.setGeometry(400, 400, width, height)
        temp = self.BASE_DIR / "Monserrat.ttf"
        self.setFont(QtGui.QFont(temp.stem, self.options["font-size"]))
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.center()

        self.open_config_action = QtWidgets.QAction(self)
        self.open_config_action.triggered.connect(self.open_config)
        self.open_config_action.setText("Open Config")

        self.close_time_action = QtWidgets.QAction(self)
        self.close_time_action.triggered.connect(lambda: sys.exit(0))
        self.close_time_action.setText("Close")        

        self.ctx_menu = QtWidgets.QMenu(self)
        self.ctx_menu.setTitle("Time Widget")
        self.ctx_menu.addActions([self.open_config_action,self.close_time_action])

        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setContextMenu(self.ctx_menu)
        temp = self.BASE_DIR / "icon.png"
        self.tray_icon.setIcon(QtGui.QIcon(temp.stem))
        self.tray_icon.show()
        
        self.time = QtWidgets.QLabel(self)
        temp1 = hex_to_rgb(self.options["font"]["color"])
        print("QLabel{{ color: rgb({0}, {1}, {2}) }} ".format(temp1[0], temp1[1], temp1[2]))
        
        self.time.setStyleSheet("QLabel{{ color: rgb({0}, {1}, {2}) }} ".format(temp1[0], temp1[1], temp1[2]))
        self.time.setText(self.current_time)
        self.time.adjustSize()
        
        self.time_timer = QtCore.QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)
        
        self.old_pos = self.pos()
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