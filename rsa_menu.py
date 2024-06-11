from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QApplication
from PyQt5 import uic
import sys
from ciphers import rsa
from algorithms import cryption

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/rsa_menu.ui', self)

        # init states
        self.encryptChoice.setChecked(True)
        self.decryptChoice.setChecked(False)
        self.decryptButton.hide()

        self.filePath = ''
        self.priKeyUploaded = False
        self.pubKeyUploaded = False

        # connection slots
        self.encryptChoice.clicked.connect(self.encryptChoiceClicked)
        self.decryptChoice.clicked.connect(self.decryptChoiceClicked)
        self.encryptButton.clicked.connect(self.encryptButtonClicked)
        self.decryptButton.clicked.connect(self.decryptButtonClicked)
        self.chooseFileButton.clicked.connect(self.chooseFileButtonClicked)
        self.generateKeyButton.clicked.connect(self.generateKeyButtonClicked)
        self.privKeyButton.clicked.connect(self.privKeyButtonClicked)
        self.pubKeyButton.clicked.connect(self.pubKeyButtonClicked)
        
    def encryptChoiceClicked(self):
        self.encryptChoice.setChecked(True)
        self.decryptChoice.setChecked(False)
        self.encryptButton.show()
        self.decryptButton.hide()

    def decryptChoiceClicked(self):
        self.encryptChoice.setChecked(False)
        self.decryptChoice.setChecked(True)
        self.encryptButton.hide()
        self.decryptButton.show()

    def encryptButtonClicked(self):
        if self.keyGenerated:
            e = self.keys['pubKey']['e']
            n = self.keys['pubKey']['n']
        elif self.priKeyUploaded and self.pubKeyUploaded:
            e = self.pubKeyFromFile['pubKey']['e']
            n = self.pubKeyFromFile['pubKey']['n']

        cryption.encrypt_file(self.filePath, e, n)
        message_box = QMessageBox()
        message_box.setText('File successfuly encrypted in the same folder.')

    def decryptButtonClicked(self):
        if self.keyGenerated:
            d = self.keys['privKey']['d']
            n = self.keys['privKey']['n']
        elif self.priKeyUploaded and self.pubKeyUploaded:
            d = self.priKeyFromFile['privKey']['d']
            n = self.priKeyFromFile['privKey']['n']
        
        cryption.decrypt_file(self.filePath, d, n)
        message_box = QMessageBox()
        message_box.setText('File successfuly decrypted in the same folder.')

    def generateKeyButtonClicked(self):
        dateOfBirth = int(f"{self.dateText.text():0>2}{self.monthText.text():0>2}{self.yearText.text():0>4}")
        keys = rsa.generate_rsa_key(dateOfBirth)
        self.keys = keys
        self.keyTextEdit.setPlainText(str(keys))
        self.keyGenerated = True
        self.priKeyUploaded = False
        self.pubKeyUploaded = False
        cryption.write_keys_to_files(keys)
        
    def chooseFileButtonClicked(self):
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, 'Open File to be Encrypted')

        if file_path:
            self.filePath = file_path
            self.filePathLineEdit.setText(self.filePath)

            file_dialog.reject()

    def privKeyButtonClicked(self):
        if (self.keyGenerated):
            self.keyTextEdit.setPlainText('')
            self.keyGenerated = False

        file_dialog = QFileDialog(self)
        pri_file_path, _ = file_dialog.getOpenFileName(self, 'Open Private Key')

        if pri_file_path:
            with open(pri_file_path, 'r') as file:
                content = file.read().strip()

            content = content[1:-1]
            d, n = map(int, content.split(','))

            priKeyFromFile = {
                'privKey': {
                    'd': d,
                    'n': n
                }
            }
            self.priKeyFromFile = priKeyFromFile
            self.keyTextEdit.appendPlainText(str(self.priKeyFromFile))
            self.priKeyUploaded = True
        
    def pubKeyButtonClicked(self):
        if (self.keyGenerated):
            self.keyTextEdit.setPlainText('')
            self.keyGenerated = False

        file_dialog = QFileDialog(self)
        pub_file_path, _ = file_dialog.getOpenFileName(self, 'Open Public Key')

        if pub_file_path:
            with open(pub_file_path, 'r') as file:
                content = file.read().strip()

            content = content[1:-1]
            e, n = map(int, content.split(','))

            pubKeyFromFile = {
                'pubKey': {
                    'e': e,
                    'n': n
                }
            }
            self.pubKeyFromFile = pubKeyFromFile
            self.keyTextEdit.appendPlainText(str(self.pubKeyFromFile))
            self.pubKeyUploaded = True
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())