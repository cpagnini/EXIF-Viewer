from PyQt5.QtWidgets import QAction,QToolBar,QMainWindow, QLabel, QVBoxLayout, QWidget, QTableWidget, QAbstractItemView, QTabWidget, QFormLayout
from PyQt5.QtGui import QPixmap, QIcon



class ImageViewer(QMainWindow):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.setWindowTitle('EXIF Viewer')
        self.setMinimumSize(400, 400)
        self.setMaximumSize(600, 600)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&Sticazzi')
        
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        self.openAction = QAction('&Open',self)
        self.openAction.setIcon(QIcon('open.png'))
        toolbar.addAction(self.openAction)

        self.rotateAction = QAction('&Rotate', self)
        self.rotateAction.setIcon(QIcon('rotate_right.png'))
        toolbar.addAction(self.rotateAction)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        lay = QVBoxLayout(self.central_widget)
        
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
        layout.addRow(self.image_label)

        tabwidget.addTab(openImage, 'Image')

        #exif tabs
        exifData = QWidget(self)
        layout = QFormLayout()
        exifData.setLayout(layout)
        layout.addRow(self.exif_table)
        tabwidget.addTab(exifData, 'Exif Infos')

        # Set up the main layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(tabwidget)
        
        lay.addWidget(tabwidget)
        
