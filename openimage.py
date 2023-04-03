import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Viewer')
        self.setMinimumSize(640, 480)

        # Add a button to open an image file
        self.open_button = QPushButton('Open Image', self)
        self.open_button.clicked.connect(self.open_image)

        # Add a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setScaledContents(True)

        # Set up the main layout
        self.setCentralWidget(self.image_label)
        self.statusBar().addPermanentWidget(self.open_button)

    def open_image(self):
        # Open a file dialog to choose an image file
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.jpg *.png *.jpeg *.bmp *.gif)", options=options)

        # Load the selected image and display it
        if file_name:
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
