from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('EXIF Viewer')
        self.setMinimumSize(1, 1)
        self.setMaximumSize(512, 512)

        # Add a button to open an image file
        self.open_button = QPushButton('Open Image', self)
        self.rotate_button = QPushButton('Rotate', self)
        global num
        num = 0
        # Add a label to display the image
        self.image_label = QLabel(self)
        self.pixmap = QPixmap()
        self.image_label.setScaledContents(True)

        # Add a label to display the EXIF data
        # scroll area widget - Labels will move inside this widget
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setMinimumSize(300, 100)

        self.exif_label = QLabel('No image opened.',  self.scroll_area)
        self.exif_label.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.exif_label.setMaximumHeight(200)

        # self.exif_label.setMinimumSize(580, 380)
        self.scroll_area.setWidget(self.exif_label)
        self.scroll_area.setWidgetResizable(True)

        # Set up the main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.scroll_area)
        self.layout.addWidget(self.rotate_button)
        self.setLayout(self.layout)
