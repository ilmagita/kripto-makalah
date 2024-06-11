from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import uic
from algorithms import signing
import sys

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('windows/sign_menu.ui', self)

        # init states
        self.signChoice.setChecked(True)
        self.verifyChoice.setChecked(False)
        self.verifyButton.hide()
        self.chooseSignatureButton.hide()

        self.filePath = ''
        self.fileType = ''
        self.fileContents = None
        self.signatureFilePath = ''

        self.priKeyFromFile = None
        self.pubKeyFromFile = None
        self.signatureFromFile = None

        # connection slots
        self.signChoice.clicked.connect(self.signChoiceClicked)
        self.verifyChoice.clicked.connect(self.verifyChoiceClicked)
        self.signButton.clicked.connect(self.signButtonClicked)
        self.verifyButton.clicked.connect(self.verifyButtonClicked)
        self.chooseFileButton.clicked.connect(self.chooseFileButtonClicked)
        self.privKeyButton.clicked.connect(self.privKeyButtonClicked)
        self.pubKeyButton.clicked.connect(self.pubKeyButtonClicked)
        self.chooseSignatureButton.clicked.connect(self.chooseSignatureButtonClicked)

    def signChoiceClicked(self):
        self.signChoice.setChecked(True)
        self.verifyChoice.setChecked(False)
        self.verifyButton.hide()
        self.signButton.show()
        self.fileToSignLabel.show()
        self.chooseFileButton.show()
        self.filePathLineEdit.show()
        self.chooseSignatureButton.hide()
        self.signatureText.setPlainText('')

    def verifyChoiceClicked(self):
        self.verifyChoice.setChecked(True)
        self.signChoice.setChecked(False)
        self.signButton.hide()
        self.verifyButton.show()
        self.chooseSignatureButton.show()
        self.signatureText.setPlainText('')

    def signButtonClicked(self):
        if self.priKeyFromFile is not None and self.pubKeyFromFile is not None:

            d = self.priKeyFromFile['privKey']['d']
            n = self.priKeyFromFile['privKey']['n']
            
            signature = signing.sign_file(self.filePath, d, n)
            self.signatureText.setPlainText(f"Signature saved in the same folder.")

            with open ('./signature/sign.txt', 'w') as signature_file:
                signature_file.write(str(signature))

    def verifyButtonClicked(self):
        e = self.pubKeyFromFile['pubKey']['e']
        n = self.pubKeyFromFile['pubKey']['n']

        with open(self.filePath, 'rb') as file:
            data = file.read()

        if signing.verify_signature(self.filePath, self.signatureFilePath, e, n):
            self.signatureText.setPlainText('Signature verified!')
        else:
            self.signatureText.setPlainText('Signature not verified!')

    def chooseFileButtonClicked(self):
        file_dialog = QFileDialog(self)

        file_path, _ = file_dialog.getOpenFileName(self, 'Open File to be Encrypted')

        if file_path:
            self.filePath = file_path
            self.filePathLineEdit.setText(self.filePath)

            file_dialog.reject()

    def chooseSignatureButtonClicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Text files (*.txt)")
        file_dialog.setDefaultSuffix("txt")
        file_dialog.setFileMode(QFileDialog.ExistingFile)

        signature_file_path, _ = file_dialog.getOpenFileName(self, 'Open Signature', filter="Text files (*.txt)")

        if signature_file_path:
            with open (signature_file_path, 'r') as signature_file:
                signature = signature_file.read()
                self.signatureFilePath = signature_file_path

            self.signatureText.setPlainText(f"""HASHED SIGNATURE BEGIN
                                                {signature}
                                                HASHED SIGNATURE END""")

    def privKeyButtonClicked(self):
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

    def pubKeyButtonClicked(self):
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())