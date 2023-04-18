from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QPushButton, QScrollArea, QSizePolicy, QTableWidget, QAbstractItemView, QTabWidget,QFormLayout
from PyQt5.QtGui import QPixmap

class ImageViewer(QWidget):
    def __init__(self, model):
        super().__init__()
        self.setWindowTitle('EXIF Viewer')
        self.setMinimumSize(400, 400)
        self.setMaximumSize(600, 600)

        # Add a button to open an image file
        self.open_button = QPushButton('Open Image', self)
        self.rotate_button = QPushButton('Rotate', self)
        global num
        num = 0
        # Add a label to display the image
        self.image_label = QLabel(self)
        self.pixmap = QPixmap()
        self.image_label.setScaledContents(True)


        #set up exifTABLE
        self.exif_table = None
        self.exif_table = QTableWidget()
        self.exif_table.setColumnCount(2)
        
        # Graphic properties
        self.exif_table.setHorizontalHeaderLabels(('Property', 'Value'))  # Set header labels
        self.exif_table.verticalHeader().setVisible(False)  # Hide rows' header (unneeded)
        self.exif_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)  # Smooth vertical scrolling
        self.exif_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)  # Smooth horizontal scrolling

        # User should not be able to edit table cell values
        self.exif_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Add tabs
        tabwidget = QTabWidget()
        
        #openimage tabs
        openImage = QWidget(self)
        layout = QFormLayout()
        openImage.setLayout(layout)
        layout.addRow(self.open_button)
        layout.addRow(self.rotate_button)
        layout.addRow(self.image_label)

        tabwidget.addTab(openImage, 'OpenImage')

        #exif tabs
        exifData = QWidget(self)
        layout = QFormLayout()
        exifData.setLayout(layout)
        layout.addRow(self.exif_table)
        tabwidget.addTab(exifData, 'exif')

        # Set up the main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(tabwidget)
        
        
        self.setLayout(self.layout)
