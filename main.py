import sys

from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
                               QMessageBox, QProgressBar, QPushButton,
                               QVBoxLayout, QWidget)


class MainWindow(QMainWindow):
    def __init__(self, parent = None ):
        super().__init__(parent)
        self.cw = QWidget()
        self.v_layout = QVBoxLayout()
        self.setWindowTitle("Leitor de Mentes")

        self.setCentralWidget(self.cw)
        self.cw.setLayout(self.v_layout) 

        self.label = QLabel('Pense em um número de 1 a 10:')
        self.v_layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.v_layout.addWidget(self.display)


        self.button = QPushButton('Ler minha mente')
        self.v_layout.addWidget(self.button)
        self.button.clicked.connect(self._openNewWindow)

        self.adjustFixedSize()

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
    
    @Slot()
    def _openNewWindow(self):
        self.new_window = NewWindow(self)
        self.new_window.show()

    def closeNewWindow(self):
        self.new_window.close()

    def boxResult(self):
        displayText = self.display.text()
        self.box = QMessageBox()
        self.box.setText(f'você está pensando no número {displayText}')
        self.box.exec()

class NewWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle('Lendo sua mente')
        self.cw = QWidget()
        self.v_layout = QVBoxLayout()

        self.setCentralWidget(self.cw)
        self.cw.setLayout(self.v_layout)
        


        self.label = QLabel('1')
        self.v_layout.addWidget(self.label)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setText('Analisando ondas cerebrais...')

        self.progress_bar = QProgressBar()
        self.v_layout.addWidget(self.progress_bar)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateProgressBar)
        self.timer_interval = 35
        self.timer.start(self.timer_interval)
        

        
    def updateProgressBar(self):

        if self.progress_bar.value() == 25:
            self.label.clear()
            self.label.setText('Escaneando memórias...')

        if self.progress_bar.value() == 50:
            self.label.clear()
            self.label.setText('Calculando probabilidades...')
        
        if self.progress_bar.value() == 75:
            self.label.clear()
            self.label.setText('Decodificando pensamentos...')
        
        if self.progress_bar.value() < 100:
            self.progress_bar.setValue( self.progress_bar.value() + 1)
            return
        
        self.timer.stop()
        self.parent().closeNewWindow() #type: ignore
        self.parent().boxResult() #type: ignore




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()