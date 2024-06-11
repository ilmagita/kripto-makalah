from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QApplication
from PyQt5 import uic
import sys
from ciphers import rsa
from algorithms import cryption

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/sign_menu.ui', self)

        # init states
        self.signChoice.setChecked(True)
        self.verifyChoice.setChecked(False)
        self.verifyButton.hide()

        self.filePath = ''
        self.fileType = ''
        self.keys = None

        self.priKeyFromFile = None
        self.pubKeyFromFile = None

        self.keyGenerated = False

        # connection slots
        self.signChoice.clicked.connect(self.signChoiceClicked)
        self.verifyChoice.clicked.connect(self.verifyChoiceClicked)
        self.signButton.clicked.connect(self.signButtonClicked)
        self.verifyButton.clicked.connect(self.verifyButtonClicked)
        self.chooseFileButton.clicked.connect(self.chooseFileButtonClicked)
        self.privKeyButton.clicked.connect(self.privKeyButtonClicked)
        self.pubKeyButton.clicked.connect(self.pubKeyButtonClicked)